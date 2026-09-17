"""
FINAL FIXED CISSP Sub-Section Classifier
=========================================
Strategy: Two-pass classification
1. First pass: Classify all questions with improved keywords
2. Second pass: Re-evaluate questions in inflated sections (1.9, 3.6, 5.3) 
   with stricter criteria to move misclassified ones to better sections
"""

import re
import json
from collections import defaultdict

with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

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
        r'\bv e r y\b': 'very', r'\bm u c h\b': 'much',
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
# KEYWORDS - Balanced specificity
# ============================================================

SECTION_KEYWORDS = {
    "1.1": {
        "strong": ["code of ethics", "(isc)2 code of ethics", "professional ethics canon",
                   "ethical violation report"],
        "medium": ["ethics", "ethical principle"]
    },
    "1.2": {
        "strong": ["cia triad", "confidentiality integrity availability", "non-repudiation security",
                   "accountability security principle"],
        "medium": ["security concept", "fundamental security"]
    },
    "1.3": {
        "strong": ["security governance framework", "steering committee security",
                   "board of directors security oversight"],
        "medium": ["governance", "enterprise governance"]
    },
    "1.4": {
        "strong": ["due diligence legal", "due care negligence", "intellectual property right",
                   "copyright law", "trademark law", "patent protection", "trade secret",
                   "privacy regulation", "gdpr compliance", "hipaa regulation",
                   "computer crime law", "evidence admissibility court", "e-discovery legal",
                   "legal hold", "civil liability", "criminal liability"],
        "medium": ["legal requirement", "regulatory compliance", "law"]
    },
    "1.5": {
        "strong": ["criminal investigation procedure", "civil investigation procedure",
                   "administrative investigation", "burden of proof standard"],
        "medium": ["investigation type"]
    },
    "1.6": {
        "strong": ["security policy document", "acceptable use policy", "information security policy",
                   "security standard baseline", "security procedure guideline"],
        "medium": ["policy", "standard", "procedure"]
    },
    "1.7": {
        "strong": ["business impact analysis bia", "maximum tolerable downtime mtd",
                   "recovery time objective rto", "recovery point objective rpo",
                   "business continuity requirement"],
        "medium": ["business continuity", "bcp"]
    },
    "1.8": {
        "strong": ["background check employee", "background investigation personnel",
                   "non-disclosure agreement nda", "job rotation mandatory vacation",
                   "separation of duties personnel", "employee termination exit interview"],
        "medium": ["personnel security", "employee screening"]
    },
    "1.9": {
        "strong": ["annualized loss expectancy ale", "single loss expectancy sle",
                   "annualized rate of occurrence aro", "exposure factor ef",
                   "quantitative risk analysis", "qualitative risk analysis",
                   "risk mitigation transfer avoid accept", "iso 31000 risk",
                   "nist risk management framework rmf"],
        "medium": ["risk assessment", "risk analysis"]
    },
    "1.10": {
        "strong": ["threat modeling stride", "threat modeling dread", "attack tree analysis",
                   "attack surface analysis threat"],
        "medium": ["threat model"]
    },
    "1.11": {
        "strong": ["supply chain risk scrm", "vendor risk assessment third-party",
                   "supplier risk outsourcing"],
        "medium": ["supply chain"]
    },
    "1.12": {
        "strong": ["security awareness program training", "phishing awareness campaign",
                   "social engineering awareness training"],
        "medium": ["awareness", "training program"]
    },
    
    # DOMAIN 2
    "2.1": {
        "strong": ["data classification level label", "asset classification scheme",
                   "sensitivity label classification", "top secret secret confidential"],
        "medium": ["classification", "labeling"]
    },
    "2.2": {
        "strong": ["data handling requirement procedure", "media handling policy"],
        "medium": ["handling requirement"]
    },
    "2.3": {
        "strong": ["resource provisioning secure", "capacity planning security"],
        "medium": ["provisioning"]
    },
    "2.4": {
        "strong": ["data lifecycle management", "data sanitization degauss purge",
                   "data remanence destruction", "crypto-shredding deletion",
                   "secure media disposal"],
        "medium": ["lifecycle", "sanitization", "disposal"]
    },
    "2.5": {
        "strong": ["retention policy schedule", "record retention legal", "legal hold retention"],
        "medium": ["retention"]
    },
    "2.6": {
        "strong": ["data security control compliance", "data governance framework"],
        "medium": ["data compliance"]
    },
    
    # DOMAIN 3
    "3.1": {
        "strong": ["defense in depth layered", "fail safe fail secure design",
                   "least privilege design principle", "economy of mechanism complete mediation",
                   "open design psychological acceptability"],
        "medium": ["secure design principle"]
    },
    "3.2": {
        "strong": ["bell-lapadula confidentiality model", "biba integrity model",
                   "clark-wilson integrity model", "brewer-nash chinese wall",
                   "state machine security model", "lattice-based access model"],
        "medium": ["security model"]
    },
    "3.3": {
        "strong": ["control baseline nist 800-53", "technical administrative control selection",
                   "preventive detective corrective deterrent compensating control"],
        "medium": ["control selection"]
    },
    "3.4": {
        "strong": ["common criteria evaluation assurance level eal",
                   "orange book tcsec trusted computing base tcb",
                   "reference monitor security kernel", "protection profile toe"],
        "medium": ["common criteria", "tcsec"]
    },
    "3.5": {
        "strong": ["buffer overflow vulnerability", "race condition toc/tou",
                   "injection flaw architecture", "web application vulnerability design"],
        "medium": ["vulnerability architecture"]
    },
    "3.6": {
        "strong": ["aes des 3des symmetric encryption", "rsa ecc elliptic curve asymmetric",
                   "diffie-hellman key exchange", "sha hash function hmac",
                   "digital signature pki certificate authority",
                   "block cipher cbc ctr gcm mode",
                   "fips 140 cryptographic module"],
        "medium": ["encryption", "cryptography", "cipher"]
    },
    "3.7": {
        "strong": ["brute force cryptanalysis", "known plaintext chosen plaintext attack",
                   "side-channel timing power analysis", "differential linear cryptanalysis",
                   "birthday collision rainbow table"],
        "medium": ["cryptanalytic attack"]
    },
    "3.8": {
        "strong": ["site facility design cpted", "crime prevention environmental design"],
        "medium": ["site design"]
    },
    "3.9": {
        "strong": ["physical access mantrap turnstile badge", "cctv surveillance camera",
                   "fire detection smoke sprinkler suppression", "fm-200 halon gaseous",
                   "hvac ups generator emi tempest faraday cage"],
        "medium": ["physical security", "facility control"]
    },
    
    # DOMAIN 4
    "4.1": {
        "strong": ["network architecture segmentation vlan", "dmz demilitarized zone screened subnet",
                   "osi tcp/ip model layer", "zero trust network sdn"],
        "medium": ["network architecture"]
    },
    "4.2": {
        "strong": ["firewall packet filter stateful", "ids intrusion detection system",
                   "ips intrusion prevention system", "waf web application firewall",
                   "router switch security hardening", "nac network access control"],
        "medium": ["firewall", "ids", "ips"]
    },
    "4.3": {
        "strong": ["ipsec vpn tunnel", "ssl tls vpn", "ssh sftp secure shell",
                   "wpa2 wpa3 wireless encryption", "802.1x radius network auth",
                   "dnssec dns security", "s/mime pgp email encryption"],
        "medium": ["vpn", "secure channel"]
    },
    
    # DOMAIN 5
    "5.1": {
        "strong": ["physical logical access control asset", "privileged access management pam"],
        "medium": ["access control"]
    },
    "5.2": {
        "strong": ["multi-factor authentication mfa 2fa", "something you know have are",
                   "biometric fingerprint retina iris", "smart card token password pin"],
        "medium": ["authentication", "biometric"]
    },
    "5.3": {
        "strong": ["federated identity saml assertion", "oauth openid connect oidc",
                   "identity provider idp service provider sp federation"],
        "medium": ["federation", "saml", "oauth"]
    },
    "5.4": {
        "strong": ["discretionary access control dac", "mandatory access control mac",
                   "role-based access control rbac", "attribute-based access control abac",
                   "access control matrix acl capability"],
        "medium": ["dac", "mac", "rbac", "abac"]
    },
    "5.5": {
        "strong": ["account provisioning deprovisioning", "access review certification recertification",
                   "entitlement review role mining"],
        "medium": ["provisioning", "access review"]
    },
    "5.6": {
        "strong": ["kerberos authentication ticket", "radius tacacs+ authentication server",
                   "ldap active directory authentication", "single sign-on sso implementation",
                   "type i ii error biometric far frr cer eer"],
        "medium": ["kerberos", "radius", "tacacs", "sso"]
    },
    
    # DOMAIN 6
    "6.1": {
        "strong": ["assessment test audit strategy design"],
        "medium": ["assessment strategy"]
    },
    "6.2": {
        "strong": ["vulnerability scanning assessment", "penetration testing ethical hacking",
                   "black white gray box penetration", "social engineering phishing test"],
        "medium": ["penetration test", "vulnerability scan"]
    },
    "6.3": {
        "strong": ["security metric kpi kri collection"],
        "medium": ["metric", "kpi"]
    },
    "6.4": {
        "strong": ["test output analysis report cvss", "false positive negative analysis",
                   "remediation recommendation report"],
        "medium": ["test report"]
    },
    "6.5": {
        "strong": ["security audit process iso 19011", "compliance audit evidence"],
        "medium": ["audit"]
    },
    
    # DOMAIN 7
    "7.1": {
        "strong": ["digital forensic investigation", "chain of custody evidence preservation",
                   "order of volatility forensic imaging"],
        "medium": ["forensic", "investigation"]
    },
    "7.2": {
        "strong": ["siem security information event management", "syslog log analysis monitoring",
                   "user behavior analytics uba anomaly"],
        "medium": ["logging", "monitoring", "siem"]
    },
    "7.3": {
        "strong": ["configuration management cmdb baseline", "configuration drift hardening"],
        "medium": ["configuration management"]
    },
    "7.4": {
        "strong": ["need-to-know least privilege operation", "separation of duties dual control",
                   "split knowledge mandatory vacation"],
        "medium": ["operational security"]
    },
    "7.5": {
        "strong": ["backup full incremental differential tape rotation",
                   "raid fault tolerance high availability"],
        "medium": ["backup", "restore"]
    },
    "7.6": {
        "strong": ["incident response csirt cert", "containment eradication recovery incident",
                   "lessons learned incident"],
        "medium": ["incident response"]
    },
    "7.7": {
        "strong": ["anti-malware antivirus edr endpoint detection",
                   "honeypot honeynet deception", "file integrity monitoring fim",
                   "data loss prevention dlp sandbox"],
        "medium": ["detective", "preventative"]
    },
    "7.8": {
        "strong": ["patch management vulnerability remediation", "zero-day emergency patch"],
        "medium": ["patch management"]
    },
    "7.9": {
        "strong": ["change management cab advisory board", "release management deployment"],
        "medium": ["change management"]
    },
    "7.10": {
        "strong": ["hot site warm site cold site mirrored", "reciprocal agreement recovery"],
        "medium": ["recovery strategy"]
    },
    "7.11": {
        "strong": ["disaster recovery plan drp activation", "disaster declaration salvage team"],
        "medium": ["disaster recovery"]
    },
    "7.12": {
        "strong": ["drp test tabletop parallel full interruption simulation"],
        "medium": ["drp test"]
    },
    "7.13": {
        "strong": ["business continuity plan bcp coop", "crisis management pandemic"],
        "medium": ["business continuity"]
    },
    "7.14": {
        "strong": ["physical security perimeter fencing gate", "cctv guard patrol",
                   "fire extinguisher sprinkler physical"],
        "medium": ["physical security"]
    },
    "7.15": {
        "strong": ["personnel safety evacuation workplace violence", "osha occupational safety"],
        "medium": ["safety"]
    },
    
    # DOMAIN 8
    "8.1": {
        "strong": ["software development life cycle sdlc", "waterfall agile scrum devops devsecops",
                   "spiral rad v-model sdlc"],
        "medium": ["sdlc"]
    },
    "8.2": {
        "strong": ["ci/cd pipeline security", "version control repository security",
                   "build process container orchestration security"],
        "medium": ["development environment"]
    },
    "8.3": {
        "strong": ["static application security testing sast", "dynamic application security testing dast",
                   "interactive iast sca composition analysis", "code review security fuzz testing"],
        "medium": ["code review", "sast", "dast"]
    },
    "8.4": {
        "strong": ["commercial off-the-shelf cots security", "open source software acquisition security",
                   "third-party component supply chain"],
        "medium": ["acquired software"]
    },
    "8.5": {
        "strong": ["secure coding input validation output encoding",
                   "parameterized query prepared statement sql injection prevention",
                   "xss cross-site scripting prevention code", "buffer overflow prevention coding",
                   "owasp secure coding guideline"],
        "medium": ["secure coding", "input validation"]
    }
}

