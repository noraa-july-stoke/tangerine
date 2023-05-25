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
from typing import List, Tuple, Callable, TypeVar, Union, Dict
import os
import mimetypes
import re
import logging
from colorama import Fore, Style

from .request import Request
from .response import Response
from .router import Router
from .print_messages import print_success
from debug_helpers import generate_diff
from .middleware import Middleware, MiddlewareResponse
from .ctx import Ctx
T = TypeVar("T")
logging.basicConfig(level=logging.DEBUG)

class Tangerine:
    def __init__(self: T, host: str = 'localhost', port: int = 8000, debug_level: int = 0) -> None:
        self.host: str = host
        self.port: int = port
        self.routes: Dict[str,
                          Dict[str, Callable[[Request, Response], None]]] = {}
        self.middlewares = Middleware()
        self._create_socket()
        self.static_route_pattern = None
        # Add this line to define the regex instance variable
        self.static_route_pattern_re = None
        self.debug_level: int = debug_level
        self.routers: Dict[str, Router] = {}
        # self.config: Dict = None
        # self.ctx = Ctx(self)
        self.response = Response()  # Initialize the Response object

    # def


    def debugger(self, middleware: Callable[[Ctx], None]) -> Callable[[Ctx], None]:
        def wrapper(ctx: Ctx) -> None:
            if self.debug_level > 0:
                old_state = ctx.to_dict()

                print(Fore.CYAN + f">>> Debug: Before middleware {middleware.__name__}" + Style.RESET_ALL)
                print("Current context state:")
                print(json.dumps(old_state, indent=2, default=str))

                if self.debug_level > 1:
                    input("Press Enter to continue...")

            middleware(ctx)

            if self.debug_level > 0:
                new_state = ctx.to_dict()

                print(Fore.CYAN + f"<<< Debug: After middleware {middleware.__name__}" + Style.RESET_ALL)
                print("New context state:")
                print(json.dumps(new_state, indent=2, default=str))

                print("Changes:")
                print(generate_diff(old_state, new_state))

                if self.debug_level > 1:
                    input("Press Enter to continue...")

        return wrapper

    def use(self, middleware: Callable[[Request, Response], None]) -> None:
        self.middlewares.use(middleware)

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


    def use_router(self, router: Router) -> None:
        router.set_debug_level(self.debug_level)
        self.routers[router.prefix] = router

    # serve static files from route pattern and folder directory specified by user
    def static(self: T, route_pattern: str, dir_path: str):
        self.static_route_pattern = route_pattern
        self.static_dir_path = dir_path
        # Use regular expressions to match the requested path against the static route pattern
        self.static_route_pattern_re = re.compile(route_pattern)


    def parse_request(self, request: bytes) -> Tuple[str, str, Dict[str, str], Union[str, bytes]]:
        # Decode the request and split it into its individual lines
        decoded_request = request.decode('utf-8')
        lines = decoded_request.split('\r\n')

        # Extract the method and path from the first line
        method, path, _ = lines[0].split(' ')

        # Extract the headers from the remaining lines
        headers = {}
        for line in lines[1:]:
            if line:
                parts = line.split(':')
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = ':'.join(parts[1:]).strip()
                    headers[key] = value

        # Extract the body, if present
        body: str = ''
        if '\r\n\r\n' in decoded_request:
            body = decoded_request.split('\r\n\r\n')[1]
        if "Content-Type" in headers and headers["Content-Type"] == "application/json" and body:
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                pass
        print("Headers:", headers)
        print("Body:", body)
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
            self.request = req  # Store the Request object in the Tangerine instance
            self.response = res  # Store the Response object in the Tangerine instance


            ctx = Ctx(req, res)
            ctx.set_socket(sock)  # Set the socket for the context
            self.middlewares.execute(ctx)

            # Check if the requested path matches any of the static routes using a regular expression
            if self.static_route_pattern_re and self.static_route_pattern_re.match(path):
                self.handle_static_route(ctx, path)

            else:
                # Check if the requested path matches any of the routes
                handler = None
                # Loop through routers to find a handler
                for prefix, router in self.routers.items():
                    if path.startswith(prefix):
                        handler = router.get_route(method, path[len(prefix):])
                        if handler:
                            router.handle_route(method, path[len(prefix):], ctx)
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
        file_path: str = os.path.join(self.static_dir_path, path.lstrip('/'))

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
        print_success(self.port, self.host, self.debug_level)
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
