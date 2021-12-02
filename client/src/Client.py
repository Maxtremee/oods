import socket
import pickle
import logging
from uuid import UUID

from oodstools import Persistent, Query, Request, Result


class Client:
    '''Class allowing for connection with OODS database.
    Requires address and port of database'''
    buffer = 4096

    def __init__(self, address, port) -> None:
        self.socket = socket.socket()
        self.address = (address, port)
        self._connect()

    def _connect(self):
        self.socket.connect(self.address)

    def disconnect(self):
        '''Close connection'''
        self.socket.close()

    def _send_request(self, req) -> Result:
        try:
            req = pickle.dumps(req)
            self.socket.sendall(req)
            res = self.socket.recv(self.buffer)
            res = pickle.loads(res)
            return res
        except socket.timeout:
            self.socket.connect(self.address)
            self.socket.sendall(req)
            res = self.socket.recv(self.buffer)
            res = pickle.loads(res)
            return res
        except Exception as e:
            logging.exception(e)
            return None

    def _send_query(self, function_name, arguments):
        req = Request()
        query = Query(function_name, arguments)
        req.add_query(query)
        return self._send_request(req)

    def save(self, obj: Persistent):
        '''Save object to database'''
        req = Request()
        req.add_to_save(obj)
        return self._send_request(req)

    def add_to_root(self, obj: Persistent):
        '''Add object as root object'''
        req = Request()
        req.add_to_root(obj)
        return self._send_request(req)

    def get_by_id(self, id: UUID):
        '''Get object by ID'''
        function_name = "get_by_id"
        arguments = {"id": id}
        return self._send_query(function_name, arguments)

    def get_by_id_and_cls(self, id: UUID, cls_name: str):
        '''Get object by ID and class name'''
        function_name = "get_by_id_and_cls"
        arguments = {"id": id, "cls_name": cls_name}
        return self._send_query(function_name, arguments)

    def get_all(self, cls_name: str):
        '''Get all objects of given class'''
        function_name = "get_all"
        arguments = {"cls_name": cls_name}
        return self._send_query(function_name, arguments)

    def get_all_where(self, cls_name: str, filters: list, limit: int = None):
        '''Get filtered objects. Use FilterBuilder from 'oodstools' to create complex queries'''
        function_name = "get_all_where"
        arguments = {"cls_name": cls_name,
                     "filters": filters, "limit": limit}
        return self._send_query(function_name, arguments)

    def delete(self, id: UUID, recursive: bool = False):
        '''Delete object in database by ID.
        
        Set "recursive" to True if nested Persistent objects should also be deleted'''
        req = Request()
        req.delete(id, recursive)
        return self._send_request(req)
