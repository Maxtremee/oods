from server.classes.Persistent import Persistent
from server.classes.Class import Class
from server.classes.Reference import Reference
from server.classes.Item import Item


class Index:
    def __init__(self):
        self.classes = {}

    def add(self, obj: Persistent) -> Reference:
        """Add or update object in class"""
        cls_name = type(obj).__name__
        cls = self.classes.get(cls_name)
        if cls:
            cls.add(obj)
        else:
            cls = Class()
            cls.add(obj)
        self.classes.update({cls_name: cls})
        return Reference(obj.id, cls_name)

    def get(self, ref: Reference) -> Item:
        """Get Item of class"""
        cls = self.classes.get(ref.cls_name)
        if cls:
            return cls.get(ref.id)

    def remove(self, ref: Reference) -> None:
        """Remove Item"""
        if ref.cls_name:
            self.classes.get(ref.cls_name).remove(ref.id)
        else:
            for cls in self.classes:
                cls.remove(ref.id)
