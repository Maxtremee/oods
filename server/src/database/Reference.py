from uuid import UUID

class Reference:
    def __init__(self, id: UUID, cls_name: str = None):
        self.id: UUID = id
        self.cls_name: str = cls_name