"""
CISSP Question Sub-Section Organizer
====================================
Classifies all 2,615 questions into their specific sub-sections within each domain
per the official ISC2 CISSP Exam Outline (Effective April 15, 2024).

Domain -> Sub-section mapping based on official ISC2 exam outline.
"""

import re
import json
from collections import defaultdict

# ============================================================
# OFFICIAL ISC2 CISSP EXAM OUTLINE (2024)
# ============================================================
CISSP_OUTLINE = {
    "1": {
        "name": "Security and Risk Management",
        "weight": "15%",
        "sections": {
            "1.1": "Understand, adhere to, and promote professional ethics",
            "1.2": "Understand and apply security concepts",
            "1.3": "Evaluate and apply security governance principles",
            "1.4": "Understand legal, regulatory, and compliance issues",
            "1.5": "Understand requirements for investigation types",
            "1.6": "Develop, document, and implement security policy, standards, procedures, and guidelines",
            "1.7": "Identify, analyze, and prioritize Business Continuity (BC) requirements",
            "1.8": "Contribute to and enforce personnel security policies and procedures",
            "1.9": "Understand and apply risk management concepts",
            "1.10": "Understand and apply threat modeling concepts and methodologies",
            "1.11": "Apply Supply Chain Risk Management (SCRM) concepts",
            "1.12": "Establish and maintain a security awareness, education, and training program"
        }
    },
    "2": {
        "name": "Asset Security",
        "weight": "10%",
        "sections": {
            "2.1": "Identify and classify information and assets",
            "2.2": "Establish information and asset handling requirements",
            "2.3": "Provision resources securely",
            "2.4": "Manage data lifecycle",
            "2.5": "Ensure appropriate asset retention",
            "2.6": "Determine data security controls and compliance requirements"
        }
    },
    "3": {
        "name": "Security Architecture and Engineering",
        "weight": "13%",
        "sections": {
            "3.1": "Research, implement and manage engineering processes using secure design principles",
            "3.2": "Understand the fundamental concepts of security models",
            "3.3": "Select controls based upon systems security requirements",
            "3.4": "Understand security capabilities of Information Systems (IS)",
            "3.5": "Assess and mitigate the vulnerabilities of security architectures, designs, and solution elements",
            "3.6": "Select and determine cryptographic solutions",
            "3.7": "Understand methods of cryptanalytic attacks",
            "3.8": "Apply security principles to site and facility design",
            "3.9": "Design site and facility security controls"
        }
    },
    "4": {
        "name": "Communication and Network Security",
        "weight": "13%",
        "sections": {
            "4.1": "Assess and implement secure design principles in network architectures",
            "4.2": "Secure network components",
            "4.3": "Implement secure communication channels according to design"
        }
    },
    "5": {
        "name": "Identity and Access Management (IAM)",
        "weight": "13%",
        "sections": {
            "5.1": "Control physical and logical access to assets",
            "5.2": "Manage identification and authentication of people, devices, and services",
            "5.3": "Federated identity with a third-party service",
            "5.4": "Implement and manage authorization mechanisms",
            "5.5": "Manage the identity and access provisioning lifecycle",
            "5.6": "Implement authentication systems"
        }
    },
    "6": {
        "name": "Security Assessment and Testing",
        "weight": "12%",
        "sections": {
            "6.1": "Design and validate assessment, test, and audit strategies",
            "6.2": "Conduct security control testing",
            "6.3": "Collect security process data",
            "6.4": "Analyze test output and generate report",
            "6.5": "Conduct or facilitate security audits"
        }
    },
    "7": {
        "name": "Security Operations",
        "weight": "13%",
        "sections": {
            "7.1": "Understand and comply with investigations",
            "7.2": "Conduct logging and monitoring activities",
            "7.3": "Perform Configuration Management (CM)",
            "7.4": "Apply foundational security operations concepts",
            "7.5": "Apply resource protection",
            "7.6": "Conduct incident management",
            "7.7": "Operate and maintain detective and preventative measures",
            "7.8": "Implement and support patch and vulnerability management",
            "7.9": "Understand and participate in change management processes",
            "7.10": "Implement recovery strategies",
            "7.11": "Implement Disaster Recovery (DR) processes",
            "7.12": "Test Disaster Recovery Plans (DRP)",
            "7.13": "Participate in Business Continuity (BC) planning and exercises",
            "7.14": "Implement and manage physical security",
            "7.15": "Address personnel safety and security concerns"
        }
    },
    "8": {
        "name": "Software Development Security",
        "weight": "11%",
        "sections": {
            "8.1": "Understand and integrate security in the Software Development Life Cycle (SDLC)",
            "8.2": "Identify and apply security controls in software development ecosystems",
            "8.3": "Assess the effectiveness of software security",
            "8.4": "Assess security impact of acquired software",
            "8.5": "Define and apply secure coding guidelines and standards"
        }
    }
}

# ============================================================
# SUB-SECTION KEYWORDS
# Each sub-section has STRONG (weight 5) and MEDIUM (weight 2) keywords
# Question text keywords weighted 2x vs explanation keywords
# ============================================================

