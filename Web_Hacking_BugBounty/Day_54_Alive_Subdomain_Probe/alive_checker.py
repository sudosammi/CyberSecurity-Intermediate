import requests
import sys
import urllib3

# Bug Bounty mein bohot se dev servers ke SSL certificate expire hote hain, 
# isliye hum is error ko hide kar rahe hain taaki terminal clean rahe.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_alive(file_path):
    print(f"\n[*] Bhai, checking which subdomains are ALIVE from the list: {file_path}...\n")
    
    try:
        # File se saare subdomains read kar rahe hain
        with open(file_path, 'r') as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print(f"[-] Arre yaar, file nahi mili: {file_path}")
        return

    alive_count = 0
    
    # Har subdomain ko check kar rahe hain
    for sub in subdomains:
        target_url = f"https://{sub}" # Pehle HTTPS try karte hain
        
        try:
            # timeout=3 seconds (zyada wait nahi karenge dead sites ke liye)
            response = requests.get(target_url, timeout=3, verify=False)
            print(f"[+] ALIVE 🟢 ({response.status_code}) : {target_url}")
            alive_count += 1
            
        except requests.exceptions.RequestException:
            # Agar HTTPS fail hua, toh HTTP try karte hain
            target_url_http = f"http://{sub}"
            try:
                response_http = requests.get(target_url_http, timeout=3)
                print(f"[+] ALIVE 🟡 ({response_http.status_code}) : {target_url_http}")
                alive_count += 1
            except requests.exceptions.RequestException:
                # Dono fail! Matlab server dead hai. Hum isko print nahi karenge taaki kachra na ho.
                pass 
                
    print(f"\n[*] Boom! Scan Complete! Found {alive_count} alive subdomains out of {len(subdomains)}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 alive_checker.py <subdomains_list.txt>")
        print("Example: python3 alive_checker.py targets.txt")
        sys.exit(1)
        
    target_file = sys.argv[1]
    check_alive(target_file)