def classify_subsection(question_text, explanation_text):
    """Classify using weighted keyword matching with question text priority"""
    qt_lower = question_text.lower()
    expl_lower = (explanation_text or "").lower()
    
    scores = {}
    for section_id, kw_groups in SECTION_KEYWORDS.items():
        score = 0
        # Question text (2x weight)
        for kw in kw_groups["strong"]:
            count = qt_lower.count(kw)
            if count > 0:
                score += 10 * count
        for kw in kw_groups["medium"]:
            count = qt_lower.count(kw)
            if count > 0:
                score += 4 * count
        # Explanation (1x weight)
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
    if best[1] < 6:
        return None
    
    return best[0]

def reclassify_inflated_sections(questions_by_section):
    """Second pass: re-evaluate questions in potentially inflated sections"""
    # Sections known to be problematic from first run
    inflated_sections = ["1.9", "3.6", "5.3"]
    
    reclassified = 0
    moved_questions = []
    
    for sec_id in inflated_sections:
        if sec_id not in questions_by_section:
            continue
        
        questions = questions_by_section[sec_id]
        keep = []
        move = []
        
        for q in questions:
            # Get the second-best classification
            qt_lower = q["question_text"].lower()
            expl_lower = (q.get("explanation") or "").lower()
            
            alt_scores = {}
            for section_id, kw_groups in SECTION_KEYWORDS.items():
                if section_id == sec_id:
                    continue  # Skip current section
                
                score = 0
                for kw in kw_groups["strong"]:
                    count = qt_lower.count(kw) + expl_lower.count(kw)
                    if count > 0:
                        score += 5 * count
                for kw in kw_groups["medium"]:
                    count = qt_lower.count(kw) + expl_lower.count(kw)
                    if count > 0:
                        score += 2 * count
                
                if score > 0:
                    alt_scores[section_id] = score
            
            if alt_scores:
                best_alt = max(alt_scores.items(), key=lambda x: x[1])
                # If alternative score is close to or better than current, move it
                current_score = sum(
                    10 * qt_lower.count(kw) + 5 * expl_lower.count(kw)
                    for kw in SECTION_KEYWORDS[sec_id]["strong"]
                ) + sum(
                    4 * qt_lower.count(kw) + 2 * expl_lower.count(kw)
                    for kw in SECTION_KEYWORDS[sec_id]["medium"]
                )
                
                if best_alt[1] >= current_score * 0.7:  # Within 70% of current score
                    move.append((q, best_alt[0]))
                    reclassified += 1
                else:
                    keep.append(q)
            else:
                keep.append(q)
        
        questions_by_section[sec_id] = keep
        for q, new_sec in move:
            if new_sec not in questions_by_section:
                questions_by_section[new_sec] = []
            questions_by_section[new_sec].append(q)
            moved_questions.append((q["question_number"], sec_id, new_sec))
    
    print(f"Reclassified {reclassified} questions from inflated sections")
    if moved_questions:
        print("Sample moves:")
        for qnum, old, new in moved_questions[:10]:
            print(f"  Q{qnum}: {old} -> {new}")
    
    return questions_by_section

