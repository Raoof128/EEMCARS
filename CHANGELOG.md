# Changelog

All notable changes to EEMCARS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-17

### Added

#### Backend
- Complete FastAPI backend with RESTful API
- Essential Eight scoring engine with maturity levels 0-3
- Automated evidence validation across all 8 pillars
- Drift detection with severity classification
- PostgreSQL database with comprehensive schema
- RBAC system (Admin, SecOps, Auditor, ExecViewer)
- Immutable audit logging with database triggers
- Celery integration for background tasks
- Redis caching layer
- JWT authentication with secure password hashing

#### Frontend
- React 18 dashboard with Material-UI
- Real-time maturity heatmap visualization
- Radar charts for Essential Eight overview
- 30-day trend analysis with line charts
- Evidence management interface
- Assessment run tracking
- Remediation task management
- Executive report generation interface
- Responsive design for all screen sizes

#### Agents
- Windows PowerShell agent for evidence collection
- Linux Bash agent for evidence collection
- Automated heartbeat and registration system
- Evidence hash integrity validation
- Support for Application Control, Patches, Office Macros, MFA, and Backups

#### Automation
- 5 Ansible playbooks for remediation:
  - Application Control configuration
  - Patch management verification
  - Office macro settings enforcement
  - MFA validation checks
  - Backup verification

#### Infrastructure
- Complete Terraform configuration for Azure AU regions
- AKS cluster with zone redundancy
- PostgreSQL Flexible Server with HA
- Azure Key Vault for secrets management
- Application Gateway with WAF (OWASP 3.2)
- Container Registry with geo-replication
- Virtual network with subnet segmentation
- Log Analytics + Application Insights

#### CI/CD
- GitHub Actions workflow for automated testing
- Security scanning with Trivy and Bandit
- Automated Docker image builds
- Automated AKS deployment
- Terraform infrastructure automation

#### Documentation
- Comprehensive README with quick start guide
- API documentation (OpenAPI/Swagger)
- Deployment guide for Azure
- Troubleshooting guide
- Contributing guidelines
- Architecture diagrams
- Essential Eight mapping documentation

#### Development Tools
- Docker Compose for local development
- Makefile with common commands
- Quick start script for one-command setup
- Health check scripts
- Database initialization scripts
- Demo data seeding

### Security
- TLS 1.2+ encryption in transit
- AES-256 encryption at rest
- Azure Key Vault integration
- WAF protection with OWASP rules
- Network segmentation with NSGs
- Immutable audit trails
- Role-based access control
- Secure password hashing (bcrypt)
- JWT token authentication

### Testing
- Unit tests for scoring engine
- Integration tests for API endpoints
- Test fixtures and conftest configuration
- pytest configuration
- Mock data for testing
- Test coverage targeting 80%+

## [Unreleased]

### Planned Features
- Machine learning for maturity drift prediction
- Azure Sentinel automated playbook integration
- Policy-as-Code (OPA) for Essential Eight rules
- Audit mode with evidence bundle export
- Mobile app for executive dashboards
- ServiceNow/Jira integration for remediation workflows
- Email notifications for drift events
- Scheduled assessment reports
- Custom report templates
- Advanced analytics dashboard
- API rate limiting
- GraphQL API support

### Known Issues
- None at initial release

---

## Version History

- **1.0.0** - Initial production release with complete Essential Eight assessment platform
