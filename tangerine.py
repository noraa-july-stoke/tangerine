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
from print_messages import print_success
from debug_helpers import generate_diff
from yuzu import Yuzu
from key_lime import KeyLime
# from tangerine import Request, Response, Ctx, PrintMessage, Route, Router, TangerineError

T = TypeVar("T")
logging.basicConfig(level=logging.DEBUG)

class Tangerine:
    """
    Initializes the Tangerine application. This includes creating the server socket and setting the host, port, and routes.

    Attributes:
    host (str): The host for the server.
    port (int): The port for the server.
    routes (dict): The routes for the application.
    middlewares (list): A list of middleware functions.
    debug_level (int): The level of debugging information to display.

    Parameters:
    host (str): The host for the server. Defaults to 'localhost'.
    port (int): The port for the server. Defaults to 8000.
    debug_level (int): The level of debugging information to display. Defaults to 0.
    """
    
    def __init__(self: T, host: str = 'localhost', port: int = 8000, debug_level: int = 0) -> None:
        self.host: str = host
        self.port: int = port
        self.routes: Dict[str,
                          Dict[str, Callable[[Request, Response], None]]] = {}
        self.middlewares: List[Callable[[Ctx], None]] = []
        self._create_socket()
        self.static_route_pattern = None
        # Add this line to define the regex instance variable
        self.static_route_pattern_re = None
        self.debug_level: int = debug_level
        self.routers: Dict[str, Router] = {}
        # self.set_terminal_background_color()
        # self.config: Dict = None
        # self.ctx = Ctx(self)

    # def


    def debugger(self, middleware: Callable[[Ctx], None]) -> Callable[[Ctx], None]:
        """
        Wraps a middleware function for debugging. If the debug level is set to a value greater than 0, it will print the state of the context before and after the middleware is applied.

        Parameters:
        middleware (Callable[[Ctx], None]): The middleware function to wrap.

        Returns:
        Callable[[Ctx], None]: The wrapped middleware function.
        """
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
        """
        Adds a middleware function to the application.

        Parameters:
        middleware (Callable[[Request, Response], None]): The middleware function to add.
        """
        self.middlewares.append(middleware)

    def _create_socket(self):
        """
        Creates the server socket and sets the appropriate options.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def register_route(self, method, path, handler):
        """
        Registers a route for the application.

        Parameters:
        method (str): The HTTP method for the route (e.g., 'GET', 'POST', etc.).
        path (str): The path for the route.
        handler (Callable): The function to handle requests to the route.
        """
        if method not in self.routes:
            self.routes[method] = {}
        self.routes[method][path] = handler


    def use_router(self: T, router: Router) -> None:
        """
        Adds a router to the application.

        Parameters:
        router (Router): The router to add to the application.
        """
        router.set_debug_level(self.debug_level)
        self.routers[router.prefix] = router

    def static(self: T, route_pattern: str, dir_path: str):
        """
        Serves static files from the specified folder directory using the given route pattern.

        Parameters:
        route_pattern (str): The route pattern to match for static files.
        dir_path (str): The folder directory to serve static files from.
        """
        self.static_route_pattern = route_pattern
        self.static_dir_path = dir_path
        # Use regular expressions to match the requested path against the static route pattern
        self.static_route_pattern_re = re.compile(route_pattern)


    def parse_request(self, request: bytes) -> Tuple[str, str, Dict[str, str], Union[str, bytes]]:
        """
        Parses an incoming HTTP request and returns the method, path, headers, and body.

        Parameters:
        request (bytes): The raw HTTP request data.

        Returns:
        Tuple[str, str, Dict[str, str], Union[str, bytes]]: A tuple containing the method, path, headers, and body.
        """
        # Split the request into its individual lines
        lines = request.decode('utf-8').split('\r\n')

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
        if '\r\n\r\n' in request.decode('utf-8'):
            body = request.decode('utf-8').split('\r\n\r\n')[1]
        if "Content-Type" in headers and headers["Content-Type"] == "application/json" and body:
            body = json.loads(body)
        return method, path, headers, body




    def handle_new_client(self, client_socket: socket.socket, inputs: List[socket.socket]) -> None:
        """
        Handles a new client connection by adding the client's socket to the inputs list.

        Parameters:
        client_socket (socket.socket): The client's socket.
        inputs (List[socket.socket]): The list of input sockets.
        """
        inputs.append(client_socket)

    def handle_existing_client(self, sock: socket.socket, inputs: List[socket.socket], outputs: List[socket.socket]) -> None:
        """
        Handles an existing client connection by processing the client's request and sending a response.

        Parameters:
        sock (socket.socket): The client's socket.
        inputs (List[socket.socket]): The list of input sockets.
        outputs (List[socket.socket]): The list of output sockets.
        """
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
                if self.debug_level:
                    wrapped_middleware = self.debugger(middleware)
                wrapped_middleware(ctx)

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
        """
        Handles a static route by serving a static file, if it exists.

        Parameters:
        ctx (Ctx): The context for the request and response.
        path (str): The requested path.
        """
        file_path: str = os.path.join(self.static_dir_path, path.lstrip('/'))

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            ctx.send(404, 'File not found')
        else:
            with open(file_path, 'rb') as f:
                data = f.read()

            content_type, _ = mimetypes.guess_type(file_path)
            ctx.send(200, data, content_type=content_type)

    def handle_not_found(self, ctx: Ctx) -> None:
        """
        Handles a 404 Not Found error by setting the appropriate status code and headers in the response.

        Parameters:
        ctx (Ctx): The context for the request and response.
        """
        ctx.send(404, b'404 Not Found')
        ctx.set_res_header('Content-Type', 'text/plain')

    def run(self) -> None:
        """
        Starts the server and processes incoming client connections.
        """
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
        """
        Starts the server and handles KeyboardInterrupt and server socket closure.
        """
        try:
            self.run()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_socket.close()
