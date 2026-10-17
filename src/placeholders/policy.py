def evaluate_placeholders(placeholders, mappings):
    result=[]; reasons=[]
    for p in placeholders:
        value=mappings.get(p["raw"]); resolved=value is not None
        result.append({**p,"status":"RESOLVED" if resolved else "UNRESOLVED","resolved":value if resolved else None})
        if p.get("mandatory") and not resolved: reasons.append({"code":"UNRESOLVED_MANDATORY_PLACEHOLDER","message":f'Mandatory placeholder {p["raw"]} is unresolved',"field_path":p.get("field_path")})
    return {"placeholders":result,"readiness_status":"BLOCKED" if reasons else "READY","blocking_reasons":reasons}
