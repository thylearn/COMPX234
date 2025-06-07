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

def read_file_list(file_path):
    try:
        with open(file_path) as f:
            file = f.read().splitlines()
    except FileNotFoundError:
        print(f"[ERROR] Cannot open file list: {file_path}")
        sys.exit(1)
    print("[INFO] Files to download:", file)
    return file
