"""Deterministic, source-verified Phase 1B Stage 3 extraction for S4615 only."""
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

COURSE = "S4615"
SOURCE_FILE = "S4615_FR_Col12_ILT_FV_Inst_A4.pdf"
EXPECTED_PAGES = 263
EXERCISE_PAGES = {1: 13, 2: 29, 3: 41, 4: 61, 5: 73, 6: 97, 7: 119,
                  8: 137, 9: 145, 10: 173, 11: 189, 12: 213, 13: 235}
SOLUTION_PAGES = {1: 16, 2: 30, 3: 43, 4: 63, 5: 75, 6: 100, 7: 123,
                  8: 139, 9: 147, 10: 175, 11: 192, 12: 216, 13: 238}
CHAPTER = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 6, 8: 7, 9: 7,
           10: 8, 11: 8, 12: 9, 13: 10}


def sid(exercise: int) -> str:
    return f"S4615_CH{CHAPTER[exercise]}_EX{exercise}"


def ref(exercise: int, section: str, page: int, term: str, excerpt: str | None = None) -> dict:
    return {"course_code": COURSE, "source_file": SOURCE_FILE, "page": page,
            "chapter": CHAPTER[exercise], "exercise": exercise, "section_type": section,
            "scenario_id": sid(exercise), "raw_excerpt": excerpt, "source_term": term}


def prov(exercise: int, term: str, excerpt: str, *, solution_excerpt: str | None = None,
         exercise_page: int | None = None, solution_page: int | None = None) -> list[dict]:
    return [ref(exercise, "EXERCISE", exercise_page or EXERCISE_PAGES[exercise], term, excerpt),
            ref(exercise, "SOLUTION", solution_page or SOLUTION_PAGES[exercise], term,
                solution_excerpt or excerpt)]


def demo_ref(chapter: int, page: int, scenario: str, term: str, excerpt: str) -> dict:
    return {"course_code": COURSE, "source_file": SOURCE_FILE, "page": page,
            "chapter": chapter, "exercise": None, "section_type": "DEMONSTRATION",
            "scenario_id": scenario, "raw_excerpt": excerpt, "source_term": term}


def relative(raw: str, offset: str | None = None) -> dict:
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
    deps = dependencies or []
    placeholders = scan_placeholders(data)
    reasons = []
    if placeholders:
        reasons.append({"code": "UNRESOLVED_MANDATORY_PLACEHOLDER",
                        "message": "Participant-specific source placeholder remains unresolved",
                        "field_path": "data"})
    if any(d["critical"] and d["status"] == "UNRESOLVED" for d in deps):
        reasons.append({"code": "UNRESOLVED_CRITICAL_DEPENDENCY",
                        "message": "A required source reference has no extractable canonical identifier",
                        "field_path": "dependencies"})
    return {"object_id": object_id, "object_type": object_type,
            "classification": classification, "scenario_id": scenario_id,
            "provenance": provenance, "lifecycle_status": "VALIDATED",
            "readiness_status": "BLOCKED" if reasons else "READY",
            "blocking_reasons": reasons, "dependencies": deps, "placeholders": placeholders,
            "validation": {"schema_valid": True, "issues": [], "confidence": confidence},
            "data": data}


def order(exercise: int, suffix: str, order_type: str, sold_to: str,
          customer_reference: str, material: str, quantity: float,
          *, payment_terms: str | None = None, requested_date: dict | None = None,
          provenance: list[dict] | None = None, scenario: str | None = None) -> dict:
    scenario = scenario or sid(exercise)
    item = {"line_id": "10", "material": material, "quantity": quantity, "unit": "PC",
            "plant": None, "ship_to_party": None, "shipping_point": None, "route": None,
            "net_weight": None, "net_weight_unit": None, "item_category": None}
    return canonical(f"{scenario}_SALES_ORDER_{suffix}", "SALES_ORDER", "TRANSACTION", scenario,
        provenance or prov(exercise, "Type de commande / domaine commercial / donneur d'ordre / référence client / article / quantité",
                           f"{order_type}; 1010/10/00; {sold_to}; {customer_reference}; {material}; {quantity} PC"),
        {"order_type": order_type, "sales_organization": "1010", "distribution_channel": "10",
         "sales_division": "00", "sold_to_party": sold_to, "ship_to_party": None,
         "customer_reference": customer_reference, "requested_delivery_date": requested_date,
         "items": [item], "payment_terms": payment_terms, "processing_status": None,
         "completeness_state": None},
        [dependency("SOLD_TO_PARTY", "BUSINESS_PARTNER", None, sold_to, False),
         dependency("USES_MATERIAL", "MATERIAL", None, material, False)])


