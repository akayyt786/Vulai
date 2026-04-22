# VulnAI Orchestrator: Autonomous Security Discovery Engine

[![Next.js](https://img.shields.io/badge/Next.js-15.0-black?logo=next.js)](https://nextjs.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**VulnAI** is a next-generation autonomous penetration testing and security discovery engine. It leverages Large Language Models (LLMs) to orchestrate a multi-layered security analysis of targets, dynamically selecting and executing tools based on discovered findings.

---

## 🚀 Key Features

- **Autonomous Orchestration**: Uses AI to decide which security tools to run next based on previous results.
- **Multi-Layered Discovery**:
    - **Layer 1**: DNS, Subdomains, Ports, and Infrastructure.
    - **Layer 2**: Directory Fuzzing, Parameter Discovery, and Crawling.
    - **Layer 3**: Vulnerability Scans (SQLi, XSS, RCE, static analysis).
- **Real-time Live Engine**: Track tool execution and AI reasoning live via WebSockets.
- **Pause & Resume**: Suspend active scans at any point and resume them without losing progress.
- **Attack Chain Intelligence**: Automatically correlates findings to build potential attack paths.
- **Responsive Dashboard**: Modern, tech-inspired UI built with Next.js and Framer Motion.

---

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2 (Python 3.9+)
- **API**: Django REST Framework
- **Real-time**: Django Channels & Daphne (ASGI)
- **Task Queue**: Celery (Background tool execution)
- **AI Brain**: Claude 3.5 Sonnet / LLM Integration

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Styling**: Tailwind CSS 4.0
- **Animations**: Framer Motion
- **Icons**: Lucide React

---

## 🏁 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- Docker (Optional, for tool containerization)
- Redis (Required for Celery and WebSockets)

### Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/akayyt786/Vulai.git
   cd vulnai
   ```

2. **Backend Setup**:
   ```bash
   # Create and activate virtual environment
   python3 -m venv .venv
   source .venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Run migrations
   python manage.py migrate

   # Start the development server (ASGI) on port 8080
   python manage.py runserver 8080
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the App**:
   - Dashboard: [http://localhost:3000](http://localhost:3000)
   - API Root: [http://localhost:8080/api/](http://localhost:8080/api/)

---

## 🛡 Supported Security Tools

| Category | Tools Included |
| :--- | :--- |
| **Reconnaissance** | `nmap`, `dnsrecon`, `subfinder`, `whatweb`, `wafw00f`, `sslyze` |
| **Surface Mapping** | `ffuf`, `gobuster`, `arjun`, `katana` |
| **Vulnerability Scanning** | `nikto`, `nuclei`, `sqlmap`, `dalfox`, `commix`, `corsy` |
| **Code & Secrets** | `semgrep`, `bandit`, `trufflehog`, `gitleaks`, `trivy`, `checkov` |

---

## 📁 Project Structure

```text
vulnai/
├── apps/
│   ├── orchestrator/   # AI Brain and Logic
│   ├── scans/          # Scan and Finding models
│   ├── tools/          # Tool Registry and Executor
│   └── reports/        # Report generation
├── frontend/           # Next.js Application
├── scripts/            # Bootstrap and helper scripts
├── config/             # Django settings
└── utils/              # Common utilities
```

---

## 🤝 Contributing

We welcome contributions! Please see our [AGENTS.md](frontend/AGENTS.md) for contribution guidelines and roadmap.

---

## ⚖️ Legal Disclaimer

*VulnAI is intended for authorized security testing and educational purposes only. Unauthorized use against targets without explicit consent is illegal and unethical.*
