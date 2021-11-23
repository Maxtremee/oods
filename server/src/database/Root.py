from oodstools import Persistent
from .Index import Index
from .Item import Item
from .Reference import Reference

from uuid import UUID
from copy import deepcopy


class Root:
    def __init__(self):
        self.items = {}
        self.index: Index = Index()

    def add_to_root(self, obj: Persistent):
        if self.items.get(obj.id):
            raise Exception("Object already in root. Try saving instead")
        else:
            obj = self.save(obj)
            self.items.update({obj.id: obj})

    def save(self, obj: Persistent):
        """Add or update persistent object
        
        Saves all Persistent objects in Index and replaces attributes containing Persistent objects as References"""
        obj = deepcopy(obj)

        for attr in dir(obj):
            if not attr.startswith("_"):
                attr_obj = getattr(obj, attr)
                if isinstance(attr_obj, Persistent):
                    setattr(obj, attr, self.save(attr_obj))
                elif isinstance(attr_obj, dict):
                    attr_obj_copy = attr_obj.copy()
                    for item in attr_obj_copy:
                        attr_obj_item = attr_obj_copy[item]
                        if isinstance(attr_obj_item, Persistent):
                            attr_obj_cpy[item] = self.save(attr_obj_item)
                    setattr(obj, attr, attr_obj_cpy)
                elif isinstance(attr_obj, list):
                    attr_obj_cpy = attr_obj.copy()
                    for item in range(len(attr_obj_cpy)):
                        attr_obj_item = attr_obj_cpy[item]
                        if isinstance(attr_obj_item, Persistent):
                            attr_obj_cpy[item] = self.save(attr_obj_item)
                    setattr(obj, attr, attr_obj_cpy)
                elif isinstance(attr_obj, tuple):
                    # convert tuple to list and back
                    attr_obj_cpy = list(attr_obj)
                    for item in range(len(attr_obj_cpy)):
                        attr_obj_item = attr_obj_cpy[item]
                        if isinstance(attr_obj_item, Persistent):
                            attr_obj_cpy[item] = self.save(attr_obj_item)
                    attr_obj_cpy = tuple(attr_obj_cpy)
                    setattr(obj, attr, attr_obj_cpy)
        return self.index.add(Item(obj))

    def get(self, id: UUID, cls_name: str = None) -> Persistent:
        """Returns specified object. Provide class name for faster access
        
        Rebuilds object by following References and retrieving actual objects"""
        try:
            obj = deepcopy(self.index.get(Reference(id, cls_name)).obj)
        except AttributeError:
            return None

        for attr in dir(obj):
            if not attr.startswith("_"):
                attr_obj = getattr(obj, attr)
                if isinstance(attr_obj, Reference):
                    index_item = self.index.get(attr_obj)
                    if index_item:
                        result_obj = self.get(
                            index_item.obj.id, index_item.cls_name)
                        setattr(obj, attr, result_obj)
                elif isinstance(attr_obj, dict):
                    new_attr_obj = {}
                    for item in attr_obj:
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            index_item = self.index.get(attr_obj_item)
                            if index_item:
                                result_obj = self.get(
                                    index_item.obj.id, index_item.cls_name)
                                new_attr_obj.update({item: result_obj})
                    setattr(obj, attr, new_attr_obj)
                elif isinstance(attr_obj, list):
                    new_attr_obj = []
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            index_item = self.index.get(attr_obj_item)
                            if index_item:
                                result_obj = self.get(
                                    index_item.obj.id, index_item.cls_name)
                                new_attr_obj.append(result_obj)
                    setattr(obj, attr, new_attr_obj)
                elif isinstance(attr_obj, tuple):
                    # convert tuple to list and back
                    new_attr_obj = []
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            index_item = self.index.get(attr_obj_item)
                            if index_item:
                                result_obj = self.get(
                                    index_item.obj.id, index_item.cls_name)
                                new_attr_obj.append(result_obj)
                    setattr(obj, attr, tuple(new_attr_obj))
        return obj

    def _delete(self, ref: Reference):
        obj = self.index.get(ref)
        if obj:
            obj = obj.obj
            for attr in dir(obj):
                if not attr.startswith("_"):
                    attr_obj = getattr(obj, attr)
                    if isinstance(attr_obj, Reference):
                        self._delete(attr_obj)
                    elif isinstance(attr_obj, dict):
                        for item in attr_obj:
                            attr_obj_item = attr_obj[item]
                            if isinstance(attr_obj_item, Reference):
                                self._delete(attr_obj_item)
                    elif isinstance(attr_obj, (list, tuple)):
                        for item in range(len(attr_obj)):
                            attr_obj_item = attr_obj[item]
                            if isinstance(attr_obj_item, Reference):
                                self._delete(attr_obj_item)
            return self.index.remove(ref)

    def delete(self, id: UUID, cls_name: str = None, recursive: bool = False):
        """Deletes specified object
        If recursive set to True will also delete any other Persistent object it or 
        its attributes might contain"""
        ref = Reference(id, cls_name)
        if recursive:
            self._delete(ref)
        else:
            self.index.remove(ref)
