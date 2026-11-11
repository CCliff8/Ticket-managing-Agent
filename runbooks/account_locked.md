# Runbook: Account Locked

## Symptoms
User receives "account locked" or "too many failed attempts" message when logging in.

## Step 1 — Self-service unlock
Accounts auto-unlock after 30 minutes. Direct the user to wait and try again, or use the self-service unlock portal at `portal.company.com/unlock-account` (requires access to registered email or phone).

## Step 2 — Verify identity before manual unlock
If manual unlock is needed, verify the user's identity before proceeding:
- Full name and employee ID
- Answer to one security question on file
- Confirmation of their manager's name

Never unlock an account without completing identity verification — locked accounts may indicate a brute-force attempt.

## Step 3 — Check for suspicious activity
Before unlocking, review the account's recent login history in the admin console at `admin.company.com/users`. If you see:
- Multiple failed attempts from an unfamiliar IP address
- Login attempts outside normal working hours
- Geographic anomalies (e.g., attempts from another country)

Do NOT unlock. Escalate to the security team immediately (see Security Incident runbook).

## Step 4 — Unlock and notify
If no suspicious activity is found, unlock the account via `admin.company.com/users`. Notify the user and recommend they change their password after regaining access.

## Risk tier: LOW for standard lockout | HIGH if suspicious activity is detected
