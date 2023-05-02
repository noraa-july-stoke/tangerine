#  ╦═╗┌─┐┌─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ╠╦╝├┤ └─┐├─┘│ ││││└─┐├┤
#  ╩╚═└─┘└─┘┴  └─┘┘└┘└─┘└─┘
# File: response.py
# Description: This file contains the Response class which is used to store
# the response data. This is used to determine the response status code,
# headers, and body.
from typing import TypeVar, Dict, Optional

T = TypeVar("T")
STATUS_CODES = {
    100: 'Continue',
    101: 'Switching Protocols',
    102: 'Processing',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    207: 'Multi-Status',
    208: 'Already Reported',
    226: 'IM Used',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    306: 'Switch Proxy',
    307: 'Temporary Redirect',
    308: 'Permanent Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Payload Too Large',
    414: 'URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Range Not Satisfiable',
    417: 'Expectation Failed',
    418: "I'm a Teapot",
    421: 'Misdirected Request',
    422: 'Unprocessable Entity',
    423: 'Locked',
    424: 'Failed Dependency',
    425: 'Too Early',
    426: 'Upgrade Required',
    428: 'Precondition Required',
    429: 'Too Many Requests',
    431: 'Request Header Fields Too Large',
    451: 'Unavailable For Legal Reasons',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported',
    506: 'Variant Also Negotiates',
    507: 'Insufficient Storage',
    508: 'Loop Detected',
    510: 'Not Extended',
    511: 'Network Authentication Required',
}


class Response:
    """
        The Response class is the class that is returned from the view function.
        It provides a way to construct the response that will be sent to the client.
    """
    def __init__(self, status_code=404, headers=None, body=''):
        # Set the status code, headers, and body of the response.
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body

    def set_header(self, name, value):
        # Set a header on the response.
        self.headers[name] = value

    def set_body(self, body):
        # Set the body of the response.
        self.body = body

    def render(self):
        # Render the response into an HTTP response string.
        # This function converts the response into a string that is sent to the client.
        # The string is a valid HTTP response.
        headers = '\r\n'.join([f'{name}: {value}' for name, value in self.headers.items()])
        return f'HTTP/1.1 {self.status_code}\r\n{headers}\r\n\r\n{self.body}'

    def to_bytes(self: T) -> bytes:
        status_line = f'HTTP/1.1 {self.status_code} {STATUS_CODES[self.status_code]}'
        # set key value pairs for headers
        headers = '\r\n'.join([f'{k}: {v}' for k, v in self.headers.items()])
        response_text = f'{status_line}\r\n{headers}\r\n\r\n'

        # Encode the response_text and the body
        return response_text.encode('utf-8') + (self.body.encode('utf-8') if isinstance(self.body, str) else self.body)



    def send(self, conn):
        # Send the response to the client.
        # This function sends the response to the client.
        conn.sendall(self.to_bytes())

    def to_dict(self) -> dict:
        """
        Creates dictionary representation of the Response Class

        Returns:
            dict: _description_
        """
        return {
            'status_code': self.status_code,
            'headers': self.headers,
            'body': self.body,
        }

    def __repr__(self):
        return f'<Response: {self.status_code}>'
