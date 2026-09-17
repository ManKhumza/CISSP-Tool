"""
FIXED CISSP Sub-Section Classifier
===================================
Addresses over-classification issues by:
1. Using more specific keyword phrases
2. Adding negative/exclusion keywords  
3. Requiring higher score thresholds
4. Better discrimination between similar sections
"""

import re
import json
from collections import defaultdict

# Read the raw text
with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Parse questions
def parse_question_blocks(text):
    blocks = []
    pattern = r'QUESTION\s+(\d+)\s*-\s*\(Topic\s+(\d+)\)'
    parts = re.split(pattern, text)
    
    for i in range(1, len(parts), 3):
        if i + 2 < len(parts):
            content = parts[i + 2]
            next_q = re.search(r'\nQUESTION \d+ - \(Topic \d+\)', content)
            if next_q:
                content = content[:next_q.start()]
            blocks.append({
                "question_number": int(parts[i]),
                "topic": int(parts[i + 1]),
                "content": content.strip()
            })
    return blocks

def clean_content(content):
    content = re.sub(r'ISC CISSP\s*\n.*?CERT EMPIRE\s*\d+', '', content, flags=re.DOTALL)
    content = re.sub(r'"Best Material, Great Results"\.\s*CERT EMPIRE\s*\d+', '', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def fix_spacing(text):
    fixes = {
        r'\bs hielde d\b': 'shielded', r'\bt h at\b': 'that', r'\bt h e\b': 'the',
        r'\ba n d\b': 'and', r'\bo f\b': 'of', r'\bi n\b': 'in', r'\bi s\b': 'is',
        r'\bt o\b': 'to', r'\bf o r\b': 'for', r'\bw i t h\b': 'with',
        r'\bw h i c h\b': 'which', r'\bb e e n\b': 'been', r'\bb y\b': 'by',
        r'\bh a s\b': 'has', r'\bh a v e\b': 'have', r'\ba r e\b': 'are',
        r'\bw a s\b': 'was', r'\bc a n\b': 'can', r'\bw i l l\b': 'will',
        r'\bs h o u l d\b': 'should', r'\bf r o m\b': 'from', r'\bt h i s\b': 'this',
        r'\bw o u l d\b': 'would', r'\bc o u l d\b': 'could', r'\bm o r e\b': 'more',
        r'\bo n e\b': 'one', r'\ba l l\b': 'all', r'\bn o t\b': 'not',
        r'\bh a d\b': 'had', r'\ba l s o\b': 'also', r'\bv e r y\b': 'very',
        r'\bm u c h\b': 'much', r'\bl i k e\b': 'like', r'\bs u r e\b': 'sure',
    }
    for pat, repl in fixes.items():
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text

def parse_question_parts(content):
    content = fix_spacing(content)
    result = {"question_text": "", "options": [], "answer": "", "explanation": "", "has_explanation": False}
    
    options_start = re.search(r'\n?[A-D]\.', content)
    if options_start:
        result["question_text"] = content[:options_start.start()].strip()
        rest = content[options_start.start():]
    else:
        result["question_text"] = content[:200].strip()
        rest = ""
    
    for match in re.finditer(r'([A-D])\.\s*(.+?)(?=\n?[A-D]\.|\n?Answer:|\Z)', rest, re.DOTALL):
        result["options"].append({"letter": match.group(1), "text": match.group(2).strip()})
    
    answer_match = re.search(r'Answer:\s*([A-D])', content)
    if answer_match:
        result["answer"] = answer_match.group(1)
    
    expl_idx = content.find("Explanation:")
    if expl_idx >= 0:
        expl_text = content[expl_idx + len("Explanation:"):].strip()
        cut_markers = ["Source:", "Reference(s)", "The following reference", "QUESTION ", "\nISC CISSP"]
        cut_pos = len(expl_text)
        for marker in cut_markers:
            pos = expl_text.find(marker)
            if pos >= 0 and pos < cut_pos:
                cut_pos = pos
        expl_text = expl_text[:cut_pos].strip()
        expl_text = re.sub(r'^Explanation\s*:\s*', '', expl_text).strip()
        if len(expl_text) > 20:
            result["explanation"] = expl_text
            result["has_explanation"] = True
    
    return result

# ============================================================
# IMPROVED SECTION KEYWORDS - More specific, less overlap
# ============================================================

SECTION_KEYWORDS = {
    # DOMAIN 1: Security and Risk Management
    "1.1": {
        "strong": ["code of ethics", "(isc)2 ethics", "professional ethics", "ethical violation",
                   "ethics canon", "ethical responsibility", "report ethics"],
        "medium": ["ethics", "ethical conduct", "moral obligation"],
        "exclude": ["database", "network", "firewall", "encryption", "password"]
    },
    "1.2": {
        "strong": ["cia triad", "confidentiality integrity availability", "security concept",
                   "non-repudiation", "accountability principle", "authenticity security"],
        "medium": ["confidentiality", "integrity", "availability", "aaa model"],
        "exclude": ["database", "sql", "table", "query", "programming"]
    },
    "1.3": {
        "strong": ["security governance", "governance framework", "steering committee",
                   "board of directors security", "executive management security",
                   "strategic alignment security"],
        "medium": ["governance", "enterprise governance"],
        "exclude": ["database", "network protocol", "encryption algorithm"]
    },
    "1.4": {
        "strong": ["legal requirement", "regulatory compliance", "due diligence", "due care",
                   "intellectual property", "copyright law", "trademark law", "patent law",
                   "trade secret", "privacy law", "gdpr", "hipaa regulation", "sox compliance",
                   "computer crime law", "cybercrime legislation", "evidence admissibility",
                   "e-discovery", "legal hold", "licensing agreement",
                   "negligence liability", "civil law", "criminal law", "administrative law"],
        "medium": ["legal", "regulation", "compliance", "law", "liability"],
        "exclude": ["database query", "network topology", "encryption key"]
    },
    "1.5": {
        "strong": ["investigation type", "criminal investigation", "civil investigation",
                   "administrative investigation", "regulatory investigation",
                   "burden of proof", "preponderance of evidence", "beyond reasonable doubt"],
        "medium": ["investigation", "evidence standard"],
        "exclude": ["database", "network", "encryption"]
    },
    "1.6": {
        "strong": ["security policy document", "security standard document", "security procedure",
                   "security guideline", "acceptable use policy", "information security policy",
                   "policy development process", "policy implementation", "policy hierarchy"],
        "medium": ["policy", "standard", "procedure", "guideline", "baseline"],
        "exclude": ["database schema", "network configuration", "encryption algorithm"]
    },
    "1.7": {
        "strong": ["business impact analysis", "bia", "maximum tolerable downtime", "mtd",
                   "recovery time objective", "rto", "recovery point objective", "rpo",
                   "business continuity requirement", "continuity planning"],
        "medium": ["business continuity", "bcp", "continuity requirement"],
        "exclude": ["database", "network security", "encryption"]
    },
    "1.8": {
        "strong": ["personnel security", "background check", "background investigation",
                   "reference check", "employment agreement", "non-disclosure agreement",
                   "nda", "job rotation", "mandatory vacation", "separation of duties personnel",
                   "employee termination", "exit interview", "termination procedure"],
        "medium": ["personnel", "employee screening", "hiring process"],
        "exclude": ["database", "network", "encryption", "software"]
    },
    "1.9": {
        "strong": ["risk assessment", "risk analysis quantitative", "risk analysis qualitative",
                   "annualized loss expectancy", "ale", "single loss expectancy", "sle",
                   "annualized rate of occurrence", "aro", "exposure factor ef",
                   "risk mitigation strategy", "risk transfer insurance", "risk avoidance",
                   "risk acceptance residual", "risk appetite tolerance", "iso 31000",
                   "nist risk management framework", "risk register"],
        "medium": ["quantitative risk", "qualitative risk", "risk treatment"],
        "exclude": ["database", "sql", "table", "query", "network protocol", "encryption cipher"]
    },
    "1.10": {
        "strong": ["threat modeling", "stride model", "dread model", "pasta methodology",
                   "attack tree analysis", "attack surface analysis", "threat intelligence feed"],
        "medium": ["threat model", "threat actor profile"],
        "exclude": ["database", "network firewall"]
    },
    "1.11": {
        "strong": ["supply chain risk", "scrm", "vendor risk assessment", "third-party risk",
                   "supplier risk", "outsourcing risk management", "supply chain attack"],
        "medium": ["supply chain", "vendor assessment"],
        "exclude": ["database", "encryption"]
    },
    "1.12": {
        "strong": ["security awareness program", "security training program", "security education",
                   "awareness campaign", "phishing awareness training", "social engineering awareness"],
        "medium": ["awareness", "training", "education program"],
        "exclude": ["database", "network", "encryption"]
    },
    
    # DOMAIN 2: Asset Security
    "2.1": {
        "strong": ["asset classification", "data classification level", "classification label",
                   "classification scheme", "sensitivity label", "top secret", "secret classification",
                   "proprietary data", "government classification system"],
        "medium": ["classification", "labeling", "sensitivity"],
        "exclude": ["network protocol", "encryption algorithm", "database query"]
    },
    "2.2": {
        "strong": ["handling requirement", "data handling procedure", "media handling",
                   "protection requirement data", "acceptable use data"],
        "medium": ["handling", "data protection requirement"],
        "exclude": ["database", "network", "encryption"]
    },
    "2.3": {
        "strong": ["provision resources", "resource allocation secure", "capacity planning security"],
        "medium": ["provisioning", "resource management"],
        "exclude": ["database", "network"]
    },
    "2.4": {
        "strong": ["data lifecycle management", "data destruction secure", "data sanitization",
                   "data remanence", "purge data", "wipe data secure", "degauss media",
                   "crypto-shredding", "secure deletion", "media disposal"],
        "medium": ["lifecycle", "sanitization", "destruction", "disposal", "remanence"],
        "exclude": ["database query", "network protocol"]
    },
    "2.5": {
        "strong": ["retention policy", "retention schedule", "record retention requirement",
                   "retention period legal", "legal hold data"],
        "medium": ["retention", "archive policy"],
        "exclude": ["database", "network"]
    },
    "2.6": {
        "strong": ["data security control", "compliance requirement data", "data governance framework"],
        "medium": ["data compliance", "data protection standard"],
        "exclude": ["database", "network"]
    },
    
    # DOMAIN 3: Security Architecture and Engineering
    "3.1": {
        "strong": ["secure design principle", "defense in depth", "layered security architecture",
                   "fail safe mechanism", "fail secure design", "least privilege design",
                   "economy of mechanism", "complete mediation", "open design principle",
                   "psychological acceptability security", "security by design"],
        "medium": ["design principle", "secure architecture"],
        "exclude": ["database query", "network routing"]
    },
    "3.2": {
        "strong": ["bell-lapadula model", "biba model", "clark-wilson model", "brewer-nash model",
                   "chinese wall model", "state machine security model", "information flow model",
                   "non-interference model", "take-grant model", "lattice-based access model"],
        "medium": ["security model", "formal security model"],
        "exclude": ["database", "network protocol"]
    },
    "3.3": {
        "strong": ["control selection criteria", "control baseline nist", "nist 800-53 control",
                   "technical control selection", "administrative control selection",
                   "preventive control type", "detective control type", "corrective control type",
                   "deterrent control", "compensating control"],
        "medium": ["control selection", "control type"],
        "exclude": ["database", "encryption algorithm"]
    },
    "3.4": {
        "strong": ["common criteria evaluation", "evaluation assurance level", "eal rating",
                   "orange book tcsec", "trusted computing base tcb", "security kernel",
                   "reference monitor concept", "protection profile common criteria",
                   "target of evaluation toe", "its evaluation criteria"],
        "medium": ["common criteria", "tcsec", "trusted computing"],
        "exclude": ["database query", "network firewall"]
    },
    "3.5": {
        "strong": ["vulnerability architecture", "design vulnerability", "buffer overflow vulnerability",
                   "race condition vulnerability", "time-of-check time-of-use", "toc/tou attack",
                   "injection flaw design", "web application vulnerability architecture",
                   "mobile vulnerability architecture", "embedded system vulnerability"],
        "medium": ["architecture vulnerability", "design flaw"],
        "exclude": ["database normal", "network routing"]
    },
    "3.6": {
        "strong": ["symmetric encryption algorithm", "asymmetric encryption algorithm",
                   "aes encryption", "des encryption", "3des triple des", "rsa algorithm",
                   "elliptic curve cryptography", "ecc crypto", "diffie-hellman key exchange",
                   "block cipher mode", "cbc mode", "ctr mode", "gcm mode",
                   "hash function sha", "sha-256", "md5 hash", "hmac",
                   "digital signature algorithm", "public key infrastructure pki",
                   "certificate authority ca", "key escrow recovery",
                   "fips 140 cryptographic module", "transport layer encryption",
                   "data at rest encryption", "end-to-end encryption design"],
        "medium": ["encryption", "cryptography", "cipher", "hash function"],
        "exclude": ["database table", "network routing protocol", "access control policy"]
    },
    "3.7": {
        "strong": ["cryptanalytic attack", "brute force cryptanalysis", "known plaintext attack crypto",
                   "chosen plaintext attack", "chosen ciphertext attack",
                   "side-channel attack timing", "power analysis attack crypto",
                   "differential cryptanalysis", "linear cryptanalysis",
                   "birthday attack collision", "rainbow table attack hash",
                   "frequency analysis cipher"],
        "medium": ["cryptanalysis", "crypto attack"],
        "exclude": ["database", "network firewall"]
    },
    "3.8": {
        "strong": ["site design security", "facility design secure", "cpted crime prevention",
                   "site selection security", "facility layout secure"],
        "medium": ["site design", "facility planning"],
        "exclude": ["database", "network"]
    },
    "3.9": {
        "strong": ["physical access control facility", "fencing perimeter", "security lighting facility",
                   "mantrap entry", "turnstile access", "badge reader physical",
                   "cctv surveillance camera", "motion detector alarm",
                   "fire detection system", "smoke detector facility", "sprinkler suppression",
                   "fm-200 gaseous suppression", "halon replacement",
                   "hvac security facility", "ups uninterruptible power",
                   "emi shielding tempest", "faraday cage", "raised floor data center"],
        "medium": ["physical security", "facility control", "perimeter security"],
        "exclude": ["database", "network protocol"]
    },
    
    # DOMAIN 4: Communication and Network Security
    "4.1": {
        "strong": ["network architecture design", "secure network design", "network segmentation vlan",
                   "dmz demilitarized zone", "screened subnet", "osi model layer",
                   "tcp/ip model layer", "network topology design", "zero trust network architecture",
                   "software-defined networking sdn", "microsegmentation network"],
        "medium": ["network architecture", "network design", "osi model"],
        "exclude": ["database", "encryption algorithm", "access control policy"]
    },
    "4.2": {
        "strong": ["firewall packet filter", "stateful inspection firewall", "application firewall waf",
                   "intrusion detection system ids", "intrusion prevention system ips",
                   "router security hardening", "switch security port", "proxy server network",
                   "load balancer security", "network access control nac",
                   "unified threat management utm"],
        "medium": ["firewall", "ids", "ips", "network device security"],
        "exclude": ["database", "encryption key"]
    },
    "4.3": {
        "strong": ["vpn virtual private network", "ipsec tunnel", "ssl vpn", "tls vpn",
                   "ssh secure shell", "sftp secure ftp", "wpa2 wireless encryption",
                   "wpa3 wireless", "802.1x network authentication", "radius network auth",
                   "dnssec dns security", "s/mime email encryption", "pgp email encryption"],
        "medium": ["vpn", "secure channel", "encrypted communication"],
        "exclude": ["database", "access control"]
    },
    
    # DOMAIN 5: Identity and Access Management
    "5.1": {
        "strong": ["physical access control asset", "logical access control asset",
                   "access control mechanism", "privileged access management pam"],
        "medium": ["access control", "restrict access"],
        "exclude": ["database query", "network firewall", "encryption"]
    },
    "5.2": {
        "strong": ["authentication factor", "something you know have are",
                   "multi-factor authentication mfa", "two-factor authentication 2fa",
                   "biometric fingerprint", "biometric retina scan", "biometric iris recognition",
                   "smart card token", "password passphrase pin"],
        "medium": ["authentication", "identify user", "biometric"],
        "exclude": ["database", "network protocol", "encryption algorithm"]
    },
    "5.3": {
        "strong": ["federated identity", "identity federation", "saml assertion",
                   "oauth authorization", "openid connect oidc", "identity provider idp",
                   "service provider sp federation", "cross-domain federation"],
        "medium": ["federation", "saml", "oauth", "openid"],
        "exclude": ["database", "network firewall", "encryption key"]
    },
    "5.4": {
        "strong": ["discretionary access control dac", "mandatory access control mac",
                   "role-based access control rbac", "attribute-based access control abac",
                   "rule-based access control", "access control matrix", "access control list acl",
                   "capability table access"],
        "medium": ["dac", "mac", "rbac", "abac", "authorization mechanism"],
        "exclude": ["database query", "network protocol"]
    },
    "5.5": {
        "strong": ["account provisioning", "account deprovisioning", "identity lifecycle",
                   "access review certification", "entitlement review", "role mining engineering"],
        "medium": ["provisioning", "deprovisioning", "access review"],
        "exclude": ["database", "network", "encryption"]
    },
    "5.6": {
        "strong": ["kerberos authentication", "radius authentication server", "tacacs+ authentication",
                   "ldap directory authentication", "active directory authentication",
                   "single sign-on sso implementation", "type i error biometric",
                   "type ii error biometric", "false acceptance rate far",
                   "false rejection rate frr", "crossover error rate cer eer"],
        "medium": ["authentication system", "sso", "kerberos", "radius", "tacacs"],
        "exclude": ["database", "network firewall"]
    },
    
    # DOMAIN 6: Security Assessment and Testing
    "6.1": {
        "strong": ["assessment strategy design", "test strategy validation", "audit strategy plan"],
        "medium": ["assessment strategy", "test strategy"],
        "exclude": ["database", "network"]
    },
    "6.2": {
        "strong": ["vulnerability scanning assessment", "penetration testing methodology",
                   "ethical hacking test", "black box penetration", "white box penetration",
                   "gray box penetration", "social engineering test phishing",
                   "wireless penetration test", "web application penetration"],
        "medium": ["penetration test", "vulnerability scan", "security testing"],
        "exclude": ["database query", "encryption algorithm"]
    },
    "6.3": {
        "strong": ["security metric collection", "key performance indicator kpi security",
                   "key risk indicator kri", "log collection security"],
        "medium": ["metric", "kpi", "kri"],
        "exclude": ["database", "network"]
    },
    "6.4": {
        "strong": ["test output analysis", "vulnerability report generation",
                   "penetration test report", "cvss scoring", "false positive analysis",
                   "remediation recommendation report"],
        "medium": ["test report", "finding report"],
        "exclude": ["database", "encryption"]
    },
    "6.5": {
        "strong": ["security audit process", "internal audit security", "external audit security",
                   "compliance audit security", "iso 19011 audit", "audit evidence collection"],
        "medium": ["audit", "auditor"],
        "exclude": ["database", "network"]
    },
    
    # DOMAIN 7: Security Operations
    "7.1": {
        "strong": ["digital forensic investigation", "chain of custody evidence",
                   "evidence preservation forensic", "forensic analysis tool",
                   "order of volatility forensic", "forensic imaging copy"],
        "medium": ["forensic", "investigation digital", "evidence"],
        "exclude": ["database query", "network protocol"]
    },
    "7.2": {
        "strong": ["siem security information event management", "log analysis monitoring",
                   "syslog collection", "user behavior analytics uba",
                   "anomaly detection monitoring", "alert triage security"],
        "medium": ["logging", "monitoring", "siem"],
        "exclude": ["database", "encryption"]
    },
    "7.3": {
        "strong": ["configuration management cm", "configuration baseline secure",
                   "configuration management database cmdb", "configuration drift detection",
                   "hardening standard baseline"],
        "medium": ["configuration management", "configuration baseline"],
        "exclude": ["database query", "network routing"]
    },
    "7.4": {
        "strong": ["need-to-know principle", "least privilege operation", "separation of duties operation",
                   "dual control two-person", "split knowledge principle", "mandatory vacation operation"],
        "medium": ["operational security", "foundational operations"],
        "exclude": ["database", "network"]
    },
    "7.5": {
        "strong": ["backup strategy full incremental differential", "tape rotation grandfather-father-son",
                   "raid disk redundancy", "fault tolerance high availability",
                   "media management protection"],
        "medium": ["backup", "restore", "redundancy"],
        "exclude": ["database query", "network protocol"]
    },
    "7.6": {
        "strong": ["incident response plan", "csirt cert team", "incident containment eradication",
                   "lessons learned incident", "incident escalation procedure"],
        "medium": ["incident response", "incident management"],
        "exclude": ["database", "encryption"]
    },
    "7.7": {
        "strong": ["anti-malware antivirus", "endpoint detection response edr",
                   "honeypot honeynet deception", "file integrity monitoring fim",
                   "data loss prevention dlp", "sandbox malware analysis"],
        "medium": ["detective measure", "preventative measure"],
        "exclude": ["database", "network protocol"]
    },
    "7.8": {
        "strong": ["patch management process", "vulnerability remediation patch",
                   "zero-day vulnerability patch", "emergency patch deployment"],
        "medium": ["patch management", "vulnerability management"],
        "exclude": ["database", "network"]
    },
    "7.9": {
        "strong": ["change management process", "change advisory board cab",
                   "change request approval", "release management deployment"],
        "medium": ["change management", "change control"],
        "exclude": ["database", "encryption"]
    },
    "7.10": {
        "strong": ["hot site warm site cold site", "reciprocal agreement recovery",
                   "mirrored site recovery", "mobile recovery site"],
        "medium": ["recovery strategy", "recovery site"],
        "exclude": ["database", "network"]
    },
    "7.11": {
        "strong": ["disaster recovery plan drp", "disaster declaration activation",
                   "drp implementation procedure", "salvage team recovery"],
        "medium": ["disaster recovery", "drp"],
        "exclude": ["database", "encryption"]
    },
    "7.12": {
        "strong": ["drp test tabletop exercise", "parallel disaster recovery test",
                   "full interruption drp test", "simulation disaster test"],
        "medium": ["drp test", "disaster recovery test"],
        "exclude": ["database", "network"]
    },
    "7.13": {
        "strong": ["business continuity plan bcp", "continuity of operations coop",
                   "crisis management plan", "pandemic continuity planning"],
        "medium": ["business continuity", "bcp exercise"],
        "exclude": ["database", "network"]
    },
    "7.14": {
        "strong": ["physical security perimeter", "fencing gate bollard", "security guard patrol",
                   "cctv surveillance physical", "fire extinguisher type", "sprinkler system physical"],
        "medium": ["physical security", "facility protection"],
        "exclude": ["database", "network protocol"]
    },
    "7.15": {
        "strong": ["personnel safety workplace", "emergency evacuation plan",
                   "workplace violence prevention", "travel security employee",
                   "osha occupational safety"],
        "medium": ["safety", "employee safety"],
        "exclude": ["database", "network"]
    },
    
    # DOMAIN 8: Software Development Security
    "8.1": {
        "strong": ["software development life cycle sdlc", "waterfall sdlc model",
                   "agile scrum devops", "devsecops integration", "spiral development model",
                   "v-model sdlc", "rapid application development rad"],
        "medium": ["sdlc", "development lifecycle"],
        "exclude": ["network protocol", "encryption algorithm"]
    },
    "8.2": {
        "strong": ["development environment security", "ci/cd pipeline security",
                   "version control repository security", "build process security",
                   "container orchestration security development"],
        "medium": ["development environment", "ci/cd"],
        "exclude": ["database query", "network firewall"]
    },
    "8.3": {
        "strong": ["static application security testing sast", "dynamic application security testing dast",
                   "interactive application security testing iast", "software composition analysis sca",
                   "code review security", "fuzz testing mutation"],
        "medium": ["code review", "sast", "dast", "security testing software"],
        "exclude": ["database", "network"]
    },
    "8.4": {
        "strong": ["commercial off-the-shelf cots security", "open source software security acquisition",
                   "third-party component security", "software supply chain acquired",
                   "outsourced development security"],
        "medium": ["acquired software", "third-party software"],
        "exclude": ["database", "network"]
    },
    "8.5": {
        "strong": ["secure coding practice", "input validation output encoding",
                   "parameterized query prepared statement", "sql injection prevention code",
                   "cross-site scripting xss prevention", "buffer overflow prevention code",
                   "owasp secure coding", "error handling secure coding"],
        "medium": ["secure coding", "input validation", "sql injection prevention"],
        "exclude": ["database administration", "network routing"]
    }
}

def classify_subsection_improved(question_text, explanation_text):
    """Improved classifier with exclusion keywords and higher thresholds"""
    qt_lower = question_text.lower()
    expl_lower = (explanation_text or "").lower()
    combined = qt_lower + " " + expl_lower
    
    scores = {}
    for section_id, kw_groups in SECTION_KEYWORDS.items():
        score = 0
        
        # Check exclusions first - if any exclusion keyword is found, skip this section
        excluded = False
        for excl in kw_groups.get("exclude", []):
            if excl in combined:
                # Only exclude if it's clearly dominant (appears multiple times or in question text)
                if excl in qt_lower or combined.count(excl) > 1:
                    excluded = True
                    break
        
        if excluded:
            continue
        
        # Question text keywords (2x weight)
        for kw in kw_groups["strong"]:
            count = qt_lower.count(kw)
            if count > 0:
                score += 10 * count  # 5 * 2 * count
        for kw in kw_groups["medium"]:
            count = qt_lower.count(kw)
            if count > 0:
                score += 4 * count   # 2 * 2 * count
        
        # Explanation keywords (1x weight)
        for kw in kw_groups["strong"]:
            count = expl_lower.count(kw)
            if count > 0:
                score += 5 * count
        for kw in kw_groups["medium"]:
            count = expl_lower.count(kw)
            if count > 0:
                score += 2 * count
        
        if score > 0:
            scores[section_id] = score
    
    if not scores:
        return None
    
    best = max(scores.items(), key=lambda x: x[1])
    
    # Require minimum score threshold to avoid weak matches
    if best[1] < 8:  # At least one strong keyword in question or equivalent
        return None
    
    return best[0]

def main():
    print("=== IMPROVED SUB-SECTION CLASSIFIER ===\n")
    
    blocks = parse_question_blocks(raw_text)
    print(f"Parsed {len(blocks)} questions\n")
    
    section_data = defaultdict(list)
    unmatched = 0
    stats = defaultdict(lambda: {"total": 0, "no_explanation": 0})
    
    for i, block in enumerate(blocks):
        if (i + 1) % 500 == 0:
            print(f"Processing {i+1}/{len(blocks)}...")
        
        content = clean_content(block["content"])
        parsed = parse_question_parts(content)
        
        section = classify_subsection_improved(parsed["question_text"], parsed["explanation"])
        
        if section is None:
            unmatched += 1
            section = "unclassified"
        
        domain_num = section.split(".")[0] if section != "unclassified" else "?"
        
        q_data = {
            "question_number": block["question_number"],
            "original_topic": block["topic"],
            "section": section,
            "domain": f"Domain {domain_num}",
            "question_text": parsed["question_text"],
            "options": parsed["options"],
            "answer": parsed["answer"],
            "explanation": parsed["explanation"],
            "has_explanation": parsed["has_explanation"]
        }
        
        section_data[section].append(q_data)
        stats[section]["total"] += 1
        if not parsed["has_explanation"]:
            stats[section]["no_explanation"] += 1
    
    print(f"\nClassification complete.")
    print(f"Unmatched: {unmatched} ({unmatched/len(blocks)*100:.1f}%)\n")
    
    # Print distribution
    print(f"{'Section':<8} {'Count':>6} {'Missing':>8}")
    print("-" * 25)
    
    total_q = 0
    total_missing = 0
    
    def sort_key(s):
        if s == "unclassified":
            return (999, 0)
        parts = s.split(".")
        return (int(parts[0]), int(parts[1]))
    
    for sec_id in sorted(section_data.keys(), key=sort_key):
        s = stats[sec_id]
        total_q += s["total"]
        total_missing += s["no_explanation"]
        print(f"{sec_id:<8} {s['total']:>6} {s['no_explanation']:>8}")
    
    print("-" * 25)
    print(f"TOTAL:   {total_q:>6} {total_missing:>8}")
    
    # Show samples from problematic sections
    print("\n=== SAMPLE CHECKS ===")
    for check_sec in ["1.9", "3.6", "5.3"]:
        qs = section_data.get(check_sec, [])
        print(f"\n{check_sec}: {len(qs)} questions")
        for q in qs[:3]:
            print(f"  Q{q['question_number']}: {q['question_text'][:100]}...")
    
    # Save improved data
    output = {
        "metadata": {
            "total_questions": total_q,
            "total_sections": len(section_data),
            "missing_explanations": total_missing,
            "unmatched_questions": unmatched,
            "classification_note": "Improved classification with exclusion keywords and higher thresholds"
        },
        "sections": {}
    }
    
    for sec_id in sorted(section_data.keys(), key=sort_key):
        qs = section_data[sec_id]
        output["sections"][sec_id] = {
            "question_count": len(qs),
            "missing_explanations": stats[sec_id]["no_explanation"],
            "questions": qs
        }
    
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\subsection_organized_v2.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {json_path}")

if __name__ == "__main__":
    main()
