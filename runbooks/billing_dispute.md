# Runbook: Billing Dispute

## Symptoms
User reports an unexpected charge, incorrect invoice amount, subscription issue, or requests a refund.

## Step 1 — Verify account ownership
Before discussing any billing details, verify the user's identity:
- Confirm name, email address on the account, and last four digits of the payment method on file.
- Never share billing details without completing this verification.

## Step 2 — Identify dispute type

**Unauthorized charge**: User did not make the purchase. Flag for the fraud team immediately at `fraud@company.com`. Do not issue a refund directly — the fraud team handles these.

**Subscription issue**: User was charged for a subscription they believed was cancelled. Check the subscription history in the billing dashboard at `billing.company.com/admin`. If a cancellation was submitted but billing continued, issue a refund for the overcharged amount.

**Invoice error**: Amount on the invoice does not match the expected price. Review the invoice line items. If a system error is confirmed, escalate to the billing engineering team with the invoice ID.

## Step 3 — Refund process
Approved refunds are processed within 5–7 business days to the original payment method. Issue refunds via `billing.company.com/refunds`. Refunds above $500 require manager approval.

## Step 4 — Document and close
Log all dispute details in the billing case management system. Send the user a confirmation email with the resolution and expected refund timeline.

## Risk tier: MEDIUM for standard disputes | HIGH for unauthorized charges (potential fraud)
