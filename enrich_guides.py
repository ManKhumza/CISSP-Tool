"""
Build per-sub-section key-term glossaries with meanings.

Term sources per sub-section:
  * its curated 'strong' vocabulary (subsection_keywords.py)
  * the terms that actually occur most in its questions (from cissp-data.js)

Meaning source: definitional sentences mined from the two reference books
(OSG 10th ed + Exam Companion). High-precision extraction; terms whose
definition cannot be found confidently are listed without a meaning.

Writes _classify/guide_terms.json  ->  {section_id: {"terms":[{t,d}], "bare":[..]}}
"""
import json, os, re, sys
from collections import Counter

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
sys.path.insert(0, BASE)
from subsection_keywords import SUBSEC_TERMS
from dataio import load_bank, section_list
import defs

OUT = os.path.join(BASE, "_classify")
BOOKS = os.path.join(BASE, "_books")

DATA, Q, SEC, DNAME = load_bank()
SECLIST = section_list(DATA)

# questions per section, keyed by the STABLE source number: the portal renumbers
# questions 1..N in study order and keeps the original number in `sourceN`.
from dataio import questions_of
QBYN = {}
for _d in DATA["domains"]:
    for _q in questions_of(_d):
        QBYN[_q.get("sourceN", _q["n"])] = _q

FINAL = {int(k): v["section"] for k, v in json.load(
    open(OUT + r"\final_assignments.json", encoding="utf-8")).items()}
QS = {}
for n, s in FINAL.items():
    QS.setdefault(s, []).append(n)

# ---------------- term harvesting ----------------
STOP = set("""the a an and or but if in on at to of for by with from as is are was were be been
being it its this that these those he she they them we you your our us i me my not no so do does
did can could will would shall may might must have has had up down out off over under all any
some such than then there here when where why how who whom which what also use used using one
two three four five six seven eight nine ten first second third other another more most
following best least true false correct incorrect answer question which type called name not
except appropriate primarily main primary goal purpose reason implemented designed provides
provide ensure security system systems information data user users access control process
computer network application software policy risk management organization asset business service
services would could may based upon within between without through should must also""".split())
WORD = re.compile(r"[a-z][a-z'\-]{2,}")
BAD_TERM = re.compile(r"^(is|are|the|a|an|of|and|or|to|in|for|with|that|which|not|no|any|all|"
                      r"some|each|both|more|most|other|such|only|own|same|too|very|just|also|"
                      r"include|includes|included|example|examples|their|about|into|within|"
                      r"between|during|without|through|should|must|would|could|may|might|"
                      r"only|because|however|therefore|while|when|where|which|whose|them|"
                      r"there|these|those|this|have|has|had|been|being|from|upon|other)\b", re.I)

def norm_key(t):
    """Collapse hyphen/space variants so 'clark-wilson' and 'clark wilson' are one term."""
    return re.sub(r"[\s\-]+", " ", t.lower()).strip()

def section_terms(sid, limit_curated=45, limit_phrase=45, limit_acronym=18):
    """Candidate terms: the section's curated vocabulary, plus meaningful PHRASES and
    acronyms mined from its questions. Single generic words are deliberately not mined —
    they produced entries like 'reducing' or 'processing' with meaningless definitions."""
    curated = [t for t in SUBSEC_TERMS.get(sid, {}).get("strong", [])
               if len(t) >= 3 and not BAD_TERM.match(t)]
    curated = sorted(curated, key=lambda t: (-len(t.split()), t))[:limit_curated]

    phrases, acronyms = Counter(), Counter()
    for n in QS.get(sid, []):
        q = QBYN.get(n)
        if not q:
            continue
        raw = q["q"] + " " + " ".join(o[1] for o in q["o"]) + " " + (q["e"] or "")
        low = raw.lower()
        toks = WORD.findall(low)
        for i in range(len(toks) - 1):
            a, b = toks[i], toks[i + 1]
            if a in STOP or b in STOP or len(a) < 4 or len(b) < 4:
                continue
            phrases[a + " " + b] += 1
        for m in re.finditer(r"\b([A-Z][A-Z0-9]{1,6})\b", raw):
            acronyms[m.group(1)] += 1

    mined = [p for p, c in phrases.most_common(limit_phrase * 3) if c >= 3][:limit_phrase]
    acros = [a for a, c in acronyms.most_common(limit_acronym * 3)
             if c >= 3 and a.lower() not in STOP][:limit_acronym]

    seen, ordered = set(), []
    for t in curated + mined + acros:
        k = norm_key(t)
        if len(k) < 4 or k in seen or BAD_TERM.match(k):
            continue
        seen.add(k)
        ordered.append(t)
    return ordered, set(norm_key(x) for x in curated)

