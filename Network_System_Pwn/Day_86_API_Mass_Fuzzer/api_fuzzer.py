import requests
import concurrent.futures
import sys
from datetime import datetime

def check_endpoint(base_url, endpoint):
    target_url = f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) API-Hunter/2.0",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(target_url, headers=headers, timeout=5)
        status = response.status_code
        
        # We are interested in finding endpoints that exist!
        # 200 = OK, 401 = Needs Auth, 403 = Forbidden, 500 = Server Error (Buggy Endpoint!)
        if status in [200, 201, 401, 403, 500]:
            return target_url, status, len(response.text)
    except requests.exceptions.RequestException:
        pass
    return None, None, None

def fuzz_api(base_url):
    print(f"\n[*] Bhai, starting Shadow Mapper: Mass API Endpoint Fuzzer on -> {base_url}")
    print("[*] Launching multi-threaded dictionary attack to uncover hidden APIs...\n")
    print("==================================================")

    # The Hacker's API Dictionary (Most common forgotten/hidden endpoints)
    api_wordlist = [
        "api/v1/users", "api/v2/users", "api/v1/admin", "api/v1/dashboard",
        "api/internal/debug", "api/dev/test", "graphql", "api/graphql",
        "api/v1/config", "swagger-ui.html", "api/docs", "api-docs",
        "v1/auth/login", "api/v1/payment", "api/beta/features",
        "api/v1/backup", "api/v1/export", "api/v1/logs"
    ]

    print(f"[*] Loaded {len(api_wordlist)} high-value API payloads.")
    print("[*] Firing threads... \n")

    start_time = datetime.now()
    found_endpoints = 0

    # Multi-threading for speed!
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(check_endpoint, base_url, path): path for path in api_wordlist}
        
        for future in concurrent.futures.as_completed(futures):
            url, status, length = future.result()
            if url:
                found_endpoints += 1
                if status == 200:
                    print(f"   [!!!] JACKPOT 🎯 [HTTP 200 OK] -> {url} (Length: {length})")
                    print("   [!!!] Data is publicly accessible! Open it in browser now.")
                elif status == 401 or status == 403:
                    print(f"   [!] LOCKED 🔒 [HTTP {status}] -> {url}")
                    print("   [!] Endpoint exists but requires authentication. Try IDOR or Token bypassing next.")
                elif status == 500:
                    print(f"   [?] BUGGY 🐛 [HTTP 500] -> {url}")
                    print("   [?] Server crashed on request. Might be vulnerable to injections!")

    end_time = datetime.now()
    print("\n==================================================")
    print(f"[*] Scan completed in: {end_time - start_time}")
    
    if found_endpoints > 0:
        print(f"[+] Total Hidden Endpoints Found: {found_endpoints}. Bug Bounty phase initiated! 💸")
    else:
        print("[-] No hidden API endpoints found from our dictionary. Target is clean or heavily filtered.")

if __name__ == "__main__":
    # Disable insecure request warnings for HTTPS
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 api_fuzzer.py <Target_Base_URL>")
        print("Example: python3 api_fuzzer.py https://api.target.com")
        sys.exit(1)
        
    target = sys.argv[1]
    if not target.startswith("http"):
        target = "https://" + target
        
    fuzz_api(target)
