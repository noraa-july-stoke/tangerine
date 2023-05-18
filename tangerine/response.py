#  ╦═╗┌─┐┌─┐┌─┐┌─┐┌┐┌┌─┐┌─┐
#  ╠╦╝├┤ └─┐├─┘│ ││││└─┐├┤
#  ╩╚═└─┘└─┘┴  └─┘┘└┘└─┘└─┘
# File: response.py
# Description: This file contains the Response class which is used to store
# the response data. This is used to determine the response status code,
# headers, and body.
from typing import TypeVar, Dict, Optional
import json

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
    The Response class is responsible for storing HTTP response data including the status code, headers, and body.
    This class provides methods to manipulate these response properties and render them into a proper HTTP response string.

    Attributes:
        status_code (int): The HTTP status code for the response.
        headers (Dict[str, str]): The headers for the response.
        body (str): The body of the response.
    """

    def __init__(self, status_code=404, headers=None, body=''):
        """
        Initializes a new instance of the Response class.

        Args:
            status_code (int, optional): The HTTP status code for the response. Defaults to 404.
            headers (Dict[str, str], optional): The headers for the response. Defaults to an empty dictionary.
            body (str, optional): The body of the response. Defaults to an empty string.
        """
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body

    def set_header(self, name, value):
        """
        Sets a header on the response.

        Args:
            name (str): The name of the header.
            value (str): The value of the header.
        """
        self.headers[name] = value

    def set_body(self, body):
        """
        Sets the body of the response.

        Args:
            body (str): The body of the response.
        """
        self.body = body

    def render(self):
        """
        Renders the response into an HTTP response string. This method converts the response properties into a valid
        HTTP response string that can be sent to the client.

        Returns:
            str: A string representation of the HTTP response.
        """
        # The string is a valid HTTP response.
        headers = '\r\n'.join([f'{name}: {value}' for name, value in self.headers.items()])
        return f'HTTP/1.1 {self.status_code}\r\n{headers}\r\n\r\n{self.body}'

    def to_bytes(self: T) -> bytes:
        """
        Converts the HTTP response string to bytes.

        Returns:
            bytes: The byte representation of the HTTP response.
        """
        status_line = f'HTTP/1.1 {self.status_code} {STATUS_CODES[self.status_code]}'
        # set key value pairs for headers
        headers = '\r\n'.join([f'{k}: {v}' for k, v in self.headers.items()])
        response_text = f'{status_line}\r\n{headers}\r\n\r\n'

        # Encode the response_text and the body
        return response_text.encode('utf-8') + (self.body.encode('utf-8') if isinstance(self.body, str) else self.body)


    def send(self, conn):
        """
        Sends the response to the client. This method converts the response into bytes and sends it to the client
        through the given connection.

        Args:
            conn: The connection to the client.
        """
        conn.sendall(self.to_bytes())

    def to_dict(self) -> dict:
        """
        Creates a dictionary representation of the Response object.

        Returns:
            dict: A dictionary representation of the Response object. Includes 'status_code', 'headers', and 'body'.
        """
        try:
            body_json = json.loads(self.body)
        except json.JSONDecodeError:
            body_json = self.body
        return {
            'status_code': self.status_code,
            'headers': self.headers,
            'body': body_json,
        }

    def __repr__(self):
        """
        Returns a string representation of the Response object, showing the status code.

        Returns:
            str: A string representation of the Response object.
        """
        return f'<Response: {self.status_code}>'
