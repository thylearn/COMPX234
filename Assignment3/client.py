# client.py - client program to interact with server
import socket
import sys
import os

# switch to the required form
# e.x. PUT Livepool 19
def switch_format(l:str):
    pass

def main():
    local_host = sys.argv[1]
    port = int(sys.argv[2])
    text_file = sys.argv[3]
    
    if not os.path.exists(text_file):
        # can't find the file
        return

    # create a TCP connection and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.connect((local_host, port))

        # open file 
        with open(text_file, "r", encoding='utf-8') as file:
            for lines in file:
                line = lines.strip()
                if not line:
                    continue

if __name__ == '__main__':
    main()