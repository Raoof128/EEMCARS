# EEMCARS Windows Agent
# Essential Eight Evidence Collection Agent for Windows

param(
    [string]$ServerUrl = "http://localhost:8000",
    [string]$AgentId = $null,
    [int]$HeartbeatInterval = 300  # 5 minutes
)

$ErrorActionPreference = "Continue"
$AgentVersion = "1.0.0"

# Generate or load Agent ID
if (-not $AgentId) {
    $AgentId = "WIN-" + $env:COMPUTERNAME + "-" + (Get-Date -Format "yyyyMMddHHmmss")
}

# Function to register agent
function Register-Agent {
    $hostname = $env:COMPUTERNAME
    $ipAddress = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notlike "*Loopback*" } | Select-Object -First 1).IPAddress

    $body = @{
        agent_id = $AgentId
        asset_id = (New-Guid).Guid
        agent_version = $AgentVersion
        platform = "Windows"
        capabilities = @{
            os = (Get-WmiObject Win32_OperatingSystem).Caption
            os_version = (Get-WmiObject Win32_OperatingSystem).Version
            hostname = $hostname
            ip_address = $ipAddress
        }
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "$ServerUrl/api/v1/agents/register" -Method Post -Body $body -ContentType "application/json"
        Write-Host "Agent registered: $($response.agent_id)"
        return $true
    }
    catch {
        Write-Error "Failed to register agent: $_"
        return $false
    }
}

# Function to send heartbeat
function Send-Heartbeat {
    $body = @{
        agent_id = $AgentId
        status = "Active"
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "$ServerUrl/api/v1/agents/heartbeat" -Method Post -Body $body -ContentType "application/json" | Out-Null
        Write-Host "Heartbeat sent at $(Get-Date)"
    }
    catch {
        Write-Error "Heartbeat failed: $_"
    }
}

# Function to collect Application Control evidence
function Get-ApplicationControlEvidence {
    $evidence = @{
        application_control = @{
            enabled = $false
            rules_count = 0
            logging_enabled = $false
        }
    }

    try {
        # Check AppLocker
        $appLockerPolicy = Get-AppLockerPolicy -Effective -ErrorAction SilentlyContinue
        if ($appLockerPolicy) {
            $evidence.application_control.enabled = $true
            $evidence.application_control.rules_count = ($appLockerPolicy.RuleCollections | Measure-Object).Count

            # Check logging
            $logConfig = wevtutil gl "Microsoft-Windows-AppLocker/EXE and DLL"
            $evidence.application_control.logging_enabled = $logConfig -match "enabled: true"
        }
    }
    catch {
        Write-Warning "Failed to collect Application Control evidence: $_"
    }

    return $evidence
}

# Function to collect Patch status evidence
function Get-PatchEvidence {
    $evidence = @{
        patch_compliance = @{
            os_patch_age_days = 999
            missing_patches_count = 0
            last_patch_date = $null
        }
    }

    try {
        # Get Windows Update history
        $updateSession = New-Object -ComObject Microsoft.Update.Session
        $updateSearcher = $updateSession.CreateUpdateSearcher()
        $historyCount = $updateSearcher.GetTotalHistoryCount()

        if ($historyCount -gt 0) {
            $updateHistory = $updateSearcher.QueryHistory(0, 1)
            $lastUpdate = $updateHistory | Select-Object -First 1
            $evidence.patch_compliance.last_patch_date = $lastUpdate.Date
            $evidence.patch_compliance.os_patch_age_days = ((Get-Date) - $lastUpdate.Date).Days
        }

        # Check for missing updates
        $criteria = "IsInstalled=0 and Type='Software'"
        $searchResult = $updateSearcher.Search($criteria)
        $evidence.patch_compliance.missing_patches_count = $searchResult.Updates.Count
    }
    catch {
        Write-Warning "Failed to collect Patch evidence: $_"
    }

    return $evidence
}

