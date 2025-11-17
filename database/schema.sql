-- Essential Eight Maturity Continuous Assessment & Remediation System
-- PostgreSQL Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Users and RBAC
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Admin', 'SecOps', 'Auditor', 'ExecViewer')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE
);

-- Assets/Endpoints
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    hostname VARCHAR(255) NOT NULL,
    ip_address INET,
    asset_type VARCHAR(50) NOT NULL CHECK (asset_type IN ('Windows', 'Linux', 'MacOS', 'Network', 'Cloud', 'Application')),
    operating_system VARCHAR(100),
    os_version VARCHAR(50),
    department VARCHAR(100),
    criticality VARCHAR(20) CHECK (criticality IN ('Critical', 'High', 'Medium', 'Low')),
    is_active BOOLEAN DEFAULT true,
    last_seen TIMESTAMP WITH TIME ZONE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Essential Eight Controls
CREATE TABLE controls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    control_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    pillar VARCHAR(100) NOT NULL CHECK (pillar IN (
        'Application Control',
        'Patch Applications',
        'Configure Microsoft Office Macro Settings',
        'User Application Hardening',
        'Restrict Administrative Privileges',
        'Patch Operating Systems',
        'Multi-Factor Authentication',
        'Regular Backups'
    )),
    acsc_reference VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Maturity Requirements
CREATE TABLE maturity_requirements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    control_id UUID REFERENCES controls(id) ON DELETE CASCADE,
    maturity_level INTEGER NOT NULL CHECK (maturity_level IN (0, 1, 2, 3)),
    requirement_text TEXT NOT NULL,
    validation_criteria JSONB,
    remediation_guidance TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Evidence Items
CREATE TABLE evidence (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    control_id UUID REFERENCES controls(id) ON DELETE CASCADE,
    evidence_type VARCHAR(100) NOT NULL,
    evidence_data JSONB NOT NULL,
    evidence_hash VARCHAR(64) NOT NULL,
    collected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    collection_method VARCHAR(50) CHECK (collection_method IN ('Agent', 'API', 'Manual', 'Integration')),
    is_valid BOOLEAN DEFAULT true,
    validation_errors JSONB,
    metadata JSONB
);

-- Assessment Runs
CREATE TABLE assessment_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_type VARCHAR(50) NOT NULL CHECK (run_type IN ('Full', 'Incremental', 'OnDemand', 'Scheduled')),
    status VARCHAR(50) NOT NULL CHECK (status IN ('Running', 'Completed', 'Failed', 'Cancelled')),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    triggered_by UUID REFERENCES users(id),
    total_assets INTEGER,
    total_controls INTEGER,
    overall_maturity_score NUMERIC(3,2),
    results JSONB,
    error_log TEXT
);

-- Assessment Results
CREATE TABLE assessment_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessment_run_id UUID REFERENCES assessment_runs(id) ON DELETE CASCADE,
    control_id UUID REFERENCES controls(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    maturity_level INTEGER CHECK (maturity_level BETWEEN 0 AND 3),
    score NUMERIC(5,2),
    passed_checks INTEGER,
    total_checks INTEGER,
    evidence_count INTEGER,
    findings JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Drift Events
CREATE TABLE drift_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    control_id UUID REFERENCES controls(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    previous_maturity_level INTEGER,
    current_maturity_level INTEGER,
    severity VARCHAR(20) CHECK (severity IN ('Critical', 'High', 'Medium', 'Low', 'Info')),
    drift_type VARCHAR(50) CHECK (drift_type IN ('Regression', 'Improvement', 'Configuration', 'Evidence')),
    description TEXT,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    acknowledged BOOLEAN DEFAULT false,
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    resolution_notes TEXT
);

-- Remediation Tasks
CREATE TABLE remediation_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    control_id UUID REFERENCES controls(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES assets(id),
    task_type VARCHAR(50) CHECK (task_type IN ('Ansible', 'PowerShell', 'Bash', 'Manual', 'API')),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) CHECK (priority IN ('Critical', 'High', 'Medium', 'Low')),
    status VARCHAR(50) DEFAULT 'Open' CHECK (status IN ('Open', 'InProgress', 'Completed', 'Failed', 'Cancelled')),
    playbook_path VARCHAR(500),
    script_content TEXT,
    assigned_to UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    execution_log TEXT,
    execution_result JSONB
);

-- Agent Registrations
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(100) UNIQUE NOT NULL,
    asset_id UUID REFERENCES assets(id) ON DELETE CASCADE,
    agent_version VARCHAR(50),
    platform VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Error')),
    last_heartbeat TIMESTAMP WITH TIME ZONE,
    capabilities JSONB,
    registered_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    configuration JSONB
);

-- Audit Logs (Immutable)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    ip_address INET,
    user_agent TEXT,
    request_data JSONB,
    response_status INTEGER,
    changes JSONB,
    severity VARCHAR(20) DEFAULT 'Info'
);

-- Create immutable audit log trigger
CREATE OR REPLACE FUNCTION prevent_audit_log_modification()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'Audit logs are immutable';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_logs_immutable
BEFORE UPDATE OR DELETE ON audit_logs
FOR EACH ROW EXECUTE FUNCTION prevent_audit_log_modification();

-- Reports
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_type VARCHAR(50) CHECK (report_type IN ('Executive', 'Detailed', 'Compliance', 'Trend')),
    format VARCHAR(20) CHECK (format IN ('PDF', 'CSV', 'JSON', 'HTML')),
    generated_by UUID REFERENCES users(id),
    assessment_run_id UUID REFERENCES assessment_runs(id),
    parameters JSONB,
    file_path VARCHAR(500),
    file_hash VARCHAR(64),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Compliance Checklists
CREATE TABLE compliance_checklists (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    target_maturity_level INTEGER CHECK (target_maturity_level BETWEEN 1 AND 3),
    checklist_items JSONB NOT NULL,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Scheduled Assessments
CREATE TABLE scheduled_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    schedule_expression VARCHAR(100) NOT NULL, -- Cron expression
    assessment_type VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    last_run TIMESTAMP WITH TIME ZONE,
    next_run TIMESTAMP WITH TIME ZONE,
    configuration JSONB,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_assets_hostname ON assets(hostname);
CREATE INDEX idx_assets_type ON assets(asset_type);
CREATE INDEX idx_assets_active ON assets(is_active);

CREATE INDEX idx_evidence_asset ON evidence(asset_id);
CREATE INDEX idx_evidence_control ON evidence(control_id);
CREATE INDEX idx_evidence_collected ON evidence(collected_at);

CREATE INDEX idx_assessment_results_run ON assessment_results(assessment_run_id);
CREATE INDEX idx_assessment_results_control ON assessment_results(control_id);
CREATE INDEX idx_assessment_results_timestamp ON assessment_results(timestamp);

CREATE INDEX idx_drift_detected ON drift_events(detected_at);
CREATE INDEX idx_drift_severity ON drift_events(severity);
CREATE INDEX idx_drift_acknowledged ON drift_events(acknowledged);

CREATE INDEX idx_remediation_status ON remediation_tasks(status);
CREATE INDEX idx_remediation_priority ON remediation_tasks(priority);
CREATE INDEX idx_remediation_assigned ON remediation_tasks(assigned_to);

CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_action ON audit_logs(action);

CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_heartbeat ON agents(last_heartbeat);

-- Insert Essential Eight Controls
INSERT INTO controls (control_id, name, description, pillar, acsc_reference) VALUES
('E8-AC', 'Application Control', 'Prevent execution of unapproved/malicious programs including .exe, DLL, scripts, installers, compiled HTML, HTML applications and control panel applets.', 'Application Control', 'ACSC-E8-AC'),
('E8-PA', 'Patch Applications', 'Update applications with the latest security patches to prevent exploitation of vulnerabilities.', 'Patch Applications', 'ACSC-E8-PA'),
('E8-MS', 'Configure Microsoft Office Macro Settings', 'Configure Microsoft Office macro settings to block macros from the Internet, and only allow vetted macros either in trusted locations with limited write access or digitally signed with a trusted certificate.', 'Configure Microsoft Office Macro Settings', 'ACSC-E8-MS'),
('E8-UAH', 'User Application Hardening', 'Configure web browsers and PDF viewers to block or disable support for web advertisements, Java, and Flash content.', 'User Application Hardening', 'ACSC-E8-UAH'),
('E8-RAP', 'Restrict Administrative Privileges', 'Restrict administrative privileges to operating systems and applications based on user duties and validate administrator activities.', 'Restrict Administrative Privileges', 'ACSC-E8-RAP'),
('E8-POS', 'Patch Operating Systems', 'Update operating systems with the latest security patches to prevent exploitation of vulnerabilities.', 'Patch Operating Systems', 'ACSC-E8-POS'),
('E8-MFA', 'Multi-Factor Authentication', 'Implement multi-factor authentication including for VPNs, RDP, SSH and other remote access, and for all users when they perform a privileged action or access important data repositories.', 'Multi-Factor Authentication', 'ACSC-E8-MFA'),
('E8-RB', 'Regular Backups', 'Ensure backups of important data, software and configuration settings are performed and retained in accordance with business continuity requirements.', 'Regular Backups', 'ACSC-E8-RB');

-- Insert Maturity Requirements for Application Control
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-AC'), 1,
'Application control implemented on workstations to restrict execution of executables, software libraries, scripts, and installers to an approved set.',
'{"checks": ["whitelisting_enabled", "execution_policies_configured", "logging_enabled"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-AC'), 2,
'Application control implemented on workstations and servers (including domain controllers, file servers and web servers) to restrict execution to an approved set.',
'{"checks": ["servers_protected", "validated_rules", "bypass_prevention", "event_monitoring"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-AC'), 3,
'Application control implemented using cryptographic hash rules, publisher certificate rules, or path rules. Microsoft's recommended block rules are implemented.',
'{"checks": ["cryptographic_validation", "microsoft_blocklist", "publisher_rules", "automated_updates"]}'::jsonb);

