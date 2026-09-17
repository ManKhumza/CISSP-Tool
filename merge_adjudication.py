"""
Merge subagent adjudication over the rule-based assignments, with a sanity filter.

A returned label is accepted unless the curated keyword evidence strongly
contradicts it (the label's own evidence is nil or the best alternative scores at
least 3x higher AND has a curated strong term in the question text). This catches
isolated slips such as filing TCSEC / Orange Book questions under 3.2 instead of 3.4.

Writes _classify/final_assignments.json
"""
import json, os, glob, re, sys
from collections import Counter

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
OUT = os.path.join(BASE, "_classify")
sys.path.insert(0, BASE)
from subsection_keywords import SUBSEC_TERMS
from dataio import load_bank, section_list

DATA, Q, SEC_INFO, DNAME = load_bank()
SECLIST = section_list(DATA)

VALID, SECTION_DOMAIN, SECTION_TITLE = set(), {}, {}
for did, rows in SECLIST.items():
    for sid, title in rows:
        VALID.add(sid); SECTION_DOMAIN[sid] = did; SECTION_TITLE[sid] = title
VALID.add("general")

# ---------- compact curated scorer (strong terms only) ----------
WORD_RX = re.compile(r"[a-z][a-z'\-]*|\d+(?:\.\d+)?")
def _kind(p):
    t = WORD_RX.findall(p)
    if t == [p]: return "w1"
    if len(t) == 2 and t[0] + " " + t[1] == p: return "w2"
    return "rx"

def _build(terms, w):
    w1, w2, rx = {}, {}, []
    for p in terms:
        k = _kind(p)
        if k == "w1": w1[p] = w
        elif k == "w2": w2[p] = w
        else: rx.append((p, re.compile(r"(?<![a-z0-9])" + re.escape(p).replace(r"\ ", r"\s+") + r"(?![a-z0-9])")))
    return w1, w2, rx

STRONG = {sid: _build(SUBSEC_TERMS.get(sid, {}).get("strong", []), 7) for sid in SECTION_TITLE}

def _norm(s): return re.sub(r"\s+", " ", (s or "").lower())

def _score_field(field, text, w1, w2, rx):
    t = _norm(text)
    ws = WORD_RX.findall(t)
    c1, c2 = Counter(ws), Counter(ws[i] + " " + ws[i+1] for i in range(len(ws)-1))
    n = 0
    for p in w1:
        n += c1.get(p, 0)
    for p in w2:
        n += c2.get(p, 0)
    for p, r in rx:
        n += len(r.findall(t))
    return n

def score(qn, sid):
    q = Q[qn]
    w1, w2, rx = STRONG.get(sid, ({}, {}, []))
    s  = 3.0 * _score_field("t", q["q"], w1, w2, rx)
    s += 1.0 * _score_field("o", " ".join(o[1] for o in q["o"]), w1, w2, rx)
    s += 0.25 * _score_field("e", q["e"] or "", w1, w2, rx)
    return s

def text_hit(qn, sid):
    q = Q[qn]
    w1, w2, rx = STRONG.get(sid, ({}, {}, []))
    return _score_field("t", q["q"], w1, w2, rx) > 0

# ---------- load ----------
base = {int(k): v for k, v in json.load(open(OUT + r"\assignments.json", encoding="utf-8")).items()}
files = sorted(glob.glob(OUT + r"\out\out_*.json"))
print(f"adjudication files: {len(files)}")

merged, bad = {}, Counter()
for fp in files:
    try:
        data = json.load(open(fp, encoding="utf-8"))
    except Exception as e:
        print(f"  !! {os.path.basename(fp)} unreadable: {e}"); continue
    ok = 0
    for k, v in data.items():
        try: qn = int(k)
        except ValueError: bad["bad key"] += 1; continue
        if qn not in base: bad["unknown qn"] += 1; continue
        lab = str(v).strip()
        if lab not in VALID: bad["invalid label " + lab] += 1; continue
        merged[qn] = lab; ok += 1
    print(f"  {os.path.basename(fp)}: {ok}")

