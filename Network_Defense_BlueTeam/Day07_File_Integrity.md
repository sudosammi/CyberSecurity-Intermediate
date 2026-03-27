# 🛡️ Blue Team Lab - Day 7: File Integrity Monitoring (FIM)

Today, I explored host-based defense by learning File Integrity Monitoring. I learned how to use cryptographic hashing to detect unauthorized modifications to critical system files.

## 🧠 Core Concepts Mastered
- **Cryptographic Hashing (SHA-256):** Generating a unique, fixed-size string (fingerprint) for a file. Even the slightest modification changes the hash entirely.
- **Integrity Verification:** Comparing a known good hash against the current state of a file to detect tampering or backdoor injections by threat actors.

## 🛠️ Practical Commands Executed

### 1. Generating a File Baseline
Created a baseline hash for a critical configuration file and stored it securely.
```bash
sha256sum system_config.txt > safe_hash.txt
