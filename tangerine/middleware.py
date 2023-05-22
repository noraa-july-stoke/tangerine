import json
from flask_cors import CORS

class Node:
    def __init__(self, fn, next_node=None):
        self.fn = fn
        self.next = next_node
        self.cors_middleware = None

class MiddlewareResponse(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

class UnauthorizedError(Exception):
    def __init__(self, message="Unauthorized"):
        self.message = message
        super().__init__(self.message)

class Middleware:
    def __init__(self):
        self.head = None
        self.tail = None

    def use(self, fn):
        new_node = Node(fn)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

        if fn == self.cors_middleware:
            self.cors_middleware = Node(fn)
        else:
            new_node = Node(fn)

    def execute(self, context):
        def dispatch(node):
            if node:
                try:
                    print(f"Executing middleware {node.fn.__name__}")
                    return node.fn(context, lambda: dispatch(node.next))
                except MiddlewareResponse as response:
                    self.handle_error(context, response)
            else:
                return None

        if self.cors_middleware:
            try:
                return self.cors_middleware.fn(context, lambda: dispatch(self.head))
            except MiddlewareResponse as response:
                self.handle_error(context, response)
        return dispatch(self.head)
       

    def handle_error(self, context, exception):
        if isinstance(exception, MiddlewareResponse):
            print(f"Sending response: {exception.status_code} {exception.message}")
        elif isinstance(exception, UnauthorizedError):  # Handle the custom exception
            context.body = json.dumps({"message": exception.message})
            context.send(401, content_type='application/json')
        else:
            print("An unhandled exception occurred:")
            print(exception)


app = Flask(__name__)
CORS(app)  # Apply CORS globally

middleware = Middleware()
middleware.use(CORS)  # Add CORS middleware to the custom Middleware class

if __name__ == '__main__':
    app.run()
