"""Attach to an already-open SAP GUI Scripting session."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .errors import SapGuiUnavailableError, SessionIdentityError, SessionNotFoundError
from .safety import AuditLogger, SafetyMode, SafetyPolicy


EXPECTED_SYSTEM = "A4H"
EXPECTED_CLIENT = "600"
EXPECTED_USER = "ABDELJ"


def _default_get_object(name: str) -> Any:
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise SapGuiUnavailableError("pywin32 is required for live SAP GUI attachment") from exc
    errors = []
    # SAP GUI commonly publishes a ROT moniker named SAPGUI.  Depending on the
    # installed pywin32/SAP GUI versions it can be exposed as a moniker or an
    # active COM class.  Every strategy below is attach-only: Dispatch and
    # OpenConnection are intentionally absent.
    for getter in (
        lambda: win32com.client.GetObject(name),
        lambda: win32com.client.GetObject(Class=name),
        lambda: win32com.client.GetObject(Class="Sapgui.ScriptingCtrl.1"),
    ):
        try:
            return getter()
        except Exception as exc:  # COM errors differ across pywin32 releases.
            errors.append(exc)
    raise SapGuiUnavailableError(
        "Could not attach to a running SAP GUI COM object; no new connection was opened"
    ) from errors[-1]


def _children(parent: Any) -> list[Any]:
    collection = parent.Children
    return [collection(index) for index in range(int(collection.Count))]


@dataclass(frozen=True)
class SapGuiInventory:
    connections: int
    sessions: int


class SapGuiConnection:
    def __init__(
        self,
        *,
        mode: SafetyMode = SafetyMode.READ,
        get_object: Callable[[str], Any] = _default_get_object,
        log_path: Path | None = None,
    ) -> None:
        self.mode = SafetyMode(mode)
        self.get_object = get_object
        self.log_path = log_path or Path("logs/sap_gui_bridge/actions.jsonl")

    def attach(self):
        from .session import SapGuiSession

        sap_gui = self.get_object("SAPGUI")
        engine = sap_gui.GetScriptingEngine
        connections = _children(engine)
        sessions = [(connection, session) for connection in connections for session in _children(connection)]
        matching = []
        for connection, raw_session in sessions:
            info = raw_session.Info
            if (
                str(info.SystemName).upper() == EXPECTED_SYSTEM
                and str(info.Client) == EXPECTED_CLIENT
                and str(info.User).upper() == EXPECTED_USER
            ):
                matching.append((connection, raw_session))
        if len(matching) != 1:
            raise SessionNotFoundError(
                f"Expected exactly one {EXPECTED_SYSTEM}/{EXPECTED_CLIENT}/{EXPECTED_USER} session; found {len(matching)}"
            )
        connection, raw_session = matching[0]
        inventory = SapGuiInventory(connections=len(connections), sessions=len(sessions))
        policy = SafetyPolicy(self.mode, AuditLogger(self.log_path))
        wrapped = SapGuiSession(raw_session, connection, inventory, policy)
        wrapped.validate_identity()
        wrapped.audit("ATTACH")
        return wrapped


def validate_identity(identity: dict[str, str]) -> None:
    expected = {"system": EXPECTED_SYSTEM, "client": EXPECTED_CLIENT, "user": EXPECTED_USER}
    actual = {key: str(identity[key]).upper() if key in {"system", "user"} else str(identity[key]) for key in expected}
    if actual != expected:
        raise SessionIdentityError(f"Session identity mismatch: expected {expected}, got {actual}")
