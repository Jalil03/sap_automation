"""Execute S4600 exercise 18 or 19 sales-order BAPI in TESTRUN mode only.

No commit function is created or called.  Exact duplicate checks are repeated
before and after the TESTRUN so an unexpected persistent effect is classified
as ambiguous instead of being retried.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

import pythoncom
import win32com.client
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.testrun_s4600_ex28_quotation_bapi import (
    get_item, structure_dispatch, structure_get, structure_set, table_append, table_get,
)
from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport


EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
SCENARIOS = {
    "18": {
        "header": {
            "DOC_TYPE": "TA", "SALES_ORG": "FR10", "DISTR_CHAN": "10", "DIVISION": "1W",
            "REQ_DATE_H": "20261101", "PURCH_NO_C": "6-100", "PMNTTRMS": "ZB00",
        },
        "items": [
            {"ITM_NUMBER": "000010", "MATERIAL": "10000282", "TARGET_QTY": "7"},
            {"ITM_NUMBER": "000020", "MATERIAL": "10000283", "TARGET_QTY": "8"},
        ],
        "schedules": [
            {"ITM_NUMBER": "000010", "SCHED_LINE": "0001", "REQ_DATE": "20261101", "REQ_QTY": "7"},
            {"ITM_NUMBER": "000020", "SCHED_LINE": "0001", "REQ_DATE": "20261101", "REQ_QTY": "8"},
        ],
        "partners": [{"PARTN_ROLE": "AG", "PARTN_NUMB": "1000000113", "ITM_NUMBER": "000000"}],
        "sold_to": "1000000113", "reference": "6-100",
        "adaptation_note": "ZB00 is the Book value and is tested, not assumed compatible with FR10.",
    },
    "19": {
        "header": {
            "DOC_TYPE": "TA", "SALES_ORG": "FR10", "DISTR_CHAN": "10", "DIVISION": "1W",
            "REQ_DATE_H": "20261029", "PURCH_NO_C": "6-400",
        },
        "items": [
            {"ITM_NUMBER": "000010", "MATERIAL": "10000282", "TARGET_QTY": "5"},
            {"ITM_NUMBER": "000020", "MATERIAL": "10000284", "TARGET_QTY": "1"},
        ],
        "schedules": [
            {"ITM_NUMBER": "000010", "SCHED_LINE": "0001", "REQ_DATE": "20261029", "REQ_QTY": "5"},
            {"ITM_NUMBER": "000020", "SCHED_LINE": "0001", "REQ_DATE": "20261029", "REQ_QTY": "1"},
        ],
        "partners": [
            {"PARTN_ROLE": "AG", "PARTN_NUMB": "1000000112", "ITM_NUMBER": "000000"},
            {"PARTN_ROLE": "WE", "PARTN_NUMB": "1000000112", "ITM_NUMBER": "000010"},
            {"PARTN_ROLE": "WE", "PARTN_NUMB": "1000000113", "ITM_NUMBER": "000020"},
        ],
        "sold_to": "1000000112", "reference": "6-400",
    },
}

# Compatible FR10 retry kept separate from the exact Book-value TESTRUN above.
# 0004 comes from the live A_CustomerSalesArea readback for customer 1000000113.
SCENARIOS["18-adapted"] = {
    **SCENARIOS["18"],
    "header": {**SCENARIOS["18"]["header"], "PMNTTRMS": "0004"},
    "adaptation_note": (
        "Book value ZB00 was rejected by SAP V1/398. Payment terms 0004 are the "
        "independently read customer default for 1000000113 in FR10/10/1W."
    ),
}
SCENARIOS["18-adapted-text"] = {
    **SCENARIOS["18-adapted"],
    "items": [
        {**SCENARIOS["18-adapted"]["items"][0], "SHORT_TEXT": "Shoes Laces"},
        {**SCENARIOS["18-adapted"]["items"][1], "SHORT_TEXT": "Leather Insoles Pair"},
    ],
    "adaptation_note": (
        "Adds the independently read EN product descriptions after BAPI V1/382, "
        "while retaining verified FR10 payment terms 0004."
    ),
}


def lookup(client, scenario: dict) -> dict:
    expression = (
        "SalesOrderType eq 'CS' and SalesOrganization eq 'FR10' and "
        "DistributionChannel eq '10' and OrganizationDivision eq '1W' and "
        f"SoldToParty eq '{scenario['sold_to']}' and "
        f"PurchaseOrderByCustomer eq '{scenario['reference']}'"
    )
    query = urlencode({"$filter": expression, "$select": "SalesOrder", "$top": "5"})
    response = client.request(
        "GET", f"sap/opu/odata/sap/API_SALES_ORDER_SRV/A_SalesOrder?{query}",
        headers={"Accept": "application/json"},
    )
    rows = response.json().get("d", {}).get("results", []) if response.status == 200 else []
    return {
        "http_status": response.status, "count": len(rows),
        "sales_orders": [str(row.get("SalesOrder")) for row in rows],
    }


def table_readback(table, row: int, fields: dict[str, str]) -> dict:
    return {field: table_get(table, row, field) for field in fields}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("exercise", choices=sorted(SCENARIOS))
    args = parser.parse_args()
    scenario = SCENARIOS[args.exercise]
    suffix = args.exercise.replace("-", "_")
    output = ROOT / "runtime" / "sap_writes" / f"s4600_ex{suffix}_order_bapi_testrun.json"

    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected identity {identity!r}")
    client = UrllibSapTransport(config)
    before = lookup(client, scenario)
    payload = {key: value for key, value in scenario.items() if key not in {"sold_to", "reference", "adaptation_note"}}
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": identity,
        "exercise": args.exercise,
        "operation": "BAPI_SALESORDER_CREATEFROMDAT2_TESTRUN_NO_COMMIT",
        "mode": "TESTRUN",
        "payload": payload,
        "payload_sha256": hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "book_or_mapping_note": scenario.get("adaptation_note"),
        "before_lookup": before,
        "commit_called": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    if before["http_status"] != 200 or before["count"]:
        result["status"] = "BLOCKED_LOOKUP"
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    pythoncom.CoInitialize()
    functions = win32com.client.Dispatch("SAP.Functions.Unicode")
    connection = functions.Connection
    connection.ApplicationServer = os.environ["SAP_APPLICATION_SERVER"]
    connection.SystemNumber = os.environ["SAP_SYSTEM_NUMBER"]
    connection.SystemID = "A4H"
    connection.Client = config.client
    connection.User = config.username
    connection.Password = os.environ["SAP_PASSWORD"]
    connection.Language = "F"
    if not bool(connection.Logon(0, True)):
        raise SystemExit("Blocked: RFC logon failed")
    actual = {
        "system": str(connection.SystemID).upper(),
        "client": str(connection.Client),
        "user": str(connection.User).upper(),
    }
    if actual != EXPECTED:
        connection.Logoff()
        raise SystemExit(f"Blocked: RFC identity mismatch {actual!r}")

    bapi = functions.Add("BAPI_SALESORDER_CREATEFROMDAT2")
    header = structure_dispatch(get_item(bapi.Exports, "ORDER_HEADER_IN"))
    header_x = structure_dispatch(get_item(bapi.Exports, "ORDER_HEADER_INX"))
    for field, value in scenario["header"].items():
        structure_set(header, field, value)
        structure_set(header_x, field, "X")
    structure_set(header_x, "UPDATEFLAG", "I")
    tables = {
        name: get_item(bapi.Tables, name)
        for name in (
            "ORDER_ITEMS_IN", "ORDER_ITEMS_INX", "ORDER_SCHEDULES_IN",
            "ORDER_SCHEDULES_INX", "ORDER_PARTNERS", "RETURN",
        )
    }
    staged = {"header": {field: structure_get(header, field) for field in scenario["header"]}}
    staged["items"] = []
    for values in scenario["items"]:
        row = table_append(tables["ORDER_ITEMS_IN"], values)
        x_values = {
            "ITM_NUMBER": values["ITM_NUMBER"], "UPDATEFLAG": "I",
            **{field: "X" for field in values if field != "ITM_NUMBER"},
        }
        table_append(tables["ORDER_ITEMS_INX"], x_values)
        staged["items"].append(table_readback(tables["ORDER_ITEMS_IN"], row, values))
    staged["schedules"] = []
    for values in scenario["schedules"]:
        row = table_append(tables["ORDER_SCHEDULES_IN"], values)
        x_values = {
            "ITM_NUMBER": values["ITM_NUMBER"], "SCHED_LINE": values["SCHED_LINE"],
            "UPDATEFLAG": "I", **{
                field: "X" for field in values if field not in {"ITM_NUMBER", "SCHED_LINE"}
            },
        }
        table_append(tables["ORDER_SCHEDULES_INX"], x_values)
        staged["schedules"].append(table_readback(tables["ORDER_SCHEDULES_IN"], row, values))
    staged["partners"] = []
    for values in scenario["partners"]:
        row = table_append(tables["ORDER_PARTNERS"], values)
        staged["partners"].append(table_readback(tables["ORDER_PARTNERS"], row, values))
    get_item(bapi.Exports, "TESTRUN").Value = "X"
    result["staged_readback"] = staged
    result["status"] = "SUBMITTED_TESTRUN"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")

    call_ok = bool(bapi.Call)
    return_table = tables["RETURN"]
    messages = [
        {
            field: table_get(return_table, row, field)
            for field in ("TYPE", "ID", "NUMBER", "MESSAGE", "PARAMETER", "ROW", "FIELD")
        }
        for row in range(1, int(return_table.RowCount) + 1)
    ]
    returned = str(get_item(bapi.Imports, "SALESDOCUMENT").Value or "")
    connection.Logoff()
    after = lookup(client, scenario)
    errors = [message for message in messages if str(message.get("TYPE", "")).upper() in {"E", "A", "X"}]
    result.update(
        call_ok=call_ok, return_messages=messages,
        returned_sales_document=returned, after_lookup=after,
    )
    unchanged = before == after
    result["status"] = (
        "TESTRUN_VALID" if call_ok and not errors and unchanged
        else "TESTRUN_REJECTED" if errors and unchanged
        else "AMBIGUOUS"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0 if result["status"] == "TESTRUN_VALID" else 2


if __name__ == "__main__":
    raise SystemExit(main())