# Function to collect Office Macro settings evidence
function Get-MacroEvidence {
    $evidence = @{
        macros_disabled = $false
        internet_macros_blocked = $false
    }

    try {
        # Check Office macro settings
        $officeVersions = @("16.0", "15.0", "14.0")
        $officeApps = @("Word", "Excel", "PowerPoint")

        foreach ($version in $officeVersions) {
            foreach ($app in $officeApps) {
                $regPath = "HKCU:\Software\Microsoft\Office\$version\$app\Security"
                if (Test-Path $regPath) {
                    $vbaWarnings = (Get-ItemProperty -Path $regPath -Name VBAWarnings -ErrorAction SilentlyContinue).VBAWarnings
                    if ($vbaWarnings -eq 3 -or $vbaWarnings -eq 4) {
                        $evidence.macros_disabled = $true
                    }

                    $blockInternet = (Get-ItemProperty -Path $regPath -Name BlockContentExecutionFromInternet -ErrorAction SilentlyContinue).BlockContentExecutionFromInternet
                    if ($blockInternet -eq 1) {
                        $evidence.internet_macros_blocked = $true
                    }
                }
            }
        }
    }
    catch {
        Write-Warning "Failed to collect Macro evidence: $_"
    }

    return $evidence
}

# Function to collect MFA evidence
function Get-MFAEvidence {
    $evidence = @{
        mfa_remote_access = $false
        rdp_nla_enabled = $false
    }

    try {
        # Check RDP Network Level Authentication
        $nla = (Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name UserAuthentication -ErrorAction SilentlyContinue).UserAuthentication
        $evidence.rdp_nla_enabled = ($nla -eq 1)
    }
    catch {
        Write-Warning "Failed to collect MFA evidence: $_"
    }

    return $evidence
}

# Function to collect backup evidence
function Get-BackupEvidence {
    $evidence = @{
        backup_schedule_configured = $false
        backup_retention_days = 0
        last_backup_days_ago = 999
    }

    try {
        # Check Windows Backup schedule
        $backupTasks = Get-ScheduledTask | Where-Object { $_.TaskName -like "*Backup*" }
        $evidence.backup_schedule_configured = ($backupTasks.Count -gt 0)

        # Check for recent backup files (example: C:\Backups)
        if (Test-Path "C:\Backups") {
            $latestBackup = Get-ChildItem "C:\Backups" -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 1
            if ($latestBackup) {
                $evidence.last_backup_days_ago = ((Get-Date) - $latestBackup.LastWriteTime).Days
            }
        }
    }
    catch {
        Write-Warning "Failed to collect Backup evidence: $_"
    }

    return $evidence
}

# Function to submit evidence
function Submit-Evidence {
    param(
        [string]$ControlId,
        [string]$EvidenceType,
        [hashtable]$EvidenceData
    )

    $body = @{
        asset_id = (New-Guid).Guid  # In production, this would be the actual asset ID
        control_id = (New-Guid).Guid  # In production, this would be the actual control ID
        evidence_type = $EvidenceType
        evidence_data = $EvidenceData
        collection_method = "Agent"
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri "$ServerUrl/api/v1/evidence" -Method Post -Body $body -ContentType "application/json" | Out-Null
        Write-Host "Evidence submitted: $EvidenceType"
    }
    catch {
        Write-Error "Failed to submit evidence: $_"
    }
}

# Main execution
Write-Host "=== EEMCARS Windows Agent v$AgentVersion ==="
Write-Host "Agent ID: $AgentId"
Write-Host "Server: $ServerUrl"

# Register agent
if (Register-Agent) {
    Write-Host "Starting evidence collection..."

    # Collect and submit evidence
    $appControlEvidence = Get-ApplicationControlEvidence
    Submit-Evidence -ControlId "E8-AC" -EvidenceType "ApplicationControl" -EvidenceData $appControlEvidence

    $patchEvidence = Get-PatchEvidence
    Submit-Evidence -ControlId "E8-PA" -EvidenceType "PatchStatus" -EvidenceData $patchEvidence

    $macroEvidence = Get-MacroEvidence
    Submit-Evidence -ControlId "E8-MS" -EvidenceType "MacroSettings" -EvidenceData $macroEvidence

    $mfaEvidence = Get-MFAEvidence
    Submit-Evidence -ControlId "E8-MFA" -EvidenceType "MFAStatus" -EvidenceData $mfaEvidence

    $backupEvidence = Get-BackupEvidence
    Submit-Evidence -ControlId "E8-RB" -EvidenceType "BackupStatus" -EvidenceData $backupEvidence

    Write-Host "Initial evidence collection complete"

    # Start heartbeat loop
    Write-Host "Starting heartbeat loop (interval: $HeartbeatInterval seconds)..."
    while ($true) {
        Send-Heartbeat
        Start-Sleep -Seconds $HeartbeatInterval
    }
}
else {
    Write-Error "Agent registration failed. Exiting."
    exit 1
}
