# Merge Resolution Report -Jose Diaz 28Sep25

## Conflict Scenario
During collaborative development, two branches introduced overlapping changes:
- **Branch A**: Added secure password hashing with Werkzeug.
- **Branch B**: Refactored database queries to use parameterized statements.

Both branches modified the `create_user` and `login` functions, leading to a **merge conflict** in:
- Password handling lines
- SQL execution lines

---

## Resolution Approach
1. **Reviewed both sets of changes**:
   - Branch A provided secure password hashing.
   - Branch B provided safe query execution.

2. **Merged complementary improvements**:
   - Integrated `generate_password_hash()` and `check_password_hash()`.
   - Replaced raw SQL string concatenation with parameterized queries (`?` placeholders).

3. **Removed redundant or insecure code**:
   - Deleted old MD5 hashing logic.
   - Eliminated string-formatted SQL queries.

4. **Updated tests accordingly**:
   - Adjusted login tests to use the new hash-based logic.
   - Confirmed database inserts work with parameterized queries.

---

## Testing Performed
- **Unit Testing**:
  - Created users with valid and invalid input.
  - Verified duplicate usernames return `409 Conflict`.
- **Integration Testing**:
  - Confirmed login succeeds with correct credentials and fails otherwise.
  - Confirmed SQL injection attempts are neutralized.
- **Manual Verification**:
  - Ran `/health`, `/users`, `/login`, and `/users` (POST) endpoints using `curl` and Postman.
  - Checked that sensitive information is no longer logged or returned in responses.

Result: Application runs securely with merged functionality intact.

---
