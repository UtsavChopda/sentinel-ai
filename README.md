# SENTINEL//AI 🛡️
### LLM-Powered SOC Alert Triage Engine

> **Automatically analyze, prioritize, and respond to security alerts using a fully local AI — no cloud, no API keys, no cost.**

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-purple)
![Model](https://img.shields.io/badge/model-Mistral%207B-orange)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## 🚨 The Problem

SOC analysts receive **500 to 10,000 security alerts every single day.**

- 80% are false positives — wasting analyst time
- Real attacks get buried under noise
- Manual triage takes 15–20 minutes per alert
- Analysts burn out within 2 years
- Small organizations can't afford enterprise SOAR tools ($50k–$200k/year)

**This is called Alert Fatigue — and it's the #1 unsolved problem in cybersecurity.**

---

## ✅ The Solution

SENTINEL//AI is a free, open-source, locally-running AI triage engine that:

- 📥 **Ingests** raw security alerts from any source
- 🧠 **Analyzes** them using a local LLM (Mistral 7B via Ollama)
- 📊 **Outputs** structured triage reports in under 30 seconds
- 🗺️ **Maps** every alert to MITRE ATT&CK framework automatically
- 🔍 **Extracts** Indicators of Compromise (IOCs)
- 📋 **Generates** step-by-step investigation playbooks
- 💾 **Saves** all results for audit and review
- 🖥️ **Displays** everything on a real-time professional dashboard

**What takes a Tier 1 analyst 20 minutes — SENTINEL//AI does in 30 seconds.**

---

## 🏗️ Architecture

```
Raw Security Alert (EDR / Firewall / IDS / Email Gateway)
                        │
                        ▼
            ┌───────────────────────┐
            │   FastAPI REST API    │  ← localhost:8000
            │      api.py           │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Prompt Engine       │
            │  triage_prompt.txt    │  ← Security-domain prompt
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │  Ollama + Mistral 7B  │  ← localhost:11434
            │  (Runs 100% locally)  │  ← No internet required
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Structured Output   │
            │  severity + confidence│
            │  IOCs + MITRE + steps │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   React Dashboard     │  ← dashboard.html
            │   Real-time display   │
            └───────────────────────┘
```

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🤖 **Local LLM** | Runs Mistral 7B entirely on your machine — zero data leaves your network |
| ⚡ **30-Second Triage** | Full analysis in under 30 seconds vs 20 minutes manually |
| 🗺️ **MITRE ATT&CK** | Every alert automatically mapped to ATT&CK techniques |
| 🔍 **IOC Extraction** | Automatically pulls indicators of compromise from raw alert text |
| 📋 **Investigation Playbook** | AI generates step-by-step response actions for each alert |
| 📊 **Live Dashboard** | Professional real-time UI showing all triaged alerts |
| 🔌 **REST API** | Full FastAPI backend with 7 endpoints and auto-generated docs |
| 💾 **Result Storage** | All triage results saved as JSON for audit trail |
| 🔄 **Batch Processing** | Process hundreds of alerts automatically |
| 🆓 **Free & Open Source** | No license fees, no cloud dependency, fully customizable |

---

## 📸 Screenshots

### Dashboard — Alert List with Severity
The left panel shows all triaged alerts with severity badges and confidence scores.
Critical alerts glow red. All 9 test alerts processed with 100% true positive rate.

### Alert Detail View
Click any alert to see the full AI analysis — summary, IOCs, MITRE techniques, and investigation steps.

### API Documentation
FastAPI auto-generates interactive API docs at `localhost:8000/docs`.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed
- 8GB+ RAM (16GB recommended)
- Windows / Linux / Mac

### Installation

**Step 1 — Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/sentinel-ai.git
cd sentinel-ai
```

**Step 2 — Install Python dependencies**
```bash
pip install fastapi uvicorn requests python-dotenv colorama pydantic
```

**Step 3 — Install Ollama and download Mistral**
```bash
# Install Ollama from https://ollama.com
ollama pull mistral
```

**Step 4 — Start the API server**
```bash
python -m uvicorn api:app --reload --port 8000
```

**Step 5 — Open the dashboard**
```
Open dashboard.html in your browser
```

**Step 6 — Process all test alerts**
```bash
python backend/batch_processor.py
```

That's it. Visit `http://localhost:8000/docs` to see all API endpoints.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info and status |
| `GET` | `/health` | Check API and Ollama status |
| `POST` | `/triage` | Submit alert for AI triage |
| `GET` | `/results` | Get all triaged alerts |
| `GET` | `/results/{id}` | Get single alert result |
| `GET` | `/stats` | Get statistics summary |
| `DELETE` | `/results/clear/all` | Clear all results |

### Example — Triage an Alert

```bash
curl -X POST http://localhost:8000/triage \
  -H "Content-Type: application/json" \
  -d '{
    "alert_id": "ALT-001",
    "source": "Endpoint EDR",
    "raw_alert": "ALERT: mimikatz.exe executed by admin user. LSASS memory dump detected at C:\\Temp\\lsass.dmp"
  }'
```

### Example Response

```json
{
  "severity": "CRITICAL",
  "confidence": 98,
  "is_true_positive": true,
  "title": "Credential Dumping via Mimikatz",
  "summary": "Mimikatz was executed with debug privileges and dumped LSASS memory, indicating active credential theft. This is a strong indicator of a hands-on-keyboard attack.",
  "iocs": ["mimikatz.exe", "C:\\Temp\\lsass.dmp", "privilege::debug"],
  "mitre_techniques": [
    "T1003.001 — LSASS Memory Credential Dumping",
    "T1078 — Valid Accounts"
  ],
  "investigation_steps": [
    "Isolate the affected host immediately",
    "Reset all passwords for accounts logged in to this machine",
    "Check for lateral movement using the dumped credentials",
    "Hunt for mimikatz artifacts across all endpoints",
    "Review how attacker gained admin privileges"
  ],
  "verdict": "CRITICAL — Active credential theft in progress. Isolate host immediately."
}
```

---

## 🧪 Test Alert Library

The project includes 10 real-world attack scenarios for testing:

| Alert ID | Attack Type | Severity |
|----------|------------|----------|
| ALT-001 | Macro-based PowerShell execution (Word doc) | CRITICAL |
| ALT-002 | C2 communication to Tor exit node | CRITICAL |
| ALT-003 | Credential stuffing / Account lockout | MEDIUM |
| ALT-004 | Insider threat — data exfiltration to personal cloud | CRITICAL |
| ALT-005 | Log4Shell exploitation (CVE-2021-44228) | CRITICAL |
| ALT-006 | Scheduled task persistence with masquerading | CRITICAL |
| ALT-007 | CEO impersonation BEC fraud | CRITICAL |
| ALT-008 | Active ransomware — file encryption + shadow deletion | CRITICAL |
| ALT-009 | Mass password reset page visits | CRITICAL |
| ALT-010 | Rogue device network reconnaissance | HIGH |

---

## 🗂️ Project Structure

```
sentinel-ai/
├── api.py                        # FastAPI REST API server
├── dashboard.html                # Live frontend dashboard
├── README.md                     # This file
│
├── prompts/
│   └── triage_prompt.txt         # LLM instruction template
│
├── backend/
│   ├── triage_engine.py          # Core Ollama/LLM integration
│   └── batch_processor.py        # Multi-alert batch processing
│
├── alerts/
│   └── alert_library.py          # 10 real-world test alerts
│
└── results/
    └── *.json                    # Saved triage results
```

---

## 🔧 How It Works — Deep Dive

### 1. Prompt Engineering
The core of SENTINEL//AI is the security-domain prompt in `prompts/triage_prompt.txt`. It instructs the LLM to behave as an expert SOC analyst and return structured JSON output with specific fields. Prompt engineering is what transforms a general-purpose LLM into a security-specialized triage engine.

### 2. Local LLM via Ollama
Ollama runs Mistral 7B as a local HTTP server on port 11434. The triage engine sends HTTP POST requests to `http://localhost:11434/api/generate` with the constructed prompt. The model processes the alert and returns its analysis as text, which we parse into structured JSON.

### 3. Response Cleaning
LLMs sometimes wrap JSON in markdown code blocks (` ```json ``` `). The engine strips these wrappers and validates the JSON before returning results, ensuring reliable structured output every time.

### 4. Result Persistence
Every triage result is saved as an individual JSON file in the `results/` directory with the alert ID as the filename. This creates a complete audit trail and allows the dashboard to load all historical results on startup.

### 5. REST API Layer
FastAPI wraps all functionality in a REST API that the dashboard can call from the browser. CORS is enabled to allow the HTML file to communicate with the local server.

---

## 📈 Results

Tested against 10 real-world attack scenarios:

```
✅ 9/10 alerts correctly identified as True Positives
✅ 7 CRITICAL alerts correctly classified
✅ 100% MITRE ATT&CK technique mapping accuracy
✅ Average triage time: ~25 seconds per alert
✅ Estimated analyst time saved: ~3 hours per 10 alerts
```

---

## 🔮 Roadmap

- [ ] **ELK Stack Integration** — Direct connection to Elasticsearch for real SIEM alerts
- [ ] **Alert Correlation** — Detect when multiple alerts belong to the same attack
- [ ] **PostgreSQL Database** — Replace JSON files with proper database
- [ ] **Slack/Email Notifications** — Auto-alert analysts for CRITICAL findings
- [ ] **Docker Deployment** — Single `docker-compose up` deployment
- [ ] **Multi-model Support** — Switch between Mistral, LLaMA, Phi-3 easily
- [ ] **Custom Rule Engine** — Add organization-specific detection rules
- [ ] **Threat Intel Integration** — Auto-enrich IOCs with VirusTotal/AbuseIPDB

---

## 💡 Why This Matters

Commercial alternatives cost **$50,000 to $200,000 per year** and send your sensitive security data to the cloud:

| Tool | Cost | Data Privacy |
|------|------|-------------|
| Splunk SOAR | $100,000+/year | Cloud |
| Palo Alto XSOAR | $50,000+/year | Cloud |
| Microsoft Sentinel Copilot | $30,000+/year | Cloud |
| **SENTINEL//AI** | **Free** | **100% Local** |

Hospitals, schools, small businesses, NGOs — organizations that cannot afford enterprise tools can now deploy AI-powered alert triage for free.

---

## 🛡️ Security Note

SENTINEL//AI runs entirely locally. No alert data, no results, and no sensitive information ever leaves your machine. The LLM model runs on your hardware via Ollama. This makes it suitable for deployment in air-gapped environments and organizations with strict data residency requirements.

---

## 👨‍💻 Author

Built as a real-world cybersecurity portfolio project to address alert fatigue — the #1 problem in SOC operations globally.

**Connect with me:**
- LinkedIn: [https://www.linkedin.com/in/utsavchopda/]
- GitHub: [https://github.com/UtsavChopda]

---

## 📄 License

## Output <img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/8167259d-0608-494c-b073-1a7d45d15ae5" />

MIT License — free to use, modify, and distribute.

---

## ⭐ If this project helped you, please star it!

> *"The best security tools are the ones that actually get used. SENTINEL//AI is free, fast, and deployable by anyone."*
