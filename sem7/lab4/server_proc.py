import socket
import time
from datetime import datetime
import multiprocessing
from server import Server


def run_server(server_port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    server_sock.bind(('', server_port))
    server_sock.listen()
    cid = 0
    while True:
        client_sock, client_addr = server_sock.accept()
        print(f'Client {cid} connected - {datetime.now().time()}')
        c_proc = multiprocessing.Process(
            target=serve_client, args=(client_sock, cid,), daemon=False)
        c_proc.start()
        cid += 1


def serve_client(client_sock, cid):
    request = client_sock.recv(1024)
    response = handle_request(request)
    client_sock.sendall(response)
    client_sock.close()
    print(f'Client {cid} served - {datetime.now().time()}')


request_map = Server.request_map


def handle_request(request):
    if not (request in request_map.keys()):
        return b"failed"
    time.sleep(request_map[request][1])
    return b"served"


if __name__ == '__main__':
    run_server(10000)
