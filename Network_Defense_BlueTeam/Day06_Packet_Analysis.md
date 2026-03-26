# 🛡️ Blue Team Lab - Day 6: Deep Packet Inspection with Tshark

Today, I learned how to perform deep packet inspection (DPI) from the command line. While my Python scripts taught me how to sniff packets offensively, using industry-standard tools like `tshark` (the CLI version of Wireshark) allows me to analyze network anomalies defensively.

## 🧠 Core Concepts Mastered
- **Packet Sniffing:** Capturing live data packets traversing the network interface.
- **BPF Syntax:** Using Berkeley Packet Filters to capture only relevant traffic (e.g., specific ports or protocols).
- **PCAP Analysis:** Saving network traffic to `.pcap` files for forensic analysis later.

## 🛠️ Practical Commands Executed

### 1. Live Interface Sniffing
Captured all incoming and outgoing packets on the primary interface.
```bash
sudo tshark -i eth0
