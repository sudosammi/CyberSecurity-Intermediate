# 🛡️ Blue Team Lab - Day 23: Memory Forensics & Volatile Data Analysis

Today, I moved from Disk Forensics to Memory Forensics. I learned how to analyze a system's RAM to find "Fileless Malware" and active threats that never touch the hard drive. 

## 🧠 Core Concepts Mastered
- **Volatile vs. Non-Volatile Data:** Understanding that RAM contains live evidence (passwords, active connections, running code) that is lost upon reboot.
- **Memory Dumping:** The process of capturing the current state of a system's physical memory for offline forensic analysis.
- **Volatility Framework:** Using industry-standard tools to parse raw memory dumps and reconstruct the system's state at the time of the breach.

## 🛠️ Practical Methodology (Volatility 3)

### 1. Process Enumeration
Analyzing the process list from a memory dump to find hidden or injected malicious processes.
```bash
vol -f memory.dump linux.pslist
