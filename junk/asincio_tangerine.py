import socket
import select
import json
from typing import List, Tuple, Callable, TypeVar, Type, Union, Dict
import os
import mimetypes
import re
import logging
import asyncio

from errors import TangerineError
from request import Request
from response import Response
from ctx import Ctx
from route import Route
from router import Router

T = TypeVar("T")
logging.basicConfig(level=logging.DEBUG)



class Tangerine:
    """
    The Tangerine class is a lightweight server configuration tool. It allows the setup and maintenance of a server
    on a given host and port. It has capabilities for handling HTTP requests and responses, route management,
    middleware processing, and socket creation.

    Attributes:
        host (str): The IP address or hostname where the server will be hosted.
        port (int): The port number where the server will be listening.
        routes (dict): A dictionary to manage routes. The keys are route URLs and the values are dictionaries with
        HTTP methods (as keys) and their associated handler functions (as values).
        middlewares (list): A list of middleware functions to be executed before the route handlers.
        static_route_pattern: Placeholder for static route patterns.
        static_route_pattern_re: Placeholder for compiled regex patterns of static routes.
    """

    def __init__(self: T, host: str = 'localhost', port: int = 8000) -> None:
        """
        Initializes a Tangerine instance with the specified host and port.

        Args:
            self (T): The instance of the Tangerine class.
            host (str, optional): The IP address or hostname where the server will be hosted. Defaults to 'localhost'.
            port (int, optional): The port number where the server will be listening. Defaults to 8000.
        """
        self.host: str = host
        self.port: int = port
        self.routes: Dict[str,
                          Dict[str, Callable[[Request, Response], None]]] = {}
        self.middlewares: List[Callable[[Request, Response], None]] = []
        self._create_socket()
        self.static_route_pattern = None
        # Add this line to define the regex instance variable
        self.static_route_pattern_re = None
        # self.config: Dict = None
        # self.ctx = Ctx(self)

    # def

    def _create_socket(self):
        """
        Creates a socket object. This method is typically called during the initialization of the Tangerine instance.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def register_route(self, method, path, handler):
        """
        Registers a route and its handler function in the routes dictionary.

        Args:
            method (str): The HTTP method of the route.
            path (str): The URL path of the route.
            handler (Callable): The function that handles the route.
        """
        if method not in self.routes:
            self.routes[method] = {}
        self.routes[method][path] = handler

    def use_router(self: T, router: Router) -> None:
        """
        Attaches a router to the Tangerine instance.

        Args:
            router (Router): The router to be used.
        """

        self.router = router

    def use(self, middleware: Callable[[Request, Response], None]) -> None:
        """
        Adds a middleware function to the middlewares list.

        Args:
            middleware (Callable): The middleware function to be added.
        """
        self.middlewares.append(middleware)

    # serve static files from route pattern and folder directory specified by user
    def static(self: T, route_pattern: str, dir_path: str):
        """
        Configures the Tangerine instance to serve static files from a directory.

        Args:
            route_pattern (str): The URL pattern that matches static file routes.
            dir_path (str): The directory from where the static files will be served.
        """
        self.static_route_pattern = route_pattern
        self.static_dir_path = dir_path
        # Use regular expressions to match the requested path against the static route pattern
        pattern = '^{}(/.*)?$'.format(self.static_route_pattern.rstrip('/'))
        self.static_route_pattern_re = re.compile(pattern)

    def parse_request(self, request: bytes) -> Tuple[str, str, Dict[str, str], Union[str, bytes]]:
        """
        Parses an HTTP request into its components.

        Args:
            request (bytes): The HTTP request to be parsed.

        Returns:
            Tuple[str, str, Dict[str, str], Union[str, bytes]]: A tuple containing the HTTP method, path, headers, and body of the request.
        """
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

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """
        Asynchronously handles a client connection.

        Args:
            reader (asyncio.StreamReader): The reader object for the client connection.
            writer (asyncio.StreamWriter): The writer object for the client connection.
        """
        request = await reader.read(4096)

        if request:
            method, path, headers, body = self.parse_request(request)
            req = Request(method, path, headers, body)
            res = Response()

            for middleware in self.middlewares:
                middleware(req, res)

            ctx = Ctx(req, res)
            ctx.set_socket(writer.get_extra_info('socket'))

            if self.static_route_pattern_re and self.static_route_pattern_re.match(path):
                file_path: str = os.path.join(self.static_dir_path, path[len(self.static_route_pattern):].lstrip('/'))

                if not os.path.exists(file_path) or not os.path.isfile(file_path):
                    ctx.send(404, 'File not found')
                else:
                    with open(file_path, 'rb') as f:
                        data = f.read()

                    content_type, _ = mimetypes.guess_type(file_path)
                    ctx.send(200, data, content_type=content_type)
            else:
                handler = self.router.get_route(method, path)
                if handler:
                    self.router.handle_route(method, path, ctx)
                else:
                    res.status_code = 404
                    res.headers['Content-Type'] = 'text/plain'
                    res.body = b'404 Not Found'

            await ctx.send_to_client()

            writer.close()
            await writer.wait_closed()

    async def run(self) -> None:
        """
        Starts the server and begins listening for connections asynchronously.

        This method sets up the server to listen for connections, logs the server startup information, and then
        enters a loop where it continuously serves incoming connections until an interrupt is received.
        """
        server = await asyncio.start_server(self.handle_client, self.host, self.port)

        logging.info(f' 🍊 Server sprouted @ {self.host}:{self.port}... 🌱🌱🌱')
        logging.info(' Press Ctrl+C to stop the server')

        async with server:
            await server.serve_forever()

    def start(self: T) -> None:
        """
        Starts the event loop.

        This method is the entry point for starting the server. It runs the event loop until the server is stopped.
        """
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            pass