# ---------- blend ----------
final, changed, overridden, conflicts = {}, 0, [], []
for qn, a in base.items():
    rule_lab = a["section"]
    lab = merged.get(qn, rule_lab)
    verdict = "rules" if qn not in merged else "llm"

    if qn in merged and lab != "general":
        s_lab = score(qn, lab)
        # Only override when the LLM label has NO curated keyword support at all
        # and another sub-section is strongly supported by the question text.
        # (A looser rule was found to override correct LLM judgements.)
        if s_lab == 0:
            alt, s_alt = None, 0.0
            for sid in SECTION_TITLE:
                if sid == lab: continue
                s = score(qn, sid)
                if s > s_alt: alt, s_alt = sid, s
            if alt and text_hit(qn, alt) and s_alt >= 12:
                conflicts.append((qn, lab, alt, round(s_lab,1), round(s_alt,1)))
                lab = alt
                verdict = "llm+rule"
                overridden.append((qn, merged[qn], alt))

    if lab != rule_lab: changed += 1
    final[qn] = {"section": lab, "domain": int(SECTION_DOMAIN.get(lab, a["domain"])), "source": verdict}

# ---------- targeted corrections ----------
# Evaluation-criteria / TCB questions belong to 3.4 (security capabilities of
# information systems), not 3.2 (formal security models). Apply only when the
# question is not really about a named model.
MODEL_RX = re.compile(r"(bell-?\s?lapadula|biba|clark-?\s?wilson|brewer-?\s?nash|chinese wall|"
                      r"lattice|state machine|information flow|non-?interference|take-?grant|"
                      r"harrison|goguen|graham-?denning|lipner|simple security property|star property)",
                      re.I)
EVAL_RX = re.compile(r"(tcsec|orange book|common criteria|iso/?iec?\s?15408|protection profile|"
                     r"target of evaluation|reference monitor|trusted computing base|trusted path|"
                     r"trusted facility|covert channel|covert storage|covert timing|pseudo\s?flaw|"
                     r"assurance level|life-?cycle assurance|trusted distribution|security class|"
                     r"evaluation criteria|diacap|\beal\s?[1-7]\b|surreptitious)", re.I)
# questions that are really about control categories stay in 3.3
CONTROL_RX = re.compile(r"(preventive|preventative|detective|corrective|deterrent|recovery control|"
                        r"directive|compensating|compensating control|technical control|"
                        r"administrative control|physical control|logical control|control categor|"
                        r"control type|control function)", re.I)

fixed = []
for qn, v in final.items():
    if v["section"] in ("3.2", "3.3", "3.4"):
        text = " ".join([Q[qn]["q"]] + [o[1] for o in Q[qn]["o"]] + [Q[qn]["e"] or ""])
        if EVAL_RX.search(text) and not MODEL_RX.search(text) and not CONTROL_RX.search(text):
            if v["section"] != "3.4":
                fixed.append((qn, v["section"], "3.4"))
                v["section"] = "3.4"; v["domain"] = 3; v["source"] = "llm+rule"
print(f"evaluation-criteria corrections (-> 3.4): {len(fixed)}")
for qn, was, now in fixed[:20]:
    print(f"   Q{qn}: {was} -> {now}   {Q[qn]['q'][:80]}")

gen = sum(1 for v in final.values() if v["section"] == "general")
print(f"\nLLM labels applied : {len(merged)}")
print(f"labels changed     : {changed}")
print(f"rule overrides     : {len(overridden)}  (clear rule evidence contradicted the LLM label)")
for qn, was, now in overridden[:25]:
    print(f"   Q{qn}: {was} -> {now}  {Q[qn]['q'][:80]}")
print(f"final general      : {gen}/{len(final)} ({gen/len(final)*100:.1f}%)")

cnt = Counter(v["section"] for v in final.values())
lines = ["FINAL SUB-SECTION ASSIGNMENT", "=" * 82,
         f"assigned to a sub-section : {len(final)-gen}/{len(final)} ({(len(final)-gen)/len(final)*100:.1f}%)",
         f"other/general             : {gen}",
         f"LLM-adjudicated labels    : {len(merged)}",
         f"rule overrides            : {len(overridden)}", ""]
for did, rows in SECLIST.items():
    lines.append(f"--- Domain {did}: {DNAME[did]} ---")
    for sid, title in rows:
        lines.append(f"  {sid:<8}{cnt.get(sid,0):>6}   {title[:62]}")
    g = sum(1 for v in final.values() if v["section"]=="general" and v["domain"]==int(did))
    lines.append(f"  {'other':<8}{g:>6}")
open(OUT + r"\final_stats.txt", "w", encoding="utf-8").write("\n".join(lines))
json.dump({str(k): v for k, v in final.items()},
          open(OUT + r"\final_assignments.json", "w", encoding="utf-8"))
json.dump({"overrides": overridden, "conflicts": conflicts},
          open(OUT + r"\overrides.json", "w", encoding="utf-8"), indent=1)
print("\nwrote final_assignments.json, final_stats.txt, overrides.json")
print("\n".join(lines[:6]))
