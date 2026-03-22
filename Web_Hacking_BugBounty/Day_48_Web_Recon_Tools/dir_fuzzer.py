import requests
import sys

def fuzz_directories(target_url):
    # Real Bug Bounty mini-wordlist (Common hidden paths)
    wordlist = [
        'admin', 'login', 'dashboard', 'api', 'backup', 'config.php', 
        '.git', 'robots.txt', 'test', 'dev', 'old', 'phpinfo.php'
    ]
    
    print(f"\n[*] Bhai, scanning {target_url} for hidden paths... [*]\n")
    
    # URL formatting check
    if not target_url.startswith('http'):
        target_url = 'http://' + target_url
    if not target_url.endswith('/'):
        target_url += '/'

    # Loop through our wordlist
    for word in wordlist:
        test_url = target_url + word
        try:
            # Sending a GET request
            response = requests.get(test_url, timeout=3)
            
            # Checking the HTTP Status Code
            if response.status_code == 200:
                print(f"[+] BOOM! FOUND (200 OK): {test_url}")
            elif response.status_code == 403:
                print(f"[~] FORBIDDEN (403): {test_url} (Bhai, access denied hai but file exist karti hai!)")
            # Hum 404 (Not Found) ko print nahi kar rahe taaki terminal clean rahe
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Connection error testing {word}: {e}")
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 dir_fuzzer.py <target_url>")
        print("Example: python3 dir_fuzzer.py example.com")
        sys.exit(1)
        
    target = sys.argv[1]
    fuzz_directories(target)