SECTION_KEYWORDS = {
    "1.1": {  # Professional Ethics
        "strong": ["code of ethics", "isc2 ethics", "professional ethics", "ethical violation",
                   "canon", "ethics canon", "ethical principle", "ethical responsibility",
                   "report ethics violation", "ethical conduct"],
        "medium": ["ethics", "ethical", "moral", "professional conduct", "isc2 code"]
    },
    "1.2": {  # Security Concepts
        "strong": ["cia triad", "confidentiality integrity availability", "security concept",
                   "security fundamental", "security principle", "information security concept",
                   "cia", "aaa", "non-repudiation", "accountability", "authenticity"],
        "medium": ["confidentiality", "integrity", "availability", "security objective",
                   "security goal", "fundamental security"]
    },
    "1.3": {  # Governance
        "strong": ["security governance", "governance principle", "governance framework",
                   "board of director", "executive management", "steering committee",
                   "governance structure", "strategic alignment", "enterprise governance"],
        "medium": ["governance", "board", "executive", "management responsibility",
                   "strategic", "organizational governance"]
    },
    "1.4": {  # Legal, Regulatory, Compliance
        "strong": ["legal requirement", "regulatory requirement", "compliance requirement",
                   "due diligence", "due care", "negligence", "liability",
                   "intellectual property", "copyright", "trademark", "patent", "trade secret",
                   "privacy law", "gdpr", "hipaa", "sox", "glba", "ferpa", "pci dss",
                   "computer crime", "computer fraud", "cybercrime law", "cfaa",
                   "evidence admissibility", "e-discovery", "legal hold",
                   "licensing", "software license", "data protection regulation",
                   "regulatory compliance", "legal compliance", "legal liability"],
        "medium": ["legal", "regulation", "compliance", "law", "regulatory",
                   "license", "privacy regulation", "intellectual property",
                   "copyright", "patent", "trademark"]
    },
    "1.5": {  # Investigation Types
        "strong": ["investigation type", "criminal investigation", "civil investigation",
                   "administrative investigation", "regulatory investigation",
                   "investigation requirement", "evidence standard",
                   "burden of proof", "preponderance of evidence", "beyond reasonable doubt"],
        "medium": ["investigation", "evidence", "forensic investigation"]
    },
    "1.6": {  # Policy, Standards, Procedures
        "strong": ["security policy", "security standard", "security procedure", "security guideline",
                   "security baseline", "policy development", "policy implementation",
                   "acceptable use policy", "information security policy",
                   "policy document", "standard document", "procedure document",
                   "policy review", "policy framework", "policy hierarchy"],
        "medium": ["policy", "standard", "procedure", "guideline", "baseline",
                   "security documentation"]
    },
    "1.7": {  # Business Continuity Requirements
        "strong": ["business continuity requirement", "bc requirement", "bcp requirement",
                   "continuity requirement", "business impact analysis", "bia",
                   "maximum tolerable downtime", "mtd", "recovery time objective", "rto",
                   "recovery point objective", "rpo", "business continuity planning",
                   "continuity of operation", "business continuity management"],
        "medium": ["business continuity", "bcp", "continuity planning", "bia",
                   "business impact", "maximum tolerable", "downtime"]
    },
    "1.8": {  # Personnel Security
        "strong": ["personnel security", "employee screening", "background check",
                   "background investigation", "reference check", "employment agreement",
                   "non-disclosure agreement", "nda", "non-compete agreement",
                   "job rotation", "mandatory vacation", "separation of duties",
                   "employee termination", "termination procedure", "exit interview",
                   "personnel policy", "personnel procedure"],
        "medium": ["personnel", "employee", "hiring", "termination", "screening",
                   "background", "job rotation", "separation of duties"]
    },
    "1.9": {  # Risk Management
        "strong": ["risk management", "risk assessment", "risk analysis", "risk mitigation",
                   "risk transfer", "risk avoidance", "risk acceptance", "risk reduction",
                   "qualitative risk", "quantitative risk", "risk framework",
                   "annualized loss expectancy", "ale", "single loss expectancy", "sle",
                   "annualized rate of occurrence", "aro", "exposure factor", "ef",
                   "risk appetite", "risk tolerance", "risk register",
                   "iso 31000", "nist risk management", "nist 800-37",
                   "residual risk", "total risk", "inherent risk",
                   "information risk", "risk treatment", "risk response"],
        "medium": ["risk", "ale", "sle", "aro", "risk analysis", "risk assessment",
                   "quantitative", "qualitative", "risk mitigation"]
    },
    "1.10": {  # Threat Modeling
        "strong": ["threat modeling", "threat model", "stride", "dread", "pasta",
                   "attack tree", "attack surface", "threat intelligence",
                   "threat actor", "threat vector", "threat source",
                   "adversary capability", "attack vector analysis"],
        "medium": ["threat model", "threat intelligence", "threat actor",
                   "stride", "dread", "attack tree"]
    },
    "1.11": {  # Supply Chain Risk Management
        "strong": ["supply chain risk", "supply chain security", "scrm",
                   "vendor risk", "third-party risk", "supplier risk",
                   "outsourcing risk", "vendor assessment", "supplier assessment",
                   "supply chain attack", "procurement risk"],
        "medium": ["supply chain", "vendor", "third-party", "supplier", "outsourcing",
                   "procurement security"]
    },
    "1.12": {  # Security Awareness, Education, Training
        "strong": ["security awareness", "security training", "security education",
                   "awareness program", "training program", "education program",
                   "security culture", "user awareness", "security communication",
                   "phishing awareness", "social engineering awareness"],
        "medium": ["awareness", "training", "education", "security culture",
                   "user education"]
    },
    
    # DOMAIN 2: ASSET SECURITY
    "2.1": {  # Identify and Classify Information and Assets
        "strong": ["asset identification", "asset inventory", "asset classification",
                   "information classification", "data classification",
                   "classification level", "classification label",
                   "classification scheme", "sensitivity level", "sensitivity label",
                   "government classification", "commercial classification",
                   "top secret", "secret", "confidential", "unclassified",
                   "proprietary", "private", "sensitive", "public",
                   "asset identification method", "inventory management"],
        "medium": ["classification", "classify", "labeling", "sensitivity",
                   "inventory", "asset management", "data categorization"]
    },
    "2.2": {  # Information and Asset Handling Requirements
        "strong": ["handling requirement", "data handling", "asset handling",
                   "handling procedure", "handling policy",
                   "data protection requirement", "protection requirement",
                   "information handling", "media handling",
                   "handling standard", "acceptable use", "data usage"],
        "medium": ["handling", "protection requirement", "data protection",
                   "acceptable use"]
    },
    "2.3": {  # Provision Resources Securely
        "strong": ["provision resources", "provisioning", "resource allocation",
                   "secure provisioning", "asset provisioning",
                   "resource management", "capacity planning", "resource security"],
        "medium": ["provision", "resource", "allocation", "capacity"]
    },
    "2.4": {  # Manage Data Lifecycle
        "strong": ["data lifecycle", "information lifecycle", "lifecycle management",
                   "data creation", "data storage", "data archival",
                   "data destruction", "data disposal", "data sanitization",
                   "data remanence", "purge data", "wipe data",
                   "degauss", "overwrite", "shredding", "crypto-shredding",
                   "secure deletion", "secure disposal",
                   "data retention", "record retention", "data lifecycle phase"],
        "medium": ["lifecycle", "destruction", "disposal", "sanitization",
                   "retention", "archival", "remanence", "degaussing",
                   "overwriting", "shredding"]
    },
    "2.5": {  # Ensure Appropriate Asset Retention
        "strong": ["asset retention", "retention policy", "retention schedule",
                   "retention requirement", "record retention",
                   "retention period", "legal hold", "retention mandate",
                   "data retention policy", "media retention"],
        "medium": ["retention", "retain", "archive", "legal hold"]
    },
    "2.6": {  # Data Security Controls and Compliance Requirements
        "strong": ["data security control", "compliance requirement", "data compliance",
                   "data protection standard", "data security standard",
                   "information security control", "data governance",
                   "compliance framework", "data protection compliance"],
        "medium": ["compliance", "data control", "security control",
                   "data governance"]
    },
    
    # DOMAIN 3: SECURITY ARCHITECTURE AND ENGINEERING
    "3.1": {  # Secure Design Principles
        "strong": ["secure design principle", "secure design", "design principle",
                   "defense in depth", "layered defense", "layered security",
                   "fail safe", "fail secure", "fail open",
                   "least privilege", "need to know", "separation of duties",
                   "economy of mechanism", "complete mediation",
                   "open design", "psychological acceptability",
                   "least common mechanism", "work factor",
                   "security by design", "privacy by design",
                   "secure engineering", "security engineering process",
                   "threat modeling design", "secure architecture design"],
        "medium": ["design principle", "defense in depth", "layered",
                   "fail safe", "fail secure", "secure design",
                   "security engineering", "architecture design"]
    },
    "3.2": {  # Security Models
        "strong": ["security model", "bell-lapadula", "biba model", "biba",
                   "clark-wilson", "brewer-nash", "chinese wall",
                   "state machine model", "information flow model",
                   "non-interference model", "take-grant model",
                   "access matrix model", "harrison-ruzzo-ullman",
                   "lattice model", "mandatory access control model",
                   "integrity model", "confidentiality model",
                   "goguen-meseguer", "sutherland model",
                   "security model comparison", "formal security model"],
        "medium": ["bell-lapadula", "biba", "clark-wilson", "brewer-nash",
                   "chinese wall", "security model", "lattice", "state machine"]
    },
    "3.3": {  # Select Controls Based on Security Requirements
        "strong": ["control selection", "select control", "control baseline",
                   "security requirement", "control requirement",
                   "nist 800-53", "iso 27002", "control catalog",
                   "control framework", "control assessment",
                   "technical control", "administrative control",
                   "preventive control", "detective control", "corrective control",
                   "deterrent control", "compensating control",
                   "control classification", "control type selection"],
        "medium": ["control selection", "security requirement", "control baseline",
                   "technical control", "administrative control",
                   "preventive", "detective", "corrective", "deterrent",
                   "compensating control"]
    },
    "3.4": {  # Security Capabilities of Information Systems
        "strong": ["security capability", "information system security",
                   "system security", "security evaluation",
                   "common criteria", "evaluation assurance level", "eal",
                   "orange book", "trusted computer system evaluation criteria", "tcsec",
                   "its", "information technology security evaluation criteria",
                   "target of evaluation", "toe", "protection profile",
                   "security target", "trusted computing base", "tcb",
                   "security kernel", "reference monitor",
                   "security perimeter", "security domain",
                   "certification and accreditation", "security certification",
                   "system accreditation"],
        "medium": ["common criteria", "orange book", "tcsec", "evaluation assurance",
                   "trusted computing base", "tcb", "security kernel",
                   "reference monitor", "protection profile", "its"]
    },
    "3.5": {  # Assess and Mitigate Vulnerabilities
        "strong": ["vulnerability assessment", "vulnerability mitigation",
                   "security vulnerability", "system vulnerability",
                   "architecture vulnerability", "design vulnerability",
                   "web vulnerability", "mobile vulnerability", "embedded vulnerability",
                   "virtualization vulnerability", "cloud vulnerability",
                   "iot vulnerability", "industrial control vulnerability",
                   "microservice vulnerability", "container vulnerability",
                   "serverless vulnerability", "edge computing vulnerability",
                   "buffer overflow", "race condition", "time-of-check time-of-use",
                   "toc/tou", "injection flaw", "memory leak",
                   "architectural weakness", "design flaw"],
        "medium": ["vulnerability", "mitigation", "vulnerability assessment",
                   "buffer overflow", "injection", "race condition"]
    },
    "3.6": {  # Cryptographic Solutions
        "strong": ["cryptographic solution", "cryptography", "encryption",
                   "symmetric encryption", "asymmetric encryption",
                   "aes", "des", "3des", "rsa", "ecc", "elliptic curve",
                   "diffie-hellman", "el gamal", "twofish", "blowfish",
                   "block cipher", "stream cipher", "cipher mode",
                   "ecb", "cbc", "cfb", "ofb", "ctr", "gcm",
                   "hash function", "sha", "md5", "hmac",
                   "digital signature", "digital certificate",
                   "public key infrastructure", "pki",
                   "certificate authority", "registration authority",
                   "key escrow", "key recovery", "key distribution",
                   "quantum cryptography", "post-quantum cryptography",
                   "cryptographic module", "fips 140",
                   "transport encryption", "data at rest encryption",
                   "end-to-end encryption", "link encryption"],
        "medium": ["encryption", "decryption", "cipher", "key", "cryptography",
                   "symmetric", "asymmetric", "hash", "digital signature",
                   "certificate", "pki", "key management", "aes", "rsa"]
    },
    "3.7": {  # Cryptanalytic Attacks
        "strong": ["cryptanalytic attack", "cryptanalysis", "attack on encryption",
                   "brute force attack", "known plaintext", "chosen plaintext",
                   "chosen ciphertext", "ciphertext-only", "adaptive chosen",
                   "side-channel attack", "timing attack", "power analysis",
                   "differential cryptanalysis", "linear cryptanalysis",
                   "frequency analysis", "meet-in-the-middle",
                   "birthday attack", "collision attack", "rainbow table",
                   "dictionary attack", "replay attack", "man-in-the-middle attack crypto",
                   "key clustering", "weak key"],
        "medium": ["cryptanalysis", "brute force", "known plaintext",
                   "chosen plaintext", "side channel", "frequency analysis",
                   "rainbow table", "dictionary attack", "collision"]
    },
    "3.8": {  # Apply Security Principles to Site and Facility Design
        "strong": ["site design", "facility design", "site security",
                   "facility planning", "site selection",
                   "crime prevention through environmental design", "cpted",
                   "site layout", "facility layout",
                   "secure facility design", "site configuration",
                   "building design security", "campu design"],
        "medium": ["site design", "facility design", "cpted", "site layout",
                   "building design", "facility planning"]
    },
    "3.9": {  # Design Site and Facility Security Controls
        "strong": ["facility security control", "site security control",
                   "physical access control", "fencing", "gate", "bollard",
                   "lighting", "security lighting", "perimeter security",
                   "mantrap", "turnstile", "access card", "proximity card",
                   "badge reader", "biometric door", "security guard",
                   "guard station", "surveillance camera", "cctv",
                   "alarm system", "motion detector", "glass break detector",
                   "door contact", "window sensor",
                   "fire detection", "smoke detector", "heat detector",
                   "flame detector", "fire suppression", "sprinkler system",
                   "gaseous suppression", "fm-200", "halon", "co2 suppression",
                   "hvac security", "power security", "ups", "generator",
                   "emi shielding", "tempest", "faraday cage", "white noise",
                   "raised floor", "hot aisle", "cold aisle",
                   "water detection", "humidity control", "temperature control"],
        "medium": ["physical security", "fencing", "gate", "lighting",
                   "mantrap", "turnstile", "badge", "guard", "surveillance",
                   "cctv", "alarm", "fire detection", "sprinkler",
                   "hvac", "ups", "generator", "tempest", "faraday cage",
                   "physical control", "facility control"]
    },
    
    # DOMAIN 4: COMMUNICATION AND NETWORK SECURITY
    "4.1": {  # Secure Design Principles in Network Architectures
        "strong": ["network architecture", "network design", "secure network design",
                   "network segmentation", "network zoning",
                   "dmz", "demilitarized zone", "screened subnet",
                   "defense in depth network", "layered network defense",
                   "network topology", "network isolation",
                   "microsegmentation", "zero trust network", "software-defined networking",
                   "sdn", "network virtualization", "virtual network",
                   "osi model", "tcp/ip model", "network layer",
                   "transport layer", "application layer", "data link layer",
                   "physical layer", "session layer", "presentation layer",
                   "network protocol design", "protocol analysis"],
        "medium": ["network architecture", "network design", "dmz",
                   "network segmentation", "osi model", "tcp/ip",
                   "network layer", "transport layer", "topology"]
    },
    "4.2": {  # Secure Network Components
        "strong": ["secure network component", "network device security",
                   "firewall", "packet filter", "stateful firewall", "application firewall",
                   "next-generation firewall", "proxy firewall", "web application firewall",
                   "intrusion detection system", "ids", "intrusion prevention system", "ips",
                   "router security", "switch security", "bridge security",
                   "load balancer", "proxy server", "reverse proxy",
                   "network access control", "nac", "endpoint security network",
                   "network device hardening", "router acl",
                   "vlan", "vlan security", "port security",
                   "span port", "network tap",
                   "content delivery network", "cdn", "wireless controller",
                   "unified threat management", "utm"],
        "medium": ["firewall", "ids", "ips", "router", "switch",
                   "proxy", "load balancer", "network device",
                   "vlan", "nac", "wireless security", "endpoint"]
    },
    "4.3": {  # Implement Secure Communication Channels
        "strong": ["secure communication", "secure channel", "encrypted communication",
                   "vpn", "virtual private network", "ipsec", "ssl vpn", "tls vpn",
                   "transport layer security", "tls", "secure socket layer", "ssl",
                   "ssh", "secure shell", "sftp", "scp",
                   "end-to-end encryption", "link encryption",
                   "wireless encryption", "wpa2", "wpa3", "wep",
                   "802.1x", "eap", "peap", "radius authentication",
                   "remote access security", "remote access vpn",
                   "site-to-site vpn", "client-based vpn",
                   "voice over ip security", "voip security",
                   "email security", "secure email", "s/mime", "pgp",
                   "dns security", "dnssec", "dns over https", "dns over tls"],
        "medium": ["vpn", "ipsec", "tls", "ssl", "wireless security",
                   "wpa", "wep", "802.1x", "remote access",
                   "secure communication", "encrypted channel",
                   "dnssec", "s/mime", "email security"]
    },
    
    # DOMAIN 5: IDENTITY AND ACCESS MANAGEMENT (IAM)
    "5.1": {  # Control Physical and Logical Access
        "strong": ["control access", "physical access control", "logical access control",
                   "access control mechanism", "access control system",
                   "access control requirement", "access control policy",
                   "secure access", "restrict access", "limit access",
                   "access management", "access governance",
                   "privileged access management", "pam",
                   "privileged account management"],
        "medium": ["access control", "physical access", "logical access",
                   "restrict access", "privileged access"]
    },
    "5.2": {  # Manage Identification and Authentication
        "strong": ["identification", "authentication", "identity verification",
                   "authentication factor", "authentication method",
                   "something you know", "something you have", "something you are",
                   "password authentication", "passphrase", "pin",
                   "token authentication", "smart card authentication",
                   "biometric authentication", "fingerprint", "retina", "iris",
                   "voice recognition", "facial recognition",
                   "keystroke dynamics", "signature dynamics",
                   "behavioral biometric", "physiological biometric",
                   "multi-factor authentication", "mfa", "two-factor authentication", "2fa",
                   "mutual authentication", "challenge-response",
                   "continuous authentication", "adaptive authentication",
                   "device authentication", "service authentication"],
        "medium": ["authentication", "identify", "password", "token",
                   "biometric", "fingerprint", "retina", "iris",
                   "multi-factor", "two-factor", "2fa", "mfa"]
    },
    "5.3": {  # Federated Identity
        "strong": ["federated identity", "federation", "identity federation",
                   "saml", "security assertion markup language",
                   "oauth", "openid connect", "oidc",
                   "identity provider", "idp", "service provider", "sp",
                   "federated sso", "federation protocol",
                   "cross-domain authentication", "cross-domain identity",
                   "claims-based authentication", "federation trust"],
        "medium": ["federation", "federated", "saml", "oauth", "openid",
                   "identity provider", "idp"]
    },
    "5.4": {  # Implement and Manage Authorization Mechanisms
        "strong": ["authorization", "access control model",
                   "discretionary access control", "dac",
                   "mandatory access control", "mac",
                   "role-based access control", "rbac",
                   "rule-based access control", "rbac",
                   "attribute-based access control", "abac",
                   "context-based access control",
                   "access control matrix", "access control list", "acl",
                   "capability table", "content-dependent access control",
                   "constrained user interface",
                   "permission management", "rights management",
                   "entitlement management", "privilege management"],
        "medium": ["authorization", "dac", "mac", "rbac", "abac",
                   "access matrix", "acl", "permission", "privilege",
                   "entitlement"]
    },
    "5.5": {  # Identity and Access Provisioning Lifecycle
        "strong": ["provisioning", "deprovisioning", "account provisioning",
                   "identity lifecycle", "access lifecycle",
                   "account creation", "account deletion", "account disable",
                   "account maintenance", "account review",
                   "access review", "access certification", "access recertification",
                   "user provisioning", "automated provisioning",
                   "provisioning workflow", "identity governance",
                   "role mining", "role engineering", "entitlement review"],
        "medium": ["provisioning", "deprovisioning", "lifecycle",
                   "account management", "access review", "identity management"]
    },
    "5.6": {  # Implement Authentication Systems
        "strong": ["authentication system", "authentication service",
                   "single sign-on", "sso",
                   "kerberos", "radius", "tacacs", "tacacs+", "diameter",
                   "ldap", "active directory",
                   "directory service", "centralized authentication",
                   "decentralized authentication", "hybrid authentication",
                   "biometric system", "biometric device",
                   "token-based system", "smart card system",
                   "type i error", "type ii error", "false acceptance rate",
                   "false rejection rate", "crossover error rate", "cer", "eer",
                   "biometric accuracy", "biometric enrollment",
                   "biometric throughput", "biometric template",
                   "callback system", "callback security"],
        "medium": ["single sign-on", "sso", "kerberos", "radius", "tacacs",
                   "ldap", "directory service", "biometric system",
                   "type i error", "type ii error", "false acceptance",
                   "false rejection", "crossover error rate"]
    },
    
    # DOMAIN 6: SECURITY ASSESSMENT AND TESTING
    "6.1": {  # Design and Validate Assessment, Test, and Audit Strategies
        "strong": ["assessment strategy", "test strategy", "audit strategy",
                   "security assessment plan", "test plan",
                   "assessment methodology", "testing methodology",
                   "vulnerability assessment strategy", "penetration test strategy",
                   "audit planning", "audit scope", "audit objective",
                   "testing schedule", "assessment frequency",
                   "continuous assessment", "continuous testing"],
        "medium": ["assessment strategy", "test strategy", "audit strategy",
                   "test plan", "audit plan", "assessment methodology"]
    },
    "6.2": {  # Conduct Security Control Testing
        "strong": ["security control testing", "control testing",
                   "vulnerability assessment", "vulnerability scanning",
                   "penetration testing", "penetration test",
                   "ethical hacking", "security testing methodology",
                   "black box testing", "white box testing", "gray box testing",
                   "external testing", "internal testing",
                   "network scanning", "port scanning",
                   "web application testing", "application security testing",
                   "social engineering test", "phishing simulation",
                   "physical penetration test", "war driving", "war dialing",
                   "wireless testing", "wireless assessment",
                   "configuration review", "configuration audit",
                   "compliance testing", "compliance scan",
                   "credentialed scan", "non-credentialed scan"],
        "medium": ["penetration test", "vulnerability scan", "vulnerability assessment",
                   "security testing", "control test", "pen test",
                   "ethical hacking", "black box", "white box", "gray box",
                   "social engineering test"]
    },
    "6.3": {  # Collect Security Process Data
        "strong": ["security process data", "process data collection",
                   "security metric collection", "metric data",
                   "key performance indicator", "kpi", "key risk indicator", "kri",
                   "security measurement", "security data collection",
                   "log collection", "event collection",
                   "security monitoring data", "collection method"],
        "medium": ["metric", "kpi", "kri", "data collection", "security metric",
                   "measurement", "monitoring data"]
    },
    "6.4": {  # Analyze Test Output and Generate Report
        "strong": ["test output analysis", "test report", "assessment report",
                   "audit report", "vulnerability report",
                   "penetration test report", "finding report",
                   "remediation recommendation", "risk rating",
                   "severity classification", "cvss",
                   "test result analysis", "false positive", "false negative",
                   "report generation", "management report",
                   "technical report", "executive summary",
                   "remediation tracking", "finding classification"],
        "medium": ["test report", "audit report", "finding", "remediation",
                   "false positive", "false negative", "report",
                   "severity", "risk rating", "cvss"]
    },
    "6.5": {  # Conduct or Facilitate Security Audits
        "strong": ["security audit", "internal audit", "external audit",
                   "compliance audit", "audit process",
                   "audit evidence", "audit finding",
                   "audit trail review", "audit log review",
                   "auditor independence", "audit standard",
                   "iso 19011", "audit methodology",
                   "audit interview", "audit sampling",
                   "audit recommendation", "audit follow-up"],
        "medium": ["audit", "auditor", "audit finding", "audit evidence",
                   "compliance audit", "internal audit"]
    },
    
    # DOMAIN 7: SECURITY OPERATIONS
    "7.1": {  # Investigations
        "strong": ["investigation", "digital investigation", "forensic investigation",
                   "evidence collection", "evidence preservation",
                   "chain of custody", "evidence handling",
                   "forensic analysis", "forensic tool",
                   "digital forensic", "computer forensic", "network forensic",
                   "evidence admissibility", "forensic procedure",
                   "investigation process", "incident investigation",
                   "root cause analysis", "crime scene",
                   "forensic image", "forensic copy", "write blocker",
                   "order of volatility", "forensic methodology"],
        "medium": ["investigation", "forensic", "evidence", "chain of custody",
                   "digital forensic", "forensic tool"]
    },
    "7.2": {  # Logging and Monitoring
        "strong": ["logging", "monitoring", "security log", "audit log",
                   "event log", "syslog", "log management",
                   "log analysis", "log review", "log retention",
                   "security information and event management", "siem",
                   "security event monitoring", "continuous monitoring",
                   "anomaly detection", "behavioral monitoring",
                   "alert management", "alert triage",
                   "log correlation", "security analytics",
                   "user behavior analytics", "uba", "ueba"],
        "medium": ["logging", "log", "monitoring", "siem", "audit trail",
                   "alert", "anomaly", "event log"]
    },
    "7.3": {  # Configuration Management
        "strong": ["configuration management", "cm", "configuration control",
                   "configuration baseline", "secure configuration",
                   "configuration item", "configuration change",
                   "configuration management database", "cmdb",
                   "baseline configuration", "configuration standard",
                   "configuration audit", "configuration review",
                   "change control board", "configuration drift",
                   "hardening standard", "secure baseline"],
        "medium": ["configuration management", "configuration control",
                   "baseline", "configuration item", "configuration change",
                   "hardening", "configuration standard"]
    },
    "7.4": {  # Foundational Security Operations Concepts
        "strong": ["security operations", "foundational operations",
                   "administrative management", "security administration",
                   "need-to-know", "least privilege operations",
                   "separation of duties operations", "job rotation operations",
                   "mandatory vacation", "dual control",
                   "split knowledge", "two-person control",
                   "operations security", "operational procedure",
                   "security operations concept"],
        "medium": ["security operations", "least privilege", "separation of duties",
                   "job rotation", "mandatory vacation", "dual control",
                   "two-person control", "split knowledge"]
    },
    "7.5": {  # Resource Protection
        "strong": ["resource protection", "protect resource",
                   "media management", "media protection", "media control",
                   "data backup", "backup strategy", "backup policy",
                   "backup frequency", "backup type", "full backup",
                   "incremental backup", "differential backup",
                   "tape rotation", "grandfather-father-son",
                   "offsite backup", "cloud backup",
                   "backup verification", "backup restoration test",
                   "asset protection", "equipment protection",
                   "redundancy", "fault tolerance", "high availability",
                   "raid", "disk mirroring", "clustering"],
        "medium": ["backup", "restore", "media protection", "resource protection",
                   "redundancy", "fault tolerance", "high availability",
                   "raid", "media management"]
    },
    "7.6": {  # Incident Management
        "strong": ["incident management", "incident response", "incident handling",
                   "security incident", "incident response plan",
                   "incident response team", "csirt", "cert",
                   "incident response procedure", "incident classification",
                   "incident prioritization", "incident escalation",
                   "incident containment", "incident eradication",
                   "incident recovery", "lessons learned",
                   "incident reporting", "incident communication",
                   "incident detection", "incident analysis"],
        "medium": ["incident", "incident response", "incident management",
                   "security incident", "csirt", "cert", "containment",
                   "eradication", "lessons learned"]
    },
    "7.7": {  # Detective and Preventative Measures
        "strong": ["detective measure", "preventative measure",
                   "intrusion detection", "intrusion prevention",
                   "anti-malware", "antivirus", "anti-spyware",
                   "endpoint detection", "edr", "endpoint protection",
                   "honeypot", "honeynet", "deception technology",
                   "file integrity monitoring", "integrity verification",
                   "security control operation", "control maintenance",
                   "whitelist", "blacklist", "allowlist", "blocklist",
                   "sandbox", "dlp", "data loss prevention"],
        "medium": ["detective", "preventative", "anti-malware", "antivirus",
                   "honeypot", "honeynet", "dlp", "data loss prevention",
                   "edr", "endpoint detection", "file integrity"]
    },
    "7.8": {  # Patch and Vulnerability Management
        "strong": ["patch management", "vulnerability management",
                   "security patch", "software update", "firmware update",
                   "patch deployment", "patch testing",
                   "patch schedule", "patch prioritization",
                   "vulnerability scanning operations", "vulnerability remediation",
                   "zero-day vulnerability", "patch management process",
                   "patch tuesday", "emergency patch"],
        "medium": ["patch", "update", "vulnerability management",
                   "patch management", "firmware update"]
    },
    "7.9": {  # Change Management
        "strong": ["change management", "change control", "change request",
                   "change approval", "change advisory board", "cab",
                   "change management process", "change schedule",
                   "emergency change", "change window",
                   "change documentation", "change review",
                   "release management", "deployment management"],
        "medium": ["change management", "change control", "change request",
                   "change approval", "release management"]
    },
    "7.10": {  # Recovery Strategies
        "strong": ["recovery strategy", "recovery site", "recovery option",
                   "hot site", "warm site", "cold site", "mobile site",
                   "mirrored site", "reciprocal agreement",
                   "alternate processing site", "recovery location",
                   "recovery time", "recovery procedure",
                   "system recovery", "service recovery",
                   "recovery strategy selection", "recovery cost"],
        "medium": ["recovery strategy", "hot site", "warm site", "cold site",
                   "reciprocal agreement", "alternate site", "recovery site"]
    },
    "7.11": {  # Disaster Recovery Processes
        "strong": ["disaster recovery process", "disaster recovery plan", "drp",
                   "disaster declaration", "disaster recovery procedure",
                   "recovery team", "recovery phase",
                   "disaster recovery activation", "disaster notification",
                   "recovery operations", "salvage team",
                   "drp implementation", "disaster recovery execution"],
        "medium": ["disaster recovery", "drp", "disaster", "recovery plan",
                   "recovery procedure", "disaster declaration"]
    },
    "7.12": {  # Test Disaster Recovery Plans
        "strong": ["drp test", "disaster recovery test", "recovery plan test",
                   "tabletop exercise", "walkthrough test", "simulation test",
                   "parallel test", "full interruption test",
                   "drp testing", "drp exercise", "test plan",
                   "recovery testing", "test result", "drp validation"],
        "medium": ["drp test", "recovery test", "tabletop", "walkthrough",
                   "simulation test", "parallel test", "full interruption"]
    },
    "7.13": {  # Business Continuity Planning and Exercises
        "strong": ["business continuity planning", "bcp", "bc exercise",
                   "continuity exercise", "business continuity test",
                   "bcp exercise", "business continuity plan",
                   "continuity of operations plan", "coop",
                   "business resumption plan", "occupant emergency plan",
                   "crisis management plan", "crisis communication",
                   "pandemic planning", "continuity capability"],
        "medium": ["business continuity", "bcp", "continuity plan",
                   "crisis management", "continuity exercise"]
    },
    "7.14": {  # Implement and Manage Physical Security
        "strong": ["physical security", "physical protection",
                   "perimeter security", "fencing", "gate", "bollard",
                   "lighting", "security lighting", "cctv", "surveillance",
                   "access card", "biometric access", "security guard",
                   "mantrap", "turnstile",
                   "fire detection", "fire suppression",
                   "smoke detector", "heat detector", "sprinkler",
                   "fire extinguisher", "halon", "fm-200",
                   "hvac", "ups", "generator", "power distribution",
                   "emi shielding", "tempest", "faraday cage"],
        "medium": ["physical security", "perimeter", "guard", "cctv",
                   "fire detection", "fire suppression", "sprinkler",
                   "access card", "biometric door"]
    },
    "7.15": {  # Personnel Safety and Security
        "strong": ["personnel safety", "employee safety", "workplace safety",
                   "safety concern", "safety procedure", "safety training",
                   "emergency evacuation", "evacuation plan",
                   "emergency response", "life safety",
                   "safety regulation", "osha", "occupational safety",
                   "employee security concern", "workplace violence",
                   "travel security", "executive protection",
                   "health and safety", "safety and security"],
        "medium": ["safety", "employee safety", "evacuation", "emergency",
                   "life safety", "personnel safety"]
    },
    
    # DOMAIN 8: SOFTWARE DEVELOPMENT SECURITY
    "8.1": {  # Security in SDLC
        "strong": ["software development life cycle", "sdlc", "system development lifecycle",
                   "secure sdlc", "security in sdlc",
                   "waterfall model", "agile", "scrum", "devops", "devsecops",
                   "spiral model", "prototyping", "incremental development",
                   "v-model", "rapid application development",
                   "sdlc phase", "requirements phase", "design phase",
                   "development phase", "testing phase", "deployment phase",
                   "maintenance phase", "security requirements",
                   "security design", "security development",
                   "security testing", "security deployment",
                   "integrate security", "shift left", "security throughout lifecycle"],
        "medium": ["sdlc", "software development", "development lifecycle",
                   "waterfall", "agile", "scrum", "devops", "devsecops",
                   "development phase", "lifecycle phase"]
    },
    "8.2": {  # Security Controls in Development Ecosystems
        "strong": ["development ecosystem", "development environment",
                   "development security", "secure development environment",
                   "development tool security", "ide security",
                   "continuous integration", "continuous deployment", "ci/cd",
                   "code repository security", "version control",
                   "source code management", "build security",
                   "software configuration management",
                   "development workstation security",
                   "test environment security", "staging environment",
                   "orchestration security", "container security development",
                   "repository security", "artifact repository"],
        "medium": ["development environment", "ci/cd", "continuous integration",
                   "version control", "code repository", "build security",
                   "container security", "orchestration"]
    },
    "8.3": {  # Assess Effectiveness of Software Security
        "strong": ["software security assessment", "security effectiveness",
                   "code review", "code analysis", "static analysis", "dynamic analysis",
                   "static application security testing", "sast",
                   "dynamic application security testing", "dast",
                   "interactive application security testing", "iast",
                   "software composition analysis", "sca",
                   "code audit", "security code review",
                   "application vulnerability assessment",
                   "software security testing", "application security testing",
                   "fuzzing", "fuzz testing", "mutation testing",
                   "security regression testing"],
        "medium": ["code review", "static analysis", "dynamic analysis",
                   "sast", "dast", "iast", "software testing",
                   "fuzzing", "code audit"]
    },
    "8.4": {  # Assess Security Impact of Acquired Software
        "strong": ["acquired software", "third-party software", "commercial off-the-shelf",
                   "cots", "open source software", "outsourced development",
                   "software acquisition", "software procurement",
                   "vendor software assessment", "software supply chain",
                   "acquired software security", "third-party component",
                   "software dependency", "library security",
                   "module security", "plugin security", "api security acquired",
                   "service-oriented architecture security", "soa security",
                   "microservice acquisition", "cloud service security acquisition"],
        "medium": ["acquired software", "third-party software", "cots",
                   "open source", "software acquisition", "vendor software",
                   "outsourced development"]
    },
    "8.5": {  # Secure Coding Guidelines and Standards
        "strong": ["secure coding", "coding guideline", "coding standard",
                   "secure coding practice", "secure coding standard",
                   "input validation", "output encoding", "parameterized query",
                   "prepared statement", "escape output",
                   "error handling secure", "exception handling secure",
                   "session management secure", "authentication coding",
                   "authorization coding", "cryptographic coding",
                   "memory management secure", "resource management coding",
                   "owasp coding", "secure coding principle",
                   "least privilege coding", "defense in depth coding",
                   "sanitization coding", "validation coding",
                   "sql injection prevention", "xss prevention",
                   "csrf prevention", "cross-site request forgery",
                   "buffer overflow prevention", "integer overflow",
                   "race condition prevention", "insecure deserialization"],
        "medium": ["secure coding", "input validation", "output encoding",
                   "parameterized query", "sql injection", "xss",
                   "csrf", "buffer overflow", "owasp",
                   "coding standard", "coding guideline", "code security"]
    }
}

