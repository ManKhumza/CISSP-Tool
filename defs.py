"""
Extract 'term = definition' pairs from the OSG body text.

The book defines terms inline ("The trusted computing base (TCB) is the combination
of ..."). For each requested term we score candidate sentences by definitional cues
and position, then keep the best one or two.

Modes:
  python defs.py test "term1" "term2" ...   -> show candidate definitions
  python defs.py build                      -> definitions for all guide terms
"""
import json, os, re, sys
from collections import defaultdict

try:                                   # avoid cp1252 console crashes on ﬂ/ﬁ ligatures
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
BOOKS = os.path.join(BASE, "_books")

def load_text(name="osg10.txt"):
    t = open(os.path.join(BOOKS, name), encoding="utf-8").read()
    t = t.replace("\ufb01", "fi").replace("\ufb02", "fl")     # ligatures
    t = t.replace("\u2019", "'").replace("\u2018", "'")
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2013", "-").replace("\u2014", "-")
    t = re.sub(r"<<<PAGE \d+>>>", " ", t)
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)              # de-hyphenate line breaks
    t = re.sub(r"\s+", " ", t)
    return t

IDX_WORD = re.compile(r"[a-z][a-z0-9'\-]{2,}")
IDX_STOP = set("""the and for with that this from are was were has have had not but you your
which their they them there these those when where what will would could should about into over
under between during without through also more most other such only same than then there here
security system systems information data using used use one two three four five six seven eight
nine ten first second third may might must can able include includes including example examples
""".split())

class Book:
    """Sentence index: lookup only the sentences that can contain a given term.
    Accepts either a file name inside _books or raw text."""
    def __init__(self, name, raw=None):
        self.name = name
        self.text = raw if raw is not None else load_text(name)
        self.sentences = sentences(self.text)
        self.index = defaultdict(list)
        for i, s in enumerate(self.sentences):
            for w in set(IDX_WORD.findall(s.lower())) - IDX_STOP:
                self.index[w].append(i)
        self.index = {k: v for k, v in self.index.items() if len(v) <= 4000}

    def candidates(self, term):
        """Sentences containing the term. We scan the postings of the RAREST word of
        the term (a superset) and let the caller's regex confirm the full phrase —
        intersecting every word failed for phrases containing a very common word."""
        words = [w for w in IDX_WORD.findall(term.lower()) if w not in IDX_STOP]
        if not words:
            words = IDX_WORD.findall(term.lower())
        if not words:
            return []
        avail = [(len(self.index[w]), w) for w in words if w in self.index]
        if not avail:
            return []
        avail.sort()
        _, best = avail[0]
        return [self.sentences[i] for i in self.index[best]]

# definitional cue patterns, strongest first
CUES = [
    (r"\bis the process of\b", 10), (r"\bis defined as\b", 10), (r"\bis the practice of\b", 10),
    (r"\bis known as\b", 8), (r"\brefers to\b", 8), (r"\bis the act of\b", 8),
    (r"\bis the combination of\b", 9), (r"\bis a type of\b", 6), (r"\bis a method\b", 7),
    (r"\bis an? approach\b", 7), (r"\bis a protocol\b", 7), (r"\bis a technique\b", 7),
    (r"\bis a term\b", 6), (r"\bis used to\b", 6), (r"\bconsists of\b", 7),
    (r"\bmeans\b", 6), (r"\bis an? \b", 5), (r"\bare the\b", 5), (r"\bis the\b", 5),
    (r"\bdescribes\b", 4), (r"\bprovides\b", 3), (r"\bincludes\b", 3),
]
# sentences that are cross-references or filler rather than definitions
CROSS_RX = re.compile(r"(chapter|discussed|discuss |see section|we will|you will|"
                      r"in this book|earlier|later in|as noted|table \d|figure \d|"
                      r"is covered|are covered|examination|exam tip|remember that)", re.I)

def sentences(text):
    return re.split(r"(?<=[.!?])\s+(?=[A-Z(])", text)

def acronym_hint(term):
    words = re.findall(r"[A-Za-z]+", term)
    skip = {"of", "and", "the", "in", "for", "to", "a", "an", "with"}
    return "".join(w[0].upper() for w in words if w.lower() not in skip)

def strip_heading(s):
    """The extraction glues section headings onto the following sentence:
    'Risk Deterrence Risk deterrence is the process of...' -> drop the duplicate head."""
    words = s.split()
    for n in range(1, 6):
        if len(words) >= 2 * n:
            head = re.sub(r"[^a-z0-9]", "", " ".join(words[:n]).lower())
            nxt = re.sub(r"[^a-z0-9]", "", " ".join(words[n:2 * n]).lower())
            if head and head == nxt and len(head) >= 3:
                return " ".join(words[n:])
    return s

