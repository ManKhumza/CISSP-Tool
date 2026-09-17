"""
Patch subsection_keywords.py:
  * promote important 'weak' terms to 'strong' (competition is local, so safe)
  * add missing vocabulary found in the unplaced questions
Writes the file back with the same structure.
"""
import io, sys, pprint
BASE = r"C:\Users\Khumza\Documents\Coding projects\CISSP"
sys.path.insert(0, BASE)
import subsection_keywords as kw

T = kw.SUBSEC_TERMS

def promote(sid, terms):
    s, w = T[sid]["strong"], T[sid]["weak"]
    for t in terms:
        if t in w:
            w.remove(t)
        if t not in s:
            s.append(t)

def add(sid, strong=(), weak=()):
    for t in strong:
        if t not in T[sid]["strong"]:
            T[sid]["strong"].append(t)
    for t in weak:
        if t not in T[sid]["weak"] and t not in T[sid]["strong"]:
            T[sid]["weak"].append(t)

# ---- promotions (important terms that were only supporting) ----
promote("1.2", ["confidentiality", "integrity", "availability", "accountability", "authenticity"])
promote("1.6", ["policy", "standard", "procedure", "guideline", "baseline"])
promote("4.2", ["ids", "ips", "wireless", "endpoint"])
promote("4.1", ["bandwidth", "cable", "topology"])
promote("7.5", ["clustering", "tape", "storage"])
promote("6.2", ["scan", "scanner"])
promote("6.5", ["audit"])
promote("2.4", ["destruction", "media"])
promote("3.4", ["virtualization"])
promote("5.2", ["biometric", "token"])

# ---- Domain 1 ----
add("1.3", strong=["senior management", "ultimately responsible", "responsibility for security",
                   "accountable", "management responsibility", "security program",
                   "security awareness program sponsor"])
add("1.2", strong=["opposite of", "security definition", "cia"])
add("1.6", strong=["step-by-step", "step by step", "control requirements",
                   "advisory policy", "regulatory policy", "security policy framework"])
add("1.9", strong=["risk analysis", "risk assessment methodology", "threat and risk"])
add("1.8", strong=["employee", "personnel"])          # these are the subject of 1.8 questions

# ---- Domain 2 ----
add("2.4", strong=["dumpster diving", "media reuse", "data remanence", "clearing and purging",
                   "magnetic media", "media viability"])
add("2.1", strong=["classification compartment", "least privilege", "need to know"])

# ---- Domain 3 ----
add("3.3", strong=["control objective", "control requirements"])
add("3.9", strong=["electrical power", "power outage", "voltage", "humidity range",
                   "operating humidity", "air conditioning", "electrostatic",
                   "fire detection", "fire suppression system", "fence height"])
add("3.5", strong=["buffer overflow"])

# ---- Domain 4 ----
add("4.1", strong=[
    "osi", "iso/osi", "tcp", "udp", "ip header", "ipv4", "ipv6", "icmp", "arp", "rarp",
    "dhcp", "dns", "snmp", "ntp", "bgp", "ospf", "rip", "eigrp", "datagram",
    "subnet mask", "default gateway", "three-way handshake", "three way handshake",
    "well-known port", "port number", "network layer", "transport layer",
    "data link layer", "physical layer", "session layer", "presentation layer",
    "application layer", "source ip", "destination ip", "packet header",
])
add("4.2", strong=["hids", "nids", "host-based intrusion", "network-based intrusion",
                   "signature-based", "anomaly detection", "behavioral-based",
                   "knowledge-based", "behavior-based", "ids"])
add("4.3", strong=["smtp", "pop3", "imap", "http", "email gateway", "send email",
                   "circuit level proxy", "application level proxy"])
add("4.1", strong=["tftp", "ftp", "telnet"])

# ---- Domain 5 ----
add("5.2", strong=["log-on", "logon", "same password", "password policy", "account lockout"])
add("5.4", strong=["content-dependent protection"])

# ---- Domain 6 ----
add("6.2", strong=["penetration", "vulnerability scanner", "network scanner"])
add("6.5", strong=["audit scope", "audit report"])
add("6.3", strong=["security metrics"])
add("6.4", strong=["remediation plan"])

# ---- Domain 7 ----
add("7.5", strong=["cluster", "server cluster", "raid level", "striping", "mirroring",
                   "fault tolerance"])
add("7.7", strong=["ids", "ips", "signature-based detection", "anomaly-based",
                   "knowledge-based ids", "behavior-based"])
add("7.1", strong=["computer crime", "evidence integrity"])
add("7.2", strong=["monitoring system", "network monitoring"])

# ---- Domain 8 ----
add("8.1", strong=["compiler", "interpreter", "compiled code", "interpreted code",
                   "expert system", "application control", "business process",
                   "application development", "programming", "source code",
                   "object-oriented", "java", "cobol", "c++", "bottom-up", "top-down",
                   "software testing approach", "database management system", "dbms"])
add("8.5", strong=["denormaliz", "normalization", "denormalized", "column", "columns",
                   "input accuracy", "information accuracy", "application control",
                   "table", "row", "tuple", "attribute", "schema", "primary key",
                   "foreign key", "referential integrity", "concurrency", "acid",
                   "polyinstantiation", "inference", "aggregation", "transaction",
                   "database security", "weakest link", "best programming",
                   "structured query language", "sql"])
add("8.2", strong=["configuration process", "software configuration", "change control board"])
add("8.3", strong=["software testing", "bottom-up testing", "top-down testing",
                   "functional testing", "white box testing"])
add("8.4", strong=["third party", "purchased software"])

# ---- write back ----
out = io.StringIO()
out.write('"""\n')
out.write("Curated within-domain keywords for CISSP sub-section classification.\n\n")
out.write("Two tiers per sub-section:\n")
out.write("  strong : distinctive, decisive vocabulary (word-boundary matched)\n")
out.write("  weak   : supporting vocabulary that only counts if a strong term already hit\n\n")
out.write("Scoring: question text x3, options x1, explanation x0.25.\n")
out.write('"""\n\nSUBSEC_TERMS = {\n')
for sid in sorted(T, key=lambda s: (int(s.split(".")[0]), int(s.split(".")[1]))):
    out.write(f"    {sid!r}: {{\n")
    for tier in ("strong", "weak"):
        vals = T[sid][tier]
        out.write(f"        {tier!r}: [\n")
        line = "            "
        for v in vals:
            piece = repr(v) + ", "
            if len(line) + len(piece) > 100:
                out.write(line.rstrip() + "\n")
                line = "            "
            line += piece
        if line.strip():
            out.write(line.rstrip() + "\n")
        out.write("        ],\n")
    out.write("    },\n")
out.write("}\n")

open(BASE + r"\subsection_keywords.py", "w", encoding="utf-8").write(out.getvalue())
print("patched subsection_keywords.py")
print("sections:", len(T))
print("strong terms:", sum(len(v["strong"]) for v in T.values()))
print("weak terms  :", sum(len(v["weak"]) for v in T.values()))
