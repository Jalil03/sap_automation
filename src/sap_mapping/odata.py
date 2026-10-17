from __future__ import annotations

from copy import deepcopy

from .common import dependency_binding, mapped_date, put, require


def map_business_partner(obj: dict) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    """Build the live-metadata-backed sequential Business Partner create plan.

    API_BUSINESS_PARTNER does not expose A_Customer as directly creatable.  A
    customer is therefore materialized by adding the observed customer roles,
    then the company-code and sales-area segments are created independently.
    Each payload is deliberately small so an executor can read back every step.
    """
    data = obj["data"]
    partner_id = data.get("partner_id")
    payloads = []

    partner = {}
    put(partner, "BusinessPartner", partner_id)
    put(partner, "BusinessPartnerGrouping", data.get("grouping"))
    # BusinessPartnerFullName is live-metadata creatable=false.  Organization
    # names must use the writable organization-name property instead.
    put(partner, "OrganizationBPName1", data.get("name"))
    payloads.append({
        "method": "POST",
        "entity_set": "A_BusinessPartner",
        "readback_entity_set": "A_BusinessPartner",
        "body": partner,
    })

    roles = list(dict.fromkeys(data.get("roles", [])))
    for role in roles:
        payloads.append({
            "method": "POST",
            "entity_set": "A_BusinessPartnerRole",
            "readback_entity_set": "A_BusinessPartnerRole",
            "body": {"BusinessPartner": partner_id, "BusinessPartnerRole": role},
        })

    company = {}
    put(company, "Customer", partner_id)
    put(company, "CompanyCode", data.get("company_code"))
    put(company, "ReconciliationAccount", data.get("reconciliation_account"))
    put(company, "PaymentTerms", data.get("payment_terms"))
    put(company, "CustomerAccountGroup", data.get("grouping"))
    if len(company) > 1:
        payloads.append({
            "method": "POST",
            "entity_set": "A_CustomerCompany",
            "readback_entity_set": "A_CustomerCompany",
            "body": company,
        })

    invalid_sales_areas = []
    for index, sales_area in enumerate(data.get("sales_areas", [])):
        parts = sales_area.split("/")
        mapped = {"Customer": partner_id}
        if len(parts) == 3:
            mapped.update({
                "SalesOrganization": parts[0],
                "DistributionChannel": parts[1],
                "Division": parts[2],
            })
        else:
            invalid_sales_areas.append(f"data.sales_areas[{index}]")
        put(mapped, "Currency", data.get("currency"))
        put(mapped, "ShippingCondition", data.get("shipping_conditions"))
        put(mapped, "SupplyingPlant", data.get("delivering_plant"))
        put(mapped, "IncotermsClassification", data.get("incoterms"))
        put(mapped, "IncotermsLocation1", data.get("incoterms_location"))
        put(mapped, "CustomerPaymentTerms", data.get("payment_terms"))
        put(mapped, "CustomerAccountAssignmentGroup", data.get("account_assignment_group"))
        put(mapped, "CustomerPricingProcedure", data.get("customer_pricing_procedure"))
        put(mapped, "CustomerAccountGroup", data.get("grouping"))
        payloads.append({
            "method": "POST",
            "entity_set": "A_CustomerSalesArea",
            "readback_entity_set": "A_CustomerSalesArea",
            "body": mapped,
        })

    missing = require(partner, ("BusinessPartner",), "A_BusinessPartner") + invalid_sales_areas
    if not roles:
        missing.append("data.roles.customer_role")
    # These collections need their own sequential live contracts.  Keeping
    # them out of the root prevents the invalid, unverified deep insert that
    # the former mapper produced.
    for field in ("addresses", "tax_classifications", "partner_functions"):
        if data.get(field):
            missing.append(f"data.{field}.sequential_create_contract")
    if data.get("fax_number") is not None:
        missing.append("data.fax_number.sequential_create_contract")
    return payloads, [], [], missing


