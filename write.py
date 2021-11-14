import logging
import pprint
import os
from uuid import UUID

from server.Database import Database
from test_classes.Furniture import Furniture
from test_classes.Home import Home
from test_classes.Room import Room

pp = pprint.PrettyPrinter(indent=5)
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
    # print(home.name)
    db.add_to_root(home)
    # db.save(home)
    # home.name = "test"
    # ref = db.save(home)
    # print(ref.id)
    # print(ref.cls_name)
    home = db.get(home.id, "Home")
    print(home.rooms[0].furniture)
    # print(db.index.classes.get("Home").get(home.id).uses)

    # print(home.rooms[0].furniture)
    # home_item = db.index.classes.get("Home").get(home.id).obj
    # print(home_item.rooms)
    # for item in dir(home_item):
    #     if not item.startswith("_"):
    #         # print(item)
    #         print(getattr(home_item, item))

    # furniture = db.index.classes.get("Room").items
    # for item in furniture:
    #     print(furniture[item].obj.furniture[0])

    # print(home.name)
    # print(db.index.classes.get("Home").get(home.id).uses)
    # for room in home.rooms:
    #     print(room.name)
    #     for furniture in room.furniture:
    #         print(f"\t{furniture.name}")

    # rooms2 = db.query.get_all("Room")
    # for room in rooms2:
    #     print(room.name)
    #     print(room.furniture)
    # print(db.index.classes.get("Home").get(home.id).uses)
    # furniture = db.query.get_all_where("Furniture", "name", "ne", "tv")
    # if furniture:
    #     for fur in furniture:
    #         print(f"{fur.name} {fur.id}")
    # print(furniture[0].id)
    # db.delete(home.id, "Home")
    # print(db.index.classes.get("Home").get(home.id).uses)
    db.delete(home.main.furniture[0].id, "Furniture")
    home2 = db.get(home.id, "Home")
    print(home2.main.furniture)
    # print("\n")
    # furniture = db.query.get_all_where("Furniture", "name", "ne", "tv")
    # if furniture:
    #     for fur in furniture:
    #         print(f"{fur.name} {fur.id}")

    # print(db.index.classes.get("Home").get(home.id).uses)
    # home = db.get(home.id, "Home")
    # print(home.name)

    Database.save("test", db)

except Exception as e:
    logging.exception(e)
    Database.save("test", db)
