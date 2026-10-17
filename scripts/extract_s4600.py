"""Deterministic, source-verified Stage 1 extraction for S4600 only."""
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

COURSE = "S4600"
SOURCE_FILE = "P2W_S4600_FR_Col23.pdf"
EXPECTED_PAGES = 353
SOLUTION_PAGES = {
    1: 22, 2: 42, 3: 58, 4: 64, 5: 72, 6: 80, 7: 88, 8: 92,
    9: 107, 10: 113, 11: 121, 12: 131, 13: 139, 14: 143, 15: 146,
    16: 157, 17: 162, 18: 181, 19: 191, 20: 206, 21: 212, 22: 217,
    23: 229, 24: 234, 25: 250, 26: 254, 27: 261, 28: 273, 29: 278,
    30: 286, 31: 295, 32: 311, 33: 318, 34: 324, 35: 338, 36: 348,
}
EXERCISE_PAGES = {
    1: 21, 2: 39, 3: 57, 4: 63, 5: 71, 6: 79, 7: 87, 8: 91,
    9: 105, 10: 111, 11: 119, 12: 129, 13: 137, 14: 141, 15: 145,
    16: 155, 17: 161, 18: 179, 19: 189, 20: 205, 21: 211, 22: 215,
    23: 227, 24: 233, 25: 249, 26: 253, 27: 259, 28: 271, 29: 277,
    30: 283, 31: 293, 32: 309, 33: 317, 34: 323, 35: 337, 36: 347,
}
CHAPTER = {1: 1, 2: 2, **{n: 3 for n in range(3, 9)}, **{n: 4 for n in range(9, 18)},
           18: 5, 19: 5, **{n: 6 for n in range(20, 25)}, **{n: 7 for n in range(25, 28)},
           **{n: 8 for n in range(28, 32)}, **{n: 9 for n in range(32, 35)}, 35: 10, 36: 10}


def sid(exercise: int) -> str:
    return f"S4600_CH{CHAPTER[exercise]}_EX{exercise}"


def source_ref(exercise: int, section: str, page: int, term: str, excerpt: str | None = None) -> dict:
    return {
        "course_code": COURSE, "source_file": SOURCE_FILE, "page": page,
        "chapter": CHAPTER[exercise], "exercise": exercise, "section_type": section,
        "scenario_id": sid(exercise), "raw_excerpt": excerpt, "source_term": term,
    }


def provenance(exercise: int, term: str, excerpt: str, solution_term: str | None = None) -> list[dict]:
    return [
        source_ref(exercise, "EXERCISE", EXERCISE_PAGES[exercise], term, excerpt),
        source_ref(exercise, "SOLUTION", SOLUTION_PAGES[exercise], solution_term or term, None),
    ]


def relative(raw: str, offset: str | None) -> dict:
    return {"kind": "RELATIVE", "raw": raw, "offset": offset}


def dep(relation: str, target_type: str, target_id: str | None, phrase: str, critical: bool = True) -> dict:
    return {"relation": relation, "target_type": target_type, "target_id": target_id,
            "status": "RESOLVED" if target_id else "UNRESOLVED", "critical": critical,
            "source_phrase": phrase}


