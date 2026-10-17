"""Offline Phase 5A source analysis and optional READ-only detail capture.

Default execution only rebuilds the two deterministic repository artifacts.
The explicit ``--live-read-only`` mode sends STATUS and INSPECT requests only;
the operator must manually position SAP GUI on a candidate's display screen.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COMPANY_SNAPSHOT = ROOT / "runtime/sap_discovery/phase4c/snapshots/008_company_code.json"
SALES_ORG_SNAPSHOT = ROOT / "runtime/sap_discovery/phase4c/snapshots/020_sales_organization.json"
PHASE5_PREPARE = ROOT / "data/provisioning/phase5_prepare_1010.json"
OUTPUT_JSON = ROOT / "data/provisioning/phase5_source_analysis_1010.json"
OUTPUT_REPORT = ROOT / "reports/phase5_source_analysis_1010.md"
LIVE_CAPTURE_DIR = ROOT / "runtime/sap_discovery/phase5_source_discovery"


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _table_rows(snapshot: dict[str, Any], table_id: str) -> list[dict[str, Any]]:
    tables = [table for table in snapshot.get("tables") or [] if table.get("id") == table_id]
    if len(tables) != 1:
        raise ValueError(f"Expected one observed table {table_id}, found {len(tables)}")
    rows = []
    for row in tables[0].get("visible_rows") or []:
        values = {value["column"]: value["text"] for value in row.get("values") or []}
        if values.get("0"):
            rows.append({"id": values["0"], "description": values.get("1")})
    return rows


def _company_candidates(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_T001"
    candidates = []
    for row in _table_rows(snapshot, table_id):
        description = row["description"] or ""
        explicit_template = description.startswith("Country Template ")
        if explicit_template:
            tier = 1
            confidence = "MEDIUM"
            rationale = "Observed description explicitly identifies a country template."
        elif row["description"]:
            tier = 2
            confidence = "LOW"
            rationale = "Existing described Company Code, but no evidence that it is a reusable template."
        else:
            tier = 3
            confidence = "LOW"
            rationale = "Existing Company Code with no comparable description in the captured summary."
        candidates.append({
            "rank_tier": tier,
            "candidate_id": row["id"],
            "observed_attributes": {"company_code": row["id"], "description": row["description"]},
            "evidence": {
                "source": str(COMPANY_SNAPSHOT.relative_to(ROOT)).replace("\\", "/"),
                "table_id": table_id,
                "fields": ["company_code", "description"],
            },
            "confidence": confidence,
            "ranking_basis": rationale,
            "suitability": "NOT_DETERMINED",
            "automatically_selected": False,
            "notes": (
                "1710 is observed but explicitly not a default template."
                if row["id"] == "1710"
                else None
            ),
        })
    return sorted(candidates, key=lambda item: (item["rank_tier"], item["candidate_id"]))


def _sales_org_candidates(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_TVKO"
    candidates = []
    for row in _table_rows(snapshot, table_id):
        described = bool(row["description"])
        candidates.append({
            "rank_tier": 1 if described else 2,
            "candidate_id": row["id"],
            "observed_attributes": {
                "sales_organization": row["id"],
                "description": row["description"],
            },
            "evidence": {
                "source": str(SALES_ORG_SNAPSHOT.relative_to(ROOT)).replace("\\", "/"),
                "table_id": table_id,
                "fields": ["sales_organization", "description"],
            },
            "confidence": "LOW",
            "ranking_basis": (
                "Description is observable, but no template designation or target-fit attributes are available."
                if described
                else "Only the identifier is observable; no template designation or comparable attributes are available."
            ),
            "suitability": "NOT_DETERMINED",
            "automatically_selected": False,
            "notes": (
                "1710 is observed but explicitly not a default template."
                if row["id"] == "1710"
                else None
            ),
        })
    return sorted(candidates, key=lambda item: (item["rank_tier"], item["candidate_id"]))


def build_analysis() -> dict[str, Any]:
    company_snapshot = _load(COMPANY_SNAPSHOT)
    sales_snapshot = _load(SALES_ORG_SNAPSHOT)
    prepare = _load(PHASE5_PREPARE)
    states = {step["step_id"]: step["current_state"] for step in prepare["ordered_steps"]}
    return {
        "analysis_id": "PHASE5A_SOURCE_ANALYSIS_1010",
        "mode": "READ_ONLY_SOURCE_ANALYSIS",
        "sap_connection_performed": False,
        "automatic_selection": None,
        "ranking_scope": "evidence completeness only; not functional suitability",
        "source_artifacts": [
            {"path": str(path.relative_to(ROOT)).replace("\\", "/"), "sha256": _sha256(path)}
            for path in (COMPANY_SNAPSHOT, SALES_ORG_SNAPSHOT, PHASE5_PREPARE)
        ],
        "objects": {
            "COMPANY_CODE_1010": {
                "current_state": states["COMPANY_CODE_1010"],
                "candidates": _company_candidates(company_snapshot),
                "known_target_values": {"company_code": "1010"},
                "missing_required_values": [
                    {
                        "field": "approved_source_candidate_or_manual_creation_decision",
                        "status": "BLOCKED_NEEDS_SOURCE",
                    },
                    {"field": "company_name", "status": "BLOCKED_NEEDS_VALUE"},
                    {"field": "city", "status": "BLOCKED_NEEDS_VALUE"},
                    {"field": "country", "status": "BLOCKED_NEEDS_VALUE"},
                    {"field": "currency", "status": "BLOCKED_NEEDS_VALUE"},
                    {"field": "language", "status": "BLOCKED_NEEDS_VALUE"},
                ],
                "fields_requiring_live_contract_confirmation": [
                    "all additional fields exposed by the V_T001 detail screen",
                    "which fields are mandatory in TEST 600",
                ],
                "status": "BLOCKED_NEEDS_SOURCE",
            },
            "SALES_ORGANIZATION_1010": {
                "current_state": states["SALES_ORGANIZATION_1010"],
                "candidates": _sales_org_candidates(sales_snapshot),
                "known_target_values": {"sales_organization": "1010"},
                "missing_required_values": [
                    {
                        "field": "approved_source_candidate_or_manual_creation_decision",
                        "status": "BLOCKED_NEEDS_SOURCE",
                    },
                    {"field": "description", "status": "BLOCKED_NEEDS_VALUE"},
                    {"field": "statistics_currency", "status": "BLOCKED_NEEDS_VALUE"},
                ],
                "fields_requiring_live_contract_confirmation": [
                    "all additional fields exposed by the V_TVKO detail screen",
                    "which fields are mandatory in TEST 600",
                ],
                "status": "BLOCKED_NEEDS_SOURCE",
            },
        },
        "live_read_only_required": True,
        "live_reason": (
            "Summary snapshots expose only identifiers and some descriptions; detail attributes, "
            "mandatory-field behavior, country/currency fit, and assignment context are not observable."
        ),
        "live_constraints": {
            "allowed_actions": ["STATUS", "INSPECT"],
            "operator_navigation_required": True,
            "forbidden_actions": [
                "SAVE", "CREATE", "COPY", "DELETE", "NEW_ENTRIES", "TRANSPORT",
                "SET_TEXT", "POST", "PATCH", "PUT", "RFC", "BAPI_WRITE",
            ],
        },
    }


def render_report(analysis: dict[str, Any]) -> str:
    lines = [
        "# Phase 5A — Analyse des sources de provisioning 1010",
        "",
        "Aucun candidat n'est sélectionné automatiquement. Le classement porte uniquement sur la complétude des preuves observées.",
        "",
    ]
    for object_id, item in analysis["objects"].items():
        lines.extend([
            f"## {object_id}",
            "",
            f"État : **{item['current_state']}** — statut : **{item['status']}**",
            "",
            "| Tier | Candidat | Attributs observés | Confidence | Suitability |",
            "|---:|---|---|---|---|",
        ])
        for candidate in item["candidates"]:
            attributes = json.dumps(candidate["observed_attributes"], ensure_ascii=False, sort_keys=True)
            lines.append(
                f"| {candidate['rank_tier']} | {candidate['candidate_id']} | `{attributes}` | "
                f"{candidate['confidence']} | {candidate['suitability']} |"
            )
        lines.extend([
            "",
            "Valeurs/champs manquants :",
            "",
            *[
                f"- `{field['field']}` — {field['status']}"
                for field in item["missing_required_values"]
            ],
            "",
            "Champs à confirmer sur le contrat live :",
            "",
            *[f"- {field}" for field in item["fields_requiring_live_contract_confirmation"]],
            "",
        ])
    lines.extend([
        "## Conclusion",
        "",
        f"Live READ-only nécessaire : **{'YES' if analysis['live_read_only_required'] else 'NO'}**.",
        "",
        "Le script live n'autorise que `STATUS` et `INSPECT`; la navigation jusqu'aux écrans de détail reste manuelle.",
        "",
        "1710 n'est ni recommandé ni sélectionné par défaut.",
        "",
    ])
    return "\n".join(lines)


def write_outputs(analysis: dict[str, Any]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    OUTPUT_REPORT.write_text(render_report(analysis), encoding="utf-8")


def _sanitized_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    allowed = {
        "transaction", "program", "screen_number", "window_title", "status_bar",
        "input_fields", "labels", "buttons", "tables", "visible_control_types",
    }
    return {key: snapshot.get(key) for key in sorted(allowed)}


def run_live_read_only_capture() -> int:
    from src.sap_gui_bridge.discovery import EXPECTED_SAP, FilesystemRunnerClient

    client = FilesystemRunnerClient()
    _, status_response = client.exchange("STATUS", {})
    if status_response.get("status") != "SUCCESS":
        raise RuntimeError("READ-only STATUS failed; no fallback mechanism attempted")
    sap = status_response.get("result") or status_response.get("sap") or {}
    for key, expected in EXPECTED_SAP.items():
        if str(sap.get(key) or "") != expected:
            raise RuntimeError(f"Unexpected SAP {key}; capture stopped fail-closed")

    LIVE_CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
    print("Open a candidate DETAIL/DISPLAY screen manually. Do not enter or change data.")
    print("Type COMPANY_CODE:<id> or SALES_ORGANIZATION:<id>; blank line ends capture.")
    while True:
        label = input("candidate> ").strip()
        if not label:
            break
        if ":" not in label:
            print("BLOCKED: expected OBJECT_TYPE:candidate_id")
            continue
        object_type, candidate_id = (part.strip() for part in label.split(":", 1))
        if object_type not in {"COMPANY_CODE", "SALES_ORGANIZATION"} or not candidate_id:
            print("BLOCKED: unsupported object type or empty candidate")
            continue
        _, response = client.exchange("INSPECT", {})
        if response.get("status") != "SUCCESS" or not isinstance(response.get("result"), dict):
            raise RuntimeError("READ-only INSPECT failed; capture stopped")
        snapshot = _sanitized_snapshot(response["result"])
        expected_transaction = "V_T001" if object_type == "COMPANY_CODE" else "V_TVKO"
        if str(snapshot.get("transaction") or "").upper() != expected_transaction:
            print(f"BLOCKED: expected transaction {expected_transaction}; snapshot not stored")
            continue
        visible = json.dumps(snapshot, ensure_ascii=False)
        if candidate_id not in visible:
            print("BLOCKED: candidate id is not observable on current screen; snapshot not stored")
            continue
        path = LIVE_CAPTURE_DIR / f"{object_type.lower()}_{candidate_id}.json"
        if path.exists():
            print(f"BLOCKED: capture already exists: {path}")
            continue
        path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"Captured READ-only evidence: {path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-read-only", action="store_true")
    args = parser.parse_args()
    if args.live_read_only:
        return run_live_read_only_capture()
    analysis = build_analysis()
    write_outputs(analysis)
    print(f"{analysis['analysis_id']}: candidates analyzed; automatic selection = NONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
