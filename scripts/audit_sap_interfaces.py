"""Build the Phase 2A SAP interface registry from local inventories only.

This script performs no network or SAP access. Every named interface is checked
for an exact match in the supplied XLSX inventories before output is written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ODATA_PATH = ROOT / "inputs/sap_inventory/odata_services.xlsx"
RFC_PATH = ROOT / "inputs/sap_inventory/rfc_remote_functions.xlsx"
CANONICAL_PATH = ROOT / "data/validated/canonical_objects.json"
TAXONOMY_PATH = ROOT / "taxonomy/object_types.yaml"
SCHEMA_INDEX_PATH = ROOT / "schemas/index.json"
OUTPUT_PATH = ROOT / "mappings/sap/interface_registry.yaml"
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def column_number(reference: str) -> int:
    letters = re.match(r"[A-Z]+", reference).group(0)
    number = 0
    for letter in letters:
        number = number * 26 + ord(letter) - 64
    return number


def read_xlsx(path: Path) -> dict[str, list[list[object]]]:
    """Read stored worksheet values using only Python's standard library."""
    with zipfile.ZipFile(path) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for entry in root.findall("m:si", NS):
                shared.append("".join(node.text or "" for node in entry.iterfind(".//m:t", NS)))
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {entry.attrib["Id"]: entry.attrib["Target"] for entry in relationships}
        result = {}
        for sheet in workbook.findall("m:sheets/m:sheet", NS):
            target = targets[sheet.attrib[f"{{{NS['r']}}}id"]].lstrip("/")
            if not target.startswith("xl/"):
                target = "xl/" + target
            xml = ET.fromstring(archive.read(target))
            rows = []
            for row in xml.findall("m:sheetData/m:row", NS):
                values = {}
                for cell in row.findall("m:c", NS):
                    index = column_number(cell.attrib["r"])
                    cell_type = cell.attrib.get("t")
                    if cell_type == "inlineStr":
                        value = "".join(node.text or "" for node in cell.iterfind(".//m:t", NS))
                    else:
                        node = cell.find("m:v", NS)
                        value = None if node is None else node.text
                        if value is not None and cell_type == "s":
                            value = shared[int(value)]
                    values[index] = value
                rows.append([values.get(i) for i in range(1, max(values, default=0) + 1)])
            result[sheet.attrib["name"]] = rows
        return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def candidate(kind: str, inventory: str | None, name: str | None, operation: str,
              rationale: str, *, external_name: str | None = None,
              version: str | None = None) -> dict:
    result = {
        "classification": kind,
        "inventory": inventory,
        "exact_name": name,
        "operation": operation,
        "evidence_basis": rationale,
    }
    if external_name:
        result["external_name"] = external_name
    if version:
        result["version"] = version
    return result


def odata(name: str, external: str, operation: str, rationale: str,
          version: str = "1", kind: str = "ODATA") -> dict:
    return candidate(kind, "odata_services.xlsx", name, operation, rationale,
                     external_name=external, version=version)


def rfc(name: str, operation: str, rationale: str,
        kind: str = "STANDARD_BAPI") -> dict:
    return candidate(kind, "rfc_remote_functions.xlsx", name, operation, rationale)


def no_match() -> dict:
    return candidate(
        "NO_INTERFACE_FOUND", None, None, "NONE",
        "No object-specific candidate was found in either supplied inventory.",
    )


def no_execution() -> dict:
    return candidate(
        "NO_EXECUTION_REQUIRED", None, None, "REFERENCE_ONLY",
        "The canonical object records a dependency/reference and must not trigger a posting.",
    )


