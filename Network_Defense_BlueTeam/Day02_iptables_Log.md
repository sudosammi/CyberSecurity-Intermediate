# 🛡️ Blue Team Lab - Day 2: Advanced Packet Filtering (iptables)

Today, I dived deeper into network security by exploring the underlying engine of Linux firewalls: `iptables`. While UFW is great for quick setups, `iptables` provides granular, kernel-level control over network traffic.

## ✅ Tasks Completed:

### 1. Understanding iptables Architecture
- Learned about the **Filter Table** (the default table used to accept or drop packets).
- Understood the core chains: 
  - `INPUT` (traffic coming to the machine)
  - `OUTPUT` (traffic leaving the machine)
  - `FORWARD` (traffic routed through the machine)

### 2. Writing Raw Firewall Rules
- **Blocking a Specific Malicious IP:**
  ```bash
  sudo iptables -A INPUT -s 192.168.1.100 -j DROP
