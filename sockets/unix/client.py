import socket
import os

"""
A simple Unix domain socket client that connects to a server,
1. socket()
2. connect()
3. send()
4. recv()
5. close()
"""

# Unix socket path
socket_path = "/tmp/python_unix_socket.sock"

# 1. Create a Unix domain socket
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect to the server
try:
    # 2. Connect to the server
    client.connect(socket_path)
    print(f"Connected to {socket_path}")
    
    # Send data
    message = "Hello from client"
    # 3. Send a message to the server
    client.sendall(message.encode())
    print(f"Sent: {message}")

    # 4. Receive response
    response = client.recv(1024).decode()
    print(f"Received: {response}")
    
finally:
    # 5. Close the socket
    client.close()
    print("Connection closed")