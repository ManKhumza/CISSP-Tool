"""
Sub-section classification v4 - within-domain + CONSERVATIVE cross-domain repair.

The existing domain grouping contains misfiled questions (honeypot / RAID / cabling
questions sitting in Domain 1). Rather than re-deriving all domains (which scrambled
~900 questions), a question only moves to another domain when the evidence is
overwhelming:
    * it has no evidence at all inside its current domain, or
    * the best section elsewhere scores >= 3x the best section inside the domain
Everything else keeps its current domain and is assigned a sub-section within it.
"""
import json, os, re, sys
from collections import Counter, defaultdict

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
sys.path.insert(0, BASE)
from subsection_keywords import SUBSEC_TERMS

OUT = os.path.join(BASE, "_classify")
os.makedirs(OUT, exist_ok=True)

src = open(os.path.join(BASE, "cissp-data.js"), encoding="utf-8-sig").read()
src = src[len("window.CISSP_DATA = "):].rstrip().rstrip(";")
DATA = json.loads(src)

SECTION_TITLES, SECTION_DOMAIN, DOMAIN_NAME, DOMAIN_ORDER = {}, {}, {}, []
for d in DATA["domains"]:
    DOMAIN_ORDER.append(str(d["id"]))
    DOMAIN_NAME[str(d["id"])] = d["name"]
    for s in d["sections"]:
        SECTION_TITLES[s["id"]] = s["title"]
        SECTION_DOMAIN[s["id"]] = str(d["id"])
ALL_SECTIONS = list(SECTION_TITLES)
SECTIONS_OF = {did: [s for s in ALL_SECTIONS if SECTION_DOMAIN[s] == did] for did in DOMAIN_ORDER}

def norm(s):
    return re.sub(r"\s+", " ", (s or "").lower())

WORD_RX = re.compile(r"[a-z][a-z'\-]*|\d+(?:\.\d+)?")

def features(text):
    ws = WORD_RX.findall(text)
    return Counter(ws), Counter((ws[i] + " " + ws[i + 1]) for i in range(len(ws) - 1))

def term_kind(p):
    toks = WORD_RX.findall(p)
    if toks == [p]:
        return "w1"
    if len(toks) == 2 and (toks[0] + " " + toks[1]) == p:
        return "w2"
    return "rx"

def build_terms(pairs):
    w1, w2, rx = {}, {}, []
    for phrase, weight in pairs:
        k = term_kind(phrase)
        if k == "w1":
            w1[phrase] = max(w1.get(phrase, 0), weight)
        elif k == "w2":
            w2[phrase] = max(w2.get(phrase, 0), weight)
        else:
            rx.append((phrase, weight,
                       re.compile(r"(?<![a-z0-9])" + re.escape(phrase).replace(r"\ ", r"\s+") + r"(?![a-z0-9])")))
    return {"w1": w1, "w2": w2, "rx": rx}

def as_pairs(t, dw):
    return list(t.items()) if isinstance(t, dict) else [(p, dw) for p in t]

STRONG = {s: build_terms(as_pairs(SUBSEC_TERMS.get(s, {}).get("strong", []), 7)) for s in ALL_SECTIONS}
WEAK = {s: build_terms(as_pairs(SUBSEC_TERMS.get(s, {}).get("weak", []), 2)) for s in ALL_SECTIONS}

def match(tm, c1, c2, text):
    out = []
    for phrase, w in tm["w1"].items():
        n = c1.get(phrase, 0)
        if n:
            out.append((phrase, w, n))
    for phrase, w in tm["w2"].items():
        n = c2.get(phrase, 0)
        if n:
            out.append((phrase, w, n))
    for phrase, w, rx in tm["rx"]:
        n = len(rx.findall(text))
        if n:
            out.append((phrase, w, n))
    return out

QUESTIONS = []
for d in DATA["domains"]:
    for q in d["questions"]:
        t, o, e = norm(q["q"]), norm(" ".join(x[1] for x in q["o"])), norm(q["e"] or "")
        QUESTIONS.append({"n": q["n"], "old_domain": str(d["id"]), "q": q["q"],
                          "t": t, "o": o, "e": e,
                          "t1": features(t)[0], "t2": features(t)[1],
                          "o1": features(o)[0], "o2": features(o)[1],
                          "e1": features(e)[0], "e2": features(e)[1]})
QBYN = {q["n"]: q for q in QUESTIONS}
MULT = {"t": 3.0, "o": 1.0, "e": 0.25}

def score_base(q, section):
    tot, vis, exp_only, detail = 0.0, 0, 0, []
    for field in ("t", "o", "e"):
        c1, c2 = q[field + "1"], q[field + "2"]
        for phrase, w, n in match(STRONG[section], c1, c2, q[field]):
            tot += w * MULT[field] * min(n, 2 if field == "t" else 1)
            if field in ("t", "o"):
                vis += 1
            else:
                exp_only += 1
            detail.append((phrase, w, field))
    return tot, vis, exp_only, detail

