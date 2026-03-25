# 🛡️ Blue Team Lab - Day 5: Honeypots & Cyber Deception

Today, I moved from passive defense to active deception. I learned how to set up a Honeypot—a decoy system designed to lure cyberattackers, waste their time, and gather threat intelligence.

## ✅ Tasks Completed:

### 1. Creating a Decoy Banner
Created a fake, enticing banner to trick attackers into thinking they found a valuable corporate server.
- **Command:** `echo Top Secret Corporate FTP Server > fake_banner.txt`

### 2. Setting the Trap with Netcat
Configured `netcat` to listen on the standard FTP port (21), serve the decoy banner, and log any incoming connections silently in the background.
- **Command:** `nc -nlvp 21 < fake_banner.txt >> honeypot_logs.txt`

### 3. Capturing Threat Intel
Successfully tested the trap and analyzed the log file to capture the attacker's source IP address and connection details.
- **Log Captured:** `connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 32848`
- **Result:** Confirmed the honeypot correctly logs the threat actor's IP and Source Port.

---
*Progress by: sudosammi* 🚀
*Note to self: The best way to understand an attacker is to let them think they are winning while you watch their every move!*
