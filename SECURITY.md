# Security Policy

## Reporting a Vulnerability

The EEMCARS team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security vulnerabilities by:

1. **GitHub Security Advisories (Preferred)**
   - Go to https://github.com/yourusername/eemcars/security/advisories/new
   - Fill out the vulnerability details
   - We will respond within 48 hours

2. **Email**
   - Send to: security@eemcars.io
   - Use PGP key: [Link to PGP key]
   - Include detailed information about the vulnerability

### What to Include

Please include the following information:
- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of affected source code (tag/branch/commit/URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue (what an attacker could do)
- Suggested remediation (if any)

### Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity
  - Critical: 24-48 hours
  - High: 7 days
  - Medium: 30 days
  - Low: 90 days

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Best Practices

### Deployment Security

#### Azure Infrastructure
- ✅ All data stored in Australian regions (data sovereignty)
- ✅ TLS 1.2+ enforced for all connections
- ✅ Azure Key Vault for secrets management
- ✅ Network isolation with VNets and NSGs
- ✅ WAF enabled with OWASP 3.2 ruleset
- ✅ DDoS protection standard

#### Database Security
- ✅ AES-256 encryption at rest
- ✅ TLS encryption in transit
- ✅ Private endpoint access only
- ✅ Automated backups with geo-redundancy
- ✅ Point-in-time recovery enabled

#### Application Security
- ✅ JWT token authentication
- ✅ Bcrypt password hashing
- ✅ Role-based access control (RBAC)
- ✅ SQL injection protection (parameterized queries)
- ✅ XSS prevention (input sanitization)
- ✅ CORS properly configured
- ✅ Rate limiting implemented
- ✅ Security headers configured

### Configuration Security

#### Required Security Settings

```bash
# .env Production Configuration
SECRET_KEY=<strong-random-key-min-32-chars>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database
DATABASE_URL=<use-azure-key-vault>
DB_POOL_SIZE=20

# Azure Security
AZURE_KEYVAULT_URL=https://your-kv.vault.azure.net/
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
```

#### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use Azure Key Vault for all secrets
- [ ] Enable HTTPS/TLS in production
- [ ] Configure proper CORS origins
- [ ] Enable WAF on Application Gateway
- [ ] Set up Azure Monitor alerts
- [ ] Configure backup retention
- [ ] Enable audit logging
- [ ] Review RBAC permissions
- [ ] Rotate credentials regularly

### Agent Security

#### Windows Agent
- Runs with minimum required permissions
- Uses TLS for API communication
- Evidence hashed with SHA-256
- No sensitive data stored locally

#### Linux Agent
- Requires sudo only for specific checks
- Validates server certificates
- Secure evidence transmission
- Log rotation configured

### Known Security Features

#### Authentication
- JWT tokens with expiration
- Bcrypt password hashing (cost factor 12)
- Session management with Redis
- Account lockout after failed attempts

#### Authorization
- Four-tier RBAC model
- Principle of least privilege
- Audit trail for all actions
- Immutable audit logs

#### Data Protection
- AES-256 encryption at rest
- TLS 1.2+ in transit
- Secrets in Azure Key Vault
- PII data minimization

#### Network Security
- Private endpoints for database
- Network Security Groups (NSGs)
- Application Gateway with WAF
- DDoS protection

### Compliance

EEMCARS is designed to support:
- **ACSC Essential Eight** - Core framework
- **Australian Privacy Principles** - Data handling
- **ISO 27001** - Information security
- **NIST Cybersecurity Framework** - Security controls

### Security Scanning

The project includes automated security scanning:
- **Trivy** - Container vulnerability scanning
- **Bandit** - Python security linting
- **npm audit** - JavaScript dependency scanning
- **Dependabot** - Automated dependency updates
- **CodeQL** - Static code analysis

### Disclosure Policy

- Security researchers will be credited (with permission)
- We follow coordinated vulnerability disclosure
- Public disclosure after patch is available
- Security advisories published on GitHub

### Hall of Fame

We thank the following security researchers:
- (Names will be added as vulnerabilities are reported and fixed)

### Contact

- Security Email: security@eemcars.io
- PGP Key: [Link to PGP key]
- Response SLA: 48 hours

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [ACSC Essential Eight](https://www.cyber.gov.au/acsc/view-all-content/essential-eight)
- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
