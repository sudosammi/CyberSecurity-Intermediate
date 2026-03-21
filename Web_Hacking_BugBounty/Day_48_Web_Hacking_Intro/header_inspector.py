import requests
import sys

def inspect_headers(url):
    print(f"\n[*] Bhai, scanning the headers for: {url} [*]\n")
    
    # Adding http:// if the user forgot it
    if not url.startswith('http'):
        url = 'http://' + url

    try:
        # Sending a GET request to the target
        response = requests.get(url, timeout=5)
        headers = response.headers
        
        print("--- [ Raw HTTP Headers ] ---")
        for key, value in headers.items():
            print(f"{key}: {value}")
        print("-" * 28 + "\n")

        # Checking for common missing security headers
        security_headers = [
            'Strict-Transport-Security',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Content-Security-Policy'
        ]

        print("--- [ Security Header Check ] ---")
        for sec_header in security_headers:
            if sec_header in headers:
                print(f"[+] Secure: {sec_header} is present.")
            else:
                print(f"[-] Vulnerable/Missing: {sec_header} is NOT found!")
                
    except requests.exceptions.RequestException as e:
        print(f"[!] Arre yaar, connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 header_inspector.py <target_url>")
        print("Example: python3 header_inspector.py example.com")
        sys.exit(1)
        
    target = sys.argv[1]
    inspect_headers(target)
