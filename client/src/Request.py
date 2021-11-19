class Request:
    def __init__(self) -> None:
        self.query = None
        self.persistent_obj = None
        self.root_obj = None

    def add_query(self, query):
        self.query = query
        self.persistent_obj = None
        self.root_obj = None
    
    def add_to_save(self, persistent_obj):
        self.persistent_obj = persistent_obj
        self.query = None
        self.root_obj = None

    def add_to_root(self, root_obj):
        self.root_obj = root_obj
        self.query = None
        self.persistent_obj = None
