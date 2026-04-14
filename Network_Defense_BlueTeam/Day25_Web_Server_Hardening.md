# 🛡️ Blue Team Lab - Day 25: Web Server Hardening & Rate Limiting

Today, I focused on securing the external perimeter by hardening a live Nginx Web Server. Public-facing web servers are the most common entry points for attackers, making configuration hardening and DDoS mitigation absolute priorities.

## 🧠 Core Concepts Mastered
- **Server Identity Masking:** Disabling server tokens to prevent attackers from footprinting the exact version of the web server, which stops automated exploit scanners.
- **Rate Limiting (Leaky Bucket Algorithm):** Protecting the server application from Application-Layer (Layer 7) DDoS attacks and brute-force attempts by restricting the number of HTTP requests a single IP can make per second.
- **Zone and Burst Configuration:** Managing memory zones for tracking IPs and allowing small legitimate bursts of traffic while dropping malicious floods.

## 🛠️ Practical Configurations Executed

### 1. Nginx Installation & Configuration
Installed Nginx on Arch Linux and modified the core `/etc/nginx/nginx.conf` file.

### 2. Implemented Security Controls
Added the following directives to the `http` and `server` blocks:
```nginx
# Hide Nginx version from HTTP headers
server_tokens off;

# Define the rate limit zone (5 requests per second per IP)
limit_req_zone $binary_remote_addr zone=mylimit:10m rate=5r/s;

# Apply the limit with a burst queue of 10
limit_req zone=mylimit burst=10 nodelay;
