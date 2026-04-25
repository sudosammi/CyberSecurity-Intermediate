import os
import subprocess

def hunt_capabilities():
    print("\n[*] Bhai, starting Linux Capabilities (Phantom Privileges) Hunter...")
    print("[*] Hunting for binaries with hidden, invisible root powers!\n")
    print("==================================================")

    try:
        print("[*] Executing 'getcap' command across the system... (Wait 2-3 seconds)")
        # getcap -r / runs recursively to find capabilities, 2>/dev/null hides permission denied errors
        cmd = "getcap -r / 2>/dev/null"
        result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        
        if not result:
            print("[-] No special capabilities found, or 'getcap' is missing on this OS.")
            return

        # The Hacker's Dictionary of Dangerous Capabilities
        # Agar yeh powers kisi aam file ko mil jayein, toh server hacked!
        dangerous_caps = [
            "cap_setuid",         # Power to change User ID (Become Root)
            "cap_setgid",         # Power to change Group ID
            "cap_dac_override",   # Bypass file read/write/execute checks (God mode for files)
            "cap_dac_read_search",# Power to read any file (e.g., /etc/shadow)
            "cap_sys_admin",      # Universal God Mode
            "cap_chown"           # Power to change file owners
        ]

        lines = result.split('\n')
        found_vuln = 0

        print("\n[+] Scanning results for Highly Exploitable Capabilities:")
        for line in lines:
            if not line.strip(): continue
            
            # Example output: /usr/bin/python3 = cap_setuid+ep
            parts = line.split('=')
            binary_path = parts[0].strip()
            caps = parts[1].strip() if len(parts) > 1 else ""

            is_dangerous = False
            for dc in dangerous_caps:
                if dc in caps:
                    is_dangerous = True
                    found_vuln += 1
                    print(f"\n   [!!!] JACKPOT 🎯 CRITICAL CAPABILITY FOUND!")
                    print(f"   [!!!] Binary Target: {binary_path}")
                    print(f"   [!!!] Hidden Power : {dc}")
                    print(f"   [!!!] Hacker Action: Go to GTFOBins (https://gtfobins.github.io/), search for '{binary_path.split('/')[-1]}', and click 'Capabilities' to get ROOT!")
                    break
            
            if not is_dangerous:
                # Sirf show off ke liye print kar rahe hain ki tool kaam kar raha hai
                print(f"    [-] Low Risk/System Default: {binary_path} -> {caps}")

        print("\n==================================================")
        if found_vuln > 0:
            print(f"[+] Scan Complete! Found {found_vuln} Dangerous Phantom Powers. Escalate to ROOT immediately! 💀")
        else:
            print("[-] Scan Complete. Admin has configured capabilities securely.")

    except Exception as e:
        print(f"[-] Error executing capability scan: {e}")

if __name__ == "__main__":
    hunt_capabilities()
