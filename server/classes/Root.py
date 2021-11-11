from server.classes.Index import Index
from server.classes.Persistent import Persistent
from server.classes.Reference import Reference
from uuid import UUID


class Root:
    def __init__(self):
        self.items = {}
        self.index: Index = Index()

    def get(self, id: UUID, cls_name: str = None) -> Persistent:
        obj = self.index.get(id, cls_name).obj

        for attr in dir(obj):
            if not attr.startswith("_"):
                attr_obj = getattr(obj, attr)
                if isinstance(attr_obj, Reference):
                    indx = self.index.get(attr_obj.id, attr_obj.cls_name)
                    indx = self.get(indx.obj.id, indx.cls_name)
                    setattr(obj, attr, indx)
                elif isinstance(attr_obj, dict):
                    for item in attr_obj:
                        attr_obj_item = attr_obj[obj]
                        if isinstance(attr_obj_item, Reference):
                            indx = self.index.get(attr_obj_item.id, attr_obj_item.cls_name)
                            indx = self.get(indx.obj.id, indx.cls_name)
                            attr_obj[item] = indx
                            setattr(obj, attr, attr_obj)
                elif isinstance(attr_obj, list):
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            indx = self.index.get(attr_obj_item.id, attr_obj_item.cls_name)
                            indx = self.get(indx.obj.id, indx.cls_name)
                            attr_obj[item] = indx
                            setattr(obj, attr, attr_obj)
                elif isinstance(attr_obj, tuple):
                    for item in range(len(attr_obj)):
                        attr_obj_item = attr_obj[item]
                        if isinstance(attr_obj_item, Reference):
                            indx = self.index.get(attr_obj_item.id, attr_obj_item.cls_name)
                            indx = self.get(indx.obj.id, indx.cls_name)
                            attr_obj = list(attr_obj)
                            attr_obj[item] = indx
                            attr_obj = tuple(attr_obj)
                            setattr(obj, attr, attr_obj)
        return obj
                        

    def add_to_root(self, obj: Persistent):
        obj = self.save(obj)
        self.items.update({id: obj})

    def save(self, obj: Persistent):
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

    def delete(self, id: UUID, cls_name: str = None):
        if cls_name:
            self.index.remove(id, cls_name)
        else:
            self.index.remove(id)

    # def _path_to_str(self, path: list):
    #     """Parses a path into single string"""
    #     path_str = ""
    #     for i in range(1, len(path)):
    #         path_item = path[i]
    #         if isinstance(path_item, dict):
    #             attr_name = path_item['attr_name']
    #             if isinstance(path_item['index'], int):
    #                 index = path_item['index']
    #             else:
    #                 index = f"\"{path_item['index']}\""
    #             path_str += f"{attr_name}[{index}]."
    #         else:
    #             path_str += f"{path_item}."
    #     # Eliminate last extra dot
    #     path_str = path_str[:-1]
    #     return path_str

    # #add
    # def save(self, obj: Persistent):
    #     """Save received object to database

    #     Based on its actual class, search for it's path
    #     and update object at the end of it
    #     Update all other object attribute's paths if neccessary
    #     """
    #     #copy old object for comparison
    #     old_obj = self.get_by_obj(obj)

    #     #find path to obj
    #     path = self.index.get_path_by_id_and_cls_name(
    #         obj.id, type(obj).__name__)
    #     target = self.items.get(path[0])

    #     # special case for saving root objects
    #     if len(path) == 1:
    #         self.items.update({path[0]: obj})
    #         self.index.process_save(obj, path, old_obj)
    #         return

    #     path_str = self._path_to_str(path)
    #     # check if item to save is actually newer than saved item
    #     if magicattr.get(target, path_str).last_changed <= obj.last_changed:
    #         try:
    #             # set attribute to new object and process it's attributes
    #             magicattr.set(target, path_str, obj)
    #             self.items.update({path[0]: target})
    #             self.index.process_save(obj, path, old_obj)
    #         except Exception as e:
    #             logging.error(e)
    #     else:
    #         raise Exception('Item to save older than saved item')

    # def add_to_root(self, obj: Persistent):
    #     """Add object to database's Root"""
    #     found_obj = self.items.get(obj.id)

    #     # if found, update
    #     if found_obj:
    #         # check if item to save is actually newer than saved item
    #         if found_obj.last_changed <= obj.last_changed:
    #             self.items.update({obj.id: obj})
    #         else:
    #             raise Exception('Item to save older than saved item')
    #     # else just append
    #     else:
    #         self.items.update({obj.id: obj})
    #     # finally process the object
    #     self.index.process_save(obj, [obj.id])

    # def remove_from_root(self, id: UUID):
    #     """Remove object from database's Root"""
    #     found_obj = self.items.get(id)

    #     if found_obj:
    #         self.items.pop(id)
    #     else:
    #         raise Exception('No such object')

    # # get
    # def _get_object_with_path(self, path: list):
    #     """Returns object at the end of given path"""
    #     target = self.items.get(path[0])
    #     if len(path) > 1:
    #         path_str = self._path_to_str(path)
    #         return magicattr.get(target, path_str)
    #     else:
    #         return target

    # def get_by_id(self, id: UUID):
    #     path = self.index.get_path_by_id(id)
    #     return self._get_object_with_path(path)

    # def get_by_id_and_cls_name(self, id: UUID, cls_name: str):
    #     path = self.index.get_path_by_id_and_cls_name(id, cls_name)
    #     return self._get_object_with_path(path)

    # def get_by_obj(self, obj: Persistent):
    #     cls_name = type(obj).__name__
    #     path = self.index.get_path_by_id_and_cls_name(obj.id, cls_name)
    #     return self._get_object_with_path(path)

    # #remove
    # def _remove_obj(self, path: list):
    #     obj = self._get_object_with_path(path)
    #     self.index.process_remove(obj)

    #     target = self.items.get(path[0])
    #     path_str = self._path_to_str(path)
    #     magicattr.delete(target, path_str)

    # def remove_by_id(self, id: UUID):
    #     path = self.index.get_path_by_id(id)
    #     self._remove_obj(path)

    # def remove_by_id_and_cls_name(self, id: UUID, cls_name: str):
    #     path = self.index.get_path_by_id_and_cls_name(cls_name, id)
    #     self._remove_obj(path)
