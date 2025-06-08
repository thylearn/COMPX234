import sys

# Parse the port number
def parse_port():
    if len(sys.argv) != 2:
        # error
        sys.exit(1)
    return int(sys.argv[1])

