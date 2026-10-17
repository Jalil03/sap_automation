"""Deterministic, source-verified Phase 1B Stage 4 extraction for S4620 only."""
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

COURSE = "S4620"
SOURCE_FILE = "S4620_FR_Col12_ILT_FV_Inst_A4.pdf"
EXPECTED_PAGES = 351
EXERCISE_PAGES = {1: 19, 2: 31, 3: 49, 4: 51, 5: 57, 6: 63, 7: 83,
                  8: 89, 9: 93, 10: 127, 11: 133, 12: 147, 13: 151,
                  14: 155, 15: 173, 16: 183, 17: 189, 18: 217, 19: 231,
                  20: 259, 21: 281, 22: 295, 23: 301, 24: 313, 25: 317,
                  26: 323, 27: 329}
SOLUTION_PAGES = {1: 23, 2: 32, 3: 50, 4: 53, 5: 59, 6: 66, 7: 85,
                  8: 91, 9: 98, 10: 129, 11: 135, 12: 148, 13: 152,
                  14: 156, 15: 177, 16: 185, 17: 192, 18: 223, 19: 233,
                  20: 262, 21: 283, 22: 297, 23: 303, 24: 314, 25: 319,
                  26: 325, 27: 330}
CHAPTER = {**{i: 1 for i in range(1, 7)}, **{i: 2 for i in range(7, 10)},
           **{i: 3 for i in range(10, 15)}, **{i: 4 for i in range(15, 18)},
           18: 5, 19: 5, 20: 6, **{i: 7 for i in range(21, 28)}}


def sid(exercise: int) -> str:
    return f"S4620_CH{CHAPTER[exercise]}_EX{exercise}"


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


def canonical(object_id: str, object_type: str, classification: str, scenario_id: str,
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
            "classification": classification, "scenario_id": scenario_id,
            "provenance": provenance, "lifecycle_status": "VALIDATED",
            "readiness_status": "BLOCKED" if reasons else "READY",
            "blocking_reasons": reasons, "dependencies": dependencies,
            "placeholders": placeholders,
            "validation": {"schema_valid": True, "issues": [], "confidence": confidence},
            "data": data}


def condition(object_id: str, exercise: int, condition_type: str, key: dict,
              *, rate: float | None = None, currency: str | None = None,
              pricing_unit: float | None = None, scales: list[dict] | None = None,
              scale_basis: str | None = None, rate_unit: str | None = None,
              semantics: str | None = None, provenance: list[dict] | None = None,
              dependencies: list[dict] | None = None, confidence: str = "HIGH",
              **extra) -> dict:
    data = {"condition_type": condition_type, "key_combination": key,
            "valid_from": extra.pop("valid_from", None), "valid_to": extra.pop("valid_to", None),
            "rate": rate, "currency": currency, "pricing_unit": pricing_unit,
            "scales": scales or [], "scale_basis": scale_basis, "rate_unit": rate_unit,
            "calculation_semantics": semantics, "record_status": extra.pop("record_status", "ACTIVE"),
            "source_operation": extra.pop("source_operation", "CREATE"),
            "adjustment_percent": extra.pop("adjustment_percent", None),
            "maximum_order_count": extra.pop("maximum_order_count", None),
            "maximum_quantity": extra.pop("maximum_quantity", None),
            "maximum_quantity_unit": extra.pop("maximum_quantity_unit", None),
            "deletion_indicator": extra.pop("deletion_indicator", False)}
    if extra:
        raise ValueError(f"Unsupported condition fields: {sorted(extra)}")
    evidence = provenance or prov(exercise, "Type de condition / combinaison-clé / montant",
                                  f"{condition_type}; {key}; {rate} {currency or rate_unit or ''}")
    return canonical(object_id, "PRICING_CONDITION", "MASTER_DATA", sid(exercise),
                     evidence, data, dependencies, confidence)


def order(exercise: int, suffix: str, customer_ref: str, customer: str, items: list[tuple],
          *, order_type: str = "CDCL", pricing_elements: list[dict] | None = None,
          dependencies: list[dict] | None = None, confidence: str = "HIGH") -> dict:
    item_data = [{"line_id": str((index + 1) * 10), "material": material,
                  "quantity": quantity, "unit": unit, "plant": None,
                  "ship_to_party": None, "shipping_point": None, "route": None,
                  "net_weight": None, "net_weight_unit": None, "item_category": None}
                 for index, (material, quantity, unit) in enumerate(items)]
    deps = [dep("SOLD_TO_PARTY", "BUSINESS_PARTNER", None, customer, False)]
    deps += [dep("USES_MATERIAL", "MATERIAL", None, material, False)
             for material, _, _ in items]
    deps += dependencies or []
    excerpt = f"{order_type}; 1010/10/00; {customer}; {customer_ref}; " + "; ".join(
        f"{m} {q} {u}" for m, q, u in items)
    return canonical(f"{sid(exercise)}_SALES_ORDER_{suffix}", "SALES_ORDER", "TRANSACTION",
        sid(exercise), prov(exercise, "Type de commande / domaine commercial / donneur d'ordre / référence client / article / quantité", excerpt),
        {"order_type": order_type, "sales_organization": "1010", "distribution_channel": "10",
         "sales_division": "00", "sold_to_party": customer, "ship_to_party": None,
         "customer_reference": customer_ref,
         "requested_delivery_date": relative("dans une semaine", "P1W"),
         "items": item_data, "payment_terms": None, "processing_status": "SAVED",
         "completeness_state": None, "pricing_elements": pricing_elements or []},
        deps, confidence)


