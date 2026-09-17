"""
Build web data for the CISSP Study Portal.

Inputs:
  corrected_questions.json              (validated domain-level question bank)
  subsection_organized_questions.json   (official ISC2 outline -> sub-section titles only)

Output:
  cissp-data.js   ->  window.CISSP_DATA = {...}

Also repairs PDF-extraction artifacts:
  - mid-word newlines      "Business Im\npact"  -> "Business Impact"
  - hyphen line breaks     "multi- \nlevel"     -> "multi-level"
  - word split by space    "technolo gy"        -> "technology"   (corpus-evidence rule)
"""
import json
import re
from collections import Counter

BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"

# ----------------------------------------------------------------------
# 1. Load sources
# ----------------------------------------------------------------------
with open(BASE + r"\corrected_questions.json", "r", encoding="utf-8") as f:
    qbank = json.load(f)

with open(BASE + r"\subsection_organized_questions.json", "r", encoding="utf-8") as f:
    outline_src = json.load(f)

OUTLINE = outline_src["outline"]          # {'1': {'name','weight','sections':{...}}, ...}

# ----------------------------------------------------------------------
# 2. Text repair
# ----------------------------------------------------------------------
def safe_normalize(t):
    if not t:
        return ""
    t = t.replace("\r", "\n")
    # repair PDF encoding artifacts for apostrophes / registered marks
    t = re.sub(r"(\w)\ufffd(\w)", r"\1'\2", t)   # it<fffd>s -> it's
    t = t.replace("\ufffd", "")
    # hyphen at line break between letters -> keep hyphen, drop break
    t = re.sub(r'([A-Za-z])-\s*\n\s*([a-z])', r'\1-\2', t)
    # newline with nothing before it -> word was split mid-word -> join directly
    t = re.sub(r'(\S)\n(\S)', r'\1\2', t)
    # any other newline -> single space
    t = re.sub(r'[ \t]*\n[ \t]*', ' ', t)
    # collapse runs of spaces
    t = re.sub(r'[ \t]{2,}', ' ', t)
    # tidy spaces before punctuation
    t = re.sub(r'\s+([,.;:!?])', r'\1', t)
    return t.strip()

def collect_texts(bank):
    out = []
    for dk, d in bank["domains"].items():
        for q in d["questions"]:
            out.append(q.get("question_text") or "")
            out.append(q.get("explanation") or "")
            for o in q.get("options") or []:
                out.append(o.get("text") or "")
    return out

TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z'\-]*")

# Words treated as legitimate standalone English words. A join is only allowed when
# at least one fragment is NOT a real word. This single guard prevents "in to"->"into",
# "with in"->"within", "a cross"->"across", "It asks"->"Itasks", while still allowing
# artifact repairs such as "se curity"->"security" and "as ymmetric"->"asymmetric".
COMMON = set("""a an the and or but if in on at to of for by with from as is are was were be been
being am it its this that these those he she they them him his her we you your our us i me my mine
not no so do does did done can could will would shall should may might must have has had having
up down out off over under all any some such than then there here when where why how who whom
which what also use used using one two three four five six seven eight nine ten first second third
about after before between during without within through against because while however therefore
into onto upon again further once only own same too very just each both more most other another
new old good bad best worst big small long short high low right left next last many much few less
least well back even still yet ever never always often sometimes now away along across around
data key risk user test file name time type size list item code page form line word call set get
run work help need want look make take give come know see find tell ask show mean keep leave try
part point place plan play please mode modes secure occurred focus operations log car pet top end
side case rate date state level order power system access control process program object subject
model phase stage range value field record server client host port node link path rule role goal
task step term text unit view zone area kind note pair room root safe self ship site skin slot
sort spot star story study style table talk team time tone tool tour town tree trip turn video
voice wall watch water wave week west will wind wine wing wire wish wood yard year mode base
ability account action activity address admin administrator algorithm analysis application
architecture asset attack attacker audit authentication backup baseline block buffer business
button cable capacity cause center central certain change channel chapter charge check choice
cipher circuit class classification clear cluster code command communication component computer
condition configuration connection console content context control cookie copy corporate cost
counter countermeasure course cover credential crime critical cross current curve customer cycle
damage data database decision default defense definition department depend deployment design
detail device diagram difference digital direct direction directory disaster disk display
document domain download drive dynamic edge element email emergency employee encryption end
endpoint engine enterprise entry environment equipment error event evidence exchange execution
exercise exist expense expert exploit exposure extension external extraction facility failure
family fault feature federal field file filter finding firewall firmware flow folder font force
forensic form format framework function gateway general generation goal government group guard
guide handling hardware hash header health help hierarchy history host hot hour identity image
impact implementation incident included increase individual industry information input inside
inspection install instance instruction integer integrity interface internal internet interval
intrusion investigation issue kernel knowledge label language laptop layer learning length
liability library license lifecycle light limitation link list listener load local location lock
logic login malware management manager mandate manual mapping margin marker master material
matter measure media medium member memory message method metric migration minimum mirror mobile
model module monitor motion multiple network node normal notebook object operating operation
operator option organization output package packet parameter password patch pattern payment
peer people percent performance perimeter permission person personnel phase physical plan
platform policy pool population port portal practice precedence premise prevention principle
print privacy private privilege problem procedure process product profile program project
prompt property protocol provider proxy public query question queue range rate ratio reaction
reader reality reason recovery reference region register registry regulation relation release
remote report repository request requirement resource response restriction result retail
retention review right risk role root route router rule runtime safeguard sample sandbox scale
scenario schedule schema scheme scope script search secret section sector secure security
segment selection sensor separation server service session setting severity shadow share shell
signature site situation skill software solution source space spam specification speed sponsor
spreadsheet stack staff stage standard state statement station status storage strategy stream
strength structure subject subnet subsystem success summary supply support surface survey switch
symbol system table target task team technique technology template tenant terminal test text
theory threat threshold time token tool topic trace tracking traffic training transaction
transfer transformation transition translation transport treatment trend trigger trust tunnel
type update upgrade upload urgency usage user utility validation value variable vendor version
video view virtual virus visibility vision volume vulnerability wallet warning web website
window wireless workflow workstation zone""".split())

