import sys
from urllib.parse import urlparse, parse_qs

def analyze_oauth_url(url):
    print(f"\n[*] Bhai, analyzing OAuth Authorization URL...\n")
    
    # URL ko hisso mein todna (Parsing)
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    
    print("--------------------------------------------------")
    print(f"[*] Target Provider: {parsed_url.netloc}")
    print("[*] Extracted Parameters:")
    for key, value in params.items():
        print(f"    -> {key}: {value[0]}")
    print("--------------------------------------------------\n")

    print("[*] Commencing Vulnerability Checks...\n")
    vulnerabilities = 0

    # 1. Check for missing 'state' parameter (CSRF / Account Takeover)
    if 'state' not in params:
        print("   [!!!] JACKPOT 🎯 CRITICAL FLAW: 'state' parameter is MISSING!")
        print("   [!!!] Impact: The application is highly vulnerable to OAuth CSRF.")
        print("   [!!!] Attack: You can link your social account to a victim's account (Account Takeover)!")
        vulnerabilities += 1
    else:
        print("   [+] Good: 'state' parameter is present.")

    # 2. Check for missing or risky 'redirect_uri'
    if 'redirect_uri' not in params:
        print("   [!] WARNING: 'redirect_uri' is missing.")
        print("   [!] The provider might rely on pre-registered URIs, but if not, this is dangerous.")
    else:
        redirect_uri = params['redirect_uri'][0]
        print(f"   [*] Analyzing redirect_uri: {redirect_uri}")
        if not redirect_uri.startswith("https"):
            print("   [!] HIGH RISK: redirect_uri is using HTTP instead of HTTPS!")
            print("   [!] Impact: An attacker on the same network (e.g., Public WiFi) can steal the OAuth token.")
            vulnerabilities += 1
        
        # Checking for potential Open Redirect patterns
        if "localhost" in redirect_uri or "127.0.0.1" in redirect_uri:
             print("   [?] Weird: redirect_uri points to localhost. Might be a dev environment leak.")

    # 3. Check Response Type
    if 'response_type' in params:
        if params['response_type'][0] == 'token':
            print("\n   [!] WARNING: Implicit Flow ('response_type=token') is being used.")
            print("   [!] Impact: Access tokens are exposed in the browser URL (URL fragment). Deprecated and risky!")
            vulnerabilities += 1

    print("\n--------------------------------------------------")
    if vulnerabilities > 0:
        print(f"[+] Scan Complete! Found {vulnerabilities} potential OAuth misconfigurations. Time to write a report!")
    else:
        print("[+] Scan Complete! This OAuth implementation looks secure from surface-level analysis.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 oauth_scanner.py '<oauth_login_url>'")
        print("Example: python3 oauth_scanner.py 'https://accounts.google.com/o/oauth2/auth?client_id=123&redirect_uri=https://target.com/callback&response_type=code'")
        sys.exit(1)
        
    target_url = sys.argv[1]
    # Handle quotes in terminal input just in case
    target_url = target_url.strip("'\"")
    analyze_oauth_url(target_url)
