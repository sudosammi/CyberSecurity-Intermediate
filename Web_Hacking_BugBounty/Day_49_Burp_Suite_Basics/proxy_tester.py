import requests
import urllib3

# Burp Suite ke SSL warnings ko hide karne ke liye
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def send_to_burp(url):
    # Yeh raha tumhara Hacker Proxy (Burp Suite ka default address)
    burp_proxy = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080",
    }
    
    print(f"\n[*] Bhai, request ko Burp Suite Proxy (127.0.0.1:8080) ke through bhej rahe hain...")
    print(f"[*] Target: {url}")
    
    try:
        # verify=False isliye taaki SSL certificate ka error na aaye (kyunki Burp beech mein hai)
        response = requests.get(url, proxies=burp_proxy, verify=False, timeout=10)
        print(f"[+] Request Successful! Server ne {response.status_code} code return kiya.")
        print("[*] Fatafat apna Burp Suite -> HTTP History check karo, wahan yeh request dikhegi! 😎\n")
        
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Arre yaar, Error aa gaya: {e}")
        print("[!] Hint: Kya tumne Kali Linux mein Burp Suite open kiya hua hai? Proxy 127.0.0.1:8080 par chalni chahiye!\n")

if __name__ == "__main__":
    target_url = "http://example.com"
    send_to_burp(target_url)