# Function words eligible to be the *result* of a short-word split repair.
FUNC = set("""the that this these those of to in is are was were and or for with from as at by on it
its be been has have had not but if then than there their they them we you he she his her him my me
our us an so do does did can could will would shall should may might must which who what when where
why how all any some each both more most other such only own same too very just also into over under
again further once here out off up down about after before between during without within through
against because while however therefore""".split())

# Curated missing-space repairs (PDF extraction dropped a space). Each entry was
# reviewed in context; legitimate compounds (lookup, income, outcome, outline,
# moreover, timeout, offline, whoever, undermine, ...) were deliberately excluded.
MISSING_SPACE = {
    "Thiscould": ("This", "could"), "isused": ("is", "used"), "thedata": ("the", "data"),
    "fromthe": ("from", "the"), "ofdata": ("of", "data"), "manyof": ("many", "of"),
    "hereis": ("here", "is"), "namecan": ("name", "can"), "suchas": ("such", "as"),
    "thanbeing": ("than", "being"), "becauseit": ("because", "it"), "intothe": ("into", "the"),
    "theyhave": ("they", "have"), "betweenthe": ("between", "the"), "usewith": ("use", "with"),
    "thatthe": ("that", "the"), "usedin": ("used", "in"), "throughthe": ("through", "the"),
    "toanother": ("to", "another"), "thanthe": ("than", "the"), "notthe": ("not", "the"),
    "theother": ("the", "other"), "thathave": ("that", "have"), "wemight": ("we", "might"),
    "aswell": ("as", "well"), "notmean": ("not", "mean"), "anotherway": ("another", "way"),
    "Themost": ("The", "most"), "andmore": ("and", "more"), "couldhave": ("could", "have"),
    "andwho": ("and", "who"), "allthe": ("all", "the"), "suchthat": ("such", "that"),
    "filefor": ("file", "for"), "themfrom": ("them", "from"), "thatcan": ("that", "can"),
    "thereis": ("there", "is"), "areport": ("a", "report"),
}

def _fix_space_wrap(tok, p1, p2):
    if tok.isupper():
        return p1.upper() + " " + p2.upper()
    if tok[0].isupper():
        return p1.capitalize() + " " + p2
    return p1 + " " + p2

MISSING_SPACE_LOOKUP = {k.lower(): v for k, v in MISSING_SPACE.items()}

MISSING_SPACE_RE = re.compile(
    r"\b(" + "|".join(sorted((k for k in MISSING_SPACE_LOOKUP), key=len, reverse=True)) + r")\b",
    re.IGNORECASE)

def apply_missing_spaces(t):
    if not t:
        return t
    def repl(m):
        p1, p2 = MISSING_SPACE_LOOKUP[m.group(1).lower()]
        return _fix_space_wrap(m.group(0), p1, p2)
    return MISSING_SPACE_RE.sub(repl, t)

# Count-based tiers: (max fragment frequency, min joined frequency).
# Each tier was reviewed against the corpus before inclusion.
REPAIR_TIERS = [(3, 3), (9, 25), (25, 120), (40, 200), (60, 400), (100, 800)]

def build_vocab(texts):
    v = Counter()
    for t in texts:
        for tok in TOKEN_RE.findall(t):
            v[tok.lower()] += 1
    return v

def discover_rules(texts, vocab):
    """Find split-word repair rules.

    Three rule families:
      R1 count-based   : concat is a corpus word and both fragments are rare.
      R2 function word : concat is an English function word and not both fragments
                         are real words. Skipped for "U.S."/"T1"-style abbreviations.
      R3 three-way     : a single-letter non-word fragment followed by a rare
                         non-word fragment ("t"+"echnique" -> "technique").

    Ambiguity guard: a rule that would absorb a single letter into a REAL word
    ("a"+"s" -> "as" in "a s ecurity") is rejected whenever that letter forms a
    word with the following token, because the letter really belongs to it.
    Those cases are resolved by R3 instead ("s"+"ecurity" -> "security").
    """
    rules = set()
    ambiguous = set()
    for t in texts:
        toks = TOKEN_RE.findall(t)
        for i in range(len(toks) - 1):
            a, b = toks[i], toks[i + 1]
            la, lb = a.lower().strip("-'"), b.lower().strip("-'")
            joined = (a + b).lower()
            both_real = (la in COMMON) and (lb in COMMON)

            # --- R1: count-based ---
            if joined in vocab and not both_real:
                for frag_max, join_min in REPAIR_TIERS:
                    if (vocab.get(la, 0) <= frag_max
                            and vocab.get(lb, 0) <= frag_max
                            and vocab[joined] >= join_min):
                        rules.add((a, b))
                        break

            # --- R3: single letter belongs to the FOLLOWING fragment ---
            if (len(a) == 1 and la not in COMMON and len(b) >= 2
                    and lb not in COMMON and joined in vocab
                    and vocab[joined] >= 3 and vocab.get(lb, 0) <= 200):
                rules.add((a, b))

            # --- R2: function-word split ---
            if joined in FUNC and not both_real:
                if len(b) == 1 and b.isupper():
                    continue                      # abbreviation like U.S. / T1
                if len(b) == 1:
                    nxt_word = None
                    if i + 2 < len(toks):
                        c = toks[i + 2]
                        if len(c) >= 2 and (b + c).lower() in vocab \
                                and vocab[(b + c).lower()] >= 3:
                            nxt_word = c
                    if nxt_word is not None:
                        # b completes the next token, so never absorb it here
                        ambiguous.add((a, b))
                        continue
                rules.add((a, b))
    return rules, ambiguous