LEAD_RX = re.compile(r"^(?:a|an|the|in|for|of|and|or|but|all|some|these|those|each|"
                     r"typically|generally|usually|often|finally|however|therefore)?$", re.I)

def looks_like_subject(s, m):
    """The term must start the sentence or follow a short determiner/lead-in,
    so that 'residual risk is known as...' does not define 'risk'."""
    before = s[:m.start()].strip().strip(",;:")
    if before == "":
        return True
    return bool(LEAD_RX.match(before))

CUE_VERB_RX = re.compile(
    r"^(?:\s*\([A-Za-z]{2,6}\))?\s*(?:is|are|was|were|be|been|refers?|means?|describ\w+|"
    r"consists?|represent\w*|involv\w+|includ\w+|provid\w+|us\w+|allow\w*|ensur\w+|"
    r"occur\w*|happen\w*|stat\w+|requir\w+|dictat\w+|defin\w+|denot\w+|signif\w+|"
    r"encompass\w*|work\w*|gather\w*|apply|applies|serv\w+|offer\w*|enabl\w+|protect\w*|"
    r"contain\w*|cover\w*|focus\w*|aim\w*|help\w*|guarantee\w*|prevent\w*|limit\w*)\b", re.I)

# front-matter / figure / TOC fragments and other non-prose junk
JUNK_RX = re.compile(r"(domain description chapter|objective map|figure \d|table \d|"
                     r"chapter \d+:|^\d+\.|^\W*[A-Z][a-z]+ \d+\.$|"
                     r"^\s*(contents|index|appendix)\b|www\.|\.com\b)", re.I)
# practice-test option text: answers include deliberate distractors, which must never
# be mined as definitions ("A security model is used to host one or more operating
# systems within the memory of a single host computer" is option D of a question)
OPTION_RX = re.compile(r"(?:^|\s)[A-D]\.\s")
OPTION_START_RX = re.compile(r"^(?:\d+\.\s*)?[A-D]\.\s")

def is_option_text(s):
    if OPTION_START_RX.match(s):
        return True
    if len(OPTION_RX.findall(s)) >= 2:
        return True
    # answer-section numbering leaks into the sentence ("... host OS. 13.")
    if re.search(r"\s\d{1,4}\.$", s):
        return True
    return False

def in_definition_position(s, m):
    tail = s[m.end():m.end() + 40]
    return bool(CUE_VERB_RX.match(tail))

def near_verb(s, m, window=4):
    """The term is followed by a definitional verb within `window` words."""
    tail = s[m.end():].split()[:window]
    return bool(tail) and bool(CUE_VERB_RX.match(" " + " ".join(tail[1:3]) if False else
                                                 " " + " ".join(tail[1:]) if len(tail) > 1 else ""))

def score_sentence(s, term_rx, cue_weight, strict=False):
    score = cue_weight
    m = term_rx.search(s)
    if m:
        pos = m.start() / max(len(s), 1)
        score += 6 * (1.0 - pos)
        subj = looks_like_subject(s, m)
        pos_ok = in_definition_position(s, m)
        if subj and pos_ok:
            score += 14
        elif pos_ok:
            score += 3
        else:
            score -= 8
    if len(s) < 55:
        score -= 5
    if len(s) > 480:
        score -= (len(s) - 480) / 60.0
    if CROSS_RX.search(s):
        score -= 9
    if re.search(r"\b(opposite of|unlike|in contrast|similar to|as opposed to)\b", s, re.I):
        score -= 12
    if s.count(":") > 3 or "  " in s:
        score -= 2
    return score

def variants_of(term):
    """Singular/plural, hyphen/space and acronym-friendly variants of a term."""
    out = [term]
    if term.lower().endswith("s"):
        out.append(term[:-1])
    else:
        out.append(term + "s")
    if "-" in term:
        out.append(term.replace("-", " "))
    else:
        out.append(term.replace(" ", "-"))
    m = re.match(r"^(.*?)\s+(model|attack|system|method|process|technique|protocol|control)$", term, re.I)
    if m:
        out.append(m.group(1))
    seen, uniq = set(), []
    for v in out:
        k = v.lower().strip()
        if k and k not in seen:
            seen.add(k)
            uniq.append(v)
    return uniq

_VAR_CACHE = {}

def compiled_variants(term):
    """Cache the (variant, regex, acronym-regex) tuples — regex compilation is the
    hot spot when scanning thousands of terms against several books."""
    if term in _VAR_CACHE:
        return _VAR_CACHE[term]
    out = []
    for v in variants_of(term):
        tnorm = v.lower().strip()
        pat = r"(?<![a-z0-9])" + re.escape(tnorm).replace(r"\ ", r"\s+") + r"(?![a-z0-9])"
        try:
            rx = re.compile(pat, re.I)
        except re.error:
            continue
        acro = acronym_hint(v)
        arx = re.compile(r"\(%s\)" % re.escape(acro), re.I) if len(acro) >= 3 else None
        out.append((v, rx, arx))
    _VAR_CACHE[term] = out
    return out

