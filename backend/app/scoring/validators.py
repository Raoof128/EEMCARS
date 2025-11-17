"""
Evidence validators for Essential Eight controls
"""
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime, timedelta
from app.models import Evidence, Asset, MaturityRequirement


class EvidenceValidator:
    """
    Validates evidence against Essential Eight requirements
    """

    def __init__(self):
        self.validators = self._register_validators()

    def _register_validators(self) -> Dict[str, Callable]:
        """Register validation functions for specific checks"""
        return {
            # Application Control validators
            "whitelisting_enabled": self._validate_whitelisting_enabled,
            "execution_policies_configured": self._validate_execution_policies,
            "logging_enabled": self._validate_logging_enabled,
            "servers_protected": self._validate_servers_protected,
            "cryptographic_validation": self._validate_cryptographic_validation,
            "microsoft_blocklist": self._validate_microsoft_blocklist,

            # Patch Application validators
            "internet_facing_patched": self._validate_internet_facing_patched,
            "patch_timeframe_2weeks": self._validate_patch_timeframe,
            "critical_48hours": self._validate_critical_48hours,
            "automated_patching": self._validate_automated_patching,

            # Microsoft Office Macros validators
            "macros_disabled_default": self._validate_macros_disabled,
            "internet_macros_blocked": self._validate_internet_macros_blocked,
            "trusted_locations": self._validate_trusted_locations,
            "digital_signatures_required": self._validate_digital_signatures,

            # User Application Hardening validators
            "flash_blocked": self._validate_flash_blocked,
            "ads_blocked": self._validate_ads_blocked,
            "java_disabled": self._validate_java_disabled,
            "pdf_javascript_disabled": self._validate_pdf_javascript,
            "browser_hardening_gpo": self._validate_browser_hardening,

            # Restrict Admin Privileges validators
            "admin_accounts_identified": self._validate_admin_accounts,
            "separation_duties": self._validate_separation_of_duties,
            "internet_restricted": self._validate_admin_internet_restricted,
            "jit_admin": self._validate_jit_admin,
            "dedicated_paw": self._validate_dedicated_paw,

            # Patch Operating Systems validators
            "os_patched_monthly": self._validate_os_patch_monthly,
            "os_patched_2weeks": self._validate_os_patch_2weeks,
            "os_version_current": self._validate_os_version_current,

            # Multi-Factor Authentication validators
            "mfa_online_services": self._validate_mfa_online_services,
            "mfa_remote_access": self._validate_mfa_remote_access,
            "mfa_privileged_actions": self._validate_mfa_privileged_actions,
            "phishing_resistant": self._validate_phishing_resistant_mfa,

            # Regular Backups validators
            "backup_schedule": self._validate_backup_schedule,
            "backup_retention": self._validate_backup_retention,
            "offline_backups": self._validate_offline_backups,
            "backup_encryption": self._validate_backup_encryption,
            "immutable_backups": self._validate_immutable_backups,
            "quarterly_restore_test": self._validate_restore_testing,
        }

    def get_validator(self, check_name: str) -> Optional[Callable]:
        """Get validator function for a specific check"""
        return self.validators.get(check_name)

    # Application Control Validators

    async def _validate_whitelisting_enabled(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate application whitelisting is enabled"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            if data.get("application_control", {}).get("enabled") is True:
                return {
                    "passed": True,
                    "message": "Application whitelisting is enabled",
                    "evidence_id": str(evidence.id)
                }
            if "applocker" in str(data).lower() or "application_control" in str(data).lower():
                if data.get("rules_count", 0) > 0:
                    return {
                        "passed": True,
                        "message": f"AppLocker configured with {data.get('rules_count')} rules",
                        "evidence_id": str(evidence.id)
                    }

        return {
            "passed": False,
            "message": "No evidence of application whitelisting",
            "evidence_id": None
        }

    async def _validate_execution_policies(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate execution policies are configured"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            if "execution_policy" in str(data).lower():
                policy = data.get("execution_policy", "").lower()
                if policy in ["restricted", "allsigned", "remotesigned"]:
                    return {
                        "passed": True,
                        "message": f"Execution policy set to {policy}",
                        "evidence_id": str(evidence.id)
                    }

        return {
            "passed": False,
            "message": "No secure execution policy configured",
            "evidence_id": None
        }

    async def _validate_logging_enabled(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate logging is enabled"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            if data.get("logging", {}).get("enabled") is True:
                return {
                    "passed": True,
                    "message": "Application control logging is enabled",
                    "evidence_id": str(evidence.id)
                }

        return {
            "passed": False,
            "message": "Application control logging not enabled",
            "evidence_id": None
        }

    async def _validate_servers_protected(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate servers have application control"""
        if asset.asset_type.value in ["Windows", "Linux"]:
            for evidence in evidence_list:
                data = evidence.evidence_data
                if data.get("server_protection", {}).get("enabled"):
                    return {
                        "passed": True,
                        "message": "Server application control is enabled",
                        "evidence_id": str(evidence.id)
                    }

        return {
            "passed": False,
            "message": "Server application control not verified",
            "evidence_id": None
        }

    async def _validate_cryptographic_validation(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate cryptographic hash or publisher certificate rules"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            rules = data.get("application_control", {}).get("rules", [])
            for rule in rules:
                if rule.get("type") in ["hash", "publisher", "certificate"]:
                    return {
                        "passed": True,
                        "message": f"Cryptographic rules configured ({rule.get('type')})",
                        "evidence_id": str(evidence.id)
                    }

        return {
            "passed": False,
            "message": "No cryptographic validation rules found",
            "evidence_id": None
        }

    async def _validate_microsoft_blocklist(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate Microsoft recommended block rules are implemented"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            if data.get("microsoft_recommended_blocks") is True:
                return {
                    "passed": True,
                    "message": "Microsoft recommended block rules implemented",
                    "evidence_id": str(evidence.id)
                }

        return {
            "passed": False,
            "message": "Microsoft recommended block rules not implemented",
            "evidence_id": None
        }

    # Patch Application Validators

    async def _validate_internet_facing_patched(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate internet-facing applications are patched"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            if data.get("internet_facing"):
                patch_age_days = data.get("patch_age_days", 999)
                if patch_age_days <= 14:
                    return {
                        "passed": True,
                        "message": f"Internet-facing app patched ({patch_age_days} days old)",
                        "evidence_id": str(evidence.id)
                    }

        return {
            "passed": False,
            "message": "Internet-facing applications not up to date",
            "evidence_id": None
        }

    async def _validate_patch_timeframe(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate patches applied within 2 weeks"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            patch_compliance = data.get("patch_compliance", {})
            if patch_compliance.get("within_14_days_percent", 0) >= 95:
                return {
                    "passed": True,
                    "message": f"Patch compliance: {patch_compliance.get('within_14_days_percent')}%",
                    "evidence_id": str(evidence.id)
                }

        return {
            "passed": False,
            "message": "Patch timeframe compliance below threshold",
            "evidence_id": None
        }

    async def _validate_critical_48hours(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate critical patches applied within 48 hours"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            critical_patches = data.get("critical_patches", {})
            if critical_patches.get("within_48_hours_percent", 0) >= 95:
                return {
                    "passed": True,
                    "message": f"Critical patch compliance: {critical_patches.get('within_48_hours_percent')}%",
                    "evidence_id": str(evidence.id)
                }

        return {
            "passed": False,
            "message": "Critical patches not applied within 48 hours",
            "evidence_id": None
        }

    async def _validate_automated_patching(
        self,
        evidence_list: List[Evidence],
        asset: Asset,
        requirement: MaturityRequirement
    ) -> Dict[str, Any]:
        """Validate automated patching is configured"""
        for evidence in evidence_list:
            data = evidence.evidence_data
            if data.get("automated_patching", {}).get("enabled") is True:
                return {
                    "passed": True,
                    "message": "Automated patching is enabled",
                    "evidence_id": str(evidence.id)
                }

        return {
            "passed": False,
            "message": "Automated patching not enabled",
            "evidence_id": None
        }

    # Additional validator stubs (simplified for brevity)

    async def _validate_macros_disabled(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("macros_disabled") is True:
                return {"passed": True, "message": "Macros disabled", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Macros not disabled", "evidence_id": None}

    async def _validate_internet_macros_blocked(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("internet_macros_blocked") is True:
                return {"passed": True, "message": "Internet macros blocked", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Internet macros not blocked", "evidence_id": None}

    async def _validate_trusted_locations(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("trusted_locations_configured"):
                return {"passed": True, "message": "Trusted locations configured", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Trusted locations not configured", "evidence_id": None}

    async def _validate_digital_signatures(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("digital_signatures_required") is True:
                return {"passed": True, "message": "Digital signatures required", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Digital signatures not required", "evidence_id": None}

    async def _validate_flash_blocked(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("flash_blocked") is True:
                return {"passed": True, "message": "Flash blocked", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Flash not blocked", "evidence_id": None}

    async def _validate_ads_blocked(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("ads_blocked") is True:
                return {"passed": True, "message": "Ads blocked", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Ads not blocked", "evidence_id": None}

    async def _validate_java_disabled(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("java_disabled") is True:
                return {"passed": True, "message": "Java disabled", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Java not disabled", "evidence_id": None}

    async def _validate_pdf_javascript(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("pdf_javascript_disabled") is True:
                return {"passed": True, "message": "PDF JavaScript disabled", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "PDF JavaScript not disabled", "evidence_id": None}

    async def _validate_browser_hardening(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("browser_hardening_gpo") is True:
                return {"passed": True, "message": "Browser hardening via GPO", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Browser hardening not via GPO", "evidence_id": None}

    async def _validate_admin_accounts(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("admin_accounts_count") is not None:
                return {"passed": True, "message": "Admin accounts identified", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Admin accounts not identified", "evidence_id": None}

    async def _validate_separation_of_duties(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("separation_of_duties") is True:
                return {"passed": True, "message": "Separation of duties implemented", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Separation of duties not implemented", "evidence_id": None}

    async def _validate_admin_internet_restricted(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("admin_internet_restricted") is True:
                return {"passed": True, "message": "Admin internet access restricted", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Admin internet access not restricted", "evidence_id": None}

    async def _validate_jit_admin(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("jit_admin_enabled") is True:
                return {"passed": True, "message": "JIT admin enabled", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "JIT admin not enabled", "evidence_id": None}

    async def _validate_dedicated_paw(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("dedicated_paw") is True:
                return {"passed": True, "message": "Dedicated PAW implemented", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Dedicated PAW not implemented", "evidence_id": None}

    async def _validate_os_patch_monthly(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("os_patch_age_days", 999) <= 30:
                return {"passed": True, "message": "OS patched within 30 days", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "OS not patched within 30 days", "evidence_id": None}

    async def _validate_os_patch_2weeks(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("os_patch_age_days", 999) <= 14:
                return {"passed": True, "message": "OS patched within 14 days", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "OS not patched within 14 days", "evidence_id": None}

    async def _validate_os_version_current(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("os_version_supported") is True:
                return {"passed": True, "message": "OS version is current and supported", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "OS version not current", "evidence_id": None}

    async def _validate_mfa_online_services(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("mfa_online_services") is True:
                return {"passed": True, "message": "MFA enabled for online services", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "MFA not enabled for online services", "evidence_id": None}

    async def _validate_mfa_remote_access(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("mfa_remote_access") is True:
                return {"passed": True, "message": "MFA enabled for remote access", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "MFA not enabled for remote access", "evidence_id": None}

    async def _validate_mfa_privileged_actions(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("mfa_privileged_actions") is True:
                return {"passed": True, "message": "MFA for privileged actions", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "MFA not enabled for privileged actions", "evidence_id": None}

    async def _validate_phishing_resistant_mfa(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("phishing_resistant_mfa") is True:
                return {"passed": True, "message": "Phishing-resistant MFA enabled", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Phishing-resistant MFA not enabled", "evidence_id": None}

    async def _validate_backup_schedule(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("backup_schedule_configured") is True:
                return {"passed": True, "message": "Backup schedule configured", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Backup schedule not configured", "evidence_id": None}

    async def _validate_backup_retention(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("backup_retention_days", 0) >= 30:
                return {"passed": True, "message": "Backup retention configured", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Backup retention not adequate", "evidence_id": None}

    async def _validate_offline_backups(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("offline_backups") is True:
                return {"passed": True, "message": "Offline backups configured", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Offline backups not configured", "evidence_id": None}

    async def _validate_backup_encryption(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("backup_encryption") is True:
                return {"passed": True, "message": "Backup encryption enabled", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Backup encryption not enabled", "evidence_id": None}

    async def _validate_immutable_backups(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            if evidence.evidence_data.get("immutable_backups") is True:
                return {"passed": True, "message": "Immutable backups configured", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Immutable backups not configured", "evidence_id": None}

    async def _validate_restore_testing(self, evidence_list, asset, requirement):
        for evidence in evidence_list:
            last_test = evidence.evidence_data.get("last_restore_test_days", 999)
            if last_test <= 90:
                return {"passed": True, "message": f"Restore tested {last_test} days ago", "evidence_id": str(evidence.id)}
        return {"passed": False, "message": "Restore not tested in last 90 days", "evidence_id": None}