def make_replacer(pairs):
    """Single-pass regex replacer for all learned pairs (longest key first)."""
    mapping = {f"{a} {b}": a + b for a, b in pairs}
    if not mapping:
        return lambda s: s
    pattern = re.compile("|".join(re.escape(k) for k in
                                  sorted(mapping, key=len, reverse=True)))
    return lambda s: pattern.sub(lambda m: mapping[m.group(0)], s)

raw_texts = collect_texts(qbank)
norm_texts = [safe_normalize(t) for t in raw_texts]

all_pairs = set()
blocked = set()
for iteration in range(10):
    vocab = build_vocab(norm_texts)
    rules, ambiguous = discover_rules(norm_texts, vocab)
    blocked |= ambiguous
    fresh = (rules - ambiguous) - all_pairs - blocked
    if not fresh:
        print(f"  converged after {iteration} iteration(s)")
        break
    all_pairs |= fresh
    repl = make_replacer(fresh)
    norm_texts = [repl(t) for t in norm_texts]
    print(f"  iteration {iteration + 1}: +{len(fresh)} rules (total {len(all_pairs)})")

print(f"  total split-word repair rules: {len(all_pairs)}")
print(f"  ambiguous rules blocked (resolved by R3 instead): {len(blocked)}")
REPLACE_ALL = make_replacer(all_pairs)

# Residual report (informational only)
vocab_final = build_vocab(norm_texts)
residual, _ = discover_rules(norm_texts, vocab_final)
residual = residual - all_pairs - blocked
print(f"  residual unrepaired candidates (informational): {len(residual)}")

def apply_single_letter_rules(t, vocab):
    """Context-sensitive repair for lone single letters left after the global pass.

    A stray letter is merged with the neighbour that forms a real word:
      "th e mission"  -> merge left  -> "the mission"   (th is not a word)
      "a s ecurity"   -> merge right -> "a security"    (a IS a word)
      "it s regulatory" -> no right merge, merge left -> "its regulatory"
    Lone UPPERCASE letters are only ever merged to the right, which preserves
    abbreviations such as "U.S.", "a T1" and "the M+1".
    """
    toks = list(TOKEN_RE.finditer(t))
    if not toks:
        return t

    edits = []
    used = set()

    for i in range(len(toks)):
        if i in used:
            continue
        m = toks[i]
        tok = m.group(0)
        if len(tok) != 1 or not tok.isalpha():
            continue

        prev = toks[i - 1] if (i > 0 and (i - 1) not in used) else None
        nxt = toks[i + 1] if (i + 1 < len(toks)) else None

        def merge_right():
            if nxt is None:
                return None
            N = nxt.group(0)
            if len(N) < 2 or N.lower().strip("-'") in COMMON:
                return None
            j = (tok + N).lower()
            return j if (j in vocab and vocab[j] >= 3) else None

        def merge_left():
            if prev is None:
                return None
            P = prev.group(0)
            if len(P) < 2:
                return None
            j = (P + tok).lower()
            return j if (j in vocab and vocab[j] >= 3) else None

        if tok.isupper():
            if merge_right():
                edits.append((m.start(), nxt.end(), tok + nxt.group(0)))
                used.update((i, i + 1))
            continue

        prev_is_word = prev is not None and prev.group(0).lower().strip("-'") in COMMON

        if prev_is_word:
            if merge_right():
                edits.append((m.start(), nxt.end(), tok + nxt.group(0)))
                used.update((i, i + 1))
            elif merge_left():
                edits.append((prev.start(), m.end(), prev.group(0) + tok))
                used.update((i, i - 1))
        else:
            if merge_left():
                edits.append((prev.start(), m.end(), prev.group(0) + tok))
                used.update((i, i - 1))
            elif merge_right():
                edits.append((m.start(), nxt.end(), tok + nxt.group(0)))
                used.update((i, i + 1))

    if not edits:
        return t

    edits.sort(key=lambda e: e[0])
    out, last = [], 0
    for s, e, r in edits:
        if s < last:
            continue
        out.append(t[last:s])
        out.append(r)
        last = e
    out.append(t[last:])
    return "".join(out)

FINAL_VOCAB = build_vocab(norm_texts)

