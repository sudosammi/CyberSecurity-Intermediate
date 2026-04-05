# 🛡️ Blue Team Lab - Day 16: Rootkit Detection with rkhunter

Today, I moved beyond standard malware detection and learned how to hunt for Rootkits—advanced malware designed to hide its presence deep within the operating system (kernel level) and blind traditional security tools.

## 🧠 Core Concepts Mastered
- **Rootkits vs. Malware:** Understanding that while normal malware does damage, rootkits focus on deep persistence and stealth by replacing fundamental system binaries (like `ls` or `netstat`).
- **Baseline Profiling:** Using file property updates (`--propupd`) to take a snapshot of a clean system. Any subsequent deviation from this baseline triggers an alert.
- **Advanced Threat Hunting:** Running automated system checks to find hidden directories, suspicious kernel modules, and modified system binaries.

## 🛠️ Practical Commands Executed

### 1. Database & Baseline Update
Ensured the tool had the latest rootkit signatures and took a cryptographic baseline of the current file system.
```bash
sudo rkhunter --update
sudo rkhunter --propupd
