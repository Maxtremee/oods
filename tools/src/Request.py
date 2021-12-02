class Request:
    '''Class being sent over socket that contains appropriate query to database'''
    def __init__(self) -> None:
        self.query = None
        self.persistent_obj = None
        self.root_obj = None
        self.delete_id = None
        self.delete_recursive = False

    def _reset(self, argument):
        args = ['query', 'persistent_obj', 'root_obj', 'delete_id']
        if argument in args:
            args = [x for x in args if x != argument]
            for arg in args:
                setattr(self, arg, None)

    def add_query(self, query):
        '''Add Query object
        
        Resets other fields'''
        self.query = query
        self._reset('query')
    
    def add_to_save(self, persistent_obj):
        '''Add Persistent object to be saved in database
        
        Resets other fields'''
        self.persistent_obj = persistent_obj
        self._reset('persistent_obj')

    def add_to_root(self, root_obj):
        '''Add Persistent object that will be the root object
        
        Resets other fields'''
        self.root_obj = root_obj
        self._reset('root_obj')

    def delete(self, id, recursive = False):
        self.delete_id = id
        self.delete_recursive = recursive
        self._reset('delete_id')