# ----------------------------------------------------------------------
# English dictionary (used to decide whether a glued token is a real word)
# ----------------------------------------------------------------------
try:
    from english_words import get_english_words_set
    ENGLISH = get_english_words_set(['web2'], lower=True)
except Exception:
    ENGLISH = set()

# Legitimate compounds that are absent from the dictionary above but must NOT be split.
LEGIT_COMPOUNDS = set("""
offline online input output throughput ongoing instead insight inland upstream downstream
underline underlying overlook overhead otherwise nevertheless notwithstanding upstairs
downside upside onto upon into within without throughout herein thereby whereby wherein
hereinafter thereof thereto hereto hereof whereof lookup underway moreover offsite onside
outsource outsourced outsourcing overwrite overwritten overwriting knowhow inline backoff
backups failover rollover takeover turnover crossover forever wherever whenever whoever
whatever anymore cornerstone underscore underwrite overrun bypass firewall download upload
update upgrade backup login logout layout upcoming uptake uptime downtime runtime somehow
somewhere sometime somewhat anyone everyone someone nothing anything everything outbound
inbound upscale overdue overall outsourced checksum timestamp hotspot desktop laptop
notebook internet intranet extranet ethernet gateway hostname username password passphrase
passcode endpoint baseline feedback payload lifecycle workflow workspace filesystem
namespace wildcard bookmark browser cookie session token buffer pointer kernel driver
plugin addon package module library daemon thread socket subnet supernet multicast
broadcast unicast anycast loopback handshake keychain keystore plaintext ciphertext
cleartext nonce digest signature certificate revocation enrollment attestation
authorization authentication identification accountability nonrepudiation
""".split())

def is_word(w):
    return w in ENGLISH or (len(w) == 1 and w in FUNC)

# R5: glue a fragment onto the neighbouring fragment when that yields a real word.
#     Two cases:
#       (a) the trailing fragment is rare            "inhere nt"      -> "inherent"
#       (b) the leading fragment is a long non-word  "classificati on" -> "classification"
def find_glue_pairs(texts, vocab):
    pairs = set()
    for t in texts:
        toks = TOKEN_RE.findall(t)
        for i in range(len(toks) - 1):
            A, B = toks[i], toks[i + 1]
            if len(A) < 2 or len(B) > 10:
                continue
            a_limit = 20 if len(A) >= 4 else 5
            if vocab.get(A.lower(), 0) > a_limit or A.lower() in ENGLISH:
                continue
            j = (A + B).lower()
            if j not in ENGLISH or vocab.get(j, 0) < 3:
                continue
            if vocab.get(B.lower(), 0) <= 5 or len(A) >= 4:
                pairs.add((A, B))
    return pairs

# Curated joins where both halves are real words, so no automatic rule may fire.
# Each was verified in context.
JOIN_PAIRS = [
    ("in", "stead"), ("with", "in"), ("in", "to"), ("so", "me"), ("with", "out"),
    ("how", "ever"), ("no", "where"), ("some", "one"),
    # acronyms / hyphenated terms split by the extraction
    ("i", "saca"), ("an", "si"), ("multi-le", "vel"), ("shielde", "d"),
]
JOIN_RE = re.compile(r"\b(" + "|".join(p1 + r"[\s]+" + p2 for p1, p2 in JOIN_PAIRS) + r")\b",
                     re.IGNORECASE)

def apply_join_pairs(t):
    if not t:
        return t
    def repl(m):
        parts = m.group(0).split()
        joined = (parts[0] + parts[1]).lower()
        if m.group(0).isupper():
            return joined.upper()
        if parts[0][0].isupper():
            return joined.capitalize()
        return joined
    return JOIN_RE.sub(repl, t)

GLUE = find_glue_pairs(norm_texts, FINAL_VOCAB)
print(f"  glue rules (rare fragment -> real word): {len(GLUE)}")
REPLACE_ALL = make_replacer(all_pairs | GLUE)

def strip_diacritics(s):
    return s

# R6: split rare non-dictionary tokens that were glued by the extraction,
#     when there is exactly one cut into two real words including a function word.
def find_split_tokens(texts, vocab):
    splits = {}
    ambiguous = {}
    for t in texts:
        for tok in TOKEN_RE.findall(t):
            tl = tok.lower()
            if tl in ENGLISH or tl in LEGIT_COMPOUNDS or tl in splits or tl in ambiguous:
                continue
            if len(tl) < 3:
                continue
            cuts = []
            for i in range(1, len(tl)):
                p1, p2 = tl[:i], tl[i:]
                if not is_word(p1) or not is_word(p2):
                    continue
                if len(p2) < 2 and p2 not in ("a", "i"):
                    continue
                if (p1 in FUNC and len(p1) >= 2 and vocab.get(p2, 0) >= 20) or \
                   (p2 in FUNC and len(p2) >= 2 and vocab.get(p1, 0) >= 20):
                    cuts.append((p1, p2))
            if len(cuts) == 1:
                splits[tl] = cuts[0]
            elif len(cuts) > 1:
                # prefer the shortest leading function word ("areport" -> "a report",
                # not "are port"); tie-break on the longest trailing word
                cuts.sort(key=lambda c: (len(c[0]), -len(c[1])))
                splits[tl] = cuts[0]
                ambiguous[tl] = cuts
    return splits, ambiguous

