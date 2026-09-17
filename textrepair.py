"""
Repair whitespace damage in the question bank's text.

The source PDF's text layer both invents and drops spaces, so the extracted
bank contains two opposite defects:

  split words   "in tended"   "h as"      "encrypti on"   "Depart ment"
  glued words   "noneed"      "ofobjects" "usingthe"      "RiskRisk"

Three witnesses decide every fix:

  DICT   a clean English word list (words_alpha.txt, ~370k words) says whether
         a token is a word at all.
  UNI/BI the two licensed study guides: how often a word, and a pair of words,
         actually occurs in 4.3 MB of prose on exactly this subject.
  RAW    the raw PDF extraction: a token the PDF writes whole is a real word.

  join   "A B" -> "AB" when AB is a word the guides use, the guides never write
         "A B" as a phrase, and at least one half is not a word / is very rare.
  split  "AB" -> "A B" when AB is not a word, every part is a real word the
         guides use, and the guides attest the two parts standing together.
  tidy   punctuation and case artefacts ("engineer.The", "?(Choose", "itselF").

Run:
  python textrepair.py             # report only, writes _text_repair_log.txt
  python textrepair.py --write     # rewrite cissp-data.js in place
  python textrepair.py --audit     # also list tokens that stay unknown
"""
import json, os, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
sys.path.insert(0, BASE)
from dataio import load_data

WRITE = "--write" in sys.argv
AUDIT = "--audit" in sys.argv
TOKEN = re.compile(r"[A-Za-z][A-Za-z'\-]*")

# ---------------------------------------------------------------- witnesses
def load_book_stats():
    uni, bi = Counter(), Counter()
    for name in ("osg10.txt", "companion.txt"):
        path = os.path.join(BASE, "_books", name)
        if not os.path.exists(path):
            sys.exit("missing " + path)
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                toks = [t.lower() for t in TOKEN.findall(line)]
                uni.update(toks)
                bi.update(zip(toks, toks[1:]))
    return uni, bi

UNI, BI = load_book_stats()

DICT = set()
_dict_path = os.path.join(BASE, "_words_alpha.txt")
if os.path.exists(_dict_path):
    with open(_dict_path, encoding="utf-8", errors="replace") as f:
        DICT = {w.strip().lower() for w in f if w.strip()}
assert DICT, "a clean word list is required (_words_alpha.txt)"

RAW = Counter()
_raw = os.path.join(BASE, "raw_text.txt")
if os.path.exists(_raw):
    with open(_raw, encoding="utf-8", errors="replace") as f:
        for line in f:
            RAW.update(t.lower() for t in TOKEN.findall(line))
for w in list(DICT):
    pass
print(f"witnesses: DICT {len(DICT):,} words | guides {len(UNI):,} words / "
      f"{len(BI):,} pairs | raw {len(RAW):,} tokens")

# ---------------------------------------------------------------- thresholds
JOIN_MIN = 5         # the joined word must occur this often in the guides
RARE = 12            # a half this rare is presumed to be a word stub
PART_MIN = 20        # a part must be a dictionary word, or this common in the guides
VERY_COMMON = 200    # unused floor kept for reference
RAW_WHOLE = 5        # seen this often whole in the raw extraction -> real word

# Real words the witnesses cannot vouch for (reviewed from the change log).
BLOCK = {"thereof", "species", "timetable", "anyhow", "inaction", "anonexpert",
         "metadata", "elgamal", "kerberos", "telnet", "delphi"}

