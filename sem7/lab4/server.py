import time
from datetime import datetime
from enum import Enum
from abc import ABC, abstractclassmethod
import threading


class Request(Enum):
    REG = b'registration'
    HOME = b'home'
    USERS = b"users"


class Server(ABC):
    port = 10000

    load_reg = 25
    t_reg = 1.5

    load_home = 15
    t_home = 2

    load_users = 1
    t_users = 3

    request_map = {
        b"registration": (load_reg, t_reg),
        b"home": (load_home, t_home),
        b"users": (load_users, t_home)
    }

    def __init__(self) -> None:
        super(ABC).__init__()
        self.load = 0
        self.cv = threading.Condition()

    @abstractclassmethod
    def run_server(self):
        pass

    def serve_client(self, client_sock, cid):
        request = client_sock.recv(1024)
        response = self.handle_request(request)
        client_sock.sendall(response)
        client_sock.close()
        print(f'Client {cid} served - {datetime.now().time()}')

    def _processing(self, load, t):
        time.sleep(t)

    def handle_request(self, request: str):
        response = b"served"
        if not (request in self.request_map.keys()):
            return b"failed"
        self._processing(*self.request_map[request])
        return response
