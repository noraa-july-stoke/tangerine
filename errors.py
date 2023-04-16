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

# print(TangerineError("A stupid error", 200))
