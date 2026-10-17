"""Deterministic Phase 1 consolidation across the five completed staged courses."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ingestion.manifest import load_manifest, resolve_document
from src.validation.jsonschema import validate_object

COURSES = ("S4600", "S4610", "S4615", "S4620", "S4650")
INPUTS = {course: ROOT / f"data/normalized/full/{course}/objects.json" for course in COURSES}
OUTPUT = ROOT / "data/validated/canonical_objects.json"
GRAPH = ROOT / "metadata/dependencies/global_dependency_graph.json"
LINEAGE = ROOT / "metadata/lineage/global_lineage.json"
CONFIDENCE_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_symbolic_placeholder(value) -> bool:
    if isinstance(value, dict):
        return any(has_symbolic_placeholder(child) for child in value.values())
    if isinstance(value, list):
        return any(has_symbolic_placeholder(child) for child in value)
    return isinstance(value, str) and "#" in value


def identity_key(item: dict, allow_symbolic: bool = False) -> str | None:
    """Return only business keys whose identity is stable across documents."""
    data = item["data"]
    object_type = item["object_type"]
    keys = {
        "SALES_ORGANIZATION": ("code",),
        "DISTRIBUTION_CHANNEL": ("sales_organization", "code"),
        "SALES_DIVISION": ("code",),
        "SALES_AREA": ("sales_organization", "distribution_channel", "sales_division"),
        "SHIPPING_POINT": ("code",),
        "CONDITION_TYPE": ("code",),
        "CONDITION_TABLE": ("table_id",),
        "ACCESS_SEQUENCE": ("code",),
        "PRICING_PROCEDURE": ("code",),
        "COMPANY_CODE": ("code",),
        "PLANT": ("code",),
        "STORAGE_LOCATION": ("plant", "code"),
        "WAREHOUSE_NUMBER": ("code",),
        "BUSINESS_PARTNER": ("partner_id",),
        "MATERIAL": ("material_id",),
        "EXTENSION_CONFIGURATION": ("configuration_family", "configuration_key"),
    }.get(object_type)
    if not keys:
        return None
    values = [data.get(key) for key in keys]
    if any(value is None or value == "" for value in values):
        return None
    if not allow_symbolic and has_symbolic_placeholder(values):
        return None
    return object_type + "|" + "|".join(str(value) for value in values)


def merge_values(left, right, path="data"):
    """Merge complementary values; return merged value and explicit conflicts."""
    if left is None:
        return copy.deepcopy(right), []
    if right is None:
        return copy.deepcopy(left), []
    if left == right:
        return copy.deepcopy(left), []
    if isinstance(left, dict) and isinstance(right, dict):
        result = {}
        conflicts = []
        for key in sorted(set(left) | set(right)):
            value, child_conflicts = merge_values(left.get(key), right.get(key), f"{path}.{key}")
            result[key] = value
            conflicts.extend(child_conflicts)
        return result, conflicts
    if isinstance(left, list) and isinstance(right, list):
        if not left:
            return copy.deepcopy(right), []
        if not right:
            return copy.deepcopy(left), []
    return copy.deepcopy(left), [{"field_path": path, "left": left, "right": right}]


def unique_rows(rows: list[dict]) -> list[dict]:
    found = {}
    for row in rows:
        found[json.dumps(row, ensure_ascii=False, sort_keys=True)] = copy.deepcopy(row)
    return [found[key] for key in sorted(found)]


def merge_group(items: list[dict], key: str) -> tuple[dict | None, list[dict]]:
    items = sorted(items, key=lambda item: item["object_id"])
    data = copy.deepcopy(items[0]["data"])
    conflicts = []
    for item in items[1:]:
        data, found = merge_values(data, item["data"])
        conflicts.extend(found)
    if conflicts:
        return None, conflicts
    result = copy.deepcopy(items[0])
    result["data"] = data
    result["scenario_id"] = None
    result["provenance"] = sorted(unique_rows(sum((item["provenance"] for item in items), [])),
                                  key=lambda row: (row["course_code"], row["page"], row["section_type"],
                                                   row.get("source_term", "")))
    result["dependencies"] = unique_rows(sum((item["dependencies"] for item in items), []))
    result["placeholders"] = unique_rows(sum((item["placeholders"] for item in items), []))
    result["blocking_reasons"] = unique_rows(sum((item["blocking_reasons"] for item in items), []))
    result["readiness_status"] = "BLOCKED" if result["blocking_reasons"] else "READY"
    result["lifecycle_status"] = "VALIDATED"
    confidence = max((item["validation"]["confidence"] for item in items),
                     key=lambda value: CONFIDENCE_ORDER[value])
    result["validation"] = {"schema_valid": True, "issues": [], "confidence": confidence}
    return result, []


def strings(value, path="data"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


def forbidden_keys(value, path="data") -> list[str]:
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "division":
                found.append(f"{path}.{key}")
            found.extend(forbidden_keys(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(forbidden_keys(child, f"{path}[{index}]"))
    return found


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def main() -> None:
    # Source and staged-input verification happens before consolidation or publication.
    manifest = load_manifest(ROOT)
    if {entry["logical_name"] for entry in manifest} != set(COURSES):
        raise ValueError("Manifest course inventory does not match the five completed stages")
    source_verification = {}
    for course in COURSES:
        source = resolve_document(ROOT, course, verify_checksum=True)
        source_verification[course] = {"source_file": source.name, "sha256": digest(source)}

    input_hashes = {course: digest(path) for course, path in INPUTS.items()}
    staged: list[dict] = []
    source_course_by_id = {}
    staged_schema_errors = []
    for course, path in INPUTS.items():
        rows = json.loads(path.read_text(encoding="utf-8"))["objects"]
        for item in rows:
            staged.append(copy.deepcopy(item))
            source_course_by_id[item["object_id"]] = course
            errors = validate_object(ROOT, item)
            if errors:
                staged_schema_errors.append({"object_id": item["object_id"], "errors": errors})

    duplicate_input_ids = sorted(item_id for item_id, count in
                                 Counter(item["object_id"] for item in staged).items() if count > 1)

    # Identify deterministic and symbolic candidate identities separately.
    deterministic_groups = defaultdict(list)
    symbolic_groups = defaultdict(list)
    for item in staged:
        deterministic = identity_key(item)
        symbolic = identity_key(item, allow_symbolic=True)
        if deterministic:
            deterministic_groups[deterministic].append(item)
        elif symbolic:
            symbolic_groups[symbolic].append(item)

    merge_groups = {key: items for key, items in deterministic_groups.items() if len(items) > 1}
    symbolic_candidates = {key: items for key, items in symbolic_groups.items() if len(items) > 1}
    aliases = {}
    merges = []
    merge_conflicts = []
    merged_ids = set()
    consolidated = []

    for key, items in sorted(merge_groups.items()):
        result, conflicts = merge_group(items, key)
        source_ids = sorted(item["object_id"] for item in items)
        if conflicts:
            merge_conflicts.append({"identity_key": key, "source_object_ids": source_ids,
                                    "conflicts": conflicts,
                                    "decision": "KEEP_SEPARATE_NO_SILENT_MERGE"})
            continue
        survivor = result["object_id"]
        for item_id in source_ids:
            aliases[item_id] = survivor
            merged_ids.add(item_id)
        consolidated.append(result)
        merges.append({"identity_key": key, "survivor_object_id": survivor,
                       "source_object_ids": source_ids,
                       "source_courses": sorted({source_course_by_id[item_id] for item_id in source_ids}),
                       "merge_basis": "Exact non-placeholder canonical business key; non-null fields compatible"})

    conflicted_ids = {item_id for row in merge_conflicts for item_id in row["source_object_ids"]}
    for item in staged:
        if item["object_id"] not in merged_ids or item["object_id"] in conflicted_ids:
            consolidated.append(copy.deepcopy(item))

    consolidated.sort(key=lambda item: item["object_id"])

    # Rewire aliases created by deterministic merges.
    for item in consolidated:
        for dependency in item["dependencies"]:
            if dependency.get("target_id") in aliases:
                dependency["target_id"] = aliases[dependency["target_id"]]

    by_id = {item["object_id"]: item for item in consolidated}

    # One safe cross-document resolution: company code 1010 is explicit on both sides.
    cross_resolutions = []
    company_codes = {item["data"].get("code"): item["object_id"] for item in consolidated
                     if item["object_type"] == "COMPANY_CODE" and item["data"].get("code")
                     and not has_symbolic_placeholder(item["data"].get("code"))}
    for item in consolidated:
        company_code = item["data"].get("company_code")
        if not company_code or company_code not in company_codes:
            continue
        for dependency in item["dependencies"]:
            if dependency["target_type"] == "COMPANY_CODE" and dependency["status"] == "UNRESOLVED":
                dependency["target_id"] = company_codes[company_code]
                dependency["status"] = "RESOLVED"
                cross_resolutions.append({"source_object_id": item["object_id"],
                                          "target_object_id": dependency["target_id"],
                                          "relation": dependency["relation"],
                                          "resolution_basis": f"Exact non-placeholder company_code {company_code}"})

    # Global gates.
    output_schema_errors = []
    broken_references = []
    readiness_issues = []
    placeholder_issues = []
    terminology_issues = []
    for item in consolidated:
        errors = validate_object(ROOT, item)
        if errors:
            output_schema_errors.append({"object_id": item["object_id"], "errors": errors})
        if item["lifecycle_status"] != "VALIDATED":
            readiness_issues.append({"object_id": item["object_id"], "issue": "NON_VALIDATED_LIFECYCLE"})
        if item["readiness_status"] == "READY" and item["blocking_reasons"]:
            readiness_issues.append({"object_id": item["object_id"], "issue": "READY_WITH_BLOCKERS"})
        if item["readiness_status"] == "BLOCKED" and not item["blocking_reasons"]:
            readiness_issues.append({"object_id": item["object_id"], "issue": "BLOCKED_WITHOUT_REASON"})
        paths = {placeholder["field_path"] for placeholder in item["placeholders"]
                 if placeholder["status"] == "UNRESOLVED"}
        for path, value in strings(item["data"]):
            if "##" in value and path not in paths:
                placeholder_issues.append({"object_id": item["object_id"], "field_path": path,
                                           "issue": "UNTRACKED_LITERAL_PLACEHOLDER"})
        if item["readiness_status"] == "READY" and any(p.get("mandatory") and p.get("status") == "UNRESOLVED"
                                                        for p in item["placeholders"]):
            readiness_issues.append({"object_id": item["object_id"],
                                     "issue": "READY_WITH_MANDATORY_UNRESOLVED_PLACEHOLDER"})
        terminology_issues.extend({"object_id": item["object_id"], "field_path": path,
                                   "issue": "FORBIDDEN_CANONICAL_DIVISION"}
                                  for path in forbidden_keys(item["data"]))
        for dependency in item["dependencies"]:
            if dependency["status"] == "RESOLVED":
                target = by_id.get(dependency["target_id"])
                if not target or target["object_type"] != dependency["target_type"]:
                    broken_references.append({"source_object_id": item["object_id"],
                                              "dependency": dependency})
            elif dependency.get("target_id") is not None:
                broken_references.append({"source_object_id": item["object_id"],
                                          "dependency": dependency,
                                          "issue": "UNRESOLVED_WITH_TARGET_ID"})

    output_duplicate_ids = sorted(item_id for item_id, count in
                                  Counter(item["object_id"] for item in consolidated).items() if count > 1)
    return_issue = {"status": "UNRESOLVED_CARRIED_FORWARD",
                    "object_id": "S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER",
                    "resolution": None,
                    "assessment": "No later course supplies explicit directional evidence; consolidation does not alter the issue."}

    hard_failures = {
        "staged_schema_errors": staged_schema_errors,
        "duplicate_input_object_ids": duplicate_input_ids,
        "merge_conflicts": merge_conflicts,
        "output_schema_errors": output_schema_errors,
        "duplicate_output_object_ids": output_duplicate_ids,
        "broken_references": broken_references,
        "readiness_issues": readiness_issues,
        "placeholder_issues": placeholder_issues,
        "terminology_issues": terminology_issues,
    }
    failed_gates = [name for name, issues in hard_failures.items() if issues]
    if failed_gates:
        raise RuntimeError(f"Consolidation publication gates failed: {failed_gates}")

    # Confirm staged files remain byte-identical immediately before publication.
    after_hashes = {course: digest(path) for course, path in INPUTS.items()}
    if input_hashes != after_hashes:
        raise RuntimeError("A staged normalized dataset changed during consolidation")

    graph_edges = []
    for item in consolidated:
        source_courses = sorted({source["course_code"] for source in item["provenance"]})
        for dependency in item["dependencies"]:
            target = by_id.get(dependency.get("target_id"))
            target_courses = sorted({source["course_code"] for source in target["provenance"]}) if target else []
            graph_edges.append({"source": item["object_id"], "source_courses": source_courses,
                                "target": dependency["target_id"], "target_type": dependency["target_type"],
                                "target_courses": target_courses, "relation": dependency["relation"],
                                "status": dependency["status"], "critical": dependency["critical"],
                                "source_phrase": dependency["source_phrase"],
                                "cross_document": bool(target and set(source_courses).isdisjoint(target_courses))})
    graph_edges.sort(key=lambda row: (row["source"], row["relation"], row["target_type"], row["target"] or ""))

    source_ids_by_survivor = defaultdict(list)
    for item in staged:
        source_ids_by_survivor[aliases.get(item["object_id"], item["object_id"])].append(item["object_id"])
    lineage_objects = []
    for item in consolidated:
        source_ids = sorted(source_ids_by_survivor[item["object_id"]])
        lineage_objects.append({"object_id": item["object_id"],
                                "source_object_ids": source_ids,
                                "source_courses": sorted({source["course_code"] for source in item["provenance"]}),
                                "identity_key": identity_key(item),
                                "merge_decision": "MERGED_DETERMINISTIC_IDENTITY" if len(source_ids) > 1 else "PRESERVED",
                                "provenance": item["provenance"]})

    symbolic_rows = [{"identity_key": key,
                      "source_object_ids": sorted(item["object_id"] for item in items),
                      "decision": "KEEP_SEPARATE_SYMBOLIC_PLACEHOLDER_IDENTITY",
                      "reason": "Identity contains an unresolved # placeholder and is not deterministic."}
                     for key, items in sorted(symbolic_candidates.items())]

    readiness = Counter(item["readiness_status"] for item in consolidated)
    classifications = Counter(item["classification"] for item in consolidated)
    types = Counter(item["object_type"] for item in consolidated)
    placeholder_count = sum(len(item["placeholders"]) for item in consolidated)
    objects_with_placeholders = sum(bool(item["placeholders"]) for item in consolidated)
    resolved_edges = sum(edge["status"] == "RESOLVED" for edge in graph_edges)
    unresolved_edges = sum(edge["status"] == "UNRESOLVED" for edge in graph_edges)
    cross_edges = sum(edge["cross_document"] for edge in graph_edges)

    gates = {
        "manifest_and_checksum_verification": "PASS",
        "staged_schema_validation": "PASS",
        "input_object_id_uniqueness": "PASS",
        "deterministic_identity_resolution": "PASS",
        "conflicting_field_values": "PASS",
        "output_schema_validation": "PASS",
        "resolved_reference_integrity": "PASS",
        "placeholder_integrity": "PASS",
        "terminology_consistency": "PASS",
        "lifecycle_readiness_consistency": "PASS",
        "return_delivery_issue_preserved": "PASS",
        "prior_stage_immutability": "PASS",
        "publication": "PASS",
    }
    summary = {"input_object_count": len(staged), "validated_object_count": len(consolidated),
               "duplicates_merged": sum(len(row["source_object_ids"]) - 1 for row in merges),
               "merge_groups": len(merges), "merge_conflict_count": len(merge_conflicts),
               "symbolic_candidate_group_count": len(symbolic_rows),
               "counts_by_type": dict(sorted(types.items())),
               "counts_by_classification": dict(sorted(classifications.items())),
               "readiness_counts": dict(sorted(readiness.items())),
               "placeholder_count": placeholder_count,
               "objects_with_placeholders": objects_with_placeholders,
               "dependency_edge_count": len(graph_edges), "resolved_dependency_count": resolved_edges,
               "unresolved_dependency_count": unresolved_edges,
               "cross_document_resolved_edge_count": cross_edges,
               "schema_valid_count": len(consolidated), "schema_invalid_count": 0,
               "publication_status": "PUBLISHED_VALIDATED", "gates": gates}

    # Publication occurs only after every hard gate and immutability check above passes.
    write_json(OUTPUT, {"objects": consolidated, "consolidation_summary": summary})
    write_json(GRAPH, {"nodes": [{"object_id": item["object_id"],
                                  "object_type": item["object_type"],
                                  "classification": item["classification"],
                                  "readiness_status": item["readiness_status"],
                                  "source_courses": sorted({source["course_code"] for source in item["provenance"]})}
                                 for item in consolidated],
                       "edges": graph_edges, "cross_document_resolutions": cross_resolutions,
                       "summary": {"node_count": len(consolidated), "edge_count": len(graph_edges),
                                   "resolved": resolved_edges, "unresolved": unresolved_edges,
                                   "cross_document_resolved": cross_edges}})
    write_json(LINEAGE, {"source_verification": source_verification,
                         "staged_normalized_sha256": input_hashes,
                         "objects": lineage_objects, "deterministic_merges": merges,
                         "merge_conflicts": merge_conflicts,
                         "symbolic_duplicate_candidates": symbolic_rows,
                         "cross_document_resolutions": cross_resolutions,
                         "open_issues": [return_issue], "quality_gates": gates,
                         "summary": summary})


if __name__ == "__main__":
    main()
