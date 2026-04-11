# 🛡️ Blue Team Lab - Day 22: Data Forensics & File Carving

Today, I explored the world of Digital Forensics. I learned that "deleted" does not mean "gone." As a Blue Teamer, I can recover malicious scripts or deleted logs left by an attacker using File Carving techniques.

## 🧠 Core Concepts Mastered
- **File Carving:** The process of reassembling files from raw disk sectors based on file signatures (Magic Numbers) rather than filesystem metadata.
- **Magic Numbers (Headers/Footers):** Unique hexadecimal signatures at the beginning of files (e.g., `FF D8 FF` for JPEG, `25 50 44 46` for PDF).
- **Forensic Integrity:** Understanding that data remains on the physical disk until it is overwritten by new data.

## 🛠️ Practical Commands Executed

### 1. Installation & Configuration
Installed Scalpel on Arch Linux and enabled specific file headers (PDF/JPG) in the configuration file.
```bash
sudo pacman -S scalpel
sudo nano /etc/scalpel/scalpel.conf