-- Insert Maturity Requirements for Patch Applications
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-PA'), 1,
'Patches, updates or vendor mitigations for security vulnerabilities in internet-facing applications are applied within two weeks of release.',
'{"checks": ["internet_facing_patched", "patch_timeframe_2weeks", "vulnerability_tracking"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-PA'), 2,
'Patches, updates or mitigations for security vulnerabilities in internet-facing and non-internet-facing applications are applied within two weeks.',
'{"checks": ["all_apps_patched", "patch_timeframe_2weeks", "automated_patching", "exception_process"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-PA'), 3,
'Patches, updates or mitigations for critical and high severity vulnerabilities in internet-facing applications are applied within 48 hours. All other applications within two weeks.',
'{"checks": ["critical_48hours", "high_48hours", "automated_deployment", "testing_process"]}'::jsonb);

-- Insert Maturity Requirements for Microsoft Office Macros
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-MS'), 1,
'Microsoft Office macros are disabled for users that do not have a legitimate business requirement.',
'{"checks": ["macros_disabled_default", "user_awareness", "policy_enforced"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-MS'), 2,
'Microsoft Office macros in files from the Internet are blocked. Macros are only allowed to run from Trusted Locations with limited write access.',
'{"checks": ["internet_macros_blocked", "trusted_locations", "write_restrictions", "gpo_configured"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-MS'), 3,
'Microsoft Office macros in files from the Internet are blocked. Only digitally signed macros are allowed with a trusted certificate or from Trusted Locations.',
'{"checks": ["digital_signatures_required", "certificate_validation", "trusted_locations", "vba_protection"]}'::jsonb);

-- Insert Maturity Requirements for User Application Hardening
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-UAH'), 1,
'Web browsers are configured to block Flash content, ads and Java. PDF software is configured to block Flash and JavaScript.',
'{"checks": ["flash_blocked", "ads_blocked", "java_disabled", "pdf_javascript_disabled"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-UAH'), 2,
'Web browsers are configured to block or disable support for Flash, ads, and Java. PDF software is configured to block Flash and disable JavaScript.',
'{"checks": ["browser_hardening_gpo", "extension_control", "pdf_hardening", "user_override_blocked"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-UAH'), 3,
'Web browsers are hardened with centrally managed settings. PDF viewers are sandboxed and hardened. Object Linking and Embedding features are disabled.',
'{"checks": ["centralized_browser_management", "pdf_sandboxing", "ole_disabled", "additional_protections"]}'::jsonb);

-- Insert Maturity Requirements for Restrict Administrative Privileges
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-RAP'), 1,
'Privileged access to systems and applications is restricted and controlled.',
'{"checks": ["admin_accounts_identified", "separation_duties", "privileged_access_controlled"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-RAP'), 2,
'Privileged accounts are prevented from accessing the internet, email and web services. Just-in-time administration is used.',
'{"checks": ["internet_restricted", "email_restricted", "jit_admin", "paw_implemented"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-RAP'), 3,
'Privileged accounts use separate, dedicated workstations or privileged access workstations. Admin activities are logged and protected.',
'{"checks": ["dedicated_paw", "admin_logging", "session_recording", "behavior_monitoring"]}'::jsonb);

-- Insert Maturity Requirements for Patch Operating Systems
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-POS'), 1,
'Patches, updates or mitigations for security vulnerabilities in operating systems are applied within one month of release.',
'{"checks": ["os_patched_monthly", "vulnerability_scanning", "patch_compliance"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-POS'), 2,
'Patches, updates or mitigations for security vulnerabilities in operating systems are applied within two weeks of release.',
'{"checks": ["os_patched_2weeks", "automated_patching", "compliance_reporting", "exception_process"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-POS'), 3,
'Patches or mitigations for critical and high vulnerabilities are applied within 48 hours. All other OS patches within two weeks. Latest version of OS used.',
'{"checks": ["critical_48hours", "os_version_current", "automated_deployment", "rollback_capability"]}'::jsonb);

