# EEMCARS Screenshots Guide

This document describes the key screens and visual elements of the EEMCARS platform. Screenshots should be captured from a production-like environment with demo data loaded.

## 1. Login Screen

**File:** `screenshots/01-login.png`

**Description:**
Clean, professional login screen with:
- EEMCARS logo (top center)
- "Essential Eight Maturity Assessment Platform" tagline
- Email and password fields
- "Remember me" checkbox
- "Forgot password?" link
- "Sign In" button (primary blue)
- Australian government compliance badges (bottom)
- Background: Subtle gradient with security-themed imagery

**Capture notes:**
- Use demo credentials: admin@example.com
- Show empty form (no filled data)
- Ensure HTTPS lock icon visible in browser
- Include full browser chrome for authenticity

## 2. Main Dashboard

**File:** `screenshots/02-dashboard-overview.png`

**Description:**
Executive dashboard showing complete Essential Eight maturity status:

**Top Section (Metrics Cards):**
- Total Assets: 500
- Compliant Assets: 275 (55%)
- Active Drift Events: 23 (red indicator)
- Open Remediation Tasks: 47

**Middle Section (Heatmap):**
- 8x4 grid showing all Essential Eight pillars and maturity levels
- Color-coded cells:
  - Application Control: L2 (green)
  - Patch Applications: L1 (yellow/orange)
  - Office Macros: L2 (green)
  - User App Hardening: L1 (orange)
  - Restrict Admin: L2 (green)
  - Patch OS: L1 (orange)
  - Multi-Factor Auth: L2 (green)
  - Regular Backups: L2 (green)

**Bottom Section:**
- Line chart showing 30-day maturity trends
- All 8 pillars visible as colored lines
- Y-axis: 0-3 (maturity levels)
- X-axis: Last 30 days
- Show gradual improvement trend

**Capture notes:**
- User logged in as admin@example.com (show in top-right)
- Date/time stamp visible
- All data loading complete (no spinners)
- Sidebar navigation visible on left

## 3. Essential Eight Maturity Heatmap (Close-up)

**File:** `screenshots/03-maturity-heatmap.png`

**Description:**
Zoomed view of the maturity heatmap with hover tooltip:

**Tooltip shown on "Application Control - Level 2":**
- Title: "Application Control - Maturity Level 2"
- Assets Compliant: 201/300 (67%)
- Requirements: 4 of 6 met
- Last Assessment: 2 hours ago
- Status: On track
- "Click for details" hint

**Color Legend:**
- Green (✓): Requirement met
- Yellow (◐): Partially met (in progress)
- Orange (⚠): Not met (action required)
- Red (✗): Critical non-compliance
- Gray: Not applicable

**Capture notes:**
- Cursor hovering over cell (visible)
- Tooltip positioned clearly
- Other cells slightly dimmed (focus effect)
- Legend visible at bottom

## 4. Controls List

**File:** `screenshots/04-controls-list.png`

**Description:**
Comprehensive list of all Essential Eight controls:

**Filter Bar (Top):**
- Pillar dropdown: "Application Control" selected
- Maturity Level: "All" (showing 0-3)
- Compliance Status: "All"
- Search box: Empty

**Table Columns:**
1. Control ID (e.g., E8-AC-L1-REQ1)
2. Description (truncated with "...")
3. Maturity Level (badge: L0, L1, L2, L3)
4. Compliance (progress bar: 67% green, 33% red)
5. Assets (201/300)
6. Last Assessed (2 hours ago)
7. Actions (View, Edit icons)

**Visible Rows (5-7):**
- Mix of L1, L2, L3 controls
- Various compliance percentages
- Color-coded status indicators

**Capture notes:**
- Show 10-15 rows
- Scroll position near top
- Pagination: "Page 1 of 8" visible
- Sort indicator on "Compliance" column (descending)

## 5. Control Detail View

**File:** `screenshots/05-control-detail.png`

**Description:**
Detailed view of single control "E8-AC-L2-REQ1":

**Header:**
- Control ID: E8-AC-L2-REQ1 (large)
- Pillar: Application Control (badge)
- Maturity Level: 2 (badge)
- Overall Status: 67% Compliant (progress bar)