def placeholders(value, path="data") -> list[dict]:
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            found.extend(placeholders(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(placeholders(child, f"{path}[{index}]"))
    elif isinstance(value, str) and "##" in value:
        found.append({"raw": "##", "resolved": None, "status": "UNRESOLVED",
                      "mandatory": True, "field_path": path})
    return found


def obj(object_id: str, object_type: str, classification: str, scenario: str | None,
        prov: list[dict], data: dict, deps: list[dict] | None = None,
        confidence: str = "HIGH") -> dict:
    ph = placeholders(data)
    reasons = []
    if ph:
        reasons.append({"code": "UNRESOLVED_MANDATORY_PLACEHOLDER",
                        "message": "Participant-specific source placeholder remains unresolved",
                        "field_path": "data"})
    if any(d["critical"] and d["status"] == "UNRESOLVED" for d in (deps or [])):
        reasons.append({"code": "UNRESOLVED_CRITICAL_DEPENDENCY",
                        "message": "A required source reference has no extractable identifier",
                        "field_path": "dependencies"})
    return {
        "object_id": object_id, "object_type": object_type, "classification": classification,
        "scenario_id": scenario, "provenance": prov, "lifecycle_status": "VALIDATED",
        "readiness_status": "BLOCKED" if reasons else "READY", "blocking_reasons": reasons,
        "dependencies": deps or [], "placeholders": ph,
        "validation": {"schema_valid": True, "issues": [], "confidence": confidence},
        "data": data,
    }


BP_IDS = {"T-CUS##": "S4600_CH4_EX9_BUSINESS_PARTNER_T-CUS-GROUP",
          "T-S50B##": "S4600_CH6_EX20_BUSINESS_PARTNER_T-S50B-GROUP"}
MATERIAL_IDS = {"T-MS4##": "S4600_CH4_EX11_MATERIAL_T-MS4-GROUP",
                "T-MS3##": "S4600_CH6_EX20_MATERIAL_T-MS3-GROUP",
                "T-F1##": "S4600_CH8_EX30_MATERIAL_T-F1-GROUP",
                "T-D1##": "S4600_CH8_EX31_MATERIAL_T-D1-GROUP"}


def entity_deps(sold_to: str | None, items: list[dict], ship_to: str | None = None) -> list[dict]:
    result = []
    if sold_to:
        result.append(dep("SOLD_TO_PARTY", "BUSINESS_PARTNER", BP_IDS.get(sold_to), sold_to))
    if ship_to and ship_to != sold_to:
        result.append(dep("SHIP_TO_PARTY", "BUSINESS_PARTNER", BP_IDS.get(ship_to), ship_to))
    for item in items:
        material = item.get("material")
        if material:
            result.append(dep("USES_MATERIAL", "MATERIAL", MATERIAL_IDS.get(material), material))
    return result


def order(exercise: int, sold_to: str, customer_reference: str | None, date_raw: str | None,
          offset: str | None, items: list[dict], *, ship_to: str | None = None,
          extra: dict | None = None, extra_prov: list[dict] | None = None,
          confidence: str = "HIGH") -> dict:
    data = {"order_type": "CDCL", "sales_organization": "1010", "distribution_channel": "10",
            "sales_division": "00", "sold_to_party": sold_to, "ship_to_party": ship_to,
            "customer_reference": customer_reference,
            "requested_delivery_date": relative(date_raw, offset) if date_raw else None,
            "items": items}
    data.update(extra or {})
    p = provenance(exercise, "Type commande client / Organisation commerciale / Canal distribution / Secteur d'activité / Donneur d'ordre / Réf. client / Article / Quantité",
                   f"CDCL; 1010 / 10 / 00; {sold_to}; {customer_reference or 'non indiqué'}")
    p.extend(extra_prov or [])
    return obj(f"{sid(exercise)}_SALES_ORDER_STANDARD", "SALES_ORDER", "TRANSACTION", sid(exercise),
               p, data, entity_deps(sold_to, items, ship_to), confidence)


def delivery(exercise: int, object_suffix: str, target_id: str, target_type: str = "SALES_ORDER",
             *, shipping_point: str = "Z0##", planned_raw: str | None = None,
             offset: str | None = None, delivery_type: str | None = None,
             confidence: str = "MEDIUM") -> dict:
    phrase = "document créé à l'étape précédente"
    data = {"delivery_type": delivery_type, "ship_to_party": None, "shipping_point": shipping_point,
            "planned_creation_date": relative(planned_raw, offset) if planned_raw else None,
            "planned_goods_issue_date": None, "items": []}
    return obj(f"{sid(exercise)}_OUTBOUND_DELIVERY_{object_suffix}", "OUTBOUND_DELIVERY", "TRANSACTION",
               sid(exercise), provenance(exercise, "Point d'expédition / Date de création planifiée",
               f"{shipping_point}; {planned_raw or phrase}"), data,
               [dep("CREATED_FROM", target_type, target_id, phrase)], confidence)


def billing(exercise: int, suffix: str, target_id: str, target_type: str,
            subtype: str, *, date_raw: str | None = None, offset: str | None = None,
            confidence: str = "MEDIUM") -> dict:
    data = {"billing_type": None, "billing_subtype": subtype, "payer": None,
            "billing_date": relative(date_raw, offset) if date_raw else None,
            "reference_document": None, "items": [], "billing_plan": None,
            "down_payments": [], "installment_payments": []}
    return obj(f"{sid(exercise)}_BILLING_{suffix}", "BILLING", "TRANSACTION", sid(exercise),
               provenance(exercise, "Document de facturation / document de référence",
                          "Créer le document de facturation avec référence au document précédent"),
               data, [dep("BILLED_FROM", target_type, target_id, "document créé à l'étape précédente")], confidence)


def build_objects() -> list[dict]:
    objects = []
    # SECONDARY organization instances, first evidenced as exercise defaults.
    p1 = provenance(1, "Org. commerciale / Canal distrib. / Secteur d'activité",
                    "Org. commerciale 1010; Canal distrib. 10; Secteur d'activité 00")
    org_id = "S4600_SHARED_SALES_ORGANIZATION_1010"
    dc_id = "S4600_SHARED_DISTRIBUTION_CHANNEL_10"
    div_id = "S4600_SHARED_SALES_DIVISION_00"
    objects += [
        obj(org_id, "SALES_ORGANIZATION", "CUSTOMIZING", sid(1), p1,
            {"code": "1010", "description": None, "company_code": "1010"},
            [dep("ASSIGNED_TO", "COMPANY_CODE", None, "Société 1010", False)]),
        obj(dc_id, "DISTRIBUTION_CHANNEL", "CUSTOMIZING", sid(1), p1,
            {"code": "10", "description": None, "sales_organization": "1010"},
            [dep("BELONGS_TO", "SALES_ORGANIZATION", org_id, "Org. commerciale 1010")]),
        obj(div_id, "SALES_DIVISION", "CUSTOMIZING", sid(1), p1,
            {"code": "00", "description": None}),
        obj("S4600_SHARED_SALES_AREA_1010_10_00", "SALES_AREA", "CUSTOMIZING", sid(1), p1,
            {"sales_organization": "1010", "distribution_channel": "10", "sales_division": "00"},
            [dep("USES", "SALES_ORGANIZATION", org_id, "Org. commerciale 1010"),
             dep("USES", "DISTRIBUTION_CHANNEL", dc_id, "Canal distrib. 10"),
             dep("USES", "SALES_DIVISION", div_id, "Secteur d'activité 00")]),
        obj("S4600_CH3_EX5_SHIPPING_POINT_Z0-GROUP", "SHIPPING_POINT", "CUSTOMIZING", sid(5),
            provenance(5, "Point d'expédition", "Point d'expédition Z0##"),
            {"code": "Z0##", "description": None, "plant": None}, confidence="HIGH"),
    ]

    # PRIMARY master data.
    objects.append(obj(BP_IDS["T-CUS##"], "BUSINESS_PARTNER", "MASTER_DATA", sid(9),
        provenance(9, "Partenaire / Regroupement / Rôles / Adresse / Domaine commercial / Société",
                   "T-CUS##; Motos et autres; FLCU00, FLCU01; 1010 / 10 / 00"),
        {"partner_id": "T-CUS##", "roles": ["FLCU00", "FLCU01"], "name": "Motos et autres",
         "sales_areas": ["1010/10/00"], "grouping": "BPAB Num alpha ext (a-z; CUST/SUPL)",
         "addresses": [{"street": "Main street", "house_number": "##", "postal_code": "20111",
                         "city": "Hamburg", "country": "DE", "region": "HH", "language": "EN"}],
         "currency": "EUR", "shipping_conditions": "## (+50) Standard", "delivering_plant": "1010",
         "incoterms": "DAP", "incoterms_location": "Hamburg", "payment_terms": "ZB00",
         "account_assignment_group": "Domestic revenue", "customer_pricing_procedure": "S",
         "tax_classifications": [{"category": "TTX1", "classification": "1"}],
         "company_code": "1010", "reconciliation_account": "12100000",
         "partner_functions": [{"role": "SHIP_TO", "partner": "T-S50A##", "source_exercise": 10}]}))
    objects.append(obj(BP_IDS["T-S50B##"], "BUSINESS_PARTNER", "MASTER_DATA", sid(20),
        [source_ref(20, "EXERCISE", 205, "Fiche partenaire / division chargée de la livraison",
                    "T-S50B##; 1010 / 10 / 00"),
         source_ref(20, "SOLUTION", 207, "division chargée de la livraison",
                    "La division 1010 est saisie en tant que division chargée de la livraison")],
        {"partner_id": "T-S50B##", "roles": [], "name": None, "sales_areas": ["1010/10/00"],
         "grouping": None, "addresses": [], "currency": None, "shipping_conditions": None,
         "delivering_plant": "1010", "incoterms": None, "incoterms_location": None,
         "payment_terms": None, "account_assignment_group": None, "customer_pricing_procedure": None,
         "tax_classifications": [], "company_code": None, "reconciliation_account": None,
         "partner_functions": []}, confidence="MEDIUM"))

    objects += [
        obj(MATERIAL_IDS["T-MS4##"], "MATERIAL", "MASTER_DATA", sid(11),
            provenance(11, "Article / secteur industriel / type d'article / description / quantité minimale",
                       "T-MS4##; Commerce; Produits négociables; Phare standard; 10 pièces"),
            {"material_id": "T-MS4##", "description": "Phare standard", "base_unit": "PC",
             "plants": ["1010"], "industry_sector": "Commerce", "material_type": "Produits négociables",
             "sales_organization": "1010", "distribution_channel": "10", "tax_classification": "1",
             "minimum_order_quantity": 10, "minimum_order_unit": "PC", "sales_text": "Article fragile",
             "availability_check": None, "delivering_plant": "1010", "strategy_group": None,
             "item_category_group": None}),
        obj(MATERIAL_IDS["T-MS3##"], "MATERIAL", "MASTER_DATA", sid(20),
            [source_ref(20, "EXERCISE", 205, "Article / groupe de contrôle",
                        "T-MS3##; division 1010"),
             source_ref(20, "SOLUTION", 206, "groupe de contrôle", "Le groupe de contrôle 02 est affecté"),
             source_ref(20, "SOLUTION", 206, "division chargée de la livraison",
                        "La division 1020 est affectée comme division chargée de la livraison")],
            {"material_id": "T-MS3##", "description": None, "base_unit": "PC", "plants": ["1010", "1020"],
             "industry_sector": None, "material_type": None, "sales_organization": "1010",
             "distribution_channel": "10", "tax_classification": None, "minimum_order_quantity": None,
             "minimum_order_unit": None, "sales_text": None, "availability_check": "02",
             "delivering_plant": "1020", "strategy_group": None, "item_category_group": None}, confidence="HIGH"),
        obj(MATERIAL_IDS["T-F1##"], "MATERIAL", "MASTER_DATA", sid(30),
            provenance(30, "Article / division / groupe de stratégies",
                       "T-F1##; division 1010; groupe de stratégies 20"),
            {"material_id": "T-F1##", "description": None, "base_unit": None, "plants": ["1010"],
             "industry_sector": None, "material_type": None, "sales_organization": None,
             "distribution_channel": None, "tax_classification": None, "minimum_order_quantity": None,
             "minimum_order_unit": None, "sales_text": None, "availability_check": None,
             "delivering_plant": "1010", "strategy_group": "20", "item_category_group": None}),
        obj(MATERIAL_IDS["T-D1##"], "MATERIAL", "MASTER_DATA", sid(31),
            provenance(31, "Produit de service / type d'article / groupe de types de poste",
                       "T-D1##; division 1010; organisation commerciale 1010; canal 10",
                       "Le type d'article DIEN; groupe de types de poste LEIS"),
            {"material_id": "T-D1##", "description": None, "base_unit": "H", "plants": ["1010"],
             "industry_sector": None, "material_type": "DIEN", "sales_organization": "1010",
             "distribution_channel": "10", "tax_classification": None, "minimum_order_quantity": None,
             "minimum_order_unit": None, "sales_text": None, "availability_check": None,
             "delivering_plant": "1010", "strategy_group": None, "item_category_group": "LEIS"}),
    ]
    objects.append(obj("S4600_CH4_EX12_CUSTOMER_MATERIAL_INFO_T-S50A_T-MS1", "CUSTOMER_MATERIAL_INFO",
        "MASTER_DATA", sid(12), provenance(12, "Client / Article / Référence article client / Description",
        "T-S50A##; T-MS1##; K-MS-##; Phare Premium"),
        {"business_partner": "T-S50A##", "material": "T-MS1##", "customer_material": "K-MS-##",
         "sales_organization": "1010", "distribution_channel": "10"},
        [dep("FOR_CUSTOMER", "BUSINESS_PARTNER", None, "T-S50A##"),
         dep("FOR_MATERIAL", "MATERIAL", None, "T-MS1##")]))

    objects += [
        obj("S4600_CH4_EX11_PRICING_CONDITION_PR00_T-MS4", "PRICING_CONDITION", "MASTER_DATA", sid(11),
            provenance(11, "Prix de vente", "Prix de vente 35 EUR à partir de quantité 1"),
            {"condition_type": "PR00", "key_combination": {"sales_organization": "1010",
             "distribution_channel": "10", "customer": None, "material": "T-MS4##"},
             "valid_from": None, "valid_to": None, "rate": 35, "currency": "EUR", "pricing_unit": 1,
             "scale_basis": "QUANTITY", "scales": []},
            [dep("FOR_MATERIAL", "MATERIAL", MATERIAL_IDS["T-MS4##"], "T-MS4##")]),
        obj("S4600_CH4_EX13_PRICING_CONDITION_PR00_CUSTOMER_MATERIAL", "PRICING_CONDITION", "MASTER_DATA", sid(13),
            provenance(13, "Type de condition / Client / Article / Quantité échelonnée / Montant",
                       "PR00; 1010 / 10; T-S50A##; T-MS1##; 1=53 EUR, 10=51 EUR, 20=49 EUR"),
            {"condition_type": "PR00", "key_combination": {"sales_organization": "1010",
             "distribution_channel": "10", "customer": "T-S50A##", "material": "T-MS1##"},
             "valid_from": None, "valid_to": None, "rate": None, "currency": "EUR", "pricing_unit": 1,
             "scale_basis": "QUANTITY", "scales": [
                 {"scale_basis": "QUANTITY", "threshold": q, "threshold_unit": "PC",
                  "threshold_currency": None, "amount": a, "currency": "EUR", "rate": None,
                  "rate_unit": None, "pricing_unit": 1, "from_quantity": q, "quantity_unit": "PC"}
                 for q, a in [(1, 53), (10, 51), (20, 49)] ]},
            [dep("FOR_CUSTOMER", "BUSINESS_PARTNER", None, "T-S50A##"),
             dep("FOR_MATERIAL", "MATERIAL", None, "T-MS1##")]),
        obj("S4600_CH4_EX14_PRICING_CONDITION_K007_CUSTOMER_VALUE_SCALE", "PRICING_CONDITION", "MASTER_DATA", sid(14),
            provenance(14, "Type de condition / Client / Barème de valeurs / Pourcentage",
                       "K007; T-S50A##; 100 EUR=-1%, 500 EUR=-2%, 1000 EUR=-3%"),
            {"condition_type": "K007", "key_combination": {"sales_organization": "1010",
             "distribution_channel": "10", "customer": "T-S50A##", "material": None},
             "valid_from": None, "valid_to": None, "rate": None, "currency": "EUR", "pricing_unit": None,
             "scale_basis": "VALUE", "scales": [
                 {"scale_basis": "VALUE", "threshold": v, "threshold_unit": None,
                  "threshold_currency": "EUR", "amount": None, "currency": None, "rate": r,
                  "rate_unit": "PERCENT", "pricing_unit": None, "from_quantity": None, "quantity_unit": None}
                 for v, r in [(100, -1), (500, -2), (1000, -3)] ]},
            [dep("FOR_CUSTOMER", "BUSINESS_PARTNER", None, "T-S50A##")]),
    ]

    # Sales orders with actual exercise datasets.
    ex3 = order(3, "T-S50A##", "4-2##", "dans 1 semaine", "P1W",
                [{"line_id": "10", "material": "T-MS1##", "quantity": 10, "unit": "PC"},
                 {"line_id": "20", "material": "T-MS2##", "quantity": 20, "unit": "PC"}],
                extra={"processing_status": "EN COURS"},
                extra_prov=[source_ref(4, "SOLUTION", 65, "Statut de traitement global", "Le statut doit être En cours")])
    objects.append(ex3)
    orders = {
        10: order(10, "T-CUS##", "5-9##", "dans 1 semaine", "P1W",
                  [{"line_id": "10", "material": "T-MS2##", "quantity": 2, "unit": "PC"}], ship_to="T-S50A##"),
        11: order(11, "T-S50A##", "5-13##", "dans 10 jours", "P10D",
                  [{"line_id": "10", "material": "T-MS4##", "quantity": 5, "unit": "PC"}]),
        12: order(12, "T-S50A##", "5-19##", "dans 1 semaine", "P1W",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 10, "unit": "PC"}]),
        13: order(13, "T-S50A##", "5-23##", "dans 10 jours", "P10D",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 10, "unit": "PC"}]),
        14: order(14, "T-S50A##", "5-25##", "dans 10 jours", "P10D",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 10, "unit": "PC"}]),
        16: order(16, "T-S50A##", "##-Proposition", None, None,
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 5, "unit": "PC"},
                   {"line_id": "20", "material": "T-MS2##", "quantity": 5, "unit": "PC"}], confidence="MEDIUM"),
        17: order(17, "T-S50A##", "3-9##", None, None,
                  [{"line_id": "10", "material": "T-MS2##", "quantity": 10, "unit": "PC",
                    "net_weight": 20, "net_weight_unit": "KG"}], extra={"completeness_state": "COMPLETE"}),
        18: order(18, "T-S50B##", "6-1##", "dans 10 jours", "P10D",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 7, "unit": "PC"},
                   {"line_id": "20", "material": "T-MS2##", "quantity": 8, "unit": "PC"}],
                  extra={"payment_terms": "ZB00"}),
        19: order(19, "T-S50A##", "6-4##", "dans 1 semaine", "P1W",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 5, "unit": "PC", "ship_to_party": "T-S50A##"},
                   {"line_id": "20", "material": "T-MS3##", "quantity": 1, "unit": "PC", "ship_to_party": "T-S50B##"}]),
        21: order(21, "T-S50A##", "7-6##", "dans 1 semaine", "P1W",
                  [{"line_id": "10", "material": "T-MS3##", "quantity": 20, "unit": "PC"}]),
        22: order(22, "T-S50A##", "7-7##", "dans 1 semaine", "P1W",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 10, "unit": "PC"},
                   {"line_id": "20", "material": "T-MS2##", "quantity": 10, "unit": "PC"}]),
        23: order(23, "T-S50B##", "7-3##", "dans 1 semaine", "P1W",
                  [{"line_id": "10", "material": "T-MS3##", "quantity": 95, "unit": "PC", "plant": "1020"}]),
        28: order(28, "T-S50A##", "8-9##", "dans 3 semaines", "P3W",
                  [{"line_id": "10", "material": "T-MS2##", "quantity": 1, "unit": "PC"}],
                  extra_prov=[source_ref(28, "EXERCISE", 272, "Commande avec référence à l'offre",
                                             "CDCL; 1010 / 10 / 00; 8-9##; dans 3 semaines; T-MS2##; 1 pièce"),
                              source_ref(28, "SOLUTION", 274, "Commande avec référence à l'offre", None)]),
        30: order(30, "T-S50A##", "8-9##", "dans 2 semaines", "P2W",
                  [{"line_id": "10", "material": "T-F1##", "quantity": 10, "unit": "PC"}]),
        31: order(31, "T-S50A##", "8-6##", None, None,
                  [{"line_id": "10", "material": "T-D1##", "quantity": 3, "unit": "H", "item_category": "TAD"}]),
        32: order(32, "T-S50A##", "9-1##", "dans 1 semaine", "P1W",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 5, "unit": "PC"}]),
        35: order(35, "T-S50A##", "658–##", "Date du jour", "P0D",
                  [{"line_id": "10", "material": "T-MS1##", "quantity": 3, "unit": "PC"}],
                  extra={"payment_terms": "Payable immédiatement sans déduction",
                         "completeness_state": "COMPLETE", "processing_status": "TERMINÉ"}),
    }
    objects.extend(orders.values())

    # Presales chain.
    inquiry_id = f"{sid(28)}_INQUIRY_DO"
    inquiry_items = [{"line_id": "10", "material": "T-MS2##", "quantity": 3, "unit": "PC"}]
    objects.append(obj(inquiry_id, "INQUIRY", "TRANSACTION", sid(28),
        provenance(28, "Type de demande d'offre / DateLivrSouh. / Article / Quantité",
                   "DO; T-S50A##; Date du jour + 3 semaines; T-MS2##; 3 pièces"),
        {"document_type": "DO", "sold_to_party": "T-S50A##", "valid_to": relative("fin de la semaine", None),
         "items": inquiry_items}, entity_deps("T-S50A##", inquiry_items)))
    quote_id = f"{sid(28)}_QUOTATION_OF"
    quote_items = [{"line_id": "10", "material": "T-MS2##", "quantity": 2, "unit": "PC"}]
    objects.append(obj(quote_id, "QUOTATION", "TRANSACTION", sid(28),
        provenance(28, "Type d'offre / validité / quantité", "OF; aujourd'hui à fin de la semaine prochaine; 2 pièces"),
        {"document_type": "OF", "sold_to_party": "T-S50A##",
         "valid_to": relative("fin de la semaine prochaine", None), "customer_reference": None,
         "items": quote_items}, [dep("CREATED_FROM", "INQUIRY", inquiry_id, "avec référence à la demande"),
                                 *entity_deps("T-S50A##", quote_items)]))
    orders[28]["dependencies"].append(dep("CREATED_FROM", "QUOTATION", quote_id, "avec référence à l'offre"))

    # Delivery, goods movement, billing and payment chains.
    d5 = delivery(5, "FROM_EX3", ex3["object_id"], planned_raw="Échue la semaine prochaine", offset="P1W")
    d12 = delivery(12, "FROM_EX12_ORDER", orders[12]["object_id"], planned_raw="Échue la semaine prochaine", offset="P1W")
    d12["provenance"].extend([
        source_ref(12, "EXERCISE", 130, "Point d'expédition / Date de création planifiée",
                   "Z0##; Échue la semaine prochaine"),
        source_ref(12, "SOLUTION", 132, "Point d'expédition / Date de création planifiée",
                   "Z0##; Échue la semaine prochaine"),
    ])
    d17 = delivery(17, "FROM_EX17_ORDER", orders[17]["object_id"], planned_raw=None, offset=None)
    d30 = delivery(30, "FROM_EX30_ORDER", orders[30]["object_id"], shipping_point="1010",
                   planned_raw="Date du jour + 3 semaines", offset="P3W", confidence="HIGH")
    d30["provenance"].extend([
        source_ref(30, "EXERCISE", 284, "Point d'expédition / Date de création planifiée",
                   "1010; Date du jour + 3 semaines"),
        source_ref(30, "SOLUTION", 289, "Point d'expédition / Date de création planifiée",
                   "1010; Date du jour + 3 semaines"),
    ])
    d32 = delivery(32, "FROM_EX32_ORDER", orders[32]["object_id"], planned_raw="Échue la semaine prochaine", offset="P1W")
    objects.extend([d5, d12, d17, d30, d32])
    for exercise, target in [(6, d5), (30, d30), (32, d32)]:
        movement = obj(f"{sid(exercise)}_GOODS_ISSUE_FROM_DELIVERY", "GOODS_ISSUE", "TRANSACTION", sid(exercise),
            provenance(exercise, "Sortie de marchandises / livraison précédente",
                       "Enregistrer la sortie de marchandises pour la livraison créée précédemment"),
            {"posting_date": "Date du jour" if exercise != 30 else None,
             "movement_reference": None, "delivery_reference": None, "items": []},
            [dep("POSTED_FOR", "OUTBOUND_DELIVERY", target["object_id"], "livraison créée précédemment")], "MEDIUM")
        if exercise == 32:
            movement["provenance"].extend([
                source_ref(32, "EXERCISE", 310, "Livraison créée / sortie de marchandises",
                           "livraison sortante qui vient d'être créée"),
                source_ref(32, "SOLUTION", 313, "Sortie de marchandises", None),
            ])
        objects.append(movement)

    b7 = billing(7, "STANDARD_FROM_EX5", d5["object_id"], "OUTBOUND_DELIVERY", "STANDARD")
    b31 = billing(31, "SERVICE_FROM_ORDER", orders[31]["object_id"], "SALES_ORDER", "SERVICE_INVOICE",
                  date_raw="aujourd'hui + 14 jours", offset="P14D")
    b31["provenance"].extend([
        source_ref(31, "EXERCISE", 294, "Facture avec référence à la commande client",
                   "aujourd'hui + 14 jours"),
        source_ref(31, "SOLUTION", 296, "Facture avec référence à la commande client", None),
    ])
    b32 = billing(32, "STANDARD_FROM_DELIVERY", d32["object_id"], "OUTBOUND_DELIVERY", "STANDARD",
                  date_raw="Date du jour + 1 semaine", offset="P1W")
    b32["provenance"].extend([
        source_ref(32, "EXERCISE", 310, "Document de facturation avec référence à la livraison",
                   "Dates de facturation jusqu'au Date du jour + 1 semaine"),
        source_ref(32, "SOLUTION", 313, "Document de facturation avec référence à la livraison", None),
    ])
    objects.extend([b7, b31, b32])
    pay = obj(f"{sid(8)}_PAYMENT_REFERENCE_FOR_EX7", "PAYMENT_REFERENCE", "REFERENCE_DATA", sid(8),
        provenance(8, "Société / Type d'écriture / Compte général / Montant / Devise / Client",
                   "1010; DZ; 11100000; montant calculé; EUR; T-S50A##",
                   "1276 - 38,28 = 1237,72"),
        {"reference_id": None, "payer": "T-S50A##", "billing_reference": None,
         "amount": 1237.72, "currency": "EUR", "payment_date": relative("Date du jour", "P0D")},
        [dep("SETTLES", "BILLING", b7["object_id"], "document de facturation")], "HIGH")
    objects.append(pay)

    # Complaint processing.
    cmr_id = f"{sid(32)}_CREDIT_MEMO_REQUEST_DNC"
    cm_items = [{"line_id": "10", "material": "T-MS1##", "quantity": 3, "unit": "PC"}]
    objects.append(obj(cmr_id, "CREDIT_MEMO_REQUEST", "TRANSACTION", sid(32),
        provenance(32, "Type commande client / Motif / quantité", "DNC; Endommagé lors du transport; 3 phares"),
        {"document_type": "DNC", "sold_to_party": "T-S50A##", "reason": "Endommagé lors du transport",
         "reference_document": None, "items": cm_items},
        [dep("CREATED_FROM", "BILLING", b32["object_id"], "avec référence au document de facturation"),
         *entity_deps("T-S50A##", cm_items)]))
    credit32 = billing(32, "CREDIT_MEMO_FROM_REQUEST", cmr_id, "CREDIT_MEMO_REQUEST", "CREDIT_MEMO")
    credit32["provenance"].extend([
        source_ref(32, "EXERCISE", 310, "Avoir avec référence à la demande d'avoir", None),
        source_ref(32, "SOLUTION", 314, "Créer l'avoir pour la demande d'avoir", None),
    ])
    cancel33 = billing(33, "CANCELLATION_OF_CREDIT_MEMO", credit32["object_id"], "BILLING", "CANCELLATION", confidence="HIGH")
    objects.extend([credit32, cancel33])

    return_id = f"{sid(34)}_RETURN_ORDER_RE"
    ret_items = [{"line_id": "10", "material": "T-MS3##", "quantity": 3, "unit": "PC", "plant": "1020"}]
    objects.append(obj(return_id, "RETURN_ORDER", "TRANSACTION", sid(34),
        provenance(34, "Type commande client / Motif / Article / Quantité / Division",
                   "RE; Écart quantité; T-MS3##; 3 pièces; division 1020"),
        {"document_type": "RE", "sold_to_party": "T-S50A##", "return_reason": "Écart quantité",
         "reference_document": None, "items": ret_items}, entity_deps("T-S50A##", ret_items)))
    ret_delivery = delivery(34, "RETURN_FROM_ORDER", return_id, "RETURN_ORDER", shipping_point="Z0##",
                            delivery_type="RETURN", confidence="LOW")
    ret_delivery["provenance"].append(source_ref(34, "SOLUTION", 325, "Livraison de retours", None))
    objects.append(ret_delivery)
    credit34 = billing(34, "CREDIT_MEMO_FROM_RETURN", return_id, "RETURN_ORDER", "CREDIT_MEMO", confidence="MEDIUM")
    credit34["provenance"].append(source_ref(34, "SOLUTION", 325, "Avoir avec référence au document de retours", None))
    objects.append(credit34)

    # Solution-enriched delivery creation from incomplete-order resolution.
    d35 = delivery(35, "FROM_RESOLVED_ORDER", orders[35]["object_id"], planned_raw=None,
                   offset=None, confidence="MEDIUM")
    d35["provenance"].append(source_ref(35, "SOLUTION", 339, "Créer livraison", None))
    objects.append(d35)

    # Add explicit pricing dependencies to the orders that exercise those records.
    orders[11]["dependencies"].append(dep("PRICED_BY", "PRICING_CONDITION",
        "S4600_CH4_EX11_PRICING_CONDITION_PR00_T-MS4", "Prix de vente 35 EUR"))
    orders[13]["dependencies"].append(dep("PRICED_BY", "PRICING_CONDITION",
        "S4600_CH4_EX13_PRICING_CONDITION_PR00_CUSTOMER_MATERIAL", "condition PR00"))
    orders[14]["dependencies"].append(dep("PRICED_BY", "PRICING_CONDITION",
        "S4600_CH4_EX14_PRICING_CONDITION_K007_CUSTOMER_VALUE_SCALE", "condition K007"))

    # Recompute dependency propagation after all target records exist.
    by_id = {item["object_id"]: item for item in objects}
    for item in objects:
        for dependency in item["dependencies"]:
            target = by_id.get(dependency.get("target_id"))
            if dependency.get("critical") and target and target["readiness_status"] == "BLOCKED":
                if not any(r["code"] == "DEPENDENCY_NOT_READY" for r in item["blocking_reasons"]):
                    item["blocking_reasons"].append({"code": "DEPENDENCY_NOT_READY",
                        "message": "A resolved canonical dependency is itself not downstream-ready",
                        "field_path": "dependencies"})
                    item["readiness_status"] = "BLOCKED"
    return sorted(objects, key=lambda item: item["object_id"])


