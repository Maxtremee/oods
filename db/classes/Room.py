from db.classes.Persistent import Persistent


class Room(Persistent):
    def __init__(self, name):
        self.name = name
