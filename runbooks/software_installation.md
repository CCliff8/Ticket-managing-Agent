# Runbook: Software Installation

## Symptoms
User requests installation of software, or existing software fails to install/update.

## Step 1 — Check approved software catalog
Before installing anything, verify the requested software is on the approved catalog at `portal.company.com/software-catalog`. If the software is not listed, do not proceed — direct the user to submit a software approval request via `helpdesk.company.com/new-request`.

## Step 2 — Check license availability
For licensed software (e.g., Adobe, Microsoft Office), check the license dashboard at `portal.company.com/licenses` to confirm an available seat. Assign a license to the user before installation.

## Step 3 — Admin rights requirement
Most installations require admin rights. Use the remote deployment tool at `admin.company.com/deploy` to push the installer to the user's machine. Do not share admin credentials with users.

## Step 4 — User-initiated installation
For software in the self-service catalog, direct users to the Company App Store at `portal.company.com/app-store`. Users can install approved self-service apps without IT involvement.

## Step 5 — Verify installation
After deployment, confirm with the user that the application launches correctly. Check for any missing dependencies or activation steps in the software's install guide linked in the catalog.

## Risk tier: LOW for catalog software | MEDIUM for new software approval requests
