import uuid
from datetime import datetime


class Persistent:
    def __init__(self):
        self.id = uuid.uuid4()
        self.last_changed = datetime.now()

    def mark_changed(self):
        self.last_changed = datetime.now()
