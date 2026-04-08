import requests
import sys

def check_cors(url):
    print(f"\n[*] Bhai, checking CORS policy on: {url}")
    
    # THE HACKER'S BAIT
    # Hum server ko bol rahe hain ki humari request 'https://evil.com' se aayi hai
    headers = {
        'Origin': 'https://evil.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        # Server ka response header check kar rahe hain
        allow_origin = response.headers.get('Access-Control-Allow-Origin')
        allow_creds = response.headers.get('Access-Control-Allow-Credentials')
        
        print("[*] Analyzing Server Headers...")
        
        if not allow_origin:
            print("[-] Server is secure 🛑. No CORS headers found. SOP is protecting the data.")
            return
            
        print(f"[*] Server replied with: Access-Control-Allow-Origin: {allow_origin}")

        # Hacker Logic: The Evaluation
        if allow_origin == 'https://evil.com':
            if allow_creds == 'true':
                print("\n   [!!!] JACKPOT 🎯 CRITICAL CORS MISCONFIGURATION FOUND!")
                print("   [!!!] Server accepted our evil origin AND allows cookies/credentials.")
                print("   [!!!] Result: Full Account Takeover is possible!")
            else:
                print("\n   [!] BINGO 🎯 Basic CORS Misconfiguration Found.")
                print("   [!] Server accepted our evil origin, but credentials aren't allowed.")
                print("   [!] Result: Good for public data theft, but no session hijacking.")
                
        elif allow_origin == '*':
            if allow_creds == 'true':
                # Note: '*' ke sath creds true hona technically allowed nahi hota browsers mein
                print("\n   [?] Weird Configuration. '*' origin with credentials=true (Browser might block this).")
            else:
                print("\n   [!] BINGO 🎯 Open CORS Policy ('*') Found.")
                print("   [!] Result: Any website can read this API's unauthenticated data.")
                
        else:
            print(f"\n[-] Server is secure 🛑. It only trusts: {allow_origin}")

    except requests.exceptions.RequestException as e:
        print(f"[-] Arre yaar, connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 cors_scanner.py <target_api_url>")
        print("Example: python3 cors_scanner.py http://testphp.vulnweb.com")
        sys.exit(1)
        
    target = sys.argv[1]
    check_cors(target)
