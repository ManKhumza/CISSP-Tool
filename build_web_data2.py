"""
Build cissp-data.js (v2) with sub-section organisation and tailored study guides.

Structure produced:
window.CISSP_DATA = {
  meta: {...},
  studyGuide: {...},                     # exam-level guide (unchanged)
  domains: [
    { id, name, weight, count, description, keyTopics,
      totalQuestions,
      sections: [
        { id, title, count, guide: {focus, mustKnow[], keyTerms[]},
          questions: [ {n, t, q, o, a, e} ... ] }
      ],
      general: { count, questions: [...] }   # questions with no confident section
    }
  ]
}
"""
import json, os, re, sys
from collections import Counter

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
sys.path.insert(0, BASE)
from subsection_guides import GUIDES
from subsection_deep_notes import DEEP_NOTES
from subsection_glossary_extra import OVERRIDE, EXTRA
from dataio import load_data, questions_of, section_list

OLD = load_data()

FINAL = {int(k): v for k, v in json.load(open(BASE + r"\_classify\final_assignments.json",
                                              encoding="utf-8")).items()}
GLOSS = json.load(open(BASE + r"\_classify\guide_terms.json", encoding="utf-8"))

def norm_term(t):
    return re.sub(r"[\s\-]+", " ", t.lower()).strip()

def clean_meaning(d):
    """Strip remnants of practice-question framing from a mined meaning."""
    d = re.sub(r"\s*\(option\s+[A-D]\)", "", d, flags=re.I)
    d = re.sub(r"\s*(answer|explanation)\s*:\s*.*$", "", d, flags=re.I)
    d = re.sub(r"\s*the correct (answer|term) (is|for)\b[^.]*\.?", "", d, flags=re.I)
    d = re.sub(r"\s{2,}", " ", d).strip()
    return d

def build_glossary(sid, limit=40):
    """Merged glossary: mined meanings + curated overrides/additions."""
    from subsection_keywords import SUBSEC_TERMS
    LOW_VALUE = {"isc2", "exam", "exams", "question", "questions", "answer", "answers",
                 "test", "tests", "security", "system", "systems", "information", "data",
                 "control", "controls", "chapter", "book", "author"}
    mined = (GLOSS.get(sid) or {}).get("terms", [])
    bare = (GLOSS.get(sid) or {}).get("bare", [])
    curated_strong = {norm_term(t) for t in SUBSEC_TERMS.get(sid, {}).get("strong", [])}
    entries, seen = [], {}

    def push(term, meaning, kind, src, curated, strict_len=False):
        k = norm_term(term)
        meaning = clean_meaning(meaning or "")
        if not k or not meaning or k in seen or (k in LOW_VALUE and not curated):
            return
        # a mined "meaning" that is just the term again (a heading) or a fragment is useless
        if strict_len and (len(meaning) < 40 or norm_term(meaning) == k
                           or (norm_term(meaning).startswith(k + " ") and len(meaning) < 60)):
            return
        seen[k] = True
        entries.append({"t": term, "d": meaning, "k": kind, "src": src, "c": curated})

    for t, meaning in (OVERRIDE.get(sid) or {}).items():
        push(t, meaning, "def", "curated", True)
    for t, meaning in (EXTRA.get(sid) or {}).items():
        push(t, meaning, "def", "curated", True)
    for e in mined:
        push(e["t"], e["d"], e.get("k", "def"), e.get("src", ""), bool(e.get("c")),
             strict_len=True)

    # "also know" chips: keep only real-looking terms (curated vocabulary, acronyms,
    # hyphenated or numbered forms) and drop generic English words mined by frequency
    good = []
    for t in bare:
        k = norm_term(t)
        if not k or k in seen:
            continue
        looks_like_term = (k in curated_strong
                           or re.match(r"^[A-Z0-9][A-Za-z0-9()\-\.]{2,}$", t)
                           or "-" in t or any(ch.isdigit() for ch in t))
        if looks_like_term:
            good.append(t)
            seen[k] = True
    entries.sort(key=lambda x: (not x["c"], x["k"] != "def"))
    return entries[:limit], good[:24]

# ---------- gather questions from the existing data file (any layout) ----------
QBYN = {}
DOMAIN_META = {}
for d in OLD["domains"]:
    DOMAIN_META[d["id"]] = d
    for q in questions_of(d):
        # Once a portal has been renumbered, sourceN remains the stable key used
        # by the reviewed classification assignments. This keeps rebuilds idempotent.
        QBYN[q.get("sourceN", q["n"])] = q

SECLIST = section_list(OLD)
SECTION_TITLES = {sid: title for did, rows in SECLIST.items() for sid, title in rows}
SECTION_DOMAIN = {sid: did for did, rows in SECLIST.items() for sid, title in rows}

