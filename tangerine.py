# ╔╦╗╔═╗╔╗╔╔═╗╔═╗╦═╗╦╔╗╔╔═╗
#  ║ ╠═╣║║║║ ╦║╣ ╠╦╝║║║║║╣
#  ╩ ╩ ╩╝╚╝╚═╝╚═╝╩╚═╩╝╚╝╚═╝
# File: tangerine.py
# Description: This file contains the Tangerine class which is used to
# create a Tangerine application.
#==============================================================================

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
from print_messages import print_success, print_debug
# from tangerine import Request, Response, Ctx, PrintMessage, Route, Router, TangerineError

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
        self.routers: List[Router] = []
        # self.set_terminal_background_color()
        # self.config: Dict = None
        # self.ctx = Ctx(self)

    # def


    def debugger(self, middleware: Callable[[Ctx], None]) -> Callable[[Ctx], None]:
        def wrapper(ctx: Ctx) -> None:
            if self.debug:
                print(Fore.CYAN + f">>> Debug: Before middleware {middleware.__name__}" + Style.RESET_ALL)

            middleware(ctx)

            if self.debug:
                print(Fore.CYAN + f"<<< Debug: After middleware {middleware.__name__}" + Style.RESET_ALL)

        return wrapper

    def use(self, middleware: Callable[[Request, Response], None]) -> None:
        self.middlewares.append(middleware)


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
        self.routers.append(router)

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

            ctx = Ctx(req, res)
            ctx.set_socket(sock)  # Set the socket for the context
            for middleware in self.middlewares:
                wrapped_middleware = middleware
                if self.debug:
                    wrapped_middleware = self.debugger(middleware)
                wrapped_middleware(ctx)

            # Check if the requested path matches any of the static routes
            if self.static_route_pattern_re and self.static_route_pattern_re.match(path):
                self.handle_static_route(ctx, path)

            else:
                handler = None
                for router in self.routers:  # Loop through routers to find a handler
                    handler = router.get_route(method, path)
                    if handler:
                        router.handle_route(method, path, ctx)
                        break
                if not handler:  # No handler found for the requested route, return 404 Not Found
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
        print_success(self.port, self.host, self.debug)
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
