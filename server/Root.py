from server.Index import Index
from server.Item import Item
from server.Persistent import Persistent
from server.query.Query import Query
from server.Reference import Reference
from uuid import UUID
from copy import deepcopy


class Root:
    def __init__(self):
        self.items = {}
        self.index: Index = Index()
        self.query: Query = Query(self)

    def add_to_root(self, obj: Persistent):
        if self.items.get(obj.id):
            raise Exception("Object already in root. Try saving instead")
        else:
            obj = self.save(obj)
            self.items.update({obj.id: obj})

    def save(self, obj: Persistent):
        """Add or update persistent object
        
        Saves all Persistent objects in Index and replaces attributes containing Persistent objects as References"""
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
        item = Item(obj)
        return self.index.add(item)

    def get(self, id: UUID, cls_name: str = None) -> Persistent:
        """Returns specified object. Provide class name for faster access
        
        Rebuilds object by following References and retrieving actual objects"""
        obj = deepcopy(self.index.get(Reference(id, cls_name)).obj)

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
                    attr_obj_copy = attr_obj.copy()
                    for item in attr_obj:
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            index_item = self.index.get(attr_obj_item)
                            if index_item:
                                result_obj = self.get(
                                    index_item.obj.id, index_item.cls_name)
                                attr_obj_copy[item] = result_obj
                            else:
                                attr_obj_cpy.pop(item)
                    setattr(obj, attr, attr_obj_copy)
                elif isinstance(attr_obj, list):
                    attr_obj_copy = attr_obj.copy()
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            index_item = self.index.get(attr_obj_item)
                            if index_item:
                                result_obj = self.get(
                                    index_item.obj.id, index_item.cls_name)
                                attr_obj_copy[item] = result_obj
                            else:
                                attr_obj_cpy.remove(attr_obj_item)
                    setattr(obj, attr, attr_obj_copy)
                elif isinstance(attr_obj, tuple):
                    # convert tuple to list and back
                    attr_obj_cpy = list(attr_obj)
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            index_item = self.index.get(attr_obj_item)
                            if index_item:
                                result_obj = self.get(
                                    index_item.obj.id, index_item.cls_name)
                                attr_obj_cpy[item] = result_obj
                            else:
                                attr_obj_cpy.remove(attr_obj_item)
                    attr_obj = tuple(attr_obj_cpy)
                    setattr(obj, attr, attr_obj)
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

    def delete(self, id: UUID, cls_name: str = None):
        """Deletes specified object and any Persistent object it might contain"""
        ref = Reference(id, cls_name)
        self._delete(ref)