SPLIT_TOKENS, AMBIGUOUS_TOKENS = find_split_tokens(norm_texts, FINAL_VOCAB)
print(f"  missing-space split rules: {len(SPLIT_TOKENS)}")
print(f"  ambiguous glued tokens (left alone): {len(AMBIGUOUS_TOKENS)}")
with open(BASE + r"\_split_rules_review.json", "w", encoding="utf-8") as _f:
    json.dump({
        "applied": {k: {"parts": v, "count": FINAL_VOCAB.get(k, 0)} for k, v in
                    sorted(SPLIT_TOKENS.items(), key=lambda kv: -FINAL_VOCAB.get(kv[0], 0))},
        "ambiguous": {k: {"cuts": v, "count": FINAL_VOCAB.get(k, 0)} for k, v in
                      sorted(AMBIGUOUS_TOKENS.items(), key=lambda kv: -FINAL_VOCAB.get(kv[0], 0))},
    }, _f, indent=1)

SPLIT_RE = re.compile(r"\b(" + "|".join(sorted(SPLIT_TOKENS, key=len, reverse=True)) + r")\b",
                      re.IGNORECASE) if SPLIT_TOKENS else None

def apply_split_tokens(t):
    if not t or SPLIT_RE is None:
        return t
    def repl(m):
        tok = m.group(0)
        p1, p2 = SPLIT_TOKENS[tok.lower()]
        if tok.isupper():
            return p1.upper() + " " + p2.upper()
        if tok[0].isupper():
            return p1.capitalize() + " " + p2
        return p1 + " " + p2
    return SPLIT_RE.sub(repl, t)

def clean(t):
    s = safe_normalize(t)
    s = REPLACE_ALL(s)
    s = apply_join_pairs(s)          # curated joins ("In stead" -> "Instead")
    s = apply_single_letter_rules(s, FINAL_VOCAB)
    s = apply_missing_spaces(s)      # curated splits take precedence
    s = apply_split_tokens(s)        # dictionary-guided automatic splits
    return s

