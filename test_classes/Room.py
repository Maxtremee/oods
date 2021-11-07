from server.classes.Persistent import Persistent
from test_classes.Furniture import Furniture


class Room(Persistent):
    def __init__(self, name, *args):
        super().__init__()
        self.name = name
        self.furniture = {}
        for item in args:
            furn = Furniture(item)
            self.furniture.update({furn.name: furn})
