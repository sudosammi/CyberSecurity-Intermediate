import requests
import re
import sys
from urllib.parse import urljoin

def hunt_api_keys(url):
    print(f"\n[*] Bhai, starting JS Recon on: {url}")
    print("[*] Fetching the main webpage to find .js files...\n")
    
    try:
        # Step 1: Main page ka source code nikalo
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Step 2: Regex se saare .js links dhoondho
        # Yeh pattern `<script src="...">` ke andar se js file ka naam nikalta hai
        js_links = re.findall(r'<script\s+.*?src=["\'](.*?\.js)["\']', response.text)
        
        if not js_links:
            print("[-] Arre yaar, koi JavaScript file nahi mili is page par.")
            return

        print(f"[+] Found {len(js_links)} JavaScript files. Commencing the hunt!\n")
        print("--------------------------------------------------")

        # Step 3: Hacker's Dictionary (Regex Patterns for Keys)
        # Yeh patterns un keys ko dhoondhte hain jo specifically dikhti hain
        key_patterns = {
            "Google API Key": r"AIza[0-9A-Za-z-_]{35}",
            "Amazon AWS Access Key": r"AKIA[0-9A-Z]{16}",
            "Stripe Standard API": r"sk_live_[0-9a-zA-Z]{24}",
            "Generic API/Secret Key": r"['\"][A-Za-z0-9-_]{32,45}['\"]"
        }

        # Step 4: Har JS file ko open karo aur keys dhoondho
        for js_path in js_links:
            # Agar link aadha hai (jaise /script.js), toh usko pura URL banao
            full_js_url = urljoin(url, js_path)
            print(f"[*] Scanning: {full_js_url}")
            
            try:
                js_response = requests.get(full_js_url, headers=headers, timeout=5)
                js_code = js_response.text
                
                # Regex patterns run karo
                for key_name, pattern in key_patterns.items():
                    matches = re.findall(pattern, js_code)
                    if matches:
                        for match in set(matches): # set() se duplicates hat jayenge
                            print(f"\n   [!!!] JACKPOT 🎯 {key_name} FOUND!")
                            print(f"   [!!!] Key: {match}")
                            print(f"   [!!!] Leaked in: {full_js_url}\n")
                            
            except requests.exceptions.RequestException:
                print(f"   [-] Could not fetch this JS file (Timeout/Error).")

        print("--------------------------------------------------")
        print("[+] JS API Key Hunt Complete, Bhai!")

    except requests.exceptions.RequestException as e:
        print(f"[!] Main website connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 js_hunter.py <target_url>")
        print("Example: python3 js_hunter.py http://testphp.vulnweb.com")
        sys.exit(1)
        
    target = sys.argv[1]
    hunt_api_keys(target)
