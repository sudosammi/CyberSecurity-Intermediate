import requests
import sys

def scan_sqli(url):
    # The Hacker's Payload: Ek simple single quote database ko break karne ke liye
    payload = "'"
    vuln_url = f"{url}{payload}"
    
    print(f"\n[*] Bhai, testing the target: {url}")
    print(f"[*] Injecting payload: {payload}")
    print(f"[*] Firing at: {vuln_url}\n")
    
    try:
        # Request bhej rahe hain
        response = requests.get(vuln_url, timeout=5)
        
        # Yeh common errors hain jo database break hone par aate hain
        sql_errors = [
            "mysql_fetch",
            "you have an error in your sql syntax",
            "unclosed quotation mark after the character string",
            "pg_query()",
            "ora-01756"
        ]
        
        is_vulnerable = False
        
        # Response text mein errors dhoondh rahe hain
        for error in sql_errors:
            if error.lower() in response.text.lower():
                print(f"[+] BOOM! 🎯 SQL Injection Vulnerability Found!")
                print(f"[+] Server leaked this error: '{error}'")
                is_vulnerable = True
                break # Ek error mil gaya toh aage check karne ki zaroorat nahi
                
        if not is_vulnerable:
            print("[-] No SQL errors found. Either it's safe, or it's a Blind SQLi.")
            
    except requests.exceptions.RequestException as e:
        print(f"[!] Arre yaar, Connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sqli_scanner.py <target_url>")
        print("Example: python3 sqli_scanner.py 'http://testphp.vulnweb.com/artists.php?artist=1'")
        sys.exit(1)
        
    target = sys.argv[1]
    scan_sqli(target)
