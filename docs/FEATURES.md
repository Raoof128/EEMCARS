# EEMCARS Feature List

Comprehensive feature catalog for the Essential Eight Maturity Continuous Assessment & Remediation System.

## Core Assessment Features

### Automated Evidence Collection

**Purpose:** Continuous, automated gathering of compliance evidence from multiple sources

**Key Capabilities:**
- **Multi-Source Integration:**
  - Microsoft Defender for Endpoint
  - Microsoft Intune
  - Azure Active Directory
  - Microsoft 365 Security Center
  - Windows Event Logs (via agents)
  - Linux Audit Logs (via agents)
  - Custom API integrations

- **Collection Frequency:** Configurable (default: every 6 hours)

- **Evidence Validation:**
  - Digital signature verification
  - Timestamp validation
  - Schema validation
  - Chain of custody tracking

- **Evidence Types:**
  - Configuration snapshots
  - Patch status
  - Application inventory
  - User access logs
  - Security policy states
  - Vulnerability scan results

**Business Value:**
- Eliminates manual evidence collection (saves 80%+ time)
- Ensures evidence authenticity
- Maintains audit trail
- Real-time compliance visibility

### Continuous Maturity Assessment

**Purpose:** Automated Essential Eight maturity level determination

**Key Capabilities:**
- **Assessment Execution:**
  - Automatic (scheduled)
  - Manual (on-demand)
  - Triggered (post-remediation)
  - Scoped (by asset group, pillar, or asset)

- **Maturity Calculation:**
  - ACSC Essential Eight Maturity Model compliance
  - Levels 0-3 for each pillar
  - Weighted scoring across requirements
  - Confidence scoring based on evidence quality

- **All 8 Pillars:**
  1. Application Control
  2. Patch Applications
  3. Configure Microsoft Office Macro Settings
  4. User Application Hardening
  5. Restrict Administrative Privileges
  6. Patch Operating Systems
  7. Multi-Factor Authentication
  8. Regular Backups

- **Assessment Reports:**
  - Overall compliance percentage
  - Maturity level per pillar
  - Detailed requirement breakdown
  - Asset-level compliance status
  - Change detection (vs. previous assessment)

**Business Value:**
- Objective, consistent scoring
- Eliminates manual assessment effort (weeks → minutes)
- Always up-to-date compliance status
- Audit-ready evidence

### Drift Detection

**Purpose:** Real-time detection of compliance degradation

**Key Capabilities:**
- **Automated Monitoring:**
  - Continuous evidence comparison
  - Maturity level change detection
  - Alert on degradation
  - Root cause analysis (automated)

- **Drift Event Details:**
  - What changed (specific control)
  - When detected (timestamp)
  - Root cause (user action, config change, patch rollback)
  - Impact assessment (score delta, risk level)
  - Evidence comparison (before/after)

- **Notifications:**
  - Email alerts
  - SMS notifications
  - Webhook integrations (Teams, Slack, SIEM)
  - Configurable severity thresholds

- **Analytics:**
  - Drift trends over time
  - Most affected pillars
  - Most affected assets
  - Recurring drift patterns
  - Average resolution time

**Business Value:**
- Prevents compliance backsliding
- Rapid incident response
- Identifies systemic issues
- Maintains continuous compliance

### Remediation Automation

**Purpose:** Automated and guided remediation of compliance gaps

**Key Capabilities:**
- **Automated Playbooks:**
  - Ansible-based automation
  - Pre-built playbooks for all Essential Eight controls
  - Cross-platform (Windows, Linux, Cloud)
  - Idempotent execution

- **Remediation Task Management:**
  - Automatic task creation (from drift events)
  - Priority assignment (Critical, High, Medium, Low)
  - Impact analysis (maturity improvement, asset count)
  - Effort estimation (time to complete)
  - SLA tracking

- **Execution Options:**
  - Immediate execution
  - Scheduled execution (maintenance windows)
  - Manual remediation (guided steps)
  - Bulk operations (multiple assets)

- **Progress Tracking:**
  - Real-time execution status
  - Asset-by-asset progress
  - Success/failure indicators
  - Detailed logs
  - Rollback capability

- **Available Playbooks:**
  - Enable application whitelisting (AppLocker, WDAC)
  - Deploy patches (Windows Update, WSUS, SCCM)
  - Configure Office macro settings (GPO, Intune)
  - Harden browsers (Chrome, Edge, Firefox policies)
  - Restrict admin privileges (UAC, LAPS, JIT)
  - Enable MFA (Azure AD conditional access)
  - Verify backups (Windows Backup, Azure Backup)
  - Custom playbooks (upload your own)

