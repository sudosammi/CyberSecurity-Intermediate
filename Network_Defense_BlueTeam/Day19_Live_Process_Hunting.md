# 🛡️ Blue Team Lab - Day 19: Live Process & Network Hunting

Today, I shifted focus to live system analysis. Having a fresh OS meant setting up my Git environment again, which served as a great reminder of configuration management. After that, I learned how to identify and terminate active, running threats in system memory.

## 🧠 Core Concepts Mastered
- **Live Memory/Process Analysis:** Moving from static file analysis to dynamic analysis of what is currently executing in the CPU/RAM.
- **Socket Statistics (`ss`):** Using network utilities to map open ports to their specific Process IDs (PIDs).
- **Process Termination:** Using the `kill -9` (SIGKILL) signal to forcefully terminate a confirmed malicious process that is communicating externally.

## 🛠️ Practical Threat Hunting Executed

### 1. Identifying the Anomalous Network Connection
Audited all active, listening TCP/UDP ports to find unauthorized backdoors.
```bash
sudo ss -tulpn
