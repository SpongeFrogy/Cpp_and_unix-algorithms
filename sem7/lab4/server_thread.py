import socket
import threading
from datetime import datetime
import time

from server import Server


class ServerTread_cv(Server):
    def __init__(self) -> None:
        super().__init__()

    def wait_for_load(self, request_load: int):
        if self.load + request_load > 100:
            with self.cv:
                self.cv.wait()

    def _processing(self, request_load: int, t):
        self.wait_for_load(request_load)
        self.load += request_load
        time.sleep(t)
        self.load -= request_load
        with self.cv:
            self.cv.notify()

    def run_server(self):
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, proto=0)
        server_socket.bind(('', self.port))
        server_socket.listen()
        cid = 0
        while True:
            client_sock, client_addr = server_socket.accept()
            print(f'Client {cid} connected - {datetime.now().time()}')
            c_thread = threading.Thread(
                target=self.serve_client, args=(client_sock, cid), daemon=False)
            c_thread.start()
            cid += 1


class ServerTread(Server):
    def __init__(self) -> None:
        super().__init__()

    def run_server(self):
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, proto=0)
        server_socket.bind(('', self.port))
        server_socket.listen()
        cid = 0
        while True:
            client_sock, client_addr = server_socket.accept()
            print(f'Client {cid} connected - {datetime.now().time()}')
            c_thread = threading.Thread(
                target=self.serve_client, args=(client_sock, cid), daemon=False)
            c_thread.start()
            cid += 1


if __name__ == '__main__':
    server = ServerTread()
    server.run_server()
