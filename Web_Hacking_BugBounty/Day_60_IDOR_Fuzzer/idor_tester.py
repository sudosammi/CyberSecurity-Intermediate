import requests
import sys
import time

def idor_fuzzer(base_url, start_id, end_id):
    print(f"\n[*] Bhai, starting IDOR Fuzzing on: {base_url}")
    print(f"[*] Testing IDs from {start_id} to {end_id}...\n")
    print("--------------------------------------------------")
    
    # Original response ki length nikal rahe hain (Reference ke liye)
    # Agar doosre IDs ki length alag aayi, matlab naya data load hua hai!
    
    for i in range(start_id, end_id + 1):
        # Base URL ke aage number jodh rahe hain (e.g., ?user=1, ?user=2)
        target_url = f"{base_url}{i}"
        
        try:
            response = requests.get(target_url, timeout=5)
            
            # Response ka size (length) aur status code
            content_length = len(response.text)
            status = response.status_code
            
            # Hacker Logic: Agar page exist karta hai (200 OK) aur size > 0 hai
            if status == 200 and content_length > 50:
                print(f"[+] JACKPOT 🎯 Data Found for ID {i} | URL: {target_url} | Size: {content_length} bytes")
            elif status == 403 or status == 401:
                print(f"[-] Blocked 🛑 ID {i} is protected (Good Security).")
            else:
                print(f"[*] Nothing found for ID {i} (Status: {status})")
                
            # Server block na kare isliye thoda delay (polite hacking)
            time.sleep(0.5)
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Arre yaar, Connection error on ID {i}: {e}")
            break

    print("--------------------------------------------------")
    print("[+] IDOR Fuzzing Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 idor_tester.py <base_url_with_parameter=> <start_id> <end_id>")
        print("Example: python3 idor_tester.py 'http://testphp.vulnweb.com/artists.php?artist=' 1 5")
        sys.exit(1)
        
    url = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    
    idor_fuzzer(url, start, end)
