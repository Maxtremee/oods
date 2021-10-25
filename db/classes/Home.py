from db.classes.Room import Room
from db.classes.Persistent import Persistent


class Home(Persistent):
    def __init__(self, name='house', *args):
        super().__init__()
        self.name = name
        self.rooms = []
        for room in args:
            self.rooms.append(Room(room))
