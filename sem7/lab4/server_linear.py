import socket
from datetime import datetime
from server import Server


class ServerLinear(Server):
    def __init__(self) -> None:
        super().__init__()

    def run_server(self):
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, proto=0)
        server_socket.bind(('', self.port))
        server_socket.listen()
        cid = 0
        while True:
            client_socket, client_addr = server_socket.accept()
            print(f'Client {cid} connected - {datetime.now().time()}')
            self.serve_client(client_socket, cid)
            cid += 1

    def serve_client(self, client_socket: socket.socket, cid: int):
        request = client_socket.recv(1024)
        response = self.handle_request(request)
        client_socket.sendall(response)
        client_socket.close()
        print(f'Client {cid} served - {datetime.now().time()}')


if __name__ == "__main__":
    server = ServerLinear()
    server.run_server()
    # print(server.load)
