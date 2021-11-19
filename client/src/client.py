import socket
import pickle
import logging
from uuid import UUID

from oodstools import Persistent
from .Query import Query
from .Filter import Filter
from .Request import Request
from .Result import Result


class Client:
    buffer = 4096

    def __init__(self, address, port) -> None:
        self.socket = socket.socket()
        self.address = (address, port)
        self._connect()

    def _connect(self):
        self.socket.connect(self.address)

    def disconnect(self):
        self.socket.close()

    def _send_request(self, req) -> Result:
        try:
            req = pickle.dumps(req)
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
        req = Request()
        req.add_to_save(obj)
        return self._send_request(req)

    def add_to_root(self, obj: Persistent):
        req = Request()
        req.add_to_root(obj)
        return self._send_request(req)

    def get_by_id(self, id: UUID):
        function_name = "get_by_id"
        arguments = {id: id}
        return self._send_query(function_name, arguments)

    def get_by_id(self, id: UUID, cls_name: str):
        function_name = "get_by_id_and_cls"
        arguments = {"id": id, "cls_name": cls_name}
        return self._send_query(function_name, arguments)

    def get_all(self, cls_name: str):
        function_name = "get_all"
        arguments = {"cls_name": cls_name}
        return self._send_query(function_name, arguments)

    def get_all_where(self, cls_name: str, filters: list, limit: int = None):
        function_name = "get_all_where"
        arguments = {"cls_name": cls_name,
                     "filters": filters, "limit": limit}
        return self._send_query(function_name, arguments)


class FilterBuilder:
    def __init__(self) -> None:
        self.argument = ''
        self.operator = 'eq'
        self.value = None

    def where(self, argument):
        self.argument = argument
        return self

    def eq(self, value):
        self.operator = 'eq'
        self.value = value
        return self

    def ne(self, value):
        self.operator = 'ne'
        self.value = value
        return self

    def lt(self, value):
        self.operator = 'lt'
        self.value = value
        return self

    def gt(self, value):
        self.operator = 'gt'
        self.value = value
        return self

    def le(self, value):
        self.operator = 'le'
        self.value = value
        return self

    def ge(self, value):
        self.operator = 'ge'
        self.value = value
        return self

    def build(self):
        return Filter(self.argument, self.operator, self.value)
