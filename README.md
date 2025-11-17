# EEMCARS - Essential Eight Maturity Continuous Assessment & Remediation System

[![CI/CD](https://github.com/yourusername/eemcars/workflows/CI%2FCD/badge.svg)](https://github.com/yourusername/eemcars/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/react-18.2-blue.svg)](https://reactjs.org/)

## 🎯 Overview

EEMCARS is a production-ready, enterprise-grade platform for **continuous Essential Eight maturity assessment and automated remediation**. Built specifically for organizations seeking to maintain and improve their cybersecurity posture in alignment with the Australian Cyber Security Centre's (ACSC) Essential Eight Maturity Model.

### Key Features

✅ **Automated Essential Eight Scoring** - Continuous maturity assessment (Levels 0-3) across all eight pillars
✅ **Real-time Evidence Collection** - Windows/Linux agents + Azure AD/Intune/Defender integrations
✅ **Drift Detection & Alerts** - Automatic detection of maturity regressions with severity scoring
✅ **Automated Remediation** - Ansible playbooks for one-click remediation
✅ **Executive Reporting** - PDF/CSV/JSON reports aligned with ACSC guidance
✅ **Enterprise Dashboard** - Real-time heatmaps, trends, and compliance tracking
✅ **Australian Data Sovereignty** - Deployed exclusively in Azure AU regions
✅ **RBAC & Audit Logging** - Four-tier role system with immutable audit trails

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Azure Application Gateway (WAF)              │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
┌───────▼────────┐                       ┌────────▼───────┐
│  React Frontend│                       │  FastAPI       │
│  (Dashboard)   │◄──────────────────────┤  Backend       │
└────────────────┘                       └────────┬───────┘
                                                  │
                 ┌────────────────────────────────┼────────────────┐
                 │                                │                │
        ┌────────▼────────┐            ┌─────────▼──────┐  ┌──────▼──────┐
        │  PostgreSQL     │            │  Redis Cache   │  │Azure KeyVault│
        │  (Flex Server)  │            │  (Celery)      │  │  (Secrets)   │
        └─────────────────┘            └────────────────┘  └──────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼──────┐  ┌───────▼──────────┐
│Windows Agents│  │  Linux Agents    │
│(PowerShell)  │  │  (Bash)          │
└──────────────┘  └──────────────────┘
```

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python 3.11 + FastAPI |
| **Frontend** | React 18 + Material-UI |
| **Database** | PostgreSQL 15 (Azure Flex Server) |
| **Cache** | Redis 7 |
| **Containers** | Docker + AKS |
| **IaC** | Terraform (Azure AU) |
| **Automation** | Ansible |
| **CI/CD** | GitHub Actions |
| **Monitoring** | Azure Monitor + Application Insights |

---

## 📋 Essential Eight Pillars

EEMCARS implements all eight mitigation strategies:

1. **Application Control** - Prevent unapproved program execution
2. **Patch Applications** - Security updates within defined timeframes
3. **Configure Microsoft Office Macro Settings** - Block/restrict macro execution
4. **User Application Hardening** - Disable Flash, Java, ads in browsers/PDFs
5. **Restrict Administrative Privileges** - JIT admin, PAWs, separation of duties
6. **Patch Operating Systems** - OS patches within 48hrs (critical) / 2 weeks (all)
7. **Multi-Factor Authentication** - MFA for all remote access and privileged actions
8. **Regular Backups** - Offline/immutable backups with quarterly restore testing

Each pillar includes:
- Maturity level validation (0-3) mapped to ACSC requirements
- Automated evidence collection and validation
- Drift detection with severity scoring
- Remediation playbooks

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Azure subscription (for production deployment)
- Terraform ≥ 1.5
- Python ≥ 3.11 (for local development)
- Node.js ≥ 18 (for frontend development)

### Local Development (Docker Compose)

```bash
# Clone repository
git clone https://github.com/yourusername/eemcars.git
cd eemcars

# Start all services
docker-compose up -d

# Initialize database
docker-compose exec backend python -m alembic upgrade head

# Load demo data (optional)
docker-compose exec backend python -m app.demo.seed_data

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

**Default Demo Credentials:**
- Username: `admin` / Password: `DemoUser123!`
- Username: `secops` / Password: `DemoUser123!`

### Azure Production Deployment

```bash
# Navigate to Terraform directory
cd terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -out=tfplan

# Deploy infrastructure
terraform apply tfplan

# Configure kubectl for AKS
az aks get-credentials --resource-group eemcars-production-rg --name eemcars-production-aks

# Deploy application to AKS
kubectl apply -f ../k8s/

# Get public IP
kubectl get service eemcars-frontend -n eemcars
```

---

## 📊 API Endpoints

### Authentication
- `POST /api/v1/auth/token` - Login and obtain JWT token
- `GET /api/v1/auth/me` - Get current user

### Controls
- `GET /api/v1/controls/` - List all Essential Eight controls
- `GET /api/v1/controls/{control_id}` - Get control details
- `POST /api/v1/controls/{control_id}/score` - Score control for asset

### Evidence
- `GET /api/v1/evidence/` - List evidence (filterable by asset/control)
- `POST /api/v1/evidence/` - Submit new evidence

### Assessments
- `POST /api/v1/assessments/run` - Trigger full assessment
- `GET /api/v1/assessments/` - List assessment runs
- `GET /api/v1/assessments/{run_id}` - Get assessment results

### Remediation
- `GET /api/v1/remediation/tasks` - List remediation tasks
- `POST /api/v1/remediation/tasks` - Create remediation task
- `POST /api/v1/remediation/tasks/{task_id}/execute` - Execute task

### Reports
- `POST /api/v1/reports/exec` - Generate executive report
- `GET /api/v1/reports/{report_id}/download` - Download report

### Dashboard
- `GET /api/v1/dashboard/summary` - Overall maturity summary
- `GET /api/v1/dashboard/maturity-heatmap` - Essential Eight heatmap
- `GET /api/v1/dashboard/trends` - Historical trends

**Full API documentation:** http://localhost:8000/api/docs

---

## 🔧 Agent Deployment

### Windows Agent (PowerShell)

```powershell
# Download agent
Invoke-WebRequest -Uri "https://your-server/agents/windows/eemcars-agent.ps1" -OutFile "eemcars-agent.ps1"

# Run agent
.\eemcars-agent.ps1 -ServerUrl "https://eemcars.yourorg.com" -HeartbeatInterval 300

# Install as Windows Service (optional)
New-Service -Name "EEMCARS-Agent" -BinaryPathName "powershell.exe -File C:\EEMCARS\eemcars-agent.ps1" -StartupType Automatic
Start-Service -Name "EEMCARS-Agent"
```

### Linux Agent (Bash)

```bash
# Download agent
curl -O https://your-server/agents/linux/eemcars-agent.sh
chmod +x eemcars-agent.sh

# Run agent
./eemcars-agent.sh

# Install as systemd service (optional)
sudo cp eemcars-agent.sh /usr/local/bin/
sudo cp eemcars-agent.service /etc/systemd/system/
sudo systemctl enable eemcars-agent
sudo systemctl start eemcars-agent
```

---

## 🎭 RBAC Roles

| Role | Permissions |
|------|------------|
| **Admin** | Full system access, user management, configuration |
| **SecOps** | Trigger assessments, execute remediation, manage evidence |
| **Auditor** | Read-only access to all data, export reports |
| **ExecViewer** | Dashboard access, executive reports only |

---

## 🔐 Security Features

- **Encryption at Rest**: AES-256 for all data in PostgreSQL and Azure Storage
- **Encryption in Transit**: TLS 1.2+ enforced for all connections
- **Secrets Management**: Azure Key Vault integration
- **Immutable Audit Logs**: All actions logged with database-level immutability
- **WAF Protection**: Azure Application Gateway with OWASP 3.2 rules
- **Network Segmentation**: Virtual network isolation with NSGs
- **RBAC**: Four-tier role-based access control
- **MFA Support**: Integrated with Azure AD Conditional Access

---

## 📈 Monitoring & Observability

- **Azure Monitor**: Infrastructure and application metrics
- **Application Insights**: Performance monitoring and distributed tracing
- **Log Analytics**: Centralized logging with 90-day retention
- **Prometheus Metrics**: Custom metrics for maturity scores
- **Health Checks**: Kubernetes liveness and readiness probes
- **Alerting**: Drift detection alerts via Azure Monitor

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest --cov=app --cov-report=html --cov-report=term

# Frontend tests
cd frontend
npm test -- --coverage

# E2E tests
npm run test:e2e

# Security scanning
docker run --rm -v $(pwd):/src aquasec/trivy fs /src
```

**Coverage Target:** ≥ 80% for scoring logic

---

## 📚 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md) - System design and data flows
- [API Reference](docs/API.md) - Complete API documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment steps
- [Essential Eight Mapping](docs/ESSENTIAL_EIGHT_MAPPING.md) - ACSC requirement mapping
- [Scoring Logic](docs/SCORING_LOGIC.md) - Maturity calculation algorithms
- [Agent Development](docs/AGENTS.md) - Custom agent development
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

---

## 🗺️ Roadmap

- [ ] Machine learning for maturity drift prediction
- [ ] Azure Sentinel automated playbook integration
- [ ] Policy-as-Code (OPA) for Essential Eight rules
- [ ] Audit mode: evidence bundle export with hashes
- [ ] Mobile app for executive dashboards
- [ ] Integration with ServiceNow/Jira for remediation workflows

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ACSC** for the Essential Eight Maturity Model
- **Microsoft** for Azure cloud infrastructure
- **FastAPI** and **React** communities

---

## 📞 Support

- **Documentation**: https://docs.eemcars.io
- **Issues**: https://github.com/yourusername/eemcars/issues
- **Email**: support@eemcars.io

---

**Built with ❤️ for Australian organizations committed to cybersecurity excellence.**
