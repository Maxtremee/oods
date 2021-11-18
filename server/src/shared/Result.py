class Result:
    def __init__(self) -> None:
        self.status = 'ok'
        self.message = None
        self.data = None

    def set_data(self, data):
        self.data = data

    def set_message(self, message):
        self.message = message

    def set_status_ok(self):
        self.status = 'ok'

    def set_status_err(self):
        self.status = 'err'