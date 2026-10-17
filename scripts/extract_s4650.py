"""Deterministic, source-verified Phase 1B Stage 5 extraction for S4650 only."""
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

COURSE = "S4650"
SOURCE_FILE = "S4650_FR_Col12_ILT_FV_Inst_A4.pdf"
EXPECTED_SHA256 = "e5601257121ad731d45297c784e25f1306cf6d8a51f215005df2b73db50efa4c"
EXPECTED_PAGES = 267
EXERCISE_PAGES = {1: 17, 2: 27, 3: 53, 4: 69, 5: 75, 6: 89, 7: 109,
                  8: 117, 9: 137, 10: 159, 11: 177, 12: 213, 13: 235}
SOLUTION_PAGES = {1: 18, 2: 29, 3: 58, 4: 71, 5: 76, 6: 90, 7: 111,
                  8: 118, 9: 139, 10: 161, 11: 179, 12: 215, 13: 237}
CHAPTER = {1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 3, 7: 3, 8: 3,
           9: 4, 10: 4, 11: 4, 12: 5, 13: 5}


def sid(exercise: int) -> str:
    return f"S4650_CH{CHAPTER[exercise]}_EX{exercise}"


def ref(exercise: int, section: str, page: int, term: str, excerpt: str) -> dict:
    return {"course_code": COURSE, "source_file": SOURCE_FILE, "page": page,
            "chapter": CHAPTER[exercise], "exercise": exercise,
            "section_type": section, "scenario_id": sid(exercise),
            "raw_excerpt": excerpt, "source_term": term}


def prov(exercise: int, term: str, excerpt: str, solution_excerpt: str | None = None,
         exercise_page: int | None = None, solution_page: int | None = None) -> list[dict]:
    return [ref(exercise, "EXERCISE", exercise_page or EXERCISE_PAGES[exercise], term, excerpt),
            ref(exercise, "SOLUTION", solution_page or SOLUTION_PAGES[exercise], term,
                solution_excerpt or excerpt)]


def relative(raw: str, offset: str | None = None) -> dict:
    return {"kind": "RELATIVE", "raw": raw, "offset": offset}


