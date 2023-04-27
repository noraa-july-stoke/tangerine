# ╔═╗┌┬┐─┐ ┬
# ║   │ ┌┴┬┘
# ╚═╝ ┴ ┴ └─
# File: ctx.py
# Description: This file contains the Ctx class which is used to store
# the request, response, keychain objects, and some useful methods.
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

    # !@#$ split this into two methods, one for successful methods, one for error methods
    def send(self: T, conn: socket) -> None:
        print(self.response.body, "===========RESPONSE BODY FROM CONTEXT==========")
        conn.sendall(self.response.body.encode())

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
