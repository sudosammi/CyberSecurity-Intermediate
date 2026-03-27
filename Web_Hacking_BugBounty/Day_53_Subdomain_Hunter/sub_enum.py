import requests
import sys

def find_subdomains(domain):
    print(f"\n[*] Bhai, hunting hidden subdomains for: {domain} (Passive Recon) ...")
    print("[*] Interrogating public CT Logs (crt.sh)... Please wait.\n")
    
    # crt.sh ka API URL (output=json humein data clean format mein dega)
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    
    try:
        # Hum apna User-Agent change kar rahe hain taaki API humein block na kare
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            subdomains = set() # 'set' duplicate subdomains ko automatically remove kar dega
            
            # API se aaye hue JSON data ko filter kar rahe hain
            for entry in data:
                name_value = entry['name_value']
                # Kabhi-kabhi ek certificate mein multiple domains hote hain (newline se separated)
                for sub in name_value.split('\n'):
                    # Wildcard (*.) ko hata rahe hain taaki clean domain mile
                    clean_sub = sub.replace('*.', '').strip()
                    if clean_sub != domain: # Main domain ko ignore kar rahe hain
                        subdomains.add(clean_sub)
            
            print(f"[+] BOOM! 🎯 Found {len(subdomains)} unique subdomains!\n")
            
            # Print all sorted subdomains
            for sub in sorted(subdomains):
                print(f" -> {sub}")
                
        else:
            print(f"[-] Arre yaar, API request failed with status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Connection failed: {e}")
    except ValueError:
        print("[!] Failed to parse JSON data. crt.sh might be overloaded.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sub_enum.py <target_domain>")
        print("Example: python3 sub_enum.py yahoo.com")
        sys.exit(1)
        
    target = sys.argv[1]
    find_subdomains(target)