# Three-way damage and junk punctuation that token rules cannot reach.
FIXES = [
    (re.compile(r"\bOff\s+i\s+cical\b"), "Official"),
    (re.compile(r"\bOff\s+i\s+cial\b"), "Official"),
    (re.compile(r"\bsoftwareitselF\b"), "software itself"),
    (re.compile(r"\bdatare\s+tention\b"), "data retention"),
    (re.compile(r"\bsuch\s+away\s+that\b"), "such a way that"),
    (re.compile(r"\binsecurecommunications\b"), "insecure communications"),
    # long-tail damage left after the token rules (reviewed one by one)
    (re.compile(r"\b(the|The)TCSEC\b"), lambda m: m.group(1) + " TCSEC"),
    (re.compile(r"\bappl\s+yingoversight\b"), "applying oversight"),
    (re.compile(r"\bimplementa\s+safeguard\b"), "implement a safeguard"),
    (re.compile(r"\bimplementa\s+control\b"), "implement a control"),
    (re.compile(r"\bthesecu\s+rity\b"), "the security"),
    (re.compile(r"\bnoread-up\b"), "no read-up"),
    (re.compile(r"\bsp\s+ecific\b"), "specific"),
    (re.compile(r"\bpres\s+erves\b"), "preserves"),
    (re.compile(r"\bspeci\s+fying\b"), "specifying"),
    (re.compile(r"\bpe\s+rtaining\b"), "pertaining"),
    (re.compile(r"\bin\s+te\s+rface\b"), "interface"),
    (re.compile(r"\bcontact\s+less\b"), "contactless"),
    (re.compile(r"\bprovi\s+sioned\b"), "provisioned"),
    (re.compile(r"\bin\s+ter\s+preta\s+tions\b"), "interpretations"),
    (re.compile(r"\bclearence\b"), "clearance"),
    (re.compile(r"\brequried\b"), "required"),
    (re.compile(r"\bauthorites\b"), "authorities"),
    (re.compile(r"\bentitys\b"), "entity's"),
    (re.compile(r"\bora\s+user\b"), "or a user"),
    # the last residual split words found by detect_text_defects.py
    (re.compile(r"\bNon\s+Discretionary\b"), "Nondiscretionary"),
    (re.compile(r"\bnon\s+discretionary\b"), "nondiscretionary"),
    (re.compile(r"\btel\s+ecommunications\b"), "telecommunications"),
    (re.compile(r"\bte\s+lecommunications\b"), "telecommunications"),
    (re.compile(r"\bTe\s+lecommunications\b"), "Telecommunications"),
    (re.compile(r"\bcomp\s+ared\b"), "compared"),
    (re.compile(r"\bst\s+ar\b"), "star"),
    (re.compile(r"\bvulnerabiliti\s+es\b"), "vulnerabilities"),
    (re.compile(r"\bre\s+sponsibilities\b"), "responsibilities"),
    # split proper nouns the word list cannot vouch for (found by _namescan.py)
    (re.compile(r"\bEl\s+Gamal\b"), "ElGamal"),
    (re.compile(r"\bDel\s+phi\b"), "Delphi"),
    (re.compile(r"\bBl\s+acks\b"), "Blacks"),
    (re.compile(r"\bCl\s+ark-Wilson\b"), "Clark-Wilson"),
    (re.compile(r"\bSt\s+andardization\b"), "Standardization"),
    (re.compile(r"\bSil\s+ver\b"), "Silver"),
    (re.compile(r"\bWa\s+rriors\b"), "Warriors"),
    (re.compile(r"\bKe\s+rberos\b"), "Kerberos"),
    (re.compile(r"\bMeta\s+data\b"), "Metadata"),
    (re.compile(r"\bAb\s+ridged\b"), "Abridged"),
    (re.compile(r"\bCyp\s+her\b"), "Cypher"),
    (re.compile(r"\bVi\s+gen\b"), "Vigen"),
    (re.compile(r"\bHa\s+rris\b"), "Harris"),
    (re.compile(r"\bArt\s+hur\b"), "Arthur"),
    (re.compile(r"\bMa\s+rtin\b"), "Martin"),
    (re.compile(r"\bRi\s+vest\b"), "Rivest"),
    (re.compile(r"\bTele\s+graph\b"), "Telegraph"),
    (re.compile(r"\bEn\s+gland\b"), "England"),
    (re.compile(r"\bWrap\s+per\b"), "Wrapper"),
    (re.compile(r"\bSt\s+uart\b"), "Stuart"),
    (re.compile(r"\bCont\s+actless\b"), "Contactless"),
    (re.compile(r"\bTick\s+et-Granting\b"), "Ticket-Granting"),
    (re.compile(r"\bHa\s+mming\b"), "Hamming"),
    (re.compile(r"\bTe\s+lnet\b"), "Telnet"),
    (re.compile(r"\bus\s+ers\b"), "users"),
    (re.compile(r"\bUs\s+ers\b"), "Users"),
    (re.compile(r"\bus\s+es\b"), "uses"),
    (re.compile(r"\bUs\s+es\b"), "Uses"),
    (re.compile(r"\(\s*\)"), ""),
    (re.compile(r"\s+'\s*>"), " "),
    (re.compile(r"'\s*>"), " "),
    (re.compile(r"\bthe\s+Wilson\s+model\s+Clark-Wilson\s+model\b"), "the Clark-Wilson model"),
]

def is_word(w):
    return w in DICT