PR00_MATERIAL = f"{sid(1)}_PRICING_CONDITION_PR00_MATERIAL"
PR00_CUSTOMER_MATERIAL = f"{sid(1)}_PRICING_CONDITION_PR00_CUSTOMER_MATERIAL_SCALE"
K007_CUSTOMER = f"{sid(1)}_PRICING_CONDITION_K007_CUSTOMER_VALUE_SCALE"
PROC_CUSTOM = f"{sid(9)}_PRICING_PROCEDURE_Z_GROUP_PRC"
ZF_TYPE = f"{sid(9)}_CONDITION_TYPE_ZF_GROUP"
ZF_RECORD = f"{sid(9)}_PRICING_CONDITION_ZF_GROUP_FREIGHT"
ZW_TYPE = f"{sid(15)}_CONDITION_TYPE_ZW_GROUP"
ZW_RECORD = f"{sid(15)}_PRICING_CONDITION_ZW_GROUP_WEIGHT_SCALE"
K005_RECORD = f"{sid(17)}_PRICING_CONDITION_K005_FIRST_ORDER"
HIERARCHY = f"{sid(19)}_CUSTOMER_HIERARCHY_TOPCO_WESTERN_EUROPE"
HI02_RECORD = f"{sid(19)}_PRICING_CONDITION_HI02_HIERARCHY_MATERIAL"
KA00_RECORD = f"{sid(20)}_PRICING_CONDITION_KA00_SALES_DEAL"
CONTRACT = f"{sid(23)}_CONDITION_CONTRACT_SALES_REBATE"


