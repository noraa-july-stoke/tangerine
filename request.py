# request.py
#import necessary modules for from_bytes method
from typing import Dict
from response import Response
import socket
import json

class Request:
    """Represents an HTTP request.

    Attributes:
        method: A string indicating the HTTP method.
        path: A string indicating the relative URL.
        headers: A dictionary mapping header names to values.
        body: A string containing the HTTP request body.
    """

    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body

    # parse and create a new request from a byte string
    def from_bytes(self, data):
        """Parse a byte string into a Request object."""
        # split the request into lines
        lines = data.decode().split('\r\n')

        # parse the request line
        request_line = lines[0].split(' ')
        method = request_line[0]
        path = request_line[1]

        # parse the headers
        headers = {}
        for line in lines[1:]:
            if line == '':
                break
            header = line.split(': ')
            headers[header[0]] = header[1]

        # parse the body
        body = lines[-1]

        return Request(method, path, headers, body)