def try_join(a, b):
    """-> merged token, or None when the two tokens should stay apart."""
    la, lb = a.lower(), b.lower()
    if len(a) > 12 or len(b) > 12 or len(a) < 1 or len(b) < 1:
        return None
    joined = la + lb
    if UNI.get(joined, 0) < JOIN_MIN:
        return None                      # the guides never use that word
    if not is_word(joined):
        return None                      # not a word at all -> damage, not a merge
    # A half is a stub when it is not a word at all, when it is a bare letter
    # (only "a" and "I" are English words), or when it is a word the guides
    # barely use while the merged word is far more common than it is.
    def bare_letter(s):
        return len(s) == 1 and s.lower() not in ("a", "i")

    if not (is_word(la) and is_word(lb)) or bare_letter(a) or bare_letter(b):
        stub, rare = True, True
    else:
        stub = False
        rare = min(UNI.get(la, 0), UNI.get(lb, 0)) <= RARE
        if BI.get((la, lb), 0) != 0:
            return None
        if not rare:
            weaker = min(UNI.get(la, 0), UNI.get(lb, 0))
            if weaker == 0 or UNI.get(joined, 0) >= 20 * weaker:
                rare = True              # "us ers" -> "users"
    if not stub and not rare:
        return None                      # both halves are ordinary words
    if b.isupper() and len(b) >= 2 and not a.isupper():
        return None                      # "has SLE" is not "hassle"
    if a.isupper() and b.isupper():
        return (a + b).upper()           # "BE ST" -> "BEST"
    return a + (b.lower() if b[:1].isupper() else b)

def _score(parts):
    s = -1.2 * (len(parts) - 1)
    for p in parts:
        s += min(UNI.get(p.lower(), 0), 20000) ** 0.5 / 130.0
    for x, y in zip(parts, parts[1:]):
        att = BI.get((x.lower(), y.lower()), 0)
        s += 0.9 if att >= 1 else 0.0
        s += 0.4 if att >= 3 else 0.0
    return s

def _candidates(tok):
    n = len(tok)
    out = []
    for i in range(1, n - 1):            # i=1 allows "a"/"i" as a leading word
        out.append([tok[:i], tok[i:]])
    for i in range(1, n - 3):
        for j in range(i + 2, n - 1):
            out.append([tok[:i], tok[i:j], tok[j:]])
    return out

BLOCK_SPLIT = {"douse", "takeover", "hyperlink", "downtime"}

# short function words that may legitimately be one half of a split ("or unintentional")
SHORT_OK = {w for w, c in UNI.items() if len(w) <= 2 and c >= 500}

def try_split(tok):
    """-> (parts, attested) when a glued token plainly holds two or more words."""
    low = tok.lower()
    if is_word(low) or low in BLOCK or low in BLOCK_SPLIT:
        return None                      # a real word in its own right
    if len(tok) < 5 or any(ch.isdigit() for ch in tok):
        return None
    if tok.isupper():
        return None                      # an acronym or an all-caps name
    if UNI.get(low, 0) >= 30:
        return None                      # established term of the guides (a name)

    def part_ok(p):
        if p in DICT or UNI.get(p, 0) >= PART_MIN:
            return True
        if p.endswith("'s"):              # possessive of a real word
            stem = p[:-2]
            return stem in DICT or UNI.get(stem, 0) >= PART_MIN
        return False

    def shape_ok(p):
        lp = p.lower()
        if p.endswith("'s"):
            return True
        if len(p) == 1:
            return lp in ("a", "i")      # never "D if fie"
        if len(p) == 2:
            return lp in SHORT_OK
        return True

    twos, threes = [], []
    for parts in _candidates(tok):
        lows = [p.lower() for p in parts]
        if any(not shape_ok(p) for p in parts):
            continue
        if any(not part_ok(p) for p in lows):
            continue                     # every part must be a real word/acronym
        anchor = any(p in DICT and UNI.get(p, 0) >= 20 for p in lows)
        att = all(BI.get((x, y), 0) >= 1 for x, y in zip(lows, lows[1:]))
        if not (anchor and (att or all(UNI[p] >= PART_MIN or p in DICT for p in lows))):
            continue
        (twos if len(parts) == 2 else threes).append((parts, _score(parts), att))
    pool = twos or threes                 # a two-way split always wins
    if not pool:
        return None
    parts, _s, att = max(pool, key=lambda r: r[1])
    return parts, att

