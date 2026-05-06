import requests
import sys

def scan_takeover(subdomain_list):
    print(f"\n[*] Bhai, starting The Ghost Host: Subdomain Takeover Scanner...")
    print(f"[*] Scanning {len(subdomain_list)} subdomains for abandoned Cloud services!\n")
    print("==================================================")

    # The Hacker's Dictionary of Cloud Takeover Signatures
    # Agar website ke source code mein yeh exact lines milti hain, 
    # iska matlab third-party service delete ho chuki hai, but DNS abhi bhi mapped hai!
    signatures = {
        "AWS S3": "The specified bucket does not exist",
        "GitHub Pages": "There isn't a GitHub Pages site here.",
        "Heroku": "No such app",
        "Shopify": "Sorry, this shop is currently unavailable.",
        "Tumblr": "Whatever you were looking for doesn't currently exist at this address.",
        "WordPress": "Do you want to register",
        "Zendesk": "Help Center Closed"
    }

    found_vulns = 0

    for subdomain in subdomain_list:
        subdomain = subdomain.strip()
        if not subdomain: continue
        
        # Ensure it has http:// or https://
        target_url = subdomain if subdomain.startswith("http") else f"http://{subdomain}"
        
        try:
            # Short timeout, we just need to see the raw text response
            response = requests.get(target_url, timeout=5)
            text = response.text

            is_vulnerable = False

            # Check the response text against our Hacker Dictionary
            for provider, sig in signatures.items():
                if sig in text:
                    print(f"   [!!!] JACKPOT 🎯 CRITICAL SUBDOMAIN TAKEOVER FOUND!")
                    print(f"   [!!!] Subdomain : {subdomain}")
                    print(f"   [!!!] Provider  : {provider}")
                    print(f"   [!!!] Action    : Go to {provider}, register this exact name, and claim the domain!\n")
                    found_vulns += 1
                    is_vulnerable = True
                    break
            
            if not is_vulnerable:
                # To keep terminal clean, we just print a dot for secure domains
                print(".", end="", flush=True)

        except requests.exceptions.RequestException:
             # Just print a comma for timeouts/errors
             print(",", end="", flush=True)

    print("\n\n==================================================")
    if found_vulns > 0:
        print(f"[+] Scan Complete! Found {found_vulns} Subdomains ripe for Takeover. This is a P1/P2 Bug! 💸")
    else:
        print("[-] Scan Complete. All subdomains seem properly configured.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) < 2:
        print("Usage (Single Target): python3 takeover_scanner.py <subdomain>")
        print("Usage (Wordlist):      python3 takeover_scanner.py -l <subdomains.txt>")
        print("Example: python3 takeover_scanner.py support.target.com")
        sys.exit(1)

    if sys.argv[1] == "-l" and len(sys.argv) == 3:
        try:
            with open(sys.argv[2], 'r') as f:
                targets = f.readlines()
            scan_takeover(targets)
        except FileNotFoundError:
            print(f"[-] Error: Could not find file {sys.argv[2]}")
    else:
        scan_takeover([sys.argv[1]])