def _sales_order_item(item: dict) -> dict:
    mapped = {}
    fields = {
        "line_id": "SalesOrderItem", "material": "Material",
        "quantity": "RequestedQuantity", "unit": "RequestedQuantityUnit",
        "plant": "ProductionPlant", "shipping_point": "ShippingPoint",
        "item_category": "SalesOrderItemCategory",
    }
    for canonical, sap in fields.items():
        put(mapped, sap, item.get(canonical))
    return mapped


def map_sales_order(obj: dict) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    data = obj["data"]
    body = {}
    fields = {
        "order_type": "SalesOrderType", "sales_organization": "SalesOrganization",
        "distribution_channel": "DistributionChannel", "sales_division": "OrganizationDivision",
        "sold_to_party": "SoldToParty",
        "customer_reference": "PurchaseOrderByCustomer", "payment_terms": "CustomerPaymentTerms",
    }
    for canonical, sap in fields.items():
        put(body, sap, data.get(canonical))
    # Phase 3B.0 supplied deterministic external-to-internal role evidence:
    # DO -> AG -> sold-to. The OData write property is the external
    # PartnerFunction; PartnerFunctionInternalCode is non-creatable.
    sold_to_party = data.get("sold_to_party")
    put(body, "to_Partner", [
        {"PartnerFunction": "DO", "Customer": sold_to_party}
    ] if sold_to_party is not None else None)
    deferred = []
    requested = mapped_date(
        data.get("requested_delivery_date"), "data.requested_delivery_date",
        "RequestedDeliveryDate", deferred,
    )
    put(body, "RequestedDeliveryDate", requested)
    items = [_sales_order_item(item) for item in data.get("items", [])]
    put(body, "to_Item", items or None)
    missing = require(
        body,
        ("SalesOrderType", "SalesOrganization", "DistributionChannel", "OrganizationDivision", "SoldToParty", "to_Item"),
        "body",
    )
    for index, item in enumerate(items):
        missing.extend(require(item, ("SalesOrderItem", "Material", "RequestedQuantity"), f"body.to_Item[{index}]"))
    return [{"body": body}], [], deferred, missing


def map_pricing_condition(obj: dict) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    data = obj["data"]
    body = {}
    put(body, "ConditionType", data.get("condition_type"))
    put(body, "ConditionRateValue", data.get("rate"))
    put(body, "ConditionRateValueUnit", data.get("currency") or data.get("rate_unit"))
    put(body, "ConditionQuantity", data.get("pricing_unit"))
    put(body, "ConditionCalculationType", data.get("calculation_semantics"))
    put(body, "ConditionIsDeleted", data.get("deletion_indicator"))
    key_fields = {
        "sales_organization": "SalesOrganization", "distribution_channel": "DistributionChannel",
        "customer": "Customer", "material": "Material", "incoterms": "IncotermsClassification",
        "destination_country": "DestinationCountry", "customer_hierarchy_node": "CustomerHierarchyNode",
        "promotion_reference": "Promotion", "sales_deal_reference": "SalesDeal",
    }
    for canonical, sap in key_fields.items():
        put(body, sap, (data.get("key_combination") or {}).get(canonical))
    deferred = []
    put(body, "ConditionValidityStartDate", mapped_date(data.get("valid_from"), "data.valid_from", "ConditionValidityStartDate", deferred))
    put(body, "ConditionValidityEndDate", mapped_date(data.get("valid_to"), "data.valid_to", "ConditionValidityEndDate", deferred))
    scales = []
    for scale in data.get("scales", []):
        mapped = {}
        scale_fields = {
            "scale_basis": "ConditionScaleBasis", "threshold": "ConditionScaleValue",
            "threshold_unit": "ConditionScaleValueUnit", "threshold_currency": "ConditionScaleValueCurrency",
            "amount": "ConditionRateValue", "currency": "ConditionRateValueUnit",
            "rate": "ConditionRateValue", "rate_unit": "ConditionRateValueUnit",
            "pricing_unit": "ConditionQuantity",
        }
        for canonical, sap in scale_fields.items():
            put(mapped, sap, scale.get(canonical))
        scales.append(mapped)
    put(body, "to_PricingScale", scales or None)
    has_value = body.get("ConditionRateValue") is not None or bool(scales)
    missing = require(body, ("ConditionType",), "body")
    if not has_value:
        missing.append("body.ConditionRateValue_or_to_PricingScale")
    return [{"body": body}], [], deferred, missing


