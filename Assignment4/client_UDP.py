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
    control_sockets = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    control_address = (host, port)
    print("Control socket created")
    return control_sockets, control_address

# Reliable send and receive
def send_receive(sock, message, server_address):
    max_retry = 5
    time_out = 1.0
    # Retry loop
    for i in range(max_retry):
        try:
            # Set a timeout and send a message
            sock.settimeout(time_out)
            sock.sendto(message.encode(), server_address)

            # Receiving response
            data, _ = sock.recvfrom(65536)
            return data.decode()
        except socket.timeout:
            # Timeout handling and retry
            print("Timeout.")
            time_out *= 2

    print("No response received.")
    return None

# Main function of the program
def main():
    host, port, file_path = parse_arguments()
    file = read_file(file_path)
    control_sockets, control_address = control_socket(host, port)