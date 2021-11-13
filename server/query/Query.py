from uuid import UUID

from server.query.Operators import Operators


class Query:
    def __init__(self, root):
        self.root = root

    def get_by_id(self, id: UUID):
        """Return object by it's ID"""
        return self.root.get(id)

    def get_by_id_and_cls(self, id: UUID, cls_name: str):
        """Return object by it's ID and class name"""
        return self.root.get(id, cls_name)

    def get_all(self, cls_name: str) -> list:
        """Return all objects of given class"""
        res = []
        items = self.root.index.get_all_by_cls(cls_name)
        if items:
            for item in items:
                obj = items[item]
                obj = self.root.get(obj.obj.id, obj.cls_name)
                res.append(obj)
            return res

    def _action(self, obj, attr: str, operator: Operators, value) -> bool:
        """Helper function that decides whether given object has an attribute 
        whose value is in relation of given operator to given value"""
        try:
            if operator == Operators.EQ:
                return getattr(obj, attr) == value
            elif operator == Operators.NE:
                return getattr(obj, attr) != value
            elif operator == Operators.GT:
                return getattr(obj, attr) > value
            elif operator == Operators.LT:
                return getattr(obj, attr) < value
            elif operator == Operators.GE:
                return getattr(obj, attr) >= value
            elif operator == Operators.LE:
                return getattr(obj, attr) <= value
            else:
                return False
        except AttributeError:
            return False

    def _filter(self, items: list, attr: str, operator: str, value: any):
        return [x for x in items if self._action(x, attr, operator, value)]

    def get_all_where(self, cls_name: str, attr: str, operator: str, value: any):
        """Returns list of all objects of given class name that have an attribute 
        whose value is in relation of given operator to given value"""
        items = self.get_all(cls_name)
        if items:
            return self._filter(items, attr, operator, value)
