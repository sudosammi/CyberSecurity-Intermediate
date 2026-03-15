import scapy.all as scapy

# Ye function network se original (asli) MAC address nikal kar layega
def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    if answered_list:
        return answered_list[0][1].hwsrc
    return None

# Ye network packets ko continuously sunega
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    # Check karo ki kya packet ARP Response (op=2) hai?
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            # Packet mein jo IP aur MAC aa raha hai (Fake ho sakta hai)
            response_mac = packet[scapy.ARP].hwsrc
            response_ip = packet[scapy.ARP].psrc
            
            # Asli MAC address check karo network se
            real_mac = get_mac(response_ip)
            
            # Agar asli MAC aur packet wala MAC match nahi karte, matlab ATTACK!
            if real_mac != response_mac:
                print(f"[***] DANGER! YOU ARE UNDER ATTACK! [***]")
                print(f"Fake MAC: {response_mac} | Real MAC: {real_mac}\n")
                
        except IndexError:
            pass

print("[*] ARP Spoof Detector Running... Monitoring Network for Attacks.")
# Agar tum LAN par ho toh "eth0", agar WiFi par ho toh "wlan0" likhna
sniff("eth0")