**Tabs:**
1. **Requirements** (active)
2. Evidence
3. Assets
4. Remediation

**Requirements Tab Content:**
- **Description:** "Application whitelisting implemented across all workstations and servers using Microsoft AppLocker or equivalent..."
- **Technical Requirements:**
  - ☑ AppLocker enabled
  - ☑ Approved application list maintained
  - ☐ Enforcement mode active (67% complete)
  - ☑ Event logging configured
  - ☐ Regular rule reviews (pending)
- **ACSC Reference:** Essential Eight Maturity Model (link)
- **Risk if not met:** "High - Increased malware execution risk"

**Right Sidebar:**
- Compliance Status: 201/300 assets (pie chart)
- Last Assessment: 2 hours ago
- Next Assessment: In 4 hours
- Evidence Sources: Defender ATP, Intune (icons)

**Capture notes:**
- Full page visible including header and sidebar
- Checkmarks/crosses clearly visible
- Links underlined
- Professional typography

## 6. Evidence List

**File:** `screenshots/06-evidence-list.png`

**Description:**
Evidence collection dashboard:

**Summary Cards (Top):**
- Total Evidence Items: 12,458
- Validated: 12,203 (98%)
- Pending Review: 45
- Rejected: 210

**Filter Bar:**
- Source: "All" (dropdown: Defender ATP, Intune, Azure AD, Agents)
- Date Range: "Last 7 days"
- Status: "All" (Validated, Pending, Rejected)
- Control: "All"

**Table:**
1. Evidence ID (EVD-2024-00123)
2. Source (icon + text: "Defender ATP")
3. Asset (DESKTOP-SALES-042)
4. Control (E8-AC-L2-REQ1)
5. Collected (2 hours ago)
6. Status (badge: "Validated" green, "Pending" yellow, "Rejected" red)
7. Actions (View, Download)

**Visible Rows:** Mix of sources, recent timestamps, mostly validated

**Capture notes:**
- Show 15-20 rows
- Icons for each source clearly visible
- Timestamps in human-readable format ("2 hours ago" not "2024-01-15 14:32:11")
- Filter selections highlighted

## 7. Evidence Detail

**File:** `screenshots/07-evidence-detail.png`

**Description:**
Detailed evidence viewer showing specific evidence item:

**Header:**
- Evidence ID: EVD-2024-00123
- Status: Validated ✓ (green badge)
- Source: Microsoft Defender ATP (icon + text)
- Collected: 2024-01-15 14:32 AEST
- Asset: DESKTOP-SALES-042

**Tabs:**
1. **Summary** (active)
2. Raw Data
3. Audit Trail

**Summary Tab:**
- **Control:** E8-AC-L2-REQ1 - Application whitelisting
- **Finding:** AppLocker enabled in enforcement mode
- **Key Data Points:**
  - Policy Status: Enabled ✓
  - Enforcement Mode: Active ✓
  - Rules Configured: 47
  - Last Updated: 2024-01-10
  - Event Logging: Enabled ✓
- **Validation:**
  - Authenticity: Verified (digital signature valid)
  - Timestamp: Verified (within valid window)
  - Schema: Valid (matches expected format)
  - Used in Assessment: Yes (Assessment-2024-00789)

**Right Sidebar:**
- **Chain of Custody:**
  1. Collected from asset (2024-01-15 14:30)
  2. Transmitted to EEMCARS (2024-01-15 14:31)
  3. Validated (2024-01-15 14:32)
  4. Used in assessment (2024-01-15 16:00)
- **Download Options:**
  - Raw JSON
  - Formatted report
  - Include in evidence package

**Capture notes:**
- Clean JSON syntax highlighting in raw data tab (if shown)
- Checkmarks and validation indicators clear
- Timeline visualization for chain of custody
- Professional data presentation

## 8. Drift Events

**File:** `screenshots/08-drift-events.png`

**Description:**
Drift detection dashboard showing compliance degradation:

**Alert Banner (Top):**
- Red warning banner: "23 active drift events require attention"
- "View All" button

**Summary Section:**
- Line chart showing drift events over 30 days
- Current spike visible (23 events)
- Average trend line showing typical drift rate

