"""Build the Phase 4 training-environment requirement inventory.

The builder is deliberately offline and deterministic.  It reads the immutable
Phase 1 canonical dataset and local contracts only; it contains no transport or
SAP client code.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = ROOT / "data" / "validated" / "canonical_objects.json"
REGISTRY_PATH = ROOT / "mappings" / "sap" / "interface_registry.yaml"
OUTPUT_PATH = ROOT / "data" / "requirements" / "training_environment_requirements.json"
REPORT_PATH = ROOT / "reports" / "phase4_training_environment_requirements.md"

BOOKS = ("S4600", "S4610", "S4615", "S4620", "S4650")
CATEGORIES = {
    "GLOBAL_CUSTOMIZING",
    "BOOK_CUSTOMIZING",
    "MASTER_DATA_SHARED",
    "MASTER_DATA_PER_BOOK",
    "MASTER_DATA_PER_USER",
    "TRANSACTIONAL_OBJECT",
    "RUNTIME_DEPENDENCY",
    "UNSUPPORTED_OR_UNKNOWN",
}
SCOPES = {"GLOBAL", "BOOK", "PER_USER"}
SAP_STATUSES = {"EXISTS", "MISSING", "UNKNOWN"}
STRATEGIES = {"CREATE", "EXTEND", "REUSE", "CUSTOMIZING", "RUNTIME_CREATE", "BLOCKED"}
RISKS = {"LOW", "MEDIUM", "HIGH"}

MASTER_TYPES = {
    "BUSINESS_PARTNER",
    "MATERIAL",
    "CUSTOMER_MATERIAL_INFO",
    "PRICING_CONDITION",
    "CUSTOMER_HIERARCHY",
    "CONDITION_CONTRACT",
    "PRODUCT_UNIT_OF_MEASURE",
}
REFERENCE_CUSTOMIZING_TYPES = {
    "COMPANY_CODE",
    "PLANT",
    "STORAGE_LOCATION",
    "WAREHOUSE_NUMBER",
}
RUNTIME_REFERENCE_TYPES = {"PURCHASE_ORDER_REFERENCE", "PAYMENT_REFERENCE"}

# Leaf names which denote a prerequisite rather than descriptive or result data.
# Values are requirement types, not new canonical object types.
REFERENCE_FIELDS = {
    "sales_organization": "SALES_ORGANIZATION",
    "distribution_channel": "DISTRIBUTION_CHANNEL",
    "source_distribution_channel": "DISTRIBUTION_CHANNEL",
    "target_distribution_channel": "DISTRIBUTION_CHANNEL",
    "sales_division": "SALES_DIVISION",
    "source_sales_division": "SALES_DIVISION",
    "target_sales_division": "SALES_DIVISION",
    "company_code": "COMPANY_CODE",
    "plant": "PLANT",
    "delivering_plant": "PLANT",
    "plants": "PLANT",
    "storage_location": "STORAGE_LOCATION",
    "warehouse_number": "WAREHOUSE_NUMBER",
    "shipping_point": "SHIPPING_POINT",
    "alternative_shipping_point": "SHIPPING_POINT",
    "sold_to_party": "BUSINESS_PARTNER",
    "ship_to_party": "BUSINESS_PARTNER",
    "payer": "BUSINESS_PARTNER",
    "business_partner": "BUSINESS_PARTNER",
    "customer": "BUSINESS_PARTNER",
    "supplier": "BUSINESS_PARTNER",
    "recipient": "BUSINESS_PARTNER",
    "partner": "BUSINESS_PARTNER",
    "material": "MATERIAL",
    "product": "MATERIAL",
    "settlement_material": "MATERIAL",
    "order_type": "SALES_ORDER_TYPE",
    "sales_document_type": "SALES_DOCUMENT_TYPE",
    "source_document_type": "SALES_DOCUMENT_TYPE",
    "target_document_type": "SALES_DOCUMENT_TYPE",
    "assigned_document_types": "SALES_DOCUMENT_TYPE",
    "billing_type": "BILLING_TYPE",
    "accounting_document_type": "ACCOUNTING_DOCUMENT_TYPE",
    "contract_type": "CONDITION_CONTRACT_TYPE",
    "condition_type": "CONDITION_TYPE",
    "condition_types_1": "CONDITION_TYPE",
    "condition_types_2": "CONDITION_TYPE",
    "quick_entry_condition_type": "CONDITION_TYPE",
    "copied_from_condition_type": "CONDITION_TYPE",
    "access_sequence": "ACCESS_SEQUENCE",
    "pricing_procedure": "PRICING_PROCEDURE",
    "condition_table": "CONDITION_TABLE",
    "condition_tables": "CONDITION_TABLE",
    "currency": "CURRENCY",
    "unit": "UNIT_OF_MEASURE",
    "base_unit": "UNIT_OF_MEASURE",
    "minimum_order_unit": "UNIT_OF_MEASURE",
    "quantity_unit": "UNIT_OF_MEASURE",
    "rate_unit": "UNIT_OF_MEASURE",
    "threshold_unit": "UNIT_OF_MEASURE",
    "net_weight_unit": "UNIT_OF_MEASURE",
    "gross_weight_unit": "UNIT_OF_MEASURE",
    "payment_terms": "PAYMENT_TERMS",
    "partner_role": "PARTNER_FUNCTION",
    "shipping_conditions": "SHIPPING_CONDITION",
    "shipping_condition": "SHIPPING_CONDITION",
    "storage_condition": "STORAGE_CONDITION",
    "loading_group": "LOADING_GROUP",
    "incoterms": "INCOTERMS",
    "chart_of_accounts": "CHART_OF_ACCOUNTS",
    "general_ledger_account": "GENERAL_LEDGER_ACCOUNT",
    "account_key": "ACCOUNT_KEY",
    "customer_account_assignment_group": "CUSTOMER_ACCOUNT_ASSIGNMENT_GROUP",
    "material_account_assignment_group": "MATERIAL_ACCOUNT_ASSIGNMENT_GROUP",
    "account_assignment_group": "CUSTOMER_ACCOUNT_ASSIGNMENT_GROUP",
    "reconciliation_account": "RECONCILIATION_ACCOUNT",
    "tax_classification": "TAX_CLASSIFICATION",
    "purchasing_organization": "PURCHASING_ORGANIZATION",
    "purchasing_group": "PURCHASING_GROUP",
    "confirmation_control": "CONFIRMATION_CONTROL",
    "bank_account": "BANK_ACCOUNT",
    "output_device": "OUTPUT_DEVICE",
    "print_queue": "OUTPUT_DEVICE",
    "form_template": "FORM_TEMPLATE",
    "output_types": "OUTPUT_TYPE",
    "material_type": "MATERIAL_TYPE",
    "item_category": "ITEM_CATEGORY",
    "source_item_category": "ITEM_CATEGORY",
    "target_item_category": "ITEM_CATEGORY",
    "roles": "BUSINESS_PARTNER_ROLE",
    "role": "PARTNER_FUNCTION",
}

CUSTOMIZING_REFERENCE_TYPES = {
    value for value in REFERENCE_FIELDS.values() if value not in MASTER_TYPES
} | REFERENCE_CUSTOMIZING_TYPES

IDENTITY_FIELDS = {
    "ACCESS_SEQUENCE": ("code",),
    "BUSINESS_PARTNER": ("partner_id",),
    "COMPANY_CODE": ("code",),
    "CONDITION_TABLE": ("table_id",),
    "CONDITION_TYPE": ("code",),
    "DISTRIBUTION_CHANNEL": ("code",),
    "EXTENSION_CONFIGURATION": ("configuration_key",),
    "MATERIAL": ("material_id",),
    "PLANT": ("code",),
    "PRICING_PROCEDURE": ("code",),
    "SALES_DIVISION": ("code",),
    "SALES_ORGANIZATION": ("code",),
    "SHIPPING_POINT": ("code",),
    "STORAGE_LOCATION": ("code",),
    "WAREHOUSE_NUMBER": ("code",),
}

LIVE_OBSERVATIONS = {
    ("SALES_ORGANIZATION", "1010"): ("MISSING", "TEST 600 live read-only validation"),
    ("DISTRIBUTION_CHANNEL", "10"): ("EXISTS", "TEST 600 live read-only validation"),
    ("SALES_DIVISION", "00"): ("EXISTS", "TEST 600 live read-only validation"),
    ("SALES_ORDER_TYPE", "BV"): ("EXISTS", "TEST 600 live read-only validation"),
    ("BUSINESS_PARTNER", "C610-A00"): ("MISSING", "TEST 600 live read-only validation"),
    ("MATERIAL", "P610-500"): ("MISSING", "TEST 600 live read-only validation"),
    ("BUSINESS_PARTNER", "C615-D00"): ("MISSING", "TEST 600 live read-only validation"),
    ("MATERIAL", "P615-400"): ("MISSING", "TEST 600 live read-only validation"),
    ("BUSINESS_PARTNER", "T-S50A00"): ("MISSING", "TEST 600 live read-only validation"),
    ("MATERIAL", "T-MS100"): ("MISSING", "TEST 600 live read-only validation"),
    ("BUSINESS_PARTNER", "C620-A00"): ("MISSING", "TEST 600 live read-only validation"),
    ("MATERIAL", "P620-100"): ("MISSING", "TEST 600 live read-only validation"),
    ("BUSINESS_PARTNER", "C650-A00"): ("MISSING", "TEST 600 live read-only validation"),
    ("MATERIAL", "P650-100"): ("MISSING", "TEST 600 live read-only validation"),
}

EXPLICIT_INTERFACES = {
    "SALES_ORDER_TYPE": {
        "classification": "LOOKUP_ONLY",
        "service": "API_SALESORDERTYPE_SRV",
        "entity_set": "A_SalesOrderType",
        "evidence": "config/sap_sales_order_prechecks.example.json; live read-only result",
    },
    "PRODUCT_UNIT_OF_MEASURE": {
        "classification": "LOOKUP_ONLY",
        "service": "API_PRODUCT_SRV",
        "entity_set": "A_ProductUnitsOfMeasure",
        "key_properties": ["Product", "AlternativeUnit"],
        "evidence": "TEST 600 live metadata validation",
    },
    "UNIT_OF_MEASURE": {
        "classification": "LOOKUP_ONLY",
        "service": "API_PRODUCT_SRV",
        "entity_set": "A_ProductUnitsOfMeasure",
        "key_properties": ["Product", "AlternativeUnit"],
        "limitation": "No standalone unit assertion; validation is product-specific.",
        "evidence": "TEST 600 live metadata validation",
    },
}


def _json_dump(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _slug_hash(*parts: str) -> str:
    payload = "|".join(parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12].upper()


def _provenance_context(obj: dict[str, Any]) -> tuple[set[str], set[str], dict[str, Any]]:
    provenance = obj["provenance"]
    books = {p["course_code"] for p in provenance if p.get("course_code") in BOOKS}
    scenarios = {p["scenario_id"] for p in provenance if p.get("scenario_id")}
    evidence = {
        "kind": "CANONICAL_OBJECT",
        "canonical_object_id": obj["object_id"],
        "course_codes": sorted(books),
        "scenario_ids": sorted(scenarios),
        "source_files": sorted({p["source_file"] for p in provenance}),
        "pages": sorted({p["page"] for p in provenance}),
    }
    return books, scenarios, evidence


def _canonical_identity(obj: dict[str, Any]) -> str:
    object_type = obj["object_type"]
    data = obj["data"]
    for field in IDENTITY_FIELDS.get(object_type, ()):
        if data.get(field) is not None:
            return str(data[field])
    if object_type == "SALES_AREA":
        return "/".join(str(data.get(k) or "?") for k in ("sales_organization", "distribution_channel", "sales_division"))
    if object_type == "CUSTOMER_MATERIAL_INFO":
        return "/".join(str(data.get(k) or "?") for k in ("business_partner", "material", "sales_organization", "distribution_channel"))
    # Complex records and all transactions retain their deterministic object ID.
    # This prevents a silent merge where the source does not expose a complete key.
    return obj["object_id"]


def _iter_leaf_references(value: Any, path: str = "data") -> Iterable[tuple[str, str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            requirement_type = REFERENCE_FIELDS.get(key)
            if requirement_type and child is not None:
                values = child if isinstance(child, list) else [child]
                for item in values:
                    if isinstance(item, (str, int, float)) and not isinstance(item, bool):
                        text = str(item).strip()
                        if text:
                            yield requirement_type, text, child_path
            yield from _iter_leaf_references(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_leaf_references(child, f"{path}[{index}]")


def _iter_product_units(value: Any, path: str = "data") -> Iterable[tuple[str, str, str]]:
    if isinstance(value, dict):
        product = value.get("material") or value.get("product") or value.get("material_id")
        units = []
        for field in ("unit", "base_unit", "minimum_order_unit", "quantity_unit"):
            unit = value.get(field)
            if isinstance(unit, str) and unit:
                units.append((unit, field))
        if isinstance(product, str):
            for unit, field in units:
                yield product, unit, f"{path}.{field}"
        for key, child in value.items():
            yield from _iter_product_units(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_product_units(child, f"{path}[{index}]")


def _interface_for(requirement_type: str, registry: dict[str, Any]) -> dict[str, Any]:
    if requirement_type in EXPLICIT_INTERFACES:
        return deepcopy(EXPLICIT_INTERFACES[requirement_type])
    entry = registry.get("object_types", {}).get(requirement_type)
    if not entry:
        return {
            "classification": "NO_INTERFACE_FOUND",
            "service": None,
            "entity_set": None,
            "evidence": "No exact local inventory/metadata contract for this requirement type.",
        }
    preferred = entry["preferred_interface"]
    return {
        "classification": preferred["classification"],
        "service": preferred.get("external_name") or preferred.get("exact_name"),
        "technical_name": preferred.get("exact_name"),
        "operation": preferred.get("operation"),
        "entity_set": None,
        "evidence": preferred.get("evidence_basis"),
    }


def _known_status(requirement_type: str, value: str) -> tuple[str, list[dict[str, Any]]]:
    evidence: list[dict[str, Any]] = []
    exact = LIVE_OBSERVATIONS.get((requirement_type, value))
    if exact:
        evidence.append({"kind": "LIVE_READ_ONLY", "value": value, "status": exact[0], "source": exact[1]})
        return exact[0], evidence
    if "##" in value:
        runtime_00 = value.replace("##", "00")
        observed = LIVE_OBSERVATIONS.get((requirement_type, runtime_00))
        if observed:
            evidence.append(
                {
                    "kind": "LIVE_READ_ONLY",
                    "training_user_code": "00",
                    "runtime_value": runtime_00,
                    "status": observed[0],
                    "source": observed[1],
                    "limitation": "Observation applies to resolved user 00; other training codes remain unverified.",
                }
            )
            return observed[0], evidence
    return "UNKNOWN", evidence


def _initial_category(classification: str, object_type: str) -> str:
    if classification == "TRANSACTION" or object_type in RUNTIME_REFERENCE_TYPES:
        return "TRANSACTIONAL_OBJECT"
    if classification == "MASTER_DATA" or object_type in MASTER_TYPES:
        return "MASTER_DATA_PER_BOOK"
    if classification == "CUSTOMIZING" or object_type in REFERENCE_CUSTOMIZING_TYPES:
        return "BOOK_CUSTOMIZING"
    if classification == "REFERENCE_DATA":
        return "BOOK_CUSTOMIZING"
    return "UNSUPPORTED_OR_UNKNOWN"


class InventoryBuilder:
    def __init__(self, registry: dict[str, Any]) -> None:
        self.registry = registry
        self.entries: dict[tuple[str, str, str], dict[str, Any]] = {}
        self.object_to_key: dict[str, tuple[str, str, str]] = {}
        self.pending_dependencies: list[tuple[tuple[str, str, str], str | tuple[str, str, str]]] = []

    def add(
        self,
        requirement_type: str,
        value: str,
        category: str,
        books: Iterable[str],
        scenarios: Iterable[str],
        evidence: dict[str, Any],
        canonical_object_id: str | None = None,
        evidence_path: str | None = None,
        contains_placeholder: bool = False,
    ) -> tuple[str, str, str]:
        value = str(value)
        kind = "TRANSACTION" if category == "TRANSACTIONAL_OBJECT" else "PREREQUISITE"
        key = (requirement_type, value, kind)
        if key not in self.entries:
            self.entries[key] = {
                "requirement_type": requirement_type,
                "value_or_template": value,
                "category_seed": category,
                "source_book": set(),
                "source_scenario": set(),
                "canonical_object_ids": set(),
                "evidence_source": [],
                "depends_on_keys": set(),
                "contains_placeholder_seed": False,
            }
        entry = self.entries[key]
        entry["source_book"].update(books)
        entry["source_scenario"].update(scenarios)
        if canonical_object_id:
            entry["canonical_object_ids"].add(canonical_object_id)
        entry["contains_placeholder_seed"] = entry["contains_placeholder_seed"] or contains_placeholder
        evidence_item = deepcopy(evidence)
        if evidence_path:
            evidence_item["field_path"] = evidence_path
        signature = _json_dump(evidence_item)
        if all(_json_dump(existing) != signature for existing in entry["evidence_source"]):
            entry["evidence_source"].append(evidence_item)
        return key

    def add_canonical(self, obj: dict[str, Any]) -> tuple[str, str, str]:
        books, scenarios, evidence = _provenance_context(obj)
        value = _canonical_identity(obj)
        category = _initial_category(obj["classification"], obj["object_type"])
        key = self.add(
            obj["object_type"],
            value,
            category,
            books,
            scenarios,
            evidence,
            obj["object_id"],
            contains_placeholder="##" in _json_dump(obj["data"]),
        )
        self.object_to_key[obj["object_id"]] = key
        return key

    def finalize(self) -> list[dict[str, Any]]:
        key_to_id: dict[tuple[str, str, str], str] = {}
        for key in self.entries:
            requirement_type, value, kind = key
            key_to_id[key] = f"REQ_{requirement_type}_{_slug_hash(requirement_type, value, kind)}"

        for source_key, target in self.pending_dependencies:
            target_key = self.object_to_key.get(target) if isinstance(target, str) else target
            if target_key in key_to_id:
                self.entries[source_key]["depends_on_keys"].add(target_key)

        result: list[dict[str, Any]] = []
        for key, raw in self.entries.items():
            requirement_type, value, _kind = key
            books = sorted(raw["source_book"])
            scenarios = sorted(raw["source_scenario"])
            contains_placeholder = raw["contains_placeholder_seed"] or "##" in value or any(
                "##" in _json_dump(e) for e in raw["evidence_source"]
            )
            if contains_placeholder:
                scope = "PER_USER"
            elif len(books) > 1:
                scope = "GLOBAL"
            else:
                scope = "BOOK"

            category = raw["category_seed"]
            if category in {"BOOK_CUSTOMIZING", "GLOBAL_CUSTOMIZING"}:
                category = "GLOBAL_CUSTOMIZING" if scope == "GLOBAL" else "BOOK_CUSTOMIZING"
            elif category.startswith("MASTER_DATA"):
                if scope == "PER_USER":
                    category = "MASTER_DATA_PER_USER"
                elif scope == "GLOBAL":
                    category = "MASTER_DATA_SHARED"
                else:
                    category = "MASTER_DATA_PER_BOOK"

            sap_status, live_evidence = _known_status(requirement_type, value)
            evidence_source = raw["evidence_source"] + live_evidence
            interface = _interface_for(requirement_type, self.registry)
            if category == "TRANSACTIONAL_OBJECT":
                strategy = "RUNTIME_CREATE"
            elif category == "RUNTIME_DEPENDENCY":
                strategy = "BLOCKED"
            elif category == "UNSUPPORTED_OR_UNKNOWN":
                strategy = "BLOCKED"
            elif sap_status == "EXISTS":
                strategy = "REUSE"
            elif category.endswith("CUSTOMIZING"):
                strategy = "CUSTOMIZING"
            elif category.startswith("MASTER_DATA"):
                # EXTEND requires proof that the root master exists and that only
                # a view/assignment is absent.  UNKNOWN must therefore fail closed.
                strategy = "CREATE" if sap_status == "MISSING" else "BLOCKED"
            else:
                strategy = "BLOCKED"

            if sap_status == "MISSING" or strategy == "BLOCKED" or category in {"RUNTIME_DEPENDENCY", "UNSUPPORTED_OR_UNKNOWN"}:
                risk = "HIGH"
            elif interface["classification"] in {"NO_INTERFACE_FOUND", "NO_EXECUTION_REQUIRED"}:
                risk = "HIGH" if strategy != "RUNTIME_CREATE" else "MEDIUM"
            elif contains_placeholder or sap_status == "UNKNOWN":
                risk = "MEDIUM"
            else:
                risk = "LOW"

            result.append(
                {
                    "requirement_id": key_to_id[key],
                    "category": category,
                    "type": requirement_type,
                    "value_template": value,
                    "source_book": books,
                    "source_scenario": scenarios,
                    "scope": scope,
                    "contains_placeholder": contains_placeholder,
                    "placeholder_pattern": "##" if contains_placeholder else None,
                    "depends_on": sorted(key_to_id[d] for d in raw["depends_on_keys"] if d in key_to_id),
                    "sap_interface_candidate": interface,
                    "current_known_sap_status": sap_status,
                    "evidence_source": sorted(evidence_source, key=_json_dump),
                    "provisioning_strategy": strategy,
                    "risk": risk,
                    "canonical_object_ids": sorted(raw["canonical_object_ids"]),
                }
            )
        return sorted(result, key=lambda r: (r["category"], r["type"], r["value_template"], r["requirement_id"]))


def build_inventory() -> dict[str, Any]:
    canonical = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    objects = canonical["objects"]
    builder = InventoryBuilder(registry)

    for obj in objects:
        builder.add_canonical(obj)

    for obj in objects:
        source_key = builder.object_to_key[obj["object_id"]]
        books, scenarios, base_evidence = _provenance_context(obj)

        for dependency in obj.get("dependencies", []):
            target_id = dependency.get("target_id")
            if target_id:
                builder.pending_dependencies.append((source_key, target_id))
                continue
            phrase = dependency.get("source_phrase")
            target_type = dependency.get("target_type")
            if not phrase or not target_type:
                continue
            dep_evidence = {
                **base_evidence,
                "kind": "CANONICAL_DEPENDENCY",
                "relation": dependency.get("relation"),
                "dependency_status": dependency.get("status"),
                "critical": bool(dependency.get("critical")),
            }
            if target_type in MASTER_TYPES or target_type in REFERENCE_CUSTOMIZING_TYPES:
                category = _initial_category("MASTER_DATA" if target_type in MASTER_TYPES else "CUSTOMIZING", target_type)
                target_key = builder.add(target_type, phrase, category, books, scenarios, dep_evidence, evidence_path="dependencies")
            else:
                value = f"{obj['scenario_id'] or obj['object_id']}|{dependency.get('relation')}|{phrase}"
                target_key = builder.add(target_type, value, "RUNTIME_DEPENDENCY", books, scenarios, dep_evidence, evidence_path="dependencies")
            builder.entries[source_key]["depends_on_keys"].add(target_key)

        for requirement_type, value, path in _iter_leaf_references(obj["data"]):
            # document_type is contextual; all canonical uses here are sales documents.
            if path.endswith(".document_type"):
                requirement_type = "SALES_DOCUMENT_TYPE"
            ref_evidence = {
                **base_evidence,
                "kind": "CANONICAL_FIELD_REFERENCE",
            }
            category = _initial_category(
                "MASTER_DATA" if requirement_type in MASTER_TYPES else "CUSTOMIZING",
                requirement_type,
            )
            target_key = builder.add(requirement_type, value, category, books, scenarios, ref_evidence, evidence_path=path)
            if target_key != source_key:
                builder.entries[source_key]["depends_on_keys"].add(target_key)

        for product, unit, path in _iter_product_units(obj["data"]):
            association = f"{product}|{unit}"
            unit_evidence = {
                **base_evidence,
                "kind": "PRODUCT_UNIT_ASSOCIATION",
                "product": product,
                "alternative_unit": unit,
                "limitation": "Existence of the unit for another product does not prove this association.",
            }
            target_key = builder.add("PRODUCT_UNIT_OF_MEASURE", association, "MASTER_DATA_PER_BOOK", books, scenarios, unit_evidence, evidence_path=path)
            builder.entries[source_key]["depends_on_keys"].add(target_key)

    requirements = builder.finalize()

    # Add the confirmed live limitation without creating FG228 as a Book requirement.
    live_context = {
        "environment": "TEST 600",
        "sap_writes_performed": False,
        "confirmed_product_uom_contract": {
            "service": "API_PRODUCT_SRV",
            "entity_set": "A_ProductUnitsOfMeasure",
            "keys": ["Product", "AlternativeUnit"],
            "observed_pair": {"Product": "FG228", "AlternativeUnit": "PC", "status": "EXISTS"},
            "scope_limitation": "The FG228/PC observation is not evidence for any absent Book product.",
        },
    }
    category_counter = Counter(r["category"] for r in requirements)
    scope_counter = Counter(r["scope"] for r in requirements)
    status_counter = Counter(r["current_known_sap_status"] for r in requirements)
    risk_counter = Counter(r["risk"] for r in requirements)
    counts = {
        "total": len(requirements),
        "by_category": {key: category_counter[key] for key in sorted(CATEGORIES)},
        "by_scope": {key: scope_counter[key] for key in sorted(SCOPES)},
        "by_sap_status": {key: status_counter[key] for key in sorted(SAP_STATUSES)},
        "by_risk": {key: risk_counter[key] for key in sorted(RISKS)},
        "by_book": {book: sum(book in r["source_book"] for r in requirements) for book in BOOKS},
    }
    return {
        "inventory_version": "1.0.0",
        "generation_policy": "OFFLINE_DETERMINISTIC_CANONICAL_AND_LOCAL_CONTRACTS_ONLY",
        "source": {
            "canonical_objects": str(CANONICAL_PATH.relative_to(ROOT)).replace("\\", "/"),
            "canonical_sha256": _sha256(CANONICAL_PATH),
            "interface_registry": str(REGISTRY_PATH.relative_to(ROOT)).replace("\\", "/"),
            "interface_registry_sha256": _sha256(REGISTRY_PATH),
            "canonical_objects_modified": False,
            "sap_connection_performed": False,
        },
        "live_evidence_context": live_context,
        "summary": counts,
        "requirements": requirements,
    }


def _md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _top_blockers(requirements: list[dict[str, Any]], limit: int = 20) -> list[dict[str, Any]]:
    status_rank = {"MISSING": 0, "UNKNOWN": 1, "EXISTS": 2}
    scope_rank = {"GLOBAL": 0, "BOOK": 1, "PER_USER": 2}
    candidates = [r for r in requirements if r["risk"] == "HIGH" or r["current_known_sap_status"] == "MISSING"]
    return sorted(
        candidates,
        key=lambda r: (status_rank[r["current_known_sap_status"]], scope_rank[r["scope"]], r["type"], r["value_template"]),
    )[:limit]


def render_report(inventory: dict[str, Any]) -> str:
    requirements = inventory["requirements"]
    summary = inventory["summary"]
    top = _top_blockers(requirements)
    lines = [
        "# Phase 4 — Prérequis de l’environnement de formation SAP",
        "",
        "## Résumé exécutif",
        "",
        f"L’inventaire consolide **{summary['total']} requirements déterministes** issus des 201 objets canoniques des cinq Books et de leurs dépendances explicites. Aucun appel ni aucune écriture SAP n’a été effectué, et `data/validated/canonical_objects.json` est resté immuable.",
        "",
        f"- Portée : **{summary['by_scope'].get('GLOBAL', 0)} GLOBAL**, **{summary['by_scope'].get('BOOK', 0)} BOOK**, **{summary['by_scope'].get('PER_USER', 0)} PER_USER**.",
        f"- État TEST 600 connu : **{summary['by_sap_status'].get('EXISTS', 0)} EXISTS**, **{summary['by_sap_status'].get('MISSING', 0)} MISSING**, **{summary['by_sap_status'].get('UNKNOWN', 0)} UNKNOWN**.",
        f"- Risque : **{summary['by_risk'].get('HIGH', 0)} HIGH**, **{summary['by_risk'].get('MEDIUM', 0)} MEDIUM**, **{summary['by_risk'].get('LOW', 0)} LOW**.",
        "- Une valeur `UNKNOWN` signifie qu’aucune preuve locale/live déterministe ne permet de conclure. Elle ne signifie pas que l’objet est absent.",
        "- Pour un template `##`, un statut live lié à l’utilisateur `00` ne prouve rien pour `01–99`; cette limite est attachée à la preuve.",
        "",
        "### A. Socle global manquant",
        "",
        "L’organisation commerciale `1010` est confirmée **MISSING** dans TEST 600. Les objets partagés qui en dépendent restent donc bloqués même si le canal `10` et le secteur d’activité `00` existent.",
        "",
        "### B. Données de base par Book",
        "",
        "Les couples client/article explicitement testés pour l’utilisateur `00` sont absents : S4600 (`T-S50A00`, `T-MS100`), S4610 (`C610-A00`, `P610-500`), S4615 (`C615-D00`, `P615-400`), S4620 (`C620-A00`, `P620-100`) et S4650 (`C650-A00`, `P650-100`). Les autres masters restent `UNKNOWN`.",
        "",
        "### C. Données par utilisateur",
        "",
        "Les templates contenant `##` sont conservés tels quels et classés `PER_USER`. Ils doivent être résolus uniquement dans une copie runtime avec un code `00–99`, puis créés ou étendus seulement pour les utilisateurs de formation actifs.",
        "",
        "### D. Customizing nécessaire",
        "",
        "Le customizing couvre notamment les domaines commerciaux, sites/points d’expédition/magasins, types de documents, pricing, détermination de comptes, copy control, textes, outputs et extensions. L’absence d’interface exacte dans le registre local est signalée; aucun endpoint n’est déduit d’un simple nom.",
        "",
        "### E. Objets transactionnels créés pendant les workflows",
        "",
        "Les commandes, livraisons, sorties de marchandises, factures, règlements/références, documents d’achat et de settlement sont `RUNTIME_CREATE`. Leurs liens vers les documents précédents restent des dépendances explicites; aucun numéro n’est inventé.",
        "",
        "### F. Éléments non automatisables ou inconnus",
        "",
        "Les requirements sans contrat/interface exact, les références runtime non résolues et les valeurs non vérifiées restent `UNKNOWN` ou `BLOCKED`. `A_ProductUnitsOfMeasure` et ses clés `Product + AlternativeUnit` sont confirmés. L’observation `FG228/PC` ne valide pas `PC` pour les produits absents des Books.",
        "",
        "## Comptages",
        "",
        "### Par catégorie",
        "",
        "| Catégorie | Nombre |",
        "|---|---:|",
    ]
    for key, value in summary["by_category"].items():
        lines.append(f"| {key} | {value} |")
    lines += ["", "### Par Book (un requirement partagé peut compter dans plusieurs Books)", "", "| Book | Requirements |", "|---|---:|"]
    for book, value in summary["by_book"].items():
        lines.append(f"| {book} | {value} |")

    lines += [
        "",
        "## Top 20 blockers",
        "",
        "| # | Requirement | Type | Valeur/template | Scope | Statut SAP | Risque | Stratégie |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for index, req in enumerate(top, 1):
        lines.append(
            f"| {index} | `{req['requirement_id']}` | {req['type']} | `{_md_escape(req['value_template'])}` | {req['scope']} | {req['current_known_sap_status']} | {req['risk']} | {req['provisioning_strategy']} |"
        )

    lines += [
        "",
        "## Ordre de provisioning recommandé",
        "",
        "1. **GLOBAL CUSTOMIZING** — créer/valider le socle organisationnel partagé, puis les sales areas.",
        "2. **PLANTS / SHIPPING / WAREHOUSE** — sites, points d’expédition, magasins, numéros d’entrepôt et affectations.",
        "3. **DOCUMENT TYPES** — types de documents commerciaux, livraisons, facturation et contrôles de copie.",
        "4. **PRICING / ACCOUNT / OUTPUT CONFIG** — tables, séquences, procédures, déterminations de comptes, textes, outputs et extensions.",
        "5. **MASTER DATA SHARED / PER BOOK** — clients, fournisseurs, articles, hiérarchies, contrats et conditions.",
        "6. **SALES-AREA EXTENSIONS / PRODUCT UoM** — étendre les masters aux vues requises et vérifier chaque association `Product + AlternativeUnit`.",
        "7. **PER USER** — résoudre `##` dans une copie runtime et provisionner uniquement les codes de formation actifs.",
        "8. **WORKFLOW** — exécuter les objets transactionnels dans l’ordre du graphe, en injectant les identifiants créés au runtime.",
        "",
        "## Règles de décision",
        "",
        "- Déduplication : uniquement sur `(type, valeur/template exacte, nature prerequisite/transaction)`. Les objets complexes sans clé source complète conservent leur `canonical_object_id` comme identité.",
        "- `EXISTS`/`MISSING` provient exclusivement des résultats live TEST 600 fournis; aucune existence n’est inférée du canonical.",
        "- `UNKNOWN` reste fail-closed pour une exécution. Une interface candidate `NO_INTERFACE_FOUND` n’est pas remplacée par un endpoint supposé.",
        "- `canonical_objects.json` n’est ni réécrit ni enrichi par cet inventaire.",
        "",
        "## Inventaire complet",
        "",
        "| Requirement | Catégorie | Type | Valeur/template | Books | Scope | SAP | Provisioning | Risque |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for req in requirements:
        lines.append(
            f"| `{req['requirement_id']}` | {req['category']} | {req['type']} | `{_md_escape(req['value_template'])}` | {', '.join(req['source_book'])} | {req['scope']} | {req['current_known_sap_status']} | {req['provisioning_strategy']} | {req['risk']} |"
        )

    lines += [
        "",
        "## Fichiers et validation",
        "",
        "- Inventaire machine-readable : `data/requirements/training_environment_requirements.json`",
        "- Générateur déterministe : `scripts/build_training_requirements.py`",
        "- Tests : `tests/test_phase4_training_requirements.py`",
        "",
        "Le détail complet des requirements, sources, dépendances, interfaces candidates et preuves est dans le fichier JSON afin d’éviter un rapport Markdown illisible de plusieurs centaines de lignes.",
        "",
    ]
    return "\n".join(lines)


def write_outputs() -> dict[str, Any]:
    inventory = build_inventory()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(inventory, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(render_report(inventory), encoding="utf-8")
    return inventory


if __name__ == "__main__":
    output = write_outputs()
    print(json.dumps(output["summary"], ensure_ascii=False, indent=2, sort_keys=True))
