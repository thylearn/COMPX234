import sys
import socket

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

