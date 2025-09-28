# Code Review Report - Jose Diaz 28Sep25

## Overview
This review evaluates the security posture of the initial `app.py` implementation.  
The code contained intentional vulnerabilities for educational purposes.  
This is a code report outlining vulnerabilities and providing professional comments.
Proposed code fixes are included in the app_fixed.py file.

---

## Security Vulnerabilities Found

1. **Hardcoded Secrets**
   - `DATABASE_URL` and `API_SECRET` were embedded directly in the source code.
   - Impact: Secrets could be leaked via version control, logs, or accidental disclosure.
   - Severity: **High**

2. **Broken Authentication / Weak Password Hashing** ChatGPT Sept 2025
   - Passwords were hashed with `MD5`, which is fast, unsalted, and broken for password storage.
   - Impact: Enables trivial cracking of leaked password hashes.
   - Severity: **High**

3. **SQL Injection**
   - User input was interpolated directly into SQL statements with string formatting.
   - Impact: Attackers could extract, modify, or delete database data.
   - Severity: **Critical**

4. **Sensitive Information Disclosure**
   - Plaintext passwords were printed to logs (`print(f"Created user: ...")`).
   - `/health` endpoint leaked the entire database connection string.
   - Impact: Exposure of credentials or sensitive system information.
   - Severity: **High**

5. **Debug Mode in Production** ChatGPT Sept 2025.
   - `app.run(debug=True)` was set by default.
   - Impact: Exposes the interactive debugger, enabling remote code execution.
   - Severity: **High**

6. **Lack of Input Validation**
   - No checks for missing or malformed `username` and `password` fields.
   - Impact: Application instability, potential abuse.
   - Severity: **Medium**

7. **Overly Permissive User Enumeration**
   - `/users` endpoint exposed all usernames publicly.
   - Impact: Enables targeted brute-force attacks.
   - Severity: **Medium**

---

## Professional Review Comments

- Secrets should **never** be hardcoded. Use environment variables or a secret manager.
- Password hashing must use a **slow, salted hash function** (e.g., `bcrypt`, `argon2`, or PBKDF2 via Werkzeug). ChatGPT Sept 2025
- Always use try/catch block to encapsulate connection functions. Best practices.
- Always use **parameterized queries** to prevent SQL injection.
- Do not log sensitive data. Redact or hash identifiers where needed.
- Avoid exposing unnecessary endpoints in production (e.g., `/users` listing).
- Debug mode must remain disabled outside of local development. ChatGPT Sept 2025
- Security should be layered: input validation, least privilege, HTTPS, and monitoring.

---

## Severity Ratings
- **Critical**: Vulnerabilities enabling direct compromise of the database or remote code execution. (SQL injection)
- **High**: Vulnerabilities exposing secrets, enabling credential theft, or unsafe deployment practices. (hardcoded secrets, MD5, logging, debug mode)
- **Medium**: Issues that aid attackers but do not directly compromise confidentiality/integrity. (input validation gaps, user enumeration)
- **Low**: Minor improvements or best practices (e.g., structured logging, more detailed error handling).

---
