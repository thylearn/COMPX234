import sys
import socket

# Parse user input
def parse_arguments():
    if len(sys.argv) != 4:
        print("The input not right.")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    return host, port, file_path

# Read file method
def read_file(file_path):
    try:
        with open(file_path) as f:
            file = f.read().splitlines()
    except FileNotFoundError:
        print(f"Cannot open file list: {file_path}")
        sys.exit(1)
    print("Files to download:", file)
    return file

# Create UDP socket
def control_socket(host, port):
    control_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_address = (host, port)
    print("Control socket created")
    return control_socket, control_address