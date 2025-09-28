# Incident Response Plan - Jose Diaz 28Sep25

## Purpose
This plan provides a structured response if the application suffers a security incident such as credential leakage, SQL injection, or unauthorized access.

---

## Step-by-Step Crisis Response Procedures

1. **Detection**
   - Monitor logs and intrusion alerts for suspicious activity (failed logins, SQL errors).
   - Use automated tools to detect abnormal traffic patterns.

2. **Containment**
   - Immediately disable compromised user accounts.
   - Block malicious IP addresses at the firewall or reverse proxy.
   - If secrets are leaked, rotate affected API keys and database credentials.

3. **Eradication**
   - Patch the underlying vulnerability (e.g., update code, reconfigure DB).
   - Verify that insecure endpoints or debug mode are disabled.

4. **Recovery**
   - Restore affected systems from clean backups.
   - Re-enable services after validation and security testing.
   - Monitor closely for repeat attempts.

5. **Post-Incident Review**
   - Document incident timeline, root cause, and remediation steps.
   - Update policies and code to prevent recurrence.

---

## Prevention Measures Implemented
- Secrets moved to environment variables and `.env` (not in code).
- Secure password hashing with Werkzeug (`pbkdf2:sha256`). ChatGPT Sept 2025
- Parameterized SQL queries to eliminate injection.
- Debug mode controlled by environment variable. ChatGPT Sept 2025
- Sensitive logs removed.

---
ChatGPT Sept 2025 - I wasn't completely sure of the required roles for this section.
## Team Communication Protocols
- **Incident Commander**: Assigns roles, coordinates response.
- **Engineering Lead**: Implements fixes and manages code changes.
- **Operations Lead**: Monitors infrastructure, rotates secrets.
- **Communications Lead**: Provides updates to stakeholders and (if necessary) end-users.
- **Post-mortem Meeting**: Held within 48 hours to share lessons learned.

---