def read_raw_text():
    with open(r"C:\Users\Khumza\Documents\Coding projects\CISSP\raw_text.txt", "r", encoding="utf-8") as f:
        return f.read()

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
    content = re.sub(r'ISC CISSP\s*\nhttps://certempire\.com/\s*\d+', '', content)
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
    content = re.sub(r'([A-D])\.\s*(.*?)([A-D])\.', r'\1. \2\n\3.', content)
    return content

def parse_question_parts(content):
    content = fix_merged_options(content)
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

def classify_subsection(question_text, explanation_text):
    """Classify into sub-section using weighted keyword matching"""
    qt_lower = question_text.lower()
    expl_lower = (explanation_text or "").lower()
    
    scores = {}
    for section_id, kw_groups in SECTION_KEYWORDS.items():
        score = 0
        # Question text keywords (2x weight)
        for kw in kw_groups["strong"]:
            if kw in qt_lower:
                score += 10  # 5 * 2
        for kw in kw_groups["medium"]:
            if kw in qt_lower:
                score += 4   # 2 * 2
        # Explanation keywords (1x weight)
        for kw in kw_groups["strong"]:
            if kw in expl_lower:
                score += 5
        for kw in kw_groups["medium"]:
            if kw in expl_lower:
                score += 2
        scores[section_id] = score
    
    best = max(scores.items(), key=lambda x: x[1])
    
    if best[1] == 0:
        return None  # No match
    return best[0]

