import sys
import socket
import base64

# Parse the port number
def parse_port():
    if len(sys.argv) != 2:
        # error
        sys.exit(1)
    return int(sys.argv[1])

# Create the UDP socket and bind the port
def server_socket(port):
    server_sockets = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sockets.bind(('', port))
    return server_socket

# The function of the file transfer thread
def handle_file_transfer(filename, client_address, port):
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data_socket.bind(('', port))
    print(f"Send datagram packet to port {port}")

# Handle the FILE GET request
def handle_file_request(message, f, client_address, data_socket, filename):
    parts = message.split()
    if len(parts) != 8 or parts[0] != "FILE" or parts[2] != "GET":
        print("Invalid FILE GET message.")
        return
    
    try:
        start = int(parts[4])
        end = int(parts[6])

        # Read the data block
        f.seek(start)
        data = f.read(end - start + 1)
        encoded = base64.b64encode(data).decode()

        # Send the response
        response = f"FILE {filename} OK START {start} END {end} DATA {encoded}"
        data_socket.sendto(response.encode(), client_address)
    except Exception as e:
        print(f"Error: {e}")