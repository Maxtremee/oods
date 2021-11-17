import argparse
import logging
import signal
import sys
from threading import Lock
from Server import Server
from database.Database import Database
from classes import *

#parse arguments
parser = argparse.ArgumentParser(description='OODS - Object Oriented Database System server', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
# Required positional argument
parser.add_argument('db', type=str,
                    help='Database name')
# Optional arguments
parser.add_argument('--addr', type=str,
                    help='Address to bind server to', default='localhost')
parser.add_argument('--port', type=int,
                    help='Port number', default=5050)
parser.add_argument('--clients', type=int,
                    help='Maximum clients number', default=5)
parser.add_argument('--log-level', type=int,
                    help='Logging level', default=20)
args = parser.parse_args()

# default arguments
PORT = args.port
ADDR = args.addr
CLIENTS = args.clients
# LOG_LEVEL = args.log_level
LOG_LEVEL = 10
DB_NAME = args.db

# setup logging
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

# create shared mutex over root
mutex = Lock()


def lock_and_save():
    mutex.acquire()
    try:
        Database.save(DB_NAME, root)
    except Exception as e:
        logging.exception(e)
    mutex.release()


def signal_handler(sig, frame):
    logging.info('Exiting...')
    server.end()
    lock_and_save()
    sys.exit(0)


# register SIGINT handler
signal.signal(signal.SIGINT, signal_handler)

# start server
try:
    Database.create(DB_NAME)
    root, query_resolver = Database.load(DB_NAME)
    server = Server(ADDR, PORT, CLIENTS, root, query_resolver, mutex)
    server.listen()
except Exception as e:
    logging.exception(e)
    lock_and_save()
