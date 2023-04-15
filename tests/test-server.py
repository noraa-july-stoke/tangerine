import asyncio
import socket
from contextlib import asynccontextmanager

from app import Tangerine


@asynccontextmanager
async def start_tangerine(host='localhost', port=8000):
    async with Tangerine(host=host, port=port) as app:
        server = asyncio.create_task(app.server.serve_forever())
        try:
            yield app
        finally:
            server.cancel()


async def test_tangerine():
    async with start_tangerine() as app:
        reader, writer = await asyncio.open_connection(app.host, app.port)
        writer.write(b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n')
        response = (await reader.read(1024)).decode()
        assert 'HTTP/1.1 200 OK' in response
        assert 'Hello, World!' in response
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    asyncio.run(test_tangerine())