**Active Drift Events Table:**
1. Event ID (DRF-2024-00045)
2. Asset (DESKTOP-SALES-042)
3. Pillar (Application Control)
4. Change (Level 2 → Level 1, with red down arrow ↓)
5. Detected (15 minutes ago)
6. Root Cause (Auto-detected: "AppLocker disabled by user")
7. Status (badge: "Open" red, "In Remediation" yellow, "Resolved" green)
8. Actions (View, Remediate)

**Visible Rows:**
- 5-7 recent drift events
- Mix of pillars
- Different timeframes
- Some with auto-detected root causes

**Right Sidebar:**
- **Drift Statistics:**
  - Most Affected Pillar: Patch Applications (8 events)
  - Most Affected Asset Type: Windows 10 Workstations
  - Average Resolution Time: 18 hours
  - Recurring Drift: 6 assets (repeated offenders)

**Capture notes:**
- Red down arrows clearly visible
- Recent timestamps (minutes/hours ago)
- Root cause text readable
- Sidebar statistics prominent

## 9. Drift Event Detail

**File:** `screenshots/09-drift-detail.png`

**Description:**
Detailed view of single drift event:

**Header:**
- Event ID: DRF-2024-00045
- Status: Open (red badge)
- Severity: High (orange badge)
- Detected: 15 minutes ago

**What Changed:**
- **Before:** Maturity Level 2 (green badge)
- **After:** Maturity Level 1 (yellow badge)
- **Impact:** Overall compliance score decreased 2% (67% → 65%)

**Affected Control:**
- E8-AC-L2-REQ1: Application whitelisting
- **Failure Reason:** AppLocker enforcement mode disabled

**Evidence Comparison:**
- Side-by-side comparison:
  - **Previous (2024-01-15 12:00):**
    ```json
    "enforcementMode": "Enabled"
    ```
  - **Current (2024-01-15 16:15):**
    ```json
    "enforcementMode": "Disabled"
    ```

**Root Cause Analysis:**
- **Auto-detected:** User action (local admin account used)
- **Timeline:**
  1. 16:10 - Local admin logon (user: john.smith)
  2. 16:12 - Group Policy refresh
  3. 16:14 - AppLocker enforcement disabled
  4. 16:15 - Drift detected
- **Confidence:** High (95%)

**Recommended Remediation:**
- **Action:** Re-enable AppLocker enforcement mode
- **Playbook:** Available ✓ (applock-reenableenforcement.yml)
- **Estimated Time:** 5 minutes
- **Impact:** 1 asset
- **Priority:** High

**Actions:**
- [Create Remediation Task] button (primary)
- [Ignore] button (secondary)
- [Export Details] button

**Capture notes:**
- Side-by-side evidence comparison clearly visible
- Timeline visualization with timestamps
- Playbook available indicator prominent
- Action buttons at bottom

## 10. Remediation Tasks Queue

**File:** `screenshots/10-remediation-queue.png`

**Description:**
Remediation task management dashboard:

**Summary Cards:**
- Open Tasks: 47
- In Progress: 12
- Completed (30d): 328
- Success Rate: 89%

**Filter/Sort Bar:**
- Priority: "All" (Critical: 8, High: 15, Medium: 24, Low: 0)
- Status: "Open" selected
- Pillar: "All"
- Assigned To: "All"
- Sort: "Priority (High to Low)"

**Task Queue Table:**
1. Task ID (REM-2024-00234)
2. Title ("Enable AppLocker whitelisting on 23 endpoints")
3. Pillar (Application Control)
4. Priority (badge: Critical red, High orange, Medium yellow)
5. Impact ("+23 assets to L2" with up arrow ↑)
6. Effort (2 hours)
7. Assigned To (Auto / John Smith)
8. Due Date (2024-01-16)
9. Status (Open, In Progress, Completed)
10. Actions (Execute, View, Assign)

**Visible Rows:**
- Mix of priorities (show critical tasks first)
- Various pillars
- Some assigned, some unassigned
- Impact indicators with up arrows

