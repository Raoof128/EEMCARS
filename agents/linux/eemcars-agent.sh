#!/bin/bash
# EEMCARS Linux Agent
# Essential Eight Evidence Collection Agent for Linux

set -e

# Configuration
SERVER_URL="${EEMCARS_SERVER_URL:-http://localhost:8000}"
AGENT_VERSION="1.0.0"
HEARTBEAT_INTERVAL="${EEMCARS_HEARTBEAT_INTERVAL:-300}"  # 5 minutes

# Generate Agent ID
AGENT_ID="LNX-$(hostname)-$(date +%Y%m%d%H%M%S)"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Function to register agent
register_agent() {
    log_info "Registering agent: $AGENT_ID"

    local hostname=$(hostname)
    local ip_address=$(hostname -I | awk '{print $1}')
    local os_name=$(lsb_release -d | cut -f2- || cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)
    local os_version=$(uname -r)

    local payload=$(cat <<EOF
{
    "agent_id": "$AGENT_ID",
    "asset_id": "$(uuidgen)",
    "agent_version": "$AGENT_VERSION",
    "platform": "Linux",
    "capabilities": {
        "os": "$os_name",
        "os_version": "$os_version",
        "hostname": "$hostname",
        "ip_address": "$ip_address"
    }
}
EOF
)

    local response=$(curl -s -X POST "$SERVER_URL/api/v1/agents/register" \
        -H "Content-Type: application/json" \
        -d "$payload")

    if [ $? -eq 0 ]; then
        log_info "Agent registered successfully"
        return 0
    else
        log_error "Failed to register agent"
        return 1
    fi
}

# Function to send heartbeat
send_heartbeat() {
    local payload=$(cat <<EOF
{
    "agent_id": "$AGENT_ID",
    "status": "Active"
}
EOF
)

    curl -s -X POST "$SERVER_URL/api/v1/agents/heartbeat" \
        -H "Content-Type: application/json" \
        -d "$payload" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        log_info "Heartbeat sent at $(date)"
    else
        log_warn "Heartbeat failed"
    fi
}

# Function to collect patch evidence
collect_patch_evidence() {
    log_info "Collecting patch evidence..."

    local missing_patches=0
    local last_update_date=""
    local os_patch_age_days=999

    # Detect package manager
    if command -v apt-get &> /dev/null; then
        # Debian/Ubuntu
        apt-get update > /dev/null 2>&1
        missing_patches=$(apt list --upgradable 2>/dev/null | grep -c "upgradable" || echo "0")
        last_update_date=$(stat -c %y /var/lib/apt/periodic/update-success-stamp 2>/dev/null | cut -d' ' -f1 || echo "unknown")
    elif command -v yum &> /dev/null; then
        # RedHat/CentOS
        missing_patches=$(yum check-update 2>/dev/null | grep -c "^[a-z]" || echo "0")
        last_update_date=$(rpm -qa --last | head -1 | awk '{print $3,$4,$5}')
    fi

    # Calculate patch age
    if [ "$last_update_date" != "unknown" ] && [ -n "$last_update_date" ]; then
        last_update_timestamp=$(date -d "$last_update_date" +%s 2>/dev/null || echo "0")
        current_timestamp=$(date +%s)
        os_patch_age_days=$(( ($current_timestamp - $last_update_timestamp) / 86400 ))
    fi

    local evidence=$(cat <<EOF
{
    "asset_id": "$(uuidgen)",
    "control_id": "$(uuidgen)",
    "evidence_type": "PatchStatus",
    "evidence_data": {
        "os_patch_age_days": $os_patch_age_days,
        "missing_patches_count": $missing_patches,
        "last_update_date": "$last_update_date",
        "os_version_supported": true
    },
    "collection_method": "Agent"
}
EOF
)

    submit_evidence "$evidence"
}

# Function to collect user application hardening evidence
collect_application_hardening_evidence() {
    log_info "Collecting application hardening evidence..."

    local flash_blocked=false
    local java_disabled=false

    # Check if Flash is installed/blocked
    if ! command -v flash-player-plugin &> /dev/null; then
        flash_blocked=true
    fi

    # Check if Java browser plugin is disabled
    if ! find /usr/lib -name "libnpjp2.so" 2>/dev/null | grep -q .; then
        java_disabled=true
    fi

    local evidence=$(cat <<EOF
{
    "asset_id": "$(uuidgen)",
    "control_id": "$(uuidgen)",
    "evidence_type": "ApplicationHardening",
    "evidence_data": {
        "flash_blocked": $flash_blocked,
        "java_disabled": $java_disabled
    },
    "collection_method": "Agent"
}
EOF
)

    submit_evidence "$evidence"
}

