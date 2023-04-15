# response.py
class Response:
    """
        The Response class is the class that is returned from the view function.
        It provides a way to construct the response that will be sent to the client.
    """
    def __init__(self, status_code=200, headers=None, body=''):
        # Set the status code, headers, and body of the response.
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body

    def set_header(self, name, value):
        # Set a header on the response.
        self.headers[name] = value

    def set_body(self, body):
        # Set the body of the response.
        self.body = body

    def render(self):
        # Render the response into an HTTP response string.
        # This function converts the response into a string that is sent to the client.
        # The string is a valid HTTP response.
        headers = '\r\n'.join([f'{name}: {value}' for name, value in self.headers.items()])
        return f'HTTP/1.1 {self.status_code}\r\n{headers}\r\n\r\n{self.body}'

    def send(self, conn):
        # Send the response to the client.
        # This function sends the response to the client.
        conn.sendall(self.render().encode('utf-8'))

    def __repr__(self):
        return f'<Response: {self.status_code}>'
