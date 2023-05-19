"""
File: ctx.py
Description: This file contains the Ctx class which is used to store
the request, response, keychain objects, and some useful methods.
from typing import Callable, TypeVar, Optional, Union, Dict, Any
"""

from typing import Callable, TypeVar, Optional, Union, Dict, Any
from socket import socket
from .request import Request
from .response import Response
from .key_lime import KeyLime
import json
from http.cookies import SimpleCookie

T = TypeVar("T")


class Ctx:
    """
    The Ctx class represents the context of an HTTP request/response cycle.

    Attributes:
        request (Request): The incoming HTTP request object.
        response (Response): The outgoing HTTP response object.
        keychain (Optional[KeyLime]): The KeyLime object containing any session
            information.
        auth (bool): A boolean indicating whether the request is authenticated
            or not.
        sock (Optional[socket]): The socket object used to send the response.

    Methods:
        req_intercept(request: Request) -> Request:
            Intercepts the incoming request and returns it.
        res_intercept(response: Response) -> Response:
            Intercepts the outgoing response and returns it.
        send(status: Optional[int] = None, body: Optional[Union[str, bytes]] = None,
             headers: Optional[Dict[str, str]] = None, content_type: Optional[str] = None) -> None:
            Sends the outgoing response with the given status code, body, headers
            and content type.
        send_to_client() -> None:
            Sends the outgoing response to the client.
        get_req_header(header: str) -> str:
            Returns the value of the specified header in the incoming request.
        set_res_header(header: str, value: str) -> None:
            Sets the value of the specified header in the outgoing response.
        set_auth(auth: bool) -> None:
            Sets the authenticated status of the request.
        set_socket(sock: socket) -> None:
            Sets the socket object used to send the response.
        __repr__() -> str:
            Returns a string representation of the Ctx object.

    """

    def __init__(self: T, request: Request, response: Response, keychain: Optional[KeyLime] = None, auth: bool = False) -> None:

        """
        Initialize a new Ctx object.

        :param request: The request object.
        :param response: The response object.
        :param keychain: Optional keychain object.
        :param auth: Optional boolean flag for authentication status.
        :param sock: Socket object.
        """

        self.request = request
        self.response = response
        self.keychain = keychain
        self.auth = auth
        self.sock: socket or None = None
        self.user = None

    def req_intercept(self: T, request: Request) -> Request:
        """
        Intercept and store the request object.

        :param request: The request object.
        :return: The request object.
        """

        self.request = request
        return self.request

    def res_intercept(self: T, response: Response) -> Response:
        """
        Intercept and store the response object.

        :param response: The response object.
        :return: The response object.
        """

        self.response = response
        return self.response

    def set_cookie(self: T, key: str, value: str, **kwargs) -> None:
        """
        Set a cookie in the response headers.

        :param key: The name of the cookie.
        :param value: The value of the cookie.
        :param kwargs: Additional attributes for the cookie such as 'expires', 'path', etc.
        """
        cookie = SimpleCookie()
        cookie[key] = value
        for attr, val in kwargs.items():
            cookie[key][attr] = val

        if 'Set-Cookie' in self.response.headers:
            self.response.headers['Set-Cookie'] += f', {cookie[key].OutputString()}'
        else:
            self.response.headers['Set-Cookie'] = cookie[key].OutputString()

    # !@#$ split this into two methods, one for successful methods, one for error methods
    def send(self: T, status: Optional[int] = None, body: Optional[Union[str, bytes]] = None, headers: Optional[Dict[str, str]] = None, content_type: Optional[str] = None) -> None:
        """
        Send a response to the client with the specified status, body, headers, and content type.

        :param status: Optional status code.
        :param body: Optional response body.
        :param headers: Optional headers dictionary.
        :param content_type: Optional content type string.
        """

        if status:
            self.response.status_code = status
        if body:
            if isinstance(body, str):
                self.response.body = body.encode()
            else:
                self.response.body = body
        if headers:
            self.response.headers.update(headers)
        if content_type:
            self.response.headers['Content-Type'] = content_type
        elif 'Content-Type' not in self.response.headers:
            # Set default Content-Type
            self.response.headers['Content-Type'] = 'application/json'

    def send_to_client(self: T) -> None:
        """
        Send the response to the client using the socket.
        """

        if self.sock:
            self.sock.sendall(self.response.to_bytes())
        else:
            raise ValueError("Socket not set for the context")

    def get_req_header(self: T, header: str) -> str:
        """
        Get a specific request header value.

        :param header: Header key.
        :return: Header value.
        """

        return self.request.headers.get(header)

    def set_res_header(self: T, header: str, value: str) -> None:
        """
        Set a specific response header value.

        :param header: Header key.
        :param value: Header value.
        """

        self.response.headers[header] = value

    def set_auth(self: T, auth: bool) -> None:
        """
        Set the authentication status.

        :param auth: Boolean flag for authentication status.
        """

        self.auth = auth

    @property
    def body(self):
        """
        Get the response body.
        """

        return self.response.body

    @body.setter
    def body(self, value):
        """
        Set the response body.

        :param value: New response body.
        """
        if isinstance(value, dict):
            self.response.body = json.dumps(value).encode()
        elif isinstance(value, str):
            self.response.body = value.encode()
        else:
            self.response.body = value

    def set_socket(self: T, sock: socket) -> None:
        """
        Set the socket for the context.

        :param sock: Socket object.
        """

        self.sock = sock

    def to_dict(self) -> Dict[str, Any]:
        return {
            'request': self.request.to_dict(),
            'response': self.response.to_dict(),
            'socket': f"<socket fd={self.sock.fileno()}>" if self.sock else None,
            'auth': self.auth,
        }

    def __getitem__(self, key: str) -> Any:
        if key == "headers":
            return self.request.headers
        elif key == "body":
            return self.request.body
        elif key == "user":
            return self.ctx.user
        else:
            raise KeyError(f"Invalid key: {key}")

    def __setitem__(self, key: str, value: Any) -> None:
        if key == "user":
            self.user = value
        else:
            raise KeyError(f"Invalid key: {key}")


    def __repr__(self: T) -> str:
        """
        Return a string representation of the Ctx object.

        :return: String representation of the Ctx object.
        """

        return f'<Ctx: {self.request} {self.response}>'
