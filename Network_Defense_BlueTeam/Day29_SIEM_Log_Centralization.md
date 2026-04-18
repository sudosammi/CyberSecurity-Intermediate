# 🛡️ Blue Team Lab - Day 29: SIEM Theory & Log Centralization

Today, I reached the penultimate day of my Blue Team challenge. I transitioned from single-host analysis to enterprise-level network monitoring by learning the theory behind SIEM (Security Information and Event Management) and the ELK Stack.

## 🧠 Core Concepts Mastered
- **Log Centralization:** The absolute necessity of aggregating logs from hundreds of servers, firewalls, and endpoints into a single, searchable database to correlate attack patterns.
- **The ELK Stack:** Understanding the industry-standard logging architecture:
  - **Elasticsearch:** The search and analytics engine (Database).
  - **Logstash:** The data processing pipeline (Log Collection & Parsing).
  - **Kibana:** The data visualization dashboard (UI/Graphs).
- **Log Forwarding:** Understanding how endpoint agents transmit local events to a central collection server using protocols like syslog (Port 514).

## 🛠️ Practical Configurations Executed

### 1. Log Forwarder Installation
Installed `rsyslog` on Arch Linux to act as the agent responsible for transmitting logs out of the local system.
```bash
sudo pacman -S rsyslog

