import hashlib
import json
import subprocess
import unittest
from collections import Counter
from pathlib import Path

from src.validation.jsonschema import validate_object

ROOT = Path(__file__).resolve().parents[1]
EXTRACTED = ROOT / "data/extracted/full/S4615/objects.json"
NORMALIZED = ROOT / "data/normalized/full/S4615/objects.json"
PRIOR = {course: ROOT / f"data/normalized/full/{course}/objects.json"
         for course in ("S4600", "S4610")}
ARTIFACTS = [EXTRACTED, NORMALIZED,
    ROOT / "metadata/lineage/full/S4615/lineage.json",
    ROOT / "metadata/lineage/full/S4615/section_inventory.json",
    ROOT / "metadata/lineage/full/S4615/cross_document_checks.json",
    ROOT / "metadata/dependencies/full/S4615/dependency_graph.json",
    ROOT / "metadata/confidence/full/S4615/confidence.json",
    ROOT / "metadata/confidence/full/S4615/extraction_summary.json"]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def strings(value, path="data"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


class S4615FullExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extracted = load(EXTRACTED)["objects"]
        cls.normalized = load(NORMALIZED)["objects"]
        cls.by_id = {item["object_id"]: item for item in cls.normalized}

    def test_stable_inventory(self):
        expected = {"ACCOUNT_DETERMINATION": 1, "BILLING": 24, "COMPANY_CODE": 1,
                    "COPY_CONTROL": 2, "OUTBOUND_DELIVERY": 8,
                    "PAYMENT_REFERENCE": 1, "SALES_ORDER": 11}
        self.assertEqual(len(self.normalized), 48)
        self.assertEqual(Counter(item["object_type"] for item in self.normalized), expected)
        self.assertEqual(len(self.by_id), 48)

    def test_schema_validation_and_lifecycle(self):
        for item in self.normalized + self.extracted:
            self.assertEqual(validate_object(ROOT, item), [], item["object_id"])
        self.assertTrue(all(item["lifecycle_status"] == "VALIDATED" for item in self.normalized))
        self.assertTrue(all(item["lifecycle_status"] == "EXTRACTED" for item in self.extracted))

    def test_provenance_and_exercise_solution_dedup(self):
        for item in self.normalized:
            for source in item["provenance"]:
                self.assertEqual(source["course_code"], "S4615")
                self.assertEqual(source["source_file"], "S4615_FR_Col12_ILT_FV_Inst_A4.pdf")
                self.assertTrue(1 <= source["page"] <= 263)
                self.assertTrue(source["source_term"])
            if "_DEMO_" not in item["object_id"]:
                self.assertTrue(any(s["section_type"] == "EXERCISE" for s in item["provenance"]), item["object_id"])
                self.assertTrue(any(s["section_type"] == "SOLUTION" for s in item["provenance"]), item["object_id"])
        inventory = load(ROOT / "metadata/lineage/full/S4615/section_inventory.json")["sections"]
        self.assertEqual(len(inventory), 13)
        self.assertEqual(next(row for row in inventory if row["exercise"] == 8)["decision"], "SKIP")

    def test_placeholder_preservation_and_readiness(self):
        for item in self.normalized:
            placeholders = {entry["field_path"]: entry for entry in item["placeholders"]}
            for path, value in strings(item["data"]):
                if "##" in value:
                    self.assertIn(path, placeholders, (item["object_id"], path))
                    self.assertIsNone(placeholders[path]["resolved"])
                    self.assertEqual(item["readiness_status"], "BLOCKED")
        self.assertEqual(Counter(item["readiness_status"] for item in self.normalized),
                         {"BLOCKED": 43, "READY": 5})

    def test_billing_subtypes_and_accounting_metadata(self):
        billings = [item for item in self.normalized if item["object_type"] == "BILLING"]
        subtypes = {item["data"]["billing_subtype"] for item in billings}
        self.assertTrue({"STANDARD", "CASH_SALE", "PRO_FORMA_INVOICE", "CREDIT_MEMO",
                         "INVOICE_LIST", "PERIODIC", "DOWN_PAYMENT_REQUEST",
                         "PARTIAL_BILLING", "INSTALLMENT_INVOICE"} <= subtypes)
        self.assertTrue(all("fi_co_dependencies" in item["data"] for item in billings))
        pro_forma = self.by_id["S4615_CH4_EX5_BILLING_PRO_FORMA"]
        self.assertEqual(pro_forma["data"]["accounting_status"], "NOT_APPLICABLE_PRO_FORMA")
        self.assertEqual(pro_forma["data"]["fi_co_dependencies"][0]["system"], "FI")

    def test_invoice_list_billing_plan_down_payment_and_installments(self):
        invoice_list = self.by_id["S4615_CH7_DEMO_INVOICE_LIST_BILLING_INVOICE_LIST"]
        self.assertEqual(invoice_list["data"]["billing_subtype"], "INVOICE_LIST")
        self.assertEqual(len([d for d in invoice_list["dependencies"] if d["relation"] == "CONTAINS"]), 2)
        periodic = self.by_id["S4615_CH8_EX10_BILLING_PERIODIC_FIRST_PERIOD"]
        self.assertEqual(periodic["data"]["billing_plan"]["plan_semantics"], "PERIODIC")
        partial = self.by_id["S4615_CH8_EX11_BILLING_FIRST_PARTIAL"]
        self.assertEqual(partial["data"]["down_payments"][0]["condition_type"], "AZWR")
        installment = self.by_id["S4615_CH8_DEMO_INSTALLMENT_PAYMENTS_BILLING_INSTALLMENT"]
        self.assertEqual(installment["data"]["payment_terms"], "R001")
        self.assertEqual(len(installment["data"]["installment_payments"]), 1)

    def test_account_determination_and_copy_control(self):
        account = self.by_id["S4615_CH9_EX12_ACCOUNT_DETERMINATION_AFFILIATED_REVENUE"]
        self.assertEqual(account["data"]["condition_table"], "001")
        self.assertEqual(account["data"]["customer_account_assignment_group"], "80+##")
        self.assertEqual(account["data"]["general_ledger_account"], "49000000")
        copy = self.by_id["S4615_CH3_EX3_COPY_CONTROL_FAIR_BILLING"]
        self.assertEqual(copy["data"]["pricing_type"], "H")
        self.assertEqual(copy["data"]["data_transfer_routine"], "3")
        self.assertEqual(copy["data"]["reference_number_rule"], "B")
        self.assertEqual(copy["data"]["assignment_number_rule"], "E")

    def test_dependency_integrity_and_relative_values(self):
        for item in self.normalized:
            for dep in item["dependencies"]:
                if dep["status"] == "RESOLVED":
                    self.assertIn(dep["target_id"], self.by_id, (item["object_id"], dep))
                    self.assertEqual(self.by_id[dep["target_id"]]["object_type"], dep["target_type"])
                else:
                    self.assertIsNone(dep["target_id"])
        app_order = self.by_id["S4615_CH6_EX7_SALES_ORDER_FIORI_APP_FINAL"]
        self.assertEqual(app_order["data"]["requested_delivery_date"]["raw"], "dans une semaine")
        self.assertEqual(app_order["data"]["requested_delivery_date"]["offset"], "P1W")

    def test_cross_document_immutability_and_return_issue(self):
        checks = load(ROOT / "metadata/lineage/full/S4615/cross_document_checks.json")
        self.assertEqual(checks["return_delivery_issue"]["status"], "UNRESOLVED_CARRIED_FORWARD")
        self.assertIsNone(checks["return_delivery_issue"]["s4615_evidence"])
        for course, path in PRIOR.items():
            self.assertEqual(checks["prior_stage_normalized_sha256"][course],
                             hashlib.sha256(path.read_bytes()).hexdigest())
        # A later explicitly authorized Phase 1 consolidation may publish globally;
        # Stage 3 itself must never publish a course-specific validated dataset.
        self.assertFalse((ROOT / "data/validated/S4615").exists())

    def test_deterministic_rerun_and_prior_stage_immutability(self):
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in ARTIFACTS}
        prior_before = {course: hashlib.sha256(path.read_bytes()).hexdigest()
                        for course, path in PRIOR.items()}
        completed = subprocess.run([str(ROOT / ".venv/Scripts/python.exe"),
                                    str(ROOT / "scripts/extract_s4615.py")], cwd=ROOT,
                                   capture_output=True, text=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(before, {path: hashlib.sha256(path.read_bytes()).hexdigest()
                                  for path in ARTIFACTS})
        self.assertEqual(prior_before, {course: hashlib.sha256(path.read_bytes()).hexdigest()
                                        for course, path in PRIOR.items()})


if __name__ == "__main__":
    unittest.main()
