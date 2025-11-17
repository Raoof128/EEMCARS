# EEMCARS Architecture Documentation

## System Overview

EEMCARS is a microservices-based platform designed for continuous assessment of Essential Eight maturity levels. The system follows a modern cloud-native architecture with clear separation of concerns.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Internet Users                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│         Azure Application Gateway (WAF)                        │
│         - TLS Termination                                      │
│         - OWASP Rule Set 3.2                                   │
│         - DDoS Protection                                      │
└────────────────────────┬───────────────────────────────────────┘
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
┌───────────────┐              ┌─────────────────────┐
│   React SPA   │              │   FastAPI Backend   │
│   (Frontend)  │◄─────────────┤   (REST API)        │
│               │              │                     │
│ - Dashboard   │              │ - Authentication    │
│ - Controls    │              │ - Scoring Engine    │
│ - Evidence    │              │ - Evidence Mgmt     │
│ - Reports     │              │ - Assessment Runs   │
└───────────────┘              │ - Remediation       │
                               └──────────┬──────────┘
                                          │
                 ┌────────────────────────┼────────────────┐
                 │                        │                │
                 ▼                        ▼                ▼
        ┌────────────────┐      ┌────────────────┐  ┌──────────────┐
        │  PostgreSQL    │      │  Redis Cache   │  │ Azure Key    │
        │  Flex Server   │      │  (Celery)      │  │ Vault        │
        │                │      │                │  │              │
        │ - Controls     │      │ - Sessions     │  │ - DB Pass    │
        │ - Evidence     │      │ - Task Queue   │  │ - API Keys   │
        │ - Assessments  │      │ - Cache        │  │ - Secrets    │
        │ - Audit Logs   │      └────────────────┘  └──────────────┘
        └────────┬───────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
┌───────────────┐  ┌──────────────────┐
│Windows Agents │  │  Linux Agents    │
│(PowerShell)   │  │  (Bash)          │
│               │  │                  │
│ - AppLocker   │  │ - Package Mgmt   │
│ - WSUS        │  │ - PAM            │
│ - GPO         │  │ - Audit Logs     │
└───────────────┘  └──────────────────┘
```

## Components

### 1. Frontend (React SPA)

**Technology:** React 18, Material-UI, Recharts

**Responsibilities:**
- User interface for dashboard, controls, evidence, assessments
- Real-time visualization of maturity scores
- Trend analysis and reporting
- Authentication and session management

**Key Features:**
- Responsive design
- Real-time data updates
- Interactive charts (heatmaps, radar, line)
- Role-based UI components

**Communication:**
- HTTP/HTTPS to Backend API
- JWT token authentication
- RESTful API calls

### 2. Backend API (FastAPI)

**Technology:** Python 3.11, FastAPI, SQLAlchemy, Celery

**Responsibilities:**
- RESTful API endpoints
- Essential Eight scoring logic
- Evidence validation
- Assessment orchestration
- Drift detection
- Remediation task management

**Key Modules:**
- `api/endpoints/` - REST API routes
- `scoring/` - Essential Eight scoring engine
- `models/` - SQLAlchemy ORM models
- `services/` - Business logic layer
- `core/` - Configuration, security, utilities

**Communication:**
- Async PostgreSQL via SQLAlchemy
- Redis for caching and task queue
- Azure Key Vault for secrets
- Celery for background tasks

### 3. Database (PostgreSQL 15)

**Technology:** Azure Database for PostgreSQL Flexible Server

**Responsibilities:**
- Persistent data storage
- Relational data management
- Audit log immutability
- Transaction management

**Key Tables:**
- `users` - Authentication and RBAC
- `assets` - Endpoints being assessed
- `controls` - Essential Eight control definitions
- `maturity_requirements` - Level 0-3 requirements
- `evidence` - Collected evidence items
- `assessment_runs` - Assessment execution tracking
- `assessment_results` - Detailed scoring results
- `drift_events` - Maturity regressions
- `remediation_tasks` - Automated remediation
- `audit_logs` - Immutable activity log

**Features:**
- High availability with zone redundancy
- Automated backups (35-day retention)
- Point-in-time recovery
- Geo-redundant backups
- Private networking (VNet integration)

### 4. Cache Layer (Redis 7)

**Technology:** Redis 7 (Azure Cache for Redis)

**Responsibilities:**
- Session storage
- API response caching
- Celery task queue
- Celery result backend

**Usage Patterns:**
- Cache frequently accessed data (controls, requirements)
- Store temporary assessment states
- Queue background tasks
- Rate limiting

### 5. Background Workers (Celery)

**Technology:** Celery 5, Redis backend

**Responsibilities:**
- Scheduled assessments
- Long-running evidence processing
- Report generation
- Email notifications
- Automated remediation execution

**Task Types:**
- Periodic (cron-based) assessments
- On-demand assessment runs
- Report generation
- Evidence validation

### 6. Agents

#### Windows PowerShell Agent

**Capabilities:**
- AppLocker configuration check
- Windows Update status
- Office macro settings
- MFA configuration
- Backup schedule verification

**Evidence Types:**
- Application Control (AppLocker rules, logging)
- Patch Status (WSUS, Windows Update)
- Office Macros (GPO settings, registry)
- MFA (RDP NLA, conditional access)
- Backups (scheduled tasks, backup files)

#### Linux Bash Agent

**Capabilities:**
- Package manager status
- PAM configuration
- System audit logs
- Backup cron jobs
- SSH hardening

**Evidence Types:**
- Patch Status (apt/yum updates)
- Admin Privileges (sudo, wheel groups)
- MFA (PAM modules)
- Backups (cron, rsync)
- Application Hardening (Flash, Java disabled)

### 7. Azure Infrastructure

#### AKS Cluster
- Kubernetes orchestration
- Auto-scaling (3-10 nodes)
- Zone redundancy
- Azure CNI networking
- Azure Policy integration

#### Networking
- Virtual Network (10.0.0.0/16)
- Subnets for AKS, PostgreSQL, Gateway
- Network Security Groups
- Private DNS zones
- Service endpoints

#### Security
- Azure Key Vault for secrets
- Managed identities for services
- RBAC at Azure level
- Network isolation
- Private endpoints

#### Monitoring
- Log Analytics workspace
- Application Insights
- Azure Monitor alerts
- Diagnostic logs
- Metrics dashboards

## Data Flow

### Assessment Flow

```
1. User triggers assessment (Dashboard)
   ↓
