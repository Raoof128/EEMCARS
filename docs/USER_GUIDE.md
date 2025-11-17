# EEMCARS User Guide

Complete guide for using the Essential Eight Maturity Continuous Assessment & Remediation System.

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Roles](#user-roles)
3. [Dashboard](#dashboard)
4. [Controls Management](#controls-management)
5. [Evidence Collection](#evidence-collection)
6. [Assessment Execution](#assessment-execution)
7. [Drift Detection](#drift-detection)
8. [Remediation](#remediation)
9. [Reporting](#reporting)
10. [Administration](#administration)

## Getting Started

### First Login

1. Navigate to the EEMCARS URL (e.g., https://eemcars.yourorg.com)
2. Enter your email and password
3. Complete MFA challenge (if enabled)
4. Accept terms of service on first login

### Changing Your Password

1. Click your profile icon (top right)
2. Select "Account Settings"
3. Click "Change Password"
4. Enter current password
5. Enter new password (must meet complexity requirements)
6. Confirm new password

**Password Requirements:**
- Minimum 12 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character
- Cannot reuse last 5 passwords

## User Roles

### Admin

**Capabilities:**
- Full system access
- User management (create, modify, delete users)
- System configuration
- Integration management
- Audit log access
- Organization management

**Typical Users:** System administrators, IT managers

### SecOps (Security Operations)

**Capabilities:**
- View all assessments
- Execute assessments
- Manage remediation tasks
- Review and approve evidence
- Configure controls
- Access API

**Typical Users:** Security analysts, compliance officers, IT security team

### Auditor

**Capabilities:**
- Read-only access to all data
- Export reports and evidence
- View audit logs
- Generate compliance reports
- No modification permissions

**Typical Users:** Internal auditors, external auditors, compliance reviewers

### Executive Viewer

**Capabilities:**
- Dashboard access
- View summary reports
- Export executive reports
- No detailed technical access
- No modification permissions

**Typical Users:** CISO, CIO, Board members, Executive management

## Dashboard

The dashboard provides an at-a-glance view of your organization's Essential Eight maturity.

### Key Metrics Cards

**Total Assets:**
- Number of endpoints under management
- Includes: Workstations, servers, cloud resources
- Click to view asset inventory

**Compliant Assets:**
- Percentage of assets meeting target maturity
- Click to filter compliant vs. non-compliant

**Active Drift Events:**
- Number of assets that have degraded from previous maturity level
- Red indicator if >10 active drifts
- Click to view drift details

**Open Remediation Tasks:**
- Number of pending remediation tasks
- Color-coded by priority (red: critical, orange: high, yellow: medium)
- Click to view task queue

### Essential Eight Maturity Heatmap

**Layout:**
- 8 rows (one per pillar)
- 4 columns (maturity levels 0-3)
- Color coding:
  - Green: Requirement met
  - Yellow: Partially met
  - Orange: In progress
  - Red: Not met
  - Gray: Not applicable

**Interaction:**
- Click any cell to view detailed requirements
- Hover to see quick statistics
- Filter by asset group, department, or location

### Maturity Level Radar Chart

**Purpose:** Visual comparison of maturity across all 8 pillars

**Features:**
- Blue area: Current maturity
- Green line: Target maturity
- Red line: Minimum acceptable maturity
- Click legend to hide/show series

### Trend Chart

**Purpose:** Track maturity changes over time

**Features:**
- Line graph showing 30-day history (default)
- One line per pillar
- Adjustable date range (7, 30, 90, 365 days)
- Export to CSV
- Identify patterns and improvement trajectories

### Recent Assessments Table

**Columns:**
- Assessment Run ID
- Date/Time
- Status (Completed, In Progress, Failed)
- Overall Score
- Changes (↑ improved, ↓ degraded, → no change)
- Actions (View Details, Export)

**Actions:**
- Click row to view full assessment report
- Compare with previous assessment
- Export assessment data

## Controls Management

### Viewing Controls

1. Navigate to **Controls** page
2. Filter by:
   - Pillar (Application Control, Patch Applications, etc.)
   - Maturity Level (0, 1, 2, 3)
   - Compliance Status (Compliant, Non-Compliant, Partial)
   - Asset Type (Windows, Linux, Cloud)

### Control Details

Each control displays:

**Control ID:** Unique identifier (e.g., E8-AC-L2-REQ1)

**Description:** Detailed requirement text from ACSC Essential Eight

**Maturity Level:** Which level this control applies to

**Technical Requirements:**
- Specific configuration settings
- Required security controls
- Evidence needed for verification

**Current Status:**
- Compliant: X assets (percentage)
- Non-Compliant: Y assets (percentage)
- Unknown: Z assets (no evidence)

**Evidence Sources:**
- Which integrations provide evidence
- Last collection time
- Evidence validity period

**Remediation:**
- Available playbooks
- Estimated remediation time
- Impact assessment

### Customizing Controls

**Admin/SecOps Only**

1. Click "Edit Control" on control detail page
2. Modify:
   - Custom requirements (organization-specific)
   - Evidence validation rules
   - Scoring weights
   - Remediation playbooks
3. Click "Save Changes"
4. Changes take effect on next assessment

**Warning:** Customizing controls may affect compliance scoring. Document all changes.

## Evidence Collection

Evidence is automatically collected from integrated sources.

### Evidence Sources

#### Microsoft Defender for Endpoint
- Installed applications
- Application control policies
- Patch status
- Vulnerability assessments
- Security configuration

#### Microsoft Intune
- Device compliance status
- Configuration profiles
- Application deployment status
- Update status

#### Azure Active Directory
- MFA status
- Privileged accounts
- Conditional access policies
- Sign-in logs

#### Windows Agents
- Local security policies
- Event logs
- Installed software
- Service status
- Backup verification

### Viewing Evidence

1. Navigate to **Evidence** page
2. Filter by:
   - Source (Defender, Intune, AAD, etc.)
   - Asset
   - Control
   - Date range
   - Validation status

3. Click evidence item to view:
   - Raw data (JSON)
   - Extracted findings
   - Validation status
   - Used in assessments
   - Chain of custody

### Manual Evidence Upload

**For sources not yet integrated:**

1. Navigate to **Evidence** > **Upload**
2. Select asset
3. Select control
4. Upload file (CSV, JSON, XML, or TXT)
5. Add notes/context
6. Click "Submit for Review"

**SecOps Review:**
1. Navigate to **Evidence** > **Pending Review**
2. Review uploaded evidence
3. Validate authenticity
4. Approve or Reject with reason

### Evidence Retention

- **Active Evidence:** 90 days (used in current assessments)
- **Historical Evidence:** 7 years (audit compliance)
- **Rejected Evidence:** 30 days then deleted

## Assessment Execution

### Automatic Assessments

Assessments run automatically:
- **Continuous:** Every 6 hours (default)
- **Weekly Summary:** Sunday 2 AM
- **Monthly Report:** First of month

### Manual Assessment

**When to use:**
- After bulk remediation
- Before audit
- After major system changes
- On-demand compliance check

**Steps:**
1. Navigate to **Assessments** > **Run Assessment**
2. Select scope:
   - All assets (full assessment)
   - Asset group (department, location)
   - Specific pillar
   - Specific assets
3. Click "Start Assessment"
4. Monitor progress (real-time)
5. View results when complete (typically 5-15 minutes)

### Understanding Assessment Results

**Overall Score:** 0-100%
- Calculated from weighted maturity levels
- Target: ≥66% (Level 2 across all pillars)
- Industry benchmark shown for comparison

**Maturity Level per Pillar:**
- Level 0: No controls (0%)
- Level 1: Basic controls (33%)
- Level 2: Good controls (66%)
- Level 3: Excellent controls (100%)

**Detailed Breakdown:**
- Requirements met/total by pillar
- Assets compliant/total
- Evidence coverage percentage
- Confidence score (based on evidence quality)

**Change Detection:**
- Improvements since last assessment
- Degradations (drift)
- New risks identified
- Resolved issues

### Comparing Assessments

1. Navigate to **Assessments** > **History**
2. Select two assessments
3. Click "Compare"
4. View side-by-side comparison:
   - Score changes
   - Maturity level changes
   - Asset status changes
   - New/resolved issues

## Drift Detection

Drift occurs when an asset's compliance status degrades.

### Viewing Drift Events

1. Navigate to **Drift Events**
2. View active drifts:
   - Asset name
   - Pillar affected
   - Previous maturity → Current maturity
   - Detection time
   - Root cause (if identified)
   - Status (Open, In Remediation, Resolved)

### Drift Details

Click drift event to see:

**What Changed:**
- Specific control that failed
- Evidence showing non-compliance
- Configuration comparison (before/after)

**Impact:**
- Maturity level change
- Overall score impact
- Risk assessment
- Affected users/systems

**Root Cause Analysis:**
- Automated detection of likely cause
- Recent changes on the asset
- User actions
- Policy changes

**Remediation:**
- Recommended actions
- Available playbooks
- Estimated time to resolve
- Priority level

### Drift Notifications

Configure notifications:
1. Profile > Notification Settings
2. Enable drift alerts
3. Select notification method:
   - Email
   - SMS
   - Teams/Slack webhook
   - SIEM integration
4. Set severity threshold (notify for Critical/High only)

### Drift Analytics

**Drift Trends Dashboard:**
- Drift events over time
- Most affected pillars
- Most affected assets
- Common root causes
- Average resolution time

**Use this to:**
- Identify systemic issues
- Improve controls
- Reduce recurring drift
- Optimize remediation

## Remediation

### Remediation Task Queue

Navigate to **Remediation** to view all tasks:

**Filters:**
- Priority (Critical, High, Medium, Low)
- Status (Open, In Progress, Completed, Failed)
- Pillar
- Assigned to
- Due date

**Sort by:**
- Priority (default)
- Impact (maturity improvement)
- Effort (time to complete)
- Due date

### Task Details

Click task to view:

**Summary:**
- Task name
- Description
- Pillar and control
- Priority and SLA
- Assigned to
- Created date
- Due date

**Impact Analysis:**
- Number of assets affected
- Current maturity level
- Target maturity level after remediation
- Overall score improvement

**Remediation Steps:**
1. Manual steps (if no automation)
2. Automated playbook (if available)
3. Verification steps
4. Rollback procedure (if needed)

**Affected Assets:**
- List of assets requiring remediation
- Current status of each
- Last evidence collected

### Executing Remediation

#### Automated Remediation (Recommended)

1. Open remediation task
2. Click "Execute Playbook"
3. Review pre-execution checks:
   - Asset compatibility
   - Dependencies
   - Backup verification
   - Change window
4. Select target assets (default: all affected)
5. Schedule:
   - Execute now
   - Schedule for specific time
   - Execute during maintenance window
6. Click "Start Execution"

**Monitor Progress:**
- Real-time status per asset
- Success/failure indicators
- Logs available for each asset
- Pause/stop execution if needed

#### Manual Remediation

1. Open remediation task
2. Click "Manual Remediation"
3. Follow documented steps
4. Complete checklist
5. Upload verification evidence
6. Click "Mark as Complete"

**SecOps Review:**
- Task marked "Pending Verification"
- SecOps reviews evidence
- Approves or requests rework
- Next assessment will validate

### Remediation Playbooks

**Available Playbooks:**
- Enable application whitelisting (Windows)
- Deploy critical patches (Windows/Linux)
- Configure Office macro settings (M365)
- Harden web browsers (Chrome/Edge/Firefox)
- Restrict administrative privileges (Windows/Linux)
- Deploy OS patches (Windows/Linux)
- Enable MFA (Azure AD)
- Verify backup status (Windows/Linux)

**Custom Playbooks:**
Admins can create custom Ansible playbooks:
1. Navigate to **Administration** > **Playbooks**
2. Click "New Playbook"
3. Upload Ansible YAML
4. Configure variables
5. Test on non-production asset
6. Activate for production use

### Remediation Reporting

**Task Completion Report:**
- Tasks completed this period
- Average time to remediation
- Success rate
- Recurring issues
- Top contributors

**Export options:** PDF, CSV, JSON

## Reporting

### Pre-Built Reports

#### Executive Summary

**Purpose:** High-level compliance overview for leadership

**Contents:**
- Overall compliance score
- Maturity by pillar (chart)
- Key achievements
- Top risks
- Remediation progress
- Trend analysis (30 days)

**Frequency:** Weekly, Monthly, Quarterly

**Format:** PDF (presentation-ready)

#### Technical Compliance Report

**Purpose:** Detailed assessment for SecOps and auditors

**Contents:**
- Full assessment results
- Control-by-control analysis
- Evidence summary
- Non-compliant assets
- Remediation status
- Detailed findings

**Frequency:** Monthly, On-demand

**Format:** PDF, Excel

#### Audit Evidence Report

**Purpose:** Compliance evidence for internal/external audits

**Contents:**
- Assessment methodology
- Evidence collection summary
- Chain of custody
- Maturity determination
- Control testing results
- Appendix: Raw evidence (optional)

**Frequency:** Quarterly, Annual, On-demand

**Format:** PDF with evidence archive (ZIP)

#### Drift Analysis Report

**Purpose:** Track compliance degradation over time

**Contents:**
- Drift events by pillar
- Root cause analysis
- Resolution time metrics
- Recurring drift patterns
- Recommendations

**Frequency:** Monthly

**Format:** PDF, Excel

### Generating Reports

1. Navigate to **Reports**
2. Select report type
3. Configure parameters:
   - Date range
   - Scope (all assets, specific groups)
   - Detail level (summary, detailed, comprehensive)
   - Include evidence (yes/no)
4. Click "Generate Report"
5. Wait for completion (15-60 seconds)
6. Download or email

### Scheduled Reports

**Configure automatic report delivery:**

1. Navigate to **Reports** > **Schedules**
2. Click "New Schedule"
3. Configure:
   - Report type
   - Frequency (daily, weekly, monthly, quarterly)
   - Day/time
   - Recipients (email addresses)
   - Format (PDF, Excel, CSV)
4. Click "Save Schedule"

**Example:**
- **Report:** Executive Summary
- **Frequency:** Weekly
- **Day:** Monday
- **Time:** 9:00 AM
- **Recipients:** ciso@example.com, board@example.com
- **Format:** PDF

### Custom Reports

**SQL Query Builder (Admin/SecOps):**

1. Navigate to **Reports** > **Custom**
2. Click "New Custom Report"
3. Build query using visual builder:
   - Select tables (assessments, evidence, controls, assets)
   - Choose columns
   - Add filters
   - Configure grouping
   - Add calculations
4. Preview results
5. Save report template
6. Generate or schedule

**Warning:** Advanced feature. Incorrect queries may impact performance.

## Administration

**Admin Role Only**

### User Management

#### Adding Users

1. Navigate to **Administration** > **Users**
2. Click "Add User"
3. Enter details:
   - Email (username)
   - First name
   - Last name
   - Role (Admin, SecOps, Auditor, Executive)
   - Department
   - Phone (for MFA)
4. Click "Send Invitation"

User receives email with:
- Invitation link (expires in 48 hours)
- Instructions to set password
- MFA setup guide

#### Modifying Users

1. Navigate to **Administration** > **Users**
2. Click user to edit
3. Modify:
   - Role
   - Department
   - Active/Inactive status
   - Password reset (force on next login)
   - MFA reset
4. Click "Save Changes"

#### Deleting Users

1. Navigate to **Administration** > **Users**
2. Click user to delete
3. Click "Deactivate" (recommended) or "Delete"
   - Deactivate: User cannot login, data retained
   - Delete: User and associated data removed (irreversible)
4. Confirm action

### System Configuration

#### Integration Settings

**Microsoft Defender:**
1. Navigate to **Administration** > **Integrations** > **Defender**
2. Click "Configure"
3. Enter:
   - Tenant ID
   - Client ID
   - Client Secret
4. Test connection
5. Configure collection schedule (default: 6 hours)
6. Save

**Similar process for:**
- Microsoft Intune
- Azure Active Directory
- Microsoft 365
- Custom APIs

#### Assessment Settings

1. Navigate to **Administration** > **Settings** > **Assessments**
2. Configure:
   - Auto-assessment frequency (1, 3, 6, 12, 24 hours)
   - Evidence validity window (24, 48, 72 hours)
   - Scoring weights (default: equal weight per pillar)
   - Confidence thresholds
3. Save changes

#### Notification Settings

1. Navigate to **Administration** > **Settings** > **Notifications**
2. Configure:
   - Email server (SMTP)
   - SMS gateway (Twilio, etc.)
   - Webhook URLs (Teams, Slack, SIEM)
   - Notification templates
3. Test notifications
4. Save

### Audit Logs

**Immutable audit trail of all system activity:**

1. Navigate to **Administration** > **Audit Logs**
2. Filter by:
   - Date range
   - User
   - Action type (login, assessment, remediation, config change)
   - Result (success, failure)
3. View log details:
   - Timestamp
   - User
   - IP address
   - Action
   - Before/after values (for changes)
   - Result

**Export audit logs:**
- Format: CSV, JSON, SIEM format
- Retention: 7 years (compliance requirement)

### Backup and Recovery

#### Database Backups

- **Automatic:** Daily at 2 AM (Azure Backup)
- **Retention:** 90 days point-in-time recovery
- **Geo-Redundant:** Replicated to Australia Southeast

#### Manual Backup

1. Navigate to **Administration** > **Backup**
2. Click "Create Backup Now"
3. Enter backup name/description
4. Click "Start Backup"
5. Download backup file (optional)

#### Recovery

**Contact system administrator or support for recovery procedures.**

## Getting Help

### In-App Help

Click **?** icon (top right) for:
- Context-sensitive help
- Video tutorials
- Knowledge base
- Contact support

### Support

**Email:** support@eemcars.com
**Phone:** 1800-EEMCARS (Australia)
**Portal:** https://support.eemcars.com

**Response Times:**
- Critical (P1): 2 hours
- High (P2): 8 hours
- Medium (P3): 1 business day
- Low (P4): 2 business days

### Training

**Available training:**
- On-demand video tutorials (https://training.eemcars.com)
- Live webinars (monthly)
- On-site training (contact sales)
- Certification program (SecOps role)

## Keyboard Shortcuts

- `Ctrl/Cmd + K`: Quick search
- `Ctrl/Cmd + D`: Open dashboard
- `Ctrl/Cmd + R`: Refresh current view
- `Ctrl/Cmd + E`: View evidence
- `Ctrl/Cmd + A`: Run assessment
- `Ctrl/Cmd + /`: Show keyboard shortcuts
- `Esc`: Close modal/dialog

## Best Practices

### For SecOps

1. **Review drift events daily** - Prevent compliance degradation
2. **Prioritize critical remediation tasks** - Fix high-impact issues first
3. **Validate evidence regularly** - Ensure data quality
4. **Monitor integration health** - Check all sources are collecting
5. **Document custom changes** - Maintain audit trail

### For Admins

1. **Regular user access reviews** - Remove inactive users
2. **Monitor system performance** - Check dashboard load times
3. **Keep integrations updated** - Update credentials before expiry
4. **Test backups quarterly** - Verify recovery procedures
5. **Review audit logs** - Detect anomalous activity

### For Executives

1. **Review weekly summary** - Stay informed on compliance posture
2. **Track long-term trends** - Identify improvement trajectory
3. **Set realistic targets** - Balance security and operational needs
4. **Allocate remediation resources** - Fund compliance improvements
5. **Communicate progress** - Share achievements with stakeholders

## Appendix

### Essential Eight Pillars Reference

1. **Application Control:** Whitelist approved applications
2. **Patch Applications:** Keep applications up to date
3. **Configure Microsoft Office Macro Settings:** Disable or restrict macros
4. **User Application Hardening:** Configure browsers and Office securely
5. **Restrict Administrative Privileges:** Limit admin access
6. **Patch Operating Systems:** Keep OS up to date
7. **Multi-Factor Authentication:** Require MFA for all users
8. **Regular Backups:** Backup data and test recovery

### Maturity Levels

- **Level 0:** No implementation
- **Level 1:** Partial implementation (basic security)
- **Level 2:** Good implementation (target for most organizations)
- **Level 3:** Excellent implementation (advanced security)

### Glossary

- **Assessment:** Evaluation of Essential Eight compliance
- **Control:** Specific security requirement
- **Drift:** Degradation in compliance status
- **Evidence:** Data proving compliance or non-compliance
- **Maturity Level:** Degree of implementation (0-3)
- **Pillar:** One of the eight Essential Eight security domains
- **Remediation:** Actions to fix non-compliance
- **Playbook:** Automated remediation script (Ansible)
