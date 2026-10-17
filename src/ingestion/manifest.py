import hashlib, json
from pathlib import Path
def load_manifest(root: Path): return json.loads((root/"docs/manifests/documents.json").read_text(encoding="utf-8"))["documents"]
def resolve_document(root: Path, logical_name: str, verify_checksum=True):
    matches=[d for d in load_manifest(root) if d["logical_name"]==logical_name]
    if len(matches)!=1: raise ValueError(f"Expected one entry for {logical_name}")
    entry=matches[0]; path=(root/entry["source_path"]).resolve()
    if not path.is_file(): raise FileNotFoundError(path)
    if verify_checksum and entry["checksum"] != "sha256:"+hashlib.sha256(path.read_bytes()).hexdigest(): raise ValueError("Checksum mismatch")
    return path
