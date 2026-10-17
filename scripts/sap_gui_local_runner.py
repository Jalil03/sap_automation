"""Manual Windows entry point for the local SAP GUI filesystem runner."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.sap_gui_bridge.runner import run_forever
from src.provisioning.sap_gui_backend import execute_runner_action


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1:] in (["-h"], ["--help"]):
            print("Usage: .venv\\Scripts\\python.exe scripts\\sap_gui_local_runner.py")
            raise SystemExit(0)
        raise SystemExit("The local runner accepts no arguments")
    run_forever(execute_handler=execute_runner_action)
