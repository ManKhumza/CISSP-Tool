"""
CORRECTED CISSP Question Organizer

Issues found and fixed:
1. Domain mapping was based on original "Topic" numbers which don't correspond to CISSP domains
   FIX: Classify each question individually using comprehensive keyword analysis
2. Some questions lack explanations in the source document
   FIX: Mark these clearly in output
3. Answer options were merged in raw text extraction 
   FIX: Better parsing with split logic for merged options
"""

import re
import json
from collections import defaultdict

def read_raw_text():
    try:
        with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_question_blocks(text):
    """Parse text into question blocks using QUESTION X - (Topic Y) pattern"""
    blocks = []
    pattern = r'QUESTION\s+(\d+)\s*-\s*\(Topic\s+(\d+)\)'
    
    parts = re.split(pattern, text)
    
    for i in range(1, len(parts), 3):
        if i + 2 < len(parts):
            blocks.append({
                "question_number": int(parts[i]),
                "topic": int(parts[i + 1]),
                "content": parts[i + 2].strip()
            })
    
    return blocks

def clean_question_content(content):
    """Remove page headers/footers and excessive whitespace"""
    # Remove page markers like "ISC CISSP" blocks
    content = re.sub(r'ISC CISSP\s*\n.*?CERT EMPIRE\s*\d+', '', content, flags=re.DOTALL)
    content = re.sub(r'https://certempire\.com/\s*\d+', '', content)
    content = re.sub(r'"Best Material, Great Results"\.?\s*CERT\s*EMP(?:IRE)?\s*\d+', '', content, flags=re.IGNORECASE)
    content = re.sub(r'ISC CISSP\s*\n.*?https://certempire', '', content, flags=re.DOTALL)
    
    # Normalize whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    
    return content.strip()

def fix_merged_options(content):
    """Fix merged options like 'B. Social EngineeringC. Object reuse'"""
    # Pattern: uppercase letter followed by period and text, then another uppercase letter+period
    # Insert newlines between merged options
    content = re.sub(r'([A-D])\.\s*(.*?)([A-D])\.', r'\1. \2\n\3.', content)
    return content

