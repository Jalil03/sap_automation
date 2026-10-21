import copy
import io
import unittest
from contextlib import redirect_stdout

from src.provisioning.s4615_implementation import (
    OPERATION_ORDER, AuditEvidenceBackend, build_dry_run, load_contract,
    target_fingerprint, validate_write_approval,
)
from scripts.run_s4615_implementation import main


class S4615ImplementationTests(unittest.TestCase):
    def test_order_and_audit_boundaries_are_explicit(self):
        contract = load_contract()
        self.assertEqual(OPERATION_ORDER, tuple(op["id"] for op in contract["operations"]))
        self.assertEqual("API_PLANT_SRV:LOOKUP_ONLY", contract["operations"][0]["preferred_interface"])
        self.assertEqual("UNPROVEN_PRODUCT_CREATE", contract["operations"][-1]["write_route"])
        self.assertTrue(all(op["write_route"].startswith("UNPROVEN") for op in contract["operations"]))

    def test_default_plan_is_deterministic_blocked_and_offline(self):
        first = build_dry_run()
        self.assertEqual(first, build_dry_run())
        self.assertEqual("BLOCKED", first["status"])
        self.assertEqual((0, 0), (first["sap_calls"], first["sap_writes"]))
        self.assertEqual(OPERATION_ORDER, tuple(step["operation"] for step in first["steps"]))
        self.assertTrue(all(step["status"] == "BLOCKED" for step in first["steps"]))
        self.assertEqual("MISSING", first["steps"][0]["before_state"])
        self.assertEqual("UNKNOWN", first["steps"][-1]["before_state"])
        self.assertIn("plant", [b["detail"] for b in first["steps"][0]["blockers"]
                      if b["code"] == "MISSING_DECISION"])

    def test_missing_plant_blocks_dependent_assignments(self):
        result = build_dry_run()
        for step in result["steps"][1:4]:
            self.assertTrue(step["depends_on"])
            self.assertIn("APPROVAL_REQUIRED", [b["code"] for b in step["blockers"]])
            self.assertIn("WRITE_CONTRACT_UNPROVEN", [b["code"] for b in step["blockers"]])
        root, customer, product = result["steps"][4:]
        self.assertEqual([], root["depends_on"])
        self.assertEqual(["S4615_CUSTOMER_BP_ROOT"], customer["depends_on"])
        self.assertNotIn("S4615_OVL2_DETERMINATION", customer["depends_on"])
        self.assertNotIn("DEPENDENCY_BLOCKED", [b["code"] for b in root["blockers"]])
        self.assertEqual(["S4615_TRAINING_PLANT"], product["depends_on"])
        self.assertEqual({"DATA_READY": True, "WRITE_ROUTE_READY": False,
                          "EXECUTION_AUTHORIZED": False}, root["readiness"])

    def test_forbidden_1710_and_protected_material_cannot_be_selected(self):
        for decisions in (
            {"S4615_TRAINING_PLANT": {"plant": "1710"}},
            {"S4615_PRODUCT_P101": {"logical_id": "10000287"}},
            {"S4615_TRAINING_PLANT": {"material_ledger": "X"}},
        ):
            with self.subTest(decisions=decisions), self.assertRaises(ValueError):
                build_dry_run(decisions=decisions)

    def test_approved_plant_propagates_without_overriding_fixed_org_values(self):
        result = build_dry_run(decisions={"S4615_TRAINING_PLANT": {"plant": "P101"}})
        self.assertEqual("P101", result["steps"][0]["target"]["plant"])
        self.assertEqual("P101", result["steps"][1]["target"]["plant"])
        self.assertEqual("P101", result["steps"][2]["target"]["plant"])
        self.assertEqual("P101", result["steps"][3]["target"]["plant"])
        with self.assertRaises(ValueError):
            build_dry_run(decisions={"S4615_TRAINING_PLANT": {"plant": "P101"},
                                     "S4615_SALES_CHANNEL_PLANT": {"plant": "P102"}})
        with self.assertRaises(ValueError):
            build_dry_run(decisions={"S4615_TRAINING_PLANT": {"company_code": "1710"}})

    def test_no_backend_write_route_exists(self):
        backend = AuditEvidenceBackend(load_contract()["operations"])
        self.assertFalse(backend.writable)
        with self.assertRaises(RuntimeError):
            backend.provision(OPERATION_ORDER[0], {}, {})
        with self.assertRaises(ValueError):
            backend.lookup("UNRELATED", {})

    def test_approval_is_exact_and_still_does_not_enable_write(self):
        op = copy.deepcopy(load_contract()["operations"][0])
        approval = {
            "system": "A4H", "client": "600", "user": "ABDELJ",
            "operation": op["id"], "allow_write": True,
            "approved_by": "FI_MM_OWNER", "authorization_evidence": "SCOPED_APPROVAL",
            "approval_scopes": [op["required_approval"]],
            "target_fingerprint": target_fingerprint(op["id"], op["target"], op["values"]),
        }
        validate_write_approval(op, approval)
        for key, wrong in (("client", "100"), ("user", "OTHER"),
                           ("target_fingerprint", "wrong"), ("approval_scopes", [])):
            changed = {**approval, key: wrong}
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_write_approval(op, changed)

    def test_su01d_profiles_are_evidence_not_business_approval(self):
        op = load_contract()["operations"][4]
        evidence = op["sap_authorization_evidence"]
        self.assertEqual("USER_REPORTED_SU01D_PROFILES", evidence["source"])
        self.assertEqual(["SAP_ALL", "SAP_SYSTEM"], evidence["profiles"])
        self.assertFalse(evidence["api_post_success_proven"])
        self.assertIsNone(evidence["customer_master_owner_approval"])
        root = build_dry_run()["steps"][4]
        self.assertTrue(root["first_write_readiness"]["SAP_AUTHORIZATION_PROFILE_EVIDENCED"])
        self.assertFalse(root["first_write_readiness"]["CUSTOMER_MASTER_OWNER_APPROVED"])
        self.assertFalse(root["first_write_readiness"]["API_POST_SUCCESS_PROVEN"])
        self.assertFalse(root["first_write_readiness"]["eligible_for_post"])
        self.assertEqual("CUSTOMER_MASTER_OWNER_APPROVAL", root["first_write_readiness"]["missing_gate"])
        with self.assertRaises(ValueError):
            validate_write_approval(op, {"authorization_evidence": evidence})

    def test_execute_without_approvals_is_blocked_before_sap(self):
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(["--execute"])
        self.assertEqual(2, exit_code)
        self.assertIn('"sap_writes": 0', output.getvalue())
        self.assertIn("requires explicit scoped approvals", output.getvalue())


if __name__ == "__main__":
    unittest.main()
