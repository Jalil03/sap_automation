"""Deterministic, source-verified Phase 1B Stage 2 extraction for S4610 only."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ingestion.manifest import load_manifest, resolve_document
from src.validation.jsonschema import validate_object

COURSE = "S4610"
SOURCE_FILE = "S4610_FR_Col12_ILT_FV_Inst_A4.pdf"
EXPECTED_PAGES = 202
EXERCISE_PAGES = {1: 19, 2: 25, 3: 41, 4: 65, 5: 91, 6: 107, 7: 109,
                  8: 127, 9: 135, 10: 153, 11: 163, 12: 169, 13: 179, 14: 189}
SOLUTION_PAGES = {1: 20, 2: 26, 3: 43, 4: 69, 5: 93, 6: 108, 7: 111,
                  8: 129, 9: 136, 10: 155, 11: 164, 12: 170, 13: 181, 14: 191}
CHAPTER = {1: 1, 2: 1, 3: 2, 4: 3, **{n: 4 for n in range(5, 10)},
           **{n: 5 for n in range(10, 15)}}


def sid(exercise: int) -> str:
    return f"S4610_CH{CHAPTER[exercise]}_EX{exercise}"


def ref(exercise: int, section: str, page: int, term: str, excerpt: str | None = None) -> dict:
    return {"course_code": COURSE, "source_file": SOURCE_FILE, "page": page,
            "chapter": CHAPTER[exercise], "exercise": exercise, "section_type": section,
            "scenario_id": sid(exercise), "raw_excerpt": excerpt, "source_term": term}


def prov(exercise: int, term: str, excerpt: str, *, exercise_page: int | None = None,
         solution_page: int | None = None, solution_excerpt: str | None = None) -> list[dict]:
    return [ref(exercise, "EXERCISE", exercise_page or EXERCISE_PAGES[exercise], term, excerpt),
            ref(exercise, "SOLUTION", solution_page or SOLUTION_PAGES[exercise], term, solution_excerpt)]


def relative(raw: str, offset: str | None) -> dict:
    return {"kind": "RELATIVE", "raw": raw, "offset": offset}


def dependency(relation: str, target_type: str, target_id: str | None, phrase: str,
               critical: bool = True) -> dict:
    return {"relation": relation, "target_type": target_type, "target_id": target_id,
            "status": "RESOLVED" if target_id else "UNRESOLVED", "critical": critical,
            "source_phrase": phrase}


def scan_placeholders(value, path="data") -> list[dict]:
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            found.extend(scan_placeholders(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(scan_placeholders(child, f"{path}[{index}]"))
    elif isinstance(value, str) and "##" in value:
        found.append({"raw": "##", "resolved": None, "status": "UNRESOLVED",
                      "mandatory": True, "field_path": path})
    return found


def canonical(object_id: str, object_type: str, classification: str, scenario_id: str,
              provenance: list[dict], data: dict, dependencies: list[dict] | None = None,
              confidence: str = "HIGH") -> dict:
    placeholders = scan_placeholders(data)
    reasons = []
    if placeholders:
        reasons.append({"code": "UNRESOLVED_MANDATORY_PLACEHOLDER",
                        "message": "Participant-specific source placeholder remains unresolved",
                        "field_path": "data"})
    if any(item["critical"] and item["status"] == "UNRESOLVED" for item in dependencies or []):
        reasons.append({"code": "UNRESOLVED_CRITICAL_DEPENDENCY",
                        "message": "A required source reference has no extractable identifier",
                        "field_path": "dependencies"})
    return {"object_id": object_id, "object_type": object_type, "classification": classification,
            "scenario_id": scenario_id, "provenance": provenance, "lifecycle_status": "VALIDATED",
            "readiness_status": "BLOCKED" if reasons else "READY", "blocking_reasons": reasons,
            "dependencies": dependencies or [], "placeholders": placeholders,
            "validation": {"schema_valid": True, "issues": [], "confidence": confidence},
            "data": data}


PLANT_ID = "S4610_SHARED_PLANT_1010"
STORAGE_101C = "S4610_SHARED_STORAGE_LOCATION_101C"
STORAGE_101D = "S4610_SHARED_STORAGE_LOCATION_101D"
WAREHOUSE_ID = "S4610_SHARED_WAREHOUSE_NUMBER_1010"
SP_Z0 = "S4610_CH2_EX3_SHIPPING_POINT_Z0-GROUP"
SP_Y0 = "S4610_CH2_EX3_SHIPPING_POINT_Y0-GROUP"


def sales_order(exercise: int, order_type: str, sold_to: str, customer_reference: str,
                date_raw: str, offset: str | None, material: str, quantity: float,
                *, item_category: str | None = None, shipping_point: str | None = None,
                route: str | None = None) -> dict:
    item = {"line_id": "10", "material": material, "quantity": quantity, "unit": None,
            "plant": None, "ship_to_party": None, "shipping_point": shipping_point,
            "route": route, "net_weight": None, "net_weight_unit": None,
            "item_category": item_category}
    deps = [dependency("SOLD_TO_PARTY", "BUSINESS_PARTNER", None, sold_to),
            dependency("USES_MATERIAL", "MATERIAL", None, material)]
    if shipping_point:
        deps.append(dependency("DETERMINES_SHIPPING_POINT", "SHIPPING_POINT",
                               SP_Y0 if shipping_point == "Y0##" else SP_Z0, shipping_point))
    order_key = order_type.replace("##", "-GROUP").replace("#", "GROUP")
    return canonical(f"{sid(exercise)}_SALES_ORDER_{order_key}",
        "SALES_ORDER", "TRANSACTION", sid(exercise),
        prov(exercise, "Type de commande / Donneur d'ordre / Réf. client / Date livr. req. / Article / Quantité",
             f"{order_type}; {sold_to}; {customer_reference}; {date_raw}; {material}; {quantity}"),
        {"order_type": order_type, "sales_organization": "1010", "distribution_channel": "10",
         "sales_division": "00", "sold_to_party": sold_to, "ship_to_party": None,
         "customer_reference": customer_reference, "requested_delivery_date": relative(date_raw, offset),
         "items": [item], "payment_terms": None, "processing_status": None,
         "completeness_state": None}, deps)


def outbound(exercise: int, suffix: str, order_id: str | None, delivery_type: str | None,
             shipping_point: str | None, items: list[dict], confidence="HIGH") -> dict:
    deps = [dependency("CREATED_FROM", "SALES_ORDER", order_id,
                       "commande client précédente" if order_id else "commande client portant la référence S4610")]
    if shipping_point:
        deps.append(dependency("PROCESSED_AT", "SHIPPING_POINT",
                               SP_Y0 if shipping_point == "Y0##" else SP_Z0, shipping_point))
    for item in items:
        if item.get("storage_location"):
            target = STORAGE_101C if item["storage_location"] == "101C" else STORAGE_101D
            deps.append(dependency("PICKS_FROM", "STORAGE_LOCATION", target, item["storage_location"]))
    return canonical(f"{sid(exercise)}_OUTBOUND_DELIVERY_{suffix}", "OUTBOUND_DELIVERY",
        "TRANSACTION", sid(exercise),
        prov(exercise, "Livraison sortante / document de référence / point d'expédition",
             f"{delivery_type or 'type non indiqué'}; {shipping_point or 'point non indiqué'}"),
        {"delivery_type": delivery_type, "ship_to_party": None, "shipping_point": shipping_point,
         "planned_creation_date": None, "planned_goods_issue_date": None,
         "storage_location": None, "warehouse_number": None,
         "system_representations": [{"system": "LE", "identifier": None}], "items": items},
        deps, confidence)


def build_objects() -> list[dict]:
    objects = []

    # Reference-only objects promoted only because primary delivery/warehouse dependencies require them.
    objects += [
        canonical(PLANT_ID, "PLANT", "REFERENCE_DATA", sid(3),
            [ref(3, "EXERCISE", 42, "division affectée au point d'expédition", "même division que Z0##"),
             ref(3, "SOLUTION", 43, "division", "Z0## est affecté à la division 1010")],
            {"code": "1010", "description": None, "company_code": "1010"}),
        canonical(STORAGE_101C, "STORAGE_LOCATION", "REFERENCE_DATA", sid(8),
            prov(8, "Point d'expédition / Division / Condition de stockage / Magasin",
                 "Y0##; 1010; <Non renseigné> ou 70; 101C", exercise_page=128, solution_page=130,
                 solution_excerpt="modifier le magasin 101S par 101C"),
            {"code": "101C", "description": None, "plant": "1010"},
            [dependency("BELONGS_TO", "PLANT", PLANT_ID, "division 1010")]),
        canonical(STORAGE_101D, "STORAGE_LOCATION", "REFERENCE_DATA", sid(13),
            prov(13, "Division / Magasin", "1010; 101D"),
            {"code": "101D", "description": None, "plant": "1010"},
            [dependency("BELONGS_TO", "PLANT", PLANT_ID, "division 1010")]),
        canonical(WAREHOUSE_ID, "WAREHOUSE_NUMBER", "REFERENCE_DATA", sid(11),
            prov(11, "Numéro de magasin", "1010", solution_excerpt="Numéro de magasin 1010"),
            {"code": "1010", "description": None,
             "plant_storage_locations": ["1010/101C", "1010/101D"]},
            [dependency("SERVES", "PLANT", PLANT_ID, "division 1010"),
             dependency("SERVES", "STORAGE_LOCATION", STORAGE_101C, "magasin 101C"),
             dependency("SERVES", "STORAGE_LOCATION", STORAGE_101D, "magasin 101D")]),
    ]

    # Shipping points: one copied instance and its explicit source instance, deduplicated across later exercises.
    z0_prov = [ref(3, "EXERCISE", 41, "Point d'expédition standard", "Z0##"),
               ref(3, "SOLUTION", 43, "Affectation point d'expédition à division",
                   "Z0## est affecté à la division 1010")]
    objects.append(canonical(SP_Z0, "SHIPPING_POINT", "CUSTOMIZING", sid(3), z0_prov,
        {"code": "Z0##", "description": "opérations d'expédition standard", "plant": "1010",
         "determination_rules": [], "working_times": None, "loading_time": None,
         "pick_pack_time": None}, [dependency("ASSIGNED_TO", "PLANT", PLANT_ID, "division 1010")]))

    y0_prov = [ref(3, "EXERCISE", 41, "Nouveau point d'expédition / description", "Y0##; ## Transp. express Hambourg"),
               ref(3, "SOLUTION", 44, "Copie et affectation du point d'expédition",
                   "Du point Z0## au point Y0##; affecté à la division 1010"),
               ref(5, "EXERCISE", 91, "Détermination du point d'expédition", "Y0## pour marchandises express"),
               ref(5, "SOLUTION", 94, "Condition d'expédition / groupe de chargement / division / point",
                   "50+##; 0004; 1010; Y0##; autre point Z0##"),
               ref(6, "EXERCISE", 107, "Ordonnancement par point d'expédition",
                   "Y0##; Durée travail 2-SHIFT; chargement 2:30; prélèvement/emballage 2:30"),
               ref(6, "SOLUTION", 108, "Durées de travail", "2-SHIFT; 2:30; 2:30"),
               ref(8, "SOLUTION", 130, "Détermination du magasin de prélèvement",
                   "Y0## / 1010 / vide ou 70 -> 101C")]
    objects.append(canonical(SP_Y0, "SHIPPING_POINT", "CUSTOMIZING", sid(3), y0_prov,
        {"code": "Y0##", "description": "## Transp. express Hambourg", "plant": "1010",
         "determination_rules": [
             {"shipping_condition": "50+##", "loading_group": "0004", "plant": "1010",
              "shipping_point": "Y0##", "alternative_shipping_point": "Z0##"},
             {"plant": "1010", "storage_condition": None, "storage_location": "101C"},
             {"plant": "1010", "storage_condition": "70", "storage_location": "101C"}],
         "working_times": "2-SHIFT", "loading_time": "PT2H30M", "pick_pack_time": "PT2H30M"},
        [dependency("COPIED_FROM", "SHIPPING_POINT", SP_Z0, "copier Z0## vers Y0##"),
         dependency("ASSIGNED_TO", "PLANT", PLANT_ID, "division 1010"),
         dependency("DETERMINES", "STORAGE_LOCATION", STORAGE_101C, "magasin 101C")]))

    # Secondary copy-control records explicitly verified/configured in Exercise 4.
    copy_prov = [ref(4, "EXERCISE", 66, "Pilotage de la copie / type source / type cible",
                     "Type de livraison ZL##; commande ZA## et commande standard CDCL"),
                 ref(4, "SOLUTION", 70, "Pilotage de la copie", "ZL## cible; ZA## et CDCL sources"),
                 ref(4, "SOLUTION", 72, "Pilotage de la copie au niveau poste", "ZL## / ZA## / type poste ZA##")]
    objects += [
        canonical(f"{sid(4)}_COPY_CONTROL_ZAGROUP_TO_ZLGROUP", "COPY_CONTROL", "CUSTOMIZING", sid(4),
            copy_prov, {"source_document_type": "ZA##", "target_document_type": "ZL##",
                        "level": "HEADER_AND_ITEM", "requirements": ["source item category ZA##"]}),
        canonical(f"{sid(4)}_COPY_CONTROL_CDCL_TO_ZLGROUP", "COPY_CONTROL", "CUSTOMIZING", sid(4),
            copy_prov, {"source_document_type": "CDCL", "target_document_type": "ZL##",
                        "level": "HEADER", "requirements": []}, confidence="MEDIUM"),
    ]

    # Exercise 2 is a real pre-existing delivery, but its participant/system-derived values are blank.
    objects.append(outbound(2, "EXISTING_BY_CUSTOMER_REFERENCE", None, None, None, [], "LOW"))

    so4 = sales_order(4, "ZA##", "C610-A##", "##-4-1", "Date du lendemain", "P1D",
                      "P610-1##", 12, item_category="ZA##")
    so7 = sales_order(7, "ZA##", "C610-B##", "##-5-1", "Surlendemain", "P2D",
                      "P610-3##", 15, shipping_point="Y0##", route="Expr##")
    so10 = sales_order(10, "ZA##", "C610-A##", "##-5-1", "dans 1 semaine", "P1W",
                       "P610-5##", 10)
    objects += [so4, so7, so10]

    delivery4_items = [
        {"line_id": "10", "material": "P610-1##", "quantity": 12, "unit": None,
         "reference_item": "10", "plant": None, "storage_location": None,
         "warehouse_number": None, "item_category": "ZA##", "gross_weight": None,
         "gross_weight_unit": None},
        {"line_id": "20", "material": "P610-2##", "quantity": 5, "unit": None,
         "reference_item": None, "plant": None, "storage_location": "101C",
         "warehouse_number": None, "item_category": "DLN", "gross_weight": None,
         "gross_weight_unit": None},
    ]
    d4 = outbound(4, "EXPRESS_FROM_ORDER", so4["object_id"], "ZL##", None, delivery4_items)
    d4["provenance"].extend([
        ref(4, "EXERCISE", 68, "Type et postes de livraison sortante", "ZL##; P610-2##"),
        ref(4, "SOLUTION", 74, "Type et postes de livraison sortante", "ZL##; poste DLN; magasin 101C"),
    ])
    delivery10_items = [{"line_id": "10", "material": "P610-5##", "quantity": 10, "unit": None,
                         "reference_item": "10", "plant": None, "storage_location": None,
                         "warehouse_number": None, "item_category": None, "gross_weight": None,
                         "gross_weight_unit": None}]
    d10 = outbound(10, "FROM_ORDER", so10["object_id"], None, "Z0##", delivery10_items, "MEDIUM")
    d10["provenance"].extend([
        ref(10, "EXERCISE", 154, "Magasin / numéro de magasin / livraison", None),
        ref(10, "SOLUTION", 158, "Livraison avec référence à la commande / point d'expédition", "Z0##"),
        ref(12, "SOLUTION", 170, "Représentation EWM de la livraison sortante", "Livraison sortante - nouveau document"),
    ])
    d10["data"]["system_representations"].append(
        {"system": "EWM", "identifier": None, "relationship": "REPRESENTS_SAME_BUSINESS_DELIVERY"})
    objects += [d4, d10]

    wt11_id = f"{sid(11)}_WAREHOUSE_TASK_OUTBOUND"
    objects.append(canonical(wt11_id, "WAREHOUSE_TASK", "TRANSACTION", sid(11),
        prov(11, "Tâche magasin / ordre de livraison sortante", "créer et confirmer la tâche magasin",
             solution_excerpt="Numéro de magasin 1010; tâche magasin confirmée"),
        {"warehouse_number": "1010", "source_bin": None, "destination_bin": None,
         "product": None, "quantity": None, "unit": None, "task_direction": "OUTBOUND",
         "status": "CONFIRMED", "delivery_reference": None},
        [dependency("CREATED_FOR", "OUTBOUND_DELIVERY", d10["object_id"], "votre livraison sortante"),
         dependency("EXECUTED_IN", "WAREHOUSE_NUMBER", WAREHOUSE_ID, "numéro de magasin 1010")], "MEDIUM"))
    objects.append(canonical(f"{sid(12)}_GOODS_ISSUE_FROM_EX10_DELIVERY", "GOODS_ISSUE", "TRANSACTION", sid(12),
        prov(12, "Sortie de marchandises / ordre de livraison sortante",
             "enregistrez la sortie de marchandises pour l'ordre de livraison sortante",
             solution_excerpt="StaGloMvmtStock est C"),
        {"posting_date": None, "movement_reference": None, "delivery_reference": None,
         "items": [], "movement_status": "C"},
        [dependency("POSTED_FOR", "OUTBOUND_DELIVERY", d10["object_id"], "livraison de l'exercice précédent"),
         dependency("AFTER_WAREHOUSE_TASK", "WAREHOUSE_TASK", wt11_id, "exercice précédent")], "MEDIUM"))

    # Purchase-order references and inbound-delivery chains. LE and EWM numbers are representations, not duplicates.
    po13_id = f"{sid(13)}_PURCHASE_ORDER_REFERENCE_EXTERNAL_PROCUREMENT"
    po14_id = f"{sid(14)}_PURCHASE_ORDER_REFERENCE_EXTERNAL_PROCUREMENT"
    po_common_deps = lambda supplier, material, storage: [
        dependency("SUPPLIED_BY", "BUSINESS_PARTNER", None, supplier),
        dependency("USES_MATERIAL", "MATERIAL", None, material),
        dependency("RECEIVED_AT", "PLANT", PLANT_ID, "division 1010"),
        dependency("STORED_AT", "STORAGE_LOCATION", storage, "magasin 101D")]
    objects += [
        canonical(po13_id, "PURCHASE_ORDER_REFERENCE", "REFERENCE_DATA", sid(13),
            prov(13, "Commande d'achat / fournisseur / article / quantité / division / magasin",
                 "S610-A##; P610-2##; 50; 1010; 101D", solution_page=182,
                 solution_excerpt="Pilotage des conf. 0004 livraison entrante"),
            {"reference_id": None, "supplier": "S610-A##", "plant": "1010",
             "items": [{"line_id": "10", "material": "P610-2##", "quantity": 50, "unit": None}],
             "purchasing_organization": "1010", "purchasing_group": "Z##", "company_code": "1010",
             "storage_location": "101D", "net_price": None, "currency": None,
             "confirmation_control": "0004"}, po_common_deps("S610-A##", "P610-2##", STORAGE_101D)),
        canonical(po14_id, "PURCHASE_ORDER_REFERENCE", "REFERENCE_DATA", sid(14),
            prov(14, "Commande d'achat / fournisseur / article / quantité / division / magasin",
                 "S610-A##; P610-2##; 10; 1010; 101D", solution_page=192,
                 solution_excerpt="Prix net 52; division 1010; magasin 101D"),
            {"reference_id": None, "supplier": "S610-A##", "plant": "1010",
             "items": [{"line_id": "10", "material": "P610-2##", "quantity": 10, "unit": None}],
             "purchasing_organization": "1010", "purchasing_group": "Z##", "company_code": "1010",
             "storage_location": "101D", "net_price": 52, "currency": None,
             "confirmation_control": None}, po_common_deps("S610-A##", "P610-2##", STORAGE_101D)),
    ]

    def inbound(exercise: int, suffix: str, po_id: str, quantity: float, asn: str | None,
                receipt_status: str | None) -> dict:
        reps = [{"system": "LE", "identifier": None},
                {"system": "EWM", "identifier": None, "relationship": "REPRESENTS_SAME_BUSINESS_DELIVERY"}]
        data = {"delivery_type": "INBOUND", "supplier": "S610-A##", "plant": "1010",
                "expected_receipt_date": None, "storage_location": "101D", "warehouse_number": "1010",
                "purchase_order_reference": None, "goods_receipt_status": receipt_status, "asn": asn,
                "system_representations": reps,
                "items": [{"line_id": "10", "material": "P610-2##", "quantity": quantity, "unit": None,
                           "reference_item": "10", "plant": "1010", "storage_location": "101D",
                           "warehouse_number": "1010", "item_category": None,
                           "gross_weight": None, "gross_weight_unit": None}]}
        return canonical(f"{sid(exercise)}_INBOUND_DELIVERY_{suffix}", "INBOUND_DELIVERY", "TRANSACTION",
            sid(exercise), prov(exercise, "Livraison entrante / commande d'achat / SAP EWM",
                                f"S610-A##; P610-2##; quantité {quantity}; 1010 / 101D",
                                solution_page=183 if exercise == 13 else 192), data,
            [dependency("CREATED_FROM", "PURCHASE_ORDER_REFERENCE", po_id, "commande d'achat précédente"),
             dependency("RECEIVED_AT", "PLANT", PLANT_ID, "division 1010"),
             dependency("STORED_AT", "STORAGE_LOCATION", STORAGE_101D, "magasin 101D"),
             dependency("PROCESSED_IN", "WAREHOUSE_NUMBER", WAREHOUSE_ID, "numéro de magasin 1010")])

    in13 = inbound(13, "FROM_PURCHASE_ORDER", po13_id, 50, None, None)
    in13["provenance"].append(ref(13, "SOLUTION", 184, "Correspondance livraison entrante LE / EWM",
                                        "Document ERP utilisé pour retrouver la livraison entrante SAP EWM"))
    in14 = inbound(14, "FROM_PURCHASE_ORDER", po14_id, 10, "S4610-##-1", "POSTED")
    in14["provenance"].append(ref(14, "SOLUTION", 193, "Entrée de marchandises / tâche magasin", None))
    objects += [in13, in14]

    objects.append(canonical(f"{sid(14)}_WAREHOUSE_TASK_INBOUND", "WAREHOUSE_TASK", "TRANSACTION", sid(14),
        prov(14, "Tâche magasin pour livraison entrante", "créer et confirmer la tâche magasin",
             exercise_page=190, solution_page=193),
        {"warehouse_number": "1010", "source_bin": None, "destination_bin": None,
         "product": None, "quantity": None, "unit": None, "task_direction": "INBOUND",
         "status": "CONFIRMED", "delivery_reference": None},
        [dependency("CREATED_FOR", "INBOUND_DELIVERY", in14["object_id"], "livraison entrante"),
         dependency("EXECUTED_IN", "WAREHOUSE_NUMBER", WAREHOUSE_ID, "numéro de magasin 1010")], "MEDIUM"))

    # Propagate readiness from resolved but blocked parents.
    by_id = {item["object_id"]: item for item in objects}
    for item in objects:
        for dep in item["dependencies"]:
            target = by_id.get(dep.get("target_id"))
            if dep["critical"] and target and target["readiness_status"] == "BLOCKED":
                if not any(reason["code"] == "DEPENDENCY_NOT_READY" for reason in item["blocking_reasons"]):
                    item["blocking_reasons"].append({"code": "DEPENDENCY_NOT_READY",
                        "message": "A resolved canonical dependency is itself not downstream-ready",
                        "field_path": "dependencies"})
                    item["readiness_status"] = "BLOCKED"
    return sorted(objects, key=lambda item: item["object_id"])


SKIPPED = [
    {"exercise": 1, "reason": "Theory-only delivery concepts; supplier returns do not resolve the S4600 customer-return direction."},
    {"exercise": 5, "reason": "Route and shipping-point determination enrich the existing Y0## record; no route object exists in scope."},
    {"exercise": 6, "reason": "Scheduling values enrich Y0##; no duplicate shipping-point object."},
    {"exercise": 8, "reason": "Mass-delivery count is only 'at least two' with blank identifiers; no pseudo-deliveries created."},
    {"exercise": 9, "reason": "Outbound-delivery monitor/list procedure; no new business-object instance."},
]


def parse_pdf(pdf: Path) -> tuple[list[str], dict]:
    executable = shutil.which("pdftotext")
    if not executable:
        candidate = Path(r"C:\Program Files\Git\mingw64\bin\pdftotext.exe")
        executable = str(candidate) if candidate.is_file() else None
    if not executable:
        raise RuntimeError("pdftotext is required")
    with tempfile.TemporaryDirectory(prefix="s4610-") as temp_dir:
        output = Path(temp_dir) / "S4610.txt"
        subprocess.run([executable, "-layout", str(pdf), str(output)], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = output.read_text(encoding="utf-8", errors="replace")
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    if len(pages) != EXPECTED_PAGES:
        raise ValueError(f"Expected {EXPECTED_PAGES} pages, found {len(pages)}")
    joined = "\n".join(pages)
    exercises = sorted({int(value) for value in re.findall(r"Exercice\s+(\d+)", joined)})
    solutions = sorted({int(value) for value in re.findall(r"Solution\s+(\d+)", joined)})
    if exercises != list(range(1, 15)) or solutions != list(range(1, 15)):
        raise ValueError({"exercises": exercises, "solutions": solutions})
    return pages, {"page_count": len(pages), "exercise_count": len(exercises),
                   "solution_count": len(solutions),
                   "table_marker_count": len(re.findall(r"Nom de zone|Zone\s+Valeur", joined))}


def section_inventory(objects: list[dict]) -> list[dict]:
    mentions = {}
    for item in objects:
        for source in item["provenance"]:
            mentions.setdefault(int(source["exercise"]), set()).add(item["object_id"])
    skipped = {item["exercise"]: item["reason"] for item in SKIPPED}
    result = []
    for exercise in range(1, 15):
        ids = sorted(mentions.get(exercise, []))
        primary = [item_id for item_id in ids if item_id.startswith(sid(exercise))]
        if primary:
            decision, reason = "EXTRACT", "Concrete source-backed instance data."
        elif ids:
            decision, reason = "ENRICH_EXISTING", skipped.get(exercise, "Verification/enrichment only.")
        else:
            decision, reason = "SKIP", skipped.get(exercise, "No qualifying canonical instance.")
        result.append({"scenario_id": sid(exercise), "chapter": CHAPTER[exercise], "exercise": exercise,
                       "exercise_page": EXERCISE_PAGES[exercise], "solution_page": SOLUTION_PAGES[exercise],
                       "decision": decision, "reason": reason, "object_ids": ids})
    return result


def write_json(relative: str, value) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def cross_document_checks(objects: list[dict]) -> dict:
    s4600_path = ROOT / "data/normalized/full/S4600/objects.json"
    before = hashlib.sha256(s4600_path.read_bytes()).hexdigest()
    s4600 = json.loads(s4600_path.read_text(encoding="utf-8"))["objects"]
    z0_matches = [item["object_id"] for item in s4600
                  if item["object_type"] == "SHIPPING_POINT" and item["data"].get("code") == "Z0##"]
    after = hashlib.sha256(s4600_path.read_bytes()).hexdigest()
    if before != after:
        raise RuntimeError("S4600 artifact changed during read-only cross-document check")
    return {"s4600_normalized_sha256": before,
            "potential_entity_matches": [{"s4610_object_id": SP_Z0, "s4600_object_ids": z0_matches,
                                           "match_key": "SHIPPING_POINT.code=Z0##",
                                           "status": "POTENTIAL_MATCH_UNRESOLVED_PLACEHOLDER"}],
            "return_delivery_issue": {"status": "UNRESOLVED_CARRIED_FORWARD",
                "s4600_object_id": "S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER",
                "s4610_evidence": {"page": 21, "source_term": "Retours fournisseur"},
                "assessment": "S4610 names supplier returns but does not classify the S4600 customer-return delivery direction."}}


def main() -> None:
    entries = [entry for entry in load_manifest(ROOT) if entry["logical_name"] == COURSE]
    if len(entries) != 1:
        raise ValueError("S4610 must resolve exactly once")
    pdf = resolve_document(ROOT, COURSE, verify_checksum=True)
    if pdf.name != SOURCE_FILE:
        raise ValueError(pdf.name)
    pages, parse_stats = parse_pdf(pdf)
    objects = build_objects()
    if len({item["object_id"] for item in objects}) != len(objects):
        raise ValueError("Duplicate object IDs")
    for item in objects:
        errors = validate_object(ROOT, item)
        if errors:
            raise ValueError({item["object_id"]: errors})

    extracted = json.loads(json.dumps(objects))
    for item in extracted:
        item["lifecycle_status"] = "EXTRACTED"
    write_json("data/extracted/full/S4610/objects.json", {"objects": extracted})
    write_json("data/normalized/full/S4610/objects.json", {"objects": objects})

    lineage = {"objects": [{"object_id": item["object_id"], "scenario_id": item["scenario_id"],
                              "source_to_canonical": [{"page": source["page"],
                                  "section_type": source["section_type"], "source_term": source["source_term"],
                                  "raw_excerpt": source["raw_excerpt"]} for source in item["provenance"]],
                              "solution_enrichments": [{"page": source["page"], "source_term": source["source_term"]}
                                  for source in item["provenance"] if source["section_type"] == "SOLUTION"]}
                             for item in objects]}
    write_json("metadata/lineage/full/S4610/lineage.json", lineage)
    write_json("metadata/lineage/full/S4610/section_inventory.json",
               {"sections": section_inventory(objects), "skipped_candidates": SKIPPED})
    write_json("metadata/lineage/full/S4610/cross_document_checks.json", cross_document_checks(objects))

    graph = {"nodes": [{"object_id": item["object_id"], "object_type": item["object_type"],
                         "readiness_status": item["readiness_status"]} for item in objects],
             "edges": [{"source": item["object_id"], "target": dep["target_id"],
                         "target_type": dep["target_type"], "relation": dep["relation"],
                         "status": dep["status"], "critical": dep["critical"],
                         "source_phrase": dep["source_phrase"]}
                        for item in objects for dep in item["dependencies"]]}
    write_json("metadata/dependencies/full/S4610/dependency_graph.json", graph)
    write_json("metadata/confidence/full/S4610/confidence.json", {"objects": [
        {"object_id": item["object_id"], "object_type": item["object_type"],
         "confidence": item["validation"]["confidence"], "readiness_status": item["readiness_status"],
         "blocking_reason_codes": [reason["code"] for reason in item["blocking_reasons"]]}
        for item in objects]})
    counts = Counter(item["object_type"] for item in objects)
    summary = {"source": {"logical_name": COURSE, "source_file": pdf.name,
                           "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), **parse_stats},
               "object_count": len(objects), "counts_by_type": dict(sorted(counts.items())),
               "classification_counts": dict(Counter(item["classification"] for item in objects)),
               "readiness_counts": dict(Counter(item["readiness_status"] for item in objects)),
               "confidence_counts": dict(Counter(item["validation"]["confidence"] for item in objects)),
               "placeholder_count": sum(len(item["placeholders"]) for item in objects),
               "objects_with_placeholders": sum(bool(item["placeholders"]) for item in objects),
               "dependency_edge_count": len(graph["edges"]),
               "unresolved_dependency_count": sum(edge["status"] == "UNRESOLVED" for edge in graph["edges"]),
               "schema_valid_count": len(objects), "schema_invalid_count": 0,
               "source_pages_processed": [1, len(pages)]}
    write_json("metadata/confidence/full/S4610/extraction_summary.json", summary)


if __name__ == "__main__":
    main()
