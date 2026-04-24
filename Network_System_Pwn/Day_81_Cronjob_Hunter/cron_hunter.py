import os
import re

def hunt_cronjobs():
    print("\n[*] Bhai, starting Automated Cronjob Privilege Escalation Hunter...")
    print("[*] Hunting for poorly configured scheduled tasks that run as ROOT!\n")
    print("==================================================")

    cron_files = [
        "/etc/crontab",
        "/etc/cron.d/",
        "/etc/cron.daily/",
        "/etc/cron.hourly/",
        "/etc/cron.weekly/",
        "/etc/cron.monthly/"
    ]

    vulnerable_found = 0

    print("[+] Step 1: Scanning System-Wide Crontab Files...\n")
    
    # Extracting file paths from the /etc/crontab using Regex
    path_regex = re.compile(r'(/[\w\.\-]+)+')
    
    try:
        with open("/etc/crontab", "r") as f:
            lines = f.readlines()
            for line in lines:
                # Ignore comments and empty lines
                if line.startswith("#") or not line.strip():
                    continue
                
                print(f"    [*] Analyzing task: {line.strip()}")
                
                # Search for file paths in the cron line
                paths = path_regex.findall(line)
                for path in paths:
                    # Often regex returns tuples/strings depending on capture groups, let's format it
                    full_path = line[line.find(path):].split()[0] 
                    if os.path.exists(full_path):
                        # The Hacker Check: Can we write to this file?
                        if os.access(full_path, os.W_OK):
                            print(f"\n   [!!!] JACKPOT 🎯 CRITICAL VULNERABILITY FOUND!")
                            print(f"   [!!!] File: {full_path}")
                            print("   [!!!] Why: This file is executed by Cron, and YOU have WRITE access!")
                            print("   [!!!] Action: Inject your reverse shell here and wait for it to execute as ROOT!\n")
                            vulnerable_found += 1
                        else:
                            print(f"        [-] Path {full_path} is secure (Read-Only).")
    except Exception as e:
        print(f"    [-] Could not read /etc/crontab: {e}")

    print("\n[+] Step 2: Checking standard Cron Directories for writable scripts...")
    for directory in cron_files[1:]:
        if os.path.exists(directory):
            try:
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        if os.access(filepath, os.W_OK):
                            print(f"   [!!!] JACKPOT 🎯 WRITABLE CRON SCRIPT FOUND: {filepath}")
                            vulnerable_found += 1
            except Exception:
                pass

    print("\n==================================================")
    if vulnerable_found > 0:
        print(f"[+] Scan Complete! Found {vulnerable_found} vulnerable Cronjobs. Time to get ROOT! 💀")
    else:
        print("[-] Scan Complete. No obviously writable cron scripts found. Admin is smart.")

if __name__ == "__main__":
    hunt_cronjobs()