**Business Value:**
- Reduces remediation time from days to minutes
- Ensures consistent, repeatable fixes
- Minimizes human error
- Tracks remediation ROI

## Reporting & Analytics

### Executive Dashboard

**Purpose:** High-level compliance visibility for leadership

**Key Capabilities:**
- **Essential Eight Maturity Heatmap:**
  - Visual 8x4 grid (pillars x levels)
  - Color-coded compliance status
  - Interactive drill-down
  - Tooltip details

- **Key Metrics:**
  - Overall compliance score (percentage)
  - Total assets under management
  - Compliant vs. non-compliant assets
  - Active drift events
  - Open remediation tasks

- **Trend Analysis:**
  - 30-day maturity trends
  - Line chart (all 8 pillars)
  - Improvement/degradation indicators
  - Adjustable timeframes (7, 30, 90, 365 days)

- **Recent Activity:**
  - Latest assessments
  - Recent drift events
  - Completed remediations
  - Evidence collection status

**Business Value:**
- Executive-level visibility
- At-a-glance compliance status
- Board presentation ready
- Tracks compliance investment ROI

### Compliance Reports

**Purpose:** Detailed, audit-ready compliance documentation

**Report Types:**

#### 1. Executive Summary
- 1-2 page overview
- Overall compliance score
- Maturity by pillar
- Key achievements
- Top risks
- Recommendations
- Trend charts
- **Frequency:** Weekly, Monthly, Quarterly
- **Format:** PDF (presentation-ready)

#### 2. Technical Compliance Report
- Detailed assessment results
- Control-by-control analysis
- Evidence summary
- Non-compliant assets (detailed list)
- Remediation status
- Technical findings and recommendations
- **Frequency:** Monthly, On-demand
- **Format:** PDF, Excel

#### 3. Audit Evidence Package
- Assessment methodology
- Evidence collection summary
- Chain of custody documentation
- Maturity determination details
- Control testing results
- Raw evidence archive (optional)
- **Frequency:** Quarterly, Annual, On-demand
- **Format:** PDF + ZIP archive

#### 4. Drift Analysis Report
- Drift events by pillar
- Root cause analysis
- Resolution time metrics
- Recurring patterns
- Remediation effectiveness
- Recommendations to prevent drift
- **Frequency:** Monthly
- **Format:** PDF, Excel

#### 5. Custom Reports
- SQL query builder
- Visual report designer
- Custom metrics and KPIs
- Scheduled delivery
- Multiple export formats

**Report Features:**
- **Scheduled Delivery:** Auto-generate and email reports
- **Multi-Format Export:** PDF, Excel, CSV, JSON
- **Customization:** Logo, branding, classification markings
- **Distribution Lists:** Send to multiple recipients
- **Archive:** Historical reports retained
- **Compliance:** Suitable for audit submission

**Business Value:**
- Eliminates manual reporting effort
- Consistent, professional output
- Audit evidence readily available
- Supports compliance communication

### Assessment History & Comparison

**Purpose:** Track compliance progress over time

**Key Capabilities:**
- **Historical Assessments:**
  - Unlimited history retention
  - Searchable/filterable
  - Sortable by date, score, maturity
  - Export to CSV/JSON

- **Assessment Comparison:**
  - Side-by-side comparison (any two assessments)
  - Score delta calculation
  - Maturity level changes
  - Asset status changes (improved/degraded)
  - Control-level differences

- **Trend Visualization:**
  - Line charts (score over time)
  - Maturity trajectory per pillar
  - Improvement velocity
  - Forecast to target

- **Analytics:**
  - Average time between assessments
  - Best/worst scores
  - Improvement rate (% per week/month)
  - Time to achieve targets

**Business Value:**
- Demonstrates compliance improvement
- Identifies stagnation
- Supports budget justification
- Tracks remediation effectiveness

## User Management & Security

### Role-Based Access Control (RBAC)

**Purpose:** Granular access control based on job function

**Roles:**

#### 1. Admin
- **Permissions:** Full system access
- **Capabilities:**
  - User management (create, modify, delete)
  - System configuration
  - Integration management
  - Audit log access
  - Organization management (multi-tenancy)
  - Custom playbook upload

#### 2. SecOps (Security Operations)
- **Permissions:** Operational access
- **Capabilities:**
  - View all assessments
  - Execute assessments
  - Manage remediation tasks
  - Review and approve evidence
  - Configure controls
  - API access
  - Generate technical reports

