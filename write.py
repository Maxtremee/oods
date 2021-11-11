import logging
import pprint
import os
from uuid import UUID

from server.classes.Database import Database
from test_classes.Furniture import Furniture
from test_classes.Home import Home
from test_classes.Room import Room

pp = pprint.PrettyPrinter(indent=5,)
pp = pp.pprint

try:
    try:
        os.remove("test.db")
    except:
        pass
    Database.create("test")
    db = Database.load("test")
    room = Room('kitchen', 'cooker', 'drawers', 'knife')
    # room.id = UUID('{12345678-1234-5678-1234-567812345678}')
    home = Home('house', room)
    print(home.name)
    db.add_to_root(home)
    db.save(home)
    home.name = "test"
    db.save(home)
    home = db.get(home.id, "Home")
    print(home.name)
    print(db.index.classes.get("Home").get(home.id).uses)

    db.delete(home.id, "Home")
    home = db.get(home.id, "Home")
    print(home.name)
    print(db.index.classes.get("Home").get(home.id).uses)

    Database.save("test", db)

except Exception as e:
    logging.exception(e)
