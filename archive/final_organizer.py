"""
FINAL CORRECTED CISSP Question Organizer

Fixes applied:
1. Explanation regex: Fixed to use non-capturing lookahead that actually works with the content
2. Content cleaning: Less aggressive - preserve data between headers
3. Classification: Use full question content (question + explanation) for better keyword matching
4. Domain mapping: Properly weighted keyword classification with fallback
"""

import re
import json
from collections import defaultdict

def read_raw_text():
    with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "r", encoding="utf-8") as f:
        return f.read()

def parse_question_blocks(text):
    """Parse text into question blocks"""
    blocks = []
    pattern = r'QUESTION\s+(\d+)\s*-\s*\(Topic\s+(\d+)\)'
    parts = re.split(pattern, text)
    
    for i in range(1, len(parts), 3):
        if i + 2 < len(parts):
            content = parts[i + 2]
            # Stop at next QUESTION marker
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
    """Light cleaning - remove page headers but keep structure"""
    # Remove page markers
    content = re.sub(r'ISC CISSP\s*\n.*?CERT EMPIRE\s*\d+', '', content, flags=re.DOTALL)
    content = re.sub(r'ISC CISSP\s*\nhttps://certempire\.com/\s*\d+', '', content)
    content = re.sub(r'ISC CISSP\s*\n"https://certempire\.com/"\s*\d+', '', content)
    content = re.sub(r'"Best Material, Great Results"\.\s*CERT EMPIRE\s*\d+', '', content)
    
    # Normalize whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()

def fix_spacing(text):
    """Fix extracted PDF spacing artifacts"""
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
        r'\bh a d\b': 'had', r'\ba l s o\b': 'also', r'\bw h e r e\b': 'where',
        r'\bw h a t\b': 'what', r'\bw h e n\b': 'when', r'\bw h o\b': 'who',
        r'\bt h e i r\b': 'their', r'\bt h e y\b': 'they', r'\bt h e r e\b': 'there',
        r'\bs o m e\b': 'some', r'\bm a y\b': 'may', r'\bm u s t\b': 'must',
        r'\bm i g h t\b': 'might', r'\bs u c h\b': 'such', r'\be a c h\b': 'each',
        r'\ba n y\b': 'any', r'\bm o s t\b': 'most', r'\bo n l y\b': 'only',
        r'\bb u t\b': 'but', r'\ba f t e r\b': 'after', r'\bb e f o r e\b': 'before',
        r'\bb e t w e e n\b': 'between', r'\bo v e r\b': 'over', r'\bu n d e r\b': 'under',
        r'\ba g a i n s t\b': 'against', r'\ba b o u t\b': 'about',
        r'\bi n t o\b': 'into', r'\bt h r o u g h\b': 'through',
        r'\bd u r i n g\b': 'during', r'\bw i t h o u t\b': 'without',
        r'\bh o w e v e r\b': 'however', r'\bt h e r e f o r e\b': 'therefore',
        r'\bb e c a u s e\b': 'because', r'\bw h i l e\b': 'while',
        r'\ba m o n g\b': 'among', r'\bw i t h i n\b': 'within',
        r'\ba w a y\b': 'away', r'\bb a c k\b': 'back', r'\bd o w n\b': 'down',
        r'\bo u t\b': 'out', r'\bo f f\b': 'off', r'\bo n c e\b': 'once',
        r'\bf i r s t\b': 'first', r'\bl a s t\b': 'last', r'\bn e x t\b': 'next',
        r'\bm a d e\b': 'made', r'\bm a k e\b': 'make', r'\bt a k e\b': 'take',
        r'\bg i v e\b': 'give', r'\bc o m e\b': 'come', r'\bk n o w\b': 'know',
        r'\bs e e\b': 'see', r'\bu s e\b': 'use', r'\bg e t\b': 'get',
        r'\bv e r y\b': 'very', r'\bm u c h\b': 'much', r'\bw e l l\b': 'well',
        r'\be v e n\b': 'even', r'\bo t h e r\b': 'other', r'\bo w n\b': 'own',
        r'\bs a m e\b': 'same', r'\bl i k e\b': 'like', r'\bs u r e\b': 'sure',
        r'\bl o n g\b': 'long', r'\bh i g h\b': 'high', r'\bl o w\b': 'low',
        r'\bl a r g e\b': 'large', r'\bs m a l l\b': 'small', r'\bf u l l\b': 'full',
        r'\bh a r d\b': 'hard', r'\be a s y\b': 'easy', r'\bf a s t\b': 'fast',
        r'\bs l o w\b': 'slow', r'\bf r e e\b': 'free', r'\bo p e n\b': 'open',
        r'\bc l o s e\b': 'close', r'\br e a d\b': 'read', r'\bw r i t e\b': 'write',
        r'\bc a l l\b': 'call', r'\bw o r k\b': 'work', r'\bh e l p\b': 'help',
        r'\bn e e d\b': 'need', r'\bw a n t\b': 'want', r'\bl o o k\b': 'look',
    }
    for pat, repl in fixes.items():
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    return text

