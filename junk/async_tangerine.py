import asyncio
import aiohttp
from aiohttp import web

class Tangerine:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app.router.add_get('/', self.handle_request)

    async def handle_request(self, request):
        # Log request info
        print(f"Request: {request}")
        return web.Response(text="Hello, Tangerine!")

    def run(self):
        web.run_app(self.app, host=self.host, port=self.port)







async def test_server():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8000/') as response:
            assert response.status == 200
            text = await response.text()
            assert "Hello, Tangerine!" in text

def main():
    # Start the server
    server = Tangerine()
    loop = asyncio.get_event_loop()
    loop.create_task(server.run())

    # Allow some time for the server to start
    loop.run_until_complete(asyncio.sleep(1))

    # Test the server
    loop.run_until_complete(test_server())
    print("Test passed!")

if __name__ == "__main__":
    main()
