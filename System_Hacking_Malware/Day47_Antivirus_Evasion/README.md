# Day 47: Antivirus Evasion (FUD Concepts)

To make a payload FUD (Fully Undetectable), a penetration tester must understand how Blue Teams and Antivirus (AV) softwares detect threats.

## 🛡️ How Antivirus Detects Malware:
1. **Signature-Based Detection:** Every file has a unique hash (MD5/SHA-256). AVs compare the file's hash against a massive database of known malware. If it matches, the file is instantly blocked.
2. **Heuristic/Behavioral Analysis:** If the hash is new, the AV monitors what the program *does*. If a simple calculator app tries to open a reverse shell on Port 4444, the AV flags this abnormal behavior and kills the process.
3. **Sandboxing:** The AV opens suspicious files in a safe, isolated virtual environment (Sandbox) first. It watches the execution for a few seconds before letting it run on the real OS.

## 🥷 How Red Teams Bypass Antivirus:
1. **Obfuscation & Crypters:** Changing the source code structure, variables, and encrypting the payload (e.g., using Base64, AES, or XOR). This changes the file's hash completely, bypassing Signature detection.
2. **Execution Delays (Sleep Timers):** Adding a `time.sleep(600)` in the script. The AV Sandbox only waits for a few seconds to analyze a file. If the malware sleeps for 10 minutes, the Sandbox assumes it's safe and lets it pass.
3. **Fileless Execution (In-Memory):** Instead of saving an `.exe` or `.py` to the hard drive, advanced hackers inject the malicious code directly into the computer's RAM. Since there is no file on the disk, the AV has nothing to scan!
