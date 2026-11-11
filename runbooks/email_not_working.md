# Runbook: Email Not Working

## Symptoms
User cannot send or receive emails, email client shows errors, or emails are not arriving.

## Step 1 — Check mail server status
Before troubleshooting the client, check the mail server status page at `status.company.com`. If there is an ongoing incident, inform the user and provide the estimated resolution time.

## Step 2 — Verify email client settings
Ensure the client is configured with the correct server settings:
- **IMAP**: `mail.company.com`, port 993, SSL/TLS
- **SMTP**: `smtp.company.com`, port 587, STARTTLS
- **Username**: full email address (e.g., `user@company.com`)

For Outlook, direct users to `portal.company.com/email-setup` for the auto-configuration tool.

## Step 3 — Check mailbox quota
Each mailbox has a 10 GB quota. A full mailbox blocks incoming mail. Check usage in the admin console at `admin.company.com/mailboxes`. If the mailbox is over 90% full, advise the user to delete or archive old emails, or request a quota increase.

## Step 4 — Spam filter false positives
If specific emails are not arriving, they may be caught by the spam filter. Ask the user to check their spam/junk folder. To whitelist a sender, use the mail admin portal at `admin.company.com/mail-filters`.

## Step 5 — Re-add account
If the above steps fail, remove the email account from the client and re-add it using the setup guide at `portal.company.com/email-setup`.

## Risk tier: LOW for standard email issues | MEDIUM if the user suspects their account has been accessed by someone else