def _delivery_item(item: dict) -> dict:
    mapped = {}
    fields = {
        "line_id": "DeliveryDocumentItem", "material": "Material",
        "quantity": "ActualDeliveryQuantity", "unit": "DeliveryQuantityUnit",
        "reference_item": "ReferenceSDDocumentItem", "plant": "Plant",
        "storage_location": "StorageLocation", "warehouse_number": "Warehouse",
        "item_category": "DeliveryDocumentItemCategory",
    }
    for canonical, sap in fields.items():
        put(mapped, sap, item.get(canonical))
    return mapped


def map_outbound_delivery(obj: dict) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    data = obj["data"]
    body = {}
    put(body, "DeliveryDocumentType", data.get("delivery_type"))
    put(body, "ShipToParty", data.get("ship_to_party"))
    put(body, "ShippingPoint", data.get("shipping_point"))
    items = [_delivery_item(item) for item in data.get("items", [])]
    put(body, "to_DeliveryDocumentItem", items or None)
    bindings = []
    dependency_binding(obj, "SALES_ORDER", "CREATED_FROM", "ReferenceSDDocument", bindings)
    deferred = []
    put(body, "SelectionDate", mapped_date(data.get("planned_creation_date"), "data.planned_creation_date", "SelectionDate", deferred))
    put(body, "PlannedGoodsIssueDate", mapped_date(data.get("planned_goods_issue_date"), "data.planned_goods_issue_date", "PlannedGoodsIssueDate", deferred))
    missing = require(body, ("ShippingPoint",), "body")
    if not items and not bindings:
        missing.append("body.to_DeliveryDocumentItem_or_binding.ReferenceSDDocument")
    return [{"body": body}], bindings, deferred, missing


def _billing_item(item: dict) -> dict:
    mapped = {}
    fields = {
        "line_id": "BillingDocumentItem", "material": "Material",
        "quantity": "BillingQuantity", "unit": "BillingQuantityUnit",
        "reference_item": "ReferenceSDDocumentItem", "net_value": "NetAmount",
        "currency": "TransactionCurrency", "sales_division": "Division",
    }
    for canonical, sap in fields.items():
        put(mapped, sap, item.get(canonical))
    return mapped


def map_billing(obj: dict) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    data = obj["data"]
    body = {}
    fields = {
        "billing_type": "BillingDocumentType", "payer": "PayerParty",
        "reference_document": "ReferenceSDDocument", "payment_terms": "CustomerPaymentTerms",
        "net_value": "TotalNetAmount", "currency": "TransactionCurrency",
    }
    for canonical, sap in fields.items():
        put(body, sap, data.get(canonical))
    deferred = []
    put(body, "BillingDocumentDate", mapped_date(data.get("billing_date"), "data.billing_date", "BillingDocumentDate", deferred))
    items = [_billing_item(item) for item in data.get("items", [])]
    put(body, "to_Item", items or None)
    bindings = []
    if not data.get("reference_document"):
        dependency_binding(obj, "OUTBOUND_DELIVERY", "BILLED_FROM", "ReferenceSDDocument", bindings)
        dependency_binding(obj, "SALES_ORDER", "BILLED_FROM", "ReferenceSDDocument", bindings)
    missing = require(body, ("BillingDocumentType",), "body")
    if not body.get("ReferenceSDDocument") and not bindings and not items:
        missing.append("body.ReferenceSDDocument_or_to_Item")
    return [{"body": body}], bindings, deferred, missing


ODATA_MAPPERS = {
    "BUSINESS_PARTNER": map_business_partner,
    "SALES_ORDER": map_sales_order,
    "PRICING_CONDITION": map_pricing_condition,
    "OUTBOUND_DELIVERY": map_outbound_delivery,
    "BILLING": map_billing,
}