# ---------------- definition lookup with cache ----------------
CACHE_PATH = os.path.join(OUT, "def_cache.json")
CACHE = json.load(open(CACHE_PATH, encoding="utf-8")) if os.path.exists(CACHE_PATH) else {}

def get_definition(term, books):
    key = term.lower().strip()
    if key in CACHE:
        return CACHE[key]
    best, best_sc, kind = None, 0.0, None
    for book in books:
        d, sc = defs.find_definition(book, term)
        if sc > best_sc:
            best, best_sc, kind = d, sc, "def"
    if not best:
        for book in books:
            d, sc = defs.find_context(book, term)
            if sc > best_sc:
                best, best_sc, kind = d, sc, "ctx"
    res = {"d": best, "sc": round(best_sc, 1), "k": kind}
    CACHE[key] = res
    return res

def main():
    books = [defs.Book(n) for n in ("osg10.txt", "companion.txt")
             if os.path.exists(os.path.join(BOOKS, n))]
    print("sources:", [(b.name, len(b.sentences)) for b in books])

    # third source: the question bank's own explanations (per section and globally),
    # so every term can be explained in the words of the material being studied
    sec_books, all_expl = {}, []
    for sid, qns in QS.items():
        parts = []
        for n in qns:
            q = QBYN.get(n)
            if not q:
                continue
            txt = (q.get("e") or "")
            if txt:
                parts.append(txt)
                all_expl.append(txt)
        if parts:
            sec_books[sid] = defs.Book("bank:" + sid, raw=" ".join(parts))
    bank_book = defs.Book("bank:all", raw=" ".join(all_expl)) if all_expl else None
    print(f"bank sources: {len(sec_books)} section books, global bank "
          f"{len(bank_book.sentences) if bank_book else 0} sentences")

    def lookup(term, sid):
        # 1) strict definitions, reference books first then the question bank
        for src in (books[:1], books[1:2],
                    ([sec_books[sid]] if sid in sec_books else []),
                    ([bank_book] if bank_book else [])):
            for b in src:
                d, sc = defs.find_definition(b, term, max_len=360)
                is_bank = b.name.startswith("bank:")
                # the question bank's own prose is sometimes a taxonomy dump; demand more
                if d and sc >= (20 if is_bank else 14) and len(d) <= 340:
                    return {"d": d, "sc": round(sc, 1), "k": "def", "src": b.name}
        # 2) meaning in context
        for src in (books[:1], books[1:2],
                    ([sec_books[sid]] if sid in sec_books else []),
                    ([bank_book] if bank_book else [])):
            for b in src:
                d, sc = defs.find_context(b, term, max_len=300)
                is_bank = b.name.startswith("bank:")
                if d and sc >= (11 if is_bank else 9):
                    return {"d": d, "sc": round(sc, 1), "k": "ctx", "src": b.name}
        return {"d": None, "sc": 0.0, "k": None, "src": None}

    def cached(term, sid):
        key = term.lower().strip() + "|" + sid
        if key not in CACHE:
            CACHE[key] = lookup(term, sid)
        return CACHE[key]

    result, stats = {}, []
    for did, rows in SECLIST.items():
        for sid, title in rows:
            terms, curated_set = section_terms(sid)
            defined, bare = [], []
            for t in terms:
                r = cached(t, sid)
                if r["d"]:
                    defined.append({"t": t, "d": r["d"], "s": r["sc"], "k": r["k"],
                                    "src": r["src"], "c": t.lower() in curated_set})
                else:
                    bare.append(t)
            defined.sort(key=lambda x: (not x["c"], x["k"] != "def", -x["s"]))
            ndef = sum(1 for x in defined if x["k"] == "def")
            defined = defined[:34]
            result[sid] = {"terms": defined, "bare": bare[:26], "ndef": ndef}
            stats.append((sid, len(terms), len(defined), len(bare), ndef))
            json.dump(CACHE, open(CACHE_PATH, "w", encoding="utf-8"), ensure_ascii=False)

    json.dump(result, open(os.path.join(OUT, "guide_terms.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)
    tot_t = sum(s[1] for s in stats)
    tot_d = sum(s[2] for s in stats)
    tot_strict = sum(s[4] for s in stats)
    print(f"\nsections: {len(stats)}  candidates: {tot_t}  with a meaning: {tot_d} "
          f"({tot_d/max(tot_t,1)*100:.0f}%)  of which strict definitions: {tot_strict}")
    thin = [s for s in stats if s[2] < 8]
    print(f"sections with fewer than 8 meanings: {len(thin)}")
    for sid, n, d, b, nd in sorted(thin, key=lambda x: x[2])[:15]:
        print(f"   {sid}: {d} meanings ({nd} strict) / {n} candidates")
    print("\nwrote _classify/guide_terms.json")

if __name__ == "__main__":
    main()
