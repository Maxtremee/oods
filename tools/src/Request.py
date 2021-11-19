class Request:
    '''Class being sent over socket that contains appropriate query to database'''
    def __init__(self) -> None:
        self.query = None
        self.persistent_obj = None
        self.root_obj = None

    def add_query(self, query):
        '''Add Query object
        
        Resets other fields'''
        self.query = query
        self.persistent_obj = None
        self.root_obj = None
    
    def add_to_save(self, persistent_obj):
        '''Add Persistent object to be saved in database
        
        Resets other fields'''
        self.persistent_obj = persistent_obj
        self.query = None
        self.root_obj = None

    def add_to_root(self, root_obj):
        '''Add Persistent object that will be the root object
        
        Resets other fields'''
        self.root_obj = root_obj
        self.query = None
        self.persistent_obj = None
