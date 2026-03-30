#!/bin/bash

# Logo / Banner
echo "========================================="
echo "   🔥 SUDOSAMMI'S MASTER RECON PIPELINE 🔥"
echo "========================================="

DOMAIN=$1

# Check if user provided a domain
if [ -z "$DOMAIN" ]; then
    echo "[-] Arre Bhai, domain name toh do!"
    echo "[*] Usage: ./recon.sh <domain.com>"
    exit 1
fi

echo "[*] Target Locked: $DOMAIN"
echo "[*] Starting the automation process..."
echo "-----------------------------------------"

# STEP 1: Subdomain Enumeration
echo "[1] Running Day 53: Subdomain Hunter..."
# Python script ko call karte hain aur 'grep' aur 'awk' se sirf domain names filter karke save karte hain
python3 ../Day_53_Subdomain_Hunter/sub_enum.py $DOMAIN | grep " -> " | awk '{print $2}' > subdomains.txt
echo "[+] Saved raw subdomains to subdomains.txt"

# STEP 2: Alive Checking
echo -e "\n[2] Running Day 54: Alive Checker..."
python3 ../Day_54_Alive_Subdomain_Probe/alive_checker.py subdomains.txt | grep "ALIVE" | awk '{print $5}' | sed 's/http:\/\///;s/https:\/\///' > alive_subdomains.txt
echo "[+] Saved ALIVE targets to alive_subdomains.txt"

# STEP 3: Wayback URLs
echo -e "\n[3] Running Day 55: Wayback Machine Recon on Main Domain..."
# Abhi ke liye hum sirf main domain ke wayback URLs nikal rahe hain taaki script fast chale
python3 ../Day_55_Wayback_Discovery/wayback_recon.py $DOMAIN > wayback_urls.txt
echo "[+] Saved juicy URLs to wayback_urls.txt"

echo "-----------------------------------------"
echo "[+] BOOM! 🎯 Master Recon Complete!"
echo "[*] Fatafat 'ls' karke check karo, saari .txt files ready hain!"
