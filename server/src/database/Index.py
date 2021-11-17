from .Class import Class
from .Reference import Reference
from .Item import Item


class Index:
    def __init__(self):
        self.classes = {}

    def add(self, item: Item) -> Reference:
        """Add or update object in class"""
        cls_name = item.cls_name
        cls = self.classes.get(cls_name)
        if cls:
            cls.add(item)
        else:
            cls = Class()
            cls.add(item)
        self.classes.update({cls_name: cls})
        ref = Reference(item.get_id(), cls_name)
        return ref

    def get(self, ref: Reference) -> Item:
        """Get Item of class"""
        if ref.cls_name:
            cls = self.classes.get(ref.cls_name)
            if cls:
                return cls.get(ref.id)
        else:
            for cls_name in self.classes:
                cls = self.classes.get(cls_name)
                item = cls.get(ref.id)
                if item:
                    return item

    def remove(self, ref: Reference) -> None:
        """Remove Item"""
        if ref.cls_name:
            self.classes.get(ref.cls_name).remove(ref.id)
        else:
            for cls in self.classes:
                self.classes.get(cls).remove(ref.id)

    def get_all_by_cls(self, cls_name: str):
        """Returns all Items of a class"""
        return self.classes.get(cls_name).items
