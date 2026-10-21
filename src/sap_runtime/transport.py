from __future__ import annotations

import base64
import http.cookiejar
import json
import re
import socket
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Mapping, Protocol
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import xml.etree.ElementTree as ET

from .config import SapRuntimeConfig
from .errors import AmbiguousTransportError, TransportError


@dataclass(frozen=True)
class HttpResponse:
    status: int
    headers: Mapping[str, str]
    body: bytes = b""

    def header(self, name: str) -> str | None:
        lowered = name.lower()
        return next((value for key, value in self.headers.items() if key.lower() == lowered), None)

    def json(self) -> dict:
        if not self.body:
            return {}
        return json.loads(self.body.decode("utf-8"))

    @property
    def error_evidence(self) -> dict[str, str | int | None] | None:
        """Structured, sanitized evidence for HTTP failures; no raw body/logging."""
        return self.sanitized_sap_error() if 400 <= self.status < 600 else None

    def sanitized_sap_error(self) -> dict[str, str | int | None]:
        """Return bounded OData error evidence, never raw headers or response body."""
        def clean(value: object) -> str | None:
            if value is None:
                return None
            result = str(value)
            result = re.sub(r"(?i)\bBasic\s+[A-Za-z0-9+/=]+", "Basic [REDACTED]", result)
            result = re.sub(r"(?i)(authorization|cookie|password|token|secret)\s*[:=]\s*[^\s,;]+",
                            r"\1=[REDACTED]", result)
            result = "".join(char for char in result if char.isprintable())[:300]
            return result or None

        code = message = correlation = None
        try:
            payload = self.json()
            error = payload.get("error", {}) if isinstance(payload, dict) else {}
            if isinstance(error, dict):
                code = error.get("code")
                value = error.get("message")
                message = value.get("value") if isinstance(value, dict) else value
                inner = error.get("innererror", {})
                if isinstance(inner, dict):
                    correlation = inner.get("transactionid") or inner.get("transactionId")
        except (ValueError, UnicodeDecodeError):
            try:
                root = ET.fromstring(self.body)
                for node in root.iter():
                    tag = node.tag.rsplit("}", 1)[-1].lower()
                    if tag == "code" and code is None:
                        code = node.text
                    elif tag == "message" and message is None:
                        message = node.text
                    elif tag in {"transactionid", "correlationid"} and correlation is None:
                        correlation = node.text
            except ET.ParseError:
                pass
        correlation = correlation or self.header("sap-correlationid") or self.header("x-correlation-id")
        return {"http_status": self.status, "sap_code": clean(code),
                "sap_message": clean(message), "correlation_id": clean(correlation)}


class SapTransport(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: bytes | None = None,
    ) -> HttpResponse: ...


class UrllibSapTransport:
    """Small synchronous HTTP transport; no logging and no automatic retries."""

    def __init__(self, config: SapRuntimeConfig):
        self.config = config
        cookie_jar = http.cookiejar.CookieJar()
        handlers: list[urllib.request.BaseHandler] = [urllib.request.HTTPCookieProcessor(cookie_jar)]
        if not config.verify_tls:
            context = ssl._create_unverified_context()  # noqa: SLF001 - explicit opt-in configuration
            handlers.append(urllib.request.HTTPSHandler(context=context))
        self._opener = urllib.request.build_opener(*handlers)
        credentials = f"{config.username}:{config.password}".encode("utf-8")
        self._authorization = "Basic " + base64.b64encode(credentials).decode("ascii")

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: Mapping[str, str] | None = None,
        body: bytes | None = None,
    ) -> HttpResponse:
        url = self.config.base_url + "/" + path.lstrip("/")
        parsed = urlsplit(url)
        query = parse_qsl(parsed.query, keep_blank_values=True)
        supplied_clients = [value for key, value in query if key.lower() == "sap-client"]
        if supplied_clients and (len(supplied_clients) != 1 or supplied_clients[0] != self.config.client):
            raise ValueError("OData sap-client conflicts with configured SAP client")
        if not supplied_clients:
            query.append(("sap-client", self.config.client))
        url = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))
        metadata = parsed.path.rstrip("/").endswith("/$metadata")
        request_headers = {
            "Accept": "application/xml" if metadata else "application/json",
            "Authorization": self._authorization,
            **dict(headers or {}),
        }
        if metadata:
            request_headers["Accept"] = "application/xml"
        request = urllib.request.Request(
            url=url,
            data=body,
            headers=request_headers,
            method=method.upper(),
        )
        try:
            with self._opener.open(request, timeout=self.config.timeout_seconds) as response:
                return HttpResponse(
                    status=response.status,
                    headers=dict(response.headers.items()),
                    body=response.read(),
                )
        except urllib.error.HTTPError as error:
            return HttpResponse(
                status=error.code,
                headers=dict(error.headers.items()) if error.headers else {},
                body=error.read(),
            )
        except (TimeoutError, socket.timeout, urllib.error.URLError, OSError) as error:
            message = f"{type(error).__name__}: transport request failed"
            if method.upper() == "POST":
                raise AmbiguousTransportError(message) from error
            raise TransportError(message) from error
