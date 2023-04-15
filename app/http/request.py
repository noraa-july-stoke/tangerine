# request.py

class Request:
    """Represents an HTTP request.

    Attributes:
        method: A string indicating the HTTP method.
        path: A string indicating the relative URL.
        headers: A dictionary mapping header names to values.
        body: A string containing the HTTP request body.
    """

    def __init__(self, method, path, headers, body):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
