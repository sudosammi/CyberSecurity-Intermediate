import requests
import sys

def scan_takeover(file_path):
    print(f"\n[*] Bhai, starting Subdomain Takeover Scan using list: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print("[-] Arre yaar, subdomains list file nahi mili!")
        return

    print(f"[*] Loaded {len(subdomains)} subdomains. Let's hunt for forgotten DNS records!\n")
    print("--------------------------------------------------")

    # The Hacker's Fingerprints Dictionary
    # Jab koi 3rd party service par app delete ho jata hai, toh woh ek specific error msg deti hai.
    # Hum bas unhi msgs ko pages par dhoondhenge!
    fingerprints = {
        "GitHub Pages": "There isn't a GitHub Pages site here.",
        "Heroku": "No such app",
        "AWS S3 Bucket": "The specified bucket does not exist",
        "Tumblr": "Whatever you were looking for doesn't currently exist at this address.",
        "WordPress": "Do you want to register",
        "Ghost": "The thing you were looking for is no longer here, or never was"
    }

    found_count = 0

    for sub in subdomains:
        if not sub.strip():
            continue
            
        # Ensure HTTP protocol is there
        if not sub.startswith("http"):
            target_url = f"http://{sub}"
        else:
            target_url = sub
            
        print(f"[*] Checking: {target_url}")
        
        try:
            # Request bhej rahe hain
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(target_url, headers=headers, timeout=5)
            
            # Fingerprints match karna
            for service, fingerprint in fingerprints.items():
                if fingerprint in response.text:
                    print(f"\n   [!!!] JACKPOT 🎯 SUBDOMAIN TAKEOVER POSSIBLE!")
                    print(f"   [!!!] Vulnerable Target: {target_url}")
                    print(f"   [!!!] Vulnerable Service: {service}")
                    print(f"   [!!!] Action: Go to {service} and claim this name ASAP!\n")
                    found_count += 1
                    break
                    
        except requests.exceptions.RequestException:
            # Agar timeout ya DNS resolution error aaye, toh ignore karke aage badho
            pass

    print("--------------------------------------------------")
    print(f"[+] Takeover Scan Complete, Bhai! Found {found_count} vulnerable subdomains.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 takeover_scanner.py <subdomains_list.txt>")
        print("Example: python3 takeover_scanner.py test_subs.txt")
        sys.exit(1)
        
    target_file = sys.argv[1]
    scan_takeover(target_file)
