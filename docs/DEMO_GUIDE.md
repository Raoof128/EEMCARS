# EEMCARS Demo Guide

Complete guide for demonstrating the Essential Eight Maturity Continuous Assessment & Remediation System.

## Pre-Demo Setup (5 minutes)

### 1. Start the System

```bash
# Quick start (recommended for demos)
./quickstart.sh

# Or use Docker Compose
docker-compose up -d

# Verify all services are running
make health-check
```

### 2. Load Demo Data

```bash
# Load comprehensive demo data
docker-compose exec backend python -m app.demo.seed_data

# Verify data loaded
curl http://localhost:8000/api/v1/health
```

### 3. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

**Demo Credentials:**
- **Admin:** admin@example.com / SecurePassword123!
- **SecOps:** secops@example.com / SecurePassword123!
- **Auditor:** auditor@example.com / SecurePassword123!
- **Executive:** exec@example.com / SecurePassword123!

## Demo Scenario: Healthcare Organization

**Organization:** Melbourne Health Services
**Size:** 500 endpoints, 200 users
**Current State:** Mixed maturity (Level 0-2)
**Goal:** Achieve Level 2 across all Essential Eight pillars

## Demo Flow (15-20 minutes)

### Part 1: Executive Overview (3 minutes)

**Login as:** exec@example.com

#### Dashboard Overview

Navigate to the main dashboard to show:

1. **Essential Eight Maturity Heatmap**
   - Visual representation of all 8 pillars
   - Current maturity levels (0-3) with color coding
   - Quick identification of weak areas

2. **Compliance Score**
   - Overall percentage: ~55% (current demo state)
   - Target: 66% (Level 2)
   - Gap analysis

3. **Key Metrics Cards**
   - Total Assets: 500
   - Compliant Assets: 275 (55%)
   - Active Drift Events: 23
   - Open Remediation Tasks: 47

**Talking Points:**
- "This dashboard provides executive-level visibility into our Essential Eight compliance posture"
- "Red/orange areas indicate where we need immediate attention"
- "The system continuously monitors 500 endpoints across the organization"

### Part 2: Detailed Assessment (5 minutes)

**Login as:** secops@example.com

#### Controls View

Navigate to **Controls** page:

1. **Filter by Pillar:** Application Control

2. **View Maturity Requirements:**
   - Level 0: No controls
   - Level 1: User-executed applications controlled
   - Level 2: All applications controlled via whitelisting
   - Level 3: Application control with validation

3. **Evidence Status:**
   - Show evidence collected from:
     - Microsoft Defender ATP
     - Intune device compliance
     - Windows Event Logs
   - Last collection: Real-time
   - Compliance: 67% (201/300 endpoints)

4. **Drill Down to Specific Control:**
   - Click "E8-AC-L2-REQ1" (Application whitelisting)
   - View detailed requirements
   - See pass/fail status by asset group
   - Review evidence supporting the assessment

**Talking Points:**
- "Each Essential Eight pillar has specific technical requirements at each maturity level"
- "We automatically collect evidence from Microsoft Defender, Intune, Azure AD, and other sources"
- "SecOps can drill down to see exactly which systems are non-compliant"

### Part 3: Evidence Collection (3 minutes)

Navigate to **Evidence** page:

1. **Recent Evidence:**
   - Show live evidence collection
   - Sources: Defender ATP, Intune, Azure AD, Windows Logs
   - Collection frequency: Every 6 hours
   - Last successful collection: 2 hours ago

2. **Evidence Details:**
   - Click on recent evidence item
   - View raw JSON payload
   - See extracted key findings
   - Validation status: Verified
   - Used in assessment: Yes

3. **Evidence Sources Configuration:**
   - Microsoft Defender ATP: Connected ✓
   - Microsoft Intune: Connected ✓
   - Azure AD: Connected ✓
   - Microsoft 365: Connected ✓
   - Windows Event Forwarding: 450/500 endpoints

**Talking Points:**
- "Evidence collection is fully automated - no manual reporting required"
- "We validate evidence authenticity before using it in assessments"
- "The system can ingest evidence from 10+ different security tools"

### Part 4: Drift Detection (3 minutes)

Navigate to **Drift Events** section:

1. **Recent Drift Event:**
   - **Asset:** DESKTOP-SALES-042
   - **Pillar:** Patch Applications
   - **Change:** Maturity Level 2 → Level 1
   - **Detected:** 15 minutes ago
   - **Reason:** 3 critical Office patches missing (detected via Intune)

2. **Drift Timeline:**
   - Show historical drift events over 30 days
   - Pattern analysis: Most drift on Fridays (users disabling updates)
   - Top affected pillar: Application Control

3. **Automated Response:**
   - Drift event triggered automatic remediation task
   - Remediation playbook: "Install Missing Office Patches"
   - Assigned to: IT Operations team
   - SLA: 24 hours (critical)

**Talking Points:**
- "The system detects compliance drift in near real-time"
- "When a system falls out of compliance, we automatically create remediation tasks"
- "This prevents compliance degradation from going unnoticed"

### Part 5: Remediation (4 minutes)

**Login as:** secops@example.com

Navigate to **Remediation Tasks**:

1. **Active Remediation Tasks (47 open):**
   - Critical: 8
   - High: 15
   - Medium: 24

2. **Select a Task:**
   - **Task:** "Enable application whitelisting on 23 endpoints"
   - **Pillar:** Application Control
   - **Priority:** High
   - **Impact:** Will improve 23 endpoints from Level 1 to Level 2
   - **Estimated Time:** 2 hours
   - **Automation:** Ansible playbook available

3. **View Remediation Playbook:**
   ```yaml
   name: Enable AppLocker Whitelisting
   platforms: [Windows 10, Windows 11, Windows Server 2019]
   steps:
     - Enable AppLocker service
     - Import approved application rules
     - Set enforcement mode
     - Verify policy application
     - Update evidence collection
   ```

4. **Execute Remediation:**
   - Click "Execute Playbook"
   - Select target endpoints (23 selected)
   - Review pre-execution checks
   - Start execution (show progress)
   - Estimated completion: 45 minutes

5. **Track Progress:**
   - Real-time execution status
   - 5/23 completed
   - 18/23 in progress
   - Logs available for each endpoint

**Talking Points:**
- "Remediation playbooks are pre-built and tested for each Essential Eight control"
- "We can execute remediation across hundreds of endpoints simultaneously"
- "The system tracks execution and automatically updates compliance status"
- "This reduces manual effort from days to minutes"

### Part 6: Reporting (2 minutes)

**Login as:** exec@example.com

Navigate to **Reports**:

1. **Generate Executive Report:**
   - Click "Generate Executive Summary"
   - Date Range: Last 30 days
   - Format: PDF
   - Generation time: 15 seconds

2. **Report Contents:**
   - Executive Summary (1 page)
   - Essential Eight Maturity by Pillar (charts)
   - Trend Analysis (30-day)
   - Top Risks and Recommendations
   - Compliance Status by Department
   - Remediation Progress
   - Audit Trail Summary

3. **Scheduled Reports:**
   - Weekly summary to CISO: Every Monday 9 AM
   - Monthly board report: First of month
   - Quarterly compliance report: End of quarter

4. **Export Options:**
   - PDF (for executives)
   - CSV (for analysis)
   - JSON (for integration)

**Talking Points:**
- "Automated reporting eliminates manual effort"
- "Reports are suitable for board presentation and audit evidence"
- "All data is traceable to source evidence"

## Advanced Features Demo (Optional - 5 minutes)

### Multi-Tenancy

**Login as:** admin@example.com

1. **Organization Management:**
   - Show multiple organizations: Melbourne Health, Brisbane Medical, Perth Care
   - Each org isolated (data sovereignty)
   - Centralized admin console

2. **Cross-Organization Comparison:**
   - Benchmark Melbourne Health against industry average
   - Identify best practices from high-performing orgs

### API Integration

