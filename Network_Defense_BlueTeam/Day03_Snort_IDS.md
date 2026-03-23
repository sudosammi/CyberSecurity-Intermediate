# 🛡️ Blue Team Lab - Day 3: Intrusion Detection with Snort (IDS)

Today, I shifted my focus from preventing attacks (Firewalls) to detecting them (Intrusion Detection Systems) using Snort. I learned how to inspect packet payloads and write custom alerts.

## ✅ Tasks Completed:

### 1. Snort Installation & Configuration
- Installed Snort to monitor network traffic at the packet level.
- Configured the network interface (`eth0`) for active network sniffing from a defensive perspective.

### 2. Writing Custom IDS Rules
- Created a custom rule in `/etc/snort/rules/local.rules` to detect ICMP (Ping) Scans.
- **Custom Rule:**
  ```text
  alert icmp any any -> any any (msg:"Ping (ICMP) Scan Detected!"; sid:1000001; rev:1;)
