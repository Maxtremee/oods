import pickle
from datetime import datetime

with open('test.pickle', 'rb') as handle:
    db = pickle.load(handle)

print(datetime.fromtimestamp(db.root.items[0].last_changed.timestamp()))

home = db.root.items[0]
# home.rooms[0].name = 'testttttttttt'
# home.mark_changed()
# db.root.save(home)
# print(datetime.fromtimestamp(db.root.items[0].last_changed.timestamp()))
# for attr in dir(home):
#     if not attr.startswith("__"):
#         print(f"{attr} {type(getattr(home, attr))}")
#         print(getattr(home, attr))


def get_item(obj, *attributes):
    item = None
    for attr in attributes:
        item = getattr(obj, attr)
    return item

# print(get_item(home, "rooms"))
print(dir(home.rooms))
# print(type(home.rooms))