**Capture notes:**
- Priority badges color-coded
- Critical tasks at top (red badges)
- Impact numbers with green up arrows
- Execute buttons prominent on automated tasks
- Timeline indicators for due dates

## 11. Remediation Task Detail

**File:** `screenshots/11-remediation-detail.png`

**Description:**
Detailed remediation task with playbook:

**Header:**
- Task ID: REM-2024-00234
- Status: Open (yellow badge)
- Priority: High (orange badge)
- Created: 1 hour ago
- Due: Tomorrow 5 PM (23 hours remaining)

**Task Summary:**
- **Title:** Enable AppLocker whitelisting on 23 endpoints
- **Pillar:** Application Control
- **Control:** E8-AC-L2-REQ1
- **Root Cause:** Drift events on 23 assets
- **Assigned To:** Unassigned (dropdown to assign)

**Impact Analysis:**
- **Assets Affected:** 23 (view list)
- **Current Maturity:** Level 1 (201/300 compliant)
- **After Remediation:** Level 2 (224/300 compliant)
- **Score Improvement:** +2.5% (65.0% → 67.5%)
- **Risk Reduction:** High → Medium

**Remediation Playbook:**
- **Name:** applockerEnable-enforcement.yml
- **Type:** Ansible Playbook
- **Automation:** Fully automated ✓
- **Estimated Time:** 5 minutes per asset (total: 2 hours)
- **Prerequisites:**
  - Assets online ✓
  - WinRM enabled ✓
  - Ansible connectivity ✓
- **Steps:**
  1. Connect to remote system via WinRM
  2. Verify AppLocker service status
  3. Enable enforcement mode in local security policy
  4. Refresh group policy
  5. Verify enforcement active
  6. Collect evidence
  7. Update compliance status

**Affected Assets List** (expandable table):
- DESKTOP-SALES-042
- DESKTOP-SALES-043
- LAPTOP-EXEC-015
- ... (20 more)

**Actions:**
- [Execute Playbook Now] button (large, primary green)
- [Schedule Execution] button (secondary)
- [Manual Remediation] button (tertiary)
- [Export Task Details] link

**Capture notes:**
- Playbook steps numbered and clear
- Prerequisites with checkmarks
- Impact numbers prominent (green up arrows)
- Asset list scrollable/expandable
- Execute button prominent and inviting

## 12. Playbook Execution Screen

**File:** `screenshots/12-playbook-execution.png`

**Description:**
Real-time playbook execution monitoring:

**Header:**
- Task: REM-2024-00234
- Playbook: applock-reenableenforcement.yml
- Status: In Progress (animated spinner)
- Started: Just now
- Estimated Completion: 2 hours

**Progress Overview:**
- Progress bar: 22% complete
- **Completed:** 5/23 assets (green)
- **In Progress:** 3/23 assets (blue, animated)
- **Queued:** 15/23 assets (gray)
- **Failed:** 0/23 assets (red)

**Asset Execution Status Table:**
1. Asset Name
2. Status (icon + text: Completed ✓, In Progress ⟳, Queued ⋯, Failed ✗)
3. Current Step ("Step 3: Enabling enforcement mode")
4. Progress (progress bar per asset)
5. Duration (2m 34s)
6. Actions (View Logs)

**Visible Rows:**
- DESKTOP-SALES-042: Completed ✓ (3m 12s)
- DESKTOP-SALES-043: Completed ✓ (2m 58s)
- LAPTOP-EXEC-015: In Progress ⟳ "Step 5: Refreshing group policy" (1m 45s)
- DESKTOP-FIN-089: In Progress ⟳ "Step 2: Verifying service status" (0m 32s)
- DESKTOP-SALES-044: Queued ⋯
- ... (15+ more)

**Live Log Feed** (bottom section):
```
[16:45:12] DESKTOP-SALES-042: Connected successfully
[16:45:15] DESKTOP-SALES-042: AppLocker service is running
[16:45:18] DESKTOP-SALES-042: Enforcement mode enabled successfully
[16:45:21] DESKTOP-SALES-042: Group policy refreshed
[16:45:24] DESKTOP-SALES-042: Enforcement verified active
[16:45:25] DESKTOP-SALES-042: ✓ Completed successfully
[16:45:26] LAPTOP-EXEC-015: Connected successfully
...
```