def fix_spacing_issues(content):
    """Fix common spacing artifacts from PDF extraction"""
    # Single character followed by space patterns
    fixes = [
        (r'\bs hielde d\b', 'shielded'),
        (r'\bt h at\b', 'that'),
        (r'\bt h e\b', 'the'),
        (r'\ba n d\b', 'and'),
        (r'\bo f\b', 'of'),
        (r'\bi n\b', 'in'),
        (r'\bi s\b', 'is'),
        (r'\bt o\b', 'to'),
        (r'\bf o r\b', 'for'),
        (r'\bw i t h\b', 'with'),
        (r'\bw h i c h\b', 'which'),
        (r'\bb e e n\b', 'been'),
        (r'\bb y\b', 'by'),
        (r'\bh a s\b', 'has'),
        (r'\bh a v e\b', 'have'),
        (r'\ba r e\b', 'are'),
        (r'\bw a s\b', 'was'),
        (r'\bc a n\b', 'can'),
        (r'\bw i l l\b', 'will'),
        (r'\bs h o u l d\b', 'should'),
        (r'\bf r o m\b', 'from'),
        (r'\bt h i s\b', 'this'),
        (r'\bw o u l d\b', 'would'),
        (r'\bc o u l d\b', 'could'),
        (r'\bm o r e\b', 'more'),
        (r'\bo n e\b', 'one'),
        (r'\ba l l\b', 'all'),
        (r'\bn o t\b', 'not'),
        (r'\bh a d\b', 'had'),
        (r'\ba l s o\b', 'also'),
        (r'\bw h e r e\b', 'where'),
        (r'\bw h a t\b', 'what'),
        (r'\bw h e n\b', 'when'),
        (r'\bw h o\b', 'who'),
        (r'\bt h e i r\b', 'their'),
        (r'\bt h e y\b', 'they'),
        (r'\bt h e r e\b', 'there'),
        (r'\bs o m e\b', 'some'),
        (r'\bm a y\b', 'may'),
        (r'\bm u s t\b', 'must'),
        (r'\bm i g h t\b', 'might'),
        (r'\bs u c h\b', 'such'),
        (r'\be a c h\b', 'each'),
        (r'\ba n y\b', 'any'),
        (r'\bm o s t\b', 'most'),
        (r'\bo n l y\b', 'only'),
        (r'\bb u t\b', 'but'),
        (r'\ba f t e r\b', 'after'),
        (r'\bb e f o r e\b', 'before'),
        (r'\bb e t w e e n\b', 'between'),
        (r'\bo v e r\b', 'over'),
        (r'\bu n d e r\b', 'under'),
        (r'\ba g a i n s t\b', 'against'),
        (r'\ba b o u t\b', 'about'),
        (r'\bi n t o\b', 'into'),
        (r'\bt h r o u g h\b', 'through'),
        (r'\bd u r i n g\b', 'during'),
        (r'\bw i t h o u t\b', 'without'),
        (r'\bh o w e v e r\b', 'however'),
        (r'\bt h e r e f o r e\b', 'therefore'),
        (r'\bb e c a u s e\b', 'because'),
        (r'\bw h i l e\b', 'while'),
        (r'\ba m o n g\b', 'among'),
        (r'\bw i t h i n\b', 'within'),
        (r'\ba w a y\b', 'away'),
        (r'\bb a c k\b', 'back'),
        (r'\bd o w n\b', 'down'),
        (r'\bo u t\b', 'out'),
        (r'\bo f f\b', 'off'),
        (r'\bo n c e\b', 'once'),
        (r'\bf i r s t\b', 'first'),
        (r'\bl a s t\b', 'last'),
        (r'\bn e x t\b', 'next'),
        (r'\bp a r t\b', 'part'),
        (r'\bm a d e\b', 'made'),
        (r'\bm a k e\b', 'make'),
        (r'\bt a k e\b', 'take'),
        (r'\bg i v e\b', 'give'),
        (r'\bc o m e\b', 'come'),
        (r'\bk n o w\b', 'know'),
        (r'\bs e e\b', 'see'),
        (r'\bu s e\b', 'use'),
        (r'\bg e t\b', 'get'),
        (r'\bp u t\b', 'put'),
        (r'\bs e t\b', 'set'),
        (r'\bl e t\b', 'let'),
        (r'\br u n\b', 'run'),
        (r'\bs a y\b', 'say'),
        (r'\bt e l l\b', 'tell'),
        (r'\bf i n d\b', 'find'),
        (r'\bh e l p\b', 'help'),
        (r'\bn e e d\b', 'need'),
        (r'\bw a n t\b', 'want'),
        (r'\bl o o k\b', 'look'),
        (r'\bw o r k\b', 'work'),
        (r'\bc a l l\b', 'call'),
        (r'\bt r y\b', 'try'),
        (r'\ba s k\b', 'ask'),
        (r'\bs h o w\b', 'show'),
        (r'\bm e a n\b', 'mean'),
        (r'\bk e e p\b', 'keep'),
        (r'\bl e a v e\b', 'leave'),
        (r'\bs t i l l\b', 'still'),
        (r'\bj u s t\b', 'just'),
        (r'\bv e r y\b', 'very'),
        (r'\bm u c h\b', 'much'),
        (r'\bw e l l\b', 'well'),
        (r'\be v e n\b', 'even'),
        (r'\bo t h e r\b', 'other'),
        (r'\bo w n\b', 'own'),
        (r'\bs a m e\b', 'same'),
        (r'\bl i k e\b', 'like'),
        (r'\bs u r e\b', 'sure'),
        (r'\bl o n g\b', 'long'),
        (r'\bh i g h\b', 'high'),
        (r'\bl o w\b', 'low'),
        (r'\bl a r g e\b', 'large'),
        (r'\bs m a l l\b', 'small'),
        (r'\bf u l l\b', 'full'),
        (r'\bh a r d\b', 'hard'),
        (r'\be a s y\b', 'easy'),
        (r'\bs o f t\b', 'soft'),
        (r'\bf a s t\b', 'fast'),
        (r'\bs l o w\b', 'slow'),
        (r'\bw a r m\b', 'warm'),
        (r'\bc o l d\b', 'cold'),
        (r'\bf r e e\b', 'free'),
        (r'\bo p e n\b', 'open'),
        (r'\bc l o s e\b', 'close'),
        (r'\br e a d\b', 'read'),
        (r'\bw r i t e\b', 'write'),
    ]
    
    for pattern, replacement in fixes:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def classify_question_domain(content):
    """
    Classify a question into the correct CISSP domain based on content analysis.
    Uses comprehensive keyword matching with weights.
    """
    content_lower = content.lower()
    
    # Domain definitions with weighted keywords
    domains = {
        "Domain 1: Security and Risk Management": {
            "weight": 0,
            "high": ["risk management", "security governance", "compliance requirement", "legal requirement",
                     "regulatory requirement", "security policy", "corporate policy", "due diligence", "due care",
                     "personnel security", "security awareness", "professional ethics", "code of ethics",
                     "business continuity plan", "disaster recovery plan", "bcp", "drp",
                     "risk assessment", "risk analysis", "risk mitigation", "risk transfer", "risk acceptance",
                     "residual risk", "total risk", "annualized loss expectancy", "ale", "sle",
                     "single loss expectancy", "annualized rate of occurrence", "aro", "exposure factor",
                     "security framework", "iso 27001", "nist", "cobi", "itil",
                     "data owner", "data custodian", "data controller", "data processor",
                     "acceptable use policy", "security baseline", "security guideline", "security standard",
                     "security procedure", "information security policy", "privacy policy"],
            "medium": ["policy", "governance", "compliance", "regulation", "standard", "procedure",
                       "guideline", "baseline", "framework", "ethics", "negligence", "liability",
                       "risk", "threat", "vulnerability", "control", "countermeasure",
                       "confidentiality", "integrity", "availability", "cia triad", "cia",
                       "data classification", "information classification"]
        },
        "Domain 2: Asset Security": {
            "weight": 0,
            "high": ["asset classification", "asset inventory", "data classification level",
                     "information classification", "data labeling", "media labeling",
                     "data retention policy", "data destruction", "media sanitization",
                     "data remanence", "data at rest", "data in transit", "data in use",
                     "data lifecycle", "information lifecycle", "record retention",
                     "privacy requirement", "data privacy", "personally identifiable", "pii",
                     "protected health information", "phi", "data ownership",
                     "data handling", "data protection standard"],
            "medium": ["asset", "classification", "labeling", "ownership", "retention",
                       "sanitization", "destruction", "disposal", "privacy", "sensitive data",
                       "data classification", "information owner", "data steward"]
        },
        "Domain 3: Security Architecture and Engineering": {
            "weight": 0,
            "high": ["security architecture", "security engineering", "security model",
                     "cryptography", "encryption", "decryption", "cipher", "cryptosystem",
                     "key management", "key escrow", "key recovery", "public key infrastructure",
                     "pki", "digital signature", "digital certificate", "certificate authority",
                     "symmetric encryption", "asymmetric encryption", "hash function",
                     "security control framework", "security evaluation", "common criteria",
                     "orange book", "tcs", "its", "evaluation assurance level",
                     "trusted computing base", "tcb", "security kernel",
                     "bell-lapadula", "biba", "clark-wilson", "brewer-nash", "chinese wall",
                     "lattice-based", "state machine model", "information flow model",
                     "physical security", "facility design", "site security",
                     "fire suppression", "fire detection", "hvac", "power supply", "ups",
                     "mantrap", "turnstile", "fencing", "lighting", "guard",
                     "environmental control", "raised floor", "hot aisle", "cold aisle",
                     "faraday cage", "tempest", "white noise", "emanations",
                     "secure design principle", "defense in depth", "layered security",
                     "fail safe", "fail secure", "open design", "economy of mechanism",
                     "complete mediation", "psychological acceptability"],
            "medium": ["architecture", "engineering", "encryption", "crypto", "key", "algorithm",
                       "symmetric", "asymmetric", "hashing", "digital", "certificate",
                       "physical security", "facility", "fire", "biometric device",
                       "biometric system", "retina", "fingerprint", "iris scanner",
                       "hand geometry", "biometric", "token", "smart card",
                       "security model", "security control", "countermeasure selection"]
        },
        "Domain 4: Communication and Network Security": {
            "weight": 0,
            "high": ["network security", "network architecture", "network protocol",
                     "osi model", "tcp/ip", "tcp", "udp", "ip", "icmp",
                     "firewall", "packet filter", "stateful inspection", "proxy firewall",
                     "intrusion detection system", "ids", "intrusion prevention system", "ips",
                     "vpn", "virtual private network", "ipsec", "ssl", "tls",
                     "wireless security", "wep", "wpa", "wpa2", "802.11", "wireless",
                     "network attack", "denial of service", "dos", "ddos",
                     "man-in-the-middle", "spoofing", "sniffing", "arp poisoning",
                     "dns security", "dnssec", "dns poisoning", "dns spoofing",
                     "router security", "switch security", "vlan", "network segmentation",
                     "dmz", "network address translation", "nat", "proxy server",
                     "remote access", "dial-up", "isdn", "dsl", "frame relay",
                     "socks", "circuit-switched", "packet-switched", "x.25",
                     "ethernet", "token ring", "fddi", "mac address"],
            "medium": ["network", "communication", "protocol", "transmission", "packet",
                       "router", "switch", "bridge", "gateway", "firewall", "port",
                       "lan", "wan", "man", "vpn", "wireless", "bandwidth", "latency",
                       "throughput", "osi", "layer", "datalink", "transport", "session",
                       "presentation", "application", "physical layer", "network layer"]
        },
        "Domain 5: Identity and Access Management (IAM)": {
            "weight": 0,
            "high": ["access control", "authentication", "authorization", "accounting",
                     "identification", "identity management", "identity provider",
                     "single sign-on", "sso", "federated identity", "federation",
                     "saml", "oauth", "openid connect", "kerberos", "ldap", 
                     "radius", "tacacs", "diameter",
                     "discretionary access control", "dac", "mandatory access control", "mac",
                     "role-based access control", "rbac", "rule-based access control",
                     "attribute-based access control", "abac", "context-based access control",
                     "access control matrix", "capability table", "acl", "access control list",
                     "password policy", "password management", "multi-factor authentication",
                     "two-factor authentication", "2fa", "mfa", "biometric authentication",
                     "something you know", "something you have", "something you are",
                     "type i error", "type ii error", "false acceptance", "false rejection",
                     "crossover error rate", "cer", "eer", "frr", "far",
                     "separation of duties", "least privilege", "need to know",
                     "privileged account", "superuser", "administrator access"],
            "medium": ["access", "authenticate", "authorize", "identity", "credential",
                       "password", "passphrase", "pin", "token", "biometric",
                       "fingerprint", "retina scan", "iris recognition", "voice recognition",
                       "signature dynamic", "keystroke dynamic",
                       "facial recognition", "palm scan", "hand geometry",
                       "permission", "privilege", "right", "entitlement", "role",
                       "group membership", "directory service"]
        },
        "Domain 6: Security Assessment and Testing": {
            "weight": 0,
            "high": ["security assessment", "security testing", "security audit",
                     "vulnerability assessment", "vulnerability scanning",
                     "penetration testing", "pen test", "ethical hacking",
                     "security control testing", "control assessment",
                     "audit trail", "audit log", "security log", "log analysis",
                     "security metric", "kpi", "key performance indicator",
                     "security monitoring", "continuous monitoring",
                     "configuration audit", "compliance audit", "security review",
                     "code review", "static analysis", "dynamic analysis",
                     "fuzzing", "fuzz testing", "regression testing",
                     "test coverage", "test strategy", "test plan",
                     "social engineering test", "phishing simulation"],
            "medium": ["assessment", "testing", "audit", "scan", "vulnerability",
                       "penetration", "log", "monitoring", "metric", "measurement",
                       "review", "evaluation", "verification", "validation",
                       "security report", "test result", "audit finding"]
        },
        "Domain 7: Security Operations": {
            "weight": 0,
            "high": ["incident response", "incident management", "incident handling",
                     "forensic", "digital forensics", "chain of custody",
                     "evidence collection", "evidence preservation", "forensic investigation",
                     "disaster recovery", "disaster recovery plan", "drp", "bcp",
                     "business continuity", "business impact analysis", "bia",
                     "recovery time objective", "rto", "recovery point objective", "rpo",
                     "maximum tolerable downtime", "mtd", "maximum allowable downtime",
                     "backup", "restore", "backup strategy", "backup policy",
                     "change management", "configuration management", "patch management",
                     "problem management", "incident management", "release management",
                     "service desk", "help desk", "operations security",
                     "administrative management", "security operations center", "soc",
                     "physical security operations", "facility security",
                     "fire extinguisher", "sprinkler system", "fire suppression",
                     "water damage", "smoke detector", "halon", "fm-200"],
            "medium": ["operation", "incident", "disaster", "recovery", "continuity",
                       "backup", "restore", "patch", "update", "change", "configuration",
                       "maintenance", "troubleshooting", "investigation", "forensics",
                       "chain of custody", "evidence", "redundancy", "failover",
                       "hot site", "warm site", "cold site", "mirrored site",
                       "reciprocal agreement", "alternate processing site"]
        },
        "Domain 8: Software Development Security": {
            "weight": 0,
            "high": ["software development", "application security", "secure coding",
                     "sdlc", "system development life cycle", "software development lifecycle",
                     "devsecops", "secure devops", "ci/cd", "continuous integration",
                     "application vulnerability", "owasp", "sql injection", "cross-site scripting",
                     "xss", "cross-site request forgery", "csrf", "buffer overflow",
                     "input validation", "output encoding", "parameterized query",
                     "prepared statement", "stored procedure",
                     "database security", "relational database", "database management",
                     "database view", "database schema", "normalization", "tuple",
                     "primary key", "foreign key", "referential integrity",
                     "software capability maturity model", "cmm", "cmmi",
                     "change control", "configuration control", "version control",
                     "agile", "waterfall", "spiral", "prototyping", "devops",
                     "code signing", "code obfuscation", "software composition analysis"],
            "medium": ["software", "development", "application", "code", "programming",
                       "testing", "quality assurance", "debugging", "compiler", "interpreter",
                       "object-oriented", "java", "c++", "python", "api", "database",
                       "sql", "query", "schema", "table", "view", "record", "field",
                       "normalization", "transaction", "commit", "rollback"]
        }
    }
    
    # Score each domain
    for domain_name, domain_data in domains.items():
        score = 0
        # High-confidence keywords (weight 3)
        for kw in domain_data["high"]:
            if kw in content_lower:
                score += 3
        # Medium-confidence keywords (weight 1)
        for kw in domain_data["medium"]:
            if kw in content_lower:
                score += 1
        domain_data["weight"] = score
    
    # Find best domain
    best_domain = max(domains.items(), key=lambda x: x[1]["weight"])
    
    # If no match found or very weak match, use fallback
    if best_domain[1]["weight"] == 0:
        return "Domain 1: Security and Risk Management"  # Default fallback
    
    return best_domain[0]