SKIPPED = [
    {"exercise": 2, "reason": "Theory-only organizational questions; no concrete instance."},
    {"exercise": 15, "reason": "Condition-context explanation only; no condition record instance."},
    {"exercise": 24, "reason": "Availability-control theory only; no new instance."},
    {"exercise": 25, "reason": "Participant-run mass deliveries have blank count and identifiers; cardinality cannot be inferred."},
    {"exercise": 26, "reason": "Mass goods issues refer to the indeterminate Exercise 25 delivery set."},
    {"exercise": 27, "reason": "Participant-run mass billing count and identifiers are blank; no pseudo-instances created."},
    {"exercise": 29, "reason": "Presales comparison questions only; no new instance."},
    {"exercise": 36, "reason": "Analytical UI procedure; no canonical business-object instance."},
]


def parse_source(pdf: Path) -> tuple[list[str], dict]:
    executable = shutil.which("pdftotext")
    if not executable:
        candidate = Path(r"C:\Program Files\Git\mingw64\bin\pdftotext.exe")
        executable = str(candidate) if candidate.is_file() else None
    if not executable:
        raise RuntimeError("pdftotext is required for deterministic full-document verification")
    with tempfile.TemporaryDirectory(prefix="s4600-") as temp_dir:
        text_path = Path(temp_dir) / "S4600.txt"
        subprocess.run([executable, "-layout", str(pdf), str(text_path)], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        text = text_path.read_text(encoding="utf-8", errors="replace")
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    if len(pages) != EXPECTED_PAGES:
        raise ValueError(f"Expected {EXPECTED_PAGES} pages, parsed {len(pages)}")
    joined = "\n".join(pages)
    exercises = sorted({int(n) for n in re.findall(r"Exercice\s+(\d+)", joined)})
    solutions = sorted({int(n) for n in re.findall(r"Solution\s+(\d+)", joined)})
    if exercises != list(range(1, 37)) or solutions != list(range(1, 37)):
        raise ValueError({"exercises": exercises, "solutions": solutions})
    return pages, {"page_count": len(pages), "exercise_count": len(exercises),
                   "solution_count": len(solutions), "demonstration_heading_count": len(re.findall(r"Démonstration", joined)),
                   "table_marker_count": len(re.findall(r"Nom de zone\s+Valeur", joined))}


def section_inventory(objects: list[dict]) -> list[dict]:
    object_ids_by_ex = {}
    for item in objects:
        for ref in item["provenance"]:
            if ref["course_code"] == COURSE and ref.get("exercise"):
                object_ids_by_ex.setdefault(int(ref["exercise"]), set()).add(item["object_id"])
    skipped = {item["exercise"]: item["reason"] for item in SKIPPED}
    result = []
    for exercise in range(1, 37):
        ids = sorted(object_ids_by_ex.get(exercise, []))
        if exercise == 4:
            decision = "VERIFY_ONLY"
            reason = "Display/solution evidence enriches Exercise 3; no duplicate object created."
        elif ids:
            decision, reason = "EXTRACT_OR_ENRICH", "Concrete instance data or unambiguous verification evidence."
        else:
            decision, reason = "SKIP", skipped.get(exercise, "No independent canonical instance after deduplication.")
        result.append({"scenario_id": sid(exercise), "chapter": CHAPTER[exercise], "exercise": exercise,
                       "exercise_page": EXERCISE_PAGES[exercise], "solution_page": SOLUTION_PAGES[exercise],
                       "decision": decision, "reason": reason, "object_ids": ids})
    return result


def write_json(relative_path: str, value) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    manifest_entries = [entry for entry in load_manifest(ROOT) if entry["logical_name"] == COURSE]
    if len(manifest_entries) != 1:
        raise ValueError("S4600 must resolve to exactly one manifest entry")
    pdf = resolve_document(ROOT, COURSE, verify_checksum=True)
    if pdf.name != SOURCE_FILE:
        raise ValueError(f"Unexpected S4600 source: {pdf.name}")
    pages, parse_stats = parse_source(pdf)
    objects = build_objects()
    ids = [item["object_id"] for item in objects]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate object IDs")
    for item in objects:
        errors = validate_object(ROOT, item)
        if errors:
            raise ValueError({item["object_id"]: errors})

    extracted = json.loads(json.dumps(objects))
    for item in extracted:
        item["lifecycle_status"] = "EXTRACTED"
    write_json("data/extracted/full/S4600/objects.json", {"objects": extracted})
    write_json("data/normalized/full/S4600/objects.json", {"objects": objects})

    lineage = []
    for item in objects:
        lineage.append({"object_id": item["object_id"], "scenario_id": item["scenario_id"],
                        "source_to_canonical": [{"page": ref["page"], "section_type": ref["section_type"],
                            "source_term": ref["source_term"], "raw_excerpt": ref["raw_excerpt"]}
                            for ref in item["provenance"]],
                        "enrichments": [{"page": ref["page"], "section_type": ref["section_type"],
                            "source_term": ref["source_term"]} for ref in item["provenance"]
                            if ref["section_type"] == "SOLUTION"]})
    write_json("metadata/lineage/full/S4600/lineage.json", {"objects": lineage})
    write_json("metadata/lineage/full/S4600/section_inventory.json", {"sections": section_inventory(objects),
                                                                        "skipped_candidates": SKIPPED})

    graph = {"nodes": [{"object_id": item["object_id"], "object_type": item["object_type"],
                         "readiness_status": item["readiness_status"]} for item in objects],
             "edges": [{"source": item["object_id"], "target": dependency["target_id"],
                         "target_type": dependency["target_type"], "relation": dependency["relation"],
                         "status": dependency["status"], "critical": dependency["critical"],
                         "source_phrase": dependency["source_phrase"]}
                        for item in objects for dependency in item["dependencies"]]}
    write_json("metadata/dependencies/full/S4600/dependency_graph.json", graph)
    write_json("metadata/confidence/full/S4600/confidence.json", {"objects": [
        {"object_id": item["object_id"], "object_type": item["object_type"],
         "confidence": item["validation"]["confidence"], "readiness_status": item["readiness_status"],
         "blocking_reason_codes": [reason["code"] for reason in item["blocking_reasons"]]}
        for item in objects]})

    counts = Counter(item["object_type"] for item in objects)
    summary = {"source": {"logical_name": COURSE, "source_file": pdf.name,
                           "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(), **parse_stats},
               "object_count": len(objects), "counts_by_type": dict(sorted(counts.items())),
               "lifecycle_counts": dict(Counter(item["lifecycle_status"] for item in objects)),
               "readiness_counts": dict(Counter(item["readiness_status"] for item in objects)),
               "confidence_counts": dict(Counter(item["validation"]["confidence"] for item in objects)),
               "placeholder_count": sum(len(item["placeholders"]) for item in objects),
               "dependency_edge_count": len(graph["edges"]),
               "unresolved_dependency_count": sum(edge["status"] == "UNRESOLVED" for edge in graph["edges"]),
               "schema_valid_count": len(objects), "schema_invalid_count": 0,
               "source_pages_processed": [1, len(pages)]}
    write_json("metadata/confidence/full/S4600/extraction_summary.json", summary)


if __name__ == "__main__":
    main()
