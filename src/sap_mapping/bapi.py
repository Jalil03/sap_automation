from __future__ import annotations

from .common import put, require


def _flags(values: dict) -> dict:
    return {key: "X" for key in values}


def map_material(obj: dict) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    """Build deterministic BAPI_MATERIAL_SAVEDATA calls, one per plant context."""
    data = obj["data"]
    header = {}
    put(header, "MATERIAL", data.get("material_id"))
    put(header, "IND_SECTOR", data.get("industry_sector"))
    put(header, "MATL_TYPE", data.get("material_type"))
    if any(data.get(key) is not None for key in ("description", "base_unit")):
        header["BASIC_VIEW"] = "X"
    if any(data.get(key) is not None for key in (
        "sales_organization", "distribution_channel", "tax_classification",
        "minimum_order_quantity", "sales_text", "delivering_plant", "item_category_group",
    )):
        header["SALES_VIEW"] = "X"

    client = {}
    put(client, "BASE_UOM", data.get("base_unit"))
    descriptions = []
    if data.get("description") is not None:
        descriptions.append({"MATL_DESC": data["description"]})

    sales = {}
    put(sales, "SALES_ORG", data.get("sales_organization"))
    put(sales, "DISTR_CHAN", data.get("distribution_channel"))
    put(sales, "DELYG_PLNT", data.get("delivering_plant"))
    put(sales, "MIN_ORDER", data.get("minimum_order_quantity"))
    put(sales, "MIN_ORDER_UNIT", data.get("minimum_order_unit"))
    put(sales, "ITEM_CAT", data.get("item_category_group"))

    tax = []
    if data.get("tax_classification") is not None:
        tax.append({"TAX_CLASS": data["tax_classification"]})

    plant_values = list(dict.fromkeys(data.get("plants", []))) or [None]
    requests = []
    for plant in plant_values:
        payload = {"HEADDATA": dict(header)}
        if client:
            payload["CLIENTDATA"] = dict(client)
            payload["CLIENTDATAX"] = _flags(client)
        if descriptions:
            payload["MATERIALDESCRIPTION"] = list(descriptions)
        if sales:
            payload["SALESDATA"] = dict(sales)
            payload["SALESDATAX"] = _flags(sales)
        if tax:
            payload["TAXCLASSIFICATIONS"] = list(tax)
        plant_data = {}
        put(plant_data, "PLANT", plant)
        put(plant_data, "AVAILCHECK", data.get("availability_check"))
        put(plant_data, "STRATEGY_GROUP", data.get("strategy_group"))
        if plant_data:
            payload["PLANTDATA"] = plant_data
            payload["PLANTDATAX"] = _flags(plant_data)
        requests.append({"body": payload, "plant_context": plant})
    missing = require(header, ("MATERIAL", "MATL_TYPE", "IND_SECTOR"), "HEADDATA")
    return requests, [], [], missing


BAPI_MAPPERS = {"MATERIAL": map_material}
