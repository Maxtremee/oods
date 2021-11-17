import pickle
import socket
import threading
import logging

from shared.Request import Request
from shared.Result import Result
from classes import *

class Server:
    def __init__(self, host, port, max_clients, root, query_resolver, mutex):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.root = root
        self.query_resolver = query_resolver
        self.active = True
        self.threads = []
        self.mutex = mutex
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(self.max_clients)
        logging.info(f'Server is listening on {(self.host, self.port)}')
        while True:
            client, address = self.sock.accept()
            client.settimeout(300)
            thread = threading.Thread(target = self.listenToClient, args = (client, address, self.root, self.query_resolver, self.mutex))
            thread.start()
            self.threads.append(thread)

    def end(self):
        self.active = False
        for thread in self.threads:
            thread.join()

    def listenToClient(self, client, address, root, query_resolver, mutex):
        logging.debug(f'Started listening to client at {address}')
        size = 4096
        while self.active:
            try:
                data = client.recv(size)
                if data:
                    res = Result()
                    try:
                        data = pickle.loads(data)
                        if isinstance(data, Request):
                            mutex.acquire()
                            if data.query:
                                query = data.query
                                method = getattr(query_resolver, query.function_name)
                                payload = method(query.arguments)
                                res.set_data(payload)
                            elif data.persistent_obj:
                                root.save(data.persistent_obj)
                                logging.debug(f'Saved object {data.persistent_obj}')
                            elif data.root_obj:
                                root.add_to_root(data.root_obj)
                                logging.debug(f'Added new object to root {data.root_obj}')
                            mutex.release()
                        else:
                            logging.warn(f'Wrong request. Object type: {type(data).__name__}')
                    except Exception as e:
                        res.set_status_err()
                        res.set_message(str(e))
                        res.set_data(None)
                        logging.exception(e)
                    finally:
                        res = pickle.dumps(res, pickle.HIGHEST_PROTOCOL)
                        client.send(res)
            except Exception as e:
                logging.error(e)
                client.close()
                break
        client.close()
