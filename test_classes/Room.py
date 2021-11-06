from server.classes.Persistent import Persistent


class Room(Persistent):
    def __init__(self, name):
        super().__init__()
        self.name = name
