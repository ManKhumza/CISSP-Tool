"""
Find text-extraction / repair artefacts in the question bank.

Reports, with context, every suspicious token so the repair rules can be
reviewed rather than guessed.

Run:  python detect_text_defects.py            -> writes _text_defects.txt
"""
import json, re, sys, os
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
sys.path.insert(0, BASE)
from dataio import load_data, questions_of

# ---------- vocabulary from the two licensed study guides ----------
VOCAB = Counter()
for name in ("osg10.txt", "companion.txt"):
    p = os.path.join(BASE, "_books", name)
    if not os.path.exists(p):
        continue
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            for w in re.findall(r"[A-Za-z][A-Za-z'\-]+", line.lower()):
                VOCAB[w] += 1
print(f"vocabulary: {len(VOCAB):,} distinct words from the study guides")

DATA = load_data()
questions = []
for d in DATA["domains"]:
    for q in questions_of(d):
        questions.append(q)
print(f"questions: {len(questions):,}")

def fields(q):
    yield q.get("q", ""), "q"
    for o in q.get("o") or []:
        yield o[1], "opt" + str(o[0])
    yield q.get("e", ""), "e"

RARE = 12          # a "fragment" appears at most this often in 4 MB of prose
COMMON = 200       # the partner word must be this common
TOKEN = re.compile(r"[A-Za-z][A-Za-z'\-]*")

joins, splits, spacing, junk = [], [], [], []

for q in questions:
    for text, field in fields(q):
        if not text:
            continue
        toks = list(TOKEN.finditer(text))
        for i in range(len(toks) - 1):
            a, b = toks[i], toks[i + 1]
            # only look at tokens that are actually adjacent (single space)
            if text[a.end():b.start()] != " ":
                continue
            A, B = a.group(), b.group()
            la, lb = A.lower(), B.lower()
            fa, fb = VOCAB.get(la, 0), VOCAB.get(lb, 0)
            if min(len(A), len(B)) > 9:
                continue
            joined = (la + lb)
            fj = VOCAB.get(joined, 0)
            if fj >= 30 and (fa <= RARE or fb <= RARE) and not (fa > COMMON and fb > COMMON):
                joins.append((q["n"], field, A + " " + B, joined, fj, fa, fb,
                              text[max(0, a.start() - 40):b.end() + 40]))
        # a token that is not a word but splits into two common words
        for t in toks:
            w = t.group().lower()
            if VOCAB.get(w, 0) > 2 or len(w) < 5 or len(w) > 9:
                continue
            for k in range(2, len(w) - 1):
                x, y = w[:k], w[k:]
                if VOCAB.get(x, 0) >= COMMON and VOCAB.get(y, 0) >= COMMON and len(x) >= 2 and len(y) >= 2:
                    splits.append((q["n"], field, t.group(), x + " " + y,
                                   VOCAB[x], VOCAB[y],
                                   text[max(0, t.start() - 40):t.end() + 40]))
                    break
        for m in re.finditer(r"\w\?\(|\w\)\w|\s[,.;:]|\s{2,}|'\s?>|\w'\s?>\w", text):
            spacing.append((q["n"], field, repr(m.group()),
                            text[max(0, m.start() - 40):m.end() + 40]))
        for m in re.finditer(r"[<>|]{1,3}\s?[A-Za-z]{2,}|\[[A-Za-z ]{0,3}\]|\bpage \d+\b", text):
            junk.append((q["n"], field, repr(m.group()),
                         text[max(0, m.start() - 40):m.end() + 40]))

def dump(title, rows, fh, limit=400):
    fh.write("\n" + "=" * 100 + f"\n{title}: {len(rows)} candidates\n" + "=" * 100 + "\n")
    for r in rows[:limit]:
        fh.write("  Q%-5s %-6s %-22s %s\n" % (r[0], r[1], str(r[2]), str(r[-1]).replace("\n", " ")))
    if len(rows) > limit:
        fh.write(f"  ... {len(rows) - limit} more\n")

out = os.path.join(BASE, "_text_defects.txt")
with open(out, "w", encoding="utf-8") as fh:
    dump("POSSIBLE BROKEN WORDS (should be one word)", joins, fh)
    dump("POSSIBLE MISSING SPACES (rare token = two common words)", splits, fh)
    dump("SPACING / PUNCTUATION ARTEFACTS", spacing, fh)
    dump("MARKUP-LIKE JUNK", junk, fh)

print(f"broken-word suspects : {len(joins)}")
print(f"missing-space suspects: {len(splits)}")
print(f"spacing artefacts    : {len(spacing)}")
print(f"markup junk          : {len(junk)}")
print(f"-> {out}")
