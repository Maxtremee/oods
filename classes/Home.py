from classes.Room import Room
from classes.Persistent import Persistent


class Home(Persistent):
    def __init__(self, name='household', *args):
        super().__init__()
        self.name = name
        self.rooms = []
        for room in args:
            self.rooms.append(Room(room))
