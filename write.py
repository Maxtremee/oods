import logging
import pprint
import os
from uuid import UUID

from server.Database import Database
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
    rooms = [Room('kitchen', 'cooker', 'drawers', 'knife'), Room(
        'living room', 'couch', 'tv', 'painting'), Room('bathroom', 'sink', 'bath', 'shower')]
    # room.id = UUID('{12345678-1234-5678-1234-567812345678}')
    home = Home('house', rooms)
    print(home.name)
    db.add_to_root(home)
    db.save(home)
    home.name = "test"
    db.save(home)
    home = db.get(home.id, "Home")
    print(home.name)
    print(db.index.classes.get("Home").get(home.id).uses)
    for room in home.rooms:
        print(room.name)
        for furniture in room.furniture:
            print(f"\t{furniture.name}")

    furniture = db.query.get_all_where("Furniture", "name", "lt", "tv")
    if furniture:
        for fur in furniture:
            print(fur.name)
    db.delete(home.id, "Home")
    # print(db.index.classes.get("Home").get(home.id).uses)
    # home = db.get(home.id, "Home")
    # print(home.name)

    Database.save("test", db)

except Exception as e:
    logging.exception(e)
    Database.save("test", db)
