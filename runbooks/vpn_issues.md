# Runbook: VPN Issues

## Symptoms
User cannot connect to VPN, VPN drops frequently, or VPN client fails to launch.

## Step 1 — Basic restart
Ask the user to fully quit the VPN client (not just disconnect) and relaunch it. If the issue persists, restart their machine and try again.

## Step 2 — Check certificate expiry
VPN certificates expire every 90 days. Ask the user to navigate to `portal.company.com/vpn-renew` and follow the on-screen renewal steps. After renewal, restart the VPN client.

## Step 3 — Verify firewall and network
Ensure the user is not on a network that blocks VPN ports (UDP 1194, TCP 443). Ask them to try connecting from a different network (e.g., mobile hotspot). If VPN works on the hotspot, the issue is with their primary network's firewall.

## Step 4 — Reinstall the VPN client
If steps 1–3 do not resolve the issue, uninstall the VPN client completely, download the latest installer from `portal.company.com/vpn-download`, and reinstall.

## Step 5 — Escalate to network team
If none of the above steps work, collect the following and escalate to the network team:
- VPN client version
- Operating system and version
- Screenshot or copy of the error message
- Result of `ping vpn.company.com` from the user's terminal

## Risk tier: LOW (unless the user reports credentials may be compromised — escalate to HIGH in that case)