def delivery(exercise: int, suffix: str, order_id: str, quantity: float,
             material: str, *, provenance: list[dict] | None = None,
             scenario: str | None = None) -> dict:
    scenario = scenario or sid(exercise)
    return canonical(f"{scenario}_OUTBOUND_DELIVERY_{suffix}", "OUTBOUND_DELIVERY",
        "TRANSACTION", scenario,
        provenance or prov(exercise, "Livraison sortante / point d'expédition / quantité",
                           f"livraison de la commande précédente; 1010; {quantity} PC"),
        {"delivery_type": "OUTBOUND", "ship_to_party": None, "shipping_point": "1010",
         "planned_creation_date": relative("date du jour + 10 jours", "P10D"),
         "planned_goods_issue_date": None, "items": [{"line_id": "10", "material": material,
         "quantity": quantity, "unit": "PC", "reference_item": "10", "plant": None,
         "storage_location": None, "warehouse_number": None, "item_category": None,
         "gross_weight": None, "gross_weight_unit": None}], "storage_location": None,
         "warehouse_number": None, "system_representations": []},
        [dependency("CREATED_FROM", "SALES_ORDER", order_id, "commande client précédente")])


def billing(exercise: int, suffix: str, billing_type: str | None, subtype: str,
            payer: str | None, reference_type: str, reference_id: str | None,
            reference_phrase: str, *, items: list[dict] | None = None,
            billing_date=None, status: str | None = "CREATED",
            accounting_status: str | None = None, posting_blocked: bool | None = None,
            billing_plan=None, down_payments=None, installments=None,
            extra_dependencies=None, provenance=None, scenario: str | None = None,
            confidence: str = "HIGH", payment_terms: str | None = None,
            net_value: float | None = None, currency: str | None = None) -> dict:
    scenario = scenario or sid(exercise)
    deps = [dependency("BILLED_FROM", reference_type, reference_id, reference_phrase)]
    deps.extend(extra_dependencies or [])
    fi_meta = []
    if accounting_status:
        fi_meta.append({"system": "FI", "relationship": "ACCOUNTING_DOCUMENT",
                        "status": accounting_status, "identifier": None})
        if accounting_status not in {"NOT_APPLICABLE_PRO_FORMA", "NO_ACCOUNTING_ENTRY"}:
            fi_meta.append({"system": "CO", "relationship": "CONTROLLING_POSTING",
                            "status": "DEPENDENT_ON_FI_TRANSFER", "identifier": None})
    data = {"billing_type": billing_type, "billing_subtype": subtype, "payer": payer,
            "billing_date": billing_date, "reference_document": None, "items": items or [],
            "billing_plan": billing_plan, "down_payments": down_payments or [],
            "installment_payments": installments or [], "billing_status": status,
            "payment_terms": payment_terms, "net_value": net_value, "currency": currency,
            "accounting_status": accounting_status, "accounting_document_type": None,
            "posting_blocked": posting_blocked, "fi_co_dependencies": fi_meta}
    return canonical(f"{scenario}_BILLING_{suffix}", "BILLING", "TRANSACTION", scenario,
        provenance or prov(exercise, "Type de facture / document de référence",
                           f"{billing_type or 'type non indiqué'}; {reference_phrase}"),
        data, deps, confidence)


COMPANY = "S4615_SHARED_COMPANY_CODE_1010"
FAIR_COPY = "S4615_CH3_EX3_COPY_CONTROL_FAIR_BILLING"
ACCOUNT_DET = "S4615_CH9_EX12_ACCOUNT_DETERMINATION_AFFILIATED_REVENUE"


