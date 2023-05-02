#  ╦═╗┌─┐┬ ┬┌┬┐┌─┐┬─┐
#  ╠╦╝│ ││ │ │ ├┤ ├┬┘
#  ╩╚═└─┘└─┘ ┴ └─┘┴└─
# File: router.py
# Description: This file contains the Router class which is used to store
# the routes and route the requests to the appropriate view function.
import json
from typing import List, Tuple, Callable, Dict
from colorama import Fore, Style
from copy import deepcopy

from tangerine import Route, Request, Response, Ctx
from debug_helpers import generate_diff, copy_context_without_socket


class Router:
    """The Router class handles HTTP requests and routes them to the appropriate view function."""
    def __init__(self, prefix: str = "", debug_level: int = 0):
        self.routes_dict = {}
        self.prefix: str = prefix
        self.debug_level: int = debug_level

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
            if self.debug_level > 0:
                view_func = self.debugger(view_func)
            view_func(ctx)

    def set_debug_level(self, debug_level: int):
        self.debug_level = debug_level

    def debugger(self, middleware: Callable[[Ctx], None]) -> Callable[[Ctx], None]:
        def wrapper(ctx: Ctx) -> None:
            if self.debug_level > 0:
                old_state = copy_context_without_socket(ctx)

                print(Fore.CYAN + f">>> Debug: After Route Handler {middleware.__name__}" + Style.RESET_ALL)
                print("Current context state:")
                print(json.dumps(old_state, indent=2, default=str))

                if self.debug_level > 1:
                    input("Press Enter to continue...")

            middleware(ctx)

            if self.debug_level > 0:
                new_state = copy_context_without_socket(ctx)

                print(Fore.CYAN + f"<<< Debug: After Route Handler: {middleware.__name__}" + Style.RESET_ALL)
                print("New context state:")
                print(json.dumps(new_state, indent=2, default=str))

                print("Changes:")
                print(generate_diff(old_state, new_state))

                if self.debug_level > 1:
                    input("Press Enter to continue...")

        return wrapper

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
