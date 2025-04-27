import threading

# Create three operations
class Operations:
    def __init__(self):
        # create tuple space
        self.tuple_space = {}

        # use lock
        self.lock = threading.Lock()
    
    def read(self, k):
        """
        if k exists return v
        else return none
        """
        with self.lock:
            return self.tuple_space.get(k, None)
        
    def get(self, k):
        """
        if k exists return v and delete (k, v)
        else return none
        """
        with self.lock:
            return self.tuple_space.pop(k, None)