def try_carried(x, y):
    """
    Three-way damage: a stub of the next word has been carried into this token.

        "thesecu rity"  -> the + secu|rity  -> "the security"
        "appl ying"     -> (handled by the plain merge)

    Returns "A rest" or None.
    """
    lx, ly = x.lower(), y.lower()
    if is_word(lx) or len(x) < 6:
        return None
    for k in range(2, len(x) - 1):
        a, b = x[:k], x[k:]
        if not (is_word(a.lower()) or UNI.get(a.lower(), 0) >= PART_MIN):
            continue
        if len(a) < 2 and a.lower() not in ("a", "i"):
            continue
        if (b + ly) in DICT and UNI.get(b + ly, 0) >= JOIN_MIN:
            return a + " " + b + y
    return None

FUNC = r"(?:in|of|to|for|from|with|at|on|by|the|a|an|and|or|is|are|was|were|that|which|as|not|you|we|they|it|this|these|their|its|his|her|our|your|be|been|has|have|had|but|if|so|no|will|would|can|could|should|must|may|might)"
KEEP_DOUBLE = {"had", "that", "very", "no", "so", "ha", "bye", "she", "he", "i", "a"}

# ---------------------------------------------------------------- one string
def repair_text(text, log, field, ref):
    if not text or not isinstance(text, str):
        return text
    for rx, rep in FIXES:
        text = rx.sub(rep, text)

    # the extractor repeats a word at box boundaries ("loss loss.") and lands
    # commas and full stops between a function word and what follows it
    before_punct = text
    text = re.sub(r"\b([A-Za-z][A-Za-z'\-]{2,})(\s+)\1\b",
                  lambda m: m.group(0) if m.group(1).lower() in KEEP_DOUBLE else m.group(1),
                  text)
    text = re.sub(r"\b" + FUNC + r",(?= [a-z])", lambda m: m.group(0)[:-1], text)
    text = re.sub(r"\b" + FUNC + r"\.(?= [a-z])", lambda m: m.group(0)[:-1], text)
    if text != before_punct:
        log.append(("punct", field, ref, "", ""))
    # repair_text is called with a string; a lambda replacement above keeps case

    for rx, rep in (
        (re.compile(r"[ \t]{2,}"), " "),
        (re.compile(r"[ \t]+([,.;:!?])"), r"\1"),
        (re.compile(r"\?\((?=[A-Za-z])"), "? ("),
        (re.compile(r"([a-z0-9])\.([A-Z][a-z])"), r"\1. \2"),
        (re.compile(r"([a-z0-9]),([A-Za-z])"), r"\1, \2"),
        (re.compile(r"([a-z0-9]);([A-Za-z])"), r"\1; \2"),
        (re.compile(r"\b(\w{4,})\)([A-Z][a-z])"), r"\1) \2"),
        (re.compile(r"([a-z]{4,})\)(?=[a-z])"), r"\1) "),
    ):
        text = rx.sub(rep, text)
    text = re.sub(r"\b([a-z]{3,})([A-Z])\b",
                  lambda m: m.group(1) + m.group(2).lower()
                  if (m.group(1) + m.group(2)).lower() in DICT
                  and UNI.get((m.group(1) + m.group(2)).lower(), 0) >= 20 else m.group(0),
                  text)

    toks = list(TOKEN.finditer(text))
    if not toks:
        return text
    out, i, guard = [], 0, 0
    while i < len(toks) and guard < 6000:
        guard += 1
        t = toks[i]
        piece = t.group()
        sp = try_split(piece)
        if sp:
            parts, att = sp
            out.append(" ".join(parts))
            log.append(("split" + ("" if att else "*"), field, ref, piece, " ".join(parts)))
            i += 1
            continue
        if i + 1 < len(toks):
            nxt = toks[i + 1]
            if text[t.end():nxt.start()] == " ":
                m = try_join(piece, nxt.group())
                if m:
                    # "a sh ared" is "a shared", never "ash ared": when the stub
                    # belongs to the following word, take the better merge.
                    m2 = None
                    if i + 2 < len(toks):
                        nxt2 = toks[i + 2]
                        if text[nxt.end():nxt2.start()] == " ":
                            m2 = try_join(nxt.group(), nxt2.group())
                    if m2 and UNI.get(m2.lower(), 0) > UNI.get(m.lower(), 0) * 2:
                        out.append(piece)
                        i += 1
                        continue
                    out.append(m)
                    log.append(("join", field, ref, piece + " " + nxt.group(), m))
                    i += 2
                    continue
                carried = try_carried(piece, nxt.group())
                if carried:
                    out.append(carried)
                    log.append(("carry", field, ref, piece + " " + nxt.group(), carried))
                    i += 2
                    continue
        out.append(piece)
        i += 1
    joined, pos = [], 0
    for t, piece in zip(toks, out):
        joined.append(text[pos:t.start()])
        joined.append(piece)
        pos = t.end()
    joined.append(text[pos:])
    return "".join(joined)

