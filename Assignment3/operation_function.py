import threading

# Create three operations
class Operations:
    def __init__(self):
        # create tuple space
        self.tuple_space = {}

        # use lock
        self.lock = threading.Lock()
    
    