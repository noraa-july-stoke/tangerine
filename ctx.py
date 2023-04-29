# ╔═╗┌┬┐─┐ ┬
# ║   │ ┌┴┬┘
# ╚═╝ ┴ ┴ └─
# File: ctx.py
# Description: This file contains the Ctx class which is used to store
# the request, response, keychain objects, and some useful methods.
from typing import Callable, TypeVar, Optional, Union, Dict
from socket import socket
from request import Request
from response import Response
from key_lime import KeyLime
from yuzu import Yuzu
T = TypeVar("T")

class Ctx:
    def __init__(self: T, request: Request, response: Response, keychain: Optional[KeyLime] = None, auth: bool = False) -> None:
        self.request = request
        self.response = response
        self.keychain = keychain
        self.auth = auth
        self.sock = None


    def req_intercept(self: T, request: Request) -> Request:
        self.request = request
        return self.request

    def res_intercept(self: T, response: Response) -> Response:
        self.response = response
        return self.response

    # !@#$ split this into two methods, one for successful methods, one for error methods
    def send(self: T, status: Optional[int] = None, body: Optional[Union[str, bytes]] = None, headers: Optional[Dict[str, str]] = None) -> None:
        if status:
            self.response.status_code = status
        if body:
            if isinstance(body, str):
                self.response.body = body.encode()
            else:
                self.response.body = body
        if headers:
            self.response.headers.update(headers)
        if 'Content-Type' not in self.response.headers:
            self.response.headers['Content-Type'] = 'application/json'  # Set default Content-Type



    def send_to_client(self: T) -> None:
        if self.sock:
            self.sock.sendall(self.response.to_bytes())
        else:
            raise ValueError("Socket not set for the context")

    def get_req_header(self: T, header: str) -> str:
        return self.request.headers.get(header)

    def set_res_header(self: T, header: str, value: str) -> None:
        self.response.headers[header] = value

    def set_auth(self: T, auth: bool) -> None:
        self.auth = auth

    @property
    def body(self):
        return self.response.body

    @body.setter
    def body(self, value):
        if isinstance(value, str):
            self.response.body = value.encode()
        else:
            self.response.body = value

    def set_socket(self: T, sock: socket) -> None:
        self.sock = sock

    def __repr__(self: T) -> str:
        return f'<Ctx: {self.request} {self.response}>'
