import requests
import sys
import concurrent.futures

def print_banner():
    print("""
    █████╗ ██╗   ██╗████████╗ ██████╗ ██████╗ ██╗    ██╗███╗   ██╗
   ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔══██╗██║    ██║████╗  ██║
   ███████║██║   ██║   ██║   ██║   ██║██████╔╝██║ █╗ ██║██╔██╗ ██║
   ██╔══██║██║   ██║   ██║   ██║   ██║██╔═══╝ ██║███╗██║██║╚██╗██║
   ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║     ╚███╔███╔╝██║ ╚████║
   ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝
            [ The 100-Day Capstone Recon Framework ]
    """)

def check_headers(url):
    print("\n[*] Scanning Security Headers...")
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        
        missing = []
        if 'X-Frame-Options' not in headers: missing.append("X-Frame-Options (Clickjacking possible)")
        if 'Strict-Transport-Security' not in headers: missing.append("Strict-Transport-Security (HSTS missing)")
        if 'Content-Security-Policy' not in headers: missing.append("Content-Security-Policy (XSS easier)")
        
        if missing:
            for m in missing:
                print(f"   [-] Missing: {m}")
        else:
            print("   [+] All basic security headers are present.")
            
        print(f"   [+] Server Banner: {headers.get('Server', 'Unknown/Hidden')}")
    except requests.exceptions.RequestException:
        print("   [!] Failed to connect for header check.")

def check_sensitive_files(url):
    print("\n[*] Hunting for Exposed Sensitive Files...")
    files_to_check = [
        ".env", ".git/config", "robots.txt", "sitemap.xml", 
        "phpinfo.php", "backup.zip", ".ssh/id_rsa"
    ]
    
    base_url = url.rstrip('/')
    
    def fetch_file(file_path):
        target = f"{base_url}/{file_path}"
        try:
            res = requests.get(target, timeout=5)
            if res.status_code == 200 and "<html" not in res.text[:20].lower():
                return f"   [!!!] JACKPOT 🎯 Found: {target} (Size: {len(res.text)} bytes)"
        except:
            pass
        return None

    # Multi-threading for fast discovery
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_file, files_to_check)
        
        found_any = False
        for result in results:
            if result:
                print(result)
                found_any = True
                
        if not found_any:
            print("   [-] No common sensitive files exposed.")

def start_autopwn(target_url):
    print_banner()
    print(f"[*] Target initialized: {target_url}")
    print("==================================================")
    
    check_headers(target_url)
    check_sensitive_files(target_url)
    
    print("\n==================================================")
    print("[+] AutoPwn Recon Complete!")
    print("[+] Master Level Unlocked! Go collect those bounties! 💸💀")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 autopwn_master.py <Target_URL>")
        print("Example: python3 autopwn_master.py https://target.com")
        sys.exit(1)
        
    target = sys.argv[1]
    if not target.startswith("http"):
        target = "https://" + target
        
    start_autopwn(target)
