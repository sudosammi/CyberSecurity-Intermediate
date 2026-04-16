# 🛡️ Blue Team Lab - Day 27: Host-Based Intrusion Detection (AIDE)

Today, I leveled up my File Integrity Monitoring (FIM) skills. Moving beyond single-file hashing, I deployed AIDE (Advanced Intrusion Detection Environment) to monitor the entire file system's integrity against unauthorized modifications.

## 🧠 Core Concepts Mastered
- **Host-Based IDS (HIDS):** Understanding how to monitor the internal OS layer, ensuring that system binaries and configuration files remain untampered.
- **Cryptographic Baselining:** Generating a master database containing the hashes, permissions, and inodes of a known-good (clean) system state.
- **Automated Auditing:** Comparing the current live state of the filesystem against the cryptographic baseline to detect Modifications, Additions, or Deletions.

## 🛠️ Practical Configurations Executed

### 1. Installation & Initialization
Installed AIDE on Arch Linux and generated the initial cryptographic baseline database.
```bash
sudo pacman -S aide
sudo aide --init
sudo cp /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz
