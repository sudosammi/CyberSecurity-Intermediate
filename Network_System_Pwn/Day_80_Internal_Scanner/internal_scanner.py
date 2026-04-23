import socket
import sys
from datetime import datetime

def scan_internal_ports(target):
    print(f"\n[*] Bhai, starting Stealth Internal Port Scan on: {target}")
    print("[*] Hunting for hidden local services (Databases, Caches, Admin Panels)...\n")
    print("==================================================")
    
    # The Hacker's Target List: These ports are usually hidden behind a firewall
    # but accessible from the inside!
    common_internal_ports = {
        21: "FTP (File Transfer)",
        22: "SSH (Secure Shell)",
        80: "HTTP (Internal Web)",
        8080: "HTTP-Alt (Internal Admin Panel)",
        3306: "MySQL Database",
        5432: "PostgreSQL Database",
        6379: "Redis In-Memory Data (Usually NO password!)",
        27017: "MongoDB (NoSQL Database)",
        11211: "Memcached",
        9000: "PHP-FPM / Debugger",
        2375: "Docker API (Unauthenticated!)"
    }
    
    found_ports = 0
    t1 = datetime.now()
    
    # Loop through each interesting port
    for port, service in common_internal_ports.items():
        try:
            # Create a raw socket connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Timeout is very short (0.5s) because we are scanning locally/internally
            socket.setdefaulttimeout(0.5)
            
            # connect_ex returns 0 if the connection is successful (Port is Open)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                print(f"   [!!!] JACKPOT 🎯: Port {port} is OPEN -> {service}")
                found_ports += 1
            
            sock.close()
            
        except KeyboardInterrupt:
            print("\n[-] Arre yaar, scan stopped by user.")
            sys.exit()
        except socket.error:
            print("[-] Socket Error. Target might be down.")
            sys.exit()
            
    t2 = datetime.now()
    
    print("==================================================")
    print(f"[*] Scan completed in: {t2 - t1}")
    if found_ports > 0:
        print(f"[+] Found {found_ports} hidden internal services! Time to attack them locally for PrivEsc.")
    else:
        print("[-] No common internal services found.")

if __name__ == "__main__":
    # If no IP is provided, it defaults to localhost (127.0.0.1)
    target_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    scan_internal_ports(target_ip)
