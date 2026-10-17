"""Guarded wrapper around a GuiSession COM object."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .connection import SapGuiInventory, validate_identity
from .safety import SafetyPolicy


@dataclass(frozen=True)
class SessionStatus:
    system: str
    client: str
    user: str
    transaction: str
    connections: int
    sessions: int
    mode: str


class SapGuiSession:
    def __init__(self, raw: Any, connection: Any, inventory: SapGuiInventory, policy: SafetyPolicy) -> None:
        self.raw = raw
        self.connection = connection
        self.inventory = inventory
        self.policy = policy

    @property
    def identity(self) -> dict[str, str]:
        info = self.raw.Info
        return {
            "system": str(info.SystemName),
            "client": str(info.Client),
            "user": str(info.User),
            "transaction": str(getattr(info, "Transaction", "")),
        }

    def validate_identity(self) -> None:
        validate_identity(self.identity)

    def audit(self, action: str, **kwargs: Any) -> None:
        self.validate_identity()
        self.policy.authorize(identity=self.identity, action=action, **kwargs)

    def status(self) -> dict[str, Any]:
        self.audit("STATUS")
        identity = self.identity
        return asdict(
            SessionStatus(
                system=identity["system"],
                client=identity["client"],
                user=identity["user"],
                transaction=identity["transaction"],
                connections=self.inventory.connections,
                sessions=self.inventory.sessions,
                mode=self.policy.mode.value,
            )
        )

    def find(self, control_id: str) -> Any:
        return self.raw.findById(control_id)