# ----------------------------------------------------------------------
# 3. Domain study-guide metadata
# ----------------------------------------------------------------------
DOMAIN_META = {
    "1": {
        "description": (
            "Security and Risk Management is the foundation domain. It covers security governance, "
            "compliance and regulatory obligations, legal issues, professional ethics, security policy "
            "and documentation, risk management concepts and analysis, threat modeling, supply chain risk, "
            "personnel security, security awareness training, and business continuity requirements."
        ),
        "key_topics": [
            "CIA triad, due care vs. due diligence, and security governance",
            "ISC2 Code of Ethics canons",
            "Legal, regulatory and compliance frameworks (GDPR, HIPAA, SOX, PCI DSS, CFAA)",
            "Intellectual property: copyright, trademark, patent, trade secret",
            "Policy / standard / procedure / guideline / baseline hierarchy",
            "Quantitative risk analysis: SLE, ALE, ARO, EF",
            "Qualitative risk analysis, risk appetite, risk tolerance, residual risk",
            "Threat modeling (STRIDE, DREAD, PASTA, attack trees)",
            "Supply chain risk management (SCRM) and third-party risk",
            "Personnel security: screening, NDAs, job rotation, mandatory vacation, termination",
            "Business impact analysis (BIA), RTO, RPO, MTD",
            "Security awareness, education and training programs"
        ],
    },
    "2": {
        "description": (
            "Asset Security covers the information and asset lifecycle: how data is identified, "
            "classified, labeled, handled, retained, and securely destroyed, and which controls and "
            "compliance requirements apply to it."
        ),
        "key_topics": [
            "Information and asset classification levels and labeling",
            "Data ownership roles: owner, custodian, steward, user",
            "Handling requirements and acceptable use",
            "Data lifecycle: creation, storage, use, sharing, archival, destruction",
            "Media sanitization: clearing, purging, degaussing, crypto-shredding, destruction",
            "Data remanence and secure disposal",
            "Retention policies, legal hold and e-discovery",
            "Privacy principles and PII / PHI protection",
            "Data security controls and compliance baselines"
        ],
    },
    "3": {
        "description": (
            "Security Architecture and Engineering covers secure design principles, security models, "
            "evaluation criteria, the security capabilities of information systems, system vulnerabilities, "
            "cryptography and cryptanalysis, plus site and facility physical security design."
        ),
        "key_topics": [
            "Secure design principles: defense in depth, least privilege, fail-safe/fail-secure, "
            "separation of duties, economy of mechanism, complete mediation, open design",
            "Security models: Bell-LaPadula, Biba, Clark-Wilson, Brewer-Nash, state machine, "
            "information flow, lattice, non-interference",
            "Evaluation criteria: TCSEC/Orange Book, ITSEC, Common Criteria EAL, protection profiles",
            "Trusted Computing Base, security kernel, reference monitor, protection rings",
            "System vulnerabilities: buffer overflow, race conditions, TOCTOU, injection flaws",
            "Cryptography: symmetric/asymmetric algorithms (AES, DES, 3DES, RSA, ECC), "
            "Diffie-Hellman, block vs. stream ciphers and modes",
            "Hashing and integrity: SHA, MD5, HMAC, digital signatures",
            "PKI, certificate authorities, key management, escrow and recovery",
            "Cryptanalytic attacks: brute force, known/chosen plaintext, side-channel, "
            "differential/linear, birthday, rainbow tables",
            "Site and facility design: CPTED, perimeter, mantraps, CCTV, fire detection and "
            "suppression (Halon, FM-200, sprinklers), HVAC, UPS/generators, TEMPEST"
        ],
    },
    "4": {
        "description": (
            "Communication and Network Security covers secure network architecture and design, "
            "network components and devices, and secure communication channels, including the "
            "protocols and attacks that apply to each."
        ),
        "key_topics": [
            "OSI and TCP/IP models, encapsulation, layer responsibilities",
            "Network topologies, segmentation, VLANs, DMZ/screened subnets, microsegmentation, "
            "zero trust and software-defined networking",
            "Firewalls: packet filtering, stateful inspection, application/proxy, NGFW, WAF",
            "IDS/IPS: host-based vs. network-based, detection methods, placement",
            "Routers, switches, load balancers, proxies, NAC, UTM",
            "VPN and tunneling: IPSec (AH/ESP, transport vs. tunnel), SSL/TLS VPN",
            "Wireless security: WEP, WPA/WPA2/WPA3, 802.1x, EAP, site surveys",
            "Secure channels: SSH, SFTP, TLS/SSL, S/MIME, PGP, DNSSEC",
            "Network attacks: DoS/DDoS, spoofing, ARP poisoning, MITM, sniffing, "
            "DNS poisoning, replay, session hijacking",
            "Transmission media, cabling standards and signal degradation"
        ],
    },
    "5": {
        "description": (
            "Identity and Access Management covers controlling physical and logical access to assets, "
            "identification and authentication of people and devices, federated identity, authorization "
            "mechanisms, and the identity/access provisioning lifecycle."
        ),
        "key_topics": [
            "Access control concepts: subjects, objects, least privilege, need to know",
            "Authentication factors: something you know / have / are / do",
            "Passwords, tokens, smart cards, biometrics (FAR, FRR, CER/EER, Type I & II errors)",
            "Multi-factor and step-up authentication",
            "Single sign-on, Kerberos, RADIUS, TACACS+, LDAP, Active Directory",
            "Federated identity: SAML, OAuth, OpenID Connect, identity providers",
            "Authorization models: DAC, MAC, RBAC, ABAC, rule-based, access matrices and ACLs",
            "Provisioning/deprovisioning, access reviews and recertification",
            "Account lifecycle and privileged access management"
        ],
    },
    "6": {
        "description": (
            "Security Assessment and Testing covers designing assessment, test and audit strategies; "
            "conducting security control testing; collecting security process data; analyzing results; "
            "and performing security audits."
        ),
        "key_topics": [
            "Assessment and audit strategy, scope, and planning",
            "Vulnerability assessment and scanning (credentialed vs. non-credentialed)",
            "Penetration testing: black/gray/white box, internal/external, rules of engagement",
            "Social engineering tests and phishing simulations",
            "Wireless and physical penetration testing",
            "Security control testing and configuration review",
            "Security metrics: KPIs, KRIs, and process data collection",
            "Log review, monitoring and continuous assessment",
            "Reporting: CVSS severity, false positives/negatives, remediation tracking",
            "Security audits: internal vs. external, evidence, findings, auditor independence"
        ],
    },
    "7": {
        "description": (
            "Security Operations covers the day-to-day running of security: investigations and forensics, "
            "logging and monitoring, configuration and change management, incident management, "
            "detective and preventive measures, patch and vulnerability management, recovery strategies, "
            "disaster recovery, business continuity, and physical/personnel safety."
        ),
        "key_topics": [
            "Investigations, digital forensics, evidence handling and chain of custody",
            "Order of volatility and forensic imaging",
            "Logging, monitoring, SIEM, audit trails, UEBA and anomaly detection",
            "Configuration management, baselines, CMDB, configuration drift",
            "Foundational operations: need to know, least privilege, separation of duties, "
            "dual control, split knowledge, mandatory vacation",
            "Resource protection: backups (full/incremental/differential), RAID, redundancy, HA",
            "Incident management: preparation, detection, containment, eradication, recovery, "
            "lessons learned",
            "Detective and preventive measures: anti-malware, EDR, honeypots, FIM, DLP, sandboxing",
            "Patch and vulnerability management",
            "Change management and change advisory boards",
            "Recovery strategies and alternate sites (hot/warm/cold, reciprocal agreements)",
            "Disaster recovery plans and DRP testing (tabletop, walkthrough, simulation, parallel, "
            "full interruption)",
            "Business continuity planning and crisis management",
            "Physical security operations and personnel safety"
        ],
    },
    "8": {
        "description": (
            "Software Development Security covers integrating security into the software development "
            "life cycle, applying security controls within development ecosystems, assessing the "
            "effectiveness of software security, evaluating acquired software, and secure coding."
        ),
        "key_topics": [
            "SDLC models: waterfall, agile/Scrum, spiral, V-model, RAD, DevOps/DevSecOps",
            "Security requirements, threat modeling and secure design in the SDLC",
            "Development ecosystem security: CI/CD, version control, build and artifact security",
            "Code review and testing: SAST, DAST, IAST, SCA, fuzzing",
            "Assessing acquired/COTS and open source software; software supply chain",
            "Secure coding: input validation, output encoding, parameterized queries, "
            "error handling, session management",
            "Common defects: SQL injection, XSS, CSRF, buffer overflow, insecure deserialization",
            "OWASP guidance and secure coding standards",
            "Database security: relational concepts, views, keys, normalization, ACID, inference"
        ],
    },
}

