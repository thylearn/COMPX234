import sys
import socket
import base64
import os
import random
import threading

# Parse the port number
def parse_port():
    if len(sys.argv) != 2:
        # error
        print("Parse port error!")
        sys.exit(1)
    return int(sys.argv[1])

# Create the UDP socket and bind the port
def server_socket(port):
    server_sockets = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_sockets.bind(('', port))
    return server_sockets

# Listen and handle the client requests
def listen_requests(server_socket):
    while True:
        try:
            request, client_address = server_socket.recvfrom(4096)
            msg = request.decode().strip()
            print(f"Received from {client_address}: {msg}")
            handle_download_request(msg, client_address, server_socket)
        except Exception as e:
            print(f"{e}")

# Send an error or start a thread
def handle_download_request(message, client_address, server_socket):
    # request message
    parts = message.split()
    if len(parts) != 2 or parts[0] != "DOWNLOAD":
        print("Invalid request.")
        return

    # The requested file name
    filename = parts[1]
    if not os.path.exists(filename):
        error_message = f"ERR {filename} NOT_FOUND"
        server_socket.sendto(error_message.encode(), client_address)
        print(f"{error_message}")
    else:
        start_thread(filename, client_address, server_socket)

# Start the thread and send the OK response
def start_thread(filename, client_address, server_socket):
    file_size = os.path.getsize(filename)
    port = random.randint(50000, 51000)

    # Confirmation message
    OK_message = f"OK {filename} SIZE {file_size} PORT {port}"

    # Send the confirmation message
    server_socket.sendto(OK_message.encode(), client_address)
    print(f"{OK_message}")

    thread = threading.Thread(target=handle_file_transfer, args=(filename, client_address[0], port))
    thread.start()

# The function of the file transfer thread
def handle_file_transfer(filename, client_ip, port):
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data_socket.bind(('', port))
    print(f"Send datagram packet to port {port} for {filename}")

    # Open the file and process the request
    try:
        with open(filename, "rb") as f:
            while True:
                request, client_address = data_socket.recvfrom(65536)
                message = request.decode().strip()
                print(f"{message}")
                if "CLOSE" in message:
                    # Handle the CLOSE request
                    close_acknowledge = f"FILE {filename} CLOSE_OK"
                    data_socket.sendto(close_acknowledge.encode(), client_address)
                    print(f"{close_acknowledge}")
                    break

                # Handle GET requests
                handle_file_request(message, f, client_address, data_socket, filename)
    except Exception as e:
        print(f"Error {filename}: {e}")
    
    finally:
        data_socket.close()
        print(f"Closed socket on port {port}")

# Handle the FILE GET request
def handle_file_request(message, f, client_address, data_socket, filename):
    parts = message.split()
    if len(parts) != 8 or parts[0] != "FILE" or parts[2] != "GET":
        print("Invalid FILE GET message.")
        return
    
    try:
        start = int(parts[4])
        end = int(parts[6])

        if start > end or start < 0 or end < 0:
            print(f"Invalid range: {start}-{end}")
            return

        # Read the data block
        f.seek(start)
        data = f.read(end - start + 1)
        encoded = base64.b64encode(data).decode()

        print(f"FILE {filename} OK START {start} END {end} DATA {message}")

        # Send the response
        response = f"FILE {filename} OK START {start} END {end} DATA {encoded}"
        data_socket.sendto(response.encode(), client_address)
    except Exception as e:
        print(f"Error: {e}")

# Main entrance
def main():
    port = parse_port()
    server_socket = server_socket(port)
    listen_requests(server_socket)

if __name__ == "__main__":
    main()