# client.py - client program to interact with server
import socket
import sys
import os

def main():
    local_host = sys.argv[1]
    port = int(sys.argv[2])
    text_file = sys.argv[3]
    
    # create a TCP connection and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((local_host, port))
if __name__ == '__main__':
    main()