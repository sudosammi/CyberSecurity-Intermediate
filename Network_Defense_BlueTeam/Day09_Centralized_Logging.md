# 🛡️ Blue Team Lab - Day 9: Centralized Logging & SIEM Foundations

Starting Week 2, I transitioned from single-host defense to enterprise-level monitoring concepts. I learned the foundation of SIEM (Security Information and Event Management) by configuring a centralized logging server.

## 🧠 Core Concepts Mastered
- **The SIEM Problem:** Managing logs on individual servers is unscalable in an enterprise. 
- **The Solution (Centralized Logging):** Configuring all endpoints to forward their logs to a single, secure master server (Control Room) for centralized analysis and correlation.
- **Rsyslog Protocol:** The standard utility for forwarding log messages in an IP network using UDP/TCP port 514.

## 🛠️ Practical Configuration Executed

### 1. Configuring the Log Receiver
Edited `/etc/rsyslog.conf` to load the `imudp` module and listen on port 514, transforming the local machine into a log aggregation server.
```bash
module(load="imudp")
input(type="imudp" port="514")
