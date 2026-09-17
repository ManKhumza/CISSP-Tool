"""
Curated within-domain keywords for CISSP sub-section classification.

Two tiers per sub-section:
  strong : distinctive, decisive vocabulary (word-boundary matched)
  weak   : supporting vocabulary that only counts if a strong term already hit

Scoring: question text x3, options x1, explanation x0.25.
"""

SUBSEC_TERMS = {
    '1.1': {
        'strong': [
            'code of ethics', 'isc2 code of ethics', 'professional ethics', 'ethics canon',
            'canons of ethics', 'ethical violation', 'ethics violation', 'code of conduct',
            'certification revocation',
        ],
        'weak': [
            'ethics', 'ethical', 'preamble', 'professional conduct',
        ],
    },
    '1.2': {
        'strong': [
            'cia triad', 'confidentiality integrity availability', 'non-repudiation',
            'nonrepudiation', 'defense in depth', 'defence in depth', 'least privilege',
            'separation of duties', 'need to know', 'need-to-know', 'aaa', 'security concepts',
            'core security principles', 'confidentiality', 'integrity', 'availability',
            'accountability', 'authenticity', 'opposite of', 'security definition', 'cia',
        ],
        'weak': [
            'control objective', 'security objective',
        ],
    },
    '1.3': {
        'strong': [
            'security governance', 'governance', 'board of directors', 'steering committee',
            'security steering', 'organizational roles', 'security roles',
            'roles and responsibilities', 'chief information security officer', 'ciso',
            'organizational structure', 'security function', 'organizational culture',
            'senior management', 'ultimately responsible', 'responsibility for security',
            'accountable', 'management responsibility', 'security program',
            'security awareness program sponsor',
        ],
        'weak': [
            'committee', 'alignment', 'roles', 'responsibilities', 'culture',
            'management commitment',
        ],
    },
    '1.4': {
        'strong': [
            'due care', 'due diligence', 'negligence', 'intellectual property', 'copyright',
            'trademark', 'patent', 'trade secret', 'licensing', 'gdpr', 'hipaa', 'sarbanes-oxley',
            'sarbanes oxley', 'gramm-leach', 'glba', 'ferpa', 'cfaa', 'computer fraud and abuse',
            'computer crime', 'e-discovery', 'legal hold', 'transborder', 'jurisdiction',
            'liability', 'breach notification', 'export control', 'admissible', 'hearsay',
            'testimony', 'common law', 'civil law', 'criminal law', 'regulatory requirement',
            'compliance requirement', 'basel ii', 'basel iii', 'pci dss', 'safe harbor',
            'warranty', 'subpoena', 'digital millennium', 'economic espionage', 'privacy law',
            'data protection law',
        ],
        'weak': [
            'legal', 'law', 'regulation', 'regulatory', 'compliance', 'court', 'privacy',
            'contract', 'statute', 'liability',
        ],
    },
    '1.5': {
        'strong': [
            'criminal investigation', 'civil investigation', 'administrative investigation',
            'regulatory investigation', 'burden of proof', 'preponderance of evidence',
            'beyond a reasonable doubt', 'investigation type', 'fraud investigation',
            'investigation',
        ],
        'weak': [
            'investigator', 'evidence', 'interview', 'witness', 'subject of',
        ],
    },
    '1.6': {
        'strong': [
            'security policy', 'acceptable use policy', 'policy statement', 'policies standards',
            'standards procedures', 'procedures and guidelines', 'iso 27001', 'iso 27002', 'cobit',
            'itil', 'policy framework', 'hierarchy of documents', 'supporting documents',
            'policy document', 'security documentation', 'policy development', 'policy exception',
            'policy', 'standard', 'procedure', 'guideline', 'baseline', 'step-by-step',
            'step by step', 'control requirements', 'advisory policy', 'regulatory policy',
            'security policy framework',
        ],
        'weak': [
            'framework', 'documentation',
        ],
    },
    '1.7': {
        'strong': [
            'business impact analysis', 'recovery time objective', 'recovery point objective',
            'maximum tolerable downtime', 'business continuity', 'continuity planning',
            'continuity requirement', 'critical business function', 'bia',
        ],
        'weak': [
            'rto', 'rpo', 'mtd', 'downtime', 'outage', 'continuity', 'bcp',
        ],
    },
    '1.8': {
        'strong': [
            'personnel security', 'background check', 'background investigation',
            'reference check', 'non-disclosure agreement', 'employment agreement', 'job rotation',
            'mandatory vacation', 'employee termination', 'termination', 'hiring process',
            'employee handbook', 'employee privacy', 'drug testing', 'non-compete',
            'fidelity bonding', 'insider threat', 'employee screening', 'employee', 'personnel',
        ],
        'weak': [
            'employee', 'personnel', 'candidate', 'resume', 'onboarding', 'offboarding',
            'human resources',
        ],
    },
    '1.9': {
        'strong': [
            'risk assessment', 'risk analysis', 'risk management', 'risk mitigation',
            'risk transfer', 'risk avoidance', 'risk acceptance', 'risk reduction',
            'residual risk', 'total risk', 'inherent risk', 'annualized loss expectancy',
            'single loss expectancy', 'annualized rate of occurrence', 'exposure factor',
            'quantitative risk', 'qualitative risk', 'risk appetite', 'risk tolerance',
            'risk register', 'risk treatment', 'risk response', 'iso 27005', 'octave',
            'cost benefit analysis', 'countermeasure cost', 'asset value', 'risk analysis team',
            'risk assessment team', 'risk assessment methodology', 'threat and risk',
        ],
        'weak': [
            'risk', 'ale', 'sle', 'aro', 'likelihood', 'monetary', 'probability', 'threat',
            'vulnerability', 'impact',
        ],
    },
    '1.10': {
        'strong': [
            'threat modeling', 'threat modelling', 'threat model', 'stride', 'dread', 'pasta',
            'attack tree', 'attack surface', 'threat intelligence', 'threat actor', 'threat agent',
            'threat vector', 'reduction analysis', 'tara',
        ],
        'weak': [
            'adversary', 'threat',
        ],
    },
    '1.11': {
        'strong': [
            'supply chain', 'supply chain risk', 'vendor risk', 'third-party risk',
            'third party risk', 'supplier', 'procurement', 'outsourcing',
            'service level agreement', 'vendor assessment', 'supply chain management',
        ],
        'weak': [
            'vendor', 'third party', 'sla', 'contract', 'outsource',
        ],
    },
    '1.12': {
        'strong': [
            'security awareness', 'awareness program', 'security training', 'security education',
            'awareness training', 'security culture', 'phishing awareness', 'user education',
            'training program', 'security awareness training',
        ],
        'weak': [
            'awareness', 'training', 'education', 'culture', 'campaign',
        ],
    },
    '2.1': {
        'strong': [
            'classification', 'classify', 'labeling', 'labelling', 'asset inventory',
            'asset identification', 'information owner', 'data owner', 'system owner',
            'business owner', 'data custodian', 'custodian', 'data steward',
            'information classification', 'asset classification', 'declassification', 'top secret',
            'proprietary information', 'information ownership',
        ],
        'weak': [
            'asset', 'label', 'sensitivity', 'owner', 'ownership',
        ],
    },
    '2.2': {
        'strong': [
            'handling requirement', 'handling procedure', 'media handling', 'marking', 'handling',
            'storage requirement', 'protection requirement', 'distribution of information',
        ],
        'weak': [
            'storage', 'distribution', 'marking', 'handling',
        ],
    },
    '2.3': {
        'strong': [
            'provisioning', 'provision resources', 'resource allocation', 'asset management',
            'decommission', 'capacity planning', 'inventory management',
        ],
        'weak': [
            'resource', 'inventory', 'capacity', 'asset',
        ],
    },
    '2.4': {
        'strong': [
            'data lifecycle', 'information lifecycle', 'sanitization', 'sanitize', 'degauss',
            'remanence', 'overwriting', 'secure disposal', 'destruction', 'data at rest',
            'data in transit', 'data in use', 'data states', 'crypto-erase', 'shredding',
            'incineration', 'purging', 'clearing', 'media sanitization', 'secure destruction',
            'media', 'dumpster diving', 'media reuse', 'data remanence', 'clearing and purging',
            'magnetic media', 'media viability',
        ],
        'weak': [
            'delete', 'erase', 'disposal', 'lifecycle', 'destruct',
        ],
    },
    '2.5': {
        'strong': [
            'retention', 'record retention', 'retention policy', 'retention period', 'legal hold',
            'archival', 'retention schedule',
        ],
        'weak': [
            'archive', 'retain',
        ],
    },
    '2.6': {
        'strong': [
            'data security control', 'data governance', 'scoping', 'control baseline',
            'baseline control', 'data protection standard', 'data control',
        ],
        'weak': [
            'compliance', 'baseline', 'standard', 'control', 'requirement',
        ],
    },
    '3.1': {
        'strong': [
            'defense in depth', 'defence in depth', 'fail safe', 'fail secure', 'fail-safe',
            'fail-secure', 'economy of mechanism', 'complete mediation', 'open design',
            'psychological acceptability', 'least common mechanism', 'least privilege',
            'separation of duties', 'secure default', 'privacy by design', 'zero trust',
            'shared responsibility', 'trust but verify', 'work factor', 'keep it simple',
            'layering', 'abstraction', 'encapsulation',
        ],
        'weak': [
            'design principle', 'security principle', 'simplicity', 'minimize', 'isolation',
        ],
    },
    '3.2': {
        'strong': [
            'bell-lapadula', 'bell lapadula', 'biba', 'clark-wilson', 'clark wilson',
            'brewer-nash', 'brewer nash', 'chinese wall', 'state machine', 'information flow',
            'non-interference', 'take-grant', 'take grant', 'lattice', 'access matrix',
            'harrison-ruzzo-ullman', 'harrison ruzzo ullman', 'goguen-meseguer', 'graham-denning',
            'security model', 'simple security property', 'star property', 'tranquility',
            'no read up', 'no write down', 'no write up', 'no read down', 'multilevel security',
            'integrity model', 'confidentiality model', 'lipner',
        ],
        'weak': [
            'model', 'property', 'sutherland',
        ],
    },
    '3.3': {
        'strong': [
            'preventive control', 'detective control', 'corrective control', 'deterrent control',
            'compensating control', 'recovery control', 'directive control', 'technical control',
            'administrative control', 'physical control', 'logical control', 'control category',
            'countermeasure', 'safeguard', 'nist 800-53', 'control baseline', 'control selection',
            'control type', 'control objective', 'control requirements',
        ],
        'weak': [
            'control', 'requirement', 'risk decision',
        ],
    },
    '3.4': {
        'strong': [
            'common criteria', 'tcsec', 'orange book', 'itsec', 'evaluation assurance level',
            'protection profile', 'target of evaluation', 'trusted computing base',
            'security kernel', 'reference monitor', 'protection ring', 'hypervisor',
            'trusted platform module', 'secure enclave', 'covert channel',
            'certification and accreditation', 'security target', 'evaluated assurance',
            'assurance level', 'security evaluation', 'virtualization',
        ],
        'weak': [
            'eal', 'toe', 'tcb', 'tpm', 'hsm', 'assurance', 'ring', 'operating system',
        ],
    },
    '3.5': {
        'strong': [
            'buffer overflow', 'race condition', 'time-of-check', 'toctou', 'side channel',
            'sql injection', 'cross-site', 'embedded system', 'internet of things', 'scada',
            'industrial control', 'microservice', 'serverless', 'container', 'mobile device',
            'web application', 'client-based', 'server-based', 'malformed input', 'memory leak',
            'integer overflow', 'input validation', 'injection flaw', 'vulnerability',
        ],
        'weak': [
            'cloud', 'virtual machine', 'distributed', 'database', 'exploit', 'attack',
            'architecture',
        ],
    },
    '3.6': {
        'strong': [
            'encryption', 'encrypt', 'decrypt', 'decryption', 'cipher', 'ciphertext', 'plaintext',
            'cryptography', 'cryptographic', 'cryptosystem', 'symmetric', 'asymmetric', 'aes',
            '3des', 'des', 'rsa', 'ecc', 'elliptic curve', 'diffie-hellman', 'diffie hellman',
            'el gamal', 'blowfish', 'twofish', 'rc4', 'rc5', 'hash function', 'hashing', 'sha-1',
            'sha-256', 'sha', 'md5', 'hmac', 'message digest', 'digital signature', 'public key',
            'private key', 'secret key', 'key management', 'key escrow', 'key recovery',
            'key distribution', 'pki', 'certificate authority', 'registration authority',
            'digital certificate', 'x.509', 'crl', 'ocsp', 'certificate revocation', 'trust model',
            'block cipher', 'stream cipher', 'ecb', 'cbc', 'cfb', 'ofb', 'gcm',
            'initialization vector', 's/mime', 'pgp', 'steganography', 'quantum', 'fips 140',
            'cryptographic module', 'salt', 'nonce', 'one-time pad', 'substitution cipher',
            'transposition cipher', 'rot13', 'vigenere', 'enigma', 'kerckhoffs', 'cryptology',
            'hash value', 'digital envelope',
        ],
        'weak': [
            'key', 'algorithm', 'certificate', 'signature',
        ],
    },
    '3.7': {
        'strong': [
            'cryptanalysis', 'cryptanalytic', 'brute force', 'known plaintext', 'chosen plaintext',
            'chosen ciphertext', 'ciphertext only', 'meet in the middle', 'birthday attack',
            'collision', 'rainbow table', 'frequency analysis', 'differential cryptanalysis',
            'linear cryptanalysis', 'side-channel attack', 'timing attack', 'power analysis',
            'fault analysis', 'weak key', 'key clustering', 'analytic attack',
            'implementation attack', 'dictionary attack', 'replay attack',
        ],
        'weak': [
            'attack', 'cryptanalysis', 'cracking',
        ],
    },
    '3.8': {
        'strong': [
            'site selection', 'site design', 'cpted',
            'crime prevention through environmental design', 'facility location',
            'natural disaster', 'topography', 'geographic', 'adjacent building', 'utility service',
            'flood', 'earthquake', 'weather', 'site survey',
        ],
        'weak': [
            'location', 'building', 'site', 'area', 'facility',
        ],
    },
    '3.9': {
        'strong': [
            'fence', 'fencing', 'lighting', 'cctv', 'camera', 'guard', 'mantrap', 'turnstile',
            'bollard', 'perimeter', 'proximity reader', 'badge', 'fire suppression', 'sprinkler',
            'halon', 'fm-200', 'fire extinguisher', 'smoke detector', 'heat detector', 'hvac',
            'humidity', 'uninterruptible', 'generator', 'brownout', 'blackout', 'spike', 'surge',
            'emi', 'rfi', 'tempest', 'faraday', 'white noise', 'raised floor', 'water detection',
            'vault', 'strong room', 'locked door', 'physical security',
            'electromagnetic interference', 'electrical power', 'power outage', 'voltage',
            'humidity range', 'operating humidity', 'air conditioning', 'electrostatic',
            'fire detection', 'fire suppression system', 'fence height',
        ],
        'weak': [
            'power', 'fire', 'physical', 'lock', 'door', 'window', 'wall', 'detector',
        ],
    },
    '4.1': {
        'strong': [
            'osi model', 'seven layers', 'tcp/ip', 'tcp/ip model', 'topology', 'star topology',
            'ring topology', 'bus topology', 'mesh', 'segmentation', 'subnet', 'cidr', 'vlan',
            'dmz', 'demilitarized zone', 'screened subnet', 'extranet', 'intranet',
            'network address translation', 'packet switching', 'circuit switching', 'isdn',
            'ethernet', 'token ring', 'fddi', 'frame relay', 'x.25', 'atm', 'mpls',
            'software defined', 'sdwan', 'convergence', 'twisted pair', 'coaxial', 'fiber optic',
            'unshielded twisted', 'cat5', 'cat6', 'attenuation', 'crosstalk', 'baseband',
            'broadband', 'multilayer switch', 'repeater', 'hub', 'bridge', 'routing protocol',
            'static route', 'dynamic route', 'network design', 'private network', 'public network',
            'encapsulation', 'deencapsulation', 'bandwidth', 'cable', 'osi', 'iso/osi', 'tcp',
            'udp', 'ip header', 'ipv4', 'ipv6', 'icmp', 'arp', 'rarp', 'dhcp', 'dns', 'snmp',
            'ntp', 'bgp', 'ospf', 'rip', 'eigrp', 'datagram', 'subnet mask', 'default gateway',
            'three-way handshake', 'three way handshake', 'well-known port', 'port number',
            'network layer', 'transport layer', 'data link layer', 'physical layer',
            'session layer', 'presentation layer', 'application layer', 'source ip',
            'destination ip', 'packet header', 'tftp', 'ftp', 'telnet',
        ],
        'weak': [
            'network', 'protocol', 'layer', 'throughput', 'media',
        ],
    },
    '4.2': {
        'strong': [
            'firewall', 'packet filter', 'stateful inspection', 'proxy server',
            'application firewall', 'web application firewall', 'intrusion detection',
            'intrusion prevention', 'router', 'switch', 'load balancer', 'content filter',
            'network access control', 'unified threat management', 'modem', 'pbx', 'access point',
            '802.11', 'wep', 'wpa', 'wpa2', 'wpa3', 'bluetooth', 'infrared', 'screened host',
            'dual-homed', 'bastion host', 'honeypot', 'vpn concentrator', 'wireless', 'ids', 'ips',
            'endpoint', 'hids', 'nids', 'host-based intrusion', 'network-based intrusion',
            'signature-based', 'anomaly detection', 'behavioral-based', 'knowledge-based',
            'behavior-based',
        ],
        'weak': [
            'waf', 'nac', 'utm', 'host', 'device',
        ],
    },
    '4.3': {
        'strong': [
            'ipsec', 'isakmp', 'ike', 'tunnel mode', 'transport mode', 'ssl', 'tls', 'https',
            'ssh', 'sftp', 'secure shell', 'privacy enhanced mail', 'voice over ip', 'voip',
            'remote access', 'dial-up', '802.1x', 'eap', 'peap', 'leap',
            'extensible authentication', 'dnssec', 'secure channel', 'callback', 'call back',
            'war dialing', 'instant messaging', 'secure socket', 'tunnel', 's/mime', 'pgp', 'smtp',
            'pop3', 'imap', 'http', 'email gateway', 'send email', 'circuit level proxy',
            'application level proxy',
        ],
        'weak': [
            'vpn', 'email', 'telephony', 'fax', 'multimedia', 'radius', 'tacacs', 'secure',
        ],
    },
    '5.1': {
        'strong': [
            'access control', 'physical access', 'logical access', 'access control category',
            'access control type', 'access control mechanism', 'access control system',
        ],
        'weak': [
            'access', 'subject', 'object', 'asset',
        ],
    },
    '5.2': {
        'strong': [
            'identification', 'authentication', 'password', 'passphrase', 'passwords',
            'one-time password', 'multi-factor', 'multifactor', 'two-factor', 'something you know',
            'something you have', 'something you are', 'biometric', 'fingerprint', 'retina',
            'iris', 'hand geometry', 'signature dynamics', 'keystroke', 'facial recognition',
            'voice recognition', 'device authentication', 'credential', 'user id', 'token',
            'log-on', 'logon', 'same password', 'password policy', 'account lockout',
        ],
        'weak': [
            'account', 'identify', 'factor', 'pin', 'enrollment', 'identity',
        ],
    },
    '5.3': {
        'strong': [
            'federation', 'federated', 'saml', 'oauth', 'openid', 'oidc', 'identity provider',
            'service provider', 'claims', 'assertion', 'cross-domain', 'trust broker',
            'federated identity',
        ],
        'weak': [
            'trust relationship', 'third-party identity', 'single sign-on',
        ],
    },
    '5.4': {
        'strong': [
            'discretionary access control', 'mandatory access control',
            'role-based access control', 'rule-based access control',
            'attribute-based access control', 'access control list', 'capability table',
            'access matrix', 'non-discretionary', 'content-dependent', 'context-dependent',
            'constrained user interface', 'authorization', 'permission', 'entitlement',
            'content-dependent protection',
        ],
        'weak': [
            'dac', 'mac', 'rbac', 'abac', 'acl', 'role', 'privilege', 'rights',
        ],
    },
    '5.5': {
        'strong': [
            'provisioning', 'deprovisioning', 'account provisioning', 'access review',
            'recertification', 'account review', 'entitlement review', 'role mining',
            'access lifecycle', 'user lifecycle', 'account creation', 'account removal',
            'account termination', 'automated provisioning', 'access certification',
        ],
        'weak': [
            'account', 'lifecycle', 'onboarding', 'offboarding',
        ],
    },
    '5.6': {
        'strong': [
            'kerberos', 'radius', 'tacacs', 'diameter', 'ldap', 'active directory',
            'directory service', 'single sign-on', 'authentication server',
            'authentication protocol', 'chap', 'pap', 'biometric system', 'false acceptance',
            'false rejection', 'type i error', 'type ii error', 'crossover error rate',
            'throughput rate', 'enrollment time', 'challenge-response', 'smart card',
        ],
        'weak': [
            'sso', 'far', 'frr', 'cer', 'eer', 'template',
        ],
    },
    '6.1': {
        'strong': [
            'assessment strategy', 'test strategy', 'audit strategy', 'rules of engagement',
            'assessment plan', 'testing methodology', 'assessment methodology', 'audit charter',
            'scope of the assessment', 'scope of the audit', 'penetration testing methodology',
        ],
        'weak': [
            'scope', 'planning', 'frequency', 'methodology', 'strategy',
        ],
    },
    '6.2': {
        'strong': [
            'vulnerability assessment', 'vulnerability scan', 'penetration test',
            'penetration testing', 'ethical hacking', 'black box', 'white box', 'gray box',
            'grey box', 'war dialing', 'war driving', 'war chalking', 'password cracking',
            'port scan', 'network mapping', 'control testing', 'compliance testing',
            'social engineering', 'scan', 'scanner', 'penetration', 'vulnerability scanner',
            'network scanner',
        ],
        'weak': [
            'test', 'testing', 'audit',
        ],
    },
    '6.3': {
        'strong': [
            'metric', 'metrics', 'key performance indicator', 'key risk indicator', 'measurement',
            'process data', 'data collection', 'scorecard', 'benchmark', 'dashboard',
            'trend analysis', 'continuous monitoring', 'security metrics',
        ],
        'weak': [
            'kpi', 'kri', 'monitoring', 'logging', 'report',
        ],
    },
    '6.4': {
        'strong': [
            'false positive', 'false negative', 'cvss', 'risk rating', 'severity', 'remediation',
            'test output', 'management report', 'finding', 'remediation plan',
        ],
        'weak': [
            'report', 'recommendation', 'analysis', 'result',
        ],
    },
    '6.5': {
        'strong': [
            'security audit', 'auditor', 'auditing', 'compliance audit', 'sas 70', 'ssae', 'soc 1',
            'soc 2', 'iso 19011', 'internal audit', 'external audit', 'audit committee',
            'audit finding', 'audit trail', 'audit log', 'auditor independence', 'audit',
            'audit scope', 'audit report',
        ],
        'weak': [
            'evidence', 'independence',
        ],
    },
    '7.1': {
        'strong': [
            'forensic', 'forensics', 'chain of custody', 'order of volatility', 'write blocker',
            'bit-level image', 'root cause', 'best evidence', 'secondary evidence', 'entrapment',
            'enticement', 'interrogation', 'investigator', 'testimonial evidence', 'e-discovery',
            'forensic image', 'evidence collection', 'computer crime', 'evidence integrity',
        ],
        'weak': [
            'evidence', 'investigation', 'suspect', 'custody', 'seizure', 'surveillance',
            'interview',
        ],
    },
    '7.2': {
        'strong': [
            'logging', 'log management', 'audit trail', 'syslog', 'siem',
            'security information and event management', 'correlation', 'event log',
            'continuous monitoring', 'user behavior analytics', 'ueba', 'log retention',
            'centralized logging', 'log review', 'monitoring system', 'network monitoring',
        ],
        'weak': [
            'log', 'monitoring', 'alert', 'alarm', 'audit record', 'sampling',
        ],
    },
    '7.3': {
        'strong': [
            'configuration management', 'baseline configuration', 'cmdb', 'configuration item',
            'hardening', 'secure configuration', 'configuration audit', 'gold image',
            'standard build', 'configuration drift', 'default configuration',
            'unnecessary service',
        ],
        'weak': [
            'baseline', 'configuration', 'drift',
        ],
    },
    '7.4': {
        'strong': [
            'need to know', 'need-to-know', 'least privilege', 'separation of duties',
            'job rotation', 'mandatory vacation', 'dual control', 'two-person control',
            'split knowledge', 'privileged account', 'service level agreement', 'acceptable use',
            'collusion', 'superuser',
        ],
        'weak': [
            'sla', 'privilege', 'account', 'fraud', 'operational',
        ],
    },
    '7.5': {
        'strong': [
            'backup', 'restore', 'full backup', 'incremental backup', 'differential backup',
            'tape rotation', 'archive bit', 'offsite', 'redundancy', 'raid', 'mirroring',
            'striping', 'parity', 'clustering', 'failover', 'high availability', 'fault tolerance',
            'hot spare', 'storage area network', 'network attached storage', 'electronic vaulting',
            'remote journaling', 'database shadowing', 'tape', 'storage', 'cluster',
            'server cluster', 'raid level',
        ],
        'weak': [
            'media', 'availability', 'san',
        ],
    },
    '7.6': {
        'strong': [
            'incident response', 'incident management', 'incident handling', 'csirt',
            'containment', 'eradication', 'triage', 'incident response plan', 'response team',
            'escalation', 'first responder', 'damage containment', 'lessons learned', 'incident',
        ],
        'weak': [
            'notification', 'declaration', 'recovery', 'response',
        ],
    },
    '7.7': {
        'strong': [
            'intrusion detection', 'intrusion prevention', 'honeypot', 'honeynet', 'antivirus',
            'anti-virus', 'anti-malware', 'malware', 'virus', 'worm', 'trojan', 'rootkit',
            'spyware', 'adware', 'logic bomb', 'backdoor', 'data loss prevention',
            'file integrity', 'sandbox', 'endpoint detection', 'whitelist', 'blacklist', 'ids',
            'ips', 'signature-based detection', 'anomaly-based', 'knowledge-based ids',
            'behavior-based',
        ],
        'weak': [
            'ids', 'ips', 'dlp', 'edr', 'detection', 'prevention', 'signature', 'deception',
        ],
    },
    '7.8': {
        'strong': [
            'patch management', 'patches', 'patch', 'zero-day', 'zero day',
            'vulnerability management', 'hotfix', 'service pack', 'software update', 'end of life',
            'legacy system',
        ],
        'weak': [
            'update', 'remediation', 'vulnerability',
        ],
    },
    '7.9': {
        'strong': [
            'change management', 'change control', 'change request', 'change advisory board',
            'release management', 'rollback', 'change log', 'emergency change', 'change window',
            'authorized change',
        ],
        'weak': [
            'cab', 'version control', 'baseline', 'impact analysis', 'change',
        ],
    },
    '7.10': {
        'strong': [
            'hot site', 'warm site', 'cold site', 'mobile site', 'reciprocal agreement',
            'alternate site', 'backup site', 'recovery site', 'mirrored site', 'tertiary site',
            'recovery strategy',
        ],
        'weak': [
            'site', 'relocation',
        ],
    },
    '7.11': {
        'strong': [
            'disaster recovery', 'disaster recovery plan', 'disaster declaration', 'salvage',
            'recovery team', 'emergency response', 'business resumption', 'crisis management',
            'disaster recovery process',
        ],
        'weak': [
            'drp', 'disaster', 'crisis', 'recovery', 'activation',
        ],
    },
    '7.12': {
        'strong': [
            'drp test', 'disaster recovery test', 'tabletop', 'walkthrough', 'walk-through',
            'simulation test', 'parallel test', 'full interruption', 'checklist test',
            'test the plan', 'disaster recovery exercise',
        ],
        'weak': [
            'exercise', 'test', 'readiness',
        ],
    },
    '7.13': {
        'strong': [
            'business continuity', 'continuity plan', 'continuity of operations',
            'crisis communication', 'pandemic', 'business recovery', 'continuity exercise',
            'mutual aid',
        ],
        'weak': [
            'bcp', 'coop', 'continuity',
        ],
    },
    '7.14': {
        'strong': [
            'physical security', 'guard', 'fence', 'cctv', 'camera', 'lighting', 'perimeter',
            'access card', 'badge', 'mantrap', 'turnstile', 'restricted area', 'visitor', 'escort',
            'sign-in', 'bollard', 'barrier', 'fire suppression', 'sprinkler', 'halon', 'hvac',
            'generator', 'uninterruptible', 'lock', 'key control',
        ],
        'weak': [
            'physical', 'fire', 'power', 'ups', 'secure area',
        ],
    },
    '7.15': {
        'strong': [
            'safety', 'evacuation', 'osha', 'workplace violence', 'travel security', 'life safety',
            'first aid', 'duress', 'personal safety', 'employee safety', 'fire drill',
            'assembly point',
        ],
        'weak': [
            'emergency', 'emergency response',
        ],
    },
    '8.1': {
        'strong': [
            'sdlc', 'system development life cycle', 'software development life cycle',
            'development lifecycle', 'waterfall', 'agile', 'scrum', 'spiral model',
            'rapid application development', 'prototyping', 'devops', 'devsecops', 'v-model',
            'requirements phase', 'design phase', 'development phase', 'implementation phase',
            'maintenance phase', 'disposal phase', 'initiation phase', 'capability maturity',
            'cmmi', 'iso 12207', 'process improvement', 'system life cycle', 'life cycle phase',
            'compiler', 'interpreter', 'compiled code', 'interpreted code', 'expert system',
            'application control', 'business process', 'application development', 'programming',
            'source code', 'object-oriented', 'java', 'cobol', 'c++', 'bottom-up', 'top-down',
            'software testing approach', 'database management system', 'dbms',
        ],
        'weak': [
            'cmm', 'life cycle', 'project management', 'lifecycle', 'phase',
        ],
    },
    '8.2': {
        'strong': [
            'continuous integration', 'continuous delivery', 'ci/cd', 'version control',
            'source control', 'code repository', 'build pipeline', 'code signing',
            'development environment', 'test environment', 'infrastructure as code',
            'container orchestration', 'artifact repository', 'software configuration management',
            'repository', 'configuration process', 'software configuration',
            'change control board',
        ],
        'weak': [
            'pipeline', 'container', 'docker', 'kubernetes', 'orchestration', 'artifact', 'build',
        ],
    },
    '8.3': {
        'strong': [
            'code review', 'static analysis', 'dynamic analysis', 'sast', 'dast', 'iast',
            'software composition analysis', 'fuzzing', 'fuzz testing', 'code audit',
            'secure code review', 'static application security testing',
            'dynamic application security testing', 'regression testing', 'unit testing',
            'integration testing', 'test coverage', 'quality assurance', 'software testing',
            'bottom-up testing', 'top-down testing', 'functional testing', 'white box testing',
        ],
        'weak': [
            'sca', 'testing', 'test', 'defect', 'bug', 'penetration test',
        ],
    },
    '8.4': {
        'strong': [
            'acquired software', 'cots', 'commercial off-the-shelf', 'off-the-shelf',
            'open source', 'third-party software', 'software acquisition',
            'outsourced development', 'vendor software', 'escrow', 'third party',
            'purchased software',
        ],
        'weak': [
            'procurement', 'supply chain', 'library', 'dependency', 'license', 'outsourcing',
            'due diligence',
        ],
    },
    '8.5': {
        'strong': [
            'secure coding', 'input validation', 'output encoding', 'parameterized query',
            'prepared statement', 'stored procedure', 'sql injection', 'cross-site scripting',
            'cross-site request forgery', 'buffer overflow', 'bounds checking',
            'memory management', 'error handling', 'exception handling', 'owasp', 'code injection',
            'command injection', 'deserialization', 'format string', 'integer overflow',
            'resource exhaustion', 'pointer arithmetic', 'database view', 'relational database',
            'normalization', 'primary key', 'foreign key', 'referential integrity',
            'structured query language', 'denormaliz', 'denormalized', 'column', 'columns',
            'input accuracy', 'information accuracy', 'application control', 'table', 'row',
            'tuple', 'attribute', 'schema', 'concurrency', 'acid', 'polyinstantiation',
            'inference', 'aggregation', 'transaction', 'database security', 'weakest link',
            'best programming', 'sql',
        ],
        'weak': [
            'xss', 'csrf', 'sqli', 'sanitize', 'race condition', 'garbage collection',
            'type safety', 'database', 'sql', 'query', 'schema', 'tuple', 'table',
        ],
    },
}
