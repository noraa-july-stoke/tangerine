i want to implement error handling like so:

```python

#tangerine_error.py

class TangerineError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

    def to_dict(self):
        return {
            'error': {
                'message': str(self),
                'status_code': self.status_code
            }
        }

#app.py (where tangerine class is defined)
def error(ctx, message, status_code):
    raise TangerineError(message, status_code)

possible implementation

```
