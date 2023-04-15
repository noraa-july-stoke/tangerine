# TODO: add comments for all imports explaining what the module does
import asyncio
import socket
import logging
import typing as t
import functools
import inspect
import json
import os
import sys
import weakref
from collections.abc import Iterator as _abc_Iterator
from datetime import timedelta
from itertools import chain
from threading import Lock
from types import TracebackType


import click

from request import Request
from response import Response
from ctx import Ctx
from route import Route
from router import Router


class Tangerine:
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port

    async def handle_client(self, reader, writer):
        while not reader.at_eof():
            data = await reader.read(1024)
            if data.startswith(b'GET / HTTP/1.1\r\n'):
                res = Response(status_code=200, body='Hello, World!')
                writer.write(res.render().encode('utf-8'))
                await writer.drain()
        writer.close()

    async def __aenter__(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()

    def start(self):
        logging.info(f'Server sprouted @ 🌱{self.host}:{self.port}...')
        logging.info('Press Ctrl+C to stop the server')

        # create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the socket to a public host, and a port
        server_socket.bind((self.host, self.port))

        # become a server socket
        server_socket.listen(5)  # backlog of 5 connections

        while True:
            # wait for a connection
            client_socket, client_address = server_socket.accept()

            # read the request
            request_data = client_socket.recv(1024)

            # create a request object
            req = Request.from_bytes(request_data)

            # create a response object
            res = Response(status_code=200, body='Hello, World!')

            # send the response
            client_socket.sendall(res.render().encode('utf-8'))

            # close the connection
            client_socket.close()