def specifications() -> dict[str, dict]:
    """Curated matches; exact names are validated later against the workbooks."""
    exact = "Exact object-specific inventory name; no generic name-only fallback used."
    lookup = "Exact reference/customizing interface restricted to validation or lookup."
    return {
        "SALES_ORGANIZATION": {"candidates": [odata("ZAPI_SALESORGANIZATION_SRV", "API_SALESORGANIZATION_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY"), rfc("BAPI_SALESORG_GET_DETAIL", "LOOKUP", lookup, "LOOKUP_ONLY")], "preferred": 0},
        "DISTRIBUTION_CHANNEL": {"candidates": [odata("ZAPI_DISTRIBUTIONCHANNEL_SRV", "API_DISTRIBUTIONCHANNEL_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY")], "preferred": 0},
        "SALES_DIVISION": {"candidates": [odata("ZAPI_DIVISION_SRV", "API_DIVISION_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY"), rfc("BAPI_DIVISION_GET_DETAIL", "LOOKUP", lookup, "LOOKUP_ONLY")], "preferred": 0},
        "SALES_AREA": {"candidates": [rfc("BAPI_SALES_AREAS_GET", "LOOKUP", lookup, "LOOKUP_ONLY")], "preferred": 0},
        "SHIPPING_POINT": {"candidates": [rfc("/SMERP/MM_CTSHIPPINGPOINT_GET", "LOOKUP", "Exact shipping-point lookup; specialized RFC, not a standard BAPI.", "LOOKUP_ONLY")], "preferred": 0},
        "CONDITION_TYPE": {"candidates": [odata("ZAPI_SLSPRICINGCONDITIONTYPE_SRV", "API_SLSPRICINGCONDITIONTYPE_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY")], "preferred": 0},
        "CONDITION_TABLE": {"candidates": [no_match()], "preferred": 0},
        "ACCESS_SEQUENCE": {"candidates": [no_match()], "preferred": 0},
        "PRICING_PROCEDURE": {"candidates": [odata("ZAPI_SLSPRICINGPROCEDURE_SRV", "API_SLSPRICINGPROCEDURE_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY")], "preferred": 0},
        "PRICING_PROCEDURE_DETERMINATION": {"candidates": [no_match()], "preferred": 0},
        "ACCOUNT_DETERMINATION": {"candidates": [no_match()], "preferred": 0},
        "COPY_CONTROL": {"candidates": [no_match()], "preferred": 0},
        "TEXT_DETERMINATION": {"candidates": [no_match()], "preferred": 0},
        "OUTPUT_DETERMINATION": {"candidates": [no_match()], "preferred": 0},
        "SHARED_MASTER_DATA_ASSIGNMENT": {"candidates": [no_match()], "preferred": 0},
        "EXTENSION_CONFIGURATION": {"candidates": [no_match()], "preferred": 0},
        "BUSINESS_PARTNER": {"candidates": [odata("ZAPI_BUSINESS_PARTNER", "API_BUSINESS_PARTNER", "MAINTAIN", exact), rfc("BAPI_BUPA_CREATE_FROM_DATA", "CREATE", exact)], "preferred": 0},
        "MATERIAL": {"candidates": [rfc("BAPI_MATERIAL_SAVEDATA", "MAINTAIN", exact), odata("ZAPI_PRODUCT_SRV", "API_PRODUCT_SRV", "MAINTAIN", "Exact product API; material is represented as product in this inventory.")], "preferred": 0},
        "CUSTOMER_MATERIAL_INFO": {"candidates": [odata("ZAPI_CUSTOMER_MATERIAL_SRV", "API_CUSTOMER_MATERIAL_SRV", "MAINTAIN", exact), rfc("BAPI_CUSTMATINFO_GETDETAILM", "LOOKUP", lookup, "LOOKUP_ONLY")], "preferred": 0},
        "PRICING_CONDITION": {"candidates": [odata("ZSD_PRICING_CONDITIONRECORD_SRV", "SD_PRICING_CONDITIONRECORD_SRV", "MAINTAIN", exact)], "preferred": 0},
        "CUSTOMER_HIERARCHY": {"candidates": [rfc("BAPI_CUSTOMER_HIERARCHIE_INS", "CREATE", exact), rfc("BAPI_CUSTOMER_HIERARCHIE_UPD", "UPDATE", exact)], "preferred": 0},
        "CONDITION_CONTRACT": {"candidates": [rfc("BAPI_CONDITION_CONTRACT_CREATE", "CREATE", exact), rfc("BAPI_CONDITION_CONTRACT_CHANGE", "UPDATE", exact)], "preferred": 0},
        "INQUIRY": {"candidates": [odata("ZAPI_SALES_INQUIRY_SRV", "API_SALES_INQUIRY_SRV", "MAINTAIN", exact), rfc("BAPI_INQUIRY_CREATEFROMDATA2", "CREATE", exact)], "preferred": 0},
        "QUOTATION": {"candidates": [odata("ZAPI_SALES_QUOTATION_SRV", "API_SALES_QUOTATION_SRV", "MAINTAIN", exact), rfc("BAPI_QUOTATION_CREATEFROMDATA2", "CREATE", exact)], "preferred": 0},
        "SALES_ORDER": {"candidates": [odata("ZAPI_SALES_ORDER_SRV", "API_SALES_ORDER_SRV", "MAINTAIN", exact), rfc("BAPI_SALESORDER_CREATEFROMDAT2", "CREATE", exact)], "preferred": 0},
        "CREDIT_MEMO_REQUEST": {"candidates": [odata("ZAPI_CREDIT_MEMO_REQUEST_SRV", "API_CREDIT_MEMO_REQUEST_SRV", "MAINTAIN", exact)], "preferred": 0},
        "RETURN_ORDER": {"candidates": [odata("ZAPI_CUSTOMER_RETURN_SRV", "API_CUSTOMER_RETURN_SRV", "MAINTAIN", exact), rfc("BAPI_CUSTOMERRETURN_CREATE", "CREATE", exact)], "preferred": 0},
        "OUTBOUND_DELIVERY": {"candidates": [odata("ZAPI_OUTBOUND_DELIVERY_SRV", "API_OUTBOUND_DELIVERY_SRV", "MAINTAIN", exact, "2"), odata("ZAPI_OUTBOUND_DELIVERY_SRV", "API_OUTBOUND_DELIVERY_SRV", "MAINTAIN", exact, "1"), rfc("BAPI_OUTB_DELIVERY_CREATE_SLS", "CREATE_FROM_SALES_ORDER", exact)], "preferred": 0},
        "INBOUND_DELIVERY": {"candidates": [odata("ZAPI_INBOUND_DELIVERY_SRV", "API_INBOUND_DELIVERY_SRV", "MAINTAIN", exact, "2"), odata("ZAPI_INBOUND_DELIVERY_SRV", "API_INBOUND_DELIVERY_SRV", "MAINTAIN", exact, "1")], "preferred": 0},
        "GOODS_ISSUE": {"candidates": [rfc("BAPI_GOODSMVT_CREATE", "POST", "Exact goods-movement posting BAPI; goods issue is a goods-movement operation."), odata("ZAPI_MATERIAL_DOCUMENT_SRV", "API_MATERIAL_DOCUMENT_SRV", "POST", "Exact material-document API; goods issue produces a material document.")], "preferred": 0},
        "WAREHOUSE_TASK": {"candidates": [odata("ZAPI_WAREHOUSE_ORDER_TASK", "API_WAREHOUSE_ORDER_TASK", "MAINTAIN", exact), rfc("/SCWM/TO_CREATE", "CREATE", exact, "RFC_FUNCTION")], "preferred": 0},
        "BILLING": {"candidates": [odata("ZAPI_BILLING_DOCUMENT_SRV", "API_BILLING_DOCUMENT_SRV", "MAINTAIN", exact), rfc("BAPI_BILLINGDOC_CREATEMULTIPLE", "CREATE", exact)], "preferred": 0},
        "SETTLEMENT_DOCUMENT": {"candidates": [rfc("BAPI_CONDITION_CONTRACT_SETTLE", "SETTLE", "Exact condition-contract settlement BAPI matching the source scenario."), rfc("WB2R_SETTLEMENT_RFC", "SETTLE", exact, "RFC_FUNCTION")], "preferred": 0},
        "COMPANY_CODE": {"candidates": [odata("ZAPI_COMPANYCODE_SRV", "API_COMPANYCODE_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY"), rfc("BAPI_COMPANYCODE_GETDETAIL", "LOOKUP", lookup, "LOOKUP_ONLY")], "preferred": 0},
        "PLANT": {"candidates": [odata("ZAPI_PLANT_SRV", "API_PLANT_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY")], "preferred": 0},
        "STORAGE_LOCATION": {"candidates": [odata("ZAPI_STORAGELOCATION_SRV", "API_STORAGELOCATION_SRV", "LOOKUP", lookup, kind="LOOKUP_ONLY")], "preferred": 0},
        "WAREHOUSE_NUMBER": {"candidates": [odata("ZAPI_WAREHOUSE", "API_WAREHOUSE", "LOOKUP", lookup, kind="LOOKUP_ONLY")], "preferred": 0},
        "PURCHASE_ORDER_REFERENCE": {"candidates": [odata("ZAPI_PURCHASEORDER_PROCESS_SRV", "API_PURCHASEORDER_PROCESS_SRV", "LOOKUP", "Exact purchase-order service, restricted to reference validation for this canonical type.", kind="LOOKUP_ONLY")], "preferred": 0},
        "PAYMENT_REFERENCE": {"candidates": [no_execution()], "preferred": 0},
    }


