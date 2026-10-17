"""Build the offline S4615 user-00 blocker-resolution contract.

The primary source is the compact provisioning facts file.  No PDF, SAP
connection, HTTP request, GUI action, or write is performed by this builder.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FACTS_PATH = ROOT / "data/books/S4615/S4615_provisioning_facts.md"
PHASE4_REQUIREMENTS = ROOT / "data/requirements/training_environment_requirements.json"
PHASE5_PREPARE = ROOT / "data/provisioning/phase5_prepare_1010.json"
OUTPUT_JSON = ROOT / "data/provisioning/s4615_user00_blocker_resolution.json"
OUTPUT_REPORT = ROOT / "reports/s4615_user00_blocker_resolution.md"

ALLOWED_CLASSIFICATIONS = {
    "BOOK_CONFIRMED",
    "SAP_CONFIRMED",
    "DERIVED_FROM_TRAINING_FAMILY",
    "UNKNOWN",
}

REQUIRED_CUSTOMER_SOURCE_FIELDS = (
    "grouping", "name", "roles", "addresses", "reconciliation_account",
    "payment_terms", "currency", "shipping_conditions", "delivering_plant",
    "incoterms", "incoterms_location", "account_assignment_group",
    "customer_pricing_procedure", "tax_classifications", "partner_functions",
)

REQUIRED_PRODUCT_SOURCE_FIELDS = (
    "description", "material_type", "industry_sector", "base_unit", "plants",
    "delivering_plant", "item_category_group", "tax_classification",
    "availability_check", "alternative_units",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fact(field: str, value: Any, classification: str, evidence: str) -> dict[str, Any]:
    if classification not in ALLOWED_CLASSIFICATIONS:
        raise ValueError(f"Unsupported classification {classification}")
    return {
        "field": field,
        "value": value,
        "classification": classification,
        "evidence": evidence,
    }


def build_resolution() -> dict[str, Any]:
    facts_text = FACTS_PATH.read_text(encoding="utf-8")
    required_markers = (
        "Company Code: `1010`",
        "Sales Organization: `1010`",
        "Sold-To Party | `C615-D00`",
        "Material | `P615-400`",
        "Customer Reference | `00S4615-BV`",
    )
    missing_markers = [marker for marker in required_markers if marker not in facts_text]
    if missing_markers:
        raise ValueError(f"Primary S4615 facts source is incomplete: {missing_markers}")

    book = "data/books/S4615/S4615_provisioning_facts.md"
    phase4 = "data/requirements/training_environment_requirements.json"
    phase5 = "data/provisioning/phase5_prepare_1010.json"
    facts = {
        "source_identity": [
            _fact("course", "S4615 - Facturation dans SAP S/4HANA Sales", "BOOK_CONFIRMED", book),
            _fact("course_version", "12", "BOOK_CONFIRMED", book),
            _fact("training_user_template", "S4615-##", "BOOK_CONFIRMED", book),
            _fact("training_user", "S4615-00", "DERIVED_FROM_TRAINING_FAMILY", book),
        ],
        "common_environment": [
            _fact("company_code", "1010", "BOOK_CONFIRMED", book),
            _fact("sales_organization", "1010", "BOOK_CONFIRMED", book),
            _fact("sales_org_company_assignment", "1010->1010", "BOOK_CONFIRMED", book),
            _fact("distribution_channel", "10", "BOOK_CONFIRMED", book),
            _fact("sales_division", "00", "BOOK_CONFIRMED", book),
            _fact("sales_area", "1010/10/00", "BOOK_CONFIRMED", book),
            _fact("shipping_point", "1010", "BOOK_CONFIRMED", book),
            _fact("company_code_live_state", "MISSING", "SAP_CONFIRMED", phase5),
            _fact("sales_organization_live_state", "MISSING", "SAP_CONFIRMED", phase4),
            _fact("distribution_channel_live_state", "EXISTS", "SAP_CONFIRMED", phase4),
            _fact("sales_division_live_state", "EXISTS", "SAP_CONFIRMED", phase4),
            _fact("sales_org_company_assignment_live_state", "UNKNOWN", "UNKNOWN", phase5),
            _fact("distribution_channel_assignment_live_state", "UNKNOWN", "UNKNOWN", phase5),
            _fact("division_assignment_live_state", "UNKNOWN", "UNKNOWN", phase5),
            _fact("company_code_name", None, "UNKNOWN", book),
            _fact("company_code_city", None, "UNKNOWN", book),
            _fact("company_code_country", None, "UNKNOWN", book),
            _fact("company_code_currency", None, "UNKNOWN", book),
            _fact("company_code_language", None, "UNKNOWN", book),
            _fact("company_code_chart_of_accounts", "INT", "BOOK_CONFIRMED", book),
            _fact("sales_organization_description", None, "UNKNOWN", book),
            _fact("sales_organization_statistics_currency", None, "UNKNOWN", book),
        ],
        "customer": [
            _fact("customer_template", "C615-D##", "BOOK_CONFIRMED", book),
            _fact("customer", "C615-D00", "DERIVED_FROM_TRAINING_FAMILY", book),
            _fact("customer_live_state", "MISSING", "SAP_CONFIRMED", phase4),
            _fact("customer_sales_area", "1010/10/00", "BOOK_CONFIRMED", book),
            _fact("incoterms", "CFR", "BOOK_CONFIRMED", book),
            _fact("incoterms_location_template", "##", "BOOK_CONFIRMED", book),
            _fact("incoterms_location", "00", "DERIVED_FROM_TRAINING_FAMILY", book),
            _fact("customer_name", None, "UNKNOWN", book),
            _fact("customer_address", None, "UNKNOWN", book),
            _fact("bp_grouping", None, "UNKNOWN", book),
            _fact("customer_roles", None, "UNKNOWN", book),
            _fact("reconciliation_account", None, "UNKNOWN", book),
            _fact("payment_terms", None, "UNKNOWN", book),
            _fact("customer_currency", None, "UNKNOWN", book),
            _fact("shipping_conditions", None, "UNKNOWN", book),
            _fact("delivering_plant", None, "UNKNOWN", book),
            _fact("account_assignment_group", None, "UNKNOWN", book),
            _fact("customer_pricing_procedure", None, "UNKNOWN", book),
            _fact("tax_classifications", None, "UNKNOWN", book),
            _fact("partner_functions", None, "UNKNOWN", book),
        ],
        "product": [
            _fact("product_template", "P615-4##", "BOOK_CONFIRMED", book),
            _fact("product", "P615-400", "DERIVED_FROM_TRAINING_FAMILY", book),
            _fact("product_live_state", "MISSING", "SAP_CONFIRMED", phase4),
            _fact("ordered_quantity", 1, "BOOK_CONFIRMED", book),
            _fact("order_unit", "PC", "BOOK_CONFIRMED", book),
            _fact("semantic_product_kind", "bicycle / stock product", "BOOK_CONFIRMED", book),
            _fact("product_description", None, "UNKNOWN", book),
            _fact("material_type", None, "UNKNOWN", book),
            _fact("industry_sector", None, "UNKNOWN", book),
            _fact("base_unit", None, "UNKNOWN", book),
            _fact("plants", None, "UNKNOWN", book),
            _fact("product_delivering_plant", None, "UNKNOWN", book),
            _fact("item_category_group", None, "UNKNOWN", book),
            _fact("product_tax_classification", None, "UNKNOWN", book),
            _fact("availability_check", None, "UNKNOWN", book),
            _fact("alternative_unit_conversions", None, "UNKNOWN", book),
        ],
        "golden_transaction": [
            _fact("sales_order_type", "BV", "BOOK_CONFIRMED", book),
            _fact("customer_reference_template", "##S4615-BV", "BOOK_CONFIRMED", book),
            _fact("customer_reference", "00S4615-BV", "DERIVED_FROM_TRAINING_FAMILY", book),
            _fact("billing_type", "BV", "BOOK_CONFIRMED", book),
            _fact("cancellation_billing_type", "SV", "BOOK_CONFIRMED", book),
            _fact("output_type", "RD03", "BOOK_CONFIRMED", book),
            _fact("delivery_created_on_cash_sale_save", True, "BOOK_CONFIRMED", book),
            _fact("pgi_required_before_real_billing", True, "BOOK_CONFIRMED", book),
            _fact("billing_reference", "sales_order", "BOOK_CONFIRMED", book),
            _fact("billing_pricing", "NO_NEW_PRICING_DETERMINATION", "BOOK_CONFIRMED", book),
            _fact("accounting_readback", "cash + domestic revenue + output VAT", "BOOK_CONFIRMED", book),
        ],
        "additional_seed_facts": [
            _fact("precreated_training_data_mechanism", "CATT import", "BOOK_CONFIRMED", book),
            _fact("customer_families", ["C615-A##", "C615-B##", "C615-C##", "C615-D##", "C615-F##"], "BOOK_CONFIRMED", book),
            _fact("product_families", ["P615-1##", "P615-2##", "P615-4##", "P615-5##", "P615-6##"], "BOOK_CONFIRMED", book),
            _fact("customer_freight_condition_type", "KF00", "BOOK_CONFIRMED", book),
            _fact("customer_freight_sales_area", "1010/10/00", "BOOK_CONFIRMED", book),
            _fact("customer_freight_incoterms", "CFR/##", "BOOK_CONFIRMED", book),
            _fact("customer_freight_rate", "10 EUR per 1 KG", "BOOK_CONFIRMED", book),
            _fact("customer_freight_required_by_golden_flow", None, "UNKNOWN", book),
            _fact("standard_item_category", "TAN", "BOOK_CONFIRMED", book),
            _fact("billing_types", ["F2", "F5", "F8", "G2", "BV", "SV"], "BOOK_CONFIRMED", book),
            _fact("pricing_condition_types", ["PR00", "KF00"], "BOOK_CONFIRMED", book),
            _fact("account_determination_procedure", "KOFI00", "BOOK_CONFIRMED", book),
            _fact("account_determination_condition_type", "KOFI", "BOOK_CONFIRMED", book),
            _fact("account_determination_table", "001", "BOOK_CONFIRMED", book),
            _fact("revenue_account_key", "ERL", "BOOK_CONFIRMED", book),
            _fact("freight_account_key", "ERF", "BOOK_CONFIRMED", book),
            _fact("account_determination_example_gl", "41000000", "BOOK_CONFIRMED", book),
            _fact("account_determination_second_example_gl", "49000000", "BOOK_CONFIRMED", book),
            _fact("material_account_assignment_group_example", "01", "BOOK_CONFIRMED", book),
            _fact("golden_flow_account_assignment_values", None, "UNKNOWN", book),
        ],
    }

    same_family_inspections = [
        {
            "target": value,
            "purpose": purpose,
            "allowed_method": "GET_READ_ONLY",
            "captured_repository_result": "NOT_CAPTURED",
            "classification": "UNKNOWN",
            "resolved_fields": {},
            "required_phase5_fields": required_fields,
            "usage": "EVIDENCE_TEMPLATE_ONLY_NEVER_SUBSTITUTE",
        }
        for value, purpose, required_fields in (
            (
                "C615-A00",
                "customer root/company/sales-area template evidence",
                list(REQUIRED_CUSTOMER_SOURCE_FIELDS),
            ),
            (
                "C615-B00",
                "customer root/company/sales-area template evidence",
                list(REQUIRED_CUSTOMER_SOURCE_FIELDS),
            ),
            (
                "P615-100",
                "product root/sales/plant/UoM template evidence",
                list(REQUIRED_PRODUCT_SOURCE_FIELDS),
            ),
            (
                "P615-200",
                "product root/sales/plant/UoM template evidence",
                list(REQUIRED_PRODUCT_SOURCE_FIELDS),
            ),
        )
    ]

    human_decisions = [
        "Company Code 1010: approved manual creation source and name/city/country/currency/language; chart of accounts is INT from the Book.",
        "Sales Org 1010: approved manual creation source, description, and statistics currency.",
        "Customer C615-D00: approve same-family template evidence or provide grouping/name/address/roles/company-code and sales-area mandatory values.",
        "Product P615-400: approve same-family template evidence or provide material type/industry/base UoM/plant/sales/logistics/valuation/tax values and PC conversion if PC is not base UoM.",
        "Customizing transport ownership/request must be supplied; release remains manual and is never automatic.",
        "Delivery, PGI, BV billing, and accounting readback need live read/write contracts before execution beyond the sales-order checkpoint.",
    ]

    workflow = [
        {"order": 1, "stage": "COMMON_ENV", "status": "BLOCKED_NEEDS_HUMAN_DECISION"},
        {"order": 2, "stage": "CUSTOMER_C615_D00", "status": "BLOCKED_NEEDS_SOURCE"},
        {"order": 3, "stage": "PRODUCT_P615_400", "status": "BLOCKED_NEEDS_SOURCE"},
        {"order": 4, "stage": "PRECHECKS", "status": "PENDING_DEPENDENCIES"},
        {"order": 5, "stage": "ANTI_DUPLICATE_00S4615_BV", "status": "PENDING_DEPENDENCIES"},
        {"order": 6, "stage": "BV_CASH_SALE", "status": "PENDING_DEPENDENCIES"},
        {"order": 7, "stage": "VERIFY_AUTO_CREATED_DELIVERY", "status": "CONTRACT_REQUIRED"},
        {"order": 8, "stage": "PGI", "status": "CONTRACT_REQUIRED"},
        {"order": 9, "stage": "BILLING_BV", "status": "CONTRACT_REQUIRED"},
        {"order": 10, "stage": "ACCOUNTING_READBACK", "status": "CONTRACT_REQUIRED"},
    ]

    return {
        "resolution_id": "S4615_USER00_FINAL_BLOCKER_RESOLUTION",
        "mode": "DRY_RUN_PREPARE",
        "sap_live_read_performed": False,
        "sap_write_performed": False,
        "primary_source": {"path": book, "sha256": _sha256(FACTS_PATH)},
        "secondary_source_read": False,
        "classification_contract": sorted(ALLOWED_CLASSIFICATIONS),
        "facts": facts,
        "same_family_read_only_inspections": same_family_inspections,
        "common_environment_status": "BLOCKED_NEEDS_HUMAN_DECISION",
        "customer_status": "BLOCKED_NEEDS_SOURCE",
        "product_status": "BLOCKED_NEEDS_SOURCE",
        "s4615_status": "BLOCKED_NOT_EXECUTION_READY",
        "workflow": workflow,
        "execution_policy": {
            "sequence": ["check", "prepare", "validate", "write", "readback"],
            "exists_behavior": "SKIP",
            "default_mode": "DRY_RUN",
            "write_gate": "--execute",
            "stop_conditions": [
                "UNEXPECTED_POPUP", "TRANSPORT_REQUIRED", "UNKNOWN_MANDATORY_VALUE",
            ],
            "transport_release": "NEVER_AUTOMATIC",
            "protected_sales_order": "148",
        },
        "exact_target": {
            "training_user": "S4615-00",
            "company_code": "1010",
            "sales_organization": "1010",
            "distribution_channel": "10",
            "sales_division": "00",
            "sales_area": "1010/10/00",
            "customer": "C615-D00",
            "product": "P615-400",
            "sales_order_type": "BV",
            "customer_reference": "00S4615-BV",
            "quantity": 1,
            "unit": "PC",
        },
        "final_human_decisions": human_decisions,
        "source_artifacts": [
            {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": _sha256(path)}
            for path in (PHASE4_REQUIREMENTS, PHASE5_PREPARE)
        ],
    }


def render_report(resolution: dict[str, Any]) -> str:
    lines = [
        "# S4615 user 00 — final blocker resolution",
        "",
        "No SAP live read or write was performed. The full clean book and original PDF were not read.",
        "",
        "## Status",
        "",
        f"- Common environment: **{resolution['common_environment_status']}**",
        f"- Customer: **{resolution['customer_status']}**",
        f"- Product: **{resolution['product_status']}**",
        f"- S4615: **{resolution['s4615_status']}**",
        "",
        "## Exact target",
        "",
        f"`{json.dumps(resolution['exact_target'], ensure_ascii=False, sort_keys=True)}`",
        "",
        "## Workflow",
        "",
        "| Order | Stage | Status |",
        "|---:|---|---|",
    ]
    lines.extend(
        f"| {item['order']} | {item['stage']} | {item['status']} |"
        for item in resolution["workflow"]
    )
    lines.extend(["", "## Final human decisions", ""])
    lines.extend(f"- {item}" for item in resolution["final_human_decisions"])
    lines.extend(["", "## Classified values", ""])
    for group, items in resolution["facts"].items():
        lines.extend([f"### {group}", "", "| Field | Value | Classification |", "|---|---|---|"])
        lines.extend(
            f"| {item['field']} | `{json.dumps(item['value'], ensure_ascii=False)}` | {item['classification']} |"
            for item in items
        )
        lines.append("")
    return "\n".join(lines)


def write_outputs(resolution: dict[str, Any]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(resolution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    OUTPUT_REPORT.write_text(render_report(resolution), encoding="utf-8")


def main() -> int:
    resolution = build_resolution()
    write_outputs(resolution)
    print(json.dumps({
        "status": resolution["s4615_status"],
        "live_read": False,
        "live_write": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
