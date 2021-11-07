from server.classes.Index import Index
from server.classes.Persistent import Persistent
from uuid import UUID
import logging
import magicattr


class Root:
    def __init__(self):
        self.items = {}
        self.index = Index()

    def _path_to_str(self, path: list):
        """Parses a path into single string"""
        path_str = ""
        for i in range(1, len(path)):
            path_item = path[i]
            if isinstance(path_item, dict):
                attr_name = path_item['attr_name']
                index = path_item['index'] if isinstance(path_item['index'], int) else f"\"{path_item['index']}\""
                path_str += f"{attr_name}[{index}]."
            else:
                path_str += f"{path_item}."
        # Eliminate last extra dot
        path_str = path_str[:-1]
        return path_str

    def save(self, obj: Persistent):
        """Save received object to database
        
        Based on its actual class, search for it's path 
        and update object at the end of it
        Update all other object attribute's paths if neccessary
        """
        path = self.index.get_path_by_id_and_cls_name(obj.id, type(obj).__name__)

        target = self.items.get(path[0])
        path_str = self._path_to_str(path)

        # check if item to save is actually newer than saved item
        if magicattr.get(target, path_str).last_changed <= obj.last_changed:
            try:
                # set attribute to new object and process it's attributes
                magicattr.set(target, path_str, obj)
                self.items.update({path[0]: target})
                self.index.process(obj, path)
            except Exception as e:
                logging.error(e)
        else:
            raise Exception('Item to save older than saved item')

    def add_to_root(self, obj: Persistent):
        """Add object to database's Root"""
        found_obj = self.items.get(obj.id)

        # if found, update
        if found_obj:
            # check if item to save is actually newer than saved item
            if found_obj.last_changed <= obj.last_changed:
                self.items.update({obj.id: obj})
            else:
                raise Exception('Item to save older than saved item')
        # else just append
        else:
            self.items.update({obj.id: obj})
        # finally process the object
        self.index.process(obj, [obj.id])

    def remove_from_root(self, id: UUID):
        """Remove object from database's Root"""
        found_obj = self.items.get(id)

        if found_obj:
            self.items.pop(id)
        else:
            raise Exception('No such object')

    def _get_object_with_path(self, path: list):
        """Returns object at the end of given path"""
        target = self.items.get(path[0])
        path_str = self._path_to_str(path)
        return magicattr.get(target, path_str)

    def get_by_id(self, id: UUID):
        path = self.index.get_path_by_id(id)
        return self._get_object_with_path(path)

    def get_by_id_and_cls_name(self, id: UUID, cls_name: str):
        path = self.index.get_path_by_id_and_cls_name(cls_name, id)
        return self._get_object_with_path(path)


# class Root:
#     def __init__(self):
#         self.items = []
#         self.index = Index()

#     def save(self, obj: Persistent, path = []):
#         cls_name = type(obj).__name__
#         cls = self.classes.get(cls_name)
#         if not cls:
#             cls = Class(cls_name)
#         cls.add_item(path)
#         for attr in dir(obj):
#             attribute_obj = getattr(obj, attr)
#             if isinstance(attribute_obj, (list, dict, tuple)):
#                 path_cpy = path
#                 path_cpy.append(attr)
#                 for item in attribute_obj:
#                     self.save(item, path_cpy)
#             if isinstance(attribute_obj, Persistent):
#                 path_cpy = path
#                 path_cpy.append(attr)
#                 self.save(attribute_obj, path)

#     def _add_to_classes(self, obj: Persistent):
#         for clss in self.classes:
#             if clss == type(obj).name:
#                 clss.add_item(obj)

#     def add_to_root(self, obj: Persistent):
#         index = 0
#         found_obj = None

#         # look for object in list
#         for x in self.items:
#             if x.id == obj.id:
#                 found_obj = x
#                 break
#             index += 1

#         # if found, update
#         if found_obj:
#             if found_obj.last_changed <= obj.last_changed:
#                 self.items[index] = obj
#             else:
#                 raise Exception('Item to save older than saved item')
#         # else just append
#         else:
#             self.items.append(obj)

#     def remove_from_root(self, id: UUID):
#         index = 0
#         found_obj = None
#         for x in self.items:
#             if x.id == id:
#                 found_obj = x
#                 break
#             index += 1

#         if found_obj:
#             self.items.remove(index)
#         else:
#             raise Exception('No such object')
