# router.py
from route import Route

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

    def get(self, path):
        """Decorator for adding a GET route."""
        def decorator(view_func):
            self.add_route(path, view_func)
            return view_func
        return decorator

    def post(self, path):
        """Decorator for adding a POST route."""
        def decorator(view_func):
            self.add_route(path, view_func)
            return view_func
        return decorator

    def put(self, path):
        """Decorator for adding a PUT route."""
        def decorator(view_func):
            self.add_route(path, view_func)
            return view_func
        return decorator

    def delete(self, path):
        """Decorator for adding a DELETE route."""
        def decorator(view_func):
            self.add_route(path, view_func)
            return view_func
        return decorator

    def route(self, path):
        """Decorator for adding a route for all methods."""
        def decorator(view_func):
            self.add_route(path, view_func)
            return view_func
        return decorator
