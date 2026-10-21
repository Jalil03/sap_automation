"""Route the existing Phase 5 operations to their evidenced backend."""

from __future__ import annotations

from typing import Any

from src.provisioning.sap_api_backend import API_OPERATIONS, SapApiBackend
from src.provisioning.sap_gui_backend import SapGuiPhase5Backend


GUI_OPERATIONS = frozenset({
    "COMPANY_CODE_1010",
    "SALES_ORGANIZATION_1010",
    "SALES_ORG_1010_TO_COMPANY_CODE_1010",
    "DISTRIBUTION_CHANNEL_10_TO_SALES_ORG_1010",
    "DIVISION_00_TO_SALES_ORG_1010",
    "VOV4_ITEM_CATEGORY_DETERMINATION",
})


class CompositeBackend:
    writable = True

    def __init__(self, *, api: SapApiBackend | None = None, gui: SapGuiPhase5Backend | None = None) -> None:
        # Constructors do not make SAP calls; routing remains lazy.
        self.api = api or SapApiBackend()
        self.gui = gui or SapGuiPhase5Backend()

    def _route(self, operation: str) -> Any:
        if operation in API_OPERATIONS:
            return self.api
        if operation in GUI_OPERATIONS:
            return self.gui
        raise ValueError(f"No proven Phase 5 provisioning route for {operation}")

    def lookup(self, operation: str, target: dict[str, Any]) -> str:
        return self._route(operation).lookup(operation, target)

    def provision(self, operation: str, target: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
        return self._route(operation).provision(operation, target, values)

    def readback(self, operation: str, target: dict[str, Any]) -> dict[str, Any] | None:
        return self._route(operation).readback(operation, target)


def create_backend() -> CompositeBackend:
    return CompositeBackend()
