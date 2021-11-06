from test_classes.Room import Room
from server.classes.Persistent import Persistent


class Home(Persistent):
    def __init__(self, name, room: Room):
        super().__init__()
        self.name = name
        self.room = room
