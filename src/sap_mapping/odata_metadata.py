from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


EDM = "http://schemas.microsoft.com/ado/2008/09/edm"
SAP = "http://www.sap.com/Protocols/SAPData"
NS = {"edm": EDM}


def _sap_attribute(element: ET.Element, name: str) -> str | None:
    return element.get(f"{{{SAP}}}{name}")


def _capability(element: ET.Element, name: str) -> dict[str, Any]:
    raw = _sap_attribute(element, name)
    return {
        "annotation": raw if raw is not None else "UNSPECIFIED",
        # SAP OData V2 capability annotations are restrictive: absent means
        # the operation is not disabled by metadata.
        "metadata_effective": raw != "false",
    }


def parse_odata_v2_metadata(path: str | Path) -> dict[str, Any]:
    """Parse a complete local OData V2 metadata document without I/O beyond disk."""
    metadata_path = Path(path)
    content = metadata_path.read_bytes()
    root = ET.fromstring(content)
    schema = root.find(".//edm:Schema", NS)
    if schema is None:
        raise ValueError("No EDM Schema element found")

    associations: dict[str, dict[str, Any]] = {}
    for association in schema.findall("edm:Association", NS):
        ends = {}
        for end in association.findall("edm:End", NS):
            ends[end.get("Role", "")] = {
                "type": end.get("Type"),
                "multiplicity": end.get("Multiplicity"),
            }
        associations[association.get("Name", "")] = {"ends": ends}

    entity_types: dict[str, dict[str, Any]] = {}
    for entity in schema.findall("edm:EntityType", NS):
        properties = {}
        for prop in entity.findall("edm:Property", NS):
            properties[prop.get("Name", "")] = {
                "edm_type": prop.get("Type"),
                "nullable": prop.get("Nullable", "true") != "false",
                "max_length": int(prop.get("MaxLength")) if prop.get("MaxLength", "").isdigit() else None,
                "precision": int(prop.get("Precision")) if prop.get("Precision", "").isdigit() else None,
                "scale": int(prop.get("Scale")) if prop.get("Scale", "").isdigit() else None,
                "creatable": _capability(prop, "creatable"),
                "updatable": _capability(prop, "updatable"),
            }
        navigations = {}
        for nav in entity.findall("edm:NavigationProperty", NS):
            relationship = (nav.get("Relationship") or "").split(".")[-1]
            association = associations.get(relationship, {"ends": {}})
            target = association["ends"].get(nav.get("ToRole", ""), {})
            navigations[nav.get("Name", "")] = {
                "relationship": nav.get("Relationship"),
                "target_type": target.get("type"),
                "multiplicity": target.get("multiplicity"),
            }
        entity_types[entity.get("Name", "")] = {
            "keys": [ref.get("Name") for ref in entity.findall("edm:Key/edm:PropertyRef", NS)],
            "properties": properties,
            "navigation_properties": navigations,
        }

    entity_sets = {}
    for entity_set in schema.findall(".//edm:EntitySet", NS):
        entity_sets[entity_set.get("Name", "")] = {
            "entity_type": entity_set.get("EntityType"),
            "create": _capability(entity_set, "creatable"),
            "update": _capability(entity_set, "updatable"),
            "delete": _capability(entity_set, "deletable"),
        }

    return {
        "sha256": hashlib.sha256(content).hexdigest(),
        "byte_count": len(content),
        "namespace": schema.get("Namespace"),
        "data_service_version": root.find(".//{http://schemas.microsoft.com/ado/2007/06/edmx}DataServices").get(
            "{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}DataServiceVersion"
        ),
        "entity_types": entity_types,
        "entity_sets": entity_sets,
        "association_count": len(associations),
    }
