#  ╦═╗┌─┐┬ ┬┌┬┐┌─┐
#  ╠╦╝│ ││ │ │ ├┤
#  ╩╚═└─┘└─┘ ┴ └─┘
# File: route.py
# Description: This file contains the Route class which is used to store
# the routes and route the requests to the appropriate view function.
class Route:
    """Represents a single route in the application.

    Attributes:
        path (str): A string indicating the path of the route.
        methods (list): A list of HTTP methods supported by the route.
        handler (callable): The handler function for the route.
    """

    def __init__(self, path: str, methods: list, handler: callable):
        self.path = path
        self.methods = methods
        self.handler = handler

    def match(self, path: str) -> bool:
        """Check if the given path matches the route's path.

        Args:
            path (str): The path to check for a match.

        Returns:
            bool: True if the given path matches the route's path, False otherwise.
        """
        return path.startswith(self.path)
