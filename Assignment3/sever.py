"""
connect with cilent
Get operations: READ, PUT, GET
Update the summary 
Function to prepare to output the result
"""
from operation_function import Operations
import sys
import socket
import threading

# implement the Operation
op = Operations()
# create lock
summary_lock = threading.Lock()

# create and initialize the summary of the current tuple space
summary = {
    # the total number of clients
    "number_client": 0,
    # the total number of operations
    "number_operations": 0,
    # total READs
    "total_reads": 0,
    # total GETs
    "total_gets": 0,
    # total PUTs
    "total_puts": 0,
    # Errors
    "number_errors": 0
}

# functions connect with the client thread
# connect with client and load the client's address
def connect_client(connection, address):
    with connection:
        while True:
            try:
                # access three word
                size_con = connection.recv(3)
                if not size_con:
                    break

                # turn to int to check
                size = int(size_con.decode())

                # remain data to store, decode as string
                data = connection.recv(size - 3).decode()
                if not data:
                    break # no content
                
                # store the operations
                # READ PUT GET
                operation = data[0] # R P G
                content = data[2:].strip() # key and value

                # initialize the response
                response = ""
                
                # update the summary
                with summary_lock:
                    summary["number_operations"] += 1

                # if the operation is READ
                if operation == "R":
                    value = op.read(content)
                    with summary_lock:
                        summary["total_reads"] += 1

                    if value is not None:
                        response = f"OK ({content}, {value}) read"
                    else:
                        summary["number_errors"] += 1
                        response = f"ERR {content} does not exist"
                
                # if the operation is PUT
                elif operation == "P":
                    kv = content.split(" ", 1)
                    k, v = kv
                    add_result = op.put(k, v)
                    with summary_lock:
                        summary["total_puts"] += 1
                        if add_result == 1: # fall
                            summary["number_errors"] += 1
                            response = f"ERR {k} already exists"
                        else:
                            # success
                            response = f"OK ({k}, {v}) added"
                
                # if the operation is GET
                elif operation == "G":
                    value = op.get(content)
                    with summary_lock:
                        summary["total_gets"] += 1
                        if value is not None:
                            response = f"OK ({content}, {value}) removed"
                        else:
                            summary["number_errors"] += 1
                            respomse = f"ERR {content} does not exist"
            except Exception as e:
                break
            pass

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