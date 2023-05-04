#  ╦═╗┌─┐┌─┐ ┬ ┬┌─┐┌─┐┌┬┐
#  ╠╦╝├┤ │─┼┐│ │├┤ └─┐ │
#  ╩╚═└─┘└─┘└└─┘└─┘└─┘ ┴
# File: request.py
# Description: This file contains the Request class which is used to store
# the request data. This is used to determine the request method, path,
# headers, and body.

from typing import Dict
from response import Response
import socket
import json

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

    @classmethod
    def from_bytes(cls, data):
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
        body = '\r\n'.join(lines[lines.index('') + 1:]).strip()

        return cls(method, path, headers, body)


    def to_dict(self) -> dict:
        """
        Creates dictionary representation of the Response Class

        Returns:
            dict: _description_
        """
        return {
            'method': self.method,
            'path': self.path,
            'headers': self.headers,
            'body': self.body,
        }

    def __repr__(self):
        return f'<Request: {self.method} {self.path}>'
