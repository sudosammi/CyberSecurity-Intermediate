# 🛡️ CyberSecurity Intermediate Framework
Welcome to my Intermediate Cybersecurity learning journey! This repository contains advanced network security scripts, focusing on packet sniffing and traffic analysis.

## 📁 Repository Structure
Currently, this repo includes:
- **Day33_HTTPS_Detection**: A Python script using Scapy to detect and distinguish between HTTP and HTTPS traffic in real-time.

## 🛠️ Features (Day 33)
- **IP Layer Detection**: Automatically identifies IP packets to avoid common Scapy errors.
- **Traffic Classification**: Separates standard web traffic (Port 80) from encrypted traffic (Port 443).
- **Real-time Sniffing**: Intercepts packets directly from the network interface.

## 🚀 How to Run
1. Clone the repository.
2. Navigate to the specific day's folder.
3. Run the script with root privileges:
   ```bash
   sudo python3 mitm_master.py