DOMAIN_NAMES = {
    "1": "Security and Risk Management",
    "2": "Asset Security",
    "3": "Security Architecture and Engineering",
    "4": "Communication and Network Security",
    "5": "Identity and Access Management (IAM)",
    "6": "Security Assessment and Testing",
    "7": "Security Operations",
    "8": "Software Development Security",
}

# ----------------------------------------------------------------------
# 4. Re-derive question TEXT from the authoritative raw extraction
#    (corrected_questions.json introduced spacing corruptions in an earlier
#     processing pass; we keep its validated DOMAIN structure but rebuild text)
# ----------------------------------------------------------------------
RAW_PATH = BASE + r"\raw_text.txt"
with open(RAW_PATH, "r", encoding="utf-8") as f:
    RAW = f.read()

RAW_Q_RE = re.compile(r'QUESTION\s+(\d+)\s*-\s*\(Topic\s+(\d+)\)')

HEADER_PATTERNS = [
    re.compile(r'ISC\s+CISSP', re.I),
    re.compile(r'[\u201c"]Best Material, Great Results[\u201d"]\.?', re.I),
    re.compile(r'CERT\s*EMPIRE\s*\d*', re.I),
    re.compile(r'https://certempire\.com/\s*\d*', re.I),
    re.compile(r'Exam\s+ISC\s+CISSP', re.I),
]

def strip_headers(s):
    for pat in HEADER_PATTERNS:
        s = pat.sub(' ', s)
    s = re.sub(r'[ \t]{2,}', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

def split_merged_options(s):
    """Kept for the explanation/text cleanup; option splitting itself is handled
    structurally by find_option_run()."""
    return s

OPT_LABEL = re.compile(r'^\s*([A-H])[\.\)]\s*(.*)$', re.DOTALL)
BULLET_LABEL = re.compile(r'^\s*[\?\u2022\*\u00b7]\s*(.*)$', re.DOTALL)

# A candidate option label: a letter A-H followed by '.' or ')' and whitespace.
# No lookbehind is used: this source glues labels to the previous option's text
# ("...RAID Level 5B. RAID Level 6"). False hits inside prose are discarded by
# the consecutive-run requirement in find_option_run().
CAND = re.compile(r'([A-H])[\.\)][ \t]+')
BULLET_CAND = re.compile(r'(?:^|(?<=\s))[\?\u2022\*\u00b7][ \t]+')

def find_option_run(region):
    """Locate the longest run of consecutive option labels (A,B,C,...).

    Labels may start at any letter (this source sometimes only shows E-H while
    the answer key refers to position) and may be glued to the previous option's
    text. Non-consecutive letter hits inside option prose are ignored."""
    cands = list(CAND.finditer(region))
    best = []
    for s in range(len(cands)):
        run = [s]
        expected = cands[s].group(1)
        for j in range(s + 1, len(cands)):
            L = cands[j].group(1)
            if L == chr(ord(expected) + 1):
                run.append(j)
                expected = L
        if len(run) > len(best):
            best = run
    return [cands[i] for i in best]

def extract_answer(s):
    m = re.search(r'Answer:\s*([A-Ha-h])\b', s)
    return m.group(1).upper() if m else ""

def extract_explanation(s):
    i = s.find("Explanation:")
    if i < 0:
        return ""
    t = s[i + len("Explanation:"):].strip()
    cut = len(t)
    for marker in ("Source:", "Reference(s)", "The following reference", "QUESTION ",
                   "References used", "Reference used"):
        p = t.find(marker)
        if 0 <= p < cut:
            cut = p
    t = t[:cut].strip()
    t = re.sub(r'^Explanation\s*:\s*', '', t).strip()
    return t if len(t) > 20 else ""

def parse_raw_question(body):
    """Extract (question_text, options, answer, explanation) from one raw block.

    Handles the quirks of this source document:
      * options glued together on one line
      * option labels offset (starting at E-G) while the answer key refers to the
        option's POSITION -> options are normalised to A.. and the key remapped
      * '?' bullets used instead of letters (again positional)
    """
    s = strip_headers(body)
    ans_m = re.search(r'Answer:\s*[A-Ha-h]\b', s)
    head = s[:ans_m.start()] if ans_m else s
    answer_letter = extract_answer(s)

    run = find_option_run(head)
    items = []
    qtext = ""

    if len(run) >= 2:
        qtext = head[:run[0].start()].strip()
        for k, m in enumerate(run):
            start = m.end()
            end = run[k + 1].start() if k + 1 < len(run) else len(head)
            items.append((m.group(1), head[start:end].strip()))
    else:
        b = list(BULLET_CAND.finditer(head))
        if len(b) >= 2:
            qtext = head[:b[0].start()].strip()
            for k, m in enumerate(b):
                start = m.end()
                end = b[k + 1].start() if k + 1 < len(b) else len(head)
                items.append((None, head[start:end].strip()))
        else:
            # last resort: some questions use "- " bullets glued together,
            # e.g. "- Operation- Initiation- Functional design- Implementation"
            parts = re.split(r'\s*[\-\u2013\u2014]\s+', head)
            cand = [p.strip() for p in parts[1:]] if len(parts) >= 3 else []
            cand = [c for c in cand if len(c) >= 2]
            if len(cand) >= 2:
                qtext = parts[0].strip()
                items = [(None, t) for t in cand]
            else:
                qtext = (head[:250] if head else s[:250]).strip()

    original_labels = [lab for lab, _ in items]
    options = [{"letter": chr(ord('A') + i), "text": txt}
               for i, (_, txt) in enumerate(items)]

    answer = ""
    if items and answer_letter:
        if answer_letter in original_labels:
            answer = chr(ord('A') + original_labels.index(answer_letter))
        else:
            idx = ord(answer_letter) - ord('A')
            answer = chr(ord('A') + idx) if 0 <= idx < len(items) else answer_letter

    return qtext, options, answer, extract_explanation(s)

raw_questions = {}
parts = RAW_Q_RE.split(RAW)
for i in range(1, len(parts), 3):
    num = int(parts[i])
    body = parts[i + 2]
    nxt = RAW_Q_RE.search(body)
    if nxt:
        body = body[:nxt.start()]
    raw_questions[num] = parse_raw_question(body)

print(f"  re-parsed {len(raw_questions)} questions from raw_text.txt")

# ----------------------------------------------------------------------
# 5. Build output payload
# ----------------------------------------------------------------------
weight_map = {k: v["weight"] for k, v in OUTLINE.items()}

domains_out = []
for i in range(1, 9):
    key = f"domain_{i}"
    src = qbank["domains"][key]
    sid = str(i)
    meta = DOMAIN_META[sid]

    sections = [{"id": sec_id, "title": title}
                for sec_id, title in OUTLINE[sid]["sections"].items()]

    questions = []
    for q in src["questions"]:
        n = q["question_number"]
        if n in raw_questions:
            qtext, options, answer, explanation = raw_questions[n]
        else:  # fallback to the JSON text
            qtext = q.get("question_text")
            options = q.get("options") or []
            answer = q.get("answer") or ""
            explanation = q.get("explanation") if q.get("has_explanation") else ""

        questions.append({
            "n": n,
            "t": q.get("original_topic"),
            "q": clean(qtext),
            "o": [[o["letter"], clean(o["text"])] for o in options],
            "a": answer or "",
            "e": clean(explanation) if explanation else "",
        })

    domains_out.append({
        "id": i,
        "name": DOMAIN_NAMES[sid],
        "full": f"Domain {i}: {DOMAIN_NAMES[sid]}",
        "weight": weight_map.get(sid, ""),
        "count": len(questions),
        "missing": sum(1 for x in questions if not x["e"]),
        "description": meta["description"],
        "keyTopics": meta["key_topics"],
        "sections": sections,
        "questions": questions,
    })
    print(f"  domain {i}: {len(questions)} questions, {len(sections)} study-guide sub-sections")

payload = {
    "meta": {
        "title": "CISSP Certification Exam — Study Portal",
        "total": qbank["metadata"]["total_questions"],
        "missingExplanations": qbank["metadata"]["missing_explanations"],
        "outlineEffective": "April 15, 2024",
        "source": "corrected_questions.json (domain-level classification)",
        "note": (
            "Questions are organised by the 8 official CISSP domains. "
            "Sub-section titles are provided as study-guide checklists before each domain's questions."
        ),
    },
    "studyGuide": {
        "strategy": [
            "Start with Domain 1 — it underpins every other domain.",
            "Study one domain at a time; finish its questions before moving on.",
            "Answer first, then read the explanation even when you were right.",
            "Keep a log of missed questions and re-test them weekly.",
            "Aim for ~1 minute per question under timed conditions before exam day."
        ],
        "priority": {
            "High weight": ["Domain 1 (15%)", "Domain 3 (13%)", "Domain 4 (13%)",
                            "Domain 5 (13%)", "Domain 7 (13%)"],
            "Medium weight": ["Domain 6 (12%)", "Domain 8 (11%)", "Domain 2 (10%)"]
        },
        "tips": [
            "Understand the \"why\" behind each answer, not just the answer itself.",
            "CISSP asks for the BEST answer — several options are often technically true.",
            "Think like a risk advisor to management, not a technician.",
            "Watch for absolutes (\"always\", \"never\", \"all\") — usually wrong.",
            "When unsure, choose the answer that protects people first, then data, then systems."
        ],
        "examDay": [
            "Get a full night's sleep and arrive early.",
            "Read each question twice; note qualifiers like BEST, FIRST, PRIMARY, NOT.",
            "Eliminate obviously wrong options before choosing.",
            "Don't over-invest time in any single question.",
            "Flag uncertain items and revisit them at the end."
        ],
        "resources": [
            "Official (ISC)2 CISSP Study Guide / CBK",
            "CISSP All-in-One Exam Guide (Shon Harris)",
            "Official (ISC)2 CISSP Practice Tests",
            "ISC2 CISSP Certification Exam Outline (April 15, 2024)"
        ]
    },
    "domains": domains_out,
}

out_path = BASE + r"\cissp-data.js"
with open(out_path, "w", encoding="utf-8-sig") as f:
    f.write("window.CISSP_DATA = ")
    json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    f.write(";\n")

import os
size_mb = os.path.getsize(out_path) / (1024 * 1024)
print(f"\nWrote {out_path} ({size_mb:.2f} MB)")
print(f"Total questions embedded: {sum(d['count'] for d in domains_out)}")