-- Insert Maturity Requirements for Multi-Factor Authentication
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-MFA'), 1,
'Multi-factor authentication is used to authenticate users to their organization's online services that process, store or communicate their organization's sensitive data.',
'{"checks": ["mfa_online_services", "user_enrollment", "mfa_enforced"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-MFA'), 2,
'Multi-factor authentication is used by all users when accessing important data repositories. MFA is used for all remote access to the organization's network.',
'{"checks": ["mfa_data_repos", "mfa_remote_access", "vpn_mfa", "rdp_mfa"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-MFA'), 3,
'Multi-factor authentication is used to authenticate all privileged actions and access to important data repositories. Phishing-resistant MFA is used.',
'{"checks": ["mfa_privileged_actions", "phishing_resistant", "hardware_tokens", "conditional_access"]}'::jsonb);

-- Insert Maturity Requirements for Regular Backups
INSERT INTO maturity_requirements (control_id, maturity_level, requirement_text, validation_criteria) VALUES
((SELECT id FROM controls WHERE control_id = 'E8-RB'), 1,
'Backups of important data, software and configuration settings are performed and retained in a secure and resilient manner.',
'{"checks": ["backup_schedule", "backup_retention", "backup_security", "restore_tested"]}'::jsonb),
((SELECT id FROM controls WHERE control_id = 'E8-RB'), 2,
'Backups are stored offline or online with multi-factor authentication and encrypted. Restoration is tested as part of disaster recovery exercises.',
'{"checks": ["offline_backups", "backup_encryption", "mfa_backup_access", "dr_testing"]}'::jsonb),
((SELECT id FROM controls WHERE control_id =='E8-RB'), 3,
'Backups are stored offline, online with immutability, or air-gapped. Full restoration is tested quarterly. Event logs for backup deletion are monitored.',
'{"checks": ["immutable_backups", "quarterly_restore_test", "backup_monitoring", "ransomware_protection"]}'::jsonb);

-- Create view for current maturity status
CREATE VIEW current_maturity_status AS
SELECT
    c.id as control_id,
    c.control_id as control_code,
    c.name as control_name,
    c.pillar,
    COALESCE(MAX(ar.maturity_level), 0) as current_maturity_level,
    COALESCE(AVG(ar.score), 0) as average_score,
    COUNT(DISTINCT ar.asset_id) as assessed_assets,
    MAX(ar.timestamp) as last_assessed
FROM controls c
LEFT JOIN assessment_results ar ON c.id = ar.control_id
GROUP BY c.id, c.control_id, c.name, c.pillar;

-- Create view for drift summary
CREATE VIEW drift_summary AS
SELECT
    de.control_id,
    c.name as control_name,
    de.severity,
    COUNT(*) as drift_count,
    MAX(de.detected_at) as latest_drift
FROM drift_events de
JOIN controls c ON de.control_id = c.id
WHERE NOT de.acknowledged
GROUP BY de.control_id, c.name, de.severity;

-- Create function for updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON assets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_controls_updated_at BEFORE UPDATE ON controls
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create demo user (password: DemoUser123!)
-- Password hash for 'DemoUser123!' using bcrypt
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@eemcars.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqKqFn9W7i', 'Admin'),
('secops', 'secops@eemcars.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqKqFn9W7i', 'SecOps'),
('auditor', 'auditor@eemcars.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqKqFn9W7i', 'Auditor'),
('executive', 'exec@eemcars.local', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqKqFn9W7i', 'ExecViewer');

-- Comments for documentation
COMMENT ON TABLE controls IS 'Essential Eight control definitions';
COMMENT ON TABLE maturity_requirements IS 'Maturity level requirements for each control (0-3)';
COMMENT ON TABLE evidence IS 'Evidence collected from assets for control validation';
COMMENT ON TABLE assessment_runs IS 'Assessment execution tracking';
COMMENT ON TABLE assessment_results IS 'Detailed results for each control/asset combination';
COMMENT ON TABLE drift_events IS 'Tracking maturity level changes and regressions';
COMMENT ON TABLE remediation_tasks IS 'Automated and manual remediation tasks';
COMMENT ON TABLE audit_logs IS 'Immutable audit trail for compliance';
