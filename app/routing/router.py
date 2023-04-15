# router.py
from .route import Route

class Router:
    """The Router class handles HTTP requests and routes them to the appropriate view function."""

    def __init__(self):
        self.routes = []

    def add_route(self, path, view_func):
        """Add a new route to the router."""
        self.routes.append(Route(path, view_func))

    def get_route(self, path):
        """Get the view function for a given path."""
        for route in self.routes:
            if route.match(path):
                return route.view_func
        return None
