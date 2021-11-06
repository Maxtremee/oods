from uuid import UUID
from server.classes.Database import Database
from test_classes.Home import Home
from test_classes.Room import Room

try:
    Database.create("testdb")
    db = Database.load("testdb")
    room = Room('kitchen')
    room.id = UUID('{12345678-1234-5678-1234-567812345678}')
    home = Home('house', room)
    # db.add_to_root(home)
    print(db.get_by_id(room.id).name)
    room.name = 'bathroom'
    db.save(room)
    print(db.get_by_id(room.id).name)
    # print(db.index.classes.get('Room').paths)
    Database.save("testdb", db)

except Exception as e:
    print(e)
