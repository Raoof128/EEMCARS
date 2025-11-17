# EEMCARS Demo Materials

This directory contains all materials needed for conducting effective demonstrations of the EEMCARS platform.

## Directory Structure

```
docs/
├── DEMO_GUIDE.md           # Comprehensive demo script and scenarios
├── USER_GUIDE.md           # End-user documentation
├── FEATURES.md             # Complete feature catalog
├── SCREENSHOTS.md          # Screenshot capture guidelines
└── demos/
    ├── README.md           # This file
    ├── scenarios/          # Demo scenarios and scripts
    ├── data/               # Sample demo data
    └── presentations/      # PowerPoint/PDF presentations
```

## Quick Start

### Running a Demo

1. **Environment Setup (5 minutes):**
   ```bash
   # Start all services
   ./quickstart.sh

   # Load demo data
   docker-compose exec backend python -m app.demo.seed_data

   # Verify health
   make health-check
   ```

2. **Access the Application:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - Demo Credentials: See [DEMO_GUIDE.md](../DEMO_GUIDE.md#pre-demo-setup-5-minutes)

3. **Follow the Demo Script:**
   - Executive Demo (5 min): [DEMO_GUIDE.md](../DEMO_GUIDE.md#demo-flow-15-20-minutes) Part 1
   - Standard Demo (20 min): Full flow
   - Technical Deep Dive (45 min): Include advanced features

## Available Demos

### 1. Executive Briefing (5 minutes)
**Audience:** CISO, CIO, Board Members, Executive Management

**Focus:**
- Dashboard overview
- Compliance score
- Executive reports

**Script:** [DEMO_GUIDE.md](../DEMO_GUIDE.md#part-1-executive-overview-3-minutes)

**Outcome:** Executive understanding of compliance posture and business value

### 2. Standard Product Demo (20 minutes)
**Audience:** Security Analysts, IT Managers, Compliance Officers

**Focus:**
- Complete Essential Eight workflow
- Assessment execution
- Drift detection
- Automated remediation

**Script:** [DEMO_GUIDE.md](../DEMO_GUIDE.md#demo-flow-15-20-minutes)

**Outcome:** Understanding of operational capabilities and automation

### 3. Technical Deep Dive (45 minutes)
**Audience:** Security Engineers, System Administrators, DevOps

**Focus:**
- Architecture and integrations
- API capabilities
- Agent deployment
- Custom playbooks
- Advanced configuration

**Script:** [DEMO_GUIDE.md](../DEMO_GUIDE.md#advanced-features-demo-optional---5-minutes)

**Outcome:** Technical confidence in implementation and customization

### 4. Auditor Walkthrough (30 minutes)
**Audience:** Internal/External Auditors, Compliance Teams

**Focus:**
- Evidence collection and validation
- Chain of custody
- Audit reports
- Immutable audit logs
- Export capabilities

**Script:** Create based on audit requirements

**Outcome:** Confidence in audit evidence quality and accessibility

## Demo Scenarios

### Healthcare Scenario
**Organization:** Melbourne Health Services
**Size:** 500 endpoints
**Current State:** Mixed maturity (L0-L2)
**Goal:** Achieve Level 2 across all pillars

**Key Story Points:**
- Recent ransomware near-miss
- Board mandate for improved security
- Limited IT security staff
- Need for automation

**Demo Data:** Pre-loaded in demo seed

### Finance Scenario
**Organization:** Sydney Financial Services
**Size:** 1,000 endpoints
**Current State:** Level 2 achieved, maintaining
**Goal:** Demonstrate continuous compliance

**Key Story Points:**
- APRA compliance requirements
- Quarterly audit reporting
- Zero drift tolerance
- Need for executive reporting

**Demo Data:** Available on request

### Government Scenario
**Organization:** Australian Government Agency (PROTECTED)
**Size:** 2,500 endpoints
**Current State:** Transitioning from manual to automated
**Goal:** ISM compliance, Level 3 target

**Key Story Points:**
- ISM Essential Eight mandate
- Data sovereignty requirements
- Multiple departments
- Audit trail requirements

**Demo Data:** Available on request

## Demo Best Practices

### Before the Demo

**1. Technical Preparation:**
- [ ] Test environment running (24 hours before)
- [ ] Demo data loaded and verified
- [ ] Browser cache cleared
- [ ] Backup instance ready
- [ ] Internet connection verified (if cloud demo)

**2. Content Preparation:**
- [ ] Understand audience (role, pain points, priorities)
- [ ] Select appropriate scenario
- [ ] Customize demo script
- [ ] Prepare answers to likely questions
- [ ] Test demo flow (dry run)

**3. Materials Preparation:**
- [ ] Presentation slides ready
- [ ] Handouts printed (architecture diagram, feature list)
- [ ] Business cards
- [ ] Laptop/projector tested
- [ ] Backup plan (pre-recorded video, screenshots)

### During the Demo

**1. Engagement:**
- Start with pain points (current challenges)
- Use their terminology and use cases
- Encourage questions throughout
- Show, don't tell (click through the app)
- Focus on value, not features

**2. Pacing:**
- Watch the clock (stick to allocated time)
- Pause for questions at logical breaks
- Skip features if running over
- Always end with Q&A time

**3. Handling Issues:**
- If demo breaks: pivot to slides/screenshots
- If question stumps you: "Great question, let me get back to you"
- If audience disengaged: ask questions, solicit input
- If internet fails: use local Docker instance

### After the Demo

**1. Follow-Up:**
- Send thank-you email within 24 hours
- Include demo recording/screenshots
- Attach relevant documentation
- Schedule next steps
- Add contacts to CRM

**2. Materials to Send:**
- Executive summary PDF
- Architecture diagram
- Integration guide
- Pricing proposal (if requested)
- Trial access (if appropriate)

**3. Internal Debrief:**
- Document questions asked
- Note objections/concerns
- Identify missing features
- Update demo script based on feedback

## Troubleshooting

### Common Issues

**Issue: Services not starting**
```bash
# Solution:
docker-compose down -v
docker-compose up -d
make health-check
```

**Issue: Demo data not loading**
```bash
# Solution:
docker-compose exec backend python -m app.demo.seed_data --force
```

**Issue: Frontend not connecting to backend**
```bash
# Check backend is running:
curl http://localhost:8000/health

# Restart frontend:
docker-compose restart frontend
```

**Issue: Slow performance**
```bash
# Allocate more resources to Docker
# Docker Desktop: Settings > Resources
# Recommended: 4 CPU, 8GB RAM

# Or restart:
docker-compose restart
```

**Issue: Authentication failing**
```bash
# Reset demo user passwords:
docker-compose exec backend python -m app.demo.reset_passwords
```

### Pre-Demo Checklist

**T-24 Hours:**
- [ ] Test environment fully functional
- [ ] Demo data loaded correctly
- [ ] All integrations showing "Connected"
- [ ] Recent assessment run (shows fresh data)
- [ ] Drift events present (for demo impact)
- [ ] Remediation tasks queued
- [ ] Reports generated successfully

**T-1 Hour:**
- [ ] Environment still running
- [ ] Browser tested (Chrome/Edge recommended)
- [ ] Projector/screen sharing working
- [ ] Demo credentials ready
- [ ] Backup plan ready
- [ ] Water/coffee available
- [ ] Phone on silent

**T-5 Minutes:**
- [ ] Environment responsive
- [ ] Dashboard loaded
- [ ] Logout (ready for login demo)
- [ ] Close unnecessary tabs
- [ ] Browser at 100% zoom
- [ ] Full screen ready

## Demo Resources

### Presentations

**Executive Overview (10 slides):**
- Problem statement
- Solution overview
- Key features (with screenshots)
- ROI calculator
- Customer success stories
- Pricing overview
- Next steps

**Technical Deep Dive (30 slides):**
- Architecture diagram
- Integration points
- API capabilities
- Security & compliance
- Deployment options
- Roadmap
- Q&A

### Handouts

**One-Pagers:**
- EEMCARS overview
- Essential Eight reference
- Integration list
- ROI calculator
- Contact information

**Technical:**
- Architecture diagram (A4)
- API endpoint list
- Agent requirements
- Deployment checklist

### Videos

**Recordings:**
- 2-minute product overview
- 5-minute feature highlights
- 15-minute full demo
- 5-minute customer testimonial

**Use Cases:**
- Pre-meeting teaser (send before demo)
- Backup (if live demo fails)
- Post-meeting reinforcement
- Training for internal team

## Feedback

### Collecting Feedback

After each demo, ask:
1. What features were most valuable to you?
2. What features are missing that you need?
3. How does this compare to your current process?
4. What concerns do you have?
5. What are the next steps?

### Improving the Demo

Track metrics:
- Demo-to-trial conversion rate
- Demo-to-sale conversion rate
- Average time to close (post-demo)
- Most requested features
- Common objections

Update demo materials based on:
- Frequent questions → Add to FAQ
- Common objections → Address proactively in demo
- Missing features → Add to roadmap slide
- Confusing areas → Simplify or clarify

## Contact

**Demo Support:**
- Email: demos@eemcars.com
- Slack: #demo-support
- Phone: 1800-EEMCARS

**Demo Requests:**
- Internal: Submit ticket in Jira (DEMO project)
- External: Schedule via Calendly (calendly.com/eemcars)

**Demo Environment Issues:**
- DevOps team: devops@eemcars.com
- Escalation: CTO (cto@eemcars.com)

## Contributing

To improve demo materials:
1. Create branch: `demo/your-improvement`
2. Make changes to demo scripts, scenarios, or data
3. Test thoroughly
4. Create PR with description of improvements
5. Tag @demo-team for review

Suggested improvements:
- New demo scenarios
- Updated screenshots
- Additional use cases
- FAQ answers
- Troubleshooting tips
