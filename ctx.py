# ╔═╗┌┬┐─┐ ┬
# ║   │ ┌┴┬┘
# ╚═╝ ┴ ┴ └─
# File: ctx.py
# this context class will take in a request and response and will be passed to the view function
# the response will start with a default of 404 not found and will be changed by the view function
# the request will be passed to the view function and the self.request will be updated with
# any necessary changes such as a change in auth status or a change in the path.

from typing import Callable, TypeVar
from socket import socket
from request import Request
from response import Response
from key_lime import KeyLime
from yuzu import Yuzu
T = TypeVar("T")

class Ctx:
    def __init__(self: T, request: Request, response: Response, keychain: KeyLime, auth: bool = False) -> None:
        self.request = request
        self.response = response
        self.keychain = keychain
        self.auth = auth

    def req_intercept(self: T, request: Request) -> Request:
        self.request = request
        return self.request

    def res_intercept(self: T, response: Response) -> Response:
        self.response = response
        return self.response

    def send(self: T, conn: socket) -> None:
        self.response.send(conn)

    def get_req_header(self: T, header: str) -> str:
        return self.request.headers.get(header)

    def set_res_header(self: T, header: str, value: str) -> None:
        self.response.headers[header] = value

    def set_auth(self: T, auth: bool) -> None:
        self.auth = auth

    # def view(self, view_func):
    #     view_func(self)

    def __repr__(self: T) -> str:
        return f'<Ctx: {self.request} {self.response}>'
