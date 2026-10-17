class SapRuntimeError(Exception):
    """Base runtime error."""


class ConfigurationError(SapRuntimeError):
    """Configuration is missing or unsafe."""


class PreflightBlocked(SapRuntimeError):
    """A deterministic preflight gate blocked execution."""


class TransportError(SapRuntimeError):
    """The HTTP outcome is known to have failed before a valid response."""


class AmbiguousTransportError(TransportError):
    """The request may have reached SAP, so retry is unsafe."""