# ---------------------------------------------------------------- walk data
SKIP_KEYS = {"id", "weight", "src", "sid", "dom", "sourceN", "k", "n", "count",
             "outlineEffective", "source", "total", "subsections", "assigned",
             "general", "missing", "numbering", "missingExplanations"}

if "--probe" in sys.argv:
    for tok in "orunintentional yingoversight implementa thesecu rmful thetcsec areasonable thereported clearence".split():
        print(f"{tok:<18} in DICT={tok in DICT!s:<6} UNI={UNI.get(tok,0):<5} "
              f"split={try_split(tok)} carried(next guess)={try_carried(tok, 'ity')} "
              f"join_with_next={try_join(tok, 'is')}")
    sys.exit()

def walk(node, field, ref, log):
    if isinstance(node, str):
        return repair_text(node, log, field, ref)
    if isinstance(node, list):
        return [walk(v, field, ref, log) for v in node]
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k in SKIP_KEYS or not isinstance(v, (str, list, dict)):
                out[k] = v
                continue
            out[k] = walk(v, k, ref, log)
        return out
    return node

DATA = load_data()
nq = sum(len(s["questions"]) for d in DATA["domains"] for s in d["sections"])
print(f"questions: {nq:,}")

log = []
new = walk(DATA, "root", None, log)
counts = Counter(k.rstrip("*") for k, *_ in log)
print("\nchanges by class:")
for k, v in counts.most_common():
    print(f"  {k:<8} {v:>7,}")
print(f"  unattested splits: {sum(1 for r in log if r[0] == 'split*')}")

out_path = os.path.join(BASE, "_text_repair_log.txt")
with open(out_path, "w", encoding="utf-8") as fh:
    for cls in ("join", "split", "split*", "carry"):
        rows = [r for r in log if r[0] == cls]
        fh.write(f"\n{'='*92}\n{cls}: {len(rows)} changes\n{'='*92}\n")
        seen = set()
        for c, field, ref, before, after in rows:
            if (before, after) in seen:
                continue
            seen.add((before, after))
            fh.write(f"  {before!r:>30} -> {after!r:<30} [{field}]\n")
print(f"distinct fixes logged -> {out_path}")

if AUDIT:
    unknown = Counter()
    def scan(node, fld):
        if isinstance(node, str):
            for t in TOKEN.findall(node):
                low = t.lower()
                if low in DICT or UNI.get(low, 0) >= 3 or len(low) < 5 or low in BLOCK:
                    continue
                if low.endswith("'s") and (low[:-2] in DICT or UNI.get(low[:-2], 0) >= 3):
                    continue             # possessive of a real word
                if low.endswith("s") and low[:-1] in DICT:
                    continue             # plural of a real word the guides never use
                if "-" in low and all(p in DICT or UNI.get(p, 0) >= 3
                                      for p in low.split("-") if p):
                    continue             # hyphenated compound of real words
                unknown[low] += 1
        elif isinstance(node, list):
            for v in node:
                scan(v, fld)
        elif isinstance(node, dict):
            for k, v in node.items():
                if k in SKIP_KEYS or not isinstance(v, (str, list, dict)):
                    continue
                scan(v, k)
    scan(new, "root")
    apath = os.path.join(BASE, "_text_unknown.txt")
    with open(apath, "w", encoding="utf-8") as fh:
        for w, c in unknown.most_common():
            fh.write(f"{c:>5}  {w}\n")
    print(f"unknown tokens left: {len(unknown):,} (types) -> {apath}")
    for w, c in unknown.most_common(25):
        print(f"   {c:>4}  {w}")

if WRITE:
    dst = os.path.join(BASE, "cissp-data.js")
    with open(dst, "w", encoding="utf-8-sig") as f:
        f.write("window.CISSP_DATA = ")
        json.dump(new, f, ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")
    print(f"rewrote {dst} ({os.path.getsize(dst)/1048576:.2f} MB)")
elif not AUDIT:
    print("(report only - re-run with --write to apply)")
