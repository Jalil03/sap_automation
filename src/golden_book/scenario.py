from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.sap_mapping import validate_runtime_contract
from src.sap_mapping.contracts import mapping_contracts
from src.training_context import PlaceholderResolver, TrainingUserContext


ROOT = Path(__file__).resolve().parents[2]
CANONICAL_PATH = ROOT / "data/validated/canonical_objects.json"
SCENARIO_CONFIG_PATH = ROOT / "config/golden_book_s4615_ch4_ex5.json"
PRECHECK_CONFIG_PATH = ROOT / "config/sap_sales_order_prechecks.example.json"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _canonical_objects(path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    objects = _load_json(path)["objects"]
    return objects, {item["object_id"]: item for item in objects}


def _values_at(data: Any, path: str) -> list[Any]:
    values = [data]
    for segment in path.split("."):
        is_array = segment.endswith("[]")
        key = segment[:-2] if is_array else segment
        next_values: list[Any] = []
        for value in values:
            if not isinstance(value, dict) or key not in value:
                continue
            child = value[key]
            if is_array and isinstance(child, list):
                next_values.extend(child)
            elif not is_array:
                next_values.append(child)
        values = next_values
    return [value for value in values if value not in (None, "", [], {})]


def _display_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _precheck_value(name: str, data: dict[str, Any]) -> list[str]:
    paths = {
        "CUSTOMER": "sold_to_party",
        "MATERIAL": "items[].material",
        "SALES_ORGANIZATION": "sales_organization",
        "DISTRIBUTION_CHANNEL": "distribution_channel",
        "ORGANIZATION_DIVISION": "sales_division",
        "SALES_ORDER_TYPE": "order_type",
        "UNIT_OF_MEASURE": "items[].unit",
    }
    return list(dict.fromkeys(_display_value(value) for value in _values_at(data, paths[name])))


def _render_filter(template: str | None, name: str, values: list[str]) -> str | None:
    if template is None:
        return None
    if not values:
        return template
    rendered = [template.replace("{" + name + "}", value.replace("'", "''")) for value in values]
    return " ; ".join(rendered)


def _workflow_label(obj: dict[str, Any]) -> str:
    data = obj["data"]
    if obj["object_type"] == "SALES_ORDER":
        return f"Commande {data.get('order_type') or 'non précisé'}"
    if obj["object_type"] == "OUTBOUND_DELIVERY":
        return "Livraison sortante"
    if obj["object_type"] == "BILLING":
        return f"Facture {data.get('billing_type') or 'non précisé'}"
    return obj["object_type"]


def _workflow_branch(object_id: str) -> str:
    return "PRO_FORMA" if "PRO_FORMA" in object_id else "CASH_SALE"


@dataclass(frozen=True)
class GoldenBookScenario:
    canonical_path: Path = CANONICAL_PATH
    scenario_config_path: Path = SCENARIO_CONFIG_PATH
    precheck_config_path: Path = PRECHECK_CONFIG_PATH

    def build(
        self,
        training_user_code: str,
        *,
        read_only_precheck_evidence: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        context = TrainingUserContext(training_user_code)
        config = _load_json(self.scenario_config_path)
        _, canonical_index = _canonical_objects(self.canonical_path)
        primary_id = config["primary_object_id"]
        source_object = canonical_index.get(primary_id)
        if source_object is None:
            raise KeyError(f"Golden Book canonical object not found: {primary_id}")
        if source_object.get("scenario_id") != config["scenario_id"]:
            raise ValueError("Golden Book primary object does not belong to configured scenario")

        resolved = PlaceholderResolver().resolve(source_object, context.training_user_code)
        runtime_object = resolved.canonical_object
        runtime_index = dict(canonical_index)
        runtime_index[primary_id] = runtime_object
        mapped = validate_runtime_contract(runtime_object, object_index=runtime_index)
        mapping = self._mapping_view(runtime_object, mapped)
        prechecks = self._prechecks(
            runtime_object,
            read_only_precheck_evidence=read_only_precheck_evidence or {},
        )
        final = self._final_result(mapped, prechecks)
        workflow = self._workflow(config, canonical_index)
        provenance = source_object["provenance"]

        value = {
            "source": {
                "book": provenance[0]["source_file"],
                "course_code": provenance[0]["course_code"],
                "chapter": provenance[0]["chapter"],
                "chapter_title": config["chapter_title"],
                "exercise": provenance[0]["exercise"],
                "exercise_title": config["exercise_title"],
                "scenario_id": source_object["scenario_id"],
                "canonical_object_id": primary_id,
                "exercise_page": next(
                    item["page"] for item in provenance if item["section_type"] == "EXERCISE"
                ),
                "solution_page": next(
                    item["page"] for item in provenance if item["section_type"] == "SOLUTION"
                ),
            },
            "original_book_data": {
                "training_user": config["training_user_template"],
                "sales_order_type": source_object["data"]["order_type"],
                "sales_organization": source_object["data"]["sales_organization"],
                "distribution_channel": source_object["data"]["distribution_channel"],
                "organization_division": source_object["data"]["sales_division"],
                "sold_to_party": source_object["data"]["sold_to_party"],
                "customer_reference": source_object["data"]["customer_reference"],
                "material": source_object["data"]["items"][0]["material"],
                "quantity": source_object["data"]["items"][0]["quantity"],
                "unit": source_object["data"]["items"][0]["unit"],
            },
            "training_context": {
                **resolved.trace_metadata(),
                "training_user": config["training_user_template"].replace(
                    "##", context.training_user_code
                ),
            },
            "runtime_data": {
                "training_user": config["training_user_template"].replace(
                    "##", context.training_user_code
                ),
                "sales_order_type": runtime_object["data"]["order_type"],
                "sales_organization": runtime_object["data"]["sales_organization"],
                "distribution_channel": runtime_object["data"]["distribution_channel"],
                "organization_division": runtime_object["data"]["sales_division"],
                "sold_to_party": runtime_object["data"]["sold_to_party"],
                "customer_reference": runtime_object["data"]["customer_reference"],
                "material": runtime_object["data"]["items"][0]["material"],
                "quantity": runtime_object["data"]["items"][0]["quantity"],
                "unit": runtime_object["data"]["items"][0]["unit"],
            },
            "workflow": workflow,
            "sap_mapping": mapping,
            "prechecks": prechecks,
            "final_result": final,
            "policy": {
                "canonical_immutable": True,
                "sap_calls_performed": 0,
                "post_allowed": False,
                "live_validation_method": "GET_READ_ONLY_ONLY",
            },
        }
        json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False)
        return value

    @staticmethod
    def _workflow(
        config: dict[str, Any], canonical_index: dict[str, dict[str, Any]]
    ) -> dict[str, Any]:
        object_ids = config["workflow_object_ids"]
        missing = [object_id for object_id in object_ids if object_id not in canonical_index]
        if missing:
            raise KeyError("Golden Book workflow objects missing: " + ", ".join(missing))
        nodes = []
        edges = []
        selected = set(object_ids)
        for object_id in object_ids:
            obj = canonical_index[object_id]
            nodes.append({
                "object_id": object_id,
                "object_type": obj["object_type"],
                "label": _workflow_label(obj),
                "branch": _workflow_branch(object_id),
                "canonical_readiness": obj["readiness_status"],
            })
            for dependency in obj.get("dependencies", []):
                target = dependency.get("target_id")
                if target in selected:
                    edges.append({
                        "from": target,
                        "to": object_id,
                        "relation": dependency["relation"],
                        "source_phrase": dependency["source_phrase"],
                        "status": dependency["status"],
                    })
        return {
            "nodes": nodes,
            "edges": sorted(edges, key=lambda item: (item["from"], item["to"], item["relation"])),
            "cash_sale_summary": "Commande BV → livraison créée avec la commande → facture BV.",
            "pro_forma_summary": "Commande standard → facture pro forma F5 avant livraison; transfert FI non applicable.",
        }

    @staticmethod
    def _mapping_view(runtime_object: dict[str, Any], mapped: dict[str, Any]) -> dict[str, Any]:
        contract = mapping_contracts()["objects"]["SALES_ORDER"]
        rows = []
        for canonical_path, field in contract["fields"].items():
            if field["disposition"] != "MAPPED":
                continue
            values = _values_at(runtime_object["data"], canonical_path)
            if not values:
                continue
            rows.append({
                "canonical_field": canonical_path,
                "canonical_value": ", ".join(_display_value(value) for value in values),
                "sap_fields": field["sap_paths"],
                "disposition": field["disposition"],
            })
        return {
            "service": contract["interface"],
            "technical_registration": contract["technical_registration"],
            "entity_set": contract["root_entity_set"],
            "protocol": contract["protocol"],
            "local_runtime_status": mapped["runtime_status"],
            "local_contract_valid": mapped["contract_validation"]["local_contract_valid"],
            "rows": rows,
            "offline_payload_preview": deepcopy(mapped["payloads"][0]["body"]),
            "write_executed": False,
        }

    def _prechecks(
        self,
        runtime_object: dict[str, Any],
        *,
        read_only_precheck_evidence: dict[str, str],
    ) -> list[dict[str, Any]]:
        probes = _load_json(self.precheck_config_path)["probes"]
        allowed_evidence = {"FOUND", "NOT_FOUND", "INTERFACE_UNAVAILABLE"}
        unknown = set(read_only_precheck_evidence.values()) - allowed_evidence
        if unknown:
            raise ValueError("Unsupported read-only precheck evidence: " + ", ".join(sorted(unknown)))
        results = []
        for probe in probes:
            name = probe["name"]
            values = _precheck_value(name, runtime_object["data"])
            evidence = read_only_precheck_evidence.get(name)
            contract_confirmed = (
                probe["status"] == "CONFIRMED"
                and probe["entity_set"]["status"] == "CONFIRMED"
                and probe["path_template"] is not None
            )
            if evidence == "FOUND" and contract_confirmed:
                status = "PASS"
                reason = "Read-only GET evidence found the exact resolved value."
            elif evidence == "FOUND":
                status = "NEEDS_LIVE_VALIDATION"
                reason = "A positive observation cannot activate an unconfirmed lookup contract."
            elif evidence == "NOT_FOUND":
                status = "BLOCKED"
                reason = "Read-only GET evidence did not find the resolved value in SAP."
            elif evidence == "INTERFACE_UNAVAILABLE":
                status = "BLOCKED"
                reason = "The configured read-only SAP interface is unavailable."
            else:
                status = "NEEDS_LIVE_VALIDATION"
                reason = "No confirmed read-only GET evidence is available offline."
            results.append({
                "name": name,
                "canonical_paths": probe["canonical_paths"],
                "resolved_values": values,
                "service": probe["service"]["external_name"],
                "technical_service": probe["service"]["technical_name"],
                "entity_set": probe["entity_set"]["name"],
                "entity_set_status": probe["entity_set"]["status"],
                "contract_status": probe["status"],
                "proposed_filter": _render_filter(probe["key_or_filter"], name, values),
                "status": status,
                "reason": reason,
                "method": "GET",
            })
        return results

    @staticmethod
    def _final_result(mapped: dict[str, Any], prechecks: list[dict[str, Any]]) -> dict[str, Any]:
        reasons = []
        if mapped["runtime_status"] != "EXECUTION_READY":
            reasons.append({
                "code": "LOCAL_MAPPING_NOT_EXECUTION_READY",
                "detail": f"Local runtime status is {mapped['runtime_status']}.",
            })
        for check in prechecks:
            if check["status"] != "PASS":
                reasons.append({
                    "code": f"PRECHECK_{check['name']}_{check['status']}",
                    "detail": check["reason"],
                })
        return {
            "status": "READY" if not reasons else "BLOCKED",
            "local_mapping_status": mapped["runtime_status"],
            "blocking_reasons": reasons,
        }


def build_golden_book_scenario(
    training_user_code: str,
    *,
    read_only_precheck_evidence: dict[str, str] | None = None,
) -> dict[str, Any]:
    return GoldenBookScenario().build(
        training_user_code,
        read_only_precheck_evidence=read_only_precheck_evidence,
    )