def fix_merged_options(content):
    """Split merged options like 'B. OptionC. Option2'"""
    # Insert newlines between options
    content = re.sub(r'([A-D])\.\s*(.*?)([A-D])\.', r'\1. \2\n\3.', content)
    return content

def parse_question_parts(content):
    """Parse question into structured parts"""
    content = fix_merged_options(content)
    content = fix_spacing(content)
    
    result = {
        "question_text": "",
        "options": [],
        "answer": "",
        "explanation": "",
        "has_explanation": False
    }
    
    # Find where options start (first A. B. C. D. pattern)
    options_start = re.search(r'\n?[A-D]\.', content)
    
    if options_start:
        qtext = content[:options_start.start()].strip()
        rest = content[options_start.start():]
    else:
        qtext = content[:200].strip()
        rest = ""
    
    result["question_text"] = qtext
    
    # Extract options from rest
    option_pattern = r'([A-D])\.\s*(.+?)(?=\n?[A-D]\.|\n?Answer:|\Z)'
    for match in re.finditer(option_pattern, rest, re.DOTALL):
        result["options"].append({
            "letter": match.group(1),
            "text": match.group(2).strip()
        })
    
    # Extract answer
    answer_match = re.search(r'Answer:\s*([A-D])', content)
    if answer_match:
        result["answer"] = answer_match.group(1)
    
    # Extract explanation - check if "Explanation:" exists at all
    expl_idx = content.find("Explanation:")
    if expl_idx >= 0:
        expl_text = content[expl_idx + len("Explanation:"):].strip()
        
        # Cut off at next structural boundary
        cut_markers = ["Source:", "Reference(s)", "The following reference", 
                       "QUESTION ", "\nISC CISSP"]
        cut_pos = len(expl_text)
        for marker in cut_markers:
            pos = expl_text.find(marker)
            if pos >= 0 and pos < cut_pos:
                cut_pos = pos
        
        expl_text = expl_text[:cut_pos].strip()
        
        # Remove leading "Explanation :" duplicates
        expl_text = re.sub(r'^Explanation\s*:\s*', '', expl_text).strip()
        
        if len(expl_text) > 20:
            result["explanation"] = expl_text
            result["has_explanation"] = True
    
    return result

