# 🛡️ Blue Team Lab - Day 4: Log Analysis & Threat Hunting

Today, I learned that a Blue Teamer's greatest weapon is the ability to read and analyze system logs. Attackers always leave footprints, and I learned how to hunt for them using Linux command-line utilities.

## 🧠 Core Concepts Mastered
- **Log Location:** In Debian-based systems (like Kali/Ubuntu), authentication logs are stored securely in `/var/log/auth.log`.
- **The CLI Toolkit:** Used `tail`, `grep`, and `wc` to parse massive log files quickly.

## 🛠️ Practical Threat Hunting Commands

### 1. Live Authentication Monitoring
Watched the authentication logs in real-time to spot active login attempts.
```bash
sudo tail -f /var/log/auth.log