def parse_question_parts(content):
    """Parse a question into structured parts: question text, options, answer, explanation"""
    result = {
        "question_text": "",
        "options": [],
        "answer": "",
        "explanation": "",
        "has_explanation": False
    }
    
    # Fix merged options first
    content = fix_merged_options(content)
    content = fix_spacing_issues(content)
    
    # Extract the question text (everything before the first option or Answer:)
    qa_match = re.match(r'^(.*?)(?=\n?[A-D]\.|\n?Answer:)', content, re.DOTALL)
    if qa_match:
        result["question_text"] = qa_match.group(1).strip()
    
    # Extract options
    option_pattern = r'([A-D])\.\s*(.*?)(?=\n?[A-D]\.|\n?Answer:|\Z)'
    for match in re.finditer(option_pattern, content, re.DOTALL):
        letter = match.group(1)
        text = match.group(2).strip()
        result["options"].append({"letter": letter, "text": text})
    
    # Extract answer
    answer_match = re.search(r'Answer:\s*([A-D])', content)
    if answer_match:
        result["answer"] = answer_match.group(1)
    
    # Extract explanation
    expl_match = re.search(r'Explanation:\s*(.*?)(?=\n(?:Source|Reference|The following reference|QUESTION \d+|ISC CISSP|$))', content, re.DOTALL)
    if expl_match:
        expl = expl_match.group(1).strip()
        if len(expl) > 20:  # Meaningful explanation
            result["explanation"] = expl
            result["has_explanation"] = True
    
    return result

