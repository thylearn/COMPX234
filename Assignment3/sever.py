"""
Function to prepare to output the result
"""
from operation_function import Operations
import sys
import socket
import threading
import time

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
                            response = f"ERR {content} does not exist"

                # except operation
                else:
                    with summary_lock:
                        summary["number_errors"] += 1

                connection.send(f"{len(response.encode()) + 3:03}".encode() + response.encode())
            except Exception as e:
                break
            
    # add clients
    with summary_lock:
        summary["number_client"] += 1

# define the server output
def server_output():
    while True:
        # set 10 seconds
        time.sleep(10)

        while summary_lock:
            num = len(op.tuple_space)
            total_key = sum(len(k) for k in op.tuple_space)
            total_value = sum(len(v) for v in op.tuple_space())

            # average key size and value size
            if num != 0:
                average_key = total_key / num
                average_value = total_value / num
            average_tuple = average_key + average_value

            # print summary
            print("\nA summary of the current tuple space")
            print("The number of tuple in the tuple space: " + str(num))
            print(f"The average tuple size: {average_tuple:.2f}")
            print(f"The average key size: {average_key:.2f}")
            print(f"The average value size: {average_value:.2f}")
            print(f"The total number of clients which have connected: {summary["number_client"]}")
            print(f"The total number of operations: {summary['number_operations']}")
            print(f"Total READs: {summary['total_reads']}")
            print(f"Total GETs: {summary['total_gets']}")
            print(f"Total PUTs: {summary['total_puts']}")
            print(f"Errors: {summary['number_errors']}")

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