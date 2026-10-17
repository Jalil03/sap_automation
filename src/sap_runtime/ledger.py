from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

from .models import ExecutionStatus


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ExecutionLedger:
    """Local SQLite execution ledger. Payloads and credentials are never stored."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS sales_order_execution (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    canonical_object_id TEXT NOT NULL,
                    correlation_id TEXT NOT NULL,
                    customer_reference TEXT NOT NULL,
                    payload_sha256 TEXT NOT NULL,
                    attempt_number INTEGER NOT NULL,
                    mode TEXT NOT NULL,
                    status TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    http_status INTEGER,
                    created_sales_order_id TEXT,
                    response_etag TEXT,
                    sanitized_error TEXT
                )
            """)
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_so_ledger_identity "
                "ON sales_order_execution(canonical_object_id, correlation_id, payload_sha256)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_so_ledger_reference "
                "ON sales_order_execution(customer_reference)"
            )

    def start(
        self,
        *,
        canonical_object_id: str,
        correlation_id: str,
        customer_reference: str,
        payload_sha256: str,
        mode: str,
        status: ExecutionStatus,
    ) -> int:
        with self._connect() as connection:
            attempt = connection.execute(
                "SELECT COALESCE(MAX(attempt_number), 0) + 1 FROM sales_order_execution "
                "WHERE canonical_object_id = ? AND correlation_id = ?",
                (canonical_object_id, correlation_id),
            ).fetchone()[0]
            cursor = connection.execute(
                """
                INSERT INTO sales_order_execution (
                    canonical_object_id, correlation_id, customer_reference, payload_sha256,
                    attempt_number, mode, status, started_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    canonical_object_id, correlation_id, customer_reference, payload_sha256,
                    attempt, mode, status.value, utc_now(),
                ),
            )
            return int(cursor.lastrowid)

    def finish(
        self,
        entry_id: int,
        *,
        status: ExecutionStatus,
        http_status: int | None = None,
        created_sales_order_id: str | None = None,
        response_etag: str | None = None,
        sanitized_error: str | None = None,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE sales_order_execution
                SET status = ?, completed_at = ?, http_status = ?, created_sales_order_id = ?,
                    response_etag = ?, sanitized_error = ?
                WHERE id = ?
                """,
                (
                    status.value, utc_now(), http_status, created_sales_order_id,
                    response_etag, sanitized_error, entry_id,
                ),
            )

    def has_successful_dry_run(self, canonical_object_id: str, payload_sha256: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT 1 FROM sales_order_execution WHERE canonical_object_id = ? "
                "AND payload_sha256 = ? AND mode = 'DRY_RUN' AND status = ? LIMIT 1",
                (canonical_object_id, payload_sha256, ExecutionStatus.DRY_RUN_OK.value),
            ).fetchone()
        return row is not None

    def execution_conflict(
        self,
        *,
        canonical_object_id: str,
        correlation_id: str,
        payload_sha256: str,
        customer_reference: str,
    ) -> str | None:
        statuses = (
            ExecutionStatus.SUBMITTED.value,
            ExecutionStatus.CREATED.value,
            ExecutionStatus.VERIFIED.value,
            ExecutionStatus.AMBIGUOUS.value,
        )
        placeholders = ",".join("?" for _ in statuses)
        with self._connect() as connection:
            row = connection.execute(
                f"""
                SELECT status, canonical_object_id, customer_reference
                FROM sales_order_execution
                WHERE status IN ({placeholders})
                  AND (
                    canonical_object_id = ? OR correlation_id = ? OR payload_sha256 = ?
                    OR customer_reference = ?
                  )
                ORDER BY id DESC LIMIT 1
                """,
                (*statuses, canonical_object_id, correlation_id, payload_sha256, customer_reference),
            ).fetchone()
        if row is None:
            return None
        return f"ledger conflict: status={row['status']} object={row['canonical_object_id']} reference={row['customer_reference']}"

    def rows(self) -> list[dict]:
        with self._connect() as connection:
            return [dict(row) for row in connection.execute(
                "SELECT * FROM sales_order_execution ORDER BY id"
            ).fetchall()]
