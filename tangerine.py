# # ╔╦╗╔═╗╔╗╔╔═╗╔═╗╦═╗╦╔╗╔╔═╗
# #  ║ ╠═╣║║║║ ╦║╣ ╠╦╝║║║║║╣
# #  ╩ ╩ ╩╝╚╝╚═╝╚═╝╩╚═╩╝╚╝╚═╝
# # File: tangerine.py
# # Description: This file contains the Tangerine class which is used to
# # create a Tangerine application.


# # TODO: add comments for all imports explaining what the module does
# # provides infrastructure for writing asynchronous code using coroutines
# import asyncio
# # provides access to low-level networking primitives
# import socket
# # provides access to high-level networking primitives
# import socketserver
# # provides logging facilities for use in library code
# import logging
# # provides access to type hints
# from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union
# T = TypeVar("T")
# # provides access to the current interpreter stack frame
# import functools
# # provides access to inspecting live objects
# import inspect
# # provides json encoding and decoding
# import json
# # provides access to the operating system
# import os
# # provides a server for HTTP
# import http.server
# import sys
# import weakref
# import mimetypes
# import http
# from collections.abc import Iterator as _abc_Iterator
# from datetime import timedelta
# from itertools import chain
# from threading import Lock
# from types import TracebackType
# import click

# from errors import TangerineError
# from request import Request
# from response import Response
# from ctx import Ctx
# from route import Route
# from router import Router

# logging.basicConfig(level=logging.DEBUG)

# class Tangerine:

#     def __init__(self: T, host: str = 'localhost', port: int = 8000) -> None:
#         self.host: str = host
#         self.port: int = port
#         self.ctx: Ctx = Ctx
#         self.middleware: List[Tuple[Tuple, Callable[[Request, Response], None]]] = []

#     def use_router(self: T, middleware_funcs: List[Callable[[Request, Response], None]]) -> None:
#         """ Takes in a middleware list and appends it to self.middleware """
#         for method_route, view_func in middleware_funcs:
#             # print(method_route, view_func,  "======METHOD_ROUTE, VIEW FUNC=====")
#             if inspect.isfunction(view_func) and view_func.__name__ == '<lambda>':
#                 l_func = self.wrap_lambda(view_func)
#                 # print(l_func,  "======L_FUNC=====")
#                 self.middleware.append((method_route, self.wrap_lambda(view_func)))
#             else:
#                 self.middleware.append((method_route, view_func))

#     def wrap_lambda(self: T, func: Callable) -> Callable:
#         func_name = f'lambda_{id(func)}'
#         wrapped_func = lambda *args, **kwargs: func(*args, **kwargs)
#         wrapped_func.__name__ = func_name
#         return wrapped_func

#     def static(self: T, dir_path: str):
#         def static_handler(ctx: Ctx):
#             # print(dir_path, "============STATIC=========")

#             file_path: str = os.path.join(dir_path, ctx.req.path.lstrip('/'))

#             if not os.path.exists(file_path) or not os.path.isfile(file_path):
#                 ctx.send(404, 'File not found')
#                 return

#             with open(file_path, 'rb') as f:
#                 data = f.read()

#             ctx.send(data, content_type='text/html')

#         return static_handler

#     async def handle_client(self: T, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
#         print(reader, writer, "===========READ/WRITE==========")
#         while not reader.at_eof():
#             data = await reader.read(1024)
#             if data.startswith(b'GET / HTTP/1.1\r\n'):
#                 try:
#                     res = Response(status_code=200, body='Hello, World!')
#                     writer.write(res.render().encode('utf-8'))
#                     await writer.drain()
#                 except TangerineError as e:
#                     res = Response(
#                         status_code=e.status_code,
#                         body=json.dumps(e.to_dict())
#                     )
#                     writer.write(res.render().encode('utf-8'))
#                     await writer.drain()
#         writer.close()


#     async def run_server(self: T) -> None:
#         self.router = Router()
#         Handler = http.server.SimpleHTTPRequestHandler

#         httpd = socketserver.TCPServer((self.host, self.port), Handler)

#         logging.info(f' 🍊 Server sprouted @ {self.host}:{self.port}... 🌱🌱🌱')
#         logging.info(' Press Ctrl+C to stop the server')
#         httpd.serve_forever()


#     async def __aenter__(self: T) -> T:
#         await self.run_server()
#         return self

#     async def __aexit__(self: T, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
#         pass


#     def start(self: T) -> None:
#         try:
#             asyncio.run(self.__aenter__())
#         except KeyboardInterrupt:
#             pass
#         finally:
#             asyncio.run(self.__aexit__(None, None, None))

import socket
import select
import json
from typing import List, Tuple, Callable, TypeVar, Type, Union, Dict
import os
import mimetypes
import re
import logging
from colorama import init, Fore, Back, Style, Cursor

