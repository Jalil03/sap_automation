"""Run the proven ST22 read-only audit with an exercise 7 evidence path."""

from __future__ import annotations

from pathlib import Path

import audit_s4600_ex6_st22_today_readonly as audit

ROOT = Path(__file__).resolve().parents[1]
audit.OUTPUT = ROOT / "runtime" / "sap_reads" / "s4600_ex7_st22_post_billing_2026-10-22.json"


if __name__ == "__main__":
    raise SystemExit(audit.main())