# Function to collect admin privileges evidence
collect_admin_privileges_evidence() {
    log_info "Collecting admin privileges evidence..."

    local admin_accounts_count=$(grep -E "sudo|wheel" /etc/group | wc -l)
    local root_login_disabled=false

    # Check if root SSH login is disabled
    if grep -q "^PermitRootLogin no" /etc/ssh/sshd_config 2>/dev/null; then
        root_login_disabled=true
    fi

    local evidence=$(cat <<EOF
{
    "asset_id": "$(uuidgen)",
    "control_id": "$(uuidgen)",
    "evidence_type": "AdminPrivileges",
    "evidence_data": {
        "admin_accounts_count": $admin_accounts_count,
        "root_login_disabled": $root_login_disabled,
        "separation_of_duties": true
    },
    "collection_method": "Agent"
}
EOF
)

    submit_evidence "$evidence"
}

# Function to collect MFA evidence
collect_mfa_evidence() {
    log_info "Collecting MFA evidence..."

    local ssh_mfa_enabled=false

    # Check if PAM MFA is configured
    if grep -q "pam_google_authenticator" /etc/pam.d/sshd 2>/dev/null; then
        ssh_mfa_enabled=true
    fi

    local evidence=$(cat <<EOF
{
    "asset_id": "$(uuidgen)",
    "control_id": "$(uuidgen)",
    "evidence_type": "MFAStatus",
    "evidence_data": {
        "mfa_remote_access": $ssh_mfa_enabled,
        "ssh_password_auth_disabled": $(grep -q "^PasswordAuthentication no" /etc/ssh/sshd_config 2>/dev/null && echo "true" || echo "false")
    },
    "collection_method": "Agent"
}
EOF
)

    submit_evidence "$evidence"
}

# Function to collect backup evidence
collect_backup_evidence() {
    log_info "Collecting backup evidence..."

    local backup_schedule_configured=false
    local last_backup_days_ago=999

    # Check for backup cron jobs
    if crontab -l 2>/dev/null | grep -qE "backup|rsync|tar"; then
        backup_schedule_configured=true
    fi

    # Check for recent backup files
    if [ -d "/backup" ]; then
        local latest_backup=$(find /backup -type f -mtime -7 | head -1)
        if [ -n "$latest_backup" ]; then
            last_backup_days_ago=$(( ($(date +%s) - $(stat -c %Y "$latest_backup")) / 86400 ))
        fi
    fi

    local evidence=$(cat <<EOF
{
    "asset_id": "$(uuidgen)",
    "control_id": "$(uuidgen)",
    "evidence_type": "BackupStatus",
    "evidence_data": {
        "backup_schedule_configured": $backup_schedule_configured,
        "last_backup_days_ago": $last_backup_days_ago,
        "backup_retention_days": 30
    },
    "collection_method": "Agent"
}
EOF
)

    submit_evidence "$evidence"
}

# Function to submit evidence
submit_evidence() {
    local evidence="$1"

    curl -s -X POST "$SERVER_URL/api/v1/evidence" \
        -H "Content-Type: application/json" \
        -d "$evidence" > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        log_info "Evidence submitted successfully"
    else
        log_error "Failed to submit evidence"
    fi
}

# Main execution
main() {
    log_info "=== EEMCARS Linux Agent v$AGENT_VERSION ==="
    log_info "Agent ID: $AGENT_ID"
    log_info "Server: $SERVER_URL"

    # Register agent
    if register_agent; then
        log_info "Starting evidence collection..."

        # Collect all evidence types
        collect_patch_evidence
        collect_application_hardening_evidence
        collect_admin_privileges_evidence
        collect_mfa_evidence
        collect_backup_evidence

        log_info "Initial evidence collection complete"

        # Start heartbeat loop
        log_info "Starting heartbeat loop (interval: $HEARTBEAT_INTERVAL seconds)..."
        while true; do
            send_heartbeat
            sleep $HEARTBEAT_INTERVAL
        done
    else
        log_error "Agent registration failed. Exiting."
        exit 1
    fi
}

# Run main function
main
