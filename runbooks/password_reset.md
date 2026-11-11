# Runbook: Password Reset

## Symptoms
User cannot log in, receives "invalid password" error, or forgot their password.

## Step 1 — Self-service reset
Direct the user to `portal.company.com/reset-password`. They must have access to their registered email address or phone number to complete the self-service reset.

## Step 2 — Identity verification (manual reset)
If the self-service portal is unavailable or the user does not have access to their recovery contact, verify identity by asking:
- Full name and employee ID
- Manager's name
- Last four digits of their employee badge number

Never reset a password without completing identity verification.

## Step 3 — Issue temporary password
After verification, issue a temporary password with the format `Temp@XXXXXX` (where X is a random 6-digit number). Temporary passwords expire after 24 hours. The user must change it on first login.

## Step 4 — MFA reset
If the user also needs to reset their MFA device (e.g., lost phone), this requires separate approval from their direct manager via email to `security@company.com`.

## Account lockout policy
Accounts are locked after 5 consecutive failed login attempts. Lockouts auto-release after 30 minutes. For immediate manual unlock, follow the Account Locked runbook.

## Risk tier: LOW for standard reset | MEDIUM if identity cannot be verified | HIGH if compromise is suspected
