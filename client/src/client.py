import argparse
import socket 
import pickle
from uuid import UUID
from classes import *
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
 
query = Request()
query.add_to_root(home)
# home.name = 'test'
# query.add_to_save(home)
query = pickle.dumps(query)
sock.send(query)
data = sock.recv(4096)
data = pickle.loads(data)
print(type(data).__name__)
print(data.status)
print(data.message)

# close the connection
sock.close()