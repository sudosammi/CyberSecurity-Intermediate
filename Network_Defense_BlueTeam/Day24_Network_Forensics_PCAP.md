# 🛡️ Blue Team Lab - Day 24: Network Forensics & Packet Analysis

Today, I completed the Forensics Triad by diving into Network Forensics. I learned how to capture, filter, and analyze live network traffic to identify malicious communication and data exfiltration.

## 🧠 Core Concepts Mastered
- **Packet Capture (PCAP):** The process of intercepting and logging traffic passing over a digital network.
- **Protocol Analysis:** Understanding how different protocols (TCP, UDP, HTTP) encapsulate data, and why unencrypted protocols are major security risks.
- **Deep Packet Inspection:** Looking beyond the packet headers and analyzing the actual payload (ASCII/Hex) to extract compromised data or malicious commands.

## 🛠️ Practical Commands Executed

### 1. Tool Installation
Installed the standard command-line packet analyzer on Arch Linux.
```bash
sudo pacman -S tcpdump
