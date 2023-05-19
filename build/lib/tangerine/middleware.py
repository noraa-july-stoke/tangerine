import json

class Node:
    def __init__(self, fn, next_node=None):
        self.fn = fn
        self.next = next_node

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
