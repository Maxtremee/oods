class Result:
    '''Class being returned on query to database.
    
    Attributes:
        status
        message
        data
    '''
    def __init__(self) -> None:
        self.status = 'ok'
        self.message = ''
        self.data = None

    def set_data(self, data):
        self.data = data

    def set_message(self, message):
        self.message = message

    def set_status_ok(self):
        self.status = 'ok'

    def set_status_err(self):
        self.status = 'err'