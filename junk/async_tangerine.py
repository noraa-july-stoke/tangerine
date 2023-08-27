
import asyncio
import aiohttp
from aiohttp import web

# ============TEST 1================
# class Tangerine:
#     def __init__(self, host='localhost', port=8000):
#         self.host = host
#         self.port = port
#         self.app = web.Application()
#         self.app.router.add_get('/', self.handle_request)

#     async def handle_request(self, request):
#         # Log request info
#         print(f"Request: {request}")
#         return web.Response(text="Hello, Tangerine!")

#     def run(self):
#         web.run_app(self.app, host=self.host, port=self.port)







# async def test_server():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://localhost:8000/') as response:
#             assert response.status == 200
#             text = await response.text()
#             assert "Hello, Tangerine!" in text

# def main():
#     # Start the server
#     server = Tangerine()
#     loop = asyncio.get_event_loop()
#     loop.create_task(server.run())

#     # Allow some time for the server to start
#     loop.run_until_complete(asyncio.sleep(1))

#     # Test the server
#     loop.run_until_complete(test_server())
#     print("Test passed!")

# if __name__ == "__main__":
#     main()


# ============TEST 2================

# import asyncio
# from aiohttp import web

# class SimpleFramework:
#     def __init__(self):
#         self.app = web.Application()
#         self.routes = []

#     def route(self, path):
#         def decorator(func):
#             if asyncio.iscoroutinefunction(func):
#                 self.routes.append((path, func))
#             else:
#                 async def wrapper(request):
#                     return func(request)
#                 self.routes.append((path, wrapper))
#             return func
#         return decorator

#     def run(self):
#         for path, handler in self.routes:
#             self.app.router.add_get(path, handler)
#         web.run_app(self.app)

# # Usage:

# framework = SimpleFramework()

# @framework.route("/")
# async def hello(request):
#     return web.Response(text="Hello, async!")

# @framework.route("/sync")
# def hello_sync(request):
#     return web.Response(text="Hello, sync!")

# if __name__ == "__main__":
#     framework.run()

# ============TEST 3================
# import asyncio
# import socket

# class TangerineAsync:
#     def __init__(self, host='localhost', port=8000):
#         self.host = host
#         self.port = port
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.server_socket.bind((host, port))
#         self.server_socket.listen()
#         self.server_socket.setblocking(False)

#     async def handle_client(self, client_socket):
#         data = await self.loop.sock_recv(client_socket, 4096)
#         # You'll need to parse this data to understand the HTTP request.
#         print(data.decode())

#         # Assuming a simple GET request:
#         response = "HTTP/1.1 200 OK\r\nContent-Length: 16\r\n\r\nHello, Tangerine!"
#         await self.loop.sock_sendall(client_socket, response.encode())
#         client_socket.close()

#     async def run(self):
#         while True:
#             client_socket, addr = await self.loop.sock_accept(self.server_socket)
#             self.loop.create_task(self.handle_client(client_socket))

#     def start(self):
#         self.loop = asyncio.get_event_loop()
#         self.loop.run_until_complete(self.run())

# if __name__ == "__main__":
#     server = TangerineAsync()
#     server.start()

# ============TEST 4================
import asyncio
import socket
import re

class TangerineAsync:
    def __init__(self, host='localhost', port=8000):
        self.routes = {}
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        self.server_socket.setblocking(False)

    def route(self, path):
        def decorator(func):
            self.routes[path] = func
            return func
        return decorator

    async def handle_client(self, client_socket):
        data = await self.loop.sock_recv(client_socket, 4096)
        decoded_data = data.decode()

        # Parse the HTTP request for the path
        match = re.search(r'^GET\s(\/\w*)\sHTTP', decoded_data)
        if match:
            path = match.group(1)
            handler = self.routes.get(path)

            if handler:
                if asyncio.iscoroutinefunction(handler):  # Check if the function is a coroutine
                    response_content = await handler()
                else:
                    response_content = handler()
                response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_content)}\r\n\r\n{response_content}"
            else:
                response = "HTTP/1.1 404 NOT FOUND\r\nContent-Length: 9\r\n\r\nNot Found"
        else:
            response = "HTTP/1.1 400 BAD REQUEST\r\nContent-Length: 11\r\n\r\nBad Request"

        await self.loop.sock_sendall(client_socket, response.encode())
        client_socket.close()

    async def run(self):
        while True:
            client_socket, addr = await self.loop.sock_accept(self.server_socket)
            self.loop.create_task(self.handle_client(client_socket))

    def start(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.run())

# Usage
app = TangerineAsync()

@app.route("/hello")
def hello():
    return "Hello, Tangerine!"

@app.route("/async")
async def async_hello():
    await asyncio.sleep(1)
    return "Async Hello, Tangerine!"

if __name__ == "__main__":
    app.start()