def find_definition(text, term, max_len=420, debug=False):
    """Return (definition, score) for the best-matching sentence.
    `text` may be a Book (fast, indexed) or a raw string."""
    sentences_iter = text.candidates(term) if isinstance(text, Book) else sentences(text)
    best = (None, 0.0)
    seen = set()
    for vi, (v, term_rx, acro_rx) in enumerate(compiled_variants(term)):
        for s in sentences_iter:
            if s in seen:
                continue
            if not term_rx.search(s):
                if not (acro_rx and acro_rx.search(s)):
                    continue
            seen.add(s)
            clean = strip_heading(s.strip())
            if is_option_text(clean):
                continue
            total = 0.0
            for cue, w in CUES:
                if re.search(cue, clean, re.I):
                    total += w
                    break
            sc = score_sentence(clean, term_rx, total)
            if vi > 0:
                sc -= 1.5 * min(vi, 3)             # prefer the exact term form
            if sc > best[1]:
                best = (clean, sc)
    if best[0] and best[1] >= 12:
        d = best[0]
        if len(d) > max_len:
            d = d[:max_len].rsplit(" ", 1)[0] + "…"
        return d, best[1]
    return None, 0.0

IMPERATIVE_RX = re.compile(r"^(ensure|remember|always|never|do not|don't|avoid|note that|"
                           r"consider|be sure|keep in mind|make sure|verify|check)\b", re.I)
EXAM_RX = re.compile(r"(exam tip|on the exam|test question|practice exam|which of the following|"
                     r"question \d|correct answer)", re.I)

def find_context(book, term, max_len=320):
    """Fallback 'meaning in context': the most definitional book sentence about the
    term, even when the term is not the grammatical subject."""
    best, best_sc = None, -99.0
    seen = set()
    for vi, (v, rx, _arx) in enumerate(compiled_variants(term)[:3]):
        for s in book.candidates(v):
            if s in seen:
                continue
            seen.add(s)
            clean = strip_heading(s.strip())
            if len(clean) < 60 or len(clean) > 420:
                continue
            if clean.endswith("?") or JUNK_RX.search(clean) or is_option_text(clean):
                continue
            if CROSS_RX.search(clean):          # cross-references are not meanings
                continue
            if IMPERATIVE_RX.match(clean) or EXAM_RX.search(clean):
                continue
            m = rx.search(clean)
            if not m:
                continue
            sc = 0.0
            if looks_like_subject(clean, m):
                sc += 6
            if in_definition_position(clean, m):
                sc += 6
            elif near_verb(clean, m):
                sc += 3
            if any(re.search(c, clean, re.I) for c, _ in CUES):
                sc += 3
            sc += 4 * (1.0 - m.start() / max(len(clean), 1))
            if len(clean) > 260:
                sc -= (len(clean) - 260) / 90.0
            if re.search(r"\b(opposite of|unlike|as opposed to)\b", clean, re.I):
                sc -= 6
            if vi > 0:
                sc -= 1.0 * vi
            if sc > best_sc:
                best, best_sc = clean, sc
    if best and best_sc >= 7:
        d = best
        if len(d) > max_len:
            d = d[:max_len].rsplit(" ", 1)[0] + "…"
        return d, round(best_sc, 1)
    return None, 0.0

def debug_term(text, term, n=6):
    """Show the best candidate sentences for a term (for tuning)."""
    tnorm = term.lower()
    pat = r"(?<![a-z0-9])" + re.escape(tnorm).replace(r"\ ", r"\s+")
    rx = re.compile(pat, re.I)
    rows = []
    for s in sentences(text):
        if not rx.search(s):
            continue
        total = 0.0
        for cue, w in CUES:
            if re.search(cue, s, re.I):
                total += w
                break
        rows.append((score_sentence(s, rx, total), s.strip()))
    rows.sort(key=lambda r: -r[0])
    print(f"\n### {term}")
    for sc, s in rows[:n]:
        print(f"  [{sc:5.1f}] {s[:260]}")
    return rows

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    if cmd == "debug":
        book = Book("osg10.txt")
        for term in sys.argv[2:]:
            rows = debug_term(book.text, term, 5)
            if not rows:
                print(f"\n### {term}: NOT FOUND IN TEXT")
    elif cmd == "test":
        book = Book("osg10.txt")
        for term in sys.argv[2:]:
            d, sc = find_definition(book, term)
            print(f"\n### {term}  (score {sc:.1f})")
            print("   ", (d or "(no definition found)")[:400])
