# 🛡️ Blue Team Lab - Day 11: Active Defense with Fail2Ban

Today, I automated the defense strategy I learned in Day 4 and Day 8. Instead of manually monitoring logs and blocking IPs, I deployed Fail2Ban to act as an automated intrusion prevention system (IPS).

## 🧠 Core Concepts Mastered
- **Intrusion Prevention (IPS):** Moving from just detecting threats to automatically taking action.
- **Jails & Filters:** Understanding how Fail2Ban maps log patterns to firewall actions.
- **Automated Mitigation:** Reducing the "Time to Respond" to a brute-force attack to near-zero.

## 🛠️ Practical Commands Executed

### 1. Configuration of SSH Jail
Created a local jail configuration (`jail.local`) to define the policy for SSH brute-force protection.
- **Max Retries:** 5 attempts.
- **Ban Time:** 1 Hour.
```bash
# Configuration snippet in /etc/fail2ban/jail.local
[sshd]
enabled = true
port    = ssh
logpath = %(sshd_log)s
maxretry = 5
bantime  = 1h
