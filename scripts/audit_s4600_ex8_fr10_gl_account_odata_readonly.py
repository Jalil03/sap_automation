"""Read-only verification of the S4600 book bank G/L account against FR10."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_runtime.config import SapRuntimeConfig
from src.sap_runtime.transport import UrllibSapTransport

EXPECTED = {"system": "A4H", "client": "600", "user": "ABDELJ"}
OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex8_fr10_gl_account_2026-10-22.json"


def clean(value):
    if isinstance(value, dict):
        return {key: clean(item) for key, item in value.items() if key != "__metadata"}
    if isinstance(value, list):
        return [clean(item) for item in value]
    return value


def get(client, path: str, params: dict[str, str]) -> dict:
    response = client.request("GET", f"{path}?{urlencode(params)}", headers={"Accept": "application/json"})
    payload = response.json() if response.status == 200 else {}
    return {
        "http_status": response.status,
        "rows": clean(payload.get("d", {}).get("results", [])) if response.status == 200 else [],
        "error_excerpt": response.body.decode("utf-8", errors="replace")[:1500] if response.status != 200 else None,
    }


def main() -> int:
    load_dotenv(ROOT / ".env")
    config = SapRuntimeConfig.from_env()
    identity = {"system": "A4H", "client": config.client, "user": config.username.upper()}
    if identity != EXPECTED:
        raise SystemExit(f"Blocked: unexpected SAP identity {identity!r}")
    client = UrllibSapTransport(config)
    companies = get(
        client,
        "sap/opu/odata/sap/API_COMPANYCODE_SRV/A_CompanyCode",
        {
            "$filter": "CompanyCode eq 'FR10' or CompanyCode eq '1010'",
            "$select": "CompanyCode,CompanyCodeName,Currency,ChartOfAccounts,CountryChartOfAccounts",
            "$top": "10",
        },
    )
    fr10 = next((row for row in companies["rows"] if row.get("CompanyCode") == "FR10"), {})
    chart = fr10.get("ChartOfAccounts", "")
    book_accounts = get(
        client,
        "sap/opu/odata/sap/API_JOURNALENTRYITEMBASIC_SRV/A_GLAccountInChartOfAccounts",
        {
            "$filter": f"ChartOfAccounts eq '{chart}' and (GLAccount eq '11100000' or GLAccount eq '0011100000')",
            "$select": "ChartOfAccounts,GLAccount,GLAccountGroup,GLAccountType,GLAccountExternal,SampleGLAccount",
            "$top": "20",
        },
    ) if chart else {"http_status": None, "rows": [], "error_excerpt": "FR10 chart of accounts unavailable"}
    used_book_accounts = get(
        client,
        "sap/opu/odata/sap/API_JOURNALENTRYITEMBASIC_SRV/A_JournalEntryItemBasic",
        {
            "$filter": "CompanyCode eq 'FR10' and (GLAccount eq '11100000' or GLAccount eq '0011100000')",
            "$select": "CompanyCode,GLAccount,GLAccountName,ChartOfAccounts,TransactionCurrency,CompanyCodeCurrency,Customer",
            "$top": "100",
        },
    )
    bank_named_accounts = get(
        client,
        "sap/opu/odata/sap/API_JOURNALENTRYITEMBASIC_SRV/A_JournalEntryItemBasic",
        {
            "$filter": "CompanyCode eq 'FR10' and (substringof('Bank',GLAccountName) or substringof('Banque',GLAccountName) or substringof('Cash',GLAccountName) or substringof('Caisse',GLAccountName))",
            "$select": "CompanyCode,GLAccount,GLAccountName,ChartOfAccounts,TransactionCurrency,CompanyCodeCurrency,Customer",
            "$top": "500",
        },
    )
    observed_accounts_raw = get(
        client,
        "sap/opu/odata/sap/API_JOURNALENTRYITEMBASIC_SRV/A_JournalEntryItemBasic",
        {
            "$filter": "CompanyCode eq 'FR10'",
            "$select": "CompanyCode,GLAccount,GLAccountName,ChartOfAccounts,CompanyCodeCurrency,Customer",
            "$top": "1000",
        },
    )
    observed_accounts = sorted(
        {
            (row.get("GLAccount", ""), row.get("GLAccountName", ""), row.get("ChartOfAccounts", ""))
            for row in observed_accounts_raw["rows"]
            if row.get("GLAccount")
        }
    )
    evidence = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "STRICT_READ_ONLY_HTTP_GET",
        "environment": identity,
        "companies": companies,
        "fr10_chart_of_accounts": chart,
        "book_account_in_fr10_chart": book_accounts,
        "book_account_observed_in_fr10_postings": used_book_accounts,
        "bank_named_accounts_observed_in_fr10_postings": bank_named_accounts,
        "observed_fr10_accounts_query": {
            "http_status": observed_accounts_raw["http_status"],
            "error_excerpt": observed_accounts_raw["error_excerpt"],
            "raw_row_count": len(observed_accounts_raw["rows"]),
        },
        "observed_fr10_accounts_unique": [
            {"GLAccount": account, "GLAccountName": name, "ChartOfAccounts": coa}
            for account, name, coa in observed_accounts
        ],
        "write_performed": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(OUTPUT.relative_to(ROOT)),
        "companies": companies,
        "book_account_in_fr10_chart": book_accounts,
        "book_account_observed_in_fr10_postings": used_book_accounts,
        "bank_named_accounts_observed_in_fr10_postings": bank_named_accounts,
        "observed_fr10_accounts_unique": [
            {"GLAccount": account, "GLAccountName": name, "ChartOfAccounts": coa}
            for account, name, coa in observed_accounts
        ],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
