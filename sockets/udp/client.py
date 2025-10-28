import socket

"""
A simple UDP client that sends a message to a server,
1. socket()
2. sendto()
3. recvfrom()
4. close()
"""

# 1. Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address and port
server_address = ('localhost', 5002)

try:
    # 2. Send a message to the server
    message = "Hello, Server!"
    client_socket.sendto(message.encode(), server_address)

    # 3. Receive response from server
    data, server = client_socket.recvfrom(1024)
    print(f"Received: {data.decode()}")
    
finally:
    # 4. Close the socket
    client_socket.close()