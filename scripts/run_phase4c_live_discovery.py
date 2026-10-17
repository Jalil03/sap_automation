"""Manual entry point for filesystem-only Phase 4C live discovery."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.discovery import (
    FilesystemRunnerClient,
    Phase4CDiscovery,
    compact_summary,
)


OUTPUT_DIR = ROOT / "runtime" / "sap_discovery" / "phase4c"


def main() -> int:
    if len(sys.argv) > 1:
        if sys.argv[1:] in (["-h"], ["--help"]):
            print("Usage: .venv\\Scripts\\python.exe scripts\\run_phase4c_live_discovery.py")
            return 0
        raise SystemExit("The Phase 4C discovery script accepts no arguments")
    discovery = Phase4CDiscovery(
        FilesystemRunnerClient(), OUTPUT_DIR, archive_existing=True
    )
    summary = discovery.run()
    print(compact_summary(summary, OUTPUT_DIR))
    return 0 if summary["status"] in {
        "SUCCESS",
        "PARTIAL",
        "COMPLETE/PARTIAL_READY_FOR_PREPARE",
        "COMPLETE_READY_FOR_PREPARE",
    } else 2


if __name__ == "__main__":
    raise SystemExit(main())
