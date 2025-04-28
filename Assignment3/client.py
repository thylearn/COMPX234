# client.py - client program to interact with server
import socket
import sys
import os

# switch to the required form
# e.x. PUT Livepool 19
def switch_format(l:str):
    # get the list of three part
    values = l.strip().split(" ", 2)
    if not values:
        return None
    
    operation = values[0]
    if operation == "READ" or operation == "GET":
        if len(values) != 2:
            return None
        k = values[1]
        format_msg = f"{operation[0]} {k}"
    
    elif operation == "PUT":
        if len(values) != 3:
            return None
        k, v = values[1], values[2]
        if len(k) + len(v) > 969:
            # can't access too long characters
            return None
        format_msg = f"{operation[0]} {k} {v}"
    
    else:
        return None
    
    return f"{len(format_msg) + 3:03}" + format_msg


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