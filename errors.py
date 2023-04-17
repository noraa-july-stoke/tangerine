# ╔╦╗┌─┐┌┐┌┌─┐┌─┐┬─┐┬┌┐┌┌─┐╔═╗┬─┐┬─┐┌─┐┬─┐
#  ║ ├─┤││││ ┬├┤ ├┬┘││││├┤ ║╣ ├┬┘├┬┘│ │├┬┘
#  ╩ ┴ ┴┘└┘└─┘└─┘┴└─┴┘└┘└─┘╚═╝┴└─┴└─└─┘┴└─
# File: errors.py
# Server errors of all kinds are the bane of my existence
# So I want to figure out something cool to do with this class.
# open to ideas

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
