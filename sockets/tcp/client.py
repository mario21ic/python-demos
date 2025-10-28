import socket

"""
A simple TCP client that connects to a server,
1. socket()
2. connect()
3. send()
4. recv()
5. close()
"""

def main():
    # Server configuration
    HOST = '127.0.0.1'
    PORT = 5001

    # 1. Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 2. Connect to the server
        client_socket.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        # 3. Send a message to the server
        message = "Hello from Client"
        client_socket.sendall(message.encode('utf-8'))
        print(f"Sent: {message}")

        # 4. Receive response from server
        data = client_socket.recv(1024)
        print(f"Received: {data.decode('utf-8')}")
        
    except ConnectionRefusedError:
        print(f"Failed to connect to {HOST}:{PORT}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # 5. Close the socket
        client_socket.close()
        print("Connection closed")

if __name__ == "__main__":
    main()