def inventory_indexes() -> tuple[dict[tuple[str, str], dict], dict[str, dict]]:
    odata_index = {}
    for row in read_xlsx(ODATA_PATH)["Data"]:
        if len(row) >= 6 and row[2]:
            odata_index[(str(row[2]), str(row[3]))] = {
                "technical_name": row[2], "version": str(row[3]), "external_name": row[5]
            }
    rfc_index = {}
    for row in read_xlsx(RFC_PATH)["Data"]:
        if len(row) >= 2 and row[1]:
            rfc_index[str(row[1])] = {
                "function_name": row[1], "program": row[2] if len(row) > 2 else None
            }
    return odata_index, rfc_index


def load_canonical() -> tuple[list[dict], dict[str, str]]:
    payload = json.loads(CANONICAL_PATH.read_text(encoding="utf-8"))
    objects = payload["objects"]
    classifications = {}
    for obj in objects:
        previous = classifications.setdefault(obj["object_type"], obj["classification"])
        if previous != obj["classification"]:
            raise ValueError(f"Conflicting classification for {obj['object_type']}")
    return objects, classifications


def build_registry() -> dict:
    objects, classifications = load_canonical()
    specs = specifications()
    schema_index = json.loads(SCHEMA_INDEX_PATH.read_text(encoding="utf-8"))
    taxonomy_types = set(re.findall(r"\b[A-Z][A-Z0-9_]+\b", TAXONOMY_PATH.read_text(encoding="utf-8")))
    taxonomy_types -= {"CUSTOMIZING", "MASTER_DATA", "TRANSACTION", "REFERENCE_DATA"}
    if taxonomy_types != set(classifications) or set(schema_index) != set(classifications):
        raise ValueError("Canonical dataset, taxonomy, and schema index do not cover the same object types")
    for object_type, classification in classifications.items():
        if schema_index[object_type]["classification"] != classification:
            raise ValueError(f"Schema classification mismatch for {object_type}")
        if not (ROOT / schema_index[object_type]["schema"]).is_file():
            raise ValueError(f"Missing schema for {object_type}")
    if set(specs) != set(classifications):
        missing = sorted(set(classifications) - set(specs))
        extra = sorted(set(specs) - set(classifications))
        raise ValueError(f"Registry coverage mismatch; missing={missing}, extra={extra}")
    odata_index, rfc_index = inventory_indexes()
    counts = Counter(obj["object_type"] for obj in objects)
    ready = Counter(obj["object_type"] for obj in objects if obj["readiness_status"] == "READY")
    blocked = Counter(obj["object_type"] for obj in objects if obj["readiness_status"] == "BLOCKED")
    entries = {}
    for object_type in sorted(specs):
        spec = specs[object_type]
        for item in spec["candidates"]:
            if item["inventory"] == "odata_services.xlsx":
                key = (item["exact_name"], item["version"])
                if key not in odata_index:
                    raise ValueError(f"Missing exact OData evidence: {key}")
                if odata_index[key]["external_name"] != item["external_name"]:
                    raise ValueError(f"External-name mismatch for {key}")
            elif item["inventory"] == "rfc_remote_functions.xlsx":
                if item["exact_name"] not in rfc_index:
                    raise ValueError(f"Missing exact RFC evidence: {item['exact_name']}")
        preferred = spec["candidates"][spec["preferred"]]
        entries[object_type] = {
            "canonical_classification": classifications[object_type],
            "canonical_object_count": counts[object_type],
            "ready_count": ready[object_type],
            "blocked_count": blocked[object_type],
            "resolution": "UNRESOLVED" if preferred["classification"] == "NO_INTERFACE_FOUND" else "RESOLVED",
            "candidates": spec["candidates"],
            "preferred_interface": preferred,
        }
    return {
        "registry_version": "1.0.0",
        "phase": "2A",
        "generated_by": "scripts/audit_sap_interfaces.py",
        "source_policy": "LOCAL_INVENTORY_EXACT_MATCH_ONLY",
        "sap_connection_performed": False,
        "mapper_implemented": False,
        "inputs": {
            "canonical_objects": {"path": "data/validated/canonical_objects.json", "sha256": sha256(CANONICAL_PATH)},
            "odata_inventory": {"path": "inputs/sap_inventory/odata_services.xlsx", "sha256": sha256(ODATA_PATH)},
            "rfc_inventory": {"path": "inputs/sap_inventory/rfc_remote_functions.xlsx", "sha256": sha256(RFC_PATH)},
            "taxonomy": {"path": "taxonomy/object_types.yaml", "sha256": sha256(TAXONOMY_PATH)},
            "schema_index": {"path": "schemas/index.json", "sha256": sha256(SCHEMA_INDEX_PATH)},
        },
        "allowed_candidate_classifications": ["ODATA", "STANDARD_BAPI", "RFC_FUNCTION", "LOOKUP_ONLY", "NO_INTERFACE_FOUND", "NO_EXECUTION_REQUIRED"],
        "object_types": entries,
    }


def render_registry(registry: dict) -> str:
    # JSON is a strict subset of YAML 1.2 and provides stable serialization.
    return json.dumps(registry, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate determinism without writing")
    args = parser.parse_args()
    registry = build_registry()
    rendered = render_registry(registry)
    if args.check:
        if not OUTPUT_PATH.exists() or OUTPUT_PATH.read_text(encoding="utf-8") != rendered:
            raise SystemExit("interface registry is missing or stale")
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    unresolved = [name for name, item in registry["object_types"].items() if item["resolution"] == "UNRESOLVED"]
    print(json.dumps({"object_types": len(registry["object_types"]), "unresolved": unresolved}, indent=2))


if __name__ == "__main__":
    main()