**Actions:**
- [Pause Execution] button
- [Stop Execution] button (with warning)
- [Download Logs] link

**Capture notes:**
- Animated elements (spinner, in-progress bars) visible
- Logs scrolling (show recent entries)
- Color coding (green success, blue in-progress)
- Timestamps in logs
- Professional monospace font for logs

## 13. Reports Dashboard

**File:** `screenshots/13-reports.png`

**Description:**
Report generation and scheduling center:

**Quick Reports** (top section with cards):
1. **Executive Summary**
   - Last generated: 2 days ago
   - Next scheduled: Monday 9 AM
   - [Generate Now] button

2. **Technical Compliance**
   - Last generated: 1 week ago
   - [Generate Now] button

3. **Audit Evidence Package**
   - Last generated: 1 month ago
   - Size: 245 MB
   - [Generate Now] button

4. **Drift Analysis**
   - Last generated: Yesterday
   - [Generate Now] button

**Recent Reports Table:**
1. Report Name
2. Type
3. Generated (timestamp)
4. Generated By (user)
5. Date Range
6. Format (PDF, Excel, CSV)
7. Size
8. Actions (Download, Email, Delete)

**Visible Rows:**
- Executive Summary - Monthly (2024-01-01 to 2024-01-31) - PDF - 2.4 MB
- Technical Compliance Report - Weekly - PDF - 15.3 MB
- Audit Evidence Package - Q4 2023 - ZIP - 245 MB
- Custom Query: Non-compliant Assets - CSV - 124 KB

**Scheduled Reports Section:**
- **Weekly Executive Summary**
  - Every Monday, 9:00 AM
  - Recipients: ciso@example.com, board@example.com
  - Format: PDF
  - [Edit] [Disable]

- **Monthly Technical Report**
  - First of month, 8:00 AM
  - Recipients: secops@example.com
  - Format: PDF + Excel
  - [Edit] [Disable]

**Actions:**
- [Create Custom Report] button (primary)
- [Schedule New Report] button

**Capture notes:**
- Report cards with icons
- File sizes visible
- Recent timestamps
- Download buttons prominent
- Schedule information clear

## 14. Executive Report Preview

**File:** `screenshots/14-report-preview.png`

**Description:**
PDF preview of executive summary report:

**Report Header:**
- Logo and title: "Essential Eight Maturity Assessment"
- Organization: Melbourne Health Services
- Report Period: January 1-31, 2024
- Generated: February 1, 2024
- Classification: PROTECTED

**Page 1 - Executive Summary:**

**Overall Compliance Score:** 67% (large, centered)
- Target: 66% (Level 2)
- Status: On Track ✓
- vs. Previous Month: +5% improvement

**Essential Eight Maturity Scorecard:**
| Pillar | Current | Target | Status |
|--------|---------|--------|---------|
| Application Control | L2 | L2 | ✓ On Track |
| Patch Applications | L1 | L2 | ⚠ Action Required |
| Office Macros | L2 | L2 | ✓ On Track |
| User App Hardening | L1 | L2 | ⚠ Action Required |
| Restrict Admin | L2 | L2 | ✓ On Track |
| Patch OS | L1 | L2 | ⚠ Action Required |
| MFA | L2 | L2 | ✓ On Track |
| Backups | L2 | L2 | ✓ On Track |

**Key Achievements This Month:**
- Improved overall score by 5% (62% → 67%)
- Achieved Level 2 for MFA across all users (100% adoption)
- Resolved 43 high-priority remediation tasks
- Zero critical drift events

**Top Risks:**
1. **Patch Applications - 155 endpoints missing critical patches**
   - Risk: High vulnerability to known exploits
   - Recommendation: Execute mass patching playbook
   - ETA to L2: 2 weeks

2. **User Application Hardening - Browser security settings inconsistent**
   - Risk: Increased phishing/malware risk
   - Recommendation: Deploy hardened browser policies
   - ETA to L2: 1 week

**30-Day Trend Chart:**
- Line graph showing maturity improvement
- All pillars trending up or stable
- Clear visual of progress

