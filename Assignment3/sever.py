"""
connect with cilent
Get operations: READ, PUT, GET
Update the summary 
Function to prepare to output the result
"""
from operation_function import Operations
import sys
import socket

# implement the Operation
op = Operations()

# create and initialize the summary of the current tuple space
summary = {
    # the total number of clients
    "number_client": 0,
    # the total number of operations
    "number_operations": 0,
    # total READs
    "total_read": 0,
    # total GETs
    "total_gets": 0,
    # total PUTs
    "total_puts": 0,
    # Errors
    "number_errors": 0
}

# main method
def main():
    port = int(sys.argv[1])

    # create legal ports
    assert 50000 <= port <= 59999

    # Use IPV4 address, TCP protocol
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen()

    # start the background statistics thread of the server
    print("The server has been started and is listening on port!")