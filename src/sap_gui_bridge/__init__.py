"""Fail-closed bridge for an already-open SAP GUI session."""

from .connection import SapGuiConnection
from .inspection import inspect_screen
from .navigation import back, open_transaction, press_safe_button, set_text
from .safety import SafetyMode

__all__ = [
    "SapGuiConnection",
    "SafetyMode",
    "inspect_screen",
    "open_transaction",
    "press_safe_button",
    "set_text",
    "back",
]