**Capture notes:**
- Professional report layout
- Charts and tables clearly formatted
- Color-coded status indicators
- Suitable for board presentation
- Headers/footers with page numbers

## 15. Assessment History

**File:** `screenshots/15-assessment-history.png`

**Description:**
Historical assessment tracking and comparison:

**Timeline View** (default):
- Visual timeline showing assessments over 90 days
- Points on timeline for each assessment
- Color-coded by overall score:
  - Green (>66%): Level 2 achieved
  - Yellow (50-66%): Approaching target
  - Red (<50%): Below target

**Assessment List:**
1. Assessment ID (ASM-2024-00789)
2. Date/Time (2024-01-15 16:00 AEST)
3. Overall Score (67%, green badge)
4. Change (vs previous: +2%, green up arrow ↑)
5. Maturity Levels (compact: 2,1,2,1,2,1,2,2)
6. Duration (12 minutes)
7. Status (Completed ✓)
8. Actions (View, Compare, Export)

**Visible Rows:** Last 10 assessments over 30 days

**Comparison Tool** (right sidebar):
- Select Assessment A: ASM-2024-00789 (latest)
- Select Assessment B: ASM-2024-00650 (1 week ago)
- [Compare] button

**Statistics:**
- Total Assessments: 1,247
- Average Score: 64%
- Best Score: 67% (current)
- Improvement Rate: +1.5% per week

**Capture notes:**
- Timeline visualization prominent
- Score trends visible
- Recent assessments at top
- Comparison tool accessible
- Green/yellow/red color scheme consistent

## 16. Assessment Comparison

**File:** `screenshots/16-assessment-comparison.png`

**Description:**
Side-by-side comparison of two assessments:

**Header:**
- **Assessment A:** ASM-2024-00789 (2024-01-15 16:00)
- **Assessment B:** ASM-2024-00650 (2024-01-08 14:30)
- Time between: 7 days

**Overall Score Comparison:**
| Metric | Assessment A | Assessment B | Change |
|--------|--------------|--------------|--------|
| Overall Score | 67% | 65% | +2% ↑ |
| Compliant Assets | 275/500 | 265/500 | +10 ↑ |
| Maturity Level Avg | 1.67 | 1.63 | +0.04 ↑ |

**Pillar-by-Pillar Comparison:**
| Pillar | Assessment A | Assessment B | Change |
|--------|--------------|--------------|--------|
| Application Control | L2 (67%) | L2 (67%) | → |
| Patch Applications | L1 (45%) | L1 (43%) | +2% ↑ |
| Office Macros | L2 (80%) | L2 (80%) | → |
| User App Hardening | L1 (55%) | L1 (52%) | +3% ↑ |
| Restrict Admin | L2 (70%) | L2 (70%) | → |
| Patch OS | L1 (50%) | L1 (48%) | +2% ↑ |
| MFA | L2 (85%) | L2 (82%) | +3% ↑ |
| Backups | L2 (75%) | L2 (75%) | → |

**Changes Detected:**
- **Improved:** 4 pillars (Patch Apps, User Hardening, Patch OS, MFA)
- **Degraded:** 0 pillars
- **Unchanged:** 4 pillars

**Asset Status Changes:**
- **Improved to Compliant:** 15 assets (list)
- **Degraded to Non-Compliant:** 5 assets (drift events)
- **Net Change:** +10 compliant assets

**Capture notes:**
- Side-by-side layout
- Change arrows (up/down/neutral)
- Color coding (green improvements, red degradations)
- Detailed breakdown tables
- Export button visible

## 17. Asset Inventory

**File:** `screenshots/17-asset-inventory.png`

**Description:**
Complete asset inventory with compliance status:

**Summary Cards:**
- Total Assets: 500
- Workstations: 350
- Servers: 100
- Cloud Resources: 50
- Compliant: 275 (55%)

**Filter Bar:**
- Type: "All" (Workstation, Server, Cloud)
- OS: "All" (Windows 10, Windows 11, Windows Server, Linux)
- Department: "All" (Sales, Finance, IT, HR, Exec)
- Location: "All" (Melbourne, Sydney, Brisbane)
- Compliance: "All" (Compliant, Non-Compliant, Unknown)