def dep(relation: str, target_type: str, target_id: str | None, phrase: str,
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


def canonical(object_id: str, object_type: str, classification: str, exercise: int,
              provenance: list[dict], data: dict, dependencies: list[dict] | None = None,
              confidence: str = "HIGH", extra_reasons: list[dict] | None = None) -> dict:
    dependencies = dependencies or []
    placeholders = scan_placeholders(data)
    reasons = list(extra_reasons or [])
    if placeholders:
        reasons.append({"code": "UNRESOLVED_MANDATORY_PLACEHOLDER",
                        "message": "Participant-specific source placeholder remains unresolved",
                        "field_path": "data"})
    if any(d["critical"] and d["status"] == "UNRESOLVED" for d in dependencies):
        reasons.append({"code": "UNRESOLVED_CRITICAL_DEPENDENCY",
                        "message": "A required source reference has no canonical identifier",
                        "field_path": "dependencies"})
    return {"object_id": object_id, "object_type": object_type,
            "classification": classification, "scenario_id": sid(exercise),
            "provenance": provenance, "lifecycle_status": "VALIDATED",
            "readiness_status": "BLOCKED" if reasons else "READY",
            "blocking_reasons": reasons, "dependencies": dependencies,
            "placeholders": placeholders,
            "validation": {"schema_valid": True, "issues": [], "confidence": confidence},
            "data": data}


def order(exercise: int, suffix: str, order_type: str, customer: str,
          customer_reference: str, material: str, quantity: float | None,
          requested_date: dict | None = None, dependencies: list[dict] | None = None,
          processing_status: str = "SAVED", confidence: str = "HIGH") -> dict:
    evidence = prov(exercise,
        "Type de commande / donneur d'ordre / référence client / article / quantité",
        f"{order_type}; 1010/10/00; {customer}; {customer_reference}; {material}; {quantity}")
    base_deps = [dep("SOLD_TO_PARTY", "BUSINESS_PARTNER", None, customer, False),
                 dep("USES_MATERIAL", "MATERIAL", None, material, False)]
    return canonical(f"{sid(exercise)}_SALES_ORDER_{suffix}", "SALES_ORDER", "TRANSACTION",
        exercise, evidence,
        {"order_type": order_type, "sales_organization": "1010",
         "distribution_channel": "10", "sales_division": "00",
         "sold_to_party": customer, "ship_to_party": None,
         "customer_reference": customer_reference,
         "requested_delivery_date": requested_date,
         "items": [{"line_id": "10", "material": material, "quantity": quantity,
                    "unit": None, "plant": None, "ship_to_party": None,
                    "shipping_point": None, "route": None, "net_weight": None,
                    "net_weight_unit": None, "item_category": None}],
         "payment_terms": None, "processing_status": processing_status,
         "completeness_state": None, "pricing_elements": []},
        base_deps + (dependencies or []), confidence)


ORG = f"{sid(1)}_SALES_ORGANIZATION_1010"
CHANNEL = f"{sid(1)}_DISTRIBUTION_CHANNEL_GROUP"
DIV00 = f"{sid(1)}_SALES_DIVISION_00"
DIV03 = f"{sid(1)}_SALES_DIVISION_03"
AREA00 = f"{sid(1)}_SALES_AREA_GROUP_00"
AREA03 = f"{sid(1)}_SALES_AREA_GROUP_03"
SHARED = f"{sid(2)}_SHARED_MASTER_DATA_ASSIGNMENT_CHANNEL_10"
COPY_OF_ZA = f"{sid(3)}_COPY_CONTROL_OF_TO_ZA_GROUP"
COPY_ZQ_OF = f"{sid(3)}_COPY_CONTROL_ZQ_GROUP_TO_OF"
COPY_ZA_LF = f"{sid(4)}_COPY_CONTROL_ZA_GROUP_TO_LF"
COPY_LF_F2 = f"{sid(5)}_COPY_CONTROL_LF_TO_F2"
TEXT_MATERIAL = f"{sid(6)}_TEXT_DETERMINATION_MATERIAL_SALES_TEXT"
TEXT_HEADER = f"{sid(7)}_TEXT_DETERMINATION_HEADER_GROUP"
OUTPUT_BA00 = f"{sid(9)}_OUTPUT_DETERMINATION_BA00"
OUTPUT_ZLD0 = f"{sid(10)}_OUTPUT_DETERMINATION_ZLD0"
OUTPUT_CONFIRM = f"{sid(11)}_OUTPUT_DETERMINATION_ORDER_CONFIRMATION_GROUP"


def build_objects() -> list[dict]:
    objects = []

    # Chapter 1: new participant distribution channel, two sales areas, and shared data.
    objects.append(canonical(ORG, "SALES_ORGANIZATION", "CUSTOMIZING", 1,
        prov(1, "Organisation commerciale", "1010"),
        {"code": "1010", "description": None, "company_code": None}))
    objects.append(canonical(CHANNEL, "DISTRIBUTION_CHANNEL", "CUSTOMIZING", 1,
        prov(1, "Canal de distribution / désignation", "D# ou E# selon groupe; Canal groupe ##",
             "D1-D0 pour groupes 01-10; E1-E0 pour groupes 11-20; Canal groupe ##"),
        {"code": "D# or E#", "description": "Canal groupe ##", "sales_organization": "1010"},
        [dep("ASSIGNED_TO", "SALES_ORGANIZATION", ORG, "affecter à l'organisation commerciale 1010")],
        "MEDIUM"))
    for division_id, code in ((DIV00, "00"), (DIV03, "03")):
        objects.append(canonical(division_id, "SALES_DIVISION", "CUSTOMIZING", 1,
            prov(1, "Secteur d'activité", code), {"code": code, "description": None}))
    for area_id, division_id, code in ((AREA00, DIV00, "00"), (AREA03, DIV03, "03")):
        objects.append(canonical(area_id, "SALES_AREA", "CUSTOMIZING", 1,
            prov(1, "Domaine commercial / règle d'affectation secteur d'activité", f"1010 / D# ou E# / {code}; règle 1"),
            {"sales_organization": "1010", "distribution_channel": "D# or E#",
             "sales_division": code, "business_area_assignment_rule": "1"},
            [dep("USES_SALES_ORGANIZATION", "SALES_ORGANIZATION", ORG, "1010"),
             dep("USES_DISTRIBUTION_CHANNEL", "DISTRIBUTION_CHANNEL", CHANNEL, "canal créé"),
             dep("USES_SALES_DIVISION", "SALES_DIVISION", division_id, code)]))

    objects.append(canonical(SHARED, "SHARED_MASTER_DATA_ASSIGNMENT", "CUSTOMIZING", 2,
        prov(2, "Canal de distribution commun", "1010; source 10; cible D# ou E#; conditions, clients et articles"),
        {"sales_organization": "1010", "source_distribution_channel": "10",
         "target_distribution_channel": "D# or E#", "source_sales_division": None,
         "target_sales_division": None,
         "scope": ["PRICING_CONDITIONS", "CUSTOMER_MASTER", "MATERIAL_MASTER"]},
        [dep("TARGETS", "DISTRIBUTION_CHANNEL", CHANNEL, "nouveau canal du groupe")]))
    objects.append(order(2, "COMMON_MASTER_DATA_TEST", "CDCL", "C650-A##", "##-2-2",
        "P650-1##", 10, relative("dans une semaine", "P1W"),
        [dep("USES_SHARED_MASTER_DATA", "SHARED_MASTER_DATA_ASSIGNMENT", SHARED,
             "accès au prix PR00 du canal 10")]))

    # Chapter 2: four copy-control records and source-backed follow-on transactions.
    objects.append(canonical(COPY_OF_ZA, "COPY_CONTROL", "CUSTOMIZING", 3,
        prov(3, "Pilotage de la copie offre vers commande", "OF -> ZA##; exigence 002; routine en-tête 951"),
        {"source_document_type": "OF", "target_document_type": "ZA##", "level": "HEADER",
         "requirements": ["002_DIFFERENT_CUSTOMER_ALLOWED"], "source_item_category": None,
         "pricing_type": None, "data_transfer_routine": "951_VBAK",
         "reference_number_rule": None, "assignment_number_rule": None,
         "billing_quantity_rule": None, "positive_negative_quantity": None,
         "target_item_category": None, "copy_requirement": "002",
         "grouping_requirement": None, "header_data_transfer_routine": "951",
         "item_data_transfer_routine": None, "document_flow_update": None,
         "pricing_source": None}))
    objects.append(canonical(COPY_ZQ_OF, "COPY_CONTROL", "CUSTOMIZING", 3,
        prov(3, "Pilotage de la copie offre de référence", "ZQ## -> OF; client différent admis; quantité positive/négative vide"),
        {"source_document_type": "ZQ##", "target_document_type": "OF", "level": "HEADER_AND_ITEM",
         "requirements": ["DIFFERENT_CUSTOMER_ALLOWED"], "source_item_category": None,
         "pricing_type": None, "data_transfer_routine": None,
         "reference_number_rule": None, "assignment_number_rule": None,
         "billing_quantity_rule": None, "positive_negative_quantity": "BLANK",
         "target_item_category": None, "copy_requirement": None,
         "grouping_requirement": None, "header_data_transfer_routine": None,
         "item_data_transfer_routine": None, "document_flow_update": None,
         "pricing_source": None}, confidence="MEDIUM"))
    objects.append(order(3, "FROM_QUOTATION_DIFFERENT_CUSTOMER", "ZA##", "C650-B##", "##-1-1.4",
        "P650-1##", None, None,
        [dep("CONTROLLED_BY", "COPY_CONTROL", COPY_OF_ZA, "OF vers ZA##"),
         dep("REFERENCES", "QUOTATION", None, "offre OF créée dans la tâche précédente")],
        confidence="MEDIUM"))
    ex3_same_order = order(3, "FROM_QUOTATION_SAME_CUSTOMER", "ZA##", "C650-A##", "##-1-2.6",
        "P650-1##", 4, None,
        [dep("CONTROLLED_BY", "COPY_CONTROL", COPY_OF_ZA, "OF vers ZA##"),
         dep("REFERENCES", "QUOTATION", None, "même offre OF")])
    ex3_same_order["provenance"] += [ref(6, "EXERCISE", 89, "Commande créée précédemment", "commande avec référence ##-1-2.6"),
                                      ref(6, "SOLUTION", 90, "Source du texte article", "objet VBBP; ID texte 0001")]
    objects.append(ex3_same_order)

    objects.append(canonical(COPY_ZA_LF, "COPY_CONTROL", "CUSTOMIZING", 4,
        prov(4, "Pilotage copie commande vers livraison", "ZA## -> LF; en-tête 001/051/001; poste TAN 101/699; flux mis à jour"),
        {"source_document_type": "ZA##", "target_document_type": "LF", "level": "HEADER_AND_ITEM",
         "requirements": ["001_HEADER", "101_ITEM"], "source_item_category": None,
         "pricing_type": None, "data_transfer_routine": None,
         "reference_number_rule": None, "assignment_number_rule": None,
         "billing_quantity_rule": None, "positive_negative_quantity": None,
         "target_item_category": "TAN", "copy_requirement": "001_HEADER;101_ITEM",
         "grouping_requirement": "051", "header_data_transfer_routine": "001",
         "item_data_transfer_routine": "699", "document_flow_update": True,
         "pricing_source": None}))
    for suffix in ("HEADER_CONTROL_TEST", "ITEM_CONTROL_TEST"):
        objects.append(canonical(f"{sid(4)}_OUTBOUND_DELIVERY_{suffix}", "OUTBOUND_DELIVERY",
            "TRANSACTION", 4,
            prov(4, "Livraison sortante / point d'expédition / date de sélection",
                 "commande créée précédemment; point d'expédition 1010; aujourd'hui + 2 semaines"),
            {"delivery_type": "LF", "ship_to_party": None, "shipping_point": "1010",
             "planned_creation_date": relative("aujourd'hui + 2 semaines", "P2W"),
             "planned_goods_issue_date": None, "items": [], "storage_location": None,
             "warehouse_number": None, "system_representations": []},
            [dep("CONTROLLED_BY", "COPY_CONTROL", COPY_ZA_LF, "ZA## vers LF"),
             dep("REFERENCES", "SALES_ORDER", None, "une des commandes créées précédemment")],
            "MEDIUM"))
    objects.append(canonical(COPY_LF_F2, "COPY_CONTROL", "CUSTOMIZING", 5,
        prov(5, "Pilotage copie livraison vers facture", "LF -> F2; exigence en-tête 003; poste TAN; source prix E"),
        {"source_document_type": "LF", "target_document_type": "F2", "level": "HEADER_AND_ITEM",
         "requirements": ["003_DELIVERY_RELATED"], "source_item_category": "TAN",
         "pricing_type": "E", "data_transfer_routine": None,
         "reference_number_rule": None, "assignment_number_rule": None,
         "billing_quantity_rule": None, "positive_negative_quantity": None,
         "target_item_category": None, "copy_requirement": "003",
         "grouping_requirement": None, "header_data_transfer_routine": None,
         "item_data_transfer_routine": None, "document_flow_update": None,
         "pricing_source": "E_DELIVERY_OR_ORDER"}))

    # Chapter 3: determination results and the participant header-text procedure.
    objects.append(canonical(TEXT_MATERIAL, "TEXT_DETERMINATION", "CUSTOMIZING", 6,
        prov(6, "Origine du texte article", "objet texte VBBP; ID 0001; texte de vente article"),
        {"procedure": None, "text_ids": ["0001"], "access_sequence": None,
         "description": "Material sales text determination result", "level": "ITEM",
         "text_object": "VBBP", "source_text_object": "MATERIAL_SALES_TEXT",
         "source_text_id": "0001", "assigned_document_types": ["ZA##"],
         "assigned_item_categories": [], "copy_reference_mode": None,
         "all_languages": None, "requirement": None},
        [dep("VERIFIES", "SALES_ORDER", ex3_same_order["object_id"], "commande ##-1-2.6")]))
    objects.append(canonical(TEXT_HEADER, "TEXT_DETERMINATION", "CUSTOMIZING", 7,
        prov(7, "Schéma / séquence / ID texte en-tête", "schéma 50+## copié de 01; séquence 90##; VBBK/Y001; exigence 1; ZA##"),
        {"procedure": "50+##", "text_ids": ["Y001"], "access_sequence": "90##",
         "description": "Texte en-tête–gr##", "level": "HEADER", "text_object": "VBBK",
         "source_text_object": "VBBK", "source_text_id": "Y001",
         "assigned_document_types": ["ZA##"], "assigned_item_categories": [],
         "copy_reference_mode": "REFERENCE_COPY", "all_languages": True,
         "requirement": "1"}))
    objects.append(order(7, "HEADER_TEXT_FROM_QUOTATION", "ZA##", "C650-B##", "##-2-4.3",
        "P650-1##", 1, None,
        [dep("USES_TEXT_DETERMINATION", "TEXT_DETERMINATION", TEXT_HEADER, "texte en-tête copié"),
         dep("REFERENCES", "QUOTATION", None, "offre OF ##-2-4.1")]))

    # Chapter 4: classic NAST and new output management configurations.
    objects.append(canonical(f"{sid(9)}_BUSINESS_PARTNER_C650_A_GROUP", "BUSINESS_PARTNER",
        "MASTER_DATA", 9, prov(9, "Client / télécopie", "C650-A##; télécopie 123456789"),
        {"partner_id": "C650-A##", "roles": ["CUSTOMER", "SOLD_TO_PARTY"], "name": None,
         "sales_areas": ["1010/10/00"], "grouping": None, "addresses": [], "currency": None,
         "shipping_conditions": None, "delivering_plant": None, "incoterms": None,
         "incoterms_location": None, "payment_terms": None, "account_assignment_group": None,
         "customer_pricing_procedure": None, "tax_classifications": [], "company_code": None,
         "reconciliation_account": None, "partner_functions": [], "fax_number": "123456789"}))
    objects.append(canonical(OUTPUT_BA00, "OUTPUT_DETERMINATION", "CUSTOMIZING", 9,
        prov(9, "Détermination message BA00", "V10000; BA00; Z001; 1010/C650-A##; FAX; date/heure 3"),
        {"procedure": "V10000", "output_types": ["BA00"], "channels": ["FAX"],
         "description": "Sales-order confirmation output", "application_object_type": "SALES_DOCUMENT",
         "framework": "NAST", "access_sequence": "Z001",
         "key_combinations": [{"fields": ["SALES_ORGANIZATION", "DISTRIBUTION_CHANNEL", "SALES_DIVISION", "CUSTOMER"]},
                              {"fields": ["SALES_ORGANIZATION", "CUSTOMER"]},
                              {"fields": ["SALES_DOCUMENT_TYPE"]}],
         "condition_records": [{"sales_organization": "1010", "customer": "C650-A##",
                                  "channel": "FAX", "send_time": "3"}],
         "processing_routines": [], "partner_role": None, "form_template": None,
         "print_queue": None, "number_of_copies": None, "send_time": "3",
         "determination_rules": [{"sales_document_type": "ZA##"}]}))
    objects.append(order(9, "BA00_OUTPUT_TEST", "ZA##", "C650-A##", "##-1-3",
        "P650-1##", 10, None, [dep("OUTPUT_BY", "OUTPUT_DETERMINATION", OUTPUT_BA00, "BA00")],
        processing_status="TESTED_SAVE_STATUS_AMBIGUOUS", confidence="MEDIUM"))

    objects.append(canonical(OUTPUT_ZLD0, "OUTPUT_DETERMINATION", "CUSTOMIZING", 10,
        prov(10, "Catégorie de message livraison", "ZLD0; V10000; séquence 0005; RLE_DELNOTE/LE_SHP_DELNOTE; LP01"),
        {"procedure": "V10000", "output_types": ["ZLD0"], "channels": ["PRINT"],
         "description": "Special delivery note", "application_object_type": "OUTBOUND_DELIVERY",
         "framework": "NAST", "access_sequence": "0005",
         "key_combinations": [{"fields": ["SALES_ORGANIZATION", "CUSTOMER"]}],
         "condition_records": [{"sales_organization": "1010", "customer": "C650-A##", "medium": "1", "send_time": "3"},
                               {"sales_organization": "1010", "customer": "C650-B##", "medium": "1", "send_time": "3"}],
         "processing_routines": [{"medium": "PRINT", "program": "RLE_DELNOTE", "form": "LE_SHP_DELNOTE"}],
         "partner_role": None, "form_template": "LE_SHP_DELNOTE", "print_queue": "LP01",
         "number_of_copies": None, "send_time": "3",
         "determination_rules": [{"shipping_point": "1010", "output_device": "LP01"}]}))
    ex10_order = order(10, "ZLD0_DELIVERY_SOURCE", "ZA##", "C650-A##", "##-4-1", "P650-100", 10,
        relative("dans une semaine", "P1W"),
        [dep("OUTPUT_CONTEXT", "OUTPUT_DETERMINATION", OUTPUT_ZLD0, "livraison ZLD0")])
    objects.append(ex10_order)
    objects.append(canonical(f"{sid(10)}_OUTBOUND_DELIVERY_ZLD0_TEST", "OUTBOUND_DELIVERY",
        "TRANSACTION", 10,
        prov(10, "Livraison sortante / message ZLD0", "commande précédente; point 1010; fin de la semaine prochaine; ZLD0"),
        {"delivery_type": None, "ship_to_party": None, "shipping_point": "1010",
         "planned_creation_date": relative("fin de la semaine prochaine", "NEXT_WEEK_END"),
         "planned_goods_issue_date": None, "items": [], "storage_location": None,
         "warehouse_number": None, "system_representations": []},
        [dep("REFERENCES", "SALES_ORDER", ex10_order["object_id"], "commande créée à l'étape précédente"),
         dep("OUTPUT_BY", "OUTPUT_DETERMINATION", OUTPUT_ZLD0, "ZLD0")]))

    objects.append(canonical(OUTPUT_CONFIRM, "OUTPUT_DETERMINATION", "CUSTOMIZING", 11,
        prov(11, "Nouvelle catégorie et règles de sortie", "ORDER_CONFIRMATION_##; SALES_DOCUMENT; ZA##; AG; C650-B##; PRINT; LP01; 1 copie"),
        {"procedure": None, "output_types": ["ORDER_CONFIRMATION_##"], "channels": ["PRINT"],
         "description": "Confirmation de commande Groupe ##", "application_object_type": "SALES_DOCUMENT",
         "framework": "NEW_OUTPUT_MANAGEMENT", "access_sequence": None,
         "key_combinations": [], "condition_records": [], "processing_routines": [],
         "partner_role": "AG", "form_template": "SD_SLS_ORDER_CONFIRM",
         "print_queue": "LP01", "number_of_copies": 1, "send_time": "1_IMMEDIATE",
         "determination_rules": [
             {"step": "OUTPUT_TYPE", "document_category": "X", "sales_document_type": "ZA##",
              "sales_organization": "1010_OPTIONAL", "output_type": "ORDER_CONFIRMATION_##"},
             {"step": "RECIPIENT", "partner_role": "AG", "exclusive": False},
             {"step": "CHANNEL", "recipient": "C650-B##", "channel": "PRINT", "exclusive": False},
             {"step": "RELEVANCE", "confirmation_status": ["C", "BLANK"], "relevant": True}]}))
    objects.append(order(11, "NEW_OUTPUT_CONFIRMATION_TEST", "ZA##", "C650-B##", "11-22-##",
        "P650-1##", 10, None,
        [dep("OUTPUT_BY", "OUTPUT_DETERMINATION", OUTPUT_CONFIRM, "ORDER_CONFIRMATION_##")]))

    # Chapter 5: explicit saved configuration instances, not UI actions or theory.
    objects.append(canonical(f"{sid(12)}_EXTENSION_CONFIGURATION_SALES_ORDER_LIST_LAYOUT",
        "EXTENSION_CONFIGURATION", "CUSTOMIZING", 12,
        prov(12, "Mise en forme liste commandes", "S4650-##; Groupe de mise en forme ##; blocages livraison/facture; initiale; utilisateur"),
        {"configuration_family": "REPORT_LAYOUT", "configuration_key": "S4650-##",
         "description": "Groupe de mise en forme ##", "target_object": "SALES_ORDER_LIST",
         "settings": [{"field": "DELIVERY_BLOCK", "visible": True},
                      {"field": "BILLING_BLOCK", "visible": True},
                      {"user_specific": True, "initial_layout": True}]}))
    objects.append(canonical(f"{sid(13)}_EXTENSION_CONFIGURATION_MATERIAL_FIELD_SELECTION",
        "EXTENSION_CONFIGURATION", "CUSTOMIZING", 13,
        prov(13, "Référence de zone / groupe / attribut", "ZM## copié de ROH; type YR##; MVKE-DWERK; groupe 95; entrée obligatoire"),
        {"configuration_family": "MATERIAL_FIELD_SELECTION",
         "configuration_key": "ZM##", "description": "Field reference for material type YR##",
         "target_object": "MATERIAL_TYPE_YR##",
         "settings": [{"copied_from": "ROH"}, {"field": "MVKE-DWERK", "canonical_term": "delivering_plant"},
                      {"field_selection_group": "95", "attribute": "REQUIRED"},
                      {"comparison_material_type": "HAWA", "attribute": "OPTIONAL"}]}))

    return propagate_dependency_readiness(objects)


def propagate_dependency_readiness(objects: list[dict]) -> list[dict]:
    by_id = {item["object_id"]: item for item in objects}
    changed = True
    while changed:
        changed = False
        for item in objects:
            if any(d["critical"] and d["status"] == "RESOLVED" and d["target_id"] in by_id
                   and by_id[d["target_id"]]["readiness_status"] == "BLOCKED"
                   for d in item["dependencies"]):
                if not any(r["code"] == "DEPENDENCY_NOT_READY" for r in item["blocking_reasons"]):
                    item["blocking_reasons"].append({"code": "DEPENDENCY_NOT_READY",
                        "message": "A resolved canonical prerequisite is not downstream-ready",
                        "field_path": "dependencies"})
                    item["readiness_status"] = "BLOCKED"
                    changed = True
    return objects


SKIPPED = [
    {"pages": [23, 26], "scenario_id": "S4650_CH1_DEMONSTRATION_COMMON_CHANNEL",
     "candidate": "instructor demonstration datasets",
     "reason": "Instructor-only examples verify the same shared-channel semantics; participant exercises remain primary."},
    {"pages": [53, 67], "scenario_id": sid(3), "candidate": "quotation instances",
     "reason": "QUOTATION is not in S4650 reviewed coverage; only dependencies are retained."},
    {"pages": [117, 119], "scenario_id": sid(8), "candidate": "standard text element",
     "reason": "A reusable standard text is not a text-determination configuration object."},
    {"pages": [193, 212], "scenario_id": "S4650_CH5_EXTENSION_THEORY",
     "candidate": "extension techniques, append fields, and reserve-field demonstrations",
     "reason": "Theory and instructor navigation are not participant configuration records; explicit exercise configurations are retained."},
    {"pages": [243, 260], "scenario_id": "S4650_CH5_CLASSIC_AND_ENHANCEMENT_FRAMEWORK",
     "candidate": "VOFM, user exits, BTE, BAdI and enhancement framework",
     "reason": "Conceptual/reference content and inspection procedures provide no saved canonical configuration instance."},
]


def parse_pdf(pdf: Path) -> tuple[list[str], dict]:
    executable = shutil.which("pdftotext") or r"C:\Program Files\Git\mingw64\bin\pdftotext.exe"
    if not Path(executable).is_file():
        raise FileNotFoundError("pdftotext is required")
    with tempfile.TemporaryDirectory() as temp_dir:
        path = Path(temp_dir) / "s4650.txt"
        subprocess.run([executable, "-layout", "-enc", "UTF-8", str(pdf), str(path)],
                       check=True, capture_output=True)
        pages = path.read_text(encoding="utf-8").split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    if len(pages) != EXPECTED_PAGES:
        raise ValueError(f"Expected {EXPECTED_PAGES} pages, got {len(pages)}")
    for number, page in EXERCISE_PAGES.items():
        if not re.search(rf"Exercice\s+{number}\b", pages[page - 1]):
            raise ValueError(f"Exercise {number} not found on page {page}")
    for number, page in SOLUTION_PAGES.items():
        if not re.search(rf"Solution\s+{number}\b", pages[page - 1]):
            raise ValueError(f"Solution {number} not found on page {page}")
    return pages, {"page_count": len(pages), "exercise_count": len(EXERCISE_PAGES),
                   "solution_count": len(SOLUTION_PAGES),
                   "copy_control_term_page_count": sum("pilotage de la copie" in p.lower() for p in pages),
                   "output_term_page_count": sum("message" in p.lower() for p in pages),
                   "extension_term_page_count": sum("extension" in p.lower() for p in pages)}


def section_inventory(objects: list[dict]) -> list[dict]:
    mentions = {}
    for item in objects:
        for source in item["provenance"]:
            if source.get("exercise"):
                mentions.setdefault(source["exercise"], set()).add(item["object_id"])
    result = []
    for exercise in range(1, 14):
        ids = sorted(mentions.get(exercise, []))
        primary = [item_id for item_id in ids if item_id.startswith(sid(exercise))]
        if exercise == 8:
            decision, reason = "SKIP", "Standard-text creation is not text-determination configuration."
        elif exercise == 6:
            decision, reason = "EXTRACT_AND_ENRICH", "Extracts determination evidence and enriches the Exercise 3 order."
        elif primary:
            decision, reason = "EXTRACT", "Concrete source-backed instance or configuration record."
        else:
            decision, reason = "SKIP", "No qualifying in-scope canonical instance."
        result.append({"scenario_id": sid(exercise), "chapter": CHAPTER[exercise],
                       "exercise": exercise, "exercise_page": EXERCISE_PAGES[exercise],
                       "solution_page": SOLUTION_PAGES[exercise], "decision": decision,
                       "reason": reason, "object_ids": ids})
    return result


def write_json(relative: str, value) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def cross_document_checks() -> dict:
    courses = ("S4600", "S4610", "S4615", "S4620")
    paths = {course: ROOT / f"data/normalized/full/{course}/objects.json" for course in courses}
    before = {course: hashlib.sha256(path.read_bytes()).hexdigest() for course, path in paths.items()}
    counts = {course: len(json.loads(path.read_text(encoding="utf-8"))["objects"])
              for course, path in paths.items()}
    after = {course: hashlib.sha256(path.read_bytes()).hexdigest() for course, path in paths.items()}
    if before != after:
        raise RuntimeError("Prior-stage artifacts changed during cross-document checks")
    return {"prior_stage_normalized_sha256": before, "prior_stage_object_counts": counts,
            "explicit_cross_document_links": [],
            "assessment": "S4650 participant identifiers are course-local; no exact identifier joins a prior staged object.",
            "return_delivery_issue": {"status": "UNRESOLVED_CARRIED_FORWARD",
                "s4600_object_id": "S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER",
                "s4650_evidence": None,
                "assessment": "S4650 copy-control exercises concern standard quotation/order/delivery/billing flows and provide no explicit customer-return direction evidence."}}


def main() -> None:
    entries = [entry for entry in load_manifest(ROOT) if entry["logical_name"] == COURSE]
    if len(entries) != 1:
        raise ValueError("S4650 must resolve exactly once")
    pdf = resolve_document(ROOT, COURSE, verify_checksum=True)
    if pdf.name != SOURCE_FILE:
        raise ValueError(pdf.name)
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(f"Unexpected S4650 hash {digest}")
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
    write_json("data/extracted/full/S4650/objects.json", {"objects": extracted})
    write_json("data/normalized/full/S4650/objects.json", {"objects": objects})
    write_json("metadata/lineage/full/S4650/lineage.json", {"objects": [
        {"object_id": item["object_id"], "scenario_id": item["scenario_id"],
         "source_to_canonical": [{"page": source["page"], "section_type": source["section_type"],
             "source_term": source["source_term"], "raw_excerpt": source["raw_excerpt"]}
             for source in item["provenance"]],
         "solution_enrichments": [{"page": source["page"], "source_term": source["source_term"]}
             for source in item["provenance"] if source["section_type"] == "SOLUTION"]}
        for item in objects]})
    write_json("metadata/lineage/full/S4650/section_inventory.json",
               {"sections": section_inventory(objects), "skipped_candidates": SKIPPED,
                "document_coverage": {"pages_processed": [1, 267], "chapters_processed": [1, 2, 3, 4, 5],
                                      "exercise_solution_pairs": 13}})
    write_json("metadata/lineage/full/S4650/cross_document_checks.json", cross_document_checks())
    graph = {"nodes": [{"object_id": item["object_id"], "object_type": item["object_type"],
                         "readiness_status": item["readiness_status"]} for item in objects],
             "edges": [{"source": item["object_id"], "target": d["target_id"],
                         "target_type": d["target_type"], "relation": d["relation"],
                         "status": d["status"], "critical": d["critical"],
                         "source_phrase": d["source_phrase"]}
                        for item in objects for d in item["dependencies"]]}
    write_json("metadata/dependencies/full/S4650/dependency_graph.json", graph)
    write_json("metadata/confidence/full/S4650/confidence.json", {"objects": [
        {"object_id": item["object_id"], "object_type": item["object_type"],
         "confidence": item["validation"]["confidence"],
         "readiness_status": item["readiness_status"],
         "blocking_reason_codes": [reason["code"] for reason in item["blocking_reasons"]]}
        for item in objects]})
    summary = {"source": {"logical_name": COURSE, "source_file": pdf.name,
                           "sha256": digest, **parse_stats},
               "object_count": len(objects),
               "counts_by_type": dict(sorted(Counter(item["object_type"] for item in objects).items())),
               "classification_counts": dict(sorted(Counter(item["classification"] for item in objects).items())),
               "readiness_counts": dict(sorted(Counter(item["readiness_status"] for item in objects).items())),
               "confidence_counts": dict(sorted(Counter(item["validation"]["confidence"] for item in objects).items())),
               "placeholder_count": sum(len(item["placeholders"]) for item in objects),
               "objects_with_placeholders": sum(bool(item["placeholders"]) for item in objects),
               "dependency_edge_count": len(graph["edges"]),
               "unresolved_dependency_count": sum(edge["status"] == "UNRESOLVED" for edge in graph["edges"]),
               "schema_valid_count": len(objects), "schema_invalid_count": 0,
               "source_pages_processed": [1, len(pages)]}
    write_json("metadata/confidence/full/S4650/extraction_summary.json", summary)


if __name__ == "__main__":
    main()
