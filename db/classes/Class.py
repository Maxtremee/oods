class Class:
    def __init__(self, name):
        self.paths = []
        self.name = name

    def add_item(self, path: list):
        found = None
        for pth in self.paths:
            if pth is path:
                found = pth
        if not found:
            self.paths.append(path)

