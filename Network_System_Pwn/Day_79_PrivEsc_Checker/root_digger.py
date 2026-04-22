import os
import subprocess

def run_cmd(cmd):
    try:
        # Command run karke output nikalna
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
        return result.decode('utf-8').strip()
    except Exception:
        return "Not available / Error"

def privesc_scan():
    print(f"\n[*] Bhai, starting Linux Privilege Escalation (PrivEsc) Automated Checks...")
    print("[*] Goal: Finding paths to escalate from 'Low User' to 'ROOT'!\n")
    print("==================================================")

    # 1. System & User Info
    print("[+] 1. Basic System Recon:")
    print("    -> Current User : " + run_cmd("whoami"))
    print("    -> User ID Info : " + run_cmd("id"))
    print("    -> Kernel Ver   : " + run_cmd("uname -r"))
    
    os_release = run_cmd("cat /etc/os-release | grep PRETTY_NAME | cut -d '=' -f2").replace('"', '')
    print("    -> OS Release   : " + os_release)

    # 2. Hunting SUID Binaries (Magic commands that run as root)
    print("\n[+] 2. Hunting for SUID Binaries (Potential Root Shortcuts):")
    # Finding files with SUID bit set, ignoring errors and containers like snap/docker
    suid_cmd = "find / -perm -4000 -type f 2>/dev/null | grep -v 'snap\|docker' | head -n 8"
    suid_results = run_cmd(suid_cmd)
    
    if suid_results:
        for line in suid_results.split('\n'):
            print(f"    [*] Found: {line}")
        print("    [!] HACKER TIP: Search these binary names on https://gtfobins.github.io/ to get Root!")
    else:
        print("    [-] No interesting SUID binaries found.")

    # 3. Weak File Permissions
    print("\n[+] 3. Checking Writable Sensitive Files:")
    files_to_check = ['/etc/passwd', '/etc/shadow', '/etc/sudoers']
    
    for f in files_to_check:
        if os.path.exists(f):
            if os.access(f, os.W_OK):
                print(f"    [!!!] JACKPOT 🎯: {f} is WRITABLE!")
                print(f"    [!!!] You can inject a new root user directly into this file!")
            else:
                print(f"    [-] {f} is safe (Read-Only).")
        else:
            print(f"    [-] {f} does not exist.")

    # 4. Sudo Privileges without password
    print("\n[+] 4. Checking 'sudo' privileges:")
    sudo_check = run_cmd("sudo -l 2>/dev/null | grep 'NOPASSWD'")
    if sudo_check:
        print("    [!!!] JACKPOT 🎯: You can run these commands as root WITHOUT a password:")
        print(f"    {sudo_check}")
    else:
        print("    [-] No passwordless sudo rules found for this user.")

    print("\n==================================================")
    print("[+] PrivEsc Scan Complete! Analyze the results and get ROOT, Bhai!")

if __name__ == "__main__":
    privesc_scan()
