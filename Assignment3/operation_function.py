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
    
    def put(self, k, v):
        """
        if k exists return 1
        else add the tuple
        """
        with self.lock:
            if (k, v) in self.tuple_space:
                return 1 # fail
            
            # Add (k, v) to the dictionary
            self.tuple_space[k] = v
            return 0 # success