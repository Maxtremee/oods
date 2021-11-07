import logging
import pprint
from uuid import UUID

from server.classes.Database import Database
from test_classes.Furniture import Furniture
from test_classes.Home import Home
from test_classes.Room import Room

pp = pprint.PrettyPrinter(indent=5,)
pp = pp.pprint

try:
    Database.create("testdb")
    db = Database.load("testdb")
    room = Room('kitchen', 'cooker', 'drawers', 'knife')
    room.id = UUID('{12345678-1234-5678-1234-567812345678}')
    home = Home('house', room)
    db.add_to_root(home)
    print(db.get_by_id(room.id).name)
    # print(db.get_by_id(furniture.id).name)
    room.name = 'bathroom'
    # furniture.name = 'cooker'
    db.save(room)
    print(db.get_by_id(room.id).name)
    # print(db.get_by_id(furniture.id).name)
    # print(db.index.classes)#.get('Furniture').paths)
    paths = db.index.classes.get('Furniture').paths
    # pp(paths)
    for item in paths:
        print(db.get_by_id(item).name)
    Database.save("testdb", db)

except Exception as e:
    logging.exception(e)
