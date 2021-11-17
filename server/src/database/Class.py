from uuid import UUID
from .Item import Item


class Class:
    def __init__(self):
        self.items = {}

    def add(self, new: Item):
        """Add or update Item of particular class"""
        id = new.get_id()
        old = self.items.get(id)
        if old:
            if old.get_last_changed() <= new.get_last_changed():
                old.set(new.obj)
                old.increment()
                self.items.update({id: old})
            else:
                #TODO: raise error
                pass
        else:
            self.items.update({id: new})

    def get(self, id: UUID) -> Item:
        """Get item with object's ID"""
        return self.items.get(id)

    def remove(self, id: UUID):
        """Remove item with object's ID
        
        Depending on uses count, either decrements the item or removes it altogether"""
        item = self.items.get(id)
        if item:
            item.decrement()
            if item.uses < 1:
                self.items.pop(id)
            else:
                self.items.update({id: item})
