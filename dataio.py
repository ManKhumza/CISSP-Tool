"""Structure-agnostic access to cissp-data.js (works with the flat v1 and nested v2 layouts)."""
import json, os

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"

def load_data(path=None):
    p = path or (BASE + r"\cissp-data.js")
    src = open(p, encoding="utf-8-sig").read()
    return json.loads(src[len("window.CISSP_DATA = "):].rstrip().rstrip(";"))

def questions_of(d):
    out = []
    if isinstance(d.get("questions"), list):
        out.extend(d["questions"])
    for s in d.get("sections", []):
        if isinstance(s, dict) and isinstance(s.get("questions"), list):
            out.extend(s["questions"])
    g = d.get("general")
    if isinstance(g, dict) and isinstance(g.get("questions"), list):
        out.extend(g["questions"])
    return out

def load_bank(path=None):
    """-> (DATA, {qn: question}, {sid: (title, domain_id)}, {domain_id: name})"""
    data = load_data(path)
    Q, SEC, DNAME = {}, {}, {}
    for d in data["domains"]:
        DNAME[d["id"]] = d["name"]
        for s in d.get("sections", []):
            if isinstance(s, dict) and "id" in s:
                SEC[s["id"]] = (s.get("title", ""), d["id"])
        for q in questions_of(d):
            Q[q["n"]] = q
    return data, Q, SEC, DNAME

def section_list(data):
    """-> {domain_id: [(sid, title), ...]} in outline order."""
    out = {}
    for d in data["domains"]:
        rows = []
        for s in d.get("sections", []):
            if isinstance(s, dict) and "id" in s:
                rows.append((s["id"], s.get("title", "")))
        out[d["id"]] = rows
    return out
