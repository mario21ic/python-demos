import socket

"""
A simple UDP server that listens for incoming messages,
1. socket()
2. bind()
3. recvfrom()
4. sendto()
5. close()
"""

# 1. Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 2. Bind the socket to the port
server_address = ('localhost', 5002)
server_socket.bind(server_address)

print(f"UDP server listening on {server_address}")

try:
    while True:
        # 3. Receive data from client
        data, client_address = server_socket.recvfrom(1024)
        
        print(f"Received from {client_address}: {data.decode()}")

        # 4. Send response back to client
        response = "Message received"
        server_socket.sendto(response.encode(), client_address)
        
except KeyboardInterrupt:
    print("\nServer shutting down...")
finally:
    server_socket.close()