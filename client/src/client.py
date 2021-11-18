import argparse
import socket 
import pickle
from uuid import UUID
from classes import *
from shared.Filter import Filter
from shared.Query import Query
from shared.Request import Request

sock = socket.socket()        
 
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
sock.connect((ADDR, PORT))

# send new home object
req = Request()
req.add_to_root(home)
# home.name = 'test'
# query.add_to_save(home)
req = pickle.dumps(req, pickle.HIGHEST_PROTOCOL)
sock.send(req)
data = sock.recv(4096)
data = pickle.loads(data)
print(f'Status: {data.status}')
print(f'Message: {data.message}')
print('Data:')
print(data.data)
print()

# query all Home objects
req = Request()
function_name = "get_all"
arguments = {"cls_name": "Home"}
query = Query(function_name, arguments)
req.add_query(query)
req = pickle.dumps(req, pickle.HIGHEST_PROTOCOL)
sock.send(req)
data = sock.recv(4096)
data = pickle.loads(data)
print(f'Status: {data.status}')
print(f'Message: {data.message}')
print('Data:')
print(data.data)
print()

# query specific furniture
req = Request()
function_name = "get_all_where"
arguments = {"cls_name": "Furniture", "filters" :[Filter("name", "ne", "tv")], "limit" : 2}
query = Query(function_name, arguments)
req.add_query(query)
req = pickle.dumps(req, pickle.HIGHEST_PROTOCOL)
sock.send(req)
data = sock.recv(4096)
data = pickle.loads(data)
print(f'Status: {data.status}')
print(f'Message: {data.message}')
print('Data:')
print(data.data)
print()

# close the connection
sock.close()