import logging
from uuid import UUID

from server.classes.Persistent import Persistent
from server.classes.Class import Class


class Index:
    def __init__(self):
        self.classes = {}

    def _add_to_class(self, obj: Persistent, path: list):
        cls_name = type(obj).__name__
        id = obj.id
        cls = self.classes.get(cls_name)
        if cls:
            cls.add(id, path)
        else:
            cls = Class()
            cls.add(id, path)
        self.classes.update({cls_name: cls})

    def process(self, obj: Persistent, path: list):
        """Creates paths to object and it's attributes 
        (have to inherit from Persistent)
        """
        self._add_to_class(obj, path)

        for attr in dir(obj):
            if not attr.startswith("_"):
                attr_obj = getattr(obj, attr)
                if isinstance(attr_obj, Persistent):
                    path_cpy = path
                    path_cpy.append(attr)
                    self.process(attr_obj, path_cpy)

    def get_path_by_id(self, id: UUID):
        """Return path to object by ID"""
        for cls in self.classes:
            paths = self.classes.get(cls).paths
            path = paths.get(id)
            if path is not None:
                return path
        return None

    def get_path_by_id_and_cls_name(self, id: UUID, cls_name: str):
        """Return path to object by class name and ID"""
        cls_obj = self.classes.get(cls_name)
        path = cls_obj.get(id)
        return path