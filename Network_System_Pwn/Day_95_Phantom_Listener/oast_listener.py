import http.server
import socketserver
import datetime
import sys

class OASTHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Disable default python HTTP logging to keep our terminal clean
        pass

    def do_GET(self):
        self.catch_ping("GET")

    def do_POST(self):
        self.catch_ping("POST")
        
    def do_HEAD(self):
         self.catch_ping("HEAD")

    def catch_ping(self, method):
        print(f"\n[!!!] JACKPOT 🎯 PHANTOM PING RECEIVED!")
        print(f"   [+] Timestamp : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   [+] Target IP : {self.client_address[0]} (The victim server reached out to us!)")
        print(f"   [+] Path Hit  : {method} {self.path}")
        print(f"   [+] Headers sent by the Target:")
        
        for key, value in self.headers.items():
            print(f"       -> {key}: {value}")
            
        print("-" * 60)
        
        # Send a simple HTTP 200 OK back so the target server doesn't crash
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK - Phantom Listener")

def start_listener(port=8000):
    print(f"\n[*] Bhai, starting The Phantom Listener (Out-of-Band / OAST Server)...")
    print(f"[*] Listening for Blind SSRF & RCE Pingbacks on Port {port}\n")
    print("==================================================")
    print("[*] Hacker Action: Inject your Fedora IP into the target website like this:")
    print(f"    Payload: http://<YOUR_IP>:{port}/ssrf_test")
    print("[*] Waiting for incoming connections... (Press Ctrl+C to stop)")
    print("==================================================\n")
    
    with socketserver.TCPServer(("0.0.0.0", port), OASTHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Shutting down The Phantom Listener. Good hunting, Bhai!")

if __name__ == "__main__":
    port_num = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_listener(port_num)
