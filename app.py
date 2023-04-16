# TODO: add comments for all imports explaining what the module does
# provides infrastructure for writing asynchronous code using coroutines
import asyncio
# provides access to low-level networking primitives
import socket
# provides access to high-level networking primitives
import socketserver
# provides logging facilities for use in library code
import logging
# provides access to type hints
import typing as t
# provides access to the current interpreter stack frame
import functools
# provides access to inspecting live objects
import inspect
# provides json encoding and decoding
import json
# provides access to the operating system
import os
# provides a server for HTTP
import http.server
import sys
import weakref
import http
from collections.abc import Iterator as _abc_Iterator
from datetime import timedelta
from itertools import chain
from threading import Lock
from types import TracebackType

import click

from errors import TangerineError
from request import Request
from response import Response
from ctx import Ctx
from route import Route
from router import Router

logging.basicConfig(level=logging.DEBUG)

class Tangerine:
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port
        self.ctx = Ctx
        self.middleware = []

    def use(self, middleware_func):
        self.middleware.append(middleware_func)

    async def handle_client(self, reader, writer):
        while not reader.at_eof():
            data = await reader.read(1024)
            if data.startswith(b'GET / HTTP/1.1\r\n'):
                try:
                    res = Response(status_code=200, body='Hello, World!')
                    writer.write(res.render().encode('utf-8'))
                    await writer.drain()
                except TangerineError as e:
                    res = Response(
                        status_code=e.status_code,
                        body=json.dumps(e.to_dict())
                    )
                    writer.write(res.render().encode('utf-8'))
                    await writer.drain()
        writer.close()

    async def run_server(self):
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer((self.host, self.port), Handler)
        logging.info(f'Server sprouted @ 🌱{self.host}:{self.port}...')
        logging.info('Press Ctrl+C to stop the server')
        httpd.serve_forever()

    async def __aenter__(self):
        await self.run_server()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def start(self):
        try:
            asyncio.run(self.__aenter__())
        except KeyboardInterrupt:
            pass
        finally:
            asyncio.run(self.__aexit__(None, None, None))

app = Tangerine()
app.start()