2. Frontend sends POST /api/v1/assessments/run
   ↓
3. Backend creates AssessmentRun record
   ↓
4. Celery task queued for each asset/control combination
   ↓
5. Workers fetch evidence from database
   ↓
6. Scoring engine validates evidence against maturity requirements
   ↓
7. AssessmentResult records created
   ↓
8. Drift detection compares with previous results
   ↓
9. DriftEvent records created if regressions detected
   ↓
10. AssessmentRun marked as completed
   ↓
11. Frontend polls for results and updates dashboard
```

### Evidence Collection Flow

```
1. Agent collects system state (Windows/Linux)
   ↓
2. Agent calculates evidence hash (SHA-256)
   ↓
3. Agent sends POST /api/v1/evidence
   ↓
4. Backend validates evidence structure
   ↓
5. Evidence record created with timestamp
   ↓
6. Triggers assessment if continuous mode enabled
   ↓
7. Evidence available for next scoring run
```

### Remediation Flow

```
1. Assessment identifies gap (e.g., Level 2 not achieved)
   ↓
2. POST /api/v1/remediation/generate creates tasks
   ↓
3. RemediationTask records created with Ansible playbooks
   ↓
4. SecOps user reviews tasks in dashboard
   ↓
5. User executes task (POST /api/v1/remediation/tasks/{id}/execute)
   ↓
6. Celery worker runs Ansible playbook
   ↓
7. Execution log captured
   ↓
8. Task status updated
   ↓
9. Next assessment verifies remediation
```

## Security Architecture

### Authentication Flow

```
1. User enters credentials (Login page)
   ↓
2. POST /api/v1/auth/token
   ↓
3. Backend verifies password hash (bcrypt)
   ↓
4. JWT token generated (HS256)
   ↓
5. Token includes: username, role, expiry
   ↓
6. Frontend stores token in localStorage
   ↓
7. All subsequent requests include Authorization header
   ↓
8. Backend validates token on each request
```

### Authorization (RBAC)

| Role | Permissions |
|------|-------------|
| **Admin** | Full access, user management, configuration |
| **SecOps** | Trigger assessments, execute remediation, manage evidence |
| **Auditor** | Read-only access, export reports |
| **ExecViewer** | Dashboard and reports only |

### Data Protection

- **At Rest:** AES-256 encryption (PostgreSQL, Storage Accounts)
- **In Transit:** TLS 1.2+ enforced
- **Secrets:** Azure Key Vault integration
- **Audit:** Immutable logs with database triggers
- **Network:** Private endpoints, NSGs, WAF

## Scaling Considerations

### Horizontal Scaling
- Frontend: CDN + multiple replicas
- Backend: AKS auto-scaling (HPA)
- Database: Read replicas (future)
- Celery: Scale worker pods independently

### Performance Optimization
- Redis caching for frequently accessed data
- Database indexing on common queries
- Connection pooling (20 connections)
- Async I/O with FastAPI
- Frontend code splitting

### Capacity Planning
- 1000 assets: 3-node AKS cluster
- 5000 assets: 5-10 node cluster
- Database: GP_Standard_D4s_v3 (4 vCPU, 16 GB)
- Redis: Standard C1 (1 GB)

## Disaster Recovery

### Backup Strategy
- PostgreSQL: Automated daily backups (35-day retention)
- Geo-redundant backup storage
- Point-in-time recovery (5 minutes RPO)
- Application data in Azure Storage (GRS)

### High Availability
- AKS: Multi-zone deployment
- PostgreSQL: Zone-redundant HA
- Application Gateway: Multi-instance
- Redis: Zone redundancy

### Recovery Procedures
1. Database restore from backup
2. Infrastructure recreation via Terraform
3. Application deployment via CI/CD
4. Evidence restoration from blob storage

## Monitoring and Observability

### Metrics
- Application: Response times, error rates, throughput
- Infrastructure: CPU, memory, disk, network
- Database: Query performance, connection pool
- Custom: Maturity scores, drift events, assessment counts

### Logs
- Application logs → Log Analytics
- Audit logs → Immutable database table
- Infrastructure logs → Azure Monitor
- Retention: 90 days

### Alerts
- High error rate (>5%)
- Assessment failures
- Drift events (critical/high)
- Infrastructure health
- Certificate expiry

## Future Enhancements

1. **GraphQL API** - More efficient data fetching
2. **WebSocket** - Real-time assessment updates
3. **Machine Learning** - Predictive drift analysis
4. **Multi-tenancy** - Support multiple organizations
5. **Mobile App** - Native iOS/Android apps
6. **Advanced Analytics** - Predictive modeling, anomaly detection