#### 3. Auditor
- **Permissions:** Read-only access
- **Capabilities:**
  - View all data (assessments, evidence, controls, assets)
  - Export reports and evidence
  - Access audit logs
  - Generate compliance reports
  - No modification permissions

#### 4. Executive Viewer
- **Permissions:** Limited read-only access
- **Capabilities:**
  - Dashboard access
  - View summary reports
  - Export executive reports
  - No technical details access
  - No modification permissions

**RBAC Features:**
- **Least Privilege:** Users only see what they need
- **Audit Trail:** All actions logged
- **Session Management:** Automatic timeout, concurrent login limits
- **MFA Support:** Optional two-factor authentication
- **SSO Integration:** Azure AD, Okta, SAML 2.0

**Business Value:**
- Meets security best practices
- Supports audit requirements
- Prevents unauthorized changes
- Enables delegation

### Audit Logging

**Purpose:** Immutable record of all system activity

**Key Capabilities:**
- **Comprehensive Logging:**
  - User authentication (login/logout)
  - Assessment execution
  - Evidence collection
  - Remediation actions
  - Configuration changes
  - Report generation
  - Data exports
  - API calls

- **Log Details:**
  - Timestamp (millisecond precision)
  - User (username + email)
  - IP address
  - Action type
  - Before/after values (for changes)
  - Result (success/failure)
  - Session ID
  - Request ID (for correlation)

- **Log Security:**
  - Immutable (write-once)
  - Tamper-evident (cryptographic hashing)
  - Encrypted at rest (AES-256)
  - Geo-redundant storage

- **Log Retention:**
  - 7 years (compliance requirement)
  - Exportable (CSV, JSON, SIEM format)
  - Searchable/filterable
  - Compliance with Australian data sovereignty

**Business Value:**
- Meets audit requirements
- Forensic investigation capability
- Detects unauthorized access
- Compliance with regulations (Privacy Act, PSPF, ISM)

## Integration & API

### REST API

**Purpose:** Programmatic access to all EEMCARS functionality

**Key Features:**
- **OpenAPI 3.0 Specification:**
  - Interactive documentation (Swagger UI)
  - Auto-generated client SDKs
  - Complete endpoint catalog

- **40+ Endpoints:**
  - Authentication (token-based)
  - Assessment CRUD operations
  - Evidence retrieval
  - Control management
  - Remediation task management
  - Report generation
  - User management (admin only)
  - System configuration

- **RESTful Design:**
  - Standard HTTP methods (GET, POST, PUT, DELETE, PATCH)
  - JSON request/response
  - Pagination support
  - Filtering and sorting
  - Error handling (RFC 7807 Problem Details)

- **Security:**
  - JWT authentication
  - API key support (service accounts)
  - Rate limiting (100 req/min default)
  - CORS support (configurable)
  - HTTPS only (TLS 1.2+)

- **Versioning:**
  - URL-based versioning (/api/v1)
  - Backward compatibility guarantee
  - Deprecation notices

**Use Cases:**
- SIEM integration (Splunk, Sentinel, QRadar)
- SOAR automation (Phantom, Demisto)
- Custom dashboards (Power BI, Tableau, Grafana)
- ServiceNow integration
- Custom applications
- Bulk operations

**Business Value:**
- Enables automation
- Integrates with existing tools
- Reduces manual effort
- Extends platform capabilities

### Native Integrations

**Microsoft Defender for Endpoint:**
- Application inventory
- Patch status
- Vulnerability assessments
- Security configuration
- Real-time sync every 6 hours

**Microsoft Intune:**
- Device compliance status
- Configuration profiles
- Application deployment
- Update status
- Conditional access policies

**Azure Active Directory:**
- User accounts
- MFA status
- Privileged accounts
- Sign-in logs
- Conditional access

**Microsoft 365:**
- Office macro settings
- Email security
- DLP policies
- Compliance center data

**Windows Agents:**
- Local security policies
- Event logs (Security, Application, System)
- Installed software
- Service status
- Backup verification
- Registry settings

**Linux Agents:**
- Auditd logs
- Package management (apt, yum)
- Service status (systemd)
- Firewall configuration (iptables, ufw)
- File integrity monitoring

**Custom API:**
- RESTful API support
- Webhook callbacks
- JSON/XML data formats
- OAuth 2.0 authentication

**Business Value:**
- Leverages existing investments
- No duplicate data entry
- Always up-to-date
- Reduces integration costs

