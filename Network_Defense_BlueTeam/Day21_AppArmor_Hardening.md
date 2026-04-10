# 🛡️ Blue Team Lab - Day 21: Mandatory Access Control (AppArmor)

Today, I explored Application Hardening and Sandboxing using AppArmor on my Arch Linux system. I learned that restricting user permissions is not enough; we must also restrict what individual applications and services are allowed to do.

## 🧠 Core Concepts Mastered
- **Mandatory Access Control (MAC):** A security model where the OS enforces strict boundaries on applications, regardless of the user running them.
- **The Concept of Sandboxing:** Confining a compromised application to a limited set of files and capabilities so the attacker cannot pivot to the rest of the system.
- **Enforce vs. Complain Modes:**
  - `Complain`: The profile allows the action but logs the violation (useful for building rules without breaking the app).
  - `Enforce`: The profile actively blocks any action outside its allowed ruleset.

## 🛠️ Practical Commands Executed

### 1. Installation & Initialization
Installed the AppArmor utility suite using the Arch package manager.
```bash
sudo pacman -S apparmor apparmor-utils
sudo systemctl enable --now apparmor
