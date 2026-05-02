import requests
import json
import sys
import re

def hunt_secrets_in_json(data, path="Root"):
    # This dictionary will store any leaked sensitive keys we find
    leaks = []
    
    # The Hacker's Target List: Keywords that should NEVER be sent to the frontend
    sensitive_keywords = [
        "password", "hash", "token", "secret", "ssn", "credit_card",
        "api_key", "auth", "session", "private", "hidden", "internal_id",
        "salary", "balance", "otp", "pin", "uuid"
    ]

    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path} -> {key}"
            
            # Check if the key itself is a sensitive word
            for keyword in sensitive_keywords:
                if keyword in key.lower():
                    leaks.append((current_path, key, str(value)[:50])) # Limit value length for display
                    break
            
            # Recursively search if the value is another dict or list
            leaks.extend(hunt_secrets_in_json(value, current_path))
            
    elif isinstance(data, list):
        for index, item in enumerate(data):
            current_path = f"{path}[{index}]"
            leaks.extend(hunt_secrets_in_json(item, current_path))
            
    return leaks

def xray_scan(target_url):
    print(f"\n[*] Bhai, starting API X-Ray Scanner (Excessive Data Exposure) on -> {target_url}")
    print("[*] Fetching raw JSON and scanning for hidden developer secrets...\n")
    print("==================================================")

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Arch Linux x86_64) API-XRay/1.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=10)
        status = response.status_code
        
        if status != 200:
             print(f"[-] Target returned HTTP {status}. Unable to fetch data properly.")
             return

        try:
            # Parse the JSON response
            json_data = response.json()
        except json.JSONDecodeError:
            print("[-] Target did not return valid JSON. Are you sure this is an API endpoint?")
            return

        print("[+] Raw JSON retrieved successfully. Initiating deep recursive scan...\n")
        
        # Start the recursive search
        found_leaks = hunt_secrets_in_json(json_data)

        if found_leaks:
            print("   [!!!] JACKPOT 🎯 SENSITIVE DATA EXPOSURE FOUND!")
            print("   [!!!] The API is sending more data than the frontend needs.\n")
            
            for path, key, value in found_leaks:
                print(f"   [!] LEAK FOUND:")
                print(f"       -> JSON Path: {path}")
                print(f"       -> Suspicious Key: '{key}'")
                print(f"       -> Exposed Value : {value}...")
                print("-" * 40)
        else:
            print("   [-] Scan complete. No obvious sensitive keywords found in the JSON keys.")
            print("   [-] The API seems to be correctly filtering the data (or uses weird key names).")

    except requests.exceptions.RequestException as e:
        print(f"[-] Connection failed: {e}")

    print("\n==================================================")
    print("[+] X-Ray Scan Complete, Bhai! 💸")

if __name__ == "__main__":
    # Ignore HTTPS warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 api_xray.py <API_Endpoint_URL>")
        print("Example: python3 api_xray.py https://api.target.com/v1/user/profile")
        sys.exit(1)
        
    target = sys.argv[1]
    xray_scan(target)
