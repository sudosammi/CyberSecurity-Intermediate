import netfilterqueue

# ==========================================
# PACKET PROCESSING LOGIC
# ==========================================
def process_packet(packet):
    # Print a message for every packet we trap
    print("[+] Packet Intercepted and Held at the Barrier!")
    
    # Technical Term: Payload Forwarding
    # Iska matlab hai ki checking ke baad packet ko aage jaane do
    packet.accept()
    
    # Note: Agar hum packet.drop() likhenge, toh victim ka internet band ho jayega!

# ==========================================
# MAIN EXECUTION (Binding the Queue)
# ==========================================
print("[*] Setting up the NFQueue Toll Plaza (Queue 0)...")

# Creating an instance of the queue
queue = netfilterqueue.NetfilterQueue()

# Queue No. 0 par hamare function ko bind (jod) do
queue.bind(0, process_packet)

try:
    print("[*] Waiting for packets... (Press Ctrl+C to stop)")
    queue.run()
except KeyboardInterrupt:
    print("\n[-] Shutting down the Toll Plaza...")
    queue.unbind()