def main():
    print("=== FINAL SUB-SECTION CLASSIFIER (Two-Pass) ===\n")
    
    blocks = parse_question_blocks(raw_text)
    print(f"Parsed {len(blocks)} questions\n")
    
    # FIRST PASS
    section_data = defaultdict(list)
    unmatched = 0
    
    for i, block in enumerate(blocks):
        if (i + 1) % 500 == 0:
            print(f"First pass: {i+1}/{len(blocks)}...")
        
        content = clean_content(block["content"])
        parsed = parse_question_parts(content)
        
        section = classify_subsection(parsed["question_text"], parsed["explanation"])
        
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
    
    print(f"\nFirst pass complete. Unmatched: {unmatched} ({unmatched/len(blocks)*100:.1f}%)\n")
    
    # Print initial distribution for inflated sections
    for sec in ["1.9", "3.6", "5.3"]:
        print(f"Before reclassification - {sec}: {len(section_data.get(sec, []))} questions")
    
    # SECOND PASS: Reclassify inflated sections
    section_data = reclassify_inflated_sections(section_data)
    
    print("\nAfter reclassification:")
    for sec in ["1.9", "3.6", "5.3"]:
        print(f"  {sec}: {len(section_data.get(sec, []))} questions")
    
    # Final stats
    total_q = sum(len(qs) for qs in section_data.values())
    total_missing = sum(
        1 for qs in section_data.values() 
        for q in qs if not q.get("has_explanation")
    )
    
    def sort_key(s):
        if s == "unclassified":
            return (999, 0)
        parts = s.split(".")
        return (int(parts[0]), int(parts[1]))
    
    print(f"\n{'Section':<10} {'Count':>6}")
    print("-" * 18)
    for sec_id in sorted(section_data.keys(), key=sort_key):
        print(f"{sec_id:<10} {len(section_data[sec_id]):>6}")
    print(f"{'TOTAL':<10} {total_q:>6}")
    
    # Save
    output = {
        "metadata": {
            "total_questions": total_q,
            "missing_explanations": total_missing,
            "classification_note": "Two-pass classification with re-evaluation of inflated sections"
        },
        "sections": {}
    }
    
    for sec_id in sorted(section_data.keys(), key=sort_key):
        qs = section_data[sec_id]
        output["sections"][sec_id] = {
            "question_count": len(qs),
            "questions": qs
        }
    
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\subsection_organized_final.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved to: {json_path}")

if __name__ == "__main__":
    main()
