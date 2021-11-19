from oodstools import Persistent


class Item:
    def __init__(self, obj: Persistent, uses: int = 1):
        self.obj = obj
        self.uses = uses
        self.cls_name = type(obj).__name__

    def decrement(self):
        self.uses -= 1

    def increment(self):
        self.uses += 1

    def set(self, obj: Persistent):
        self.obj = obj

    def get_id(self):
        return self.obj.id

    def get_last_changed(self):
        return self.obj.last_changed
