# ЛР #4: Параллельные алгоритмы

## Цель

Познакомить студента с инструментами, направленными на решение
задач, использующих технологии распараллеливания.
Задача
Моделирование нагрузки пользователей, которые обращаются почти
одновременно на сервер (запросы выстраиваются в очередь).
__Дано__:

- Действие 1: Регистрация на портале (время обработки T1, нагрузка
на процессор ~25%)
- Действие 2: Получение главной страницы (время обработки T2,
нагрузка на процессор ~15%)

- Действие 3: Просмотр перечня зарегистрированных пользователей
(время обработки T3, нагрузка на процессор ~1%)

- U1 – количество пользователей, которые отправляют запрос на
действие 1
- U2 – количество пользователей, которые отправляют запрос на
действие 2
- U3 – количество пользователей, которые отправляют запрос на
действие 3

## Решение

```python
def generate_client(idx: int, text: str):
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(('127.0.0.1', 10000))
    client_sock.sendall(text.encode())
    data = client_sock.recv(1024)
    client_sock.close()
    print(f"I'm - {idx} and server response: {data.decode()}")
```

```python
class Server(ABC):

    request_map = {...}

    ...

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
```

```python
class ServerLinear(Server):
    ...

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
```

```python
class ServerTread(Server):
    ...

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
```

```python
class ServerTread_cv(Server):
    def __init__(self) -> None:
        super().__init__()
        self.load = 0
        self.cv = threading.Condition()

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
```

```python
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

```

```python
counter = 0

async def run_server(host, server_port):
    server = await asyncio.start_server(serve_client, host, server_port)
    await server.serve_forever()


async def serve_client(reader, writer):
    global counter
    cid = counter
    counter += 1
    print(f'Client {cid} connected - {datetime.now().time()}')
    request = await reader.read(1024)
    response = await handle_request(request)
    writer.write(response)
    await writer.drain()
    writer.close()
    print(f'Client {cid} served - {datetime.now().time()}')


async def handle_request(request):
    if not (request in request_map.keys()):
        return b"failed"
    await asyncio.sleep(request_map[request][1])
    return b"served"

```

## Результаты

Данные:

```python
N1, N2, N3, N4 = 20, 16, 33, 5
A1, A2, A3, A4= 'registration', 'home', 'users', 'bimbimbombom'
PURPOSES = [A1] * N1 + [A2] * N2 + [A3] * N3 + [A4] * N4
```

Время выполнения:

- Последовательный сервер: 128 секунд
- Поточный сервер (без учета загрузки): 2 секунды
- Поточный сервер (с учетом загрузки): 10 секунд
- Сервер на процессах: 5 секунд
- Асинхронный сервер: 2 секунды

## Вывод

Лучше всего себя показали поточный и асинхронный серверы.
