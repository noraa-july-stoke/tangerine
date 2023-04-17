#  ╦═╗┌─┐┬ ┬┌┬┐┌─┐┬─┐
#  ╠╦╝│ ││ │ │ ├┤ ├┬┘
#  ╩╚═└─┘└─┘ ┴ └─┘┴└─
# File: router.py
# Description: This file contains the Router class which is used to store
# the routes and route the requests to the appropriate view function.

from tangerine import Route

class Router:
    """The Router class handles HTTP requests and routes them to the appropriate view function."""
    def __init__(self):
        self.routes = {}

    def add_route(self, method, path, view_func):
        """Add a new route to the router."""
        self.routes[(method, path)] = view_func
        print(self.routes, "===========READ/WRITE==========")

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
        return self.routes.get((method, path))
