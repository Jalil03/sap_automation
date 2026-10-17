from __future__ import annotations

import re


SENSITIVE_PATTERN = re.compile(
    r"(?i)(authorization|x-csrf-token|csrf|cookie|set-cookie|password)\s*[:=]\s*([^\s,;]+)"
)


def sanitize_error(value: object, *, limit: int = 1000) -> str:
    """Return a bounded message with common credential/header values removed."""
    text = str(value).replace("\r", " ").replace("\n", " ")
    text = SENSITIVE_PATTERN.sub(lambda match: f"{match.group(1)}=<redacted>", text)
    return text[:limit]
