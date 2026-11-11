# Runbook: Security Incident — HIGH RISK

## ⚠ This is a HIGH RISK runbook. Immediate escalation is mandatory.

## Symptoms
Unauthorized access to accounts, suspicious login alerts, phishing attacks, malware detection, data exfiltration, or any event where systems or data may have been compromised.

## Step 1 — Contain immediately (do not delay)
- Ask the user to disconnect their device from all networks (Wi-Fi, Ethernet, VPN) immediately.
- Do not power off the machine — this can destroy volatile forensic evidence.
- If the incident involves a cloud account (email, SaaS), revoke active sessions immediately via `admin.company.com/sessions`.

## Step 2 — Escalate within 15 minutes
Security incidents must be reported to the security team within 15 minutes of identification:
- Email: `security@company.com` with subject `[INCIDENT] <brief description>`
- Slack: `#security-incidents` channel
- Phone (for critical incidents): extension 911 (internal)

Do not attempt to investigate or remediate without the security team's involvement.

## Step 3 — Preserve evidence
Do not delete emails, files, or logs related to the incident. Take screenshots of any suspicious messages, alerts, or activity before closing them. Document the timeline: when the user first noticed the issue, what they did, and when they reported it.

## Step 4 — Communication protocol
Do not communicate about the incident outside of secure channels. Do not post on public Slack channels or send details via personal email. All external communication (e.g., to customers or regulators) must be approved by Legal and the CISO.

## Step 5 — Post-incident review
Once the incident is contained, the security team will schedule a post-incident review within 5 business days. The support agent should provide a full timeline of actions taken.

## Risk tier: HIGH — never auto-resolve, always escalate to human
