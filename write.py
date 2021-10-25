from db.classes.Home import Home
from db.classes.Database import Database

try:
    Database.create("testdb")
    db = Database.load("testdb")
    db.add_to_root(Home("house_test", "kitchen"))
    print(db.items[0].rooms[0].name)
except Exception as e:
    print(e)