def curated_text_hit(q, section):
    """True when a curated (hand-written) strong term appears in the question text."""
    return bool(match(STRONG[section], q["t1"], q["t2"], q["t"]))

MINED = {}

def score_full(q, section):
    tot, vis, exp_only, detail = score_base(q, section)
    m = MINED.get(section)
    if m:
        for field in ("t", "o", "e"):
            c1, c2 = q[field + "1"], q[field + "2"]
            for phrase, w, n in match(m, c1, c2, q[field]):
                tot += w * MULT[field] * min(n, 2 if field == "t" else 1)
                if field in ("t", "o"):
                    vis += 1
                else:
                    exp_only += 1
                detail.append((phrase, w, field))
    if tot > 0:
        for field in ("t", "o", "e"):
            c1, c2 = q[field + "1"], q[field + "2"]
            for phrase, w, n in match(WEAK[section], c1, c2, q[field]):
                tot += w * MULT[field] * min(n, 2 if field == "t" else 1)
                detail.append((phrase, w, field))
    return tot, vis, exp_only, detail

# ---- stage A/B: seeds + mined terms (as v3) ----
seeds = defaultdict(list)
for q in QUESTIONS:
    scored = []
    for s in ALL_SECTIONS:
        tot, vis, exp_only, _ = score_base(q, s)
        if tot > 0 and (vis >= 1 or exp_only >= 2):
            scored.append((s, tot))
    scored.sort(key=lambda x: -x[1])
    if scored:
        best, second = scored[0], (scored[1][1] if len(scored) > 1 else 0.0)
        if best[1] >= 14 and best[1] >= 2.0 * max(second, 1.0):
            seeds[best[0]].append(q["n"])

STOP = set("""the a an and or but if in on at to of for by with from as is are was were be been
being it its this that these those he she they them we you your our us i me my not no so do does
did can could will would shall should may might must have has had up down out off over under all
any some such than then there here when where why how who whom which what also use used using
one two three four five six seven eight nine ten first second third other another more most
following best least true false correct incorrect answer question which type called name not
except appropriate primarily main primary goal purpose reason implemented designed provides
provide ensure security system systems information data user users access control process
computer network application software policy risk management organization asset business service
services would could may based upon within between during without through""".split())

def doc_terms(q):
    toks = WORD_RX.findall(q["t"] + " " + q["o"] + " " + q["e"])
    uni = {w for w in toks if w not in STOP and len(w) >= 4}
    bi = {toks[i] + " " + toks[i + 1] for i in range(len(toks) - 1)
          if toks[i] not in STOP and toks[i + 1] not in STOP
          and len(toks[i]) >= 4 and len(toks[i + 1]) >= 4}
    return uni | bi

df = defaultdict(Counter)
for s, qns in seeds.items():
    for qn in qns:
        for term in doc_terms(QBYN[qn]):
            df[s][term] += 1

for s in list(df.keys()):
    cnt = df[s]
    dom = SECTION_DOMAIN[s]
    sib = [x for x in SECTIONS_OF[dom] if x != s]
    other = [x for x in ALL_SECTIONS if SECTION_DOMAIN[x] != dom]
    picked = []
    for term, c in cnt.most_common(600):
        if c < 4:
            continue
        e_sib = sum(df.get(x, Counter()).get(term, 0) for x in sib)
        e_oth = sum(df.get(x, Counter()).get(term, 0) for x in other)
        if c >= 3 * (e_sib + 1) and c >= 2 * (e_oth + 1):
            picked.append(term)
        if len(picked) >= 60:
            break
    MINED[s] = build_terms([(p, 5) for p in picked])

print(f"seeds {sum(len(v) for v in seeds.values())} | mined "
      f"{sum(len(v['w1']) + len(v['w2']) + len(v['rx']) for v in MINED.values())} terms")

# ---- stage C: within-domain + conservative repair ----
assign = {}
moved = []
for q in QUESTIONS:
    dom = q["old_domain"]
    in_rows = []
    for s in SECTIONS_OF[dom]:
        tot, vis, exp_only, detail = score_full(q, s)
        if tot > 0 and (vis >= 1 or exp_only >= 2):
            in_rows.append((s, tot, vis, exp_only, detail))
    in_rows.sort(key=lambda r: (-r[1], r[0]))

    g_rows = []
    for s in ALL_SECTIONS:
        tot, vis, exp_only, detail = score_full(q, s)
        if tot > 0 and (vis >= 1 or exp_only >= 2):
            g_rows.append((s, tot, vis, exp_only, detail))
    g_rows.sort(key=lambda r: (-r[1], r[0]))

    in_best = in_rows[0] if in_rows else None
    g_best = g_rows[0] if g_rows else None

    chosen = None
    if g_best is not None and SECTION_DOMAIN[g_best[0]] != dom:
        in_score = in_best[1] if in_best else 0.0
        g_vis = g_best[2]
        # move only when the question has NO evidence at all inside its current
        # domain and the section found elsewhere is backed by visible evidence
        if in_score == 0.0 and g_vis >= 1 and g_best[1] >= 7 \
                and curated_text_hit(q, g_best[0]):
            chosen = g_best
            moved.append((q["n"], dom, SECTION_DOMAIN[g_best[0]], round(in_score, 1), round(g_best[1], 1)))
    if chosen is None:
        chosen = in_best

    if chosen is None:
        assign[q["n"]] = {"section": "general", "domain": int(dom), "score": 0.0,
                          "margin": 0.0, "detail": []}
        continue

    s, tot, vis, exp_only, detail = chosen
    second = next((r[1] for r in (in_rows if chosen in in_rows else g_rows) if r[0] != s), 0.0)
    top = sorted(detail, key=lambda d: -(d[1] * MULT[d[2]]))[:6]
    assign[q["n"]] = {
        "section": s, "domain": int(SECTION_DOMAIN[s]), "score": round(tot, 1),
        "margin": round(tot - second, 1),
        "detail": [{"p": p, "w": w, "f": f} for p, w, f in top],
    }

