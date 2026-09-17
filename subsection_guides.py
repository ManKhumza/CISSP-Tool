"""
Curated study-guide content for every CISSP sub-section.
Written for this question bank: 'focus' explains the sub-section in exam terms and
'mustKnow' lists the facts the questions in this bank actually test.
Auto-extracted 'key terms' are added at build time from the assigned questions.
"""

GUIDES = {
    # ---------------- DOMAIN 1 ----------------
    "1.1": {
        "focus": "The (ISC)2 Code of Ethics and professional conduct. Expect questions on the four mandatory canons, the order in which they apply, and what happens when a CISSP violates the code.",
        "mustKnow": [
            "Four canons, in priority order: protect society and the common good; act honourably and justly; provide diligent service to principals; advance and protect the profession.",
            "The Code of Ethics takes precedence over an employer's instructions when they conflict.",
            "Complaints are handled by a peer review panel; sanctions include revocation of certification.",
            "Ethics violations include knowingly associating with criminal activity and failing to report violations.",
        ],
    },
    "1.2": {
        "focus": "Core security concepts: the CIA triad, AAA (authentication, authorization, accountability), non-repudiation and the basic control objectives that every other domain builds on.",
        "mustKnow": [
            "Confidentiality = preventing unauthorised disclosure; Integrity = preventing unauthorised or accidental modification; Availability = timely, reliable access.",
            "Non-repudiation is provided by digital signatures, not by symmetric encryption alone.",
            "Authentication proves identity, authorization decides what that identity may do, accountability ties actions to an identity.",
            "Integrity protects against both malicious modification and accidental corruption; its opposites are alteration and loss of internal/external consistency.",
            "Controls are classified by function (preventive, detective, corrective, deterrent, recovery, directive) and by nature (technical, administrative, physical).",
        ],
    },
    "1.3": {
        "focus": "Security governance: who sets direction, who owns risk, and how the security function is organised inside the business. Questions usually ask who is ultimately responsible.",
        "mustKnow": [
            "The board and senior management oversee organisational risk; the CISO leads the security programme, and business owners accept risks within their authority.",
            "Governance = setting strategy, direction and objectives; management = executing them.",
            "Typical roles: CISO, security manager, data owner, data custodian, system owner, security administrator, user, auditor.",
            "Security must be aligned to business objectives and measured with metrics reported to management.",
            "The data owner decides classification and access rules; the custodian implements them; the auditor independently verifies.",
        ],
    },
    "1.4": {
        "focus": "Legal, regulatory and compliance obligations: due care vs due diligence, negligence, intellectual property, privacy law, computer crime law and the handling of evidence.",
        "mustKnow": [
            "Due diligence = investigating and identifying risk; due care = doing something reasonable about it. Failing either can establish negligence and liability.",
            "Intellectual property: copyright (expression), trademark (brand), patent (invention), trade secret (confidential formula/process, no registration, must be protected).",
            "Distinguish laws and regulations (such as GDPR and HIPAA) from industry standards (PCI DSS) and contractual obligations; applicability depends on jurisdiction, data and activity.",
            "Evidence must be admissible: best evidence rule, hearsay exceptions for business records, chain of custody.",
            "Transborder data flow restrictions and export controls limit where data and crypto may go.",
        ],
    },
    "1.5": {
        "focus": "Types of investigation (criminal, civil, administrative, regulatory) and the standard of proof each demands.",
        "mustKnow": [
            "Criminal investigation: beyond a reasonable doubt; the state prosecutes; prison can follow.",
            "Civil investigation: preponderance of the evidence; one party sues another; remedy is usually money.",
            "Administrative investigation: internal to the organisation, governed by employment policy, not the courts.",
            "Regulatory investigation: a government/industry body enforcing compliance rules.",
            "Evidence handling must be consistent with the type of investigation and the forum that will hear it.",
        ],
    },
    "1.6": {
        "focus": "Security documentation: the hierarchy of policy, standard, procedure, guideline and baseline, and how each is used.",
        "mustKnow": [
            "Policy = mandatory management intent (what and why); Standard = mandatory specific requirements; Procedure = step-by-step how; Guideline = recommended advice; Baseline = minimum configuration.",
            "Policies are high level and change infrequently; procedures are detailed and change often.",
            "An effective policy is written for its audience, is enforceable, and is supported by standards, procedures and guidelines.",
            "Security policy must be approved by senior management and communicated to all staff.",
            "Frameworks and standards commonly referenced: ISO/IEC 27001/27002, NIST SP 800-53, COBIT, ITIL, PCI DSS.",
        ],
    },
    "1.7": {
        "focus": "Business continuity requirements: the analysis and management decisions that precede recovery planning.",
        "mustKnow": [
            "Business Impact Analysis (BIA) identifies critical business functions and the impact of their loss over time.",
            "MTD (maximum tolerable downtime), RTO (recovery time objective) and RPO (recovery point objective) drive every later recovery decision.",
            "Continuity strategy selection compares cost of downtime with cost of the recovery capability.",
            "BCP is business-driven and owned by senior management; the BIA must be repeated whenever the business changes.",
        ],
    },
    "1.8": {
        "focus": "Personnel security across the employment lifecycle: screening before hire, controls during employment, and safe termination.",
        "mustKnow": [
            "Pre-employment: background checks, reference checks, education/credit verification, NDAs, acceptable-use agreements.",
            "During employment: least privilege, separation of duties, job rotation, mandatory vacation, awareness training, performance review.",
            "Termination: friendly vs unfriendly; immediate disabling of accounts and removal of physical access for unfriendly or high-risk leavers.",
            "Exit interview, return of company property and reminder of continuing confidentiality obligations.",
            "Insider threat is the hardest to detect — controls are behavioural and administrative as much as technical.",
        ],
    },
    "1.9": {
        "focus": "Risk management: identification, analysis (quantitative and qualitative), treatment (mitigate, transfer, avoid, accept) and continuous monitoring of residual risk.",
        "mustKnow": [
            "Single loss expectancy (SLE) = asset value × exposure factor; annual loss expectancy (ALE) = SLE × annual rate of occurrence (ARO). Compare annual control cost with expected loss reduction.",
            "Risk depends on likelihood and impact. Residual risk remains after controls; financial savings inform decisions alongside safety, legal duties and business objectives.",
            "Risk treatment options: mitigation (reduce), transference (insure/outsource), avoidance (stop the activity), acceptance (documented decision by the owner).",
            "Quantitative analysis uses monetary values and ALE/ARO/EF; qualitative analysis uses scenarios, rankings and expert judgement.",
            "Risk appetite/tolerance is set by management; risk is always owned by the business, never by the security team alone.",
            "Risk assessment should be repeated at planned intervals and after significant change.",
        ],
    },
    "1.10": {
        "focus": "Threat modelling: structured ways to enumerate threats, attack paths and mitigations before code or architecture is built.",
        "mustKnow": [
            "STRIDE: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.",
            "DREAD scores risk: Damage, Reproducibility, Exploitability, Affected users, Discoverability.",
            "PASTA is an attacker-centric, seven-stage threat-modelling method.",
            "Attack trees decompose a goal into sub-goals; attack surface is everything reachable by an attacker.",
            "Threat intelligence feeds describe real adversaries (actors, TTPs) and should inform control selection.",
        ],
    },
    "1.11": {
        "focus": "Supply chain risk management (SCRM): the risk introduced by vendors, suppliers, outsourcers and the hardware/software they provide.",
        "mustKnow": [
            "Perform due diligence on vendors; require security requirements in contracts and SLAs.",
            "Assess vendor security posture before onboarding and periodically afterwards.",
            "Software/hardware provenance matters: counterfeit, tampered or unsupported components are supply-chain risks.",
            "Define right-to-audit clauses and exit/transition plans; understand shared responsibility.",
        ],
    },
    "1.12": {
        "focus": "Security awareness, training and education: changing behaviour, not just delivering content.",
        "mustKnow": [
            "Awareness = what everyone must know; Training = teaching the skills for a role; Education = deep knowledge for specialists.",
            "New employees must be trained before access; training is repeated at least annually and after incidents.",
            "Measure effectiveness (phishing simulation results, completion rates), do not just count attendance.",
            "Cover: policy, acceptable use, incident reporting, social engineering, clean desk, password/passphrase hygiene, data handling.",
        ],
    },

    # ---------------- DOMAIN 2 ----------------
    "2.1": {
        "focus": "Identifying and classifying information and assets, and the roles that own and protect them.",
        "mustKnow": [
            "Classification levels map sensitivity to required protection; labelling is how the level is communicated.",
            "Information/data owner: accountable for classification, access rules and protection requirements.",
            "Custodian: implements and operates the controls chosen by the owner. User: follows the rules. Auditor: verifies.",
            "Classification criteria: value to the business, legal/regulatory obligations, sensitivity, criticality.",
            "Government: Top Secret, Secret, Confidential, Unclassified/Sensitive-but-Unclassified; commercial schemes are organisation-specific.",
        ],
    },
    "2.2": {
        "focus": "Handling requirements for information and media across its whole life, so that protection matches the classification.",
        "mustKnow": [
            "Handling rules cover marking, storage, transmission, distribution and disposal per classification level.",
            "Media must be labelled, logged and stored with physical protection appropriate to its content.",
            "Acceptable-use rules define what may be stored, processed or transmitted on company systems.",
        ],
    },
    "2.3": {
        "focus": "Provisioning and managing assets securely: knowing what you own, who owns it, and how it is allocated and retired.",
        "mustKnow": [
            "Maintain an accurate asset inventory (hardware, software, data, services) — you cannot protect what you have not identified.",
            "Assign an owner to every asset and record its classification and location.",
            "Secure provisioning: hardened standard images, least privilege, tracked allocation and return.",
            "Decommissioning must include secure data removal.",
        ],
    },
    "2.4": {
        "focus": "Managing the data lifecycle, especially secure destruction of data and media (the most heavily tested part).",
        "mustKnow": [
            "Data states: at rest, in transit, in use — each needs different controls.",
            "Clear protects against ordinary recovery; purge resists advanced recovery; destroy renders the media unusable. Choose and verify a method suitable for the medium and sensitivity.",
            "Degaussing applies to magnetic media, not SSDs. Multiple overwrites are not universally required; SSD spare cells and wear levelling require appropriate device sanitisation methods.",
            "Data remanence is the residual data left after deletion; it is why simple deletion is never sufficient.",
            "Crypto-shredding destroys the key rather than the data; paper is shredded/incinerated; dumpster diving and media reuse are classic attack vectors.",
        ],
    },
    "2.5": {
        "focus": "Retention: how long information is kept, and the legal/regulatory drivers that decide it.",
        "mustKnow": [
            "Retention periods come from legal, regulatory, contractual and business requirements — not from IT convenience.",
            "Keep records only as long as required and destroy them securely at end of life; over-retention increases liability.",
            "Litigation hold suspends normal destruction once litigation is reasonably anticipated.",
        ],
    },
    "2.6": {
        "focus": "Choosing data security controls and demonstrating compliance with them.",
        "mustKnow": [
            "Controls must be scoped to the data classification and the regulatory regime that applies.",
            "Baselines and standards translate policy into measurable, auditable requirements.",
            "Compliance is evidenced by records: inventories, classification decisions, access reviews, destruction certificates.",
        ],
    },

    # ---------------- DOMAIN 3 ----------------
    "3.1": {
        "focus": "Secure design principles applied to engineering processes — the principles exam questions most often test directly.",
        "mustKnow": [
            "Defence in depth / layering: multiple independent controls so no single failure is fatal.",
            "Least privilege, separation of duties, economy of mechanism, complete mediation, open design, psychological acceptability, least common mechanism.",
            "Fail-safe (fails to a safe state, e.g. doors unlock) vs fail-secure (fails closed, e.g. denies access).",
            "Keep it simple; do not rely on obscurity; isolate and encapsulate; minimise the attack surface; use secure defaults.",
            "Privacy by design builds minimisation and appropriate data use into the system; zero trust removes implicit trust based on network location.",
        ],
    },
    "3.2": {
        "focus": "Formal security models and the rules they enforce (no-read-up, no-write-down, integrity properties).",
        "mustKnow": [
            "Bell-LaPadula (confidentiality): simple security property = no read up; *-property (star) = no write down; plus the tranquility principle.",
            "Biba (integrity): no read down, no write up; prevents contamination by lower-integrity data.",
            "Clark-Wilson (integrity): well-formed transactions, separation of duties, constrained data items, transformation procedures and integrity verification.",
            "Brewer-Nash (Chinese Wall): prevents conflicts of interest, dynamically changes access as data is accessed.",
            "Other models: state machine, information-flow, non-interference, Take-Grant, Harrison-Ruzzo-Ullman, Graham-Denning, Lattice, Lipner, Goguen-Meseguer.",
            "Models express policy; mechanisms enforce it. Label-based confidentiality, transaction integrity and owner-controlled permissions solve different problems.",
        ],
    },
    "3.3": {
        "focus": "Selecting controls from security requirements — the control categories and their functions.",
        "mustKnow": [
            "By function: preventive, detective, corrective, deterrent, recovery, directive, compensating.",
            "By nature: technical (logical), administrative (management), physical.",
            "A compensating control is an alternative when the primary control is not feasible — the residual risk must still be accepted.",
            "Controls are chosen from risk assessment output and a control framework (e.g. NIST SP 800-53, ISO 27002).",
        ],
    },
    "3.4": {
        "focus": "Security capabilities of information systems: evaluation criteria, assurance, TCB concepts and hardware/OS security features.",
        "mustKnow": [
            "TCSEC (Orange Book) divisions D, C1/C2, B1/B2/B3, A1 — D is minimal, A1 is verified design.",
            "ITSEC separates functionality and assurance; Common Criteria (ISO 15408) uses EAL1–EAL7 and defines Protection Profile, Security Target, Target of Evaluation.",
            "Trusted Computing Base (TCB) is all hardware, software and firmware that enforces security; the security kernel implements the reference monitor which must be tamper-proof, always invoked and small enough to verify.",
            "Protection rings: ring 0 is the most privileged (kernel); ring 3 the least.",
            "Hardware roots of trust: TPM, HSM, secure enclave. Virtualisation adds hypervisor risk; covert channels leak data through shared resources.",
        ],
    },
    "3.5": {
        "focus": "Vulnerabilities inherent in architectures and technology elements (client, server, web, mobile, embedded, cloud, industrial).",
        "mustKnow": [
            "Buffer overflow, TOCTOU/race conditions, integer overflow and memory leaks come from unsafe code and resource handling.",
            "Web/mobile/embedded/IoT/SCADA systems each have characteristic weaknesses (unsafe defaults, weak update paths, long service life).",
            "Cloud, containers, microservices and serverless shift responsibility but never eliminate it.",
            "Input validation, error handling and sandboxing mitigate most of these classes.",
        ],
    },
    "3.6": {
        "focus": "Cryptography: algorithms, keys, digital signatures, PKI and the correct use of each — the largest single block of questions.",
        "mustKnow": [
            "Symmetric encryption uses a shared secret for efficient bulk protection. Authenticated encryption, such as AES-GCM, also detects tampering; DES, 3DES and RC4 belong to legacy material.",
            "Public-key algorithms have different roles: Diffie-Hellman agrees keys, signature schemes sign, and suitable RSA schemes encrypt or sign. Hybrid protocols combine these with symmetric encryption.",
            "A hash detects change only against a trusted reference; HMAC authenticates with a shared key. Signatures use a private key and support origin verification and non-repudiation when identity and keys are trustworthy.",
            "Modes: ECB is weak (patterns leak); CBC/CFB/OFB/CTR/GCM chain or stream; GCM also authenticates.",
            "PKI: CA, RA, certificates (X.509), CRL and OCSP for revocation, key escrow/recovery, trust models (hierarchical, mesh, web of trust).",
            "Key management is the hardest part: generation, distribution, storage, rotation, destruction; Kerckhoffs's principle says the algorithm may be public but the key must not.",
            "Steganography hides the existence of data; it complements, not replaces, encryption.",
        ],
    },
    "3.7": {
        "focus": "Cryptanalytic attacks — how cryptosystems are broken rather than bypassed.",
        "mustKnow": [
            "Ciphertext-only, known-plaintext, chosen-plaintext and chosen-ciphertext attacks (in increasing attacker power).",
            "Brute force depends on key length; birthday attack exploits hash collisions; rainbow tables precompute hashes.",
            "Analytic attacks: differential and linear cryptanalysis; implementation attacks: side-channel, timing, power, fault.",
            "Weak keys and key clustering mean some keys are insecure; meet-in-the-middle attacks the double encryption.",
            "Frequency analysis breaks simple substitution ciphers; polyalphabetic ciphers (Vigenère) resist it.",
        ],
    },
    "3.8": {
        "focus": "Applying security principles to site and facility design — choosing and laying out a location.",
        "mustKnow": [
            "Site selection considers crime rate, proximity to hazards (flood, earthquake, industrial), utilities, emergency services and visibility.",
            "CPTED (Crime Prevention Through Environmental Design) uses natural surveillance, natural access control and territorial reinforcement.",
            "Avoid obvious/visible locations; consider adjacency of hazardous neighbours and shared walls.",
        ],
    },
    "3.9": {
        "focus": "Physical security controls: perimeter, interior, fire, power and environmental protection.",
        "mustKnow": [
            "Perimeter: fencing, lighting, bollards, CCTV, guards; the higher the security need, the more layers.",
            "Interior: mantraps, turnstiles, locks, badges, visitor control, restricted/safe areas.",
            "Fire protection combines detection, alarms, evacuation and suitable suppression. Fire-class labels vary by jurisdiction; select agents and systems for the actual hazard, occupied space and applicable building requirements.",
            "Power: UPS for short outages, generators for long ones; brownout (low voltage), blackout (total loss), spike, surge, sag, fault.",
            "Environmental protection covers cooling, equipment-appropriate temperature and humidity, leak detection and EMI/RFI shielding. Faraday cages reduce electromagnetic leakage; secure-emissions controls address compromising emanations.",
            "Media storage, vaults and secure rooms protect backup data.",
        ],
    },

    # ---------------- DOMAIN 4 ----------------
    "4.1": {
        "focus": "Secure network architecture and design: layers, topologies, protocols, segmentation and transmission media.",
        "mustKnow": [
            "OSI layers and their protocols/data units: physical (bits), data link (frames, MAC), network (packets, IP/ICMP/routing), transport (segments, TCP/UDP), session, presentation, application.",
            "TCP is connection-oriented (three-way handshake); UDP is connectionless and used by DNS/DHCP/TFTP/SNMP.",
            "Topologies: bus, star, ring, mesh; LAN/WAN/MAN; intranet/extranet/internet; DMZ and screened subnets; VLANs and subnetting/CIDR.",
            "Media: UTP categories (Cat3/5/5e/6), coax (10Base2 = 185 m, 10Base5 = 500 m), fibre (immune to EMI, hardest to tap); attenuation and crosstalk.",
            "Architectures: circuit vs packet switching, frame relay, X.25, ISDN, ATM, MPLS, SDN/zero trust.",
        ],
    },
    "4.2": {
        "focus": "Securing network components: firewalls, IDS/IPS, routers/switches, proxies and wireless access.",
        "mustKnow": [
            "Firewalls: packet filtering (stateless), stateful inspection, application/proxy, NGFW; WAF protects web applications.",
            "IDS detects (signature vs anomaly/behaviour based); IPS blocks inline; HIDS on hosts, NIDS on the network — encryption limits NIDS visibility.",
            "Routers and switches: ACLs, VLANs, port security; a multilayer switch routes and switches.",
            "Wireless: WEP is broken; WPA/WPA2 (personal vs enterprise) and WPA3; 802.1x/EAP for authentication; site surveys for coverage.",
            "Proxies, load balancers, content filters, UTM and bastion/screened hosts reduce exposure.",
        ],
    },
    "4.3": {
        "focus": "Building secure communication channels: VPNs, secure protocols for web, e-mail, voice and remote access.",
        "mustKnow": [
            "IPsec: AH authenticates without encryption; ESP can provide encryption and integrity. Transport mode protects the payload; tunnel mode wraps the original IP packet. IKE negotiates keys and security associations.",
            "HTTPS uses TLS; SSL is obsolete. SSH and SFTP protect remote administration and file transfer; S/MIME and OpenPGP protect email content.",
            "Remote access: VPN concentrators, dial-up, callback systems, 802.1x/EAP (PEAP, LEAP); RADIUS/TACACS+ for centralised auth.",
            "Voice, fax and multimedia traffic need their own security (VoIP, WTLS in WAP).",
            "DNSSEC protects name resolution integrity; TFTP is inherently insecure (no authentication).",
        ],
    },

    # ---------------- DOMAIN 5 ----------------
    "5.1": {
        "focus": "Controlling physical and logical access to assets: the vocabulary of subjects, objects and access control categories.",
        "mustKnow": [
            "Subject (active entity requesting access) and object (passive resource being accessed).",
            "Access is granted on the basis of least privilege and need to know.",
            "Access control types: preventive, detective, corrective, deterrent, recovery, directive, compensating.",
            "Physical access (locks, guards, mantraps) and logical access (logon, ACLs, tokens) must be balanced.",
        ],
    },
    "5.2": {
        "focus": "Identification and authentication of people, devices and services — factors, credentials and biometrics.",
        "mustKnow": [
            "Identification claims an identity; authentication proves it; authorization determines what is allowed.",
            "Authentication factors: something you know (password/PIN), have (token, smart card), or are (biometrics, including behavioural traits). Location and device context inform risk but are not independent factor categories.",
            "Two-factor/strong authentication requires two DIFFERENT factor types — a password plus a PIN is still one factor.",
            "Passwords need length, compromised-password screening, rate limiting and salted, costly hashing. Change them after compromise; routine expiry and composition rules are not universal requirements. One-time codes resist reuse but may still be phished.",
            "Biometrics: FAR (Type II, accepts impostors), FRR (Type I, rejects valid users), CER/EER is the crossover point — lower CER is better.",
            "Devices and services need credentials too (certificates, keys, service accounts); smart cards may be contact, contactless, hybrid (two chips) or dual-interface (one chip).",
        ],
    },
    "5.3": {
        "focus": "Federated identity: letting an external trusted provider assert a user's identity across domains.",
        "mustKnow": [
            "SAML is XML-based and common for web SSO; OAuth 2.0 is for delegated authorization (not authentication); OpenID Connect adds an identity layer on OAuth.",
            "Identity provider (IdP) authenticates; service provider (SP) relies on the assertion/claims.",
            "Federation trust needs ongoing key rotation, metadata maintenance, claim validation and coordinated account removal.",
            "Risks: trust misconfiguration, token replay, assertion forgery, over-broad claims.",
        ],
    },
    "5.4": {
        "focus": "Authorization mechanisms: how the system decides what an authenticated subject may do.",
        "mustKnow": [
            "DAC lets owners grant permissions; MAC centrally enforces labels and clearances. Suitability depends on policy and enforcement, not a universal ranking.",
            "RBAC assigns permissions through job roles; rule-based controls apply conditions such as time or network origin.",
            "ABAC evaluates subject, object, action and environment attributes; precise policies require accurate attributes and careful rule testing.",
            "Implementations: access control matrix, ACLs (per-object), capability tables (per-subject), constrained user interfaces.",
            "Non-discretionary and content/context-dependent controls constrain what a user can see or do regardless of permissions.",
        ],
    },
    "5.5": {
        "focus": "The identity and access provisioning lifecycle: creating, changing, reviewing and removing accounts.",
        "mustKnow": [
            "Provisioning must be authorised by the data/asset owner and follow least privilege at creation.",
            "Role changes (transfers, promotions) must be re-authorised; do not accumulate privileges.",
            "Access reviews/recertification confirm entitlements periodically; role mining/engineering builds clean roles.",
            "Deprovisioning on termination must be immediate and complete across all systems.",
        ],
    },
    "5.6": {
        "focus": "Implementing authentication systems: protocols, centralised services and biometric system operation.",
        "mustKnow": [
            "Kerberos: ticket-based, time-synchronised, symmetric keys, KDC/AS/TGS, mutual authentication (SSO within a realm).",
            "Classic RADIUS uses UDP and hides the password field; TACACS+ uses TCP, protects the packet body and separates AAA. Neither legacy protection replaces a secure transport or trusted management network.",
            "LDAP/Active Directory as the directory service behind SSO.",
            "CHAP (challenge-response, never sends the password) vs PAP (cleartext) — PAP is insecure.",
            "Biometric system properties: FAR/FRR/CER, throughput rate, enrolment time, template storage; the enrolment and data-acquisition process affects user acceptance.",
        ],
    },

    # ---------------- DOMAIN 6 ----------------
    "6.1": {
        "focus": "Designing assessment, test and audit strategies: scope, rules of engagement and methodology before testing starts.",
        "mustKnow": [
            "Define scope, objectives, constraints, timelines and rules of engagement in writing and get authorisation.",
            "Choose the methodology to match the goal: audit, vulnerability assessment or penetration test are not interchangeable.",
            "Testing frequency is driven by risk, change and regulatory requirement.",
        ],
    },
    "6.2": {
        "focus": "Conducting security control testing: vulnerability assessment and penetration testing techniques.",
        "mustKnow": [
            "Vulnerability assessment identifies and ranks weaknesses; penetration testing actively exploits them to prove impact.",
            "Black box (no knowledge), white box (full knowledge), gray box (partial) — knowledge changes effort and coverage.",
            "Techniques: scanning, war dialing/driving, password cracking, social engineering, network mapping, control testing.",
            "Testing must be authorised, time-boxed and stop before damaging production; findings need evidence.",
        ],
    },
    "6.3": {
        "focus": "Collecting security process data: the measurements that show whether controls work.",
        "mustKnow": [
            "Metrics must be actionable, repeatable and tied to objectives (KPIs for performance, KRIs for risk).",
            "Sources: log and event data, vulnerability and patch status, incident counts, training completion, access review results.",
            "Continuous monitoring supplements periodic assessments with current evidence; independent testing still checks coverage and control effectiveness.",
        ],
    },
    "6.4": {
        "focus": "Analysing test output and reporting: turning findings into decisions.",
        "mustKnow": [
            "Classify findings by severity (e.g. CVSS) and distinguish real findings from false positives/negatives.",
            "Reports must be written for the audience: technical detail for engineers, risk and cost language for management.",
            "Include remediation recommendations, owners and target dates, then track them to closure.",
        ],
    },
    "6.5": {
        "focus": "Conducting or facilitating security audits: independent verification of controls and compliance.",
        "mustKnow": [
            "Auditors must be independent of the area audited; they report to management/board, not to the IT function they review.",
            "Evidence types: direct inspection, observation, interview, documentation review; sampling is normal.",
            "Relevant standards: ISO 19011 (audit guidance), SSAE 18 / SOC 1 and SOC 2 reports, SAS 70 (historical).",
            "Audit findings need a management response and remediation plan; audit trails/logs support the audit.",
        ],
    },

    # ---------------- DOMAIN 7 ----------------
    "7.1": {
        "focus": "Investigations and forensics: gathering evidence that will survive legal scrutiny.",
        "mustKnow": [
            "Chain of custody records who had the evidence, when and why, from seizure to presentation.",
            "Order of volatility: collect CPU registers/cache, RAM, then swap, then disk, then backups/archives.",
            "Work on forensic copies (bit-level images) using write blockers; hash the original and the copy.",
            "Evidence types: best evidence (original), secondary (copy), direct, circumstantial, hearsay (with business-record exception), testimonial.",
            "Deception and investigator conduct require legal review; entrapment rules and admissibility depend on jurisdiction and who conducts the investigation.",
            "Root-cause analysis determines why an incident happened, not just what happened.",
        ],
    },
    "7.2": {
        "focus": "Logging and monitoring: producing and reviewing the records that make detection and accountability possible.",
        "mustKnow": [
            "Log what matters (authentication, privilege use, changes, errors) with accurate timestamps and synchronised clocks.",
            "Centralise logs and protect them from tampering; retain per policy and legal requirement.",
            "SIEM correlates events across sources; UEBA baselines behaviour to spot anomalies.",
            "Review logs regularly — unreviewed logs provide no detection value.",
        ],
    },
    "7.3": {
        "focus": "Configuration management: knowing and controlling what is in the environment.",
        "mustKnow": [
            "Establish secure baselines/gold images, then detect and correct drift.",
            "Configuration items and the CMDB record the authorised state; configuration audits compare actual with authorised.",
            "Hardening removes unnecessary services, accounts and defaults.",
        ],
    },
    "7.4": {
        "focus": "Foundational operations concepts that keep day-to-day security trustworthy.",
        "mustKnow": [
            "Need to know, least privilege, separation of duties, job rotation, mandatory vacation, dual control, split knowledge.",
            "Privileged accounts (root, admin, service accounts) need extra control, monitoring and vaulting.",
            "SLAs and acceptable-use rules define the operating expectations with users and providers.",
            "Collusion defeats separation of duties — hence rotation, monitoring and mandatory vacation.",
        ],
    },
    "7.5": {
        "focus": "Resource protection: backups, redundancy and storage resilience (RAID is heavily tested here).",
        "mustKnow": [
            "Backup types: full (everything), incremental (changes since last backup of any type — fastest backup, slowest restore), differential (changes since last full — slower backup, faster restore).",
            "Archive vs restore procedure; verify restores, keep copies offsite, protect backup media to the same classification as the data.",
            "RAID 0 stripes without redundancy; RAID 1 mirrors; RAID 3 uses byte striping and dedicated parity; RAID 4 uses block striping and dedicated parity; RAID 5 distributes single parity; RAID 6 uses dual parity; RAID 10 stripes mirrored pairs.",
            "Journaling/shadowing/vaulting (electronic, remote, database shadowing) support recovery; clustering, failover and hot spares provide high availability and fault tolerance.",
            "Storage: SAN (block, dedicated network), NAS (file, over the LAN).",
        ],
    },
    "7.6": {
        "focus": "Incident management: the lifecycle from detection to lessons learned.",
        "mustKnow": [
            "Phases: preparation, detection/identification, containment, eradication, recovery, lessons learned/post-incident review.",
            "A CSIRT with defined roles, escalation paths and communication plans is the core of preparation.",
            "Contain the damage first; preserve evidence; do not destroy it while eradicating.",
            "Declare/report incidents as required by policy and regulation; the first responder's actions set the evidentiary quality.",
        ],
    },
    "7.7": {
        "focus": "Detective and preventive measures that operate the environment.",
        "mustKnow": [
            "IDS/IPS signatures vs anomaly/behavioural detection: signatures miss new attacks, anomaly detection produces false positives.",
            "Honeypots/honeynets deceive and gather intelligence; they must not become a pivot into production.",
            "Anti-malware categories: virus, worm, Trojan, rootkit, spyware, adware, logic bomb, backdoor.",
            "DLP, file-integrity monitoring, endpoint detection and response, sandboxing, allow-lists and block-lists.",
        ],
    },
    "7.8": {
        "focus": "Patch and vulnerability management: closing known weaknesses predictably.",
        "mustKnow": [
            "Cycle: inventory, scan, prioritise (severity + exposure + exploitability), test, deploy, verify.",
            "Use an emergency change process when an urgent fix exists; for an unpatched zero-day, limit exposure through isolation, feature restrictions and monitoring.",
            "Unsupported or end-of-life systems cannot be patched and need compensating controls and documented acceptance.",
        ],
    },
    "7.9": {
        "focus": "Change management: controlling alteration of the environment.",
        "mustKnow": [
            "Flow: request → impact analysis → test and plan rollback → approval → implementation → validation → documentation and review.",
            "Emergency changes are allowed but must be documented and reviewed afterwards.",
            "Change management and configuration management work together; version/change logs provide auditability.",
        ],
    },
    "7.10": {
        "focus": "Recovery strategies: the alternate processing arrangements available when the primary site is lost.",
        "mustKnow": [
            "Hot sites have ready equipment and usually recover fastest; warm sites need preparation; cold sites need equipment and restoration. Actual recovery time depends on data, staff and dependencies.",
            "Reciprocal agreements (mutual aid) are cheap but uncertain and legally weak; mobile and mirrored sites fill other niches.",
            "Site choice is driven by RTO/MTD and cost; the strategy must be tested.",
        ],
    },
    "7.11": {
        "focus": "Disaster recovery processes: activating and running the recovery.",
        "mustKnow": [
            "Declaration/activation criteria and authority must be defined in advance.",
            "Recovery teams (damage assessment, salvage, restoration, communications) have defined roles and alternates.",
            "The DR plan is business-driven, documented, distributed and maintained; it covers people, facilities, data and communications.",
        ],
    },
    "7.12": {
        "focus": "Testing disaster recovery plans and the five standard test types.",
        "mustKnow": [
            "Checklist review (read the plan), walkthrough/tabletop (discuss roles and steps), simulation (practice a scenario without moving operations).",
            "Parallel test: recovery site runs alongside production — least risky live test.",
            "Full-interruption test: primary is shut down and the alternate takes over — most realistic, most risky, needs management approval.",
            "Testing is how the plan's gaps are found; results must feed back into plan updates.",
        ],
    },
    "7.13": {
        "focus": "Business continuity planning and exercises: keeping the business running during and after disruption.",
        "mustKnow": [
            "BCP scope is the whole business, not just IT; it is owned by senior management and driven by the BIA.",
            "Crisis management and communication plans cover employees, customers, media and regulators.",
            "Exercises (including pandemic and succession scenarios) validate continuity capability and mutual-aid arrangements.",
        ],
    },
    "7.14": {
        "focus": "Implementing and managing physical security in operations.",
        "mustKnow": [
            "Layered perimeter: fencing, lighting, guards, CCTV, bollards, barriers; interior: badges, locks, mantraps, turnstiles.",
            "Visitor control, escorting, sign-in logs and restricted/safe areas protect the facility.",
            "Fire detection/suppression, HVAC and backup power must be maintained and monitored, not just installed.",
        ],
    },
    "7.15": {
        "focus": "Personnel safety and security concerns — the people side of physical security.",
        "mustKnow": [
            "Evacuation routes, assembly points, fire drills and emergency response procedures must be current and practised.",
            "Workplace violence, duress and travel security plans protect staff; consider OSHA/legal duties.",
            "Safety of people always takes precedence over protection of assets.",
        ],
    },

    # ---------------- DOMAIN 8 ----------------
    "8.1": {
        "focus": "Integrating security into the software/system development life cycle.",
        "mustKnow": [
            "Phases: initiation/requirements, design, development/acquisition, implementation/testing, operation/maintenance, disposal — security activity belongs in EVERY phase.",
            "Methodologies: waterfall and V-model are sequential; spiral emphasises risk; agile/Scrum is iterative; DevOps/DevSecOps automates security into delivery.",
            "Maturity models: CMM/CMMI levels 1–5 (initial, repeatable/managed, defined, quantitatively managed, optimising).",
            "Requirements must be testable; design must include security controls; disposal must destroy data.",
            "Application control and change control prevent unauthorised code reaching production.",
        ],
    },
    "8.2": {
        "focus": "Security controls inside the development ecosystem itself (tooling, repositories, build and environments).",
        "mustKnow": [
            "Protect source code and repositories with access control and audit; use version control and code signing.",
            "Separate development, test and production. Prefer synthetic or masked test data; any sensitive live data needs explicit approval and appropriate protection.",
            "CI/CD pipelines need secrets management, artifact integrity and automated security checks.",
            "Containers and orchestration need image provenance, least privilege and hardened base images.",
        ],
    },
    "8.3": {
        "focus": "Assessing whether software security actually works — review and test techniques.",
        "mustKnow": [
            "Code review (manual/peer) plus automated analysis: SAST (source, white box), DAST (running app, black box), IAST, SCA for dependencies.",
            "Fuzzing feeds malformed input to find crashes; regression and unit/integration testing confirm fixes stay fixed.",
            "Testing strategy can be top-down (stubs) or bottom-up (drivers); functional vs non-functional; white vs black box.",
            "Quality assurance covers process and product, not only defects.",
        ],
    },
    "8.4": {
        "focus": "Security impact of software you acquire rather than build.",
        "mustKnow": [
            "COTS/open-source and outsourced code must be assessed before acquisition (due diligence) and tracked afterwards (licences, updates, vulnerabilities).",
            "Software escrow protects continued access to source if the vendor fails.",
            "Third-party libraries and dependencies expand the attack surface; maintain an inventory (SBOM) and monitor advisories.",
            "Contracts should include security requirements, right to audit, patching obligations and support lifetime.",
        ],
    },
    "8.5": {
        "focus": "Secure coding and database security: the concrete defects and the practices that prevent them.",
        "mustKnow": [
            "Validate input on the server; encode output; never build SQL by concatenation — use parameterised queries/prepared statements.",
            "OWASP categories: injection (SQL/command), broken authentication/session management, XSS, CSRF, insecure deserialization, security misconfiguration, sensitive-data exposure.",
            "Buffer overflows come from unchecked bounds; use safe languages/libraries, bounds checking and memory management.",
            "Handle errors without leaking detail; fail safely; avoid race conditions and resource exhaustion.",
            "Database concepts: tables/rows/columns (tuples/attributes), primary and foreign keys, referential integrity, normalisation vs denormalisation, views, ACID transactions, concurrency and locking, plus database-specific risks: aggregation, inference and polyinstantiation.",
        ],
    },
}
