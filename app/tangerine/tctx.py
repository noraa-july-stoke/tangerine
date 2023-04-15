#tctx.py
# this context class will take in a request and response and will be passed to the view function
# the response will start with a default of 404 not found and will be changed by the view function
# the request will be passed to the view function and the self.request will be updated with
# any necessary changes such as a change in auth status or a change in the path.

from typing import Callable
from socket import socket

class Tctx:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    def req_intercept(self, request):
        self.request = request
        return self.request

    def res_intercept(self, response):
        self.response = response
        return self.response

    def send(self, conn: socket):
        self.response.send(conn)

    # def view(self, view_func):
    #     view_func(self)


    def __repr__(self):
        return f'<Tctx: {self.request} {self.response}>'