### Webhook Support

**Purpose:** Real-time event notifications to external systems

**Events:**
- Assessment completed
- Maturity level changed
- Drift detected
- Remediation completed
- Critical alert triggered

**Supported Platforms:**
- Microsoft Teams
- Slack
- SIEM platforms
- SOAR platforms
- Custom webhooks (HTTP POST)

**Payload:**
- JSON format
- Event type
- Timestamp
- Affected assets
- Compliance data
- Customizable fields

**Business Value:**
- Real-time alerting
- Integration with workflow tools
- Reduces notification latency
- Enables automation

## Platform Features

### Multi-Tenancy

**Purpose:** Support multiple organizations in single deployment

**Key Capabilities:**
- **Tenant Isolation:**
  - Separate databases per tenant (optional)
  - Schema isolation (default)
  - Data segregation (mandatory)
  - Cross-tenant queries prohibited

- **Centralized Administration:**
  - Global admin console
  - Tenant management (create, configure, delete)
  - Usage monitoring
  - License management

- **Per-Tenant Customization:**
  - Branding (logo, colors)
  - Custom controls
  - Assessment schedules
  - Notification settings
  - User roles

- **Cross-Tenant Analytics:**
  - Benchmark comparison
  - Industry averages
  - Best practice identification
  - Anonymized data only

**Use Cases:**
- Managed service providers (MSPs)
- Large enterprises (divisions as tenants)
- Government departments
- SaaS deployment

**Business Value:**
- Economies of scale
- Centralized management
- Tenant independence
- Revenue opportunity (SaaS)

### Agent Management

**Purpose:** Lightweight agents for Windows and Linux endpoints

**Windows Agent:**
- **Collection Sources:**
  - Event logs (Security, Application, System)
  - Security policy (Group Policy, Local Policy)
  - Installed applications (Registry, WMI)
  - Services (Service Control Manager)
  - Updates (Windows Update, WSUS)
  - Backup status (Windows Backup, Task Scheduler)

- **Deployment:**
  - Group Policy (GPO)
  - Microsoft Intune
  - SCCM
  - Manual installer (MSI)

- **Footprint:**
  - ~50 MB installed
  - <50 MB RAM usage
  - <5% CPU during collection (burst)
  - <1% CPU idle

**Linux Agent:**
- **Collection Sources:**
  - Audit logs (auditd)
  - Package management (dpkg, rpm)
  - Service status (systemd, init)
  - Firewall rules (iptables, ufw, firewalld)
  - File integrity (AIDE, Tripwire)
  - Backup scripts

- **Deployment:**
  - Ansible playbook
  - Chef/Puppet
  - Package managers (apt, yum)
  - Manual installer (tar.gz, rpm, deb)

- **Footprint:**
  - ~30 MB installed
  - <30 MB RAM usage
  - <3% CPU during collection
  - <1% CPU idle

**Agent Features:**
- **Secure Communication:**
  - TLS 1.2+ encryption
  - Certificate-based authentication
  - Mutual TLS (optional)

- **Resilience:**
  - Automatic retry on network failure
  - Offline queue (store-and-forward)
  - Graceful degradation

- **Management:**
  - Centralized configuration
  - Remote updates
  - Health monitoring
  - Automatic registration

**Business Value:**
- Comprehensive endpoint visibility
- Minimal performance impact
- Easy deployment
- Centralized management

### Search & Filtering

**Purpose:** Rapid data discovery

**Capabilities:**
- **Global Search:**
  - Keyboard shortcut (Ctrl/Cmd + K)
  - Search across: Assets, Controls, Evidence, Tasks
  - Fuzzy matching
  - Recent searches

- **Advanced Filtering:**
  - Multiple criteria (AND/OR logic)
  - Date ranges
  - Numeric ranges
  - Multi-select dropdowns
  - Saved filters

- **Sorting:**
  - Any column
  - Ascending/descending
  - Multi-column sort

- **Pagination:**
  - Configurable page size (10, 25, 50, 100)
  - Jump to page
  - Total count visible

**Business Value:**
- Rapid data discovery
- Improved productivity
- Better user experience

### Export & Import

**Purpose:** Data portability

**Export Formats:**
- PDF (reports, evidence)
- Excel (.xlsx)
- CSV
- JSON
- XML

**Export Scopes:**
- Current view (filtered/sorted)
- Selected rows
- All data
- Custom query

**Import Capabilities:**
- Bulk asset import (CSV, Excel)
- Evidence upload (JSON, XML, CSV)
- Custom control definitions (YAML)
- User import (CSV)

