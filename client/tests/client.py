import argparse
from uuid import UUID
from time import sleep

from oodsclient import Client
from oodstools import FilterBuilder
from classes import *

# Define the port on which you want to connect
parser = argparse.ArgumentParser(description='OODS')
parser.add_argument('--addr', type=str,
                    help='Address to bind server to (default: localhost)')
parser.add_argument('--port', type=int,
                    help='Port number (default: 5000)')
args = parser.parse_args()

PORT = args.port or 5050
ADDR = args.addr or'localhost'

rooms = [Room('kitchen', 'cooker', 'drawers', 'knife'), Room(
            'living room', 'couch', 'tv', 'painting'), Room('bathroom', 'sink', 'bath', 'shower')]
home = Home('house', rooms)
test_id = UUID("12345678123456781234567812345678")
home.id = test_id
 
# connect to the server
db_client = Client(ADDR, PORT)


# send new home object
data = db_client.add_to_root(home)
print(f'Status: {data.status}')
print(f'Message: {data.message}')
print('Data:')
print(data.data)
print()

# query all Home objects
data = db_client.get_all("Home")
print(f'Status: {data.status}')
print(f'Message: {data.message}')
print('Data:')
print(data.data)
print()

# query specific furniture
filterBuilder = FilterBuilder()
filter = filterBuilder.where("name").eq("tv").build()
data = db_client.get_all_where("Furniture", [filter])
print(f'Status: {data.status}')
print(f'Message: {data.message}')
print('Data:')
print(data.data)
print()

sleep (6)

# query specific furniture
filterBuilder = FilterBuilder()
filter = filterBuilder.where("name").ne("tv").build()
data = db_client.get_all_where("Furniture", [filter])
print(f'Status: {data.status}')
print(f'Message: {data.message}')
print('Data:')
print(data.data)
print()

db_client.disconnect()