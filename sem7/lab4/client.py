import socket
import threading
import random
import time

N1, N2, N3, N4 = 20, 16, 33, 5
A1, A2, A3, A4= 'registration', 'home', 'users', 'bimbimbombom'
PURPOSES = [A1] * N1 + [A2] * N2 + [A3] * N3 + [A4] * N4

random.shuffle(PURPOSES)


def generate_client(idx: int, text: str):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 10000))
    client_sock.sendall(text.encode())
    data = client_sock.recv(1024)
    client_sock.close()
    print(f"I'm - {idx} and server response: {data.decode()}")


if __name__ == '__main__':
    clients = []
    start = time.time()
    for i, purpose in enumerate(PURPOSES):
        clients.append(threading.Thread(target=generate_client, args=(i, purpose), daemon=False))
        clients[i].start()

    for client in clients:
        client.join()
    print(f'Serve time: {int(time.time() - start)} seconds')