def build_objects() -> list[dict]:
    objects = []
    objects.append(canonical(COMPANY, "COMPANY_CODE", "REFERENCE_DATA", sid(2),
        prov(2, "Société affectée à l'organisation commerciale 1010", "1010"),
        {"code": "1010", "description": None}))

    fair_prov = prov(3, "Type de facture par défaut pour commande/livraison Foire",
                     "ZA## utilise ZF## pour la facturation liée à la commande ou à la livraison")
    fair_prov += [ref(6, "SOLUTION", 103, "Pilotage copie livraison vers facture",
                      "cible ZF##; source LF; poste TAN; détermination du prix H"),
                  ref(9, "SOLUTION", 148, "Données VBRK/VBRP",
                      "cible ZF##; source LF; poste TAN; routine 3 Facture individuelle"),
                  ref(13, "SOLUTION", 241, "Numéro de référence / numéro d'affectation",
                      "référence B (commande client); affectation E (facture actuelle)")]
    objects.append(canonical(FAIR_COPY, "COPY_CONTROL", "CUSTOMIZING", sid(3), fair_prov,
        {"source_document_type": "LF", "target_document_type": "ZF##",
         "level": "HEADER_AND_ITEM", "requirements": ["billing from delivery",
         "re-determine freight", "one billing document per delivery", "FI reference transfer"],
         "source_item_category": "TAN", "pricing_type": "H",
         "data_transfer_routine": "3", "reference_number_rule": "B",
         "assignment_number_rule": "E", "billing_quantity_rule": None,
         "positive_negative_quantity": None}))

    # Exercise 1: imported, pre-existing invoice; generated identifiers remain unknown.
    objects.append(billing(1, "IMPORTED_A3", None, "STANDARD", "C615-A##",
        "OUTBOUND_DELIVERY", None, "livraison ayant servi de modèle au document de facturation",
        items=[{"line_id": "10", "material": None, "quantity": None, "unit": None,
                "reference_item": None, "net_value": 1400, "currency": "EUR",
                "sales_division": "03", "condition_values": [{"condition_type": "PR00",
                "amount": 1400, "currency": "EUR"}]}], accounting_status="POSTED_TO_FI",
        posting_blocked=False, confidence="MEDIUM",
        provenance=prov(1, "Commande d'achat / facture / modèle document / PR00 / secteur d'activité",
                        "##S4615-A3; facture importée; livraison non notée; PR00 1 400 EUR; secteur 03",
                        solution_excerpt="pièce comptable créée; FI liquidé; PR00 1 400 EUR; secteur 03")))

    # Exercise 3: existing F2 plus a complete fair-order test chain.
    objects.append(billing(3, "F2_FROM_IMPORTED_DELIVERY", "F2", "STANDARD", None,
        "OUTBOUND_DELIVERY", None, "livraison de la commande d'achat ##S4615-A1",
        accounting_status="POSTED_TO_FI", posting_blocked=False, confidence="MEDIUM"))
    ex3_order = order(3, "FAIR", "ZA##", "C615-A##", "S4615-ZF##", "P615-1##", 5)
    objects.append(ex3_order)
    ex3_delivery = delivery(3, "FAIR", ex3_order["object_id"], 5, "P615-1##")
    objects.append(ex3_delivery)
    objects.append(billing(3, "FAIR", "ZF##", "STANDARD", "C615-A##",
        "OUTBOUND_DELIVERY", ex3_delivery["object_id"], "livraison de la commande Foire ##",
        items=[{"line_id": "10", "material": "P615-1##", "quantity": 5, "unit": "PC",
                "reference_item": "10", "net_value": None, "currency": None,
                "sales_division": "00", "condition_values": []}],
        accounting_status="POSTED_TO_FI", posting_blocked=False,
        extra_dependencies=[dependency("CONTROLLED_BY", "COPY_CONTROL", FAIR_COPY,
                                       "type par défaut ZF## pour ZA##")]))

    # Exercise 4: invoice correction and explicit bill-to-sales-document copy control.
    original_ex4 = billing(4, "ORIGINAL_F2", "F2", "STANDARD", "C615-A##",
        "SALES_ORDER", None, "commande portant la référence ##S4615-A4",
        status="PRE_EXISTING", accounting_status="POSTED_TO_FI", posting_blocked=False,
        confidence="MEDIUM")
    objects.append(original_ex4)
    correction_control = canonical(f"{sid(4)}_COPY_CONTROL_F2_TO_RK", "COPY_CONTROL",
        "CUSTOMIZING", sid(4), prov(4, "Pilotage copie facture vers document de vente",
        "source F2; cible RK; poste TAN; propositions débit/crédit et détermination du prix"),
        {"source_document_type": "F2", "target_document_type": "RK", "level": "ITEM",
         "requirements": ["create paired credit and debit items"], "source_item_category": "TAN",
         "pricing_type": None, "data_transfer_routine": None, "reference_number_rule": None,
         "assignment_number_rule": None, "billing_quantity_rule": None,
         "positive_negative_quantity": "opposite signs"})
    objects.append(correction_control)
    objects.append(billing(4, "CREDIT_MEMO", None, "CREDIT_MEMO", "C615-A##",
        "CREDIT_MEMO_REQUEST", None, "demande de correction de facture créée depuis la facture F2",
        items=[{"line_id": "40", "material": None, "quantity": None, "unit": None,
                "reference_item": "10", "net_value": 1000, "currency": "EUR",
                "sales_division": None, "condition_values": [{"condition_type": "PR00",
                "adjustment": -100, "currency": "EUR", "per_unit": True}]}],
        accounting_status="POSTED_TO_FI", posting_blocked=False,
        extra_dependencies=[dependency("CORRECTS", "BILLING", original_ex4["object_id"],
                                       "facture F2 de référence"),
                            dependency("CONTROLLED_BY", "COPY_CONTROL",
                                       correction_control["object_id"], "F2 vers RK")]))

    # Exercise 5: cash sale and pro forma order-related billing.
    cash_order = order(5, "CASH_SALE", "BV", "C615-D##", "##S4615-BV", "P615-4##", 1)
    objects.append(cash_order)
    cash_delivery = delivery(5, "CASH_SALE", cash_order["object_id"], 1, "P615-4##")
    objects.append(cash_delivery)
    objects.append(billing(5, "CASH_SALE", "BV", "CASH_SALE", "C615-D##",
        "SALES_ORDER", cash_order["object_id"], "vente au comptant BV",
        items=[{"line_id": "10", "material": "P615-4##", "quantity": 1, "unit": "PC",
                "reference_item": "10", "net_value": None, "currency": None,
                "sales_division": "00", "condition_values": []}],
        accounting_status="POSTED_TO_CASH_REVENUE_TAX", posting_blocked=False,
        extra_dependencies=[dependency("DELIVERED_VIA", "OUTBOUND_DELIVERY",
                                       cash_delivery["object_id"], "livraison créée avec la commande")]))
    pf_order = order(5, "PRO_FORMA", "CDLC", "C615-A##", "##S4615-PF", "P615-2##", 5)
    objects.append(pf_order)
    objects.append(billing(5, "PRO_FORMA", "F5", "PRO_FORMA_INVOICE", "C615-A##",
        "SALES_ORDER", pf_order["object_id"], "commande avant livraison",
        items=[{"line_id": "10", "material": "P615-2##", "quantity": 5, "unit": "PC",
                "reference_item": "10", "net_value": None, "currency": None,
                "sales_division": "00", "condition_values": []}],
        accounting_status="NOT_APPLICABLE_PRO_FORMA", posting_blocked=False))

    # Exercise 6: explicit F1 override and fair-order freight re-determination.
    objects.append(billing(6, "F1_OVERRIDE", "F1", "STANDARD", None,
        "OUTBOUND_DELIVERY", None, "livraison de la commande d'achat ##S4615-A5",
        items=[{"line_id": "10", "material": "P615-1##", "quantity": None, "unit": None,
                "reference_item": None, "net_value": 1700, "currency": "EUR",
                "sales_division": None, "condition_values": [{"condition_type": "PR00",
                "amount": 1700, "currency": "EUR"}]}], accounting_status="POSTED_TO_FI",
        posting_blocked=False, confidence="MEDIUM"))
    ex6_order = order(6, "FAIR_FREIGHT", "ZA##", "C615-D##", "##fret", "P615-1##", 1)
    objects.append(ex6_order)
    ex6_delivery = delivery(6, "FAIR_FREIGHT", ex6_order["object_id"], 1, "P615-1##")
    objects.append(ex6_delivery)
    objects.append(billing(6, "FAIR_FREIGHT", "ZF##", "STANDARD", "C615-D##",
        "OUTBOUND_DELIVERY", ex6_delivery["object_id"], "livraison Foire avec frais de transport",
        items=[{"line_id": "10", "material": "P615-1##", "quantity": 1, "unit": "PC",
                "reference_item": "10", "net_value": 1900, "currency": "EUR",
                "sales_division": "00", "condition_values": [{"condition_type": "KF00",
                "rate": 10, "currency": "EUR", "per": 1, "unit": "KG"}]}],
        accounting_status="POSTED_TO_FI", posting_blocked=False, net_value=1900, currency="EUR",
        extra_dependencies=[dependency("CONTROLLED_BY", "COPY_CONTROL", FAIR_COPY,
                                       "ZF## / LF / TAN / type de prix H")]))

    # Exercise 7: monthly delivery billing and the two Fiori invoice states.
    month_order = order(7, "MONTH_END", "CDLC", "C615-B##", "##-mois", "P615-2##", 2)
    objects.append(month_order)
    month_delivery = delivery(7, "MONTH_END", month_order["object_id"], 2, "P615-2##")
    objects.append(month_delivery)
    objects.append(billing(7, "MONTH_END", None, "STANDARD", "C615-B##",
        "OUTBOUND_DELIVERY", month_delivery["object_id"], "livraison facturée à la fin du mois",
        billing_date=relative("fin du mois", "MONTH_END"), accounting_status="POSTED_TO_FI",
        posting_blocked=False, confidence="MEDIUM"))
    app_prov = prov(7, "Commande CDLC / référence / date / article / quantité",
                    "CDLC; ##-app-1; dans une semaine; P-Service; quantité initiale 10 puis 8",
                    exercise_page=121, solution_page=127)
    app_order = order(7, "FIORI_APP_FINAL", "CDLC", "C615-A##", "##-app-1", "P-Service", 8,
                      requested_date=relative("dans une semaine", "P1W"), provenance=app_prov)
    objects.append(app_order)
    first_app = billing(7, "FIORI_APP_CANCELLED", None, "STANDARD", "C615-A##",
        "SALES_ORDER", app_order["object_id"], "commande ##-app-1 avant réduction de quantité",
        items=[{"line_id": "10", "material": "P-Service", "quantity": 10, "unit": None,
                "reference_item": "10", "net_value": None, "currency": None,
                "sales_division": "00", "condition_values": []}], status="CANCELLED",
        accounting_status="NO_ACCOUNTING_ENTRY", posting_blocked=False,
        provenance=prov(7, "Facture Fiori / statut / écriture comptable",
                        "facture sauvegardée, À enregistrer, aucune écriture, puis annulée",
                        exercise_page=121, solution_page=128))
    objects.append(first_app)
    objects.append(billing(7, "FIORI_APP_POSTED", None, "STANDARD", "C615-A##",
        "SALES_ORDER", app_order["object_id"], "commande ##-app-1 modifiée à 8",
        items=[{"line_id": "10", "material": "P-Service", "quantity": 8, "unit": None,
                "reference_item": "10", "net_value": None, "currency": None,
                "sales_division": "00", "condition_values": []}], status="POSTED",
        accounting_status="POSTED_TO_FI_UNCLEARED", posting_blocked=False,
        provenance=prov(7, "Nouvelle facture / quantité / écriture comptable",
                        "quantité 8; facture sauvegardée puis enregistrée; écriture Non rapprochée",
                        exercise_page=122, solution_page=129)))

    # Exercise 9 saves two F1 invoices after a split; identifiers and source deliveries are blank.
    for index, phrase in ((1, "première livraison de l'échéancier"),
                          (2, "livraison liée à la commande ##S4615-A10")):
        objects.append(billing(9, f"SPLIT_{index}", "F1", "STANDARD", "C615-C##",
            "OUTBOUND_DELIVERY", None, phrase, billing_date=relative("premier jour du mois", "MONTH_START"),
            accounting_status="POSTED_TO_FI", posting_blocked=False, confidence="LOW"))

    # Instructor demonstration: two invoices and their invoice list are concrete datasets.
    invoice_demo = "S4615_CH7_DEMO_INVOICE_LIST"
    demo_prov = [demo_ref(7, 152, invoice_demo, "Commande d'achat / client / payeur",
                          "00S4615-A11 C615-GB00; 00S4615-A12 C615-GA00; payeur C615-GC00")]
    demo_bill_ids = []
    for suffix, customer, po in (("A11", "C615-GB00", "00S4615-A11"),
                                 ("A12", "C615-GA00", "00S4615-A12")):
        item = billing(0, f"INVOICE_LIST_SOURCE_{suffix}", None, "STANDARD", "C615-GC00",
            "SALES_ORDER", None, f"commande {po} du client {customer}",
            accounting_status="POSTED_TO_FI_DUNNING_BLOCK", posting_blocked=False,
            provenance=demo_prov, scenario=invoice_demo, confidence="MEDIUM")
        objects.append(item); demo_bill_ids.append(item["object_id"])
    objects.append(canonical(f"{invoice_demo}_BILLING_INVOICE_LIST", "BILLING", "TRANSACTION",
        invoice_demo, [demo_ref(7, 153, invoice_demo, "Relevé de factures",
        "liste sauvegardée pour C615-GC00 contenant les deux documents de facturation")],
        {"billing_type": "LR", "billing_subtype": "INVOICE_LIST", "payer": "C615-GC00",
         "billing_date": relative("du premier jour de la semaine à la fin du mois"),
         "reference_document": None, "items": [], "billing_plan": None, "down_payments": [],
         "installment_payments": [], "billing_status": "CREATED", "payment_terms": None,
         "net_value": None, "currency": None, "accounting_status": "FI_REFERENCES_REPLACED_BY_LIST",
         "accounting_document_type": None, "posting_blocked": False,
         "fi_co_dependencies": [{"system": "FI", "relationship": "REFERENCE_NUMBER",
                                  "status": "INVOICE_LIST_REFERENCE", "identifier": None}]},
        [dependency("CONTAINS", "BILLING", item_id, "document de facturation du relevé")
         for item_id in demo_bill_ids], "HIGH"))

    # Exercise 10: one saved first-period invoice with a periodic plan.
    objects.append(billing(10, "PERIODIC_FIRST_PERIOD", None, "PERIODIC", "C615-E##",
        "SALES_CONTRACT_REFERENCE", None, "contrat de maintenance WV ##S6415-PB",
        billing_date=relative("dernier jour du mois", "MONTH_END"), status="CREATED",
        accounting_status="POSTED_TO_FI", posting_blocked=False,
        billing_plan={"plan_type": "02", "plan_semantics": "PERIODIC", "item_category": "WVN",
                      "date_category": "01", "first_period_status": "C_BILLED",
                      "pricing_condition": "PPSV", "calculation_rule": "M_MONTHLY_QUANTITY"}))

    # Exercise 11: down-payment request, FI receipt and first partial invoice.
    dp_order = order(11, "DOWN_PAYMENT", "CDLC", "C615-F##", "##S4615-AZ", "P615-6##", 1)
    objects.append(dp_order)
    dp_request = billing(11, "DOWN_PAYMENT_REQUEST", "FAZ", "DOWN_PAYMENT_REQUEST", "C615-F##",
        "SALES_ORDER", dp_order["object_id"], "commande avec calendrier d'acompte",
        accounting_status="DOWN_PAYMENT_REQUEST_POSTED_TO_FI", posting_blocked=False,
        billing_plan={"plan_semantics": "MILESTONE_PARTIAL", "due_date": "UNRESOLVED_SOURCE_RESULT"},
        down_payments=[{"kind": "REQUEST", "amount": None, "currency": None,
                        "tax_inclusive_amount": 33000, "status": "BILLED"}])
    objects.append(dp_request)
    payment = canonical(f"{sid(11)}_PAYMENT_REFERENCE_DOWN_PAYMENT", "PAYMENT_REFERENCE",
        "REFERENCE_DATA", sid(11), prov(11, "Acompte / compte bancaire / code CGS / montant",
        "client C615-F##; compte 11100025; code A; montant acompte + TVA = 33000"),
        {"reference_id": None, "payer": "C615-F##", "billing_reference": None,
         "amount": 33000, "currency": None, "payment_date": relative("date du jour", "P0D"),
         "bank_account": "11100025", "special_gl_indicator": "A", "payment_status": "POSTED"},
        [dependency("SETTLES", "BILLING", dp_request["object_id"], "demande d'acompte FAZ")])
    objects.append(payment)
    objects.append(billing(11, "FIRST_PARTIAL", None, "PARTIAL_BILLING", "C615-F##",
        "SALES_ORDER", dp_order["object_id"], "première période de décompte",
        accounting_status="POSTED_TO_FI_WITH_DOWN_PAYMENT_CLEARING", posting_blocked=False,
        billing_plan={"plan_semantics": "MILESTONE_PARTIAL", "period": 1,
                      "billing_block_removed": True},
        down_payments=[{"condition_type": "AZWR", "amount": 33000, "currency": None,
                        "status": "TO_BE_CLEARED"}],
        extra_dependencies=[dependency("CLEARS", "PAYMENT_REFERENCE", payment["object_id"],
                                       "acompte versé par le client")]))

    # Chapter 8 demonstration: installment invoice (one billing document, multiple FI entries).
    installment_demo = "S4615_CH8_DEMO_INSTALLMENT_PAYMENTS"
    inst_prov = [demo_ref(8, 200, installment_demo, "Conditions de paiement / commande / article",
                         "OR; 1010/10/00; C615-A00; 4712; R001; P615-100; 10 PC")]
    inst_order = order(0, "INSTALLMENT", "OR", "C615-A00", "4712", "P615-100", 10,
                       payment_terms="R001", provenance=inst_prov, scenario=installment_demo)
    objects.append(inst_order)
    inst_delivery = delivery(0, "INSTALLMENT", inst_order["object_id"], 10, "P615-100",
                             provenance=inst_prov, scenario=installment_demo)
    objects.append(inst_delivery)
    objects.append(billing(0, "INSTALLMENT", "F2", "INSTALLMENT_INVOICE", "C615-A00",
        "OUTBOUND_DELIVERY", inst_delivery["object_id"], "livraison de la commande 4712",
        payment_terms="R001", accounting_status="POSTED_TO_MULTIPLE_FI_RECEIVABLE_ITEMS",
        posting_blocked=False, installments=[{"terms": "R001", "installment_count": None,
        "percentages": [], "semantic": "one billing document; multiple FI customer entries"}],
        provenance=inst_prov, scenario=installment_demo))

    # Exercise 12: explicit account determination record and its validation chain.
    objects.append(canonical(ACCOUNT_DET, "ACCOUNT_DETERMINATION", "CUSTOMIZING", sid(12),
        prov(12, "Table 001 / application / type de condition / plan comptable / organisation commerciale / groupes d'imputation / clé / compte",
        "001; V; KOFI; YCOA; 1010; 80+##; 01; ERL; 49000000"),
        {"chart_of_accounts": "YCOA", "account_key": "ERL", "general_ledger_account": "49000000",
         "application": "V", "condition_type": "KOFI", "account_determination_procedure": "KOFI00",
         "access_sequence": "KOFI", "condition_table": "001", "sales_organization": "1010",
         "customer_account_assignment_group": "80+##", "material_account_assignment_group": "01"},
        [dependency("APPLIES_IN", "COMPANY_CODE", COMPANY, "société 1010")]))
    ex12_order = order(12, "ACCOUNT_DETERMINATION_TEST", "CDLC", "C615-B##", "##S4615-KO", "P615-1##", 1)
    objects.append(ex12_order)
    ex12_delivery = delivery(12, "ACCOUNT_DETERMINATION_TEST", ex12_order["object_id"], 1, "P615-1##")
    objects.append(ex12_delivery)
    objects.append(billing(12, "ACCOUNT_DETERMINATION_TEST", None, "STANDARD", "C615-B##",
        "OUTBOUND_DELIVERY", ex12_delivery["object_id"], "livraison de la commande ##S4615-KO",
        accounting_status="POSTED_TO_GL_49000000", posting_blocked=False,
        extra_dependencies=[dependency("ACCOUNT_DETERMINED_BY", "ACCOUNT_DETERMINATION",
                                       ACCOUNT_DET, "table 001 vers compte 49000000")]))

    # Exercise 13: two explicit fair-order chains; the second verifies changed FI reference rules.
    for suffix, customer_ref, accounting in (("POSTING_BLOCK", "##S4615-BS", "POSTED_AFTER_MANUAL_RELEASE"),
                                             ("FI_REFERENCE", "##S4615-Réf", "POSTED_AFTER_MANUAL_RELEASE")):
        ex13_order = order(13, suffix, "ZA##", "C615-A##", customer_ref, "P615-1##", 1)
        objects.append(ex13_order)
        ex13_delivery = delivery(13, suffix, ex13_order["object_id"], 1, "P615-1##")
        objects.append(ex13_delivery)
        objects.append(billing(13, suffix, "ZF##", "STANDARD", "C615-A##",
            "OUTBOUND_DELIVERY", ex13_delivery["object_id"], "livraison de la commande Foire ##",
            status="POSTED", accounting_status=accounting, posting_blocked=True,
            extra_dependencies=[dependency("CONTROLLED_BY", "COPY_CONTROL", FAIR_COPY,
                "ZF##/LF avec référence B et affectation E")]))

    return propagate_dependency_readiness(objects)


