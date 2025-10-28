import socket

"""
A simple TCP server that listens for incoming connections,
1. socket()
2. bind()
3. listen()
4. accept()
5. recv()
6. send()
7. close()
"""

# 1. Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Bind to localhost on port 5000
server_socket.bind(('localhost', 5001))

# 3. Listen for incoming connections
server_socket.listen(1)
print("Server listening on port 5000...")

# 4. Accept a single connection
client_socket, address = server_socket.accept()
print(f"Connection from Client: {address}")

try:
    # 5. Receive data from client
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")

    # 6. Send response back to client
    client_socket.send(b"Server: Message received")
finally:
    # 7. Close the sockets
    client_socket.close()
    server_socket.close()
    print("Connection closed")