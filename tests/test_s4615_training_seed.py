import hashlib
import unittest
from pathlib import Path

import yaml

from src.provisioning.phase5 import (
    ALLOWED_SEED_PROVENANCE,
    S4615_SEED_PATH,
    EvidenceBackend,
    Phase5ProvisioningEngine,
    load_seed,
)


ROOT = Path(__file__).resolve().parents[1]


class MissingBackend:
    writable = False

    def lookup(self, operation, target):
        return "MISSING"

    def provision(self, operation, target, values):
        raise AssertionError("seed dry-run must not write")

    def readback(self, operation, target):
        raise AssertionError("seed dry-run must not read back a write")


class S4615TrainingSeedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = yaml.safe_load(S4615_SEED_PATH.read_text(encoding="utf-8"))
        cls.decisions = load_seed()

    def test_seed_identity_and_default_mode(self):
        self.assertEqual("S4615_CONTROLLED_MINIMAL_TRAINING_SEED", self.raw["seed_id"])
        self.assertEqual("DRY_RUN_DEFAULT", self.raw["mode"])
        self.assertTrue(self.raw["canonical_immutable"])

    def test_every_non_book_value_has_explicit_allowed_provenance(self):
        for operation in self.raw["operations"].values():
            for contract in operation["fields"].values():
                self.assertIn(contract["provenance"], ALLOWED_SEED_PROVENANCE)
        for contract in self.raw["book_process"].values():
            self.assertEqual("BOOK_CONFIRMED", contract["provenance"])

    def test_exact_ids_and_book_values_are_preserved(self):
        operations = self.raw["operations"]
        self.assertEqual("1010", operations["COMPANY_CODE_1010"]["target"]["company_code"])
        self.assertEqual("BE01", self.decisions["COMPANY_CODE_1010"]["technical_template"])
        self.assertEqual("CABE", self.decisions["COMPANY_CODE_1010"]["chart_of_accounts"])
        self.assertEqual("C615-D00", operations["CUSTOMER_C615_D00"]["target"]["partner_id"])
        self.assertEqual("CFR", self.decisions["CUSTOMER_C615_D00"]["incoterms"])
        self.assertEqual("00", self.decisions["CUSTOMER_C615_D00"]["incoterms_location"])
        self.assertEqual("P615-400", operations["PRODUCT_P615_400"]["target"]["material_id"])
        self.assertEqual("PC", self.decisions["PRODUCT_P615_400"]["base_unit"])
        self.assertEqual("1710", self.decisions["SALES_ORGANIZATION_1010"]["technical_template"])
        self.assertEqual("17100002", self.decisions["CUSTOMER_C615_D00"]["technical_template"])
        self.assertEqual("FG228", self.decisions["PRODUCT_P615_400"]["technical_template"])

    def test_template_policies_forbid_identity_copy(self):
        customer = self.raw["operations"]["CUSTOMER_C615_D00"]["template_policy"]
        product = self.raw["operations"]["PRODUCT_P615_400"]["template_policy"]
        self.assertEqual("17100002", customer["template_id"])
        self.assertTrue(customer["identity_copy_forbidden"])
        self.assertTrue(customer["organizational_id_copy_forbidden"])
        self.assertEqual("FG228", product["template_id"])
        self.assertTrue(product["identity_copy_forbidden"])

    def test_optional_sales_org_fields_are_blank_and_nonblocking(self):
        decision = self.decisions["SALES_ORGANIZATION_1010"]
        for field in (
            "intercompany_customer", "purchasing_organization", "purchasing_group",
            "purchasing_order_type", "rebate_active", "address_text",
            "letter_header_text", "footer_text", "sales_org_calendar",
            "greeting_text", "standard_text",
        ):
            self.assertIsNone(decision[field])
        result = Phase5ProvisioningEngine(
            backend=MissingBackend(), decisions=self.decisions
        )._ensure("SALES_ORGANIZATION_1010")
        self.assertEqual("WOULD_PROVISION", result.status)

    def test_explicit_company_template_strategy_is_accepted(self):
        decision = dict(self.decisions["COMPANY_CODE_1010"])
        result = Phase5ProvisioningEngine(
            backend=MissingBackend(), decisions={"COMPANY_CODE_1010": decision}
        ).ensure_company_code()
        self.assertEqual("WOULD_PROVISION", result.status)

    def test_dry_run_defers_assignment_reads_and_plans_dependents(self):
        result = Phase5ProvisioningEngine(
            backend=EvidenceBackend(), decisions=self.decisions
        ).plan(include_book_data=True)
        self.assertEqual("READY", result["status"])
        self.assertEqual([], result["blockers"])
        statuses = {item["operation"]: item["status"] for item in result["results"]}
        for operation in (
            "SALES_ORG_1010_TO_COMPANY_CODE_1010",
            "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
            "DIVISION_00_TO_SALES_ORG_1010",
        ):
            self.assertEqual("DEFERRED_READ_CHECK", statuses[operation])
        self.assertEqual(
            "WOULD_PROVISION_AFTER_COMMON_ENV", statuses["CUSTOMER_C615_D00"]
        )
        self.assertEqual(
            "WOULD_PROVISION_AFTER_COMMON_ENV", statuses["PRODUCT_P615_400"]
        )

    def test_canonical_dataset_is_not_modified(self):
        canonical = ROOT / "data/validated/canonical_objects.json"
        before = hashlib.sha256(canonical.read_bytes()).hexdigest()
        load_seed()
        after = hashlib.sha256(canonical.read_bytes()).hexdigest()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