# ---------- key-term extraction per sub-section ----------
STOP = set("""the a an and or but if in on at to of for by with from as is are was were be been
being it its this that these those he she they them we you your our us i me my not no so do does
did can could will would shall should may might must have has had up down out off over under all
any some such than then there here when where why how who whom which what also use used using
one two three four five six seven eight nine ten first second third other another more most
following best least true false correct incorrect answer question which type called name not
except appropriate primarily main primary goal purpose reason implemented designed provides
provide ensure security system systems information data user users access control process
computer network application software policy risk management organization asset business service
services would could may based upon within between during without through should must also""".split())
WORD = re.compile(r"[a-z][a-z'\-]{2,}")

def key_terms(questions, limit=14):
    df = Counter()
    for q in questions:
        text = (q["q"] + " " + " ".join(o[1] for o in q["o"]) + " " + (q["e"] or "")).lower()
        seen = set()
        for w in WORD.findall(text):
            if w in STOP or len(w) < 4:
                continue
            seen.add(w)
        # prefer technical tokens and acronyms
        for w in seen:
            df[w] += 1
    scored = sorted(df.items(), key=lambda kv: (-kv[1], kv[0]))
    out = [w for w, c in scored if c >= 3][:limit]
    if len(out) < 8:
        out += [w for w, c in scored if w not in out][:8 - len(out)]
    return out

# ---------- assemble ----------
domains_out = []
for d in OLD["domains"]:
    did = d["id"]
    sections_out = []
    placed = 0
    for sid, title in SECLIST.get(did, []):
        qs = [dict(QBYN[n]) for n, a in FINAL.items() if a["section"] == sid]
        qs.sort(key=lambda q: q["n"])
        placed += len(qs)
        guide = GUIDES.get(sid, {})
        glossary, bare_terms = build_glossary(sid)
        sections_out.append({
            "id": sid,
            "title": title,
            "count": len(qs),
            "guide": {
                "focus": guide.get("focus", ""),
                "mustKnow": guide.get("mustKnow", []),
                "deepNotes": DEEP_NOTES.get(sid, []),
                "keyTerms": key_terms(qs),
                "glossary": glossary,
                "bareTerms": bare_terms,
            },
            "questions": qs,
        })

    gen = [dict(QBYN[n]) for n, a in FINAL.items()
           if a["section"] == "general" and a["domain"] == did]
    gen.sort(key=lambda q: q["n"])

    all_q = []
    for s in sections_out:
        all_q.extend(s["questions"])
    all_q.extend(gen)

    domains_out.append({
        "id": did,
        "name": d["name"],
        "full": d.get("full", "Domain %s: %s" % (did, d["name"])),
        "weight": d["weight"],
        "count": len(all_q),
        "placed": placed,
        "missing": sum(1 for q in all_q if not q.get("e")),
        "description": d["description"],
        "keyTopics": d["keyTopics"],
        "sections": sections_out,
        "general": {"count": len(gen), "questions": gen},
    })

payload = {
    "meta": dict(OLD["meta"]),
    "studyGuide": OLD["studyGuide"],
    "domains": domains_out,
}
payload["meta"].update({
    "total": len(FINAL),
    "subsections": len(SECTION_TITLES),
    "assigned": sum(1 for v in FINAL.values() if v["section"] != "general"),
    "general": sum(1 for v in FINAL.values() if v["section"] == "general"),
    "note": ("Every question is filed under the sub-section of the official ISC2 CISSP exam outline "
             "that it tests. Placement was produced by keyword analysis of the question bank and then "
             "reviewed question-by-question, so each sub-section contains only questions on its topic. "
             "Each sub-section carries its own study guide written for the questions it holds."),
})

# Renumber in the exact order learners encounter the bank. Keep the source number
# for traceability while using the new number everywhere in the portal UI/progress.
sequence = 0
for d in domains_out:
    for s in d["sections"]:
        for q in s["questions"]:
            sequence += 1
            q["sourceN"] = q.get("sourceN", q["n"])
            q["n"] = sequence
    for q in d["general"]["questions"]:
        sequence += 1
        q["sourceN"] = q.get("sourceN", q["n"])
        q["n"] = sequence
payload["meta"]["numbering"] = "Questions are numbered consecutively in study order from 1 to %d." % sequence

out_path = BASE + r"\cissp-data.js"
with open(out_path, "w", encoding="utf-8-sig") as f:
    f.write("window.CISSP_DATA = ")
    json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")

size = os.path.getsize(out_path) / (1024 * 1024)
print(f"wrote {out_path} ({size:.2f} MB)")
print(f"assigned {payload['meta']['assigned']}/{payload['meta']['total']}  "
      f"general {payload['meta']['general']}")
for d in domains_out:
    tops = ", ".join(f"{s['id']}:{s['count']}" for s in d["sections"][:4])
    print(f"  D{d['id']:<2} placed {d['placed']:>4}  general {d['general']['count']:>3}   {tops}")
# sanity: no duplicate assignment
seen = set()
dups = 0
for d in domains_out:
    for s in d["sections"]:
        for q in s["questions"]:
            if q["n"] in seen:
                dups += 1
            seen.add(q["n"])
    for q in d["general"]["questions"]:
        if q["n"] in seen:
            dups += 1
        seen.add(q["n"])
print(f"duplicate placements: {dups} | questions covered: {len(seen)}")
