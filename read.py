import pickle
from datetime import datetime

with open('test.pickle', 'rb') as handle:
    db = pickle.load(handle)

print(datetime.fromtimestamp(db.root.items[0].last_changed.timestamp()))

home = db.root.items[0]
home.rooms[0].name = 'testttttttttt'
home.mark_changed()
db.root.save(home)

print(datetime.fromtimestamp(db.root.items[0].last_changed.timestamp()))