def classify_domain(question_text, explanation_text):
    """
    Classify question into CISSP domain using weighted keyword matching.
    Question text gets 2x weight vs explanation text.
    """
    # Question text weighted 2x, explanation 1x
    qt_lower = question_text.lower()
    expl_lower = explanation_text.lower() if explanation_text else ""
    
    # Domain keywords with weights
    # Higher weight = stronger indicator
    domains = {
        "Domain 1: Security and Risk Management": {
            "strong": [
                "risk assessment", "risk analysis", "risk mitigation", "residual risk",
                "security governance", "security policy", "corporate security policy",
                "due diligence", "due care", "personnel security",
                "business continuity plan", "disaster recovery plan",
                "annualized loss expectancy", "single loss expectancy",
                "annualized rate of occurrence", "exposure factor",
                "data owner", "data custodian", "acceptable use policy",
                "security framework", "iso 27001", "cobit",
                "cia triad", "confidentiality, integrity, availability"
            ],
            "medium": [
                "risk management", "governance", "compliance", "legal",
                "regulation", "ethics", "security standard",
                "security procedure", "security guideline", "security baseline",
                "policy", "confidentiality", "integrity", "availability"
            ]
        },
        "Domain 2: Asset Security": {
            "strong": [
                "data classification", "information classification",
                "asset inventory", "data retention", "media sanitization",
                "data destruction", "data remanence", "data lifecycle",
                "data labeling", "personally identifiable information",
                "protected health information"
            ],
            "medium": [
                "asset", "classification", "data ownership",
                "privacy", "retention", "labeling", "sanitization",
                "disposal", "sensitive data"
            ]
        },
        "Domain 3: Security Architecture and Engineering": {
            "strong": [
                "cryptography", "encryption algorithm", "decryption",
                "key management", "public key infrastructure",
                "digital signature", "certificate authority",
                "security model", "bell-lapadula", "biba model",
                "clark-wilson", "brewer-nash", "common criteria",
                "evaluation assurance level", "orange book",
                "trusted computing base", "security kernel",
                "physical security", "facility design",
                "faraday cage", "tempest", "white noise",
                "fire suppression", "sprinkler system",
                "mantrap", "turnstile",
                "defense in depth", "layered security",
                "biometric system", "biometric device"
            ],
            "medium": [
                "encryption", "cipher", "cryptosystem", "key",
                "architecture", "engineering", "secure design",
                "security control", "facility", "biometric",
                "crossover error rate", "false acceptance",
                "false rejection", "type i error", "type ii error"
            ]
        },
        "Domain 4: Communication and Network Security": {
            "strong": [
                "network security", "network protocol",
                "firewall", "packet filter", "stateful inspection",
                "intrusion detection system", "intrusion prevention system",
                "virtual private network", "vpn", "ipsec",
                "wireless security", "wep", "wpa", "wpa2",
                "denial of service", "dos attack", "ddos",
                "man-in-the-middle", "arp spoofing",
                "osi model", "tcp/ip", "network layer",
                "transport layer", "session layer",
                "circuit-switched", "packet-switched",
                "x.25", "frame relay", "ethernet",
                "mac address", "subnet", "vlan",
                "dns security", "dnssec",
                "proxy server", "network address translation"
            ],
            "medium": [
                "network", "protocol", "router", "switch",
                "bridge", "gateway", "packet", "transmission",
                "wireless", "bandwidth", "tcp", "udp",
                "port", "socket", "host-based ids", "nids", "hids"
            ]
        },
        "Domain 5: Identity and Access Management (IAM)": {
            "strong": [
                "access control", "authentication", "authorization",
                "identification", "identity management",
                "single sign-on", "federated identity",
                "saml", "kerberos", "ldap", "radius", "tacacs",
                "discretionary access control", "mandatory access control",
                "role-based access control", "rbac",
                "attribute-based access control",
                "access control matrix", "access control list",
                "multi-factor authentication", "two-factor",
                "biometric authentication",
                "separation of duties", "least privilege",
                "need to know", "need-to-know"
            ],
            "medium": [
                "access", "authenticate", "authorize",
                "password", "passphrase", "token", "smart card",
                "biometric", "fingerprint", "retina scan",
                "iris", "hand geometry", "signature dynamic",
                "permission", "privilege", "role",
                "account", "login", "logon", "credential"
            ]
        },
        "Domain 6: Security Assessment and Testing": {
            "strong": [
                "security assessment", "security testing",
                "security audit", "vulnerability assessment",
                "penetration testing", "pen test",
                "security control testing", "control assessment",
                "audit trail", "audit log",
                "security metric", "security monitoring",
                "continuous monitoring",
                "static analysis", "dynamic analysis"
            ],
            "medium": [
                "assessment", "testing", "audit",
                "vulnerability", "penetration",
                "logging", "monitoring", "metric",
                "scan", "review"
            ]
        },
        "Domain 7: Security Operations": {
            "strong": [
                "incident response", "incident management",
                "digital forensic", "chain of custody",
                "disaster recovery", "disaster recovery plan",
                "business continuity", "business impact analysis",
                "recovery time objective", "recovery point objective",
                "maximum tolerable downtime",
                "backup strategy", "backup policy",
                "patch management", "change management",
                "problem management", "security operations center",
                "fire extinguisher", "smoke detector",
                "hvac", "uninterruptible power supply",
                "hot site", "warm site", "cold site"
            ],
            "medium": [
                "incident", "forensic", "disaster",
                "recovery", "backup", "restore",
                "patch", "change", "configuration",
                "operation", "maintenance",
                "redundancy", "failover",
                "evidence", "investigation"
            ]
        },
        "Domain 8: Software Development Security": {
            "strong": [
                "software development", "application security",
                "sdlc", "system development life cycle",
                "secure coding", "devsecops",
                "owasp", "sql injection", "cross-site scripting",
                "buffer overflow", "input validation",
                "database security", "relational database",
                "database view", "database schema",
                "primary key", "foreign key", "normalization",
                "capability maturity model",
                "configuration control", "change control",
                "object-oriented programming"
            ],
            "medium": [
                "software", "development", "application",
                "code", "programming", "database",
                "sql", "query", "schema", "table",
                "testing", "debugging",
                "agile", "waterfall", "devops"
            ]
        }
    }
    
    scores = {}
    for domain_name, kw_groups in domains.items():
        score = 0
        # Score from question text (2x weight)
        for kw in kw_groups["strong"]:
            if kw in qt_lower:
                score += 6  # 3 * 2
        for kw in kw_groups["medium"]:
            if kw in qt_lower:
                score += 2  # 1 * 2
        # Score from explanation text (1x weight)
        for kw in kw_groups["strong"]:
            if kw in expl_lower:
                score += 3
        for kw in kw_groups["medium"]:
            if kw in expl_lower:
                score += 1
        scores[domain_name] = score
    
    best = max(scores.items(), key=lambda x: x[1])
    
    if best[1] == 0:
        # No keywords matched - use original topic as hint
        return "Domain 1: Security and Risk Management"
    
    return best[0]