# ---- report ----
sec_counts = Counter(v["section"] for v in assign.values())
gen_by_dom = Counter(v["domain"] for v in assign.values() if v["section"] == "general")
new_by_dom = Counter(v["domain"] for v in assign.values() if v["section"] != "general")
old_by_dom = Counter(int(q["old_domain"]) for q in QUESTIONS)
tot_q = len(QUESTIONS)
gen_total = sum(gen_by_dom.values())

lines = ["SUB-SECTION CLASSIFICATION (v4: within-domain + conservative repair)", "=" * 88]
lines.append(f"assigned to a sub-section : {tot_q - gen_total}/{tot_q} ({(tot_q-gen_total)/tot_q*100:.1f}%)")
lines.append(f"general bucket            : {gen_total} ({gen_total/tot_q*100:.1f}%)")
lines.append(f"questions moved domain    : {len(moved)}")
lines.append("")
lines.append(f"{'DOM':<5}{'OLD':>6}{'NEW':>6}{'GEN':>7}   NAME")
for did in DOMAIN_ORDER:
    lines.append(f"{did:<5}{old_by_dom.get(int(did),0):>6}{new_by_dom.get(int(did),0):>6}"
                 f"{gen_by_dom.get(int(did),0):>7}   {DOMAIN_NAME[did][:52]}")
lines.append("")
for did in DOMAIN_ORDER:
    lines.append(f"--- Domain {did}: {DOMAIN_NAME[did]} ---")
    for s in SECTIONS_OF[did]:
        lines.append(f"  {s:<8}{sec_counts.get(s,0):>6}   {SECTION_TITLES[s][:62]}")
    lines.append(f"  {'general':<8}{gen_by_dom.get(int(did),0):>6}")
lines.append("")
lines.append(f"--- sample of moved questions ({min(len(moved),80)} of {len(moved)}) ---")
for qn, od, nd, isc, gsc in moved[:80]:
    lines.append(f"  Q{qn}: D{od} -> D{nd} (in {isc} vs global {gsc}) {QBYN[qn]['q'][:95]}")
open(os.path.join(OUT, "stats.txt"), "w", encoding="utf-8").write("\n".join(lines))

rev = []
for did in DOMAIN_ORDER:
    rev.append(f"\n{'#'*88}\n# DOMAIN {did}: {DOMAIN_NAME[did]}\n{'#'*88}")
    for s in SECTIONS_OF[did]:
        qs = [q for q in QUESTIONS if assign[q["n"]]["section"] == s]
        rev.append(f"\n===== {s}  {SECTION_TITLES[s]}   [{len(qs)} questions] =====")
        picks = (qs[:5] + qs[len(qs)//2:len(qs)//2 + 5] + qs[-5:]) if len(qs) > 15 else qs[:15]
        seen = set()
        for q in picks:
            if q["n"] in seen:
                continue
            seen.add(q["n"])
            a = assign[q["n"]]
            rev.append(f"  Q{q['n']} [s{a['score']} m{a['margin']}] {q['q'][:130]}")
            if a["detail"]:
                rev.append("        <- " + ", ".join(h["p"] for h in a["detail"][:5]))
    gen = sorted(k for k, v in assign.items() if v["section"] == "general" and v["domain"] == int(did))
    if gen:
        rev.append(f"\n----- general ({len(gen)}) -----")
        for qn in gen[:20]:
            rev.append(f"  Q{qn} {QBYN[qn]['q'][:130]}")
open(os.path.join(OUT, "review.txt"), "w", encoding="utf-8").write("\n".join(rev))
json.dump(assign, open(os.path.join(OUT, "assignments.json"), "w", encoding="utf-8"))
json.dump({"mined": {k: (list(v["w1"]) + list(v["w2"]) + [p for p, _, _ in v["rx"]])
                     for k, v in MINED.items()},
           "moved": moved},
          open(os.path.join(OUT, "mined_terms.json"), "w", encoding="utf-8"), indent=1)

print("\n".join(lines[:16]))
