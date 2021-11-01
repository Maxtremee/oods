import pprint

from db.classes.Home import Home
from db.classes.Database import Database

try:
    Database.create("testdb")
    db = Database.load("testdb")
    db.add_to_root(Home("house_test", "kitchen"))
    db.save()
    pprint(db.classes)

except Exception as e:
    print(e)
