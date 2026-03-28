# 🛡️ Blue Team Lab - Day 8: Week 1 Capstone (Incident Response)

Today, I combined all the concepts learned in Week 1 (Firewalls, IDS, Logs, and FIM) to simulate a full Incident Response (IR) lifecycle. I acted as a SOC Analyst responding to a simulated "Midnight Breach".

## 🧠 Core IR Phases Executed
1. **Detection & Analysis:** Used Linux log analysis tools (`grep`, `tail`, `wc`) to identify a brute-force attack on SSH and extract the malicious IP address.
2. **Damage Assessment:** Leveraged File Integrity Monitoring (`sha256sum`) to check if critical system configurations were tampered with during the breach window.
3. **Containment & Eradication:** Deployed raw `iptables` rules to immediately drop all network traffic from the attacker's source IP, cutting off their access.

## 🛠️ The Defensive Playbook (Commands Used)

### Phase 1: Identifying the Attack
```bash
sudo grep "Failed password" /var/log/auth.log | tail -n 10