**Business Value:**
- Data portability
- Integration with other tools
- Bulk operations
- Backup/restore

## Security & Compliance

### Data Sovereignty

**Purpose:** Compliance with Australian data protection requirements

**Key Features:**
- **Australian Data Centers:**
  - Azure Australia East (primary)
  - Azure Australia Southeast (secondary)
  - No data leaves Australian regions

- **Compliance:**
  - Privacy Act 1988
  - PSPF (Protective Security Policy Framework)
  - ISM (Information Security Manual)
  - ACSC guidelines

- **Data Classification:**
  - OFFICIAL
  - OFFICIAL: Sensitive
  - PROTECTED (with additional controls)

**Business Value:**
- Meets government requirements
- Protects sensitive data
- Avoids legal issues
- Enables government contracts

### Encryption

**Purpose:** Protect data confidentiality

**Encryption at Rest:**
- AES-256 encryption
- Transparent Database Encryption (TDE)
- Encrypted backups
- Encrypted evidence storage

**Encryption in Transit:**
- TLS 1.2+ (HTTPS only)
- Certificate pinning (optional)
- Perfect forward secrecy
- Strong cipher suites only

**Key Management:**
- Azure Key Vault integration
- Hardware Security Module (HSM) backed
- Automatic key rotation
- Key access auditing

**Business Value:**
- Protects sensitive data
- Meets compliance requirements
- Prevents data breaches
- Supports audit

### Disaster Recovery

**Purpose:** Business continuity

**Backup Strategy:**
- **Automated Backups:**
  - Database: Daily (Azure Backup)
  - Evidence: Continuous (geo-redundant storage)
  - Configuration: Daily

- **Retention:**
  - Daily: 7 days
  - Weekly: 4 weeks
  - Monthly: 12 months
  - Yearly: 7 years (compliance)

- **Geo-Redundancy:**
  - Primary: Australia East
  - Secondary: Australia Southeast
  - Automatic replication

**Recovery:**
- **RTO (Recovery Time Objective):** 4 hours
- **RPO (Recovery Point Objective):** 1 hour
- **Point-in-Time Restore:** Up to 90 days

**Testing:**
- Quarterly DR tests
- Annual full failover test
- Documented procedures

**Business Value:**
- Protects against data loss
- Ensures business continuity
- Meets compliance requirements
- Reduces risk

## Performance & Scalability

### Performance

**Response Times:**
- Dashboard load: <2 seconds
- API calls: <500ms (p95)
- Assessment execution: 5-15 minutes (500 assets)
- Report generation: 10-60 seconds

**Throughput:**
- 100+ concurrent users
- 1000+ API requests/minute
- 10,000+ assets supported
- 100,000+ evidence items/day

**Optimization:**
- Database indexing
- Query optimization
- Caching (Redis)
- CDN (static assets)
- Lazy loading
- Pagination

### Scalability

**Horizontal Scaling:**
- Stateless backend (scale to N instances)
- Load balancing (Azure Load Balancer / App Gateway)
- Database read replicas
- Celery workers (auto-scale)

**Vertical Scaling:**
- Database tier upgrade
- Compute tier upgrade
- Memory/CPU expansion

**Auto-Scaling:**
- Kubernetes Horizontal Pod Autoscaler (HPA)
- CPU/memory-based scaling
- Min/max replica configuration
- Scale-down delay

**Business Value:**
- Supports growth
- Handles peak loads
- Cost optimization
- Future-proof

## Unique Differentiators

### 1. Continuous vs. Point-in-Time
**Traditional:** Annual/quarterly manual assessments
**EEMCARS:** Continuous automated monitoring

### 2. Objective vs. Subjective
**Traditional:** Spreadsheet self-assessment
**EEMCARS:** Evidence-based objective scoring

### 3. Reactive vs. Proactive
**Traditional:** Discover issues during audit
**EEMCARS:** Drift detection prevents degradation

### 4. Manual vs. Automated
**Traditional:** Weeks of manual effort
**EEMCARS:** Minutes for complete assessment

### 5. Generic vs. Essential Eight Native
**Traditional:** Adapt generic GRC tool
**EEMCARS:** Purpose-built for Essential Eight

### 6. Siloed vs. Integrated
**Traditional:** Separate tools for assessment, remediation
**EEMCARS:** End-to-end platform

### 7. Single-Use vs. Continuous Value
**Traditional:** Assessment data stale quickly
**EEMCARS:** Always current, always actionable