def main():
    print("=== FINAL CORRECTED CISSP ORGANIZER ===\n")
    
    text = read_raw_text()
    if not text:
        return
    
    print("1. Parsing questions...")
    blocks = parse_question_blocks(text)
    print(f"   Found {len(blocks)} questions")
    
    print("2. Classifying by domain and extracting content...")
    domain_questions = defaultdict(list)
    stats = defaultdict(lambda: {"total": 0, "no_explanation": 0})
    
    for i, block in enumerate(blocks):
        if (i + 1) % 500 == 0:
            print(f"   Processing {i+1}/{len(blocks)}...")
        
        content = clean_content(block["content"])
        
        # Parse parts first
        parsed = parse_question_parts(content)
        
        # Use BOTH question text AND explanation for classification
        # Question text gets 2x weight
        domain = classify_domain(parsed["question_text"], parsed["explanation"])
        
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
        stats[domain]["total"] += 1
        if not parsed["has_explanation"]:
            stats[domain]["no_explanation"] += 1
    
    print(f"   Done. {len(blocks)} questions classified.")
    
    # Print domain distribution
    print("\n3. Domain Distribution:")
    print(f"   {'Domain':<50} {'Questions':>10} {'Missing Expl':>13}")
    print(f"   {'-'*50} {'-'*10} {'-'*13}")
    
    total_q = 0
    total_missing = 0
    for dk in sorted(domain_questions.keys()):
        s = stats[dk]
        total_q += s["total"]
        total_missing += s["no_explanation"]
        print(f"   {dk:<50} {s['total']:>10} {s['no_explanation']:>13}")
    
    print(f"   {'-'*50} {'-'*10} {'-'*13}")
    print(f"   {'TOTAL':<50} {total_q:>10} {total_missing:>13}")
    print(f"   Missing rate: {total_missing/total_q*100:.1f}%")
    
    # Show sample classification from each domain
    print("\n4. Sample questions from each domain:")
    for dk in sorted(domain_questions.keys()):
        qs = domain_questions[dk]
        sample = qs[0]
        qtext = sample["question_text"][:100].replace('\n', ' ')
        print(f"   {dk}:")
        print(f"     Q{sample['question_number']} (Topic {sample['original_topic']}): {qtext}...")
        print(f"     Has explanation: {sample['has_explanation']}, Options: {len(sample['options'])}")
    
    # Save results
    print("\n5. Saving corrected data...")
    
    output = {
        "metadata": {
            "total_questions": total_q,
            "total_domains": len(domain_questions),
            "missing_explanations": total_missing,
            "classification_note": "Questions classified individually using weighted keyword analysis across all 8 CISSP domains. Original 'Topic' numbers were NOT used for classification."
        },
        "domains": {}
    }
    
    for domain, questions in sorted(domain_questions.items()):
        domain_num_match = re.search(r'Domain (\d+)', domain)
        domain_key = f"domain_{domain_num_match.group(1)}" if domain_num_match else domain
        
        output["domains"][domain_key] = {
            "name": domain,
            "question_count": len(questions),
            "missing_explanations": stats[domain]["no_explanation"],
            "questions": questions
        }
    
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\corrected_questions.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"   Saved to: {json_path}")
    return output

if __name__ == "__main__":
    main()