import socket

class Server:
    def __init__(self, host='localhost', port=8000):
        self.host = host
        self.port = port

    def start(self):
        print(f'Starting server at {self.host}:{self.port}...')

        # create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the socket to a public host, and a port
        server_socket.bind((self.host, self.port))

        # become a server socket
        server_socket.listen(1)

        while True:
            # wait for a connection
            client_socket, client_address = server_socket.accept()

            # read the request
            request_data = client_socket.recv(1024)

            # create a request object
            request = Request.from_bytes(request_data)

            # create a response object
            response = Response(status_code=200, body='Hello, World!')

            # send the response
            client_socket.sendall(response.render().encode('utf-8'))

            # close the connection
            client_socket.close()
