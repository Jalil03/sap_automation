"""Build the deterministic, offline Phase 5 PREPARE plan for the 1010 foundation.

This script reads repository evidence and writes planning artifacts only.  It
contains no SAP GUI, HTTP, RFC, BAPI, save, create, copy, delete, or transport
operation.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE4_REQUIREMENTS = ROOT / "data/requirements/training_environment_requirements.json"
PHASE4B_PLAN = ROOT / "data/requirements/golden_book_s4615_ch4_ex5_provisioning.json"
PHASE4C_SUMMARY = ROOT / "runtime/sap_discovery/phase4c/discovery_summary.json"
PHASE4C_COMPANY_SNAPSHOT = ROOT / "runtime/sap_discovery/phase4c/snapshots/008_company_code.json"
OUTPUT_JSON = ROOT / "data/provisioning/phase5_prepare_1010.json"
OUTPUT_REPORT = ROOT / "reports/phase5_prepare_1010.md"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _requirement(inventory: dict[str, Any], object_type: str, template: str) -> dict[str, Any]:
    matches = [
        item
        for item in inventory["requirements"]
        if item.get("type") == object_type and item.get("value_template") == template
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one {object_type} requirement for {template}, found {len(matches)}")
    return matches[0]


def _company_code_state(snapshot: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    search = snapshot.get("table_value_search") or {}
    position_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtVIM_POSITION_INFO"
    totals = []
    for field in snapshot.get("input_fields") or []:
        if field.get("id") != position_id:
            continue
        match = re.search(r"/\s*(\d+)\s*$", str(field.get("text") or ""))
        if match:
            totals.append(int(match.group(1)))
    sap_total = totals[0] if len(totals) == 1 else None
    unique_rows = search.get("unique_rows_read", search.get("rows_read"))
    unique_rows = int(unique_rows) if isinstance(unique_rows, (int, str)) and str(unique_rows).isdigit() else None
    target_found = search.get("result") == "FOUND" or search.get("found_row") is not None
    if target_found:
        state = "EXISTS"
    elif sap_total is not None and unique_rows is not None and unique_rows >= sap_total:
        state = "MISSING"
    else:
        state = "UNKNOWN"
    return state, {
        "source": str(PHASE4C_COMPANY_SNAPSHOT.relative_to(ROOT)).replace("\\", "/"),
        "transaction": search.get("transaction"),
        "program": search.get("program"),
        "table_id": search.get("table_id"),
        "target_field": search.get("column"),
        "target_value": search.get("value"),
        "sap_total_entries": sap_total,
        "unique_rows_read": unique_rows,
        "found_row": search.get("found_row"),
        "visited_scroll_positions": search.get("visited_scroll_positions") or [],
        "conclusion": state,
    }


def build_plan(root: Path = ROOT) -> dict[str, Any]:
    if root != ROOT:
        raise ValueError("Phase 5 source paths are repository-root scoped")
    inventory = _load(PHASE4_REQUIREMENTS)
    phase4b = _load(PHASE4B_PLAN)
    phase4c = _load(PHASE4C_SUMMARY)
    company_snapshot = _load(PHASE4C_COMPANY_SNAPSHOT)

    company_req = _requirement(inventory, "COMPANY_CODE", "1010")
    sales_org_req = _requirement(inventory, "SALES_ORGANIZATION", "1010")
    channel_req = _requirement(inventory, "DISTRIBUTION_CHANNEL", "10")
    division_req = _requirement(inventory, "SALES_DIVISION", "00")
    sales_area_req = _requirement(inventory, "SALES_AREA", "1010/10/00")
    sales_area_assessment = next(
        item
        for item in phase4b["structural_dependency_assessment"]
        if item.get("component") == "SALES_AREA_1010_10_00"
    )

    company_state, company_evidence = _company_code_state(company_snapshot)
    sales_org_state = sales_org_req["current_known_sap_status"]
    if sales_org_state not in {"EXISTS", "MISSING", "UNKNOWN"}:
        sales_org_state = "UNKNOWN"

    steps = [
        {
            "order": 1,
            "step_id": "COMPANY_CODE_1010",
            "target": {"type": "COMPANY_CODE", "company_code": "1010"},
            "current_state": company_state,
            "evidence": [
                company_evidence,
                {
                    "source": str(PHASE4_REQUIREMENTS.relative_to(ROOT)).replace("\\", "/"),
                    "requirement_id": company_req["requirement_id"],
                    "source_books": company_req["source_book"],
                },
            ],
            "required_action": "PREPARE_CREATE_COMPANY_CODE",
            "source_candidates": [],
            "missing_values": [
                "approved_company_code_source_or_complete_manual_definition",
                "required_company_code_customizing_values",
            ],
            "depends_on": [],
            "status": "BLOCKED_NEEDS_SOURCE" if company_state == "MISSING" else (
                "NO_ACTION_REQUIRED" if company_state == "EXISTS" else "BLOCKED_NEEDS_VALUE"
            ),
        },
        {
            "order": 2,
            "step_id": "SALES_ORGANIZATION_1010",
            "target": {"type": "SALES_ORGANIZATION", "sales_organization": "1010"},
            "current_state": sales_org_state,
            "evidence": [
                {
                    "source": str(PHASE4_REQUIREMENTS.relative_to(ROOT)).replace("\\", "/"),
                    "requirement_id": sales_org_req["requirement_id"],
                    "known_status": sales_org_req["current_known_sap_status"],
                    "source_books": sales_org_req["source_book"],
                },
                {
                    "source": str(PHASE4C_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
                    "discovery_status": phase4c["targets"]["sales_organization"]["status"],
                    "meaning": "maintenance screen discovered; existence is sourced from Phase 4 live evidence",
                },
            ],
            "required_action": "PREPARE_CREATE_SALES_ORGANIZATION",
            "source_candidates": [],
            "missing_values": [
                "approved_sales_organization_source_or_complete_manual_definition",
                "required_sales_organization_customizing_values",
            ],
            "depends_on": ["COMPANY_CODE_1010"],
            "status": "BLOCKED_NEEDS_SOURCE" if sales_org_state == "MISSING" else (
                "NO_ACTION_REQUIRED" if sales_org_state == "EXISTS" else "BLOCKED_NEEDS_VALUE"
            ),
        },
        {
            "order": 3,
            "step_id": "SALES_ORG_1010_TO_COMPANY_CODE_1010",
            "target": {
                "type": "SALES_ORG_COMPANY_CODE_ASSIGNMENT",
                "sales_organization": "1010",
                "company_code": "1010",
            },
            "current_state": "UNKNOWN",
            "evidence": [{
                "source": str(PHASE4C_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
                "discovery_status": phase4c["targets"]["sales_org_company_assignment"]["status"],
                "meaning": "exact IMG activity reached; assignment row/value was not verified",
            }],
            "required_action": "READ_VALIDATE_THEN_PREPARE_ASSIGNMENT_IF_MISSING",
            "source_candidates": [{
                "kind": "SOURCE_BACKED_TARGET_VALUES",
                "sales_organization": "1010",
                "company_code": "1010",
                "requirement_ids": [sales_org_req["requirement_id"], company_req["requirement_id"]],
            }],
            "missing_values": [],
            "depends_on": ["COMPANY_CODE_1010", "SALES_ORGANIZATION_1010"],
            "status": "BLOCKED_DEPENDENCY",
        },
        {
            "order": 4,
            "step_id": "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
            "target": {
                "type": "DISTRIBUTION_CHANNEL_SALES_ORG_ASSIGNMENT",
                "distribution_channel": "10",
                "sales_organization": "1010",
            },
            "current_state": "UNKNOWN",
            "evidence": [
                {
                    "source": str(PHASE4_REQUIREMENTS.relative_to(ROOT)).replace("\\", "/"),
                    "requirement_id": channel_req["requirement_id"],
                    "distribution_channel_status": channel_req["current_known_sap_status"],
                },
                {
                    "source": str(PHASE4C_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
                    "discovery_status": phase4c["targets"]["distribution_channel_assignment"]["status"],
                    "meaning": "exact IMG activity reached; assignment row/value was not verified",
                },
            ],
            "required_action": "READ_VALIDATE_THEN_PREPARE_ASSIGNMENT_IF_MISSING",
            "source_candidates": [{
                "kind": "SOURCE_BACKED_TARGET_VALUES",
                "distribution_channel": "10",
                "sales_organization": "1010",
                "requirement_ids": [channel_req["requirement_id"], sales_org_req["requirement_id"]],
            }],
            "missing_values": [],
            "depends_on": ["SALES_ORGANIZATION_1010"],
            "status": "BLOCKED_DEPENDENCY",
        },
        {
            "order": 5,
            "step_id": "DIVISION_00_TO_SALES_ORG_1010",
            "target": {
                "type": "DIVISION_SALES_ORG_ASSIGNMENT",
                "sales_division": "00",
                "sales_organization": "1010",
            },
            "current_state": "UNKNOWN",
            "evidence": [
                {
                    "source": str(PHASE4_REQUIREMENTS.relative_to(ROOT)).replace("\\", "/"),
                    "requirement_id": division_req["requirement_id"],
                    "sales_division_status": division_req["current_known_sap_status"],
                },
                {
                    "source": str(PHASE4C_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
                    "discovery_status": phase4c["targets"]["division_assignment"]["status"],
                    "meaning": "exact IMG activity reached; assignment row/value was not verified",
                },
                {
                    "source": str(PHASE4B_PLAN.relative_to(ROOT)).replace("\\", "/"),
                    "sales_area_requirement_id": sales_area_req["requirement_id"],
                    "sales_area": "1010/10/00",
                    "phase4b_boundary": sales_area_assessment["reason"],
                },
            ],
            "required_action": "READ_VALIDATE_THEN_PREPARE_ASSIGNMENT_IF_MISSING",
            "source_candidates": [{
                "kind": "SOURCE_BACKED_TARGET_VALUES",
                "sales_division": "00",
                "sales_organization": "1010",
                "sales_area": "1010/10/00",
                "requirement_ids": [division_req["requirement_id"], sales_org_req["requirement_id"], sales_area_req["requirement_id"]],
            }],
            "missing_values": [],
            "depends_on": ["SALES_ORGANIZATION_1010", "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010"],
            "status": "BLOCKED_DEPENDENCY",
        },
    ]

    return {
        "plan_id": "PHASE5_PREPARE_1010",
        "mode": "PREPARE",
        "execution_performed": False,
        "sap_connection_performed": False,
        "safety": {
            "allowed": ["READ_LOCAL_ARTIFACTS", "PREPARE_PLAN"],
            "forbidden": ["SAP_CONNECTION", "SAVE", "CREATE", "COPY", "DELETE", "TRANSPORT"],
            "automatic_template_selection": False,
            "prohibited_automatic_template": "1710",
        },
        "source_artifacts": [
            {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": _sha256(path)}
            for path in (PHASE4_REQUIREMENTS, PHASE4B_PLAN, PHASE4C_SUMMARY, PHASE4C_COMPANY_SNAPSHOT)
        ],
        "ordered_steps": steps,
        "blockers": [
            {
                "step_id": step["step_id"],
                "status": step["status"],
                "missing_values": step["missing_values"],
                "depends_on": step["depends_on"],
            }
            for step in steps
            if step["status"].startswith("BLOCKED")
        ],
        "overall_status": "BLOCKED",
    }


def render_report(plan: dict[str, Any]) -> str:
    lines = [
        "# Phase 5 — PREPARE du socle 1010",
        "",
        "Mode strict : **PREPARE local uniquement**. Aucune connexion ou écriture SAP n'a été effectuée.",
        "",
        "## Plan ordonné",
        "",
        "| Ordre | Target | État | Action préparée | Statut |",
        "|---:|---|---|---|---|",
    ]
    for step in plan["ordered_steps"]:
        lines.append(
            f"| {step['order']} | {step['step_id']} | {step['current_state']} | "
            f"{step['required_action']} | {step['status']} |"
        )
    lines.extend(["", "## Détail", ""])
    for step in plan["ordered_steps"]:
        lines.extend([
            f"### {step['order']}. {step['step_id']}",
            "",
            f"- Target : `{json.dumps(step['target'], ensure_ascii=False, sort_keys=True)}`",
            f"- Current state : **{step['current_state']}**",
            f"- Required action : `{step['required_action']}`",
            f"- Status : **{step['status']}**",
            f"- Depends on : {', '.join(step['depends_on']) or 'None'}",
            f"- Source candidates : `{json.dumps(step['source_candidates'], ensure_ascii=False, sort_keys=True)}`",
            f"- Missing values : {', '.join(step['missing_values']) or 'None'}",
            f"- Evidence : `{json.dumps(step['evidence'], ensure_ascii=False, sort_keys=True)}`",
            "",
        ])
    lines.extend([
        "## Blockers",
        "",
        *[
            f"- {item['step_id']}: {item['status']}"
            + (f" — {', '.join(item['missing_values'])}" if item["missing_values"] else "")
            + (f" — dependencies: {', '.join(item['depends_on'])}" if item["depends_on"] else "")
            for item in plan["blockers"]
        ],
        "",
        "Aucun template 1710 n'est proposé ou sélectionné automatiquement.",
        "",
    ])
    return "\n".join(lines)


def write_outputs(plan: dict[str, Any]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    OUTPUT_REPORT.write_text(render_report(plan), encoding="utf-8")


def main() -> int:
    plan = build_plan()
    write_outputs(plan)
    print(f"{plan['plan_id']}: {plan['overall_status']} ({len(plan['ordered_steps'])} steps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