def build_objects() -> list[dict]:
    objects = []

    # Chapter 1: explicit condition records, condition-type settings, and saved test orders.
    objects.append(condition(PR00_MATERIAL, 1, "PR00",
        {"sales_organization": "1010", "distribution_channel": "10", "customer": None,
         "material": "P620-1##", "incoterms": None, "destination_country": None,
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        rate=280, currency="EUR", pricing_unit=1,
        provenance=prov(1, "PR00 / article / organisation commerciale / canal / prix",
                        "PR00; P620-1##; 1010; 10; 280 EUR; validité par défaut")))
    qty_scales = [{"scale_basis": "QUANTITY", "threshold": q, "threshold_unit": "PC",
                   "threshold_currency": None, "amount": amount, "currency": "EUR",
                   "rate": None, "rate_unit": None, "pricing_unit": None,
                   "from_quantity": q, "quantity_unit": "PC"}
                  for q, amount in ((1, 250), (10, 240), (100, 230))]
    objects.append(condition(PR00_CUSTOMER_MATERIAL, 1, "PR00",
        {"sales_organization": "1010", "distribution_channel": "10", "customer": "C620-A##",
         "material": "P620-1##", "incoterms": None, "destination_country": None,
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        currency="EUR", scales=qty_scales, scale_basis="QUANTITY",
        provenance=prov(1, "PR00 / Client-article avec statut de validation / barème quantité",
                        "C620-A##; P620-1##; seuils 1/10/100 PC; 250/240/230 EUR")))
    value_scales = [{"scale_basis": "VALUE", "threshold": q, "threshold_unit": None,
                     "threshold_currency": "EUR", "amount": None, "currency": None,
                     "rate": rate, "rate_unit": "%", "pricing_unit": None,
                     "from_quantity": None, "quantity_unit": None}
                    for q, rate in ((100, 2), (1000, 3), (5000, 5))]
    objects.append(condition(K007_CUSTOMER, 1, "K007",
        {"sales_organization": "1010", "distribution_channel": "10", "customer": "C620-A##",
         "material": None, "incoterms": None, "destination_country": None,
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        scales=value_scales, scale_basis="VALUE", rate_unit="%", semantics="DISCOUNT",
        provenance=prov(1, "K007 / Client avec statut validation / barème valeur",
                        "C620-A##; seuils 100/1000/5000 EUR; déduction 2/3/5 %")))
    objects.append(canonical(f"{sid(2)}_CONDITION_TYPE_K007", "CONDITION_TYPE", "CUSTOMIZING",
        sid(2), prov(2, "Type de condition K007 / règle de calcul / unité de référence",
                     "K007; A - En %; B - Barème valeurs"),
        {"code": "K007", "description": "Déduction client", "calculation_type": "A_PERCENTAGE",
         "access_sequence": None, "reference_base": "B_VALUE_SCALE", "group_condition": None,
         "plus_minus_rule": "DISCOUNT_ONLY", "manual_entry_rule": "D_NOT_MANUALLY_EDITABLE",
         "condition_update": None, "scale_control": None, "copied_from_condition_type": None}))
    objects.append(order(1, "WITH_MATERIAL_PRICE", "##-1-2", "C620-A##",
        [("P620-1##", 10, None)], pricing_elements=[{"condition_type": "PR00", "rate": 280,
        "currency": "EUR", "pricing_unit": 1, "source": "AUTOMATIC"}],
        dependencies=[dep("PRICED_BY", "PRICING_CONDITION", PR00_MATERIAL,
                          "PR00 article créé à l'étape précédente")]))
    objects.append(order(1, "WITH_SCALES", "##-1-3", "C620-A##",
        [("P620-1##", 10, None)], pricing_elements=[
            {"condition_type": "PR00", "rate": 240, "currency": "EUR", "source": "AUTOMATIC"},
            {"condition_type": "K007", "rate": 3, "rate_unit": "%", "calculation_semantics": "DISCOUNT", "source": "AUTOMATIC"}],
        dependencies=[dep("PRICED_BY", "PRICING_CONDITION", PR00_CUSTOMER_MATERIAL,
                          "barème PR00 client/article"),
                      dep("DISCOUNTED_BY", "PRICING_CONDITION", K007_CUSTOMER,
                          "barème K007 client")]))
    objects.append(order(4, "MANUAL_ADJUSTMENT", "##-2-3", "C620-A##",
        [("P620-1##", 10, None)], pricing_elements=[
            {"condition_type": "RC00", "rate": -10, "currency": "EUR", "rate_unit": "PER_PIECE", "source": "MANUAL"},
            {"condition_type": "K007", "rate": 10, "rate_unit": "%", "calculation_semantics": "DISCOUNT", "source": "MANUAL_OVERRIDE"}],
        dependencies=[dep("STARTS_FROM", "PRICING_CONDITION", K007_CUSTOMER,
                          "K007 automatique modifiée manuellement", False)]))
    objects.append(order(5, "HEADER_CONDITIONS", "##-2-4", "C620-A##",
        [("P620-1##", 10, None), ("P620-2##", 10, None)], pricing_elements=[
            {"condition_type": "HB00", "rate": -100, "currency": None, "level": "HEADER", "source": "MANUAL"},
            {"condition_type": "RB00", "rate": -100, "currency": None, "level": "HEADER", "source": "MANUAL"}]))
    objects.append(order(6, "REPRICING_TYPE_B", "##-2-5", "C620-A##",
        [("P620-1##", 10, None)], pricing_elements=[
            {"condition_type": "PR00", "source": "AUTOMATIC"},
            {"condition_type": "K007", "source": "AUTOMATIC"},
            {"condition_type": "RC00", "rate": -100, "currency": None, "source": "MANUAL_REMOVED_BY_REPRICING_B"}],
        dependencies=[dep("PRICED_BY", "PRICING_CONDITION", PR00_CUSTOMER_MATERIAL, "PR00"),
                      dep("DISCOUNTED_BY", "PRICING_CONDITION", K007_CUSTOMER, "K007")]))

    # Chapter 2: inspected standard technique and the complete participant pricing model.
    table_ids = [("305", ["CUSTOMER", "MATERIAL"]),
                 ("306", ["PRICE_LIST_TYPE", "CURRENCY", "MATERIAL"]),
                 ("304", ["PRICE_LIST_TYPE", "MATERIAL"])]
    for table_id, fields in table_ids:
        objects.append(canonical(f"{sid(7)}_CONDITION_TABLE_{table_id}", "CONDITION_TABLE",
            "CUSTOMIZING", sid(7), prov(7, "Tables de conditions de la séquence PR02",
            "PR02 utilise les tables 305, 306 et 304"),
            {"table_id": table_id, "key_fields": fields, "description": None}))
    objects.append(canonical(f"{sid(7)}_ACCESS_SEQUENCE_PR02", "ACCESS_SEQUENCE", "CUSTOMIZING",
        sid(7), prov(7, "Séquence d'accès PR02 / tables de conditions",
                     "PR02; accès 10/20/30; tables 305/306/304"),
        {"code": "PR02", "condition_tables": ["305", "306", "304"], "description": None},
        [dep("USES_TABLE", "CONDITION_TABLE", f"{sid(7)}_CONDITION_TABLE_{t}", t, False)
         for t, _ in table_ids]))
    objects.append(canonical(f"{sid(7)}_CONDITION_TYPE_PR00", "CONDITION_TYPE", "CUSTOMIZING",
        sid(7), prov(7, "Type de condition PR00 / séquence d'accès", "PR00 utilise PR02"),
        {"code": "PR00", "description": "Prix", "calculation_type": None,
         "access_sequence": "PR02", "reference_base": None, "group_condition": None,
         "plus_minus_rule": None, "manual_entry_rule": None, "condition_update": None,
         "scale_control": None, "copied_from_condition_type": None},
        [dep("USES_ACCESS_SEQUENCE", "ACCESS_SEQUENCE", f"{sid(7)}_ACCESS_SEQUENCE_PR02", "PR02")]))
    objects.append(canonical(f"{sid(7)}_PRICING_PROCEDURE_RVAA01", "PRICING_PROCEDURE",
        "CUSTOMIZING", sid(7), prov(7, "Schéma de calcul standard", "RVAA01"),
        {"code": "RVAA01", "steps": [], "description": "Schéma standard",
         "exclusion_groups": []}))
    objects.append(canonical(f"{sid(8)}_PRICING_PROCEDURE_DETERMINATION_RVAA01",
        "PRICING_PROCEDURE_DETERMINATION", "CUSTOMIZING", sid(8),
        prov(8, "Détermination du schéma de calcul", "1010/10/00; schéma document A; schéma client 1; RVAA01"),
        {"sales_organization": "1010", "distribution_channel": "10", "sales_division": "00",
         "document_pricing_procedure": "A", "customer_pricing_procedure": "1",
         "pricing_procedure": "RVAA01", "quick_entry_condition_type": None,
         "determination_context": "SALES_DOCUMENT", "settlement_document_schema_group": None},
        [dep("DETERMINES", "PRICING_PROCEDURE", f"{sid(7)}_PRICING_PROCEDURE_RVAA01", "RVAA01")]))
    objects.append(canonical(f"{sid(9)}_CONDITION_TABLE_7_GROUP", "CONDITION_TABLE", "CUSTOMIZING",
        sid(9), prov(9, "Table de conditions / zones", "7##; organisation commerciale; Incoterms; pays destinataire"),
        {"table_id": "7##", "key_fields": ["SALES_ORGANIZATION", "INCOTERMS", "DESTINATION_COUNTRY"],
         "description": "Org.comm./Incoterms/Pays dest. GR##"}))
    objects.append(canonical(f"{sid(9)}_ACCESS_SEQUENCE_ZA_GROUP", "ACCESS_SEQUENCE", "CUSTOMIZING",
        sid(9), prov(9, "Séquence d'accès / accès / table", "ZA##; accès 10; table 7##"),
        {"code": "ZA##", "condition_tables": ["7##"], "description": "Séquence d'accès ##"},
        [dep("USES_TABLE", "CONDITION_TABLE", f"{sid(9)}_CONDITION_TABLE_7_GROUP", "7##")]))
    zf_prov = prov(9, "Type de condition / description / séquence d'accès", "ZF##; Fret-Gr##; ZA##")
    zf_prov += [ref(15, "EXERCISE", 174, "Base des frais de fret", "ZF## basé sur le poids brut de tous les postes"),
                ref(15, "SOLUTION", 180, "Base des frais de fret", "ZF##; condition de groupe; unité de référence D - barème poids brut")]
    objects.append(canonical(ZF_TYPE, "CONDITION_TYPE", "CUSTOMIZING", sid(9), zf_prov,
        {"code": "ZF##", "description": "Fret-Gr##", "calculation_type": None,
         "access_sequence": "ZA##", "reference_base": "D_GROSS_WEIGHT_SCALE",
         "group_condition": True, "plus_minus_rule": None, "manual_entry_rule": None,
         "condition_update": None, "scale_control": None, "copied_from_condition_type": "KF00"},
        [dep("USES_ACCESS_SEQUENCE", "ACCESS_SEQUENCE", f"{sid(9)}_ACCESS_SEQUENCE_ZA_GROUP", "ZA##")]))
    proc_prov = prov(9, "Schéma de calcul / type de condition", "Z##PRC copié de RVAA01; KF00 remplacé par ZF##")
    proc_prov += [ref(15, "EXERCISE", 174, "Ordre des types de conditions", "ZW## immédiatement avant ZF##"),
                  ref(15, "SOLUTION", 181, "Schéma de calcul", "Z##PRC contient ZW## avant ZF##"),
                  ref(16, "EXERCISE", 183, "Groupes d'exclusion", "Z1##/ZW## et Z2##/ZF##; comparaison D"),
                  ref(16, "SOLUTION", 186, "Exclusion dans Z##PRC", "ordre 10; procédure D; groupes Z1## et Z2##")]
    objects.append(canonical(PROC_CUSTOM, "PRICING_PROCEDURE", "CUSTOMIZING", sid(9), proc_prov,
        {"code": "Z##PRC", "description": "Groupe##-Schéma",
         "steps": [{"order": 1, "condition_type": "ZW##", "position": "IMMEDIATELY_BEFORE_ZF"},
                   {"order": 2, "condition_type": "ZF##", "replaces": "KF00"}],
         "exclusion_groups": [{"order": 10, "comparison_procedure": "D",
             "group_1": "Z1##", "condition_types_1": ["ZW##"],
             "group_2": "Z2##", "condition_types_2": ["ZF##"]}]},
        [dep("USES_CONDITION_TYPE", "CONDITION_TYPE", ZF_TYPE, "ZF##"),
         dep("USES_CONDITION_TYPE", "CONDITION_TYPE", ZW_TYPE, "ZW##")]))
    objects.append(canonical(f"{sid(9)}_PRICING_PROCEDURE_DETERMINATION_Z_GROUP",
        "PRICING_PROCEDURE_DETERMINATION", "CUSTOMIZING", sid(9),
        prov(9, "Détermination du schéma de calcul personnalisée",
             "1010/10/00; schéma document A; schéma client <YY>; Z##PRC; saisie rapide PR00"),
        {"sales_organization": "1010", "distribution_channel": "10", "sales_division": "00",
         "document_pricing_procedure": "A", "customer_pricing_procedure": "<YY>",
         "pricing_procedure": "Z##PRC", "quick_entry_condition_type": "PR00",
         "determination_context": "SALES_DOCUMENT", "settlement_document_schema_group": None},
        [dep("DETERMINES", "PRICING_PROCEDURE", PROC_CUSTOM, "Z##PRC")]))
    objects.append(condition(ZF_RECORD, 9, "ZF##",
        {"sales_organization": "1010", "distribution_channel": None, "customer": None,
         "material": None, "incoterms": "EXW", "destination_country": "DE",
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        rate=10, currency="EUR", semantics="FREIGHT",
        provenance=prov(9, "Enregistrement de conditions de fret", "ZF##; 1010; EXW; DE; 10 EUR"),
        dependencies=[dep("USES_CONDITION_TYPE", "CONDITION_TYPE", ZF_TYPE, "ZF##")]))
    objects.append(order(9, "CUSTOM_PRICING_MODEL", "##-3-3", "C620-A##",
        [("P620-1##", 10, None)], dependencies=[
            dep("PRICED_BY", "PRICING_CONDITION", ZF_RECORD, "ZF##"),
            dep("USES_PROCEDURE", "PRICING_PROCEDURE", PROC_CUSTOM, "Z##PRC")]))

    # Chapter 3: copied/future condition records. Exercise 13 enriches, not duplicates, Exercise 12.
    for material, suffix in (("P620-2##", "P620_2"), ("P620-3##", "P620_3")):
        p = prov(12, "Création avec référence / validité", f"PR00 article {material}; année prochaine")
        p += [ref(13, "EXERCISE", 151, "Modification du montant", f"{material}; augmentation 5 %"),
              ref(13, "SOLUTION", 152, "Modification simultanée", f"{material}; pourcentage 5")]
        objects.append(condition(f"{sid(12)}_PRICING_CONDITION_PR00_{suffix}_NEXT_YEAR", 12, "PR00",
            {"sales_organization": "1010", "distribution_channel": "10", "customer": None,
             "material": material, "incoterms": None, "destination_country": None,
             "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
            valid_from=relative("01 janvier de l'année prochaine", "NEXT_YEAR_START"),
            valid_to=relative("31 décembre de l'année prochaine", "NEXT_YEAR_END"),
            source_operation="COPY_WITH_REFERENCE", adjustment_percent=5,
            provenance=p, dependencies=[dep("COPIED_FROM", "PRICING_CONDITION", None,
                f"enregistrement PR00 existant pour {material}", False)], confidence="MEDIUM"))
    objects.append(condition(f"{sid(14)}_PRICING_CONDITION_PR00_CUSTOMER_COPY", 14, "PR00",
        {"sales_organization": "1010", "distribution_channel": "10", "customer": "C620-B##",
         "material": "P620-1##", "incoterms": None, "destination_country": None,
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        currency="EUR", scales=qty_scales, scale_basis="QUANTITY", source_operation="COPY",
        provenance=prov(14, "Copie d'enregistrement client/article", "C620-A##/P620-1## vers C620-B##/P620-1##"),
        dependencies=[dep("COPIED_FROM", "PRICING_CONDITION", PR00_CUSTOMER_MATERIAL,
                          "condition de prix propre au client C620-A## et à l'article P620-1##")]))

    # Chapters 4-6: weight pricing, condition update, hierarchy pricing, and sales-deal pricing.
    objects.append(canonical(ZW_TYPE, "CONDITION_TYPE", "CUSTOMIZING", sid(15),
        prov(15, "Type de condition / règle / condition de groupe / unité de référence",
             "ZW##; Walldorf##—Parcel; ZA##; B montant fixe; condition de groupe; D barème poids brut"),
        {"code": "ZW##", "description": "Walldorf##—Parcel", "calculation_type": "B_FIXED_AMOUNT",
         "access_sequence": "ZA##", "reference_base": "D_GROSS_WEIGHT_SCALE",
         "group_condition": True, "plus_minus_rule": None, "manual_entry_rule": None,
         "condition_update": None, "scale_control": "UNRESTRICTED_NON_MONOTONIC",
         "copied_from_condition_type": "KF00"},
        [dep("USES_ACCESS_SEQUENCE", "ACCESS_SEQUENCE", f"{sid(9)}_ACCESS_SEQUENCE_ZA_GROUP", "ZA##")]))
    weight_scales = [{"scale_basis": "QUANTITY", "threshold": q, "threshold_unit": "KG",
                      "threshold_currency": None, "amount": amount, "currency": "EUR",
                      "rate": None, "rate_unit": None, "pricing_unit": None,
                      "from_quantity": q, "quantity_unit": "KG"}
                     for q, amount in ((0, 8), (0.5, 10), (1, 12), (2, 14), (5, 16),
                                       (10, 20), (20, 30), (30.001, 0))]
    objects.append(condition(ZW_RECORD, 15, "ZW##",
        {"sales_organization": "1010", "distribution_channel": None, "customer": None,
         "material": None, "incoterms": "EXW", "destination_country": "DE",
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        currency="EUR", scales=weight_scales, scale_basis="QUANTITY", semantics="FREIGHT_BY_GROSS_WEIGHT",
        provenance=prov(15, "Barème de poids brut ZW##", "0/0,5/1/2/5/10/20/30,001 KG; 8/10/12/14/16/20/30/0 EUR",
                        solution_excerpt="30,001 kg indique supérieur à 30 kg; montant 0 EUR"),
        dependencies=[dep("USES_CONDITION_TYPE", "CONDITION_TYPE", ZW_TYPE, "ZW##")]))
    objects.append(order(15, "WEIGHT_BASED_FREIGHT", "##-5-1", "C620-A##",
        [("P620-1##", 10, None), ("P620-3##", 5, None)], dependencies=[
            dep("PRICED_BY", "PRICING_CONDITION", ZW_RECORD, "ZW##"),
            dep("PRICED_BY", "PRICING_CONDITION", ZF_RECORD, "ZF##"),
            dep("USES_PROCEDURE", "PRICING_PROCEDURE", PROC_CUSTOM, "Z##PRC")]))
    objects.append(order(16, "FREIGHT_EXCLUSION", "##-5-2", "C620-A##",
        [("P620-1##", 10, None), ("P620-3##", 10, None)], dependencies=[
            dep("PRICED_BY", "PRICING_CONDITION", ZW_RECORD, "ZW##"),
            dep("PRICED_BY", "PRICING_CONDITION", ZF_RECORD, "ZF##"),
            dep("USES_PROCEDURE", "PRICING_PROCEDURE", PROC_CUSTOM, "groupes d'exclusion Z1##/Z2##")]))
    objects.append(canonical(f"{sid(17)}_CONDITION_TYPE_K005", "CONDITION_TYPE", "CUSTOMIZING",
        sid(17), prov(17, "Type de condition K005 / MAJ conditions", "K005; case MAJ conditions cochée"),
        {"code": "K005", "description": "Déduction client-article", "calculation_type": None,
         "access_sequence": None, "reference_base": None, "group_condition": None,
         "plus_minus_rule": "DISCOUNT_ONLY", "manual_entry_rule": None,
         "condition_update": True, "scale_control": None, "copied_from_condition_type": None}))
    objects.append(condition(K005_RECORD, 17, "K005",
        {"sales_organization": "1010", "distribution_channel": "10", "customer": "C620-B##",
         "material": "P620-2##", "incoterms": None, "destination_country": None,
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        rate=-100, currency="EUR", semantics="DISCOUNT", maximum_order_count=1,
        maximum_quantity=15, maximum_quantity_unit="PC", deletion_indicator=True,
        record_status="DELETED_AFTER_TEST", provenance=prov(17, "K005 / montant / limite / code suppression",
            "K005; C620-B##; P620-2##; -100 EUR; une commande puis limite 15 pièces; suppression activée")))
    for suffix, customer_ref, qty in (("FIRST_K005", "##-5-3-1", 10),
                                      ("SECOND_K005", "##-5-3-2", 10),
                                      ("QUANTITY_LIMIT_K005", "##-5-3-3", 15)):
        objects.append(order(17, suffix, customer_ref, "C620-B##", [("P620-2##", qty, None)],
            dependencies=[dep("PRICED_BY", "PRICING_CONDITION", K005_RECORD, "K005")]))
    objects.append(order(18, "HEADER_NET_VALUE", "##-6-1", "C620-A##",
        [("P620-1##", 1, None), ("P620-2##", 2, None)], order_type="CDLC",
        pricing_elements=[{"condition_type": "HM00", "rate": 400, "currency": "EUR",
                           "level": "HEADER", "source": "MANUAL"}]))
    objects.append(order(18, "ITEM_NET_PRICE", "##-6-2", "C620-A##",
        [("P620-1##", 10, None)], order_type="CDLC",
        pricing_elements=[{"condition_type": "PN00", "rate": 200, "currency": "EUR",
                           "rate_unit": "PER_PIECE", "source": "MANUAL"}]))
    objects.append(canonical(HIERARCHY, "CUSTOMER_HIERARCHY", "MASTER_DATA", sid(19),
        prov(19, "Hiérarchie clients / affectation", "TOPCO; C620-ZEW Europe occidentale; C620-A##; 1010/10/00"),
        {"hierarchy_type": "CUSTOMER_PRICING_HIERARCHY",
         "nodes": [{"node_id": "C620-ZE", "description": "TOPCO Europe"},
                   {"node_id": "C620-ZEW", "description": "TOPCO Western Europe", "parent": "C620-ZE"},
                   {"customer": "C620-A##", "parent": "C620-ZEW"}],
         "valid_from": None, "valid_to": None,
         "sales_area": {"sales_organization": "1010", "distribution_channel": "10", "sales_division": "00"}}))
    objects.append(condition(HI02_RECORD, 19, "HI02",
        {"sales_organization": None, "distribution_channel": None, "customer": None,
         "material": "P620-2##", "incoterms": None, "destination_country": None,
         "customer_hierarchy_node": "C620-ZE", "promotion_reference": None, "sales_deal_reference": None},
        rate=50, currency="EUR", semantics="DISCOUNT",
        provenance=prov(19, "HI02 hiérarchie/article", "C620-ZE; P620-2##; remise forfaitaire 50 EUR"),
        dependencies=[dep("APPLIES_TO_HIERARCHY", "CUSTOMER_HIERARCHY", HIERARCHY, "C620-ZE")]))
    objects.append(order(19, "HIERARCHY_PRICING", "##-6-5", "C620-A##",
        [("P620-2##", 1, None)], order_type="CDLC",
        dependencies=[dep("PRICED_BY", "PRICING_CONDITION", HI02_RECORD, "HI02"),
                      dep("CUSTOMER_IN_HIERARCHY", "CUSTOMER_HIERARCHY", HIERARCHY, "TOPCO")]))
    objects.append(condition(KA00_RECORD, 20, "KA00",
        {"sales_organization": "1010", "distribution_channel": "10", "customer": "C620-B##",
         "material": "P620-2##", "incoterms": None, "destination_country": None,
         "customer_hierarchy_node": None, "promotion_reference": None, "sales_deal_reference": None},
        rate=10, rate_unit="%", semantics="DISCOUNT", confidence="MEDIUM",
        provenance=prov(20, "KA00 / action commerciale / client / article / remise",
            "KA00; action commerciale créée depuis promotion; C620-B##; P620-2##; 10 %",
            solution_excerpt="KA00; C620-B##; P620-2# (coquille d'un # dans la solution); remise 10 %")))
    objects.append(order(20, "SALES_DEAL", "##-9-2", "C620-B##", [("P620-2##", 10, None)],
        order_type="CDLC", dependencies=[dep("PRICED_BY", "PRICING_CONDITION", KA00_RECORD, "KA00")]))

    # Chapter 7: settlement determination, source orders, contract, and settlement documents.
    objects.append(canonical(f"{sid(21)}_PRICING_PROCEDURE_A10005", "PRICING_PROCEDURE",
        "CUSTOMIZING", sid(21), prov(21, "Schéma de calcul du document de décompte",
                                      "A10005 - Ristourne (DE)"),
        {"code": "A10005", "steps": [], "description": "Ristourne (DE)", "exclusion_groups": []}))
    objects.append(canonical(f"{sid(21)}_PRICING_PROCEDURE_DETERMINATION_SETTLEMENT",
        "PRICING_PROCEDURE_DETERMINATION", "CUSTOMIZING", sid(21),
        prov(21, "Détermination pour document de décompte", "groupe de schémas 0S; schéma A10005"),
        {"sales_organization": None, "distribution_channel": None, "sales_division": None,
         "document_pricing_procedure": None, "customer_pricing_procedure": None,
         "pricing_procedure": "A10005", "quick_entry_condition_type": None,
         "determination_context": "SETTLEMENT_DOCUMENT",
         "settlement_document_schema_group": "0S"},
        [dep("DETERMINES", "PRICING_PROCEDURE", f"{sid(21)}_PRICING_PROCEDURE_A10005", "A10005")]))
    ex22_orders = []
    for suffix, customer_ref in (("BUSINESS_VOLUME_1", "##-9-1"), ("BUSINESS_VOLUME_2", "##-9-2")):
        obj = order(22, suffix, customer_ref, "C620-B##", [("P620-3##", 10, None)], order_type="CDLC")
        objects.append(obj); ex22_orders.append(obj["object_id"])
    contract_prov = prov(23, "Contrat de conditions / critères de CA / conditions / calendrier",
        "0S01; C620-B##; P620-3##; 01/01-31/12/AAAA; RES1 10 EUR/pce; REA1 -10 EUR/pce; AJ")
    objects.append(canonical(CONTRACT, "CONDITION_CONTRACT", "MASTER_DATA", sid(23), contract_prov,
        {"contract_id": None, "contract_type": "0S01_SALES_REBATE", "business_partner": "C620-B##",
         "valid_from": relative("01/01/AAAA (premier jour de l'année en cours)", "CURRENT_YEAR_START"),
         "valid_to": relative("31/12/AAAA (dernier jour de l'année en cours)", "CURRENT_YEAR_END"),
         "conditions": [{"condition_type": "RES1", "calculation_rule": "QUANTITY", "rate": 10,
                          "currency": "EUR", "pricing_unit": 1, "quantity_unit": "PC"},
                        {"condition_type": "REA1", "calculation_rule": "QUANTITY", "rate": -10,
                          "currency": "EUR", "pricing_unit": 1, "quantity_unit": "PC"}],
         "sales_area": {"sales_organization": "1010", "distribution_channel": "10", "sales_division": "00"},
         "business_volume_selection_criteria": [{"criterion": "0001_CUSTOMER", "value": "C620-B##"},
                                                {"criterion": "0009_MATERIAL", "value": "P620-3##"}],
         "settlement_schedule": [{"calendar": "AJ_ANNUAL_AGREEMENT", "type": "FINAL",
                                  "date": "31.12.AAAA"}],
         "settlement_material": None, "contract_status": "VALIDATED_AND_SAVED"},
        [dep("BUSINESS_VOLUME_FROM", "SALES_ORDER", object_id,
             "factures issues des commandes créées à l'exercice 22", False)
         for object_id in ex22_orders]))
    delta_id = f"{sid(24)}_SETTLEMENT_DOCUMENT_DELTA_ACCRUAL"
    objects.append(canonical(delta_id, "SETTLEMENT_DOCUMENT", "TRANSACTION", sid(24),
        prov(24, "Provisions delta / date / montant", "date du jour; exécution réelle; 200 EUR"),
        {"settlement_type": "DELTA_ACCRUAL", "condition_contract": None,
         "settlement_date": relative("date du jour", "P0D"), "amount": 200, "currency": "EUR",
         "execution_type": "ACTUAL_RUN", "document_id": None, "settlement_status": "CREATED",
         "business_volume": {"source": "PRIOR_BILLINGS", "order_count": 2},
         "accounting_metadata": [{"entry": "REBATE_ACCRUAL_PAYABLE", "amount": -200, "currency": "EUR",
                                  "accounting_document_id": None}]},
        [dep("SETTLES", "CONDITION_CONTRACT", CONTRACT, "contrat créé à l'exercice précédent")]))
    partial_id = f"{sid(25)}_SETTLEMENT_DOCUMENT_PARTIAL_CREDIT"
    objects.append(canonical(partial_id, "SETTLEMENT_DOCUMENT", "TRANSACTION", sid(25),
        prov(25, "Décompte partiel / volume d'affaires / montant", "20 pièces; REBV 5 360; avoir net 200 EUR"),
        {"settlement_type": "PARTIAL_SETTLEMENT_CREDIT", "condition_contract": None,
         "settlement_date": relative("date du jour", "P0D"), "amount": 200, "currency": "EUR",
         "execution_type": "ACTUAL_RUN", "document_id": None, "settlement_status": "CREATED",
         "business_volume": {"quantity": 20, "quantity_unit": "PC", "rebate_volume": 5360,
                             "currency": None, "source_billing_count": 2},
         "accounting_metadata": [{"entry": "CUSTOMER_CREDIT", "amount": 200, "currency": "EUR",
                                  "accounting_document_id": None}]},
        [dep("SETTLES", "CONDITION_CONTRACT", CONTRACT, "contrat de conditions"),
         dep("FOLLOWS", "SETTLEMENT_DOCUMENT", delta_id, "provisions delta déjà décomptées")]))
    ex26_order = order(26, "ADDITIONAL_BUSINESS_VOLUME", "##-9-3", "C620-B##",
                       [("P620-3##", 10, None), ("P620-2##", 5, None)], order_type="CDLC")
    objects.append(ex26_order)
    objects.append(canonical(f"{sid(27)}_SETTLEMENT_DOCUMENT_FINAL_CREDIT", "SETTLEMENT_DOCUMENT",
        "TRANSACTION", sid(27), prov(27, "Décompte final / date / montant net",
                                     "31.12.AAAA; exécution réelle; avoir net 100 EUR"),
        {"settlement_type": "FINAL_SETTLEMENT_CREDIT", "condition_contract": None,
         "settlement_date": relative("31.12.AAAA (date de fin de l'exercice)", "CURRENT_YEAR_END"),
         "amount": 100, "currency": "EUR", "execution_type": "ACTUAL_RUN",
         "document_id": None, "settlement_status": "CREATED",
         "business_volume": {"eligible_material": "P620-3##", "total_quantity": 30,
                             "quantity_unit": "PC", "previously_settled_quantity": 20},
         "accounting_metadata": [{"entry": "CUSTOMER_CREDIT", "amount": 100, "currency": "EUR",
                                  "accounting_document_id": None}]},
        [dep("SETTLES", "CONDITION_CONTRACT", CONTRACT, "contrat de conditions"),
         dep("FOLLOWS", "SETTLEMENT_DOCUMENT", partial_id, "décompte partiel antérieur"),
         dep("BUSINESS_VOLUME_FROM", "SALES_ORDER", ex26_order["object_id"],
             "processus de vente supplémentaire", False)]))

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
                    item["readiness_status"] = "BLOCKED"; changed = True
    return objects


SKIPPED = [
    {"pages": [49, 50], "scenario_id": sid(3), "candidate": "condition-technique terminology",
     "reason": "Concept questions only; no additional record beyond explicit objects in Exercises 7-9."},
    {"pages": [63, 69], "scenario_id": sid(6), "candidate": "F1/F2 copy control and billing",
     "reason": "COPY_CONTROL/BILLING are outside S4620 coverage; billing was saved but its identifier is blank."},
    {"pages": [127, 138], "scenario_id": sid(10), "candidate": "condition-list menu and variant",
     "reason": "UI/reporting configuration has no approved S4620 canonical type."},
    {"pages": [133, 145], "scenario_id": sid(11), "candidate": "condition list definition",
     "reason": "Reporting/list definition is not a condition record or approved canonical type."},
    {"pages": [259, 266], "scenario_id": sid(20), "candidate": "promotion, sales deal, delivery, billing",
     "reason": "Promotion/sales-deal types are absent from the taxonomy; delivery/billing are outside S4620 coverage. KA00 and the sales order are retained."},
    {"pages": [295, 300], "scenario_id": sid(22), "candidate": "deliveries and billing documents",
     "reason": "Outside S4620 coverage and generated identifiers are blank; source orders are retained as settlement-volume dependencies."},
    {"pages": [323, 326], "scenario_id": sid(26), "candidate": "delivery and billing",
     "reason": "Outside S4620 coverage and generated identifiers are blank; the explicit sales order is retained."},
    {"pages": [332, 334], "scenario_id": "S4620_CH7_OPTIONAL_DEMO_CONTRACT", "candidate": "optional alternate condition contract",
     "reason": "Instructor-only optional English demonstration marked 'When in doubt leave it out'; it is not a completed participant instance."},
]


def parse_pdf(pdf: Path) -> tuple[list[str], dict]:
    executable = shutil.which("pdftotext") or r"C:\Program Files\Git\mingw64\bin\pdftotext.exe"
    if not Path(executable).is_file():
        raise FileNotFoundError("pdftotext is required")
    with tempfile.TemporaryDirectory() as tmp:
        text_path = Path(tmp) / "s4620.txt"
        subprocess.run([executable, "-layout", "-enc", "UTF-8", str(pdf), str(text_path)],
                       check=True, capture_output=True)
        text = text_path.read_text(encoding="utf-8")
    pages = text.split("\f")
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
                   "condition_term_page_count": sum("condition" in page.lower() for page in pages)}


def section_inventory(objects: list[dict]) -> list[dict]:
    mentions = {}
    for item in objects:
        for source in item["provenance"]:
            if source.get("exercise"):
                mentions.setdefault(source["exercise"], set()).add(item["object_id"])
    decisions = {3: ("SKIP", "Theory questions only."), 10: ("SKIP", "UI/report menu only."),
                 11: ("SKIP", "Condition-list reporting only."),
                 13: ("ENRICH_EXISTING", "Adds 5% adjustment evidence to Exercise 12 records.")}
    result = []
    for exercise in range(1, 28):
        ids = sorted(mentions.get(exercise, []))
        primary = [item_id for item_id in ids if item_id.startswith(sid(exercise))]
        if exercise in decisions:
            decision, reason = decisions[exercise]
        elif primary:
            decision, reason = "EXTRACT", "Concrete source-backed instance or configuration record."
        elif ids:
            decision, reason = "ENRICH_EXISTING", "Explicit evidence enriches a prior scenario object."
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
    paths = {course: ROOT / f"data/normalized/full/{course}/objects.json"
             for course in ("S4600", "S4610", "S4615")}
    before = {course: hashlib.sha256(path.read_bytes()).hexdigest() for course, path in paths.items()}
    counts = {course: len(json.loads(path.read_text(encoding="utf-8"))["objects"])
              for course, path in paths.items()}
    after = {course: hashlib.sha256(path.read_bytes()).hexdigest() for course, path in paths.items()}
    if before != after:
        raise RuntimeError("Prior-stage artifacts changed during cross-document checks")
    return {"prior_stage_normalized_sha256": before, "prior_stage_object_counts": counts,
            "explicit_cross_document_links": [],
            "assessment": "S4620 examples use course-local participant identifiers; no explicit identifier joins a prior staged object.",
            "return_delivery_issue": {"status": "UNRESOLVED_CARRIED_FORWARD",
                "s4600_object_id": "S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER",
                "s4620_evidence": None,
                "assessment": "S4620 pricing and settlement content supplies no explicit directional evidence for the S4600 customer-return delivery."}}


def main() -> None:
    entries = [entry for entry in load_manifest(ROOT) if entry["logical_name"] == COURSE]
    if len(entries) != 1:
        raise ValueError("S4620 must resolve exactly once")
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
    write_json("data/extracted/full/S4620/objects.json", {"objects": extracted})
    write_json("data/normalized/full/S4620/objects.json", {"objects": objects})
    write_json("metadata/lineage/full/S4620/lineage.json", {"objects": [
        {"object_id": item["object_id"], "scenario_id": item["scenario_id"],
         "source_to_canonical": [{"page": source["page"], "section_type": source["section_type"],
             "source_term": source["source_term"], "raw_excerpt": source["raw_excerpt"]}
             for source in item["provenance"]],
         "solution_enrichments": [{"page": source["page"], "source_term": source["source_term"]}
             for source in item["provenance"] if source["section_type"] == "SOLUTION"]}
        for item in objects]})
    write_json("metadata/lineage/full/S4620/section_inventory.json",
               {"sections": section_inventory(objects), "skipped_candidates": SKIPPED})
    write_json("metadata/lineage/full/S4620/cross_document_checks.json", cross_document_checks())
    graph = {"nodes": [{"object_id": item["object_id"], "object_type": item["object_type"],
                         "readiness_status": item["readiness_status"]} for item in objects],
             "edges": [{"source": item["object_id"], "target": d["target_id"],
                         "target_type": d["target_type"], "relation": d["relation"],
                         "status": d["status"], "critical": d["critical"],
                         "source_phrase": d["source_phrase"]}
                        for item in objects for d in item["dependencies"]]}
    write_json("metadata/dependencies/full/S4620/dependency_graph.json", graph)
    write_json("metadata/confidence/full/S4620/confidence.json", {"objects": [
        {"object_id": item["object_id"], "object_type": item["object_type"],
         "confidence": item["validation"]["confidence"],
         "readiness_status": item["readiness_status"],
         "blocking_reason_codes": [reason["code"] for reason in item["blocking_reasons"]]}
        for item in objects]})
    summary = {"source": {"logical_name": COURSE, "source_file": pdf.name,
                           "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), **parse_stats},
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
    write_json("metadata/confidence/full/S4620/extraction_summary.json", summary)


if __name__ == "__main__":
    main()
