from werkzeug.wrappers import Request
from werkzeug.serving import run_simple
from werkzeug.exceptions import NotFound
from werkzeug.utils import secure_filename
from werkzeug import Response
import os

class StaticServer:
    def __init__(self, static_folder: str):
        self.static_folder = static_folder

    def serve_file(self, filename: str):
        file_path = os.path.join(self.static_folder, secure_filename(filename))
        if not os.path.isfile(file_path):
            raise NotFound('File not found')
        return Response(open(file_path, 'rb'), mimetype='text/html')

    def __call__(self, environ, start_response):
        request = Request(environ)
        path = request.path.lstrip('/')
        if path == '':
            path = 'index.html'
        try:
            response = self.serve_file(path)
            return response(environ, start_response)
        except NotFound:
            response = Response('File not found', status=404)
            return response(environ, start_response)

if __name__ == '__main__':
    server = StaticServer('public')
    run_simple('localhost', 5000, server)
