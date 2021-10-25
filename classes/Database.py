from classes.Root import Root


class Database:
    def __init__(self, name):
        self.name = name
        self.root = Root()
