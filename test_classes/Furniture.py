from server.Persistent import Persistent

class Furniture(Persistent):
    def __init__(self, name):
        super().__init__()
        self.name = name