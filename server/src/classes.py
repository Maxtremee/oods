from shared.Persistent import Persistent

class Furniture(Persistent):
    def __init__(self, name):
        super().__init__()
        self.name = name


class Room(Persistent):
    def __init__(self, name, *args):
        super().__init__()
        self.name = name
        furniture = []
        for item in args:
            furn = Furniture(item)
            furniture.append(furn)
        self.furniture = tuple(furniture)


class Home(Persistent):
    def __init__(self, name, rooms: list):
        super().__init__()
        self.name = name
        self.rooms = rooms
        self.main = Room("garage", "lift", "car")