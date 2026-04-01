# 🛡️ Blue Team Lab - Day 12: OS Hardening & SUID Hunting

Today, I shifted focus to internal Host-Based security, implementing the principle of "Defense in Depth". I learned how to lock down file permissions and hunt for potential Privilege Escalation vectors left by attackers.

## 🧠 Core Concepts Mastered
- **Linux Permission Matrix:** Understanding the Octal (e.g., `755`, `600`) and Symbolic (e.g., `-rwxr-xr-x`) representation of User, Group, and Public permissions.
- **The Principle of Least Privilege:** Using `chmod` to strip away unnecessary access from sensitive files, ensuring only authorized owners can interact with them.
- **SUID (Set-user Identification):** Understanding how attackers exploit the SUID bit to maintain persistent elevated (root) privileges.

## 🛠️ Practical Threat Hunting Executed

### 1. Locking Down Sensitive Data
Created a mock sensitive credential file and hardened it using `chmod 600`, completely cutting off Group and Public access.
```bash
echo "SECRET_KEY=123" > api_keys.txt
chmod 600 api_keys.txt
ls -l api_keys.txt
