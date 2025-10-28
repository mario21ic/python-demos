import socket
import os

"""
A simple Unix domain socket server that listens for incoming connections,
1. socket()
2. bind()
3. listen()
4. accept()
5. recv()
6. send()
7. close()
"""

# Socket file path
socket_file = "/tmp/python_unix_socket.sock"

# Remove socket file if it already exists
try:
    os.remove(socket_file)
except OSError:
    if os.path.exists(socket_file):
        raise

# 1. Create a Unix domain socket
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# 2. Bind the socket to the port
server.bind(socket_file)

# 3. Listen for incoming connections
server.listen(1)
print(f"Server listening on {socket_file}")

# 4. Accept a single connection
connection, client_address = server.accept()
try:
    print("Connection received")
    
    # Receive data
    while True:
        # 5. Receive data from client
        data = connection.recv(1024)
        if data:
            # 6. Send response back to client
            print(f"Received: {data.decode()}")
            connection.sendall(b"Message received")
        else:
            break
finally:
    # 7. Close the sockets
    connection.close()
    server.close()
    os.remove(socket_file)