from uuid import UUID


class Class:
    def __init__(self):
        self.paths = {}

    def add(self, id: UUID, path: list):
        """Add or update object of particular class to dict of paths"""
        self.paths.update({id: path})

    def get(self, id: UUID):
        """Get object's path with ID"""
        return self.paths.get(id)

    def remove(self, id: UUID):
        """Remove path with ID"""
        self.paths.pop(id)