def main():
    print("=== CISSP SUB-SECTION ORGANIZER ===\n")
    print("Official ISC2 CISSP Exam Outline (April 15, 2024)")
    print("=" * 60)
    
    text = read_raw_text()
    if not text:
        return
    
    print("\n1. Parsing questions...")
    blocks = parse_question_blocks(text)
    print(f"   Found {len(blocks)} questions")
    
    print("2. Classifying by sub-section...")
    section_data = defaultdict(list)
    unmatched = 0
    stats = defaultdict(lambda: {"total": 0, "no_explanation": 0, "unmatched": 0})
    
    for i, block in enumerate(blocks):
        if (i + 1) % 500 == 0:
            print(f"   Processing {i+1}/{len(blocks)}...")
        
        content = clean_content(block["content"])
        parsed = parse_question_parts(content)
        
        section = classify_subsection(parsed["question_text"], parsed["explanation"])
        
        if section is None:
            unmatched += 1
            section = "unclassified"
        
        # Determine domain from section
        if section != "unclassified":
            domain_num = section.split(".")[0]
        else:
            domain_num = "?"
        
        q_data = {
            "question_number": block["question_number"],
            "original_topic": block["topic"],
            "section": section,
            "section_name": CISSP_OUTLINE.get(domain_num, {}).get("sections", {}).get(section, "Unclassified"),
            "domain": f"Domain {domain_num}: {CISSP_OUTLINE.get(domain_num, {}).get('name', 'Unknown')}",
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
        if section == "unclassified":
            stats[section]["unmatched"] += 1
    
    print(f"   Done. {len(blocks)} questions classified.")
    print(f"   Unmatched (no keywords): {unmatched} ({unmatched/len(blocks)*100:.1f}%)")
    
    # Print detailed breakdown
    print("\n3. Sub-section Distribution:")
    print(f"   {'Section':<8} {'Description':<55} {'Q Count':>8} {'Missing':>8}")
    print(f"   {'-'*8} {'-'*55} {'-'*8} {'-'*8}")
    
    total_q = 0
    total_missing = 0
    for section_id in sorted(section_data.keys(), key=natural_sort_key):
        s = stats[section_id]
        total_q += s["total"]
        total_missing += s["no_explanation"]
        if section_id == "unclassified":
            desc = "Unclassified (no keyword match)"
        else:
            domain_num = section_id.split(".")[0]
            desc = CISSP_OUTLINE.get(domain_num, {}).get("sections", {}).get(section_id, "Unknown")
            if len(desc) > 55:
                desc = desc[:52] + "..."
        print(f"   {section_id:<8} {desc:<55} {s['total']:>8} {s['no_explanation']:>8}")
    
    print(f"   {'-'*8} {'-'*55} {'-'*8} {'-'*8}")
    print(f"   {'TOTAL':<8} {'':<55} {total_q:>8} {total_missing:>8}")
    
    # Show a few samples
    print("\n4. Sample questions:")
    for section_id in sorted(section_data.keys(), key=natural_sort_key)[:10]:
        qs = section_data[section_id]
        if qs:
            sample = qs[0]
            qtext = sample["question_text"][:120].replace('\n', ' ')
            print(f"   {section_id}: Q{sample['question_number']}: {qtext}...")
    
    # Save data
    print("\n5. Saving sub-section organized data...")
    
    output = {
        "metadata": {
            "total_questions": total_q,
            "total_sections": len(section_data),
            "missing_explanations": total_missing,
            "unmatched_questions": unmatched,
            "cissp_exam_outline_effective_date": "April 15, 2024",
            "classification_note": "Questions classified into CISSP sub-sections using weighted keyword analysis per official ISC2 exam outline."
        },
        "outline": CISSP_OUTLINE,
        "sections": {}
    }
    
    for section_id in sorted(section_data.keys(), key=natural_sort_key):
        qs = section_data[section_id]
        output["sections"][section_id] = {
            "question_count": len(qs),
            "missing_explanations": stats[section_id]["no_explanation"],
            "questions": qs
        }
    
    json_path = r"C:\Users\Khumza\Documents\Coding projects\CISSP\subsection_organized_questions.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"   Saved to: {json_path}")
    return output

def natural_sort_key(s):
    """Sort section IDs like 1.1, 1.2, ..., 1.12, 2.1, ..., unclassified"""
    if s == "unclassified":
        return (999, 0)
    parts = s.split(".")
    return (int(parts[0]), int(parts[1]))

if __name__ == "__main__":
    main()