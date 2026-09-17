"""
Hand-written glossary entries for sub-sections the reference books treat only briefly,
plus overrides for a few mined definitions that were inaccurate.

OVERRIDE replaces a mined meaning; EXTRA adds a meaning when the term has none.
"""

OVERRIDE = {
    "3.2": {
        "security model":
            "A formal description of how a system enforces its security policy. The classic "
            "models — Bell-LaPadula (confidentiality), Biba and Clark-Wilson (integrity), "
            "Brewer-Nash (conflict of interest) — each define rules that govern access.",
        "lattice":
            "A partially ordered set of security levels used by mandatory access control. "
            "Every subject and object carries a label, and information may flow only in the "
            "directions the model permits.",
        "star property":
            "The Bell-LaPadula *-property (no write down): a subject may not write to an object "
            "at a lower sensitivity level, which prevents leakage of higher-classified data.",
        "integrity model":
            "A model that protects data from unauthorised or accidental modification — Biba "
            "(no read down, no write up) and Clark-Wilson (well-formed transactions, separation "
            "of duties) are the canonical examples.",
        "confidentiality model":
            "A model that prevents unauthorised disclosure; Bell-LaPadula is the standard "
            "example, using no read up and no write down rules over sensitivity labels.",
    },
    "4.1": {
        "tcp/ip":
            "The four-layer Internet protocol suite — network access (link), internet (IP), "
            "transport (TCP/UDP) and application — that maps onto and predates the seven-layer "
            "OSI reference model.",
    },
    "7.5": {
        "raid":
            "Redundant Array of Independent Disks — combining disks for performance and/or "
            "fault tolerance: RAID 0 striping, RAID 1 mirroring, RAID 5 distributed parity, "
            "RAID 6 dual parity, RAID 10 mirrored stripes.",
    },
    "7.1": {
        "forensic":
            "The application of scientific methods to the collection, preservation and analysis "
            "of evidence, so that findings can be relied on and presented in legal proceedings.",
    },
    "3.9": {
        "brownout":
            "A prolonged drop in supply voltage below the normal level; it can cause equipment "
            "to malfunction or overheat, so critical systems run on conditioned power.",
        "blackout":
            "A complete loss of electrical power. Long outages are covered by a generator, while "
            "brief ones are bridged by an uninterruptible power supply.",
        "surge":
            "A brief, sharp increase in voltage above the normal level; surge protectors divert "
            "it away from equipment.",
        "spike":
            "A momentary, very high-voltage burst. A surge protector or line conditioner is the "
            "usual countermeasure.",
    },
    "7.5": {
        "full backup":
            "A backup that copies every selected file, whether or not it has changed; it is the "
            "slowest to create but the fastest to restore.",
        "incremental backup":
            "A backup that copies only files changed since the last backup of any type; fastest "
            "to create, but every increment must be restored in order.",
        "differential backup":
            "A backup that copies every file changed since the last full backup; larger and "
            "slower than an incremental, but only the last full plus the latest differential "
            "are needed to restore.",
    },
    "8.3": {
        "white box testing":
            "Testing with full knowledge of the internal structure of the code or system, so the "
            "tester can target specific paths and logic.",
        "black box testing":
            "Testing with no knowledge of internal structure; the tester exercises the system "
            "only through its interfaces.",
    },
    "4.3": {
        "sftp":
            "SSH File Transfer Protocol — transfers files over an encrypted SSH channel, "
            "replacing the cleartext FTP.",
    },
    "7.14": {
        "access card":
            "A credential that opens a controlled door or turnstile when read by a card reader; "
            "often combined with a PIN or biometric for two-factor entry.",
    },
    "3.3": {
        "corrective control":
            "A control that repairs damage or restores normal operation after an incident, for "
            "example restoring from backup or applying a patch.",
        "preventive control":
            "A control that stops an incident from occurring, such as a firewall rule, a lock or "
            "a separation-of-duties procedure.",
        "detective control":
            "A control that identifies an incident while or after it happens, such as logging, "
            "an IDS alert or a review of audit trails.",
    },
    "2.1": {
        "data steward":
            "The role that manages data quality and metadata on behalf of the data owner, "
            "ensuring definitions, standards and usage rules are followed.",
    },
    "2.4": {
        "incineration":
            "Physical destruction of media by burning; it renders the data unrecoverable and is "
            "used for the highest classifications.",
        "degaussing":
            "Erasing magnetic media by applying a strong magnetic field. It destroys the data and "
            "the media's usability, and it does not work on optical or solid-state media.",
    },
    "3.2": {
        "graham-denning":
            "A security model that extends the access matrix concept by defining eight primitive "
            "operations for creating and deleting subjects, objects and rights, and for "
            "transferring rights between them.",
    },
}

