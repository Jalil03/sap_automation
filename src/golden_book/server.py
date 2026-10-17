from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from src.training_context import TrainingContextError

from .scenario import build_golden_book_scenario


STATIC_ROOT = Path(__file__).with_name("static")


class GoldenBookHandler(BaseHTTPRequestHandler):
    server_version = "GoldenBookOffline/1.0"

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler contract
        parsed = urlsplit(self.path)
        if parsed.path == "/api/golden-book":
            self._api(parsed.query)
            return
        if parsed.path in {"/", "/index.html"}:
            self._file("index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/styles.css":
            self._file("styles.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/app.js":
            self._file("app.js", "text/javascript; charset=utf-8")
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802 - explicitly forbid writes
        self.send_error(HTTPStatus.METHOD_NOT_ALLOWED, "Golden Book is read-only")

    def log_message(self, format: str, *args: object) -> None:
        return

    def _api(self, query: str) -> None:
        code = parse_qs(query).get("training_user", ["07"])[0]
        try:
            payload = build_golden_book_scenario(code)
            self._json(HTTPStatus.OK, payload)
        except (TrainingContextError, KeyError, ValueError) as error:
            self._json(HTTPStatus.BAD_REQUEST, {"status": "BLOCKED", "error": str(error)})

    def _file(self, name: str, content_type: str) -> None:
        body = (STATIC_ROOT / name).read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: HTTPStatus, value: dict) -> None:
        body = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    server = ThreadingHTTPServer((host, port), GoldenBookHandler)
    print(f"Golden Book offline view: http://{host}:{server.server_port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
