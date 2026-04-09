# 🛡️ Blue Team Lab - Day 20: Modern Log Auditing with journalctl

Today, I transitioned my environment to Arch Linux. This required a shift in my threat hunting methodology. Since modern Linux distributions (like Arch) rely heavily on `systemd`, traditional plaintext log files (`/var/log/auth.log`) are replaced by a centralized, binary logging system queried via `journalctl`.

## 🧠 Core Concepts Mastered
- **Systemd Journal:** Understanding the modern, centralized approach to Linux logging where kernel and user-space logs are unified.
- **Service-Specific Auditing:** Moving away from `grep` and using native `journalctl` flags to isolate logs for critical services like SSH.
- **Time-Bound Forensics:** Leveraging natural language time queries to isolate security events during a specific breach window.

## 🛠️ Practical Threat Hunting Executed

### 1. Live System Monitoring
Used the follow flag to monitor system events and kernel messages in real-time.
```bash
journalctl -f
