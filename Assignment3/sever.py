"""
connect with cilent
initialize summary of tuple space
Get operations: READ, PUT, GET
Update the summary 
Function to prepare to output the result
"""
from operation_function import Operations

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