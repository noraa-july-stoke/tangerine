#  ╦═╗┌─┐┬ ┬┌┬┐┌─┐┬─┐
#  ╠╦╝│ ││ │ │ ├┤ ├┬┘
#  ╩╚═└─┘└─┘ ┴ └─┘┴└─
# File: router.py
# Description: This file contains the Router class which is used to store
# the routes and route the requests to the appropriate view function.

from tangerine import Route, Request, Response
from typing import List, Tuple
from print_messages import print_debug

class Router:
    """The Router class handles HTTP requests and routes them to the appropriate view function."""
    def __init__(self, prefix: str = "", debug: bool = False):
        self.routes_dict = {}
        self.debug = debug
        self.prefix: str = prefix

    def add_route(self, method, path, view_func):
        """Add a new route to the router."""
        self.routes_dict[(method, path)] = view_func

    def get(self, path, view_func):
        """Add a new GET route to the router."""
        self.add_route('GET', path, view_func)

    def post(self, path, view_func):
        """Add a new POST route to the router."""
        self.add_route('POST', path, view_func)

    def put(self, path, view_func):
        """Add a new PUT route to the router."""
        self.add_route('PUT', path, view_func)

    def delete(self, path, view_func):
        """Add a new DELETE route to the router."""
        self.add_route('DELETE', path, view_func)

    def route(self, path, view_func):
        """Add a new route for all methods to the router."""
        self.add_route('GET', path, view_func)
        self.add_route('POST', path, view_func)
        self.add_route('PUT', path, view_func)
        self.add_route('DELETE', path, view_func)

    def get_route(self, method, path):
        """Get the view function for a given method and path."""
        return self.routes_dict.get((method, path))

    def get_decorator(self, path):
        def decorator(view_func):
            self.add_route('GET', path, view_func)
            return view_func
        return decorator

    def handle_route(self, method, path, ctx):
        """Handle the route given the method and path."""
        view_func = self.get_route(method, path)
        if view_func:
            if self.debug:
                view_func = self.debugger(view_func)
            view_func(ctx)

    def debugger(self, handler):
        def wrapper(ctx):
            if self.debug:
                print_debug(f">>> Debug: Before handler {handler.__name__, ctx}")

            handler(ctx)

            if self.debug:
                print_debug(f"<<< Debug: After handler {handler.__name__, ctx}")

        return wrapper


    # def handle_request(self, req: Request, res: Response) -> None:
    #     handler = self.get_route(req.method, req.path)
    #     if handler:
    #         if self.debug:
    #             handler = self.debugger(handler)
    #         handler(req, res)
    #     else:
    #         res.status_code = 404
    #         res.headers['Content-Type'] = 'text/plain'
    #         res.body = '404 Not Found'

    def routes (self):
        """Get all the routes in the router and collect them into a list and then return it."""
        routes: List[Tuple[str, str]] = []
        for route, view_func in self.routes_dict.items():
            # append a tuple of the route and the view_func to the routes list
            routes.append((route, view_func))
        return routes

    def send(self, status_code, body=None):
        self.response.status_code = status_code
        if body:
            self.response.body = body
        return self.response

    def debugger(self, handler):
        def wrapper(ctx):
            if self.debug:
                print_debug(f">>> Debug: Before handler {handler.__name__, ctx}")

            handler(ctx)

            if self.debug:
                print_debug(f"<<< Debug: After handler {handler.__name__, ctx}")

        return wrapper