from errors import TangerineError
from request import Request
from response import Response
from ctx import Ctx
from route import Route
from router import Router
from print_messages import PrintMessage

T = TypeVar("T")
logging.basicConfig(level=logging.DEBUG)



class Tangerine:
    def __init__(self: T, host: str = 'localhost', port: int = 8000, debug: bool = False) -> None:
        self.host: str = host
        self.port: int = port
        self.routes: Dict[str,
                          Dict[str, Callable[[Request, Response], None]]] = {}
        self.middlewares: List[Callable[[Request, Response], None]] = []
        self._create_socket()
        self.static_route_pattern = None
        # Add this line to define the regex instance variable
        self.static_route_pattern_re = None
        self.debug: bool = debug
        # self.config: Dict = None
        # self.ctx = Ctx(self)

    # def

    def _create_socket(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def register_route(self, method, path, handler):
        if method not in self.routes:
            self.routes[method] = {}
        self.routes[method][path] = handler

    def use_router(self: T, router: Router) -> None:
        self.router = router

    # serve static files from route pattern and folder directory specified by user
    def static(self: T, route_pattern: str, dir_path: str):
            self.static_route_pattern = route_pattern
            self.static_dir_path = dir_path
            # Use regular expressions to match the requested path against the static route pattern
            pattern = '^{}(/.*)?$'.format(self.static_route_pattern.rstrip('/'))
            self.static_route_pattern_re = re.compile(pattern)
            # print("STATIC ROUTE PATTERN", self.static_route_pattern, self.static_route_pattern_re, self.static_dir_path)

    def parse_request(self, request: bytes) -> Tuple[str, str, Dict[str, str], Union[str, bytes]]:
        # Split the request into its individual lines
        lines = request.decode('utf-8').split('\r\n')

        # Extract the method and path from the first line
        method, path, _ = lines[0].split(' ')

        # Extract the headers from the remaining lines
        headers = {}
        for line in lines[1:]:
            if line:
                key, value = line.split(': ')
                headers[key] = value

        # Extract the body, if present
        body = b''
        if '\r\n\r\n' in request.decode('utf-8'):
            body = request.decode('utf-8').split('\r\n\r\n')[1].encode('utf-8')

        return method, path, headers, body

    def handle_new_client(self, client_socket: socket.socket, inputs: List[socket.socket]) -> None:
        inputs.append(client_socket)

    def handle_existing_client(self, sock: socket.socket, inputs: List[socket.socket], outputs: List[socket.socket]) -> None:
        request = sock.recv(4096)
        if request:
            # Parse the HTTP request and extract the method, path, and headers
            method, path, headers, body = self.parse_request(request)

            # Create a Request object to encapsulate the request data
            req = Request(method, path, headers, body)

            # Create a Response object with default status code and headers
            res = Response()

            # Apply the middleware to the Request and Response objects
            for middleware in self.middlewares:
                middleware(req, res)

            ctx = Ctx(req, res)
            ctx.set_socket(sock)  # Set the socket for the context

            # Check if the requested path matches any of the static routes
            if self.static_route_pattern_re and self.static_route_pattern_re.match(path):
                self.handle_static_route(ctx, path)

            else:
                handler = self.router.get_route(method, path)
                if handler:
                    self.router.handle_route(method, path, ctx)
                else:
                    # No handler found for the requested route, return 404 Not Found
                    self.handle_not_found(ctx)

            # Send the HTTP response back to the client
            ctx.send_to_client()  # Send the response using the context
            sock.close()
            inputs.remove(sock)

        else:
            # Empty data from existing client connection, remove from inputs
            sock.close()
            inputs.remove(sock)

    def handle_static_route(self, ctx: Ctx, path: str) -> None:
        file_path: str = os.path.join(self.static_dir_path, path[len(self.static_route_pattern):].lstrip('/'))

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            ctx.send(404, 'File not found')
        else:
            with open(file_path, 'rb') as f:
                data = f.read()

            content_type, _ = mimetypes.guess_type(file_path)
            ctx.send(200, data, content_type=content_type)

    def handle_not_found(self, ctx: Ctx) -> None:
        ctx.send(404, b'404 Not Found')
        ctx.set_res_header('Content-Type', 'text/plain')

    def run(self) -> None:
        inputs = [self.server_socket]
        outputs = []
        PrintMessage(self.port, self.host, self.debug)

        while inputs:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)

            for sock in readable:
                if sock is self.server_socket:
                    # New client connection
                    client_socket, address = self.server_socket.accept()
                    self.handle_new_client(client_socket, inputs)

                else:
                    # Existing client connection with new data
                    self.handle_existing_client(sock, inputs, outputs)

    def start(self: T) -> None:
        try:
            self.run()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_socket.close()
