"""Offline, metadata-checked API_BUSINESS_PARTNER root-create contract.

This module prepares a minimal root payload only. It never sends HTTP. The
installed metadata and an unambiguous anti-duplicate lookup are prerequisites
for registering a writable route.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from src.sap_runtime.transport import HttpResponse
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


EDM = "http://schemas.microsoft.com/ado/2008/09/edm"
SAP = "http://www.sap.com/Protocols/SAPData"

ROOT_FIELDS = {
    "bp_grouping": "BusinessPartnerGrouping",
    "bp_category": "BusinessPartnerCategory",
    "training_name": "OrganizationBPName1",
    "duplicate_key": "SearchTerm1",
}
OPTIONAL_ROOT_FIELDS = {"language": "Language"}

CREATION_ENTITIES = (
    "A_BusinessPartner", "A_BusinessPartnerAddress", "A_BusinessPartnerRole",
    "A_Customer", "A_CustomerCompany", "A_CustomerSalesArea",
)


def inspect_creation_metadata(
    metadata_xml: bytes | str, *, entities: tuple[str, ...] = CREATION_ENTITIES,
) -> dict[str, Any]:
    """Summarize only installed OData V2 entity and property evidence."""
    root = ET.fromstring(metadata_xml)
    result = {}
    for entity_name in entities:
        entity_sets = [node for node in root.iter() if node.tag == f"{{{EDM}}}EntitySet"
                       and node.get("Name") == entity_name]
        if len(entity_sets) != 1:
            raise ValueError(f"Exactly one {entity_name} EntitySet is required")
        entity_set = entity_sets[0]
        entity_type_name = (entity_set.get("EntityType") or "").split(".")[-1]
        entity_types = [node for node in root.iter() if node.tag == f"{{{EDM}}}EntityType"
                        and node.get("Name") == entity_type_name]
        if len(entity_types) != 1:
            raise ValueError(f"{entity_name} EntityType is not resolved")
        entity_type = entity_types[0]
        annotation = entity_set.get(f"{{{SAP}}}creatable")
        result[entity_name] = {
            "entity_set": entity_name,
            "entity_type": entity_type_name,
            # An absent SAP annotation does not explicitly forbid create, but
            # does not prove that a POST will be accepted or authorized.
            "create_annotation": annotation,
            "metadata_allows_create": annotation != "false",
            "keys": [node.get("Name") for node in entity_type.findall(
                f"{{{EDM}}}Key/{{{EDM}}}PropertyRef")],
            "fields": {
                node.get("Name"): {
                    "edm_type": node.get("Type"),
                    "nullable": node.get("Nullable") != "false",
                    "creatable": node.get(f"{{{SAP}}}creatable") != "false",
                    "max_length": node.get("MaxLength"),
                }
                for node in entity_type.findall(f"{{{EDM}}}Property")
            },
            "navigation": [node.get("Name") for node in entity_type.findall(
                f"{{{EDM}}}NavigationProperty")],
        }
    return result


def inspect_root_metadata(metadata_xml: bytes | str) -> dict[str, Any]:
    return inspect_creation_metadata(metadata_xml, entities=("A_BusinessPartner",))["A_BusinessPartner"]


def prepare_bp_root(values: dict[str, Any], metadata_xml: bytes | str | None) -> dict[str, Any]:
    """Produce only proven fields; internal numbering never sends Book ID."""
    missing = [name for name in ROOT_FIELDS if not isinstance(values.get(name), str) or not values[name].strip()]
    if missing:
        return {"status": "BLOCKED_DATA", "missing": missing, "payload": None}
    if values.get("business_partner") not in (None, ""):
        return {"status": "BLOCKED_CONTRACT", "reason": "External BP number is not proven for the selected grouping", "payload": None}
    if values.get("logical_id") and values["duplicate_key"] != values["logical_id"]:
        return {"status": "BLOCKED_DATA", "reason": "SearchTerm1 must equal the approved logical ID", "payload": None}
    if metadata_xml is None:
        return {"status": "BLOCKED_METADATA", "reason": "Installed API_BUSINESS_PARTNER metadata is not stored", "payload": None}
    contract = inspect_root_metadata(metadata_xml)
    if not contract["metadata_allows_create"]:
        return {"status": "BLOCKED_CONTRACT", "reason": "A_BusinessPartner is not creatable", "payload": None}
    payload = {}
    for source, field in {**ROOT_FIELDS, **OPTIONAL_ROOT_FIELDS}.items():
        if source in OPTIONAL_ROOT_FIELDS and values.get(source) in (None, ""):
            continue
        property_contract = contract["fields"].get(field)
        if not property_contract or property_contract["edm_type"] != "Edm.String" or not property_contract["creatable"]:
            return {"status": "BLOCKED_CONTRACT", "reason": f"{field} is absent or non-creatable", "payload": None}
        value = values[source]
        max_length = property_contract["max_length"]
        if max_length and max_length.isdigit() and len(value) > int(max_length):
            return {"status": "BLOCKED_DATA", "reason": f"{field} exceeds MaxLength", "payload": None}
        payload[field] = value
    return {
        "status": "PAYLOAD_PREPARED", "entity_set": "A_BusinessPartner", "payload": payload,
        "data_ready": True,
        "write_route_ready": False,
        "duplicate_checks": duplicate_check_filters(values["duplicate_key"], values["training_name"]),
        "later_extensions": {
            "address": {"Country": values.get("country")},
            "roles": ["FLCU00", "FLCU01"],
            "company": "A_CustomerCompany",
            "sales_area": {"entity_set": "A_CustomerSalesArea", "Currency": values.get("sales_currency")},
        },
        "remaining_contracts": [
            "final duplicate lookup by approved SearchTerm1 and name immediately before write",
            "explicit scoped approval and POST authorization for BPAB root creation",
            "generated BusinessPartner ID capture and fresh-session readback",
            "approved address, FLCU00/FLCU01, company and sales-area values",
        ],
    }


def duplicate_check_filters(logical_id: str, training_name: str) -> dict[str, str]:
    """Three exact GET checks; absence cannot prove no unlabelled internal BP."""
    def literal(value: str) -> str:
        return "'" + value.replace("'", "''") + "'"

    return {
        "external_key": f"BusinessPartner eq {literal(logical_id)}",
        "project_marker": f"SearchTerm1 eq {literal(logical_id)}",
        "exact_name": f"OrganizationBPName1 eq {literal(training_name)}",
    }


def capture_generated_bp_id(response: HttpResponse) -> str:
    """Accept only an explicit SAP-returned root key, never a proposed ID."""
    if response.status not in {200, 201}:
        raise ValueError("BP root creation response is not a confirmed success")
    data = response.json().get("d")
    sap_id = data.get("BusinessPartner") if isinstance(data, dict) else None
    if not isinstance(sap_id, str) or not sap_id or len(sap_id) > 10 or "##" in sap_id:
        raise ValueError("BP root response lacks an unambiguous generated BusinessPartner key")
    return sap_id


def generated_bp_readback_keys(sap_id: str) -> dict[str, str]:
    """Exact GET keys for a new independent session; no network call here."""
    if not isinstance(sap_id, str) or not sap_id or len(sap_id) > 10 or "'" in sap_id:
        raise ValueError("Invalid generated BusinessPartner key")
    return {
        "root": f"A_BusinessPartner('{sap_id}')",
        "customer": f"A_Customer('{sap_id}')",
        "flcu00": f"A_BusinessPartnerRole(BusinessPartner='{sap_id}',BusinessPartnerRole='FLCU00')",
        "flcu01": f"A_BusinessPartnerRole(BusinessPartner='{sap_id}',BusinessPartnerRole='FLCU01')",
    }


def verify_generated_bp_readback(
    response: HttpResponse, sap_id: str, expected_payload: dict[str, str],
) -> bool:
    """Require an independent GET to match the returned key and root fields."""
    if response.status != 200:
        return False
    data = response.json().get("d")
    if not isinstance(data, dict) or data.get("BusinessPartner") != sap_id:
        return False
    return all(data.get(field) == value for field, value in expected_payload.items())


def assess_bp_root_identity_readback(
    response: HttpResponse, sap_id: str, expected_payload: dict[str, str],
    metadata_xml: bytes | str,
) -> dict[str, Any]:
    """Verify persisted identity; record optional Language without hiding drift."""
    contract = inspect_root_metadata(metadata_xml)
    mandatory = {"BusinessPartnerGrouping", "BusinessPartnerCategory",
                 "OrganizationBPName1", "SearchTerm1"}
    if not mandatory.issubset(expected_payload) or response.status != 200:
        return {"verified": False, "reason": "Mandatory payload or GET missing"}
    data = response.json().get("d")
    if not isinstance(data, dict) or data.get("BusinessPartner") != sap_id:
        return {"verified": False, "reason": "Generated BusinessPartner key mismatch"}
    mismatches = {}
    optional_mismatches = {}
    for field, expected in expected_payload.items():
        actual = data.get(field)
        if actual == expected:
            continue
        difference = {"expected": expected, "observed": actual}
        field_contract = contract["fields"].get(field)
        if field == "Language" and field_contract and field_contract["nullable"]:
            optional_mismatches[field] = difference
        else:
            mismatches[field] = difference
    return {
        "verified": not mismatches,
        "mandatory_mismatches": mismatches,
        "optional_mismatches": optional_mismatches,
        "observed_language": data.get("Language"),
        "verified_fields": ["BusinessPartner", *sorted(mandatory)] if not mismatches else [],
    }


def execute_approved_bp_root_once(
    *, config: SapRuntimeConfig, approval_path: Path, mapping_path: Path,
    attempt_path: Path, transport_factory: Any = UrllibSapTransport,
) -> dict[str, Any]:
    """One explicitly approved BP-root pilot; no other entity may be written.

    The exclusive attempt record prevents an accidental second run after an
    ambiguous POST. It contains no credentials, cookies, or CSRF token.
    """
    from .s4615_implementation import load_contract, validate_write_approval
    from .sap_api_backend import persist_mapping

    op = next(item for item in load_contract()["operations"]
              if item["id"] == "S4615_CUSTOMER_BP_ROOT")
    if config.client != "600" or config.username.upper() != "ABDELJ":
        raise ValueError("BP pilot requires A4H client 600 / ABDELJ")
    approval_document = json.loads(Path(approval_path).read_text(encoding="utf-8"))
    approval = approval_document.get(op["id"])
    if not isinstance(approval, dict):
        raise ValueError("Exact CUSTOMER_MASTER_OWNER approval is missing")
    validate_write_approval(op, approval)
    if approval.get("limit") != "ONE_BP_ROOT_POST_ONLY":
        raise ValueError("Approval does not limit the operation to one BP-root POST")
    if Path(attempt_path).exists():
        raise RuntimeError("BP-root POST has already been attempted; never retry automatically")

    values = op["values"]
    logical_id = values["logical_id"]
    if logical_id != "C615-A01" or op["target"] != {"logical_id": logical_id, "sap_partner_id": None}:
        raise ValueError("BP-root pilot target mismatch")
    if mapping_path.exists():
        mappings = json.loads(mapping_path.read_text(encoding="utf-8")).get("mappings", {})
        if logical_id in mappings:
            raise RuntimeError("C615-A01 already has a logical-to-SAP mapping")

    service = "sap/opu/odata/sap/API_BUSINESS_PARTNER/"
    client = transport_factory(config)
    metadata = client.request("GET", service + "$metadata?sap-client=600",
                              headers={"Accept": "application/xml"})
    if metadata.status != 200:
        raise RuntimeError(f"BP metadata GET failed: HTTP {metadata.status}")
    prepared = prepare_bp_root(values, metadata.body)
    if prepared["status"] != "PAYLOAD_PREPARED":
        raise RuntimeError(f"BP root payload blocked: {prepared['status']}")
    payload = prepared["payload"]

    for label, filter_value in prepared["duplicate_checks"].items():
        query = urlencode({"sap-client": "600", "$filter": filter_value,
                           "$select": "BusinessPartner", "$top": "2"})
        response = client.request("GET", service + "A_BusinessPartner?" + query)
        if response.status != 200:
            raise RuntimeError(f"BP duplicate {label} GET failed: HTTP {response.status}")
        data = response.json().get("d")
        rows = data.get("results") if isinstance(data, dict) else None
        if not isinstance(rows, list):
            raise RuntimeError(f"BP duplicate {label} response shape is unverified")
        if rows:
            raise RuntimeError(f"BP duplicate {label} found; no POST")

    csrf = client.request("GET", service + "?sap-client=600", headers={"X-CSRF-Token": "Fetch"})
    token = csrf.header("X-CSRF-Token")
    if csrf.status != 200 or not token:
        raise RuntimeError(f"BP CSRF/session preflight failed: HTTP {csrf.status}")

    attempt_path.parent.mkdir(parents=True, exist_ok=True)
    with attempt_path.open("x", encoding="utf-8") as handle:
        json.dump({"operation": op["id"], "logical_id": logical_id,
                   "status": "POST_ATTEMPTED", "post_count_limit": 1}, handle)
        handle.write("\n")
    # This is the only write call. Any exception/ambiguous response leaves the
    # attempt marker in place, so a new invocation cannot silently retry.
    response = client.request(
        "POST", service + "A_BusinessPartner?sap-client=600",
        headers={"Content-Type": "application/json", "X-CSRF-Token": token},
        body=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
    )
    sap_id = capture_generated_bp_id(response)
    readback_client = transport_factory(config)
    readback_key = generated_bp_readback_keys(sap_id)["root"]
    query = urlencode({"sap-client": "600", "$select": "BusinessPartner," + ",".join(payload)})
    readback = readback_client.request("GET", service + readback_key + "?" + query)
    assessment = assess_bp_root_identity_readback(readback, sap_id, payload, metadata.body)
    if not assessment["verified"]:
        raise RuntimeError("Generated BP independent readback failed; do not retry POST")

    persist_mapping(mapping_path, logical_id, sap_id, {
        "service": "API_BUSINESS_PARTNER", "entity_set": "A_BusinessPartner",
        "root_readback": "EXISTS", "scope": "BP_ROOT_ONLY",
        "optional_field_mismatches": assessment["optional_mismatches"],
        "observed_language": assessment["observed_language"],
    })
    attempt_path.write_text(json.dumps({"operation": op["id"], "logical_id": logical_id,
                                        "sap_id": sap_id, "status": "VERIFIED",
                                        "post_count": 1}, sort_keys=True) + "\n", encoding="utf-8")
    return {"status": "VERIFIED", "logical_id": logical_id, "sap_id": sap_id,
            "entity_set": "A_BusinessPartner", "post_count": 1}
