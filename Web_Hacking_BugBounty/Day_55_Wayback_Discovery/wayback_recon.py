import requests
import sys

def get_wayback_urls(domain):
    print(f"\n[*] Bhai, hunting 'Ghosts' (old & hidden URLs) for {domain} in the Wayback Machine...")
    print("[*] Interacting with web.archive.org API... Please wait.\n")
    
    # Wayback Machine ka CDX API - yeh saare archived URLs return karta hai
    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=txt&fl=original&collapse=urlkey"
    
    try:
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            urls = response.text.split('\n')
            juicy_urls = set() # Duplicate URLs ko hatane ke liye
            
            # Hum sirf wahi URLs filter karenge jisme hacking ka scope ho (?parameters, .php, .js)
            for u in urls:
                if '?' in u or u.endswith('.php') or u.endswith('.js') or u.endswith('.aspx'):
                    juicy_urls.add(u)
                    
            print(f"[+] BOOM! 🎯 Found {len(juicy_urls)} juicy URLs with parameters/scripts!\n")
            
            # Terminal clean rakhne ke liye sirf top 20 print karenge
            count = 0
            for ju in juicy_urls:
                if ju.strip(): # Empty lines ignore karne ke liye
                    print(f" -> {ju}")
                    count += 1
                if count >= 20:
                    print(f"\n[!] And many more... (Total: {len(juicy_urls)} juicy endpoints found!)")
                    print("[*] Pro Tip: Real hacking mein hum is list ko ek file mein save karte hain.")
                    break
                    
        else:
            print(f"[-] Arre yaar, API request failed with status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 wayback_recon.py <target_domain>")
        print("Example: python3 wayback_recon.py testphp.vulnweb.com")
        sys.exit(1)
        
    target = sys.argv[1]
    get_wayback_urls(target)
