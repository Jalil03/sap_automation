from __future__ import annotations

import argparse
import json
import sys

from .scenario import build_golden_book_scenario
from .server import serve


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="S4615 Golden Book offline demonstration")
    value.add_argument("--training-user", default="07", metavar="00-99")
    value.add_argument("--serve", action="store_true", help="Serve the local read-only web view")
    value.add_argument("--host", default="127.0.0.1")
    value.add_argument("--port", type=int, default=8765)
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.serve:
        serve(args.host, args.port)
        return 0
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(
        build_golden_book_scenario(args.training_user),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