Navigate to **API Documentation** (http://localhost:8000/docs):

1. **Show REST API:**
   - 40+ endpoints
   - Complete CRUD operations
   - Swagger documentation

2. **Example API Call:**
   ```bash
   # Get current maturity status
   curl -X GET "http://localhost:8000/api/v1/summary" \
     -H "Authorization: Bearer $TOKEN"
   ```

3. **Webhook Integration:**
   - Trigger on maturity change
   - Send to SIEM/SOAR
   - Real-time compliance feed

### RBAC Demo

Show different user roles:

1. **Admin** - Full system access, user management, system configuration
2. **SecOps** - Assessment execution, remediation, evidence review
3. **Auditor** - Read-only access, export capabilities, audit logs
4. **Executive** - Dashboard, reports, high-level metrics

## Demo Data Scenarios

The demo database includes:

### Organizations
- Melbourne Health Services (500 endpoints)
- Brisbane Medical Center (250 endpoints)
- Perth Care Hospital (150 endpoints)

### Asset Mix
- 40% Windows 10
- 30% Windows 11
- 20% Windows Server 2019
- 10% Linux servers

### Maturity Distribution
- **Application Control:** Level 2 (67%)
- **Patch Applications:** Level 1 (45%)
- **Office Macro Settings:** Level 2 (80%)
- **User Application Hardening:** Level 1 (55%)
- **Restrict Admin Privileges:** Level 2 (70%)
- **Patch Operating Systems:** Level 1 (50%)
- **Multi-Factor Authentication:** Level 2 (85%)
- **Regular Backups:** Level 2 (75%)

### Drift Events (Last 30 days)
- 143 total drift events
- 23 currently active
- 120 resolved
- Average resolution time: 18 hours

### Remediation Tasks
- 47 open tasks
- 328 completed (last 30 days)
- 89% automation success rate

## Common Demo Questions & Answers

### Q: How does this differ from manual Essential Eight assessments?

**A:** Traditional assessments:
- Manual spreadsheet tracking
- Annual or quarterly reviews
- Point-in-time snapshot
- Weeks to complete
- Subjective evidence evaluation

EEMCARS:
- Fully automated continuous monitoring
- Real-time drift detection
- Objective evidence-based scoring
- Always up-to-date
- Automated remediation

### Q: What data sources do you support?

**A:** Currently integrated:
- Microsoft Defender for Endpoint
- Microsoft Intune
- Azure Active Directory
- Microsoft 365 Security Center
- Windows Event Logs (via agents)
- Linux audit logs (via agents)
- Custom evidence APIs

Roadmap:
- CrowdStrike
- Qualys
- Tenable
- ServiceNow

### Q: How do you ensure data sovereignty for Australian organizations?

**A:**
- All data stored in Azure Australia East/Southeast
- No data leaves Australian regions
- Encryption at rest (AES-256) and in transit (TLS 1.2+)
- Compliant with PSPF, ISM, Privacy Act 1988

### Q: Can this be used for audit evidence?

**A:**
Yes. The system provides:
- Immutable audit logs
- Evidence chain of custody
- Timestamped assessments
- Exportable compliance reports
- All data traceable to source

### Q: What's the deployment time?

**A:**
- **Proof of Concept:** 1 day (Docker Compose)
- **Production (Azure):** 1 week
  - Day 1-2: Infrastructure (Terraform)
  - Day 3-4: Integration (Azure AD, Defender, Intune)
  - Day 5: Agent deployment
  - Day 6-7: Validation and training

### Q: What's the pricing model?

**A:** (Adjust based on your business model)
- Subscription based on endpoints
- Tiered pricing: 0-100, 101-500, 501-2000, Enterprise
- Includes: software, updates, support, training
- Optional: professional services for integration

## Post-Demo Follow-Up

### Materials to Provide:
1. PDF Export of demo report
2. Architecture diagram
3. Integration guide
4. ROI calculator
5. Reference architecture
6. Trial instance credentials

### Next Steps:
1. Schedule technical deep-dive
2. Provide trial environment (30 days)
3. Conduct integration assessment
4. Develop implementation plan
5. Provide pricing proposal

## Troubleshooting Demo Issues

### Services not starting:
```bash
docker-compose down -v
docker-compose up -d
make health-check
```

### Demo data not loading:
```bash
docker-compose exec backend python -m app.demo.seed_data --force
```

### Frontend not connecting:
```bash
# Check backend is running
curl http://localhost:8000/health

# Restart frontend
docker-compose restart frontend
```

### Performance issues:
```bash
# Allocate more resources to Docker
# Docker Desktop: Settings > Resources
# Recommended: 4 CPU, 8GB RAM
```

## Demo Environment Reset

```bash
# Complete reset (WARNING: Deletes all data)
docker-compose down -v
docker volume prune -f
docker-compose up -d
docker-compose exec backend python -m app.demo.seed_data
```

## Presentation Tips

1. **Start with the problem:** "Manual Essential Eight compliance is time-consuming and error-prone"
2. **Show immediate value:** "Real-time compliance visibility in one dashboard"
3. **Demonstrate automation:** "From drift detection to remediation in minutes"
4. **Use specific examples:** "23 endpoints out of compliance detected in real-time"
5. **End with ROI:** "Reduce compliance effort from weeks to hours"

## Demo Timing

- **Quick Demo:** 10 minutes (Dashboard + Assessment + Remediation)
- **Standard Demo:** 20 minutes (Full flow)
- **Deep Dive:** 45 minutes (Include advanced features, API, architecture)
- **Executive Briefing:** 5 minutes (Dashboard + Reports only)
