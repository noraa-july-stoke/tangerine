class Route:
    """Represents a single route in the application.

    Attributes:
        path: A string indicating the path of the route.
        methods: A list of HTTP methods supported by the route.
        handler: The handler function for the route.
    """

    def __init__(self, path, methods, handler):
        self.path = path
        self.methods = methods
        self.handler = handler

    def match(self, path):
        """Return True if the given path matches the route's path."""
        return self.path == path
