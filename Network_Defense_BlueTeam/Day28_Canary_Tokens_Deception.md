# 🛡️ Blue Team Lab - Day 28: Cyber Deception with Canary Tokens

Today, I moved into the domain of "Active Defense" and "Cyber Deception." I learned that a good defender doesn't just build walls; they also set traps (Honeypots) to identify an intruder the moment they touch a sensitive-looking asset.

## 🧠 Core Concepts Mastered
- **Deception Technology:** Using fake assets (tokens/files) to lure attackers into revealing their presence.
- **Canary Tokens:** Small, unique tracking identifiers embedded in documents, folders, or API keys that trigger an alert when accessed.
- **Early Warning System:** Reducing "Dwell Time" (the time an attacker stays in a system undetected) by setting digital tripwires.

## 🛠️ Practical Implementation

### 1. Token Generation & Deployment
Utilized CanaryTokens technology to generate a weaponized "Bait" document.
- **Token Type:** MS Word / Excel Document.
- **Trigger:** Webhook-based alert on file 'Open' event.

### 2. Strategic Placement
Deployed the bait file in a directory that would typically be a high-value target for an attacker (e.g., `/home/user/Documents/Passwords/`).

### 3. Incident Notification Test
Simulated a breach by opening the tokenized file.
- **Result:** Successfully received an out-of-band Email alert containing the attacker's Source IP, User-Agent, and Geolocation data.

---
*Progress by: sudosammi* 🚀
*Note to self: The best way to catch a thief is to leave a wallet on the table that screams 'I'm here!' when touched.*
