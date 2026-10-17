import re
def scenario_id(course,chapter,exercise):
    clean=lambda v: re.sub(r"[^A-Za-z0-9-]","",str(v))
    return f"{course}_CH{clean(chapter)}_EX{clean(exercise)}"
def merge_scenario_sections(sections):
    grouped={}
    for s in sections:
        b=grouped.setdefault(s["scenario_id"],{"primary":None,"verification":[]})
        if s["section_type"]=="EXERCISE":
            if b["primary"] is not None: raise ValueError("Duplicate exercise")
            b["primary"]=s
        elif s["section_type"]=="SOLUTION": b["verification"].append(s)
    if any(v["primary"] is None for v in grouped.values()): raise ValueError("Solution without exercise")
    return grouped
