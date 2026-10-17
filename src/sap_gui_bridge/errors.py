"""Errors raised by the fail-closed SAP GUI bridge."""


class SapGuiBridgeError(RuntimeError):
    """Base bridge error."""


class SapGuiUnavailableError(SapGuiBridgeError):
    """SAP GUI scripting or its COM runtime is unavailable."""


class SessionNotFoundError(SapGuiBridgeError):
    """No unique session matching the expected identity was found."""


class SessionIdentityError(SapGuiBridgeError):
    """The selected SAP session does not match the allowlisted identity."""


class ActionBlockedError(SapGuiBridgeError):
    """An action was denied by the bridge policy."""


class ExecuteDisabledError(NotImplementedError, SapGuiBridgeError):
    """EXECUTE mode is intentionally disabled."""


class ProtocolError(SapGuiBridgeError):
    """A local runner request or response violates the protocol."""


class DuplicateRequestError(ProtocolError):
    """A request identity already exists in the queue lifecycle."""


class ResponseTimeoutError(ProtocolError):
    """No local-runner response arrived within the bounded wait."""
