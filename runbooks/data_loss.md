# Runbook: Data Loss — HIGH RISK

## ⚠ This is a HIGH RISK incident. Escalate immediately.

## Symptoms
User reports missing files, deleted data, corrupted documents, or accidental overwrites.

## Step 1 — Immediate containment
Do NOT attempt to recover data without first containing the incident:
- Ask the user to stop using the affected device or storage location immediately.
- Do not write new data to the affected disk or share — this can overwrite recoverable data.

## Step 2 — Assess scope
Ask the user:
- What data is missing? (file names, folders, approximate size)
- When was it last known to be present?
- Was the data on a local drive, network share, or cloud storage?

## Step 3 — Restore from backup
Backups run daily and are retained for 30 days. Use the backup management portal at `backup.company.com/restore` to locate and restore the affected files. Provide the user with the estimated restoration time (typically 1–4 hours for under 10 GB).

## Step 4 — Forensic preservation
Before restoring, preserve a snapshot of the current state for investigation purposes. Log the incident in the security ticket system with a timestamp, scope, and the user's account details.

## Step 5 — Mandatory escalation
All data loss incidents must be reported to:
- The user's direct manager
- The security team: `security@company.com`
- The data protection officer if the data contains personal information (GDPR/CCPA obligation)

Do not close this ticket until the security team has acknowledged the report.

## Risk tier: HIGH — always escalate, never auto-resolve
