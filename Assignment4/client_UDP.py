import sys

# Parse user input
def parse_arguments():
    if len(sys.argv) != 4:
        print("The input not right.")
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    file_path = sys.argv[3]
    return host, port, file_path