def propagate_dependency_readiness(objects: list[dict]) -> list[dict]:
    by_id = {item["object_id"]: item for item in objects}
    changed = True
    while changed:
        changed = False
        for item in objects:
            blocked_targets = [d for d in item["dependencies"] if d["status"] == "RESOLVED"
                               and d["critical"] and d["target_id"] in by_id
                               and by_id[d["target_id"]]["readiness_status"] == "BLOCKED"]
            if blocked_targets and not any(r["code"] == "DEPENDENCY_NOT_READY"
                                           for r in item["blocking_reasons"]):
                item["blocking_reasons"].append({"code": "DEPENDENCY_NOT_READY",
                    "message": "A resolved canonical prerequisite is not downstream-ready",
                    "field_path": "dependencies"})
                item["readiness_status"] = "BLOCKED"; changed = True
    return objects


SKIPPED = [
    {"pages": [29, 32], "scenario_id": sid(2), "candidate": "organizational navigation",
     "reason": "UI/navigation review; no new in-scope instance beyond company code 1010."},
    {"pages": [119, 126], "scenario_id": sid(7), "candidate": "three pre-existing due-list billings",
     "reason": "Batch count is known but source deliveries and invoice identities are blank; no synthetic IDs were created."},
    {"pages": [137, 140], "scenario_id": sid(8), "candidate": "simulated grouped invoice",
     "reason": "Simulation explicitly not saved; retained as explanatory evidence only."},
    {"pages": [155, 157], "scenario_id": "S4615_CH7_EBDR", "candidate": "external billing document request",
     "reason": "Reference-only demonstration and no approved canonical EBDR type."},
    {"pages": [249, 250], "scenario_id": "S4615_CH11_OUTPUT", "candidate": "output determination",
     "reason": "Appendix explains BRFplus/NAST channels but supplies no concrete rule instance."},
    {"pages": [261, 261], "scenario_id": "S4615_CH11_ACCOUNTING_EXAMPLE", "candidate": "generic FI/CO postings",
     "reason": "Theory example, not a separate business instance; FI/CO relationships are retained on qualifying billings."},
]


def parse_pdf(pdf: Path) -> tuple[list[str], dict]:
    executable = shutil.which("pdftotext") or r"C:\Program Files\Git\mingw64\bin\pdftotext.exe"
    if not Path(executable).is_file():
        raise FileNotFoundError("pdftotext is required")
    with tempfile.TemporaryDirectory() as tmp:
        text_path = Path(tmp) / "s4615.txt"
        subprocess.run([executable, "-layout", "-enc", "UTF-8", str(pdf), str(text_path)],
                       check=True, capture_output=True)
        text = text_path.read_text(encoding="utf-8")
    pages = text.split("\f")
    if pages and not pages[-1].strip(): pages.pop()
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
                   "table_marker_count": sum(page.count("Valeur de données") for page in pages)}


def section_inventory(objects: list[dict]) -> list[dict]:
    mentions = {}
    for item in objects:
        for source in item["provenance"]:
            if source.get("exercise"):
                mentions.setdefault(source["exercise"], set()).add(item["object_id"])
    skip_reason = {2: "Navigation/customizing review only; company code retained as shared reference.",
                   8: "Simulation only; no billing document saved."}
    result = []
    for exercise in range(1, 14):
        ids = sorted(mentions.get(exercise, []))
        primary = [item_id for item_id in ids if item_id.startswith(sid(exercise))]
        if primary:
            decision, reason = "EXTRACT", "Concrete source-backed instance data."
        elif ids:
            decision, reason = "ENRICH_EXISTING", "Explicit evidence enriches a previously extracted object."
        else:
            decision, reason = "SKIP", skip_reason.get(exercise, "No qualifying canonical instance.")
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
             for course in ("S4600", "S4610")}
    before = {course: hashlib.sha256(path.read_bytes()).hexdigest()
              for course, path in paths.items()}
    # Read only enough to prove that no explicit cross-course identifier can be joined.
    inventories = {course: len(json.loads(path.read_text(encoding="utf-8"))["objects"])
                   for course, path in paths.items()}
    after = {course: hashlib.sha256(path.read_bytes()).hexdigest()
             for course, path in paths.items()}
    if before != after:
        raise RuntimeError("Prior-stage artifacts changed during cross-document checks")
    return {"prior_stage_normalized_sha256": before, "prior_stage_object_counts": inventories,
            "explicit_cross_document_links": [],
            "assessment": "S4615 references course-local prior orders/deliveries; no source identifier explicitly joins an S4600 or S4610 staged object.",
            "return_delivery_issue": {"status": "UNRESOLVED_CARRIED_FORWARD",
                "s4600_object_id": "S4600_CH9_EX34_OUTBOUND_DELIVERY_RETURN_FROM_ORDER",
                "s4615_evidence": None,
                "assessment": "S4615 billing content supplies no explicit directional evidence for the S4600 customer-return delivery."}}


def main() -> None:
    entries = [entry for entry in load_manifest(ROOT) if entry["logical_name"] == COURSE]
    if len(entries) != 1: raise ValueError("S4615 must resolve exactly once")
    pdf = resolve_document(ROOT, COURSE, verify_checksum=True)
    if pdf.name != SOURCE_FILE: raise ValueError(pdf.name)
    pages, parse_stats = parse_pdf(pdf)
    objects = build_objects()
    if len({item["object_id"] for item in objects}) != len(objects):
        raise ValueError("Duplicate object IDs")
    for item in objects:
        errors = validate_object(ROOT, item)
        if errors: raise ValueError({item["object_id"]: errors})

    extracted = json.loads(json.dumps(objects))
    for item in extracted: item["lifecycle_status"] = "EXTRACTED"
    write_json("data/extracted/full/S4615/objects.json", {"objects": extracted})
    write_json("data/normalized/full/S4615/objects.json", {"objects": objects})
    write_json("metadata/lineage/full/S4615/lineage.json", {"objects": [
        {"object_id": item["object_id"], "scenario_id": item["scenario_id"],
         "source_to_canonical": [{"page": source["page"], "section_type": source["section_type"],
             "source_term": source["source_term"], "raw_excerpt": source["raw_excerpt"]}
             for source in item["provenance"]],
         "solution_enrichments": [{"page": source["page"], "source_term": source["source_term"]}
             for source in item["provenance"] if source["section_type"] == "SOLUTION"]}
        for item in objects]})
    write_json("metadata/lineage/full/S4615/section_inventory.json",
               {"sections": section_inventory(objects), "skipped_candidates": SKIPPED,
                "demonstrations": [{"scenario_id": "S4615_CH7_DEMO_INVOICE_LIST", "pages": [152, 153]},
                                   {"scenario_id": "S4615_CH8_DEMO_INSTALLMENT_PAYMENTS", "pages": [199, 200]}]})
    write_json("metadata/lineage/full/S4615/cross_document_checks.json", cross_document_checks())
    graph = {"nodes": [{"object_id": item["object_id"], "object_type": item["object_type"],
                         "readiness_status": item["readiness_status"]} for item in objects],
             "edges": [{"source": item["object_id"], "target": dep["target_id"],
                         "target_type": dep["target_type"], "relation": dep["relation"],
                         "status": dep["status"], "critical": dep["critical"],
                         "source_phrase": dep["source_phrase"]}
                        for item in objects for dep in item["dependencies"]]}
    write_json("metadata/dependencies/full/S4615/dependency_graph.json", graph)
    write_json("metadata/confidence/full/S4615/confidence.json", {"objects": [
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
    write_json("metadata/confidence/full/S4615/extraction_summary.json", summary)


if __name__ == "__main__":
    main()
