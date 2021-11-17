from shared.Persistent import Persistent
from Furniture import Furniture


class Room(Persistent):
    def __init__(self, name, *args):
        super().__init__()
        self.name = name
        furniture = []
        for item in args:
            furn = Furniture(item)
            furniture.append(furn)
        self.furniture = tuple(furniture)
