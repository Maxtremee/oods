from db.classes.Persistent import Persistent
from db.classes.Class import Class
from uuid import UUID


class Root:
    def __init__(self):
        self.items = []
        self.classes = {}

    def save(self, obj: Persistent, path = []):
        cls_name = type(obj).__name__
        cls = self.classes.get(cls_name)
        if not cls:
            cls = Class(cls_name)
        cls.add_item(path)
        for attr in dir(obj):
            attribute_obj = getattr(obj, attr)
            if isinstance(attribute_obj, (list, dict, tuple)):
                path_cpy = path
                path_cpy.append(attr)
                for item in attribute_obj:
                    self.save(item, path_cpy)
            if isinstance(attribute_obj, Persistent):
                path_cpy = path
                path_cpy.append(attr)
                self.save(attribute_obj, path)

    def _add_to_classes(self, obj: Persistent):
        for clss in self.classes:
            if clss == type(obj).name:
                clss.add_item(obj)

    def add_to_root(self, obj: Persistent):
        index = 0
        found_obj = None

        # look for object in list
        for x in self.items:
            if x.id == obj.id:
                found_obj = x
                break
            index += 1

        # if found, update
        if found_obj:
            if found_obj.last_changed <= obj.last_changed:
                self.items[index] = obj
            else:
                raise Exception('Item to save older than saved item')
        # else just append
        else:
            self.items.append(obj)

    def remove_from_root(self, id: UUID):
        index = 0
        found_obj = None
        for x in self.items:
            if x.id == id:
                found_obj = x
                break
            index += 1

        if found_obj:
            self.items.remove(index)
        else:
            raise Exception('No such object')
