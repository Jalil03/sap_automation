from __future__ import annotations

import base64
import http.cookiejar
import json
import socket
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Mapping, Protocol

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
        request_headers = {
            "Accept": "application/json",
            "Authorization": self._authorization,
            **dict(headers or {}),
        }
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