def main():
    print("=== CORRECTED CISSP QUESTION ORGANIZER ===\n")
    
    text = read_raw_text()
    if not text:
        return
    
    print("1. Parsing question blocks...")
    blocks = parse_question_blocks(text)
    print(f"   Found {len(blocks)} questions")
    
    print("2. Classifying questions by domain (content analysis)...")
    domain_questions = defaultdict(list)
    domain_stats = defaultdict(lambda: {"total": 0, "no_explanation": 0})
    
    for i, block in enumerate(blocks):
        if (i + 1) % 500 == 0:
            print(f"   Processed {i+1}/{len(blocks)}...")
        
        content = clean_question_content(block["content"])
        parsed = parse_question_parts(content)
        domain = classify_question_domain(content)
        
        q_data = {
            "question_number": block["question_number"],
            "original_topic": block["topic"],
            "domain": domain,
            "question_text": parsed["question_text"],
            "options": parsed["options"],
            "answer": parsed["answer"],
            "explanation": parsed["explanation"],
            "has_explanation": parsed["has_explanation"]
        }
        
        domain_questions[domain].append(q_data)
        domain_stats[domain]["total"] += 1
        if not parsed["has_explanation"]:
            domain_stats[domain]["no_explanation"] += 1
    
    print(f"   Completed classification of {len(blocks)} questions")
    
    print("\n3. Domain distribution after reclassification:")
    print(f"   {'Domain':<50} {'Questions':>10} {'Missing Expl':>13} {'Rate':>10}")
    print(f"   {'-'*50} {'-'*10} {'-'*13} {'-'*10}")
    
    total_q = 0
    total_missing = 0
    for domain_key in sorted(domain_questions.keys()):
        stats = domain_stats[domain_key]
        total_q += stats["total"]
        total_missing += stats["no_explanation"]
        rate = f"{stats['no_explanation']/stats['total']*100:.1f}%"
        print(f"   {domain_key:<50} {stats['total']:>10} {stats['no_explanation']:>13} {rate:>10}")
    
    print(f"   {'-'*50} {'-'*10} {'-'*13} {'-'*10}")
    print(f"   {'TOTAL':<50} {total_q:>10} {total_missing:>13} {f'{total_missing/total_q*100:.1f}%':>10}")
    
    # Save corrected data
    print("\n4. Saving corrected JSON data...")
    
    output = {
        "metadata": {
            "total_questions": total_q,
            "total_domains": len(domain_questions),
            "questions_missing_explanations": total_missing,
            "domain_weights": {
                "Domain 1: Security and Risk Management": "15%",
                "Domain 2: Asset Security": "10%",
                "Domain 3: Security Architecture and Engineering": "13%",
                "Domain 4: Communication and Network Security": "13%",
                "Domain 5: Identity and Access Management (IAM)": "13%",
                "Domain 6: Security Assessment and Testing": "12%",
                "Domain 7: Security Operations": "13%",
                "Domain 8: Software Development Security": "11%"
            }
        },
        "domains": {}
    }
    
    for domain, questions in sorted(domain_questions.items()):
        domain_num_match = re.search(r'Domain (\d+)', domain)
        domain_key = f"domain_{domain_num_match.group(1)}" if domain_num_match else domain
        
        output["domains"][domain_key] = {
            "name": domain,
            "question_count": len(questions),
            "missing_explanations": domain_stats[domain]["no_explanation"],
            "questions": questions
        }
    
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\corrected_questions.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"   Saved to: {json_path}")
    
    # Also create a human-readable report
    report_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\Accuracy_Evaluation_Report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("CISSP QUESTION ORGANIZATION - ACCURACY EVALUATION REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write("ISSUES FOUND IN PREVIOUS WORK:\n")
        f.write("-" * 40 + "\n")
        f.write("1. CRITICAL: Domain mapping was based on arbitrary 'Topic' numbers from the\n")
        f.write("   original PDF. These do NOT correspond to CISSP 8-domain structure.\n")
        f.write("   FIX: Each question is now individually classified using comprehensive\n")
        f.write("   keyword analysis across all 8 domains.\n\n")
        f.write("2. MINOR: Some questions lack explanations in the source document.\n")
        f.write(f"   {total_missing} out of {total_q} questions ({total_missing/total_q*100:.1f}%) have no explanation.\n")
        f.write("   FIX: These are now clearly marked in the JSON output.\n\n")
        f.write("3. MINOR: Answer options were merged in raw text extraction.\n")
        f.write("   e.g., 'B. Social EngineeringC. Object reuseD. Wiretaping'\n")
        f.write("   FIX: Enhanced parsing splits merged options using regex.\n\n")
        f.write("4. MINOR: Spacing artifacts from PDF extraction.\n")
        f.write("   e.g., 'th at' instead of 'that'\n")
        f.write("   FIX: Comprehensive cleanup function handles known patterns.\n\n")
        f.write("\nUPDATED DOMAIN DISTRIBUTION:\n")
        f.write("-" * 40 + "\n")
        for domain_key in sorted(domain_questions.keys()):
            stats = domain_stats[domain_key]
            f.write(f"{domain_key}: {stats['total']} questions ({stats['no_explanation']} missing explanations)\n")
        f.write(f"\nTOTAL: {total_q} questions\n")
    
    print(f"   Report saved to: {report_path}")
    
    return output

if __name__ == "__main__":
    main()