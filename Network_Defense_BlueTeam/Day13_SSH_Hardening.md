# 🛡️ Blue Team Lab - Day 13: SSH Server Hardening

Today, I focused on securing the most targeted service on any Linux server: SSH. I learned how to modify the SSH daemon configuration to drastically reduce the attack surface and prevent common automated attacks.

## 🧠 Core Concepts Mastered
- **Security by Obscurity (Port Changing):** Moving SSH away from the default Port 22 to evade mass automated botnet scanners.
- **Root Login Disabling:** Preventing direct `root` access via SSH. Attackers must now guess a standard username *and* its password, and then attempt privilege escalation, adding multiple layers of difficulty.
- **Connection Limitations:** Lowering `MaxAuthTries` to drop connections quickly during a brute-force attempt.

## 🛠️ Practical Commands & Configurations Executed

### 1. Pre-requisite: Firewall Update
Allowed the new custom SSH port through UFW *before* restarting the service to prevent administrative lockouts.
```bash
sudo ufw allow 2222/tcp
sudo ufw reload
