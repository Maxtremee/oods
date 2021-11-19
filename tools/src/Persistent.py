import uuid
from datetime import datetime


class Persistent:
    '''Base class for OODS. Inherit from it to be able to save it in database'''
    def __init__(self):
        self.id = uuid.uuid4()
        self.last_changed = datetime.now()

    def mark_changed(self):
        '''Calling changes date of last change. 
        If not called changes to object will not be 
        processed - it's user responsibility to call it'''
        self.last_changed = datetime.now()