**Asset Table:**
1. Asset Name (DESKTOP-SALES-042)
2. Type (icon + text: Workstation, Server, Cloud)
3. OS (Windows 10 Pro 22H2)
4. Department (Sales)
5. Location (Melbourne)
6. Compliance Score (67%, progress bar)
7. Maturity Level (2,1,2,1,2,1,2,2 - compact badges)
8. Last Assessed (2 hours ago)
9. Status (Compliant ✓, Non-Compliant ⚠, Unknown ?)
10. Actions (View, Assess)

**Visible Rows:** Mix of asset types, departments, compliance statuses

**Bulk Actions:**
- Checkbox column (select multiple)
- [Run Assessment] button (for selected)
- [Export Selected] button

**Capture notes:**
- Asset type icons visible
- Progress bars showing compliance percentage
- Color-coded status
- Sortable columns (show sort indicator)
- Bulk selection checkboxes

## 18. Asset Detail View

**File:** `screenshots/18-asset-detail.png`

**Description:**
Comprehensive asset profile and compliance details:

**Header:**
- Asset Name: DESKTOP-SALES-042 (large)
- Type: Workstation (icon + text)
- Status: Compliant ✓ (67%, green badge)
- Last Assessed: 2 hours ago

**Tabs:**
1. **Overview** (active)
2. Compliance
3. Evidence
4. History

**Overview Tab:**

**System Information:**
- OS: Windows 10 Pro 22H2 (Build 19045.3803)
- Manufacturer: Dell Inc.
- Model: OptiPlex 7090
- CPU: Intel Core i7-11700 @ 2.50GHz
- RAM: 16 GB
- Disk: 512 GB SSD
- IP Address: 10.0.1.142
- MAC Address: 00:1A:2B:3C:4D:5E
- Domain: MELHEALTH.LOCAL
- OU: Sales/Workstations

**User Information:**
- Primary User: John Smith (john.smith@example.com)
- Department: Sales
- Location: Melbourne - Level 12
- Last Login: 2024-01-15 08:32 AEST

**Agent Status:**
- EEMCARS Agent: Installed ✓ (v1.2.3)
- Last Heartbeat: 5 minutes ago
- Collection Status: Active ✓
- Next Collection: In 3 hours

**Compliance Summary:**
- Overall Score: 67%
- Essential Eight Maturity:
  - Application Control: L2 ✓
  - Patch Applications: L1 ⚠
  - Office Macros: L2 ✓
  - User App Hardening: L1 ⚠
  - Restrict Admin: L2 ✓
  - Patch OS: L1 ⚠
  - MFA: L2 ✓
  - Backups: L2 ✓

**Actions:**
- [Run Assessment Now]
- [View Full Compliance Report]
- [Edit Asset Details]
- [Decommission]

**Capture notes:**
- Clean information layout
- Checkmarks for active/compliant items
- System specs detailed
- User information visible
- Agent status prominent

## 19. User Management (Admin)

**File:** `screenshots/19-user-management.png`

**Description:**
User administration panel:

**Summary Cards:**
- Total Users: 24
- Active Users: 22
- Inactive: 2
- Last 30 days logins: 18

**Filter Bar:**
- Role: "All" (Admin, SecOps, Auditor, Executive)
- Status: "Active"
- Department: "All"
- Search: Empty

**User Table:**
1. Name (John Smith)
2. Email (john.smith@example.com)
3. Role (badge: Admin blue, SecOps green, Auditor yellow, Executive purple)
4. Department (IT Operations)
5. Last Login (2 hours ago)
6. MFA Status (Enabled ✓ / Disabled ⚠)
7. Status (Active ✓ / Inactive ⚠)
8. Actions (Edit, Deactivate, Reset Password)

**Visible Rows:** 8-10 users with mix of roles

**Actions:**
- [Add New User] button (primary, top-right)
- [Bulk Import] button
- [Export User List] link

**User Activity Graph:**
- Bar chart showing logins per day (last 30 days)
- Peak activity Monday-Friday
- Lower weekend activity

