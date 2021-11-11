from uuid import UUID
from server.classes.Item import Item
from server.classes.Persistent import Persistent

class Class:
    def __init__(self):
        self.items = {}

    def add(self, obj: Persistent):
        """Add or update item of particular class"""
        item = self.items.get(obj.id)
        if item:
            item.increment()
            item.set(obj)
        else:
            item = Item(obj)
        self.items.update({obj.id: item})

    def get(self, id: UUID) -> Item:
        """Get item with object's ID"""
        return self.items.get(id)

    def remove(self, id: UUID):
        """Remove item with object's ID
        
        Depending on uses count either decrements the item or removes it altogether"""
        item = self.items.get(id)
        if item:
            if item.uses < 1:
                self.items.pop(id)
            else:
                item.decrement()
                self.items.update({id: item})
