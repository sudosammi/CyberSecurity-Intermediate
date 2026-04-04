import requests
import sys

def dir_bruteforce(url, wordlist_path):
    print(f"\n[*] Bhai, starting Directory Bruteforce on: {url}")
    print(f"[*] Loading wordlist from: {wordlist_path}\n")
    
    try:
        with open(wordlist_path, 'r') as file:
            directories = file.read().splitlines()
    except FileNotFoundError:
        print("[-] Arre yaar, wordlist file nahi mili! Path check karo.")
        return

    print(f"[*] Loaded {len(directories)} words. Let's hunt!\n")
    print("--------------------------------------------------")
    
    # Check if URL ends with '/'
    if not url.endswith('/'):
        url += '/'
        
    found_count = 0

    # Ek-ek word ko test kar rahe hain
    for dir_name in directories:
        if not dir_name.strip(): # Empty line skip karo
            continue
            
        target_url = f"{url}{dir_name}"
        
        try:
            # Server ko request bhejna
            response = requests.get(target_url, timeout=5)
            
            # Hacker Logic: Status Code check karna
            if response.status_code == 200:
                print(f"[+] JACKPOT 🎯 200 OK Found: {target_url}")
                found_count += 1
            elif response.status_code == 403:
                print(f"[!] FORBIDDEN 🛑 403 Found (Exists, but locked): {target_url}")
                found_count += 1
            elif response.status_code in [301, 302]:
                print(f"[*] REDIRECT 🔀 Redirecting to somewhere else: {target_url}")
                found_count += 1
                
        except requests.exceptions.RequestException:
            pass # Timeout aane par ignore karke aage badho taaki script na ruke

    print("--------------------------------------------------")
    print(f"[+] Bruteforce Complete! Found {found_count} hidden paths.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 dir_hunter.py <target_url> <wordlist.txt>")
        print("Example: python3 dir_hunter.py http://testphp.vulnweb.com wordlist.txt")
        sys.exit(1)
        
    target = sys.argv[1]
    wordlist = sys.argv[2]
    
    dir_bruteforce(target, wordlist)
