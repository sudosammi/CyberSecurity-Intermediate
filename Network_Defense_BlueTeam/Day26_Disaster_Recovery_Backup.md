# 🛡️ Blue Team Lab - Day 26: Automated Backup & Disaster Recovery (DR)

Today, I implemented the ultimate safety net for any system: an Automated Backup & Recovery plan. In cybersecurity, we assume the system will eventually fail or be breached; Disaster Recovery ensures business continuity despite such events.

## 🧠 Core Concepts Mastered
- **RPO & RTO:** Understanding Recovery Point Objective (how much data loss is acceptable) and Recovery Time Objective (how fast can we get back online).
- **Incremental Backups with Rsync:** Using `rsync` to synchronize only the changes in files, drastically reducing bandwidth and storage overhead.
- **Automation via Cron:** Scheduling backup tasks to run during low-traffic hours without manual intervention.

## 🛠️ Practical Implementation Executed

### 1. Automation Scripting
Created a bash script to aggregate critical configuration and web directories, creating timestamped backup snapshots.
```bash
#!/bin/bash
rsync -avz /etc /var/www/html /path/to/backup/$(date +%F)
