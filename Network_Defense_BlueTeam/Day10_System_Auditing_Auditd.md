# 🛡️ Blue Team Lab - Day 10: Kernel-Level Auditing with Auditd

Today, I explored deep system monitoring using the Linux Audit Daemon (`auditd`). While syslog provides general event logging, `auditd` hooks directly into the kernel to provide granular, forensic-level details about file access and system calls.

## 🧠 Core Concepts Mastered
- **Auditd Architecture:** A userspace utility that interacts directly with the kernel's audit framework.
- **Watch Rules:** Configuring rules to monitor specific files or directories for Read, Write, Execute, or Attribute changes (RWXA).
- **Ausearch:** The native tool used to query and filter the complex audit logs generated in `/var/log/audit/audit.log`.

## 🛠️ Practical Configuration & Threat Hunting

### 1. Deploying the Watch Rule
Set up a monitor on the critical `/etc/passwd` file, looking specifically for 'write' or 'attribute' modifications. Assigned a unique key (`passwd_monitor`) for easy retrieval.
```bash
sudo auditctl -w /etc/passwd -p wa -k passwd_monitor
