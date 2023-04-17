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
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union
T = TypeVar("T")
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
    def __init__(self: T, host: str = 'localhost', port: int = 8000) -> None:
        self.host: str = host
        self.port: int = port
        self.ctx: Ctx = Ctx
        self.middleware: List[Callable[[Request, Response], None]] = []

    def use(self: T, middleware_func: Callable[[Request, Response], None]):
        self.middleware.append(middleware_func)

    async def handle_client(self: T, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
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

    async def run_server(self: T) -> None:
        self.router = Router()
        Handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer((self.host, self.port), Handler)
        logging.info(f' 🍊 Server sprouted @ {self.host}:{self.port}.. 🌱🌱🌱')
        logging.info(' Press Ctrl+C to stop the server')
        httpd.serve_forever()


    async def __aenter__(self: T) -> T:
        await self.run_server()
        return self

    async def __aexit__(self: T, exc_type: Type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> None:
        pass


    def start(self: T) -> None:
        try:
            asyncio.run(self.__aenter__())
        except KeyboardInterrupt:
            pass
        finally:
            asyncio.run(self.__aexit__(None, None, None))