**Capture notes:**
- Role badges color-coded
- MFA status clearly indicated
- Last login in human-readable format
- Activity graph showing patterns
- Add user button prominent

## 20. System Settings (Admin)

**File:** `screenshots/20-system-settings.png`

**Description:**
System configuration panel:

**Navigation (Left Sidebar):**
- General Settings
- Integrations (active)
- Assessment Configuration
- Notifications
- Security
- Backup & Recovery
- Audit Logs

**Integrations Panel** (active):

**Microsoft Defender for Endpoint:**
- Status: Connected ✓ (green indicator)
- Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- Last Sync: 10 minutes ago
- Collection Schedule: Every 6 hours
- Next Collection: In 5 hours 50 minutes
- Collected Items (24h): 1,247
- [Test Connection] button
- [Reconfigure] button

**Microsoft Intune:**
- Status: Connected ✓
- Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- Last Sync: 15 minutes ago
- Collection Schedule: Every 6 hours
- Next Collection: In 5 hours 45 minutes
- Collected Items (24h): 892
- [Test Connection] button
- [Reconfigure] button

**Azure Active Directory:**
- Status: Connected ✓
- Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- Last Sync: 5 minutes ago
- Collection Schedule: Every 12 hours
- Next Collection: In 11 hours 55 minutes
- Collected Items (24h): 456
- [Test Connection] button
- [Reconfigure] button

**Windows Agents:**
- Status: 450/500 online (90%)
- Agent Version: v1.2.3
- Last Update Check: 1 hour ago
- Update Available: No
- [View Agent Status] link
- [Deploy to New Endpoints] button

**Custom API Integration:**
- Status: Not Configured
- [Configure New Integration] button

**Actions:**
- [Add Integration] button (top-right)
- [Test All Connections] button

**Capture notes:**
- Green indicators for connected services
- Sync times recently updated
- Collection schedules visible
- Item counts showing activity
- Configuration buttons accessible

## General Screenshot Guidelines

### Resolution and Format
- **Resolution:** 1920x1080 (Full HD) minimum
- **Format:** PNG (lossless)
- **Color Space:** sRGB
- **DPI:** 72-96 (web standard)

### Browser
- **Recommended:** Chrome or Edge (latest)
- **Show Browser Chrome:** Yes (URL bar, tabs visible)
- **Zoom Level:** 100% (default)
- **Extensions:** Hide extension icons
- **URL:** Show full URL with HTTPS

### Data
- **Use Demo Data:** Always use seeded demo data
- **Realistic Values:** No placeholder text like "Lorem ipsum"
- **Dates:** Recent/current dates (not 2020, not far future)
- **Australian Context:** AU timezone (AEST/AEDT), AU date format
- **No Sensitive Info:** No real company names, emails, IPs (except demo)

### Composition
- **Full Page:** Include headers, navigation, footers
- **No Cut-offs:** Ensure all content visible (no truncated text)
- **Scrolled Position:** Top of page unless showing specific lower content
- **Modals:** If present, ensure background visible (shows context)
- **Hover States:** Capture where it adds value (tooltips, dropdown menus)

### Annotations
- **Version 1:** Clean screenshots (no annotations)
- **Version 2:** Annotated versions with:
  - Numbered callouts
  - Arrows highlighting key features
  - Text explanations
  - Use for marketing/tutorials

### File Naming
```
screenshots/
  01-login.png
  02-dashboard-overview.png
  03-maturity-heatmap.png
  ...
  annotated/
    02-dashboard-overview-annotated.png
    05-control-detail-annotated.png
```

## Marketing Screenshots

For marketing materials, capture additional views:

- **Hero Image:** Dashboard full screen, impressive maturity heatmap
- **Before/After:** Comparison showing improvement over time
- **Mobile View:** Responsive dashboard on tablet/mobile
- **Dark Mode:** If implemented, show dark theme screenshots
- **Integration:** Show integration configuration screens
- **API:** Swagger/OpenAPI documentation page
- **Automation:** Playbook execution in action

## Video Screenshots

For creating demo videos, capture keyframes:
- Every major transition
- Every button click (before/after)
- Loading states
- Success confirmations
- Error states (if demonstrating error handling)

Use these as storyboard for video production.
