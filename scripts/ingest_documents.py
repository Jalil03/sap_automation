"""Verify manifest-backed sources only; no business extraction."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.ingestion.manifest import load_manifest, resolve_document
if __name__=="__main__":
    for d in load_manifest(ROOT): print(f'{d["logical_name"]}: {resolve_document(ROOT,d["logical_name"])}')
