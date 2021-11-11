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
    os.remove("testdb.db")
    Database.create("testdb")
    db = Database.load("testdb")
    room = Room('kitchen', 'cooker', 'drawers', 'knife')
    # room.id = UUID('{12345678-1234-5678-1234-567812345678}')
    home = Home('house', room)
    db.add_to_root(home)
    pp(db.index.classes.get('Home').paths)
    pp(db.index.classes.get('Room').paths)
    print('saving new attr')
    home.atest = room
    print(dir(home))
    db.save(home)
    # print(db.get_by_id(room.id).name)
    # print(home.name)
    # home = db.get_by_id(home.id)
    # print(home.name)
    # room.name = 'test'
    # furn = Furniture('test')
    # room.title = furn
    # db.save(room)
    # print(db.get_by_id(home.id).room.name)
    # print(db.get_by_id(home.id).room.title)
    pp(db.index.classes.get('Home').paths)
    pp(db.index.classes.get('Room').paths)
    # pp(db.index.classes.get('Furniture').paths)
    # print(db.get_by_id(furn.id).name)
    # db.remove_by_id(room.id)
    # print(db.get_by_id(room.id))
    # pp(db.index.classes.get('Home').paths)
    # pp(db.index.classes.get('Room').paths)
    # pp(db.index.classes.get('Furniture').paths)
    # print(db.index.classes.get('Furniture').paths)
    # paths = db.index.classes.get('Room').paths
    # for item in paths:
    #     obj = db.get_by_id(item)
    #     obj.item = 
    Database.save("testdb", db)

except Exception as e:
    logging.exception(e)
