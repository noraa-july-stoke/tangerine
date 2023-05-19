#  ╦═╗┌─┐┬ ┬┌┬┐┌─┐┬─┐
#  ╠╦╝│ ││ │ │ ├┤ ├┬┘
#  ╩╚═└─┘└─┘ ┴ └─┘┴└─
# File: router.py
# Description: This file contains the Router class which is used to store
# the routes and route the requests to the appropriate view function.
import json
from typing import List, Tuple, Callable, Dict
from colorama import Fore, Style

from .ctx import Ctx
from debug_helpers import generate_diff

class Router:
    """The Router class handles HTTP requests and routes them to the appropriate view function.

    Attributes:
        routes_dict (dict): A dictionary containing the routes managed by the router.
        prefix (str): A string representing the common path prefix for all routes.
        debug_level (int): A dictionary containing the routes managed by the router.
    """
    def __init__(self, prefix: str = "", debug_level: int = 0):
        self.routes_dict = {}
        self.prefix: str = prefix
        self.debug_level: int = debug_level

    def add_route(self, method: str, path: str, view_func: callable):
        """Add a new route to the router.

        Args:
            method (str): A string representing the method.
            path (str): A string representing the path of the route.
            view_func (callable):
        """
        self.routes_dict[(method, path)] = view_func

    def get(self, path: str, view_func: callable):
        """Add a new GET route to the router.

        Args:
            path (str): A string representing the path of the route.
            view_func (callable): The view function to handle GET requests for this route.
        """
        self.add_route('GET', path, view_func)

    def post(self, path: str, view_func: callable):
        """Add a new POST route to the router.

        Args:
            path (str): A string representing the path of the route.
            view_func (callable): The view function to handle POST requests for this route.
        """
        self.add_route('POST', path, view_func)

    def put(self, path: str, view_func: callable):
        """Add a new PUT route to the router.

        Args:
            path (str): A string representing the path of the route.
            view_func (callable): The view function to handle PUT requests for this route.
        """
        self.add_route('PUT', path, view_func)

    def delete(self, path: str, view_func: callable):
        """Add a new DELETE route to the router.

        Args:
            path (str): A string representing the path of the route.
            view_func (callable): The view function to handle DELETE requests for this route.
        """
        self.add_route('DELETE', path, view_func)

    def route(self, path: str, view_func: callable):
        """Add a new route for all methods to the router.

        Args:
            path (str): A string representing the path of the route.
            view_func (callable): The view function to handle requests for this route.
        """
        self.add_route('GET', path, view_func)
        self.add_route('POST', path, view_func)
        self.add_route('PUT', path, view_func)
        self.add_route('DELETE', path, view_func)

    @staticmethod
    def auth_required(handler):
        def auth_wrapper(ctx, next=None):
            print(ctx.auth, ctx.user)
            if ctx.auth and ctx.user:
                handler(ctx)
            else:
                ctx.body = json.dumps({"message": "Unauthorized"})
                ctx.send(401, content_type='application/json')
        return auth_wrapper

    def get_route(self, method: str, path: str):
        """Get the view function for a given method and path.

        Args:
            method (str): A string representing the method.
            path (str): A string representing the path of the route.

        Returns:
            view_func (callable[[Ctx,None]]): The view function associated with the given method and path,
                or None if no matching route is found in the routes_dict.
        """
        return self.routes_dict.get((method, path))

    def get_decorator(self, path: str):
        def decorator(view_func):
            self.add_route('GET', path, view_func)
            return view_func
        return decorator

    def handle_route(self, method, path, ctx):
        """Handle the route given the method and path.

        Args:
            method (str): A string representing the method.
            path (str): A string representing the path.
            ctx (Ctx): A callable
        """
        view_func = self.get_route(method, path)
        if view_func:
            if self.debug_level > 0:
                view_func = self.debugger(view_func)
            view_func(ctx)

    def set_debug_level(self, debug_level: int):
        """Set the debugging level of router.

        Args:
            debug_level (int): A integer representing the debugging level.
        """
        self.debug_level = debug_level

    def debugger(self, middleware: Callable[[Ctx], None]) -> Callable[[Ctx], None]:
        """Wrap a middleware function with debugging information.

        Args:
            middleware (Callable[[Ctx], None]): The middleware function to wrap with debugging information.

        Returns:
            wapper (Callable[[Ctx], None]]): The wrapped middleware function that includes debugging information.
        """

        def wrapper(ctx: Ctx) -> None:
            if self.debug_level > 0:
                old_state = ctx.to_dict()

                print(Fore.CYAN + f">>> Debug: Before route handler: {middleware.__name__}" + Style.RESET_ALL)
                print("Current context state:")
                print(json.dumps(old_state, indent=2, default=str))

                if self.debug_level > 1:
                    input("Press Enter to continue...")

            middleware(ctx)

            if self.debug_level > 0:
                new_state = ctx.to_dict()

                print(Fore.CYAN + f"<<< Debug: After route handler: {middleware.__name__}" + Style.RESET_ALL)
                print("New context state:")
                print(json.dumps(new_state, indent=2, default=str))

                print("Changes:")
                print(generate_diff(old_state, new_state))

                if self.debug_level > 1:
                    input("Press Enter to continue...")

        return wrapper


    def routes (self):
        """Get all the routes in the router and collect them into a list and then return it.

        Args:
            None

        Returns:
            routes (list): A List is returned containing the routes on the Router.
        """
        routes: List[Tuple[str, str]] = []
        for route, view_func in self.routes_dict.items():
            # append a tuple of the route and the view_func to the routes list
            routes.append((route, view_func))
        return routes

    def send(self, status_code: int, body: str = None):
        """Create the response from the router.

        Args:
            status_code (int): An int that represents
            body (str, optional): A string that represents the body of the response.

        Returns:
            response (Response): The Response object with the specified status_code and body.
        """
        self.response.status_code = status_code
        if body:
            self.response.body = body
        return self.response
