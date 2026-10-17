import json
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

def schema_registry(root: Path):
    registry=Registry()
    for path in (root/"schemas").rglob("*.schema.json"):
        registry=registry.with_resource(path.resolve().as_uri(),Resource.from_contents(json.loads(path.read_text(encoding="utf-8"))))
    return registry

def validate_object(root: Path, obj):
    index=json.loads((root/"schemas/index.json").read_text(encoding="utf-8"))
    path=(root/index[obj["object_type"]]["schema"]).resolve()
    schema=json.loads(path.read_text(encoding="utf-8"))
    schema.setdefault("$id",path.as_uri())
    errors=sorted(Draft202012Validator(schema,registry=schema_registry(root)).iter_errors(obj),key=lambda e:list(e.path))
    return [{"path":".".join(map(str,e.absolute_path)),"message":e.message} for e in errors]
