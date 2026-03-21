# 🛡️ Blue Team Lab - Day 1: Host Hardening

Today I started my defensive security module to counter the network attacks I previously learned (MITM, ARP Spoofing).

## ✅ Tasks Completed:

### 1. Static ARP Configuration (Anti-MITM)
Prevented ARP Spoofing by hardcoding the gateway's MAC address.
- **Command:** `sudo ip neigh add 10.0.2.2 lladdr 52:55:0a:00:02:02 dev eth0 nud permanent`
- **Why:** This stops the OS from accepting fake ARP replies from an attacker.

### 2. ARP Monitoring (IDS)
Installed and configured `arpwatch` to monitor network anomalies.
- **Monitoring Tool:** `journalctl -u arpwatch -f`

### 3. Firewall Implementation (UFW)
Locked down the system using a "Least Privilege" approach.
- **Policy:** Default Deny Incoming, Default Allow Outgoing.
- **Rules:** Explicitly allowed SSH (Port 22).
- **Status:** Active & Hardened.

---
*Progress by: sudosammi* 🚀
