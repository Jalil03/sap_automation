"""Build the offline Phase 4B minimal provisioning plan for S4615 CH4 EX5."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "data" / "requirements" / "training_environment_requirements.json"
CANONICAL_PATH = ROOT / "data" / "validated" / "canonical_objects.json"
REGISTRY_PATH = ROOT / "mappings" / "sap" / "interface_registry.yaml"
CONTRACT_PATH = ROOT / "schemas" / "sap" / "core_mapping_contracts.json"
METADATA_PATH = ROOT / "evidence" / "sap_live" / "odata" / "API_SALES_ORDER_SRV.metadata.xml"
OUTPUT_PATH = ROOT / "data" / "requirements" / "golden_book_s4615_ch4_ex5_provisioning.json"
REPORT_PATH = ROOT / "reports" / "phase4b_golden_book_s4615_provisioning.md"
BROWSER_SCRIPT_PATH = ROOT / "scripts" / "browser_checks_s4615_ch4_ex5.js"

CANONICAL_ID = "S4615_CH4_EX5_SALES_ORDER_CASH_SALE"
SCENARIO_ID = "S4615_CH4_EX5"
TRAINING_USER = "00"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hash_id(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()[:12].upper()


def _resolve(value: str) -> str:
    return value.replace("##", TRAINING_USER)


def _find_requirement(requirements: list[dict[str, Any]], requirement_type: str, value: str) -> dict[str, Any]:
    matches = [r for r in requirements if r["type"] == requirement_type and r["value_template"] == value]
    if len(matches) != 1:
        raise ValueError(f"Expected one {requirement_type}={value!r}, found {len(matches)}")
    return matches[0]


def _interface_details(req: dict[str, Any]) -> tuple[str, str | None, str, list[str]]:
    candidate = req["sap_interface_candidate"]
    classification = candidate.get("classification")
    service = candidate.get("service")
    operation = candidate.get("operation")
    evidence = [candidate.get("evidence") or "No interface evidence."]

    if req["current_known_sap_status"] == "EXISTS":
        return "UNKNOWN", service, "NOT_APPLICABLE", evidence + ["No write is required for an existing prerequisite."]
    if req["type"] == "SALES_ORDER":
        return (
            "ODATA_CREATE_SUPPORTED",
            "A_SalesOrder",
            "HIGH",
            evidence
            + [
                "evidence/sap_live/odata/API_SALES_ORDER_SRV.metadata.xml confirms A_SalesOrder and metadata-level create capability.",
                "Deep-insert execution and authorization remain unproven.",
            ],
        )
    if req["type"] == "BUSINESS_PARTNER":
        return (
            "ODATA_CREATE_SUPPORTED",
            "A_BusinessPartner (mapper contract; local service metadata absent)",
            "MEDIUM",
            evidence + ["Phase 2 contract maps BUSINESS_PARTNER to API_BUSINESS_PARTNER; exact create shape is not live-validated."],
        )
    if req["type"] == "MATERIAL":
        return (
            "BAPI_SUPPORTED",
            "BAPI_MATERIAL_SAVEDATA",
            "HIGH",
            evidence + ["Exact STANDARD_BAPI candidate with MAINTAIN operation in the local inventory."],
        )
    if req["type"] == "PRODUCT_UNIT_OF_MEASURE":
        return (
            "UNKNOWN",
            "A_ProductUnitsOfMeasure",
            "HIGH",
            evidence + ["Entity set and Product + AlternativeUnit keys are read-confirmed; write capability is not proven."],
        )
    if req["type"] == "UNIT_OF_MEASURE":
        return (
            "UNKNOWN",
            "A_ProductUnitsOfMeasure (product-specific lookup only)",
            "HIGH",
            evidence + ["There is no evidenced standalone unit write contract."],
        )
    if classification == "LOOKUP_ONLY":
        return "MANUAL_CUSTOMIZING_REQUIRED", service, "HIGH", evidence + ["The registry restricts this interface to lookup."]
    if classification == "ODATA" and operation == "MAINTAIN":
        return "ODATA_CREATE_SUPPORTED", service, "MEDIUM", evidence
    if classification == "STANDARD_BAPI":
        return "BAPI_SUPPORTED", service, "MEDIUM", evidence
    if classification == "RFC_FUNCTION":
        return "RFC_SUPPORTED", service, "MEDIUM", evidence
    if classification == "NO_INTERFACE_FOUND":
        return "INTERFACE_NOT_FOUND", None, "HIGH", evidence
    return "UNKNOWN", service, "LOW", evidence


def _base_layer(req: dict[str, Any]) -> str:
    if req["current_known_sap_status"] == "EXISTS":
        return "EXISTING"
    if req["type"] in {"COMPANY_CODE", "SALES_ORGANIZATION"}:
        return "GLOBAL_CUSTOMIZING"
    if req["type"] in {"DISTRIBUTION_CHANNEL", "SALES_DIVISION", "SALES_AREA"}:
        return "SALES_AREA_CUSTOMIZING"
    if req["type"] in {"BUSINESS_PARTNER", "MATERIAL"}:
        return "MASTER_DATA_CREATE"
    if req["type"] in {"PRODUCT_UNIT_OF_MEASURE"}:
        return "MASTER_DATA_EXTEND"
    if req["type"] == "SALES_ORDER":
        return "TRANSACTIONAL_RUNTIME"
    return "UNKNOWN"


def _plan_requirement(req: dict[str, Any], direct_ids: set[str]) -> dict[str, Any]:
    capability, target, confidence, capability_evidence = _interface_details(req)
    strategy = req["provisioning_strategy"]
    if req["type"] in {"BUSINESS_PARTNER", "MATERIAL"}:
        # The live observation proves the scenario-facing object is missing, but
        # the repository does not preserve enough evidence to distinguish root
        # creation from role/view extension.
        strategy = "BLOCKED"
    # In the scenario-specific plan every non-existing prerequisite is an
    # execution blocker, even when its broad Phase 4 inventory risk was medium.
    scenario_risk = "LOW" if req["current_known_sap_status"] == "EXISTS" else "HIGH"
    return {
        "requirement_id": req["requirement_id"],
        "type": req["type"],
        "template": req["value_template"],
        "runtime_value": _resolve(req["value_template"]),
        "scope": req["scope"],
        "direct_or_transitive": "DIRECT" if req["requirement_id"] in direct_ids else "TRANSITIVE",
        "depends_on": list(req["depends_on"]),
        "current_sap_status": req["current_known_sap_status"],
        "risk": scenario_risk,
        "provisioning_strategy": strategy,
        "provisioning_layer": _base_layer(req),
        "write_capability": capability,
        "interface_candidate": req["sap_interface_candidate"].get("service"),
        "entity_set_or_bapi": target,
        "confidence": confidence,
        "evidence": capability_evidence + [f"Phase 4 requirement {req['requirement_id']}"],
    }


def _synthetic_requirement(
    requirement_type: str,
    template: str,
    depends_on: list[str],
    interface: str,
    target: str,
    capability: str,
    evidence: list[str],
) -> dict[str, Any]:
    return {
        "requirement_id": f"REQ_{requirement_type}_{_hash_id(requirement_type + '|' + template)}",
        "type": requirement_type,
        "template": template,
        "runtime_value": _resolve(template),
        "scope": "PER_USER",
        "direct_or_transitive": "TRANSITIVE",
        "depends_on": sorted(depends_on),
        "current_sap_status": "UNKNOWN",
        "risk": "HIGH",
        "provisioning_strategy": "BLOCKED",
        "provisioning_layer": "MASTER_DATA_EXTEND",
        "write_capability": capability,
        "interface_candidate": interface,
        "entity_set_or_bapi": target,
        "confidence": "MEDIUM",
        "evidence": evidence,
    }


def build_plan() -> dict[str, Any]:
    inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    canonical = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))
    requirements = inventory["requirements"]
    index = {r["requirement_id"]: r for r in requirements}
    root_matches = [r for r in requirements if CANONICAL_ID in r["canonical_object_ids"]]
    if len(root_matches) != 1:
        raise ValueError(f"Expected one root requirement, found {len(root_matches)}")
    root = root_matches[0]
    direct_ids = {root["requirement_id"], *root["depends_on"]}

    closure_ids: set[str] = set()
    pending = [root["requirement_id"]]
    while pending:
        requirement_id = pending.pop()
        if requirement_id in closure_ids:
            continue
        closure_ids.add(requirement_id)
        pending.extend(index[requirement_id]["depends_on"])

    # The exact 1010/10/00 combination is source-backed elsewhere in the
    # canonical dataset and is structurally required by the selected order.
    sales_area = _find_requirement(requirements, "SALES_AREA", "1010/10/00")
    closure_ids.add(sales_area["requirement_id"])
    pending = list(sales_area["depends_on"])
    while pending:
        requirement_id = pending.pop()
        if requirement_id not in closure_ids:
            closure_ids.add(requirement_id)
            pending.extend(index[requirement_id]["depends_on"])

    planned = [_plan_requirement(index[rid], direct_ids) for rid in closure_ids]
    planned_index = {r["requirement_id"]: r for r in planned}
    bp = _find_requirement(requirements, "BUSINESS_PARTNER", "C615-D##")
    material = _find_requirement(requirements, "MATERIAL", "P615-4##")
    product_uom = _find_requirement(requirements, "PRODUCT_UNIT_OF_MEASURE", "P615-4##|PC")

    customer_extension = _synthetic_requirement(
        "CUSTOMER_SALES_AREA_EXTENSION",
        "C615-D##|1010/10/00",
        [bp["requirement_id"], sales_area["requirement_id"]],
        "API_BUSINESS_PARTNER",
        "A_CustomerSalesArea (Phase 2 mapping path; local metadata not captured)",
        "ODATA_UPDATE_SUPPORTED",
        [
            "schemas/sap/core_mapping_contracts.json maps sales_areas to to_CustomerSalesArea[].",
            "No local API_BUSINESS_PARTNER metadata proves create/update facets for this entity set.",
        ],
    )
    product_extension = _synthetic_requirement(
        "PRODUCT_SALES_AREA_EXTENSION",
        "P615-4##|1010/10",
        [material["requirement_id"], _find_requirement(requirements, "SALES_ORGANIZATION", "1010")["requirement_id"], _find_requirement(requirements, "DISTRIBUTION_CHANNEL", "10")["requirement_id"]],
        "BAPI_MATERIAL_SAVEDATA",
        "SALESDATA.SALES_ORG + SALESDATA.DISTR_CHAN",
        "BAPI_SUPPORTED",
        [
            "schemas/sap/core_mapping_contracts.json maps material sales_organization and distribution_channel to BAPI SALESDATA.",
            "Required BAPI create/extend attributes are not present in the selected SALES_ORDER canonical object.",
        ],
    )
    planned.extend([customer_extension, product_extension])
    planned_index.update({customer_extension["requirement_id"]: customer_extension, product_extension["requirement_id"]: product_extension})

    # Strengthen dependencies which were intentionally not inferred globally in
    # Phase 4 because they are scenario-specific composite views.
    root_plan = planned_index[root["requirement_id"]]
    root_plan["depends_on"] = sorted(set(root_plan["depends_on"]) | {customer_extension["requirement_id"], product_extension["requirement_id"]})
    planned_index[product_uom["requirement_id"]]["depends_on"] = sorted(
        set(planned_index[product_uom["requirement_id"]]["depends_on"]) | {material["requirement_id"]}
    )

    layer_order = {
        "EXISTING": 0,
        "GLOBAL_CUSTOMIZING": 1,
        "SALES_AREA_CUSTOMIZING": 2,
        "MASTER_DATA_CREATE": 3,
        "MASTER_DATA_EXTEND": 4,
        "UNKNOWN": 5,
        "TRANSACTIONAL_RUNTIME": 6,
    }
    planned.sort(key=lambda r: (layer_order[r["provisioning_layer"]], r["type"], r["runtime_value"]))

    customizing_types = {"COMPANY_CODE", "SALES_ORGANIZATION", "DISTRIBUTION_CHANNEL", "SALES_DIVISION", "SALES_AREA", "SALES_ORDER_TYPE"}
    master_types = {"BUSINESS_PARTNER", "MATERIAL", "CUSTOMER_SALES_AREA_EXTENSION", "PRODUCT_SALES_AREA_EXTENSION", "PRODUCT_UNIT_OF_MEASURE", "UNIT_OF_MEASURE"}
    counts = {
        "total": len(planned),
        "direct": sum(r["direct_or_transitive"] == "DIRECT" for r in planned),
        "transitive": sum(r["direct_or_transitive"] == "TRANSITIVE" for r in planned),
        "exists": sum(r["current_sap_status"] == "EXISTS" for r in planned),
        "missing": sum(r["current_sap_status"] == "MISSING" for r in planned),
        "unknown": sum(r["current_sap_status"] == "UNKNOWN" for r in planned),
        "high_risk": sum(r["risk"] == "HIGH" for r in planned),
        "customizing": sum(r["type"] in customizing_types for r in planned),
        "master_data": sum(r["type"] in master_types for r in planned),
        "transactional": sum(r["provisioning_layer"] == "TRANSACTIONAL_RUNTIME" for r in planned),
    }

    dag_layers = []
    for layer, title in [
        (0, "EXISTING prerequisites"),
        (1, "Global / organizational customizing"),
        (2, "Sales-area customizing"),
        (3, "Customer / product root master data"),
        (4, "Master-data extensions and product-specific unit"),
        (5, "Read-only runtime qualification checks"),
        (6, "Sales Order BV runtime creation"),
        (7, "Downstream outcome observation"),
    ]:
        ids = [r["requirement_id"] for r in planned if layer_order.get(r["provisioning_layer"]) == layer]
        if layer == 5:
            ids = ["CHECK_CUSTOMER_ROOT_VS_EXTENSION", "CHECK_PRODUCT_ROOT_VS_EXTENSION", "CHECK_SALES_AREA", "CHECK_PRODUCT_UOM", "CHECK_DUPLICATE_ORDER"]
        if layer == 7:
            ids = ["OBSERVE_AUTO_OUTBOUND_DELIVERY", "OBSERVE_CASH_SALE_BILLING"]
        dag_layers.append({"layer": layer, "name": title, "nodes": ids})

    return {
        "plan_version": "1.0.0",
        "policy": "OFFLINE_READ_ONLY_NO_SAP_EXECUTION",
        "scenario": {
            "book": "S4615",
            "chapter": 4,
            "exercise": 5,
            "scenario_id": SCENARIO_ID,
            "canonical_object_id": CANONICAL_ID,
            "training_user_code": TRAINING_USER,
            "training_user_runtime": "S4615-00",
            "selection_boundary": "Selected cash-sale SALES_ORDER and its prerequisites; pro-forma branch excluded.",
        },
        "source_integrity": {
            "phase4_inventory": str(INVENTORY_PATH.relative_to(ROOT)).replace("\\", "/"),
            "phase4_inventory_sha256": _sha(INVENTORY_PATH),
            "canonical_objects": str(CANONICAL_PATH.relative_to(ROOT)).replace("\\", "/"),
            "canonical_sha256": _sha(CANONICAL_PATH),
            "canonical_modified": False,
            "sap_connection_performed": False,
        },
        "summary": counts,
        "requirements": planned,
        "structural_dependency_assessment": [
            {"component": "COMPANY_CODE_1010", "necessity": "REQUIRED_FOR_BOOK", "reason": "Source-backed dependency of Sales Organization 1010; existence remains UNKNOWN."},
            {"component": "SALES_ORGANIZATION_1010", "necessity": "REQUIRED_FOR_BOOK", "reason": "Exact order header value; confirmed MISSING."},
            {"component": "DISTRIBUTION_CHANNEL_10", "necessity": "REQUIRED_FOR_BOOK", "reason": "Exact order header value; code EXISTS, assignment to 1010 still requires sales-area validation."},
            {"component": "SALES_DIVISION_00", "necessity": "REQUIRED_FOR_BOOK", "reason": "Exact order header value; code EXISTS, assignment still requires sales-area validation."},
            {"component": "SALES_AREA_1010_10_00", "necessity": "REQUIRED_FOR_BOOK", "reason": "Exact composite used by the order and customer extension."},
            {"component": "SALES_ORDER_TYPE_BV", "necessity": "REQUIRED_FOR_BOOK", "reason": "Exact order type; confirmed EXISTS."},
            {"component": "PLANT", "necessity": "MAY_BE_REQUIRED", "reason": "No plant is supplied by the canonical item; SAP determination may require a valid customer/product plant setup."},
            {"component": "PLANT_TO_SALES_ORGANIZATION", "necessity": "MAY_BE_REQUIRED", "reason": "Relevant only if plant determination is needed; no exact assignment is source-backed for this scenario."},
            {"component": "SHIPPING_POINT", "necessity": "MAY_BE_REQUIRED", "reason": "No shipping point is supplied; cash-sale delivery may require determination."},
            {"component": "SHIPPING_DETERMINATION", "necessity": "MAY_BE_REQUIRED", "reason": "Required only if automatic delivery needs shipping-point determination; exact rule is absent from this scenario."},
            {"component": "PRICING_CONFIGURATION", "necessity": "MAY_BE_REQUIRED", "reason": "The order contains no explicit pricing condition or procedure identity."},
            {"component": "OTHER_S4615_DOCUMENT_TYPES", "necessity": "NOT_REQUIRED_FOR_THIS_BOOK", "reason": "Only BV is required for the selected cash-sale order."},
            {"component": "PRO_FORMA_BRANCH", "necessity": "NOT_REQUIRED_FOR_THIS_BOOK", "reason": "The selected canonical object is the cash-sale order; pro-forma objects are a sibling branch, not prerequisites."},
        ],
        "customer_assessment": {
            "runtime_customer": "C615-D00",
            "decision": "C_CANNOT_DETERMINE_WITHOUT_LIVE_CHECK",
            "reason": "MISSING is established for the scenario-facing customer, but retained evidence does not distinguish absent BP root, absent customer role, or absent 1010/10/00 sales-area extension.",
            "required_views_if_root_exists": ["Customer role/entity", "Customer sales area 1010/10/00"],
            "possibly_required_for_downstream_billing": ["Customer company-code view 1010"],
            "unknown_create_attributes": ["Business-partner grouping", "name/address", "customer account group", "mandatory sales-area attributes"],
        },
        "product_assessment": {
            "runtime_product": "P615-400",
            "decision": "C_CANNOT_DETERMINE_WITHOUT_LIVE_CHECK",
            "reason": "MISSING is established for the scenario-facing material, but retained evidence does not distinguish absent product root from missing sales/plant views.",
            "required_views": ["Product/material root", "Sales organization 1010 / distribution channel 10", "Product-specific unit P615-400 + PC"],
            "possibly_required": ["Plant extension for the SAP-determined plant", "delivery-related product data"],
            "unknown_create_attributes": ["Industry sector", "material type", "base unit if different from the order unit", "mandatory valuation/plant attributes"],
            "uom_rule": "PC remains PC. The observed FG228/PC association and runtime code 289 do not authorize a conversion for P615-400.",
        },
        "cash_sale_assessment": {
            "sales_order_type": "BV",
            "status": "EXISTS",
            "required": ["valid sales area", "sold-to customer usable in 1010/10/00", "product usable in 1010/10", "product-specific PC unit"],
            "downstream": {
                "S4615_CH4_EX5_OUTBOUND_DELIVERY_CASH_SALE": "EXPECTED_WORKFLOW_OUTCOME_NOT_PROVISIONING_PREREQUISITE",
                "S4615_CH4_EX5_BILLING_CASH_SALE": "EXPECTED_FOLLOW_UP_NOT_ROOT_PREREQUISITE",
                "S4615_CH4_EX5_SALES_ORDER_PRO_FORMA": "EXCLUDED_SIBLING_BRANCH",
                "S4615_CH4_EX5_BILLING_PRO_FORMA": "EXCLUDED_SIBLING_BRANCH",
            },
        },
        "provisioning_dag": dag_layers,
        "read_only_validation_plan": {
            "script": "scripts/browser_checks_s4615_ch4_ex5.js",
            "execution_performed": False,
            "checks": [
                "Company Code 1010 existence",
                "Sales area 1010/10/00 exact assignment (no confirmed browser endpoint; manual read-only validation needed)",
                "Business Partner root, customer role, and customer sales-area extension for C615-D00",
                "Product root and sales-view metadata for P615-400",
                "Product-specific P615-400 + PC association",
                "Pre-existing duplicate cash-sale order fingerprint",
            ],
        },
        "first_required_sap_write": {
            "component": "SALES_ORGANIZATION_1010",
            "kind": "MANUAL_CUSTOMIZING_REQUIRED",
            "reason": "It is a required order-header prerequisite and is confirmed MISSING; the local registry exposes lookup only.",
            "authorized": False,
        },
    }


def render_report(plan: dict[str, Any]) -> str:
    s = plan["summary"]
    lines = [
        "# Phase 4B — Golden Book S4615 CH4 EX5 minimal provisioning",
        "",
        "## Conclusion",
        "",
        "**BLOCKED.** Le premier write nécessaire serait le customizing de l’organisation commerciale `1010`, confirmée absente. Aucun contrat writable local ne couvre cette opération : le registre ne fournit qu’un lookup. Le customer `C615-D00` et le product `P615-400` sont également absents au niveau testé, mais les preuves conservées ne permettent pas encore de choisir création complète ou extension.",
        "",
        "Aucune connexion SAP et aucune écriture n’ont été effectuées. Le canonical est inchangé.",
        "",
        "## Périmètre et comptages",
        "",
        f"- Requirements : **{s['total']}** — {s['direct']} directs, {s['transitive']} transitifs.",
        f"- États : **{s['exists']} EXISTS**, **{s['missing']} MISSING**, **{s['unknown']} UNKNOWN**.",
        f"- Risque : **{s['high_risk']} HIGH RISK**.",
        f"- Nature : **{s['customizing']} customizing**, **{s['master_data']} master data**, **{s['transactional']} transactionnel**.",
        "- Frontière : commande Cash Sale BV sélectionnée et prérequis; branche pro forma exclue car elle n’est pas une dépendance du canonical sélectionné.",
        "",
        "## Requirements minimaux",
        "",
        "| Requirement | Type | Template | Runtime 00 | Direct/transitif | SAP | Layer | Write capability |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for req in plan["requirements"]:
        lines.append(
            f"| `{req['requirement_id']}` | {req['type']} | `{req['template']}` | `{req['runtime_value']}` | {req['direct_or_transitive']} | {req['current_sap_status']} | {req['provisioning_layer']} | {req['write_capability']} |"
        )
    lines += [
        "",
        "## A. Minimal blockers",
        "",
        "1. `SalesOrganization 1010` est MISSING et doit précéder toute donnée de base liée à 1010/10/00.",
        "2. L’existence du `CompanyCode 1010` et du sales area exact `1010/10/00` reste à confirmer.",
        "3. `C615-D00` est MISSING, mais root BP versus extension customer/sales area n’est pas distingué.",
        "4. `P615-400` est MISSING, mais root product versus extension sales/plant n’est pas distingué.",
        "5. `P615-400 + PC` reste UNKNOWN; `FG228 + PC` ne constitue pas une preuve transférable.",
        "6. Le deep insert `A_SalesOrder` reste metadata-compatible mais non démontré en write.",
        "",
        "## B. Exact provisioning order",
        "",
    ]
    for layer in plan["provisioning_dag"]:
        lines.append(f"### Layer {layer['layer']} — {layer['name']}")
        lines.append("")
        for node in layer["nodes"]:
            lines.append(f"- `{node}`")
        if not layer["nodes"]:
            lines.append("- Aucun nœud minimal.")
        lines.append("")
    lines += [
        "## C. Automatisation possible avec les interfaces existantes",
        "",
        "- SALES_ORDER : `API_SALES_ORDER_SRV/A_SalesOrder`, contrat mapper et metadata locale disponibles; l’exécution write reste non prouvée.",
        "- BUSINESS_PARTNER : `API_BUSINESS_PARTNER` est inventorié en MAINTAIN et le mapper couvre les sales areas; metadata write locale absente.",
        "- MATERIAL : `BAPI_MATERIAL_SAVEDATA` est un candidat exact; les attributs obligatoires de création ne figurent pas dans ce scénario.",
        "- Product UoM : `A_ProductUnitsOfMeasure` est utilisable en GET avec les clés Product + AlternativeUnit; aucune capacité write n’est prouvée.",
        "",
        "## D. Customizing SAP probable",
        "",
        "`1010`, son affectation au company code, l’affectation du canal `10`, du secteur `00` et le sales area `1010/10/00` relèvent du customizing. Les interfaces locales correspondantes sont lookup-only : le plan ne prétend pas pouvoir les créer automatiquement.",
        "",
        "Le plant, l’affectation plant↔sales organization, le shipping point, la shipping determination et le pricing sont `MAY_BE_REQUIRED`, car le canonical exact ne fournit aucune valeur permettant de les provisionner sans invention.",
        "",
        "## E. Vérifications GET restantes",
        "",
        "Le script `scripts/browser_checks_s4615_ch4_ex5.js` charge d’abord le `$metadata` de chaque service. Il n’émet le GET de données que si l’EntitySet et les propriétés attendues sont réellement présents. Pour le sales area, aucun endpoint navigateur exact n’est prouvé : le résultat reste `NEEDS_LIVE_VALIDATION` au lieu de deviner une API.",
        "",
        "## F. Premier point nécessitant une écriture SAP",
        "",
        "Le premier write serait **la création/configuration de Sales Organization 1010**. Il est explicitement hors autorisation dans cette phase et nécessite vraisemblablement du customizing manuel ou un transport SAP gouverné.",
        "",
        "## Customer C615-D00",
        "",
        "Décision : **C — impossible à déterminer sans live check**. Si le BP root existe, les vues minimales connues sont le rôle/customer entity et la sales-area view `1010/10/00`. Pour la facturation aval, une company-code view `1010` peut être nécessaire, mais le scénario ne fournit pas assez d’éléments pour la déclarer certaine ni pour fabriquer ses attributs.",
        "",
        "## Product P615-400",
        "",
        "Décision : **C — impossible à déterminer sans live check**. Les besoins connus sont le root product/material, la vue ventes `1010/10` et l’association product-specific `P615-400 + PC`. Une extension plant est seulement potentielle. `PC` n’est jamais converti en `289`.",
        "",
        "## G. Fichiers",
        "",
        "- `data/requirements/golden_book_s4615_ch4_ex5_provisioning.json`",
        "- `reports/phase4b_golden_book_s4615_provisioning.md`",
        "- `scripts/browser_checks_s4615_ch4_ex5.js`",
        "- `scripts/build_golden_book_provisioning.py`",
        "- `tests/test_phase4b_golden_book_provisioning.py`",
        "",
        "## H. Tests",
        "",
        "Les tests vérifient la fermeture, la résolution `00`, l’absence de mutation canonical, le DAG, les statuts live, les décisions customer/product et le caractère GET-only du script navigateur.",
        "",
    ]
    return "\n".join(lines)


def browser_script() -> str:
    return r'''(() => {
  "use strict";

  const BASE = "/sap/opu/odata/sap";
  const checks = [
    { name: "COMPANY_CODE", value: "1010", service: "API_COMPANYCODE_SRV", entitySet: "A_CompanyCode", filters: { CompanyCode: "1010" }, select: ["CompanyCode"] },
    { name: "SALES_ORGANIZATION", value: "1010", service: "API_SALESORGANIZATION_SRV", entitySet: "A_SalesOrganization", filters: { SalesOrganization: "1010" }, select: ["SalesOrganization"] },
    { name: "DISTRIBUTION_CHANNEL", value: "10", service: "API_DISTRIBUTIONCHANNEL_SRV", entitySet: "A_DistributionChannel", filters: { DistributionChannel: "10" }, select: ["DistributionChannel"] },
    { name: "ORGANIZATION_DIVISION", value: "00", service: "API_DIVISION_SRV", entitySet: "A_Division", filters: { Division: "00" }, select: ["Division"] },
    { name: "CUSTOMER_TEMPLATE_A00_BP", value: "C615-A00", service: "API_BUSINESS_PARTNER", entitySet: "A_BusinessPartner", filters: { BusinessPartner: "C615-A00" }, select: ["BusinessPartner"], evidenceFields: ["BusinessPartnerGrouping", "OrganizationBPName1"] },
    { name: "CUSTOMER_TEMPLATE_A00_COMPANY", value: "C615-A00|1010", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerCompany", filters: { Customer: "C615-A00", CompanyCode: "1010" }, select: ["Customer", "CompanyCode"], evidenceFields: ["ReconciliationAccount", "PaymentTerms"] },
    { name: "CUSTOMER_TEMPLATE_A00_SALES_AREA", value: "C615-A00|1010/10/00", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerSalesArea", filters: { Customer: "C615-A00", SalesOrganization: "1010", DistributionChannel: "10", Division: "00" }, select: ["Customer", "SalesOrganization", "DistributionChannel", "Division"], evidenceFields: ["Currency", "ShippingCondition", "SupplyingPlant", "IncotermsClassification", "IncotermsLocation1", "CustomerAccountAssignmentGroup", "CustomerPricingProcedure"] },
    { name: "CUSTOMER_TEMPLATE_B00_BP", value: "C615-B00", service: "API_BUSINESS_PARTNER", entitySet: "A_BusinessPartner", filters: { BusinessPartner: "C615-B00" }, select: ["BusinessPartner"], evidenceFields: ["BusinessPartnerGrouping", "OrganizationBPName1"] },
    { name: "CUSTOMER_TEMPLATE_B00_COMPANY", value: "C615-B00|1010", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerCompany", filters: { Customer: "C615-B00", CompanyCode: "1010" }, select: ["Customer", "CompanyCode"], evidenceFields: ["ReconciliationAccount", "PaymentTerms"] },
    { name: "CUSTOMER_TEMPLATE_B00_SALES_AREA", value: "C615-B00|1010/10/00", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerSalesArea", filters: { Customer: "C615-B00", SalesOrganization: "1010", DistributionChannel: "10", Division: "00" }, select: ["Customer", "SalesOrganization", "DistributionChannel", "Division"], evidenceFields: ["Currency", "ShippingCondition", "SupplyingPlant", "IncotermsClassification", "IncotermsLocation1", "CustomerAccountAssignmentGroup", "CustomerPricingProcedure"] },
    { name: "CUSTOMER_BP_ROOT", value: "C615-D00", service: "API_BUSINESS_PARTNER", entitySet: "A_BusinessPartner", filters: { BusinessPartner: "C615-D00" }, select: ["BusinessPartner"] },
    { name: "CUSTOMER_ROLE", value: "C615-D00", service: "API_BUSINESS_PARTNER", entitySet: "A_Customer", filters: { Customer: "C615-D00" }, select: ["Customer"] },
    { name: "CUSTOMER_SALES_AREA", value: "C615-D00|1010/10/00", service: "API_BUSINESS_PARTNER", entitySet: "A_CustomerSalesArea", filters: { Customer: "C615-D00", SalesOrganization: "1010", DistributionChannel: "10", Division: "00" }, select: ["Customer", "SalesOrganization", "DistributionChannel", "Division"] },
    { name: "PRODUCT_ROOT", value: "P615-400", service: "API_PRODUCT_SRV", entitySet: "A_Product", filters: { Product: "P615-400" }, select: ["Product"] },
    { name: "PRODUCT_UOM", value: "P615-400|PC", service: "API_PRODUCT_SRV", entitySet: "A_ProductUnitsOfMeasure", filters: { Product: "P615-400", AlternativeUnit: "PC" }, select: ["Product", "AlternativeUnit"] },
    { name: "PRODUCT_TEMPLATE_100", value: "P615-100", service: "API_PRODUCT_SRV", entitySet: "A_Product", filters: { Product: "P615-100" }, select: ["Product"], evidenceFields: ["ProductType", "IndustrySector", "BaseUnit"] },
    { name: "PRODUCT_TEMPLATE_100_PLANT", value: "P615-100", service: "API_PRODUCT_SRV", entitySet: "A_ProductPlant", filters: { Product: "P615-100" }, select: ["Product", "Plant"], evidenceFields: ["AvailabilityCheckType"] },
    { name: "PRODUCT_TEMPLATE_100_SALES", value: "P615-100|1010/10", service: "API_PRODUCT_SRV", entitySet: "A_ProductSalesDelivery", filters: { Product: "P615-100", ProductSalesOrg: "1010", ProductDistributionChnl: "10" }, select: ["Product", "ProductSalesOrg", "ProductDistributionChnl"], evidenceFields: ["SupplyingPlant", "ItemCategoryGroup", "AccountDetnProductGroup"] },
    { name: "PRODUCT_TEMPLATE_100_UOM", value: "P615-100|PC", service: "API_PRODUCT_SRV", entitySet: "A_ProductUnitsOfMeasure", filters: { Product: "P615-100", AlternativeUnit: "PC" }, select: ["Product", "AlternativeUnit"], evidenceFields: ["QuantityNumerator", "QuantityDenominator"] },
    { name: "PRODUCT_TEMPLATE_200", value: "P615-200", service: "API_PRODUCT_SRV", entitySet: "A_Product", filters: { Product: "P615-200" }, select: ["Product"], evidenceFields: ["ProductType", "IndustrySector", "BaseUnit"] },
    { name: "PRODUCT_TEMPLATE_200_PLANT", value: "P615-200", service: "API_PRODUCT_SRV", entitySet: "A_ProductPlant", filters: { Product: "P615-200" }, select: ["Product", "Plant"], evidenceFields: ["AvailabilityCheckType"] },
    { name: "PRODUCT_TEMPLATE_200_SALES", value: "P615-200|1010/10", service: "API_PRODUCT_SRV", entitySet: "A_ProductSalesDelivery", filters: { Product: "P615-200", ProductSalesOrg: "1010", ProductDistributionChnl: "10" }, select: ["Product", "ProductSalesOrg", "ProductDistributionChnl"], evidenceFields: ["SupplyingPlant", "ItemCategoryGroup", "AccountDetnProductGroup"] },
    { name: "PRODUCT_TEMPLATE_200_UOM", value: "P615-200|PC", service: "API_PRODUCT_SRV", entitySet: "A_ProductUnitsOfMeasure", filters: { Product: "P615-200", AlternativeUnit: "PC" }, select: ["Product", "AlternativeUnit"], evidenceFields: ["QuantityNumerator", "QuantityDenominator"] },
    { name: "DUPLICATE_CASH_SALE", value: "BV|1010/10/00|C615-D00|00S4615-BV", service: "API_SALES_ORDER_SRV", entitySet: "A_SalesOrder", filters: { SalesOrderType: "BV", SalesOrganization: "1010", DistributionChannel: "10", OrganizationDivision: "00", SoldToParty: "C615-D00", PurchaseOrderByCustomer: "00S4615-BV" }, select: ["SalesOrder", "SalesOrderType", "SalesOrganization", "DistributionChannel", "OrganizationDivision", "SoldToParty", "PurchaseOrderByCustomer"], invert: true }
  ];

  const escapeLiteral = value => String(value).replace(/'/g, "''");
  const results = [];
  const metadataCache = new Map();

  async function read(url, accept) {
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
      headers: { Accept: accept }
    });
    if (response.status === 401 || response.status === 403) {
      throw new Error(`Authentication stopped validation (${response.status})`);
    }
    return response;
  }

  async function metadata(service) {
    if (!metadataCache.has(service)) {
      const response = await read(`${BASE}/${service}/$metadata`, "application/xml");
      if (!response.ok) throw new Error(`${service} metadata HTTP ${response.status}`);
      metadataCache.set(service, new DOMParser().parseFromString(await response.text(), "application/xml"));
    }
    return metadataCache.get(service);
  }

  function entityProperties(doc, entitySetName) {
    const sets = [...doc.getElementsByTagNameNS("*", "EntitySet")];
    const set = sets.find(node => node.getAttribute("Name") === entitySetName);
    if (!set) return null;
    const qualifiedType = set.getAttribute("EntityType") || "";
    const typeName = qualifiedType.split(".").pop();
    const types = [...doc.getElementsByTagNameNS("*", "EntityType")];
    const type = types.find(node => node.getAttribute("Name") === typeName);
    if (!type) return null;
    return new Set([...type.getElementsByTagNameNS("*", "Property")].map(node => node.getAttribute("Name")));
  }

  async function runCheck(check) {
    const doc = await metadata(check.service);
    const available = entityProperties(doc, check.entitySet);
    const required = [...Object.keys(check.filters), ...check.select];
    if (!available || !required.every(name => available.has(name))) {
      return { PRECHECK: check.name, VALUE: check.value, SERVICE: check.service, ENTITYSET: check.entitySet, HTTP: "METADATA_ONLY", RESULT: "NEEDS_LIVE_VALIDATION" };
    }
    const evidenceFields = (check.evidenceFields || []).filter(name => available.has(name));
    const selectedFields = [...new Set([...check.select, ...evidenceFields])];
    const filter = Object.entries(check.filters).map(([key, value]) => `${key} eq '${escapeLiteral(value)}'`).join(" and ");
    const query = new URLSearchParams({ "$filter": filter, "$select": selectedFields.join(","), "$top": "1", "$format": "json" });
    const response = await read(`${BASE}/${check.service}/${check.entitySet}?${query.toString()}`, "application/json");
    if (!response.ok) return { PRECHECK: check.name, VALUE: check.value, SERVICE: check.service, ENTITYSET: check.entitySet, HTTP: response.status, RESULT: "NEEDS_LIVE_VALIDATION" };
    const body = await response.json();
    const rows = body && body.d ? (Array.isArray(body.d.results) ? body.d.results : [body.d]) : [];
    const found = rows.length > 0;
    const result = check.invert ? (found ? "DUPLICATE_FOUND_BLOCKED" : "CONFIRMED_CLEAR") : (found ? "CONFIRMED_FOUND" : "CONFIRMED_NOT_FOUND");
    const evidence = found ? Object.fromEntries(evidenceFields.map(name => [name, rows[0][name] ?? null])) : {};
    return { PRECHECK: check.name, VALUE: check.value, SERVICE: check.service, ENTITYSET: check.entitySet, HTTP: response.status, RESULT: result, EVIDENCE: evidence };
  }

  (async () => {
    results.push({ PRECHECK: "SALES_AREA", VALUE: "1010/10/00", SERVICE: "BAPI_SALES_AREAS_GET", ENTITYSET: "N/A", HTTP: "NOT_RUN", RESULT: "NEEDS_LIVE_VALIDATION" });
    results.push({ PRECHECK: "PRODUCT_SALES_VIEW", VALUE: "P615-400|1010/10", SERVICE: "API_PRODUCT_SRV", ENTITYSET: "NOT_CONFIRMED", HTTP: "METADATA_ONLY", RESULT: "NEEDS_LIVE_VALIDATION" });
    for (const check of checks) results.push(await runCheck(check));
    console.table(results);
    console.log(
      results
        .map(r => `${r.PRECHECK} | ${r.VALUE} | ${r.HTTP} | ${r.RESULT}`)
        .join("\n")
    );
    return results;
  })().catch(error => {
    console.table(results);
    console.error(String(error.message || error));
  });
})();
'''


def write_outputs() -> dict[str, Any]:
    plan = build_plan()
    OUTPUT_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(render_report(plan), encoding="utf-8")
    BROWSER_SCRIPT_PATH.write_text(browser_script(), encoding="utf-8")
    return plan


if __name__ == "__main__":
    plan = write_outputs()
    print(json.dumps(plan["summary"], ensure_ascii=False, indent=2, sort_keys=True))
