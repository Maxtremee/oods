from test_classes.Room import Room
from server.Persistent import Persistent


class Home(Persistent):
    def __init__(self, name, rooms: list):
        super().__init__()
        self.name = name
        self.rooms = rooms
        self.main = Room("garage", "lift", "car")