EXTRA = {
    "1.1": {
        "ISC2 Code of Ethics":
            "The four mandatory canons every CISSP agrees to uphold: protect society and the "
            "common good; act honourably, honestly, justly and legally; provide diligent and "
            "competent service to principals; and advance and protect the profession.",
        "Canon 1 – society and the common good":
            "Protect society, the common good, necessary public trust and confidence, and the "
            "infrastructure. This canon ranks highest when duties conflict.",
        "Canon 2 – act honourably":
            "Act honourably, honestly, justly, responsibly and legally, and report unethical "
            "behaviour by other certificate holders.",
        "Canon 3 – service to principals":
            "Provide diligent and competent service to principals (employers and clients), "
            "including advising them honestly about risk.",
        "Canon 4 – advance the profession":
            "Advance and protect the profession, including promoting the understanding and "
            "acceptance of prudent security measures.",
        "peer review panel":
            "The ISC2 body that examines alleged Code of Ethics violations; sanctions range up "
            "to revocation of certification.",
        "organizational code of ethics":
            "An employer's own ethics policy. It may add obligations, but where it conflicts "
            "with the ISC2 Code, the ISC2 Code prevails.",
        "ethics and employment conflict":
            "A professional must not follow an employer instruction that would breach the Code "
            "of Ethics, even at the risk of their job.",
    },
    "2.2": {
        "handling requirements":
            "The rules for each classification level describing how information must be marked, "
            "stored, transmitted, shared and destroyed.",
        "marking (labelling)":
            "Applying the classification label to a document, file or medium so that anyone "
            "handling it knows the protection it requires.",
        "storage requirements":
            "The physical and logical protection required for media at each classification "
            "level, such as a locked container, safe or encrypted volume.",
        "distribution and transmission rules":
            "Who may receive the information and what protection is required while it is in "
            "transit, such as encryption, courier or signed receipt.",
        "acceptable use policy":
            "The rules describing how organizational systems, networks and information may "
            "legitimately be used, and what is prohibited.",
        "clean desk and clear screen":
            "Handling rules requiring sensitive material to be secured and displays locked when "
            "a workspace is left unattended.",
    },
    "2.3": {
        "asset inventory":
            "An accurate, maintained record of hardware, software, data and services, each with "
            "an owner, location and classification.",
        "asset owner":
            "The role accountable for an asset's classification, protection requirements and "
            "access decisions.",
        "secure provisioning":
            "Allocating accounts, equipment and data to a user or process under least privilege, "
            "based on an authorised request and a hardened standard build.",
        "standard build (baseline image)":
            "A hardened reference configuration used to deploy new systems consistently and "
            "predictably.",
        "decommissioning":
            "The controlled retirement of an asset: remove data securely, revoke access, update "
            "the inventory and dispose of hardware safely.",
    },
    "2.5": {
        "retention policy":
            "Rules defining how long each record type must be kept, driven by legal, regulatory, "
            "contractual and business requirements.",
        "retention schedule":
            "The practical timetable mapping record types to their retention period and the "
            "approved destruction method to use at end of life.",
        "legal hold":
            "Suspension of normal record destruction when litigation, audit or investigation is "
            "reasonably anticipated.",
        "over-retention":
            "Keeping information longer than required; it increases storage cost, discovery "
            "burden and legal liability.",
        "destruction at end of life":
            "Records must be destroyed by an approved method once their retention period "
            "expires, and the destruction evidenced.",
    },
    "5.5": {
        "provisioning":
            "Creating an identity and granting the minimum access its role requires, based on an "
            "authorised request from the asset owner.",
        "deprovisioning":
            "Removing accounts and access promptly and completely when a person leaves or "
            "changes role.",
        "access review (recertification)":
            "Periodic confirmation by managers or owners that each identity's entitlements are "
            "still required and appropriate.",
        "role mining / role engineering":
            "Analysing existing entitlements to derive clean, non-overlapping roles that "
            "simplify administration.",
        "entitlement":
            "A specific right, permission or resource granted to an identity.",
        "privilege creep":
            "The gradual accumulation of unnecessary access as users change roles; controlled by "
            "recertification and least privilege.",
    },
    "6.1": {
        "assessment strategy":
            "The documented plan for an assessment: objectives, scope, methodology, resources, "
            "timeline and constraints.",
        "rules of engagement":
            "The written agreement defining what testers may do, when, against which targets, "
            "and what is explicitly out of scope, together with the escalation path.",
        "scope":
            "The boundary of the assessment — which systems, networks, locations and time "
            "windows are included or excluded.",
        "test methodology":
            "The chosen approach (for example black, grey or white box, scanning versus "
            "exploitation) and the standard or framework it follows.",
        "audit charter":
            "The document establishing an audit function's authority, purpose, scope and "
            "reporting line to the board or audit committee.",
        "assurance":
            "The level of confidence that controls operate as intended, evidenced by testing and "
            "documented results.",
        "authorization to test":
            "Written management approval naming the targets and time window; without it testing "
            "is an attack and creates legal exposure.",
    },
    "6.4": {
        "finding":
            "A documented weakness or control deficiency with evidence, impact and severity, "
            "written so that it can be remediated and retested.",
        "severity rating":
            "A ranking, often CVSS-based, combining exploitability and impact to prioritise "
            "remediation.",
        "false positive":
            "A reported issue that is not actually a vulnerability, or is not exploitable in the "
            "system's real configuration.",
        "false negative":
            "A real vulnerability that the assessment failed to detect; it undermines confidence "
            "in the result.",
        "remediation recommendation":
            "The specific corrective action for each finding, with an owner and a target date.",
        "management report":
            "The summary of results written in business-risk language for decision makers, "
            "separate from the technical detail.",
    },
    "7.9": {
        "change management":
            "The process that ensures changes are requested, assessed, approved, tested, "
            "documented, reversible and reviewed after implementation.",
        "request for change (RFC)":
            "The formal proposal describing the change, its justification, risk and back-out "
            "plan.",
        "change advisory board (CAB)":
            "The group that evaluates and approves changes, including their security and "
            "availability impact.",
        "impact analysis":
            "Assessing how a proposed change affects security, availability and dependent "
            "systems before approval.",
        "emergency change":
            "An urgent change executed with expedited approval; it must still be documented and "
            "reviewed afterwards.",
        "rollback (back-out) plan":
            "The documented method for reverting a change if it fails or causes unacceptable "
            "impact.",
        "configuration control":
            "Ensuring that only approved, documented changes alter a system's authorised "
            "configuration.",
    },
    "7.10": {
        "hot site":
            "A fully equipped alternate facility with systems, data and connectivity ready for "
            "immediate takeover; the most expensive option and the shortest recovery time.",
        "warm site":
            "A partially equipped facility with power and network but requiring configuration "
            "and data restoration; typically hours to days to bring online.",
        "cold site":
            "Space, power and cooling only — equipment must be installed and data restored; "
            "days to weeks, and the cheapest option.",
        "mobile site":
            "A trailer or container-based facility that can be transported to a chosen location "
            "and brought online there.",
        "reciprocal agreement (mutual aid)":
            "Another organization agrees to host recovery operations; inexpensive but uncertain "
            "and legally weak.",
        "mirrored site":
            "A fully redundant site operating in parallel with the primary, giving the fastest "
            "and most seamless recovery.",
        "recovery strategy selection":
            "Choosing the alternate processing arrangement that meets the RTO/MTD at an "
            "acceptable cost.",
    },
    "7.12": {
        "read-through (checklist) review":
            "The team reviews the plan document against a checklist without performing any "
            "recovery steps; lowest cost and lowest risk.",
        "walkthrough (tabletop exercise)":
            "Participants discuss their roles and responses to a scenario, usually in a "
            "conference room, without touching systems.",
        "simulation test":
            "A practice run of a scenario that exercises response procedures but does not move "
            "operations to the recovery site.",
        "parallel test":
            "The recovery site processes data alongside production for a period; the least risky "
            "live test.",
        "full-interruption test":
            "Production is shut down and the alternate site takes over — the most realistic and "
            "most disruptive test, requiring senior management approval.",
        "DRP test objective":
            "Validate the plan's accuracy and team readiness, and identify gaps to correct "
            "before a real disaster.",
    },
    "7.15": {
        "personnel safety":
            "The controls that protect people from harm; safety always takes precedence over the "
            "protection of assets.",
        "evacuation route":
            "A predefined, signed path out of a facility, with at least two routes from each "
            "work area where possible.",
        "assembly point":
            "The designated safe location where personnel gather after evacuation so that "
            "everyone can be accounted for.",
        "duress system":
            "A silent alarm — such as a duress code or button — that lets a person under threat "
            "signal for help without alerting the attacker.",
        "workplace violence program":
            "Policy, training and reporting channels that prevent, recognise and respond to "
            "violent behaviour at work.",
        "OSHA":
            "The US Occupational Safety and Health Administration, which sets workplace safety "
            "requirements employers must meet.",
        "travel security":
            "Briefings, tracking and controls that protect personnel travelling or working in "
            "higher-risk locations.",
    },
    "1.11": {
        "supply chain risk management (SCRM)":
            "Identifying, assessing and mitigating the risk introduced by vendors, suppliers, "
            "service providers and the products or components they supply.",
        "vendor due diligence":
            "Assessing a supplier's security posture, financial stability and compliance before "
            "onboarding, and periodically afterwards.",
        "service level agreement (SLA)":
            "A contract defining the service, performance and security obligations of a "
            "provider, with remedies for failure.",
        "right to audit":
            "A contractual clause permitting the customer to verify the provider's security "
            "controls and practices.",
        "shared responsibility":
            "The division of security duties between the organization and its service "
            "providers; the organization always retains accountability for its data.",
        "counterfeit or tampered components":
            "Hardware or software of unknown or falsified provenance that may contain defects, "
            "malware or implants.",
    },
    "8.4": {
        "commercial off-the-shelf (COTS)":
            "Software purchased ready-made; assess its security, support lifetime and licensing "
            "before adoption.",
        "open source software":
            "Freely available source code; assess licence terms, provenance, maintenance "
            "activity and known vulnerabilities before use.",
        "software escrow":
            "A third party holds the source code so the customer can maintain the software if "
            "the vendor fails or withdraws support.",
        "software bill of materials (SBOM)":
            "An inventory of the components, libraries and dependencies contained in a product, "
            "used to track vulnerability exposure.",
        "third-party dependency risk":
            "Vulnerabilities in libraries or components the organization did not write but must "
            "still patch and monitor.",
        "outsourced development":
            "Development performed by a third party; requires security requirements in the "
            "contract, right to audit and acceptance testing.",
    },
    "1.5": {
        "investigation":
            "A formal inquiry into an event or allegation, conducted to establish the facts and "
            "support a decision, disciplinary action or legal process.",
        "criminal investigation":
            "An inquiry into an alleged offence against the state, conducted by law enforcement "
            "and proved beyond a reasonable doubt; sanctions can include imprisonment.",
        "civil investigation":
            "An inquiry into a dispute between parties, decided on the preponderance of the "
            "evidence; the remedy is usually monetary compensation.",
        "administrative investigation":
            "An internal inquiry into a breach of organizational policy; the outcome is "
            "disciplinary or procedural rather than criminal.",
        "regulatory investigation":
            "An inquiry by a government or industry body into compliance with the rules it "
            "enforces, which can lead to penalties or loss of licence.",
        "burden of proof":
            "The obligation on the party bringing a case to prove its assertions to the standard "
            "the forum requires.",
        "evidence":
            "Anything presented to establish the facts of a case; it must be relevant, authentic "
            "and admissible to be relied upon.",
        "e-discovery":
            "The identification, preservation, collection and production of electronically "
            "stored information for legal proceedings.",
        "interview versus interrogation":
            "An interview gathers information from a willing party; an interrogation is a "
            "structured questioning of a suspect, with different legal constraints.",
    },
    "2.6": {
        "data security controls":
            "The technical, administrative and physical safeguards applied to data according to "
            "its classification and the obligations that apply to it.",
        "baseline":
            "The minimum set of controls that must be applied to a system, data set or "
            "environment; deviations require documented approval.",
        "scoping":
            "Determining which systems, data, locations and controls fall inside a standard, "
            "regulation or audit and which are explicitly excluded.",
        "data governance":
            "The roles, policies, standards and processes that determine how data is managed, "
            "protected, shared and used.",
        "compliance requirement":
            "An obligation imposed by law, regulation, contract or standard that the "
            "organization must meet and be able to evidence.",
        "control framework":
            "A structured catalogue of controls — for example ISO/IEC 27002 or NIST SP 800-53 — "
            "used to select, organise and assess safeguards.",
        "audit trail":
            "Records that allow activity on data to be traced to an identity, used to detect "
            "misuse and to evidence compliance.",
    },
    "7.13": {
        "business continuity plan (BCP)":
            "The documented arrangements for keeping critical business functions running during "
            "and after a disruption, and for returning to normal operation.",
        "business impact analysis (BIA)":
            "The analysis that identifies critical business functions and the impact of their "
            "loss over time; it sets the priorities the BCP is built on.",
        "continuity of operations (COOP)":
            "The plan for keeping an organization's essential functions running from an "
            "alternate location or with reduced resources.",
        "crisis management":
            "The structure, decision authority and communications used to manage the wider "
            "organizational response to a major disruption.",
        "crisis communication":
            "Predefined messages, spokespeople and channels for informing staff, customers, "
            "media and regulators during a crisis.",
        "continuity exercise":
            "A rehearsal of the continuity plan that validates roles, communications and "
            "recovery capability, and identifies gaps to correct.",
        "recovery team":
            "The group with defined roles and alternates responsible for executing continuity "
            "and recovery activities.",
        "mutual aid agreement":
            "An arrangement with another organization to share resources or facilities during a "
            "disruption; helpful but not guaranteed.",
        "maximum tolerable downtime (MTD)":
            "The longest a business function can be unavailable before its loss becomes "
            "unacceptable to the organization.",
    },
}
