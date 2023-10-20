import asyncio
from datetime import datetime
from server import Server


request_map = Server.request_map

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

if __name__ == '__main__':
    asyncio.run(run_server('127.0.0.1', 10000))
