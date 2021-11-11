from server.classes.Index import Index
from server.classes.Persistent import Persistent
from server.classes.Reference import Reference
from uuid import UUID


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
        for attr in dir(obj):
            if not attr.startswith("_"):
                attr_obj = getattr(obj, attr)
                if isinstance(attr_obj, Persistent):
                    setattr(obj, attr, self.save(attr_obj))
                elif isinstance(attr_obj, dict):
                    for item in attr_obj:
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Persistent):
                            attr_obj[item] = self.save(attr_obj_item)
                            setattr(obj, attr, attr_obj)
                elif isinstance(attr_obj, list):
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Persistent):
                            attr_obj[item] = self.save(attr_obj_item)
                            setattr(obj, attr, attr_obj)
                elif isinstance(attr_obj, tuple):
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Persistent):
                            # convert tuple to list and back
                            attr_obj = list(attr_obj)
                            attr_obj[item] = self.save(attr_obj_item)
                            attr_obj = tuple(attr_obj)
                            setattr(obj, attr, attr_obj)
        return self.index.add(obj)

    def get(self, id: UUID, cls_name: str = None) -> Persistent:
        """Returns specified object. Provide class name for faster access
        
        Rebuilds object by following References and retrieving actual objects"""
        obj = self.index.get(Reference(id, cls_name)).obj

        for attr in dir(obj):
            if not attr.startswith("_"):
                attr_obj = getattr(obj, attr)
                if isinstance(attr_obj, Reference):
                    indx = self.index.get(attr_obj)
                    indx = self.get(indx.obj.id, indx.cls_name)
                    setattr(obj, attr, indx)
                elif isinstance(attr_obj, dict):
                    for item in attr_obj:
                        attr_obj_item = attr_obj[obj]
                        if isinstance(attr_obj_item, Reference):
                            indx = self.index.get(attr_obj_item)
                            indx = self.get(indx.obj.id, indx.cls_name)
                            attr_obj[item] = indx
                            setattr(obj, attr, attr_obj)
                elif isinstance(attr_obj, list):
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            indx = self.index.get(attr_obj_item)
                            indx = self.get(indx.obj.id, indx.cls_name)
                            attr_obj[item] = indx
                            setattr(obj, attr, attr_obj)
                elif isinstance(attr_obj, tuple):
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            indx = self.index.get(attr_obj_item)
                            indx = self.get(indx.obj.id, indx.cls_name)
                            attr_obj = list(attr_obj)
                            attr_obj[item] = indx
                            attr_obj = tuple(attr_obj)
                            setattr(obj, attr, attr_obj)
        return obj

    def _delete(self, ref: Reference):
        obj = self.index.get(ref)
        for attr in dir(obj):
            attr_obj = getattr(obj, attr)
            if not attr.startswith("_"):
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
        self.index.remove(ref)


    def delete(self, id: UUID, cls_name: str = None):
        """Deletes specified object and any Persistent object it might contain"""
        ref = Reference(id, cls_name)
        self._delete(ref)
        
        
