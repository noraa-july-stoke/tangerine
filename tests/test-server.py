# python -m pytest -v tests/test-server.py to run this test
import asyncio
import socket
import requests
from contextlib import asynccontextmanager
import os
import time
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import Tangerine
import threading
pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
class start_tangerine:
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.host = host
        self.port = port

    async def __aenter__(self):
        self.app = Tangerine(self.host, self.port)
        await self.app.__aenter__()
        return self.app

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.app.__aexit__(exc_type, exc_val, exc_tb)


@pytest.mark.asyncio
class TestTangerine:
    def test_server(self):
        def run_server():
            from app import Tangerine
            app = Tangerine()
            app.start()

        server_thread = threading.Thread(target=run_server)
        server_thread.start()

        # Wait for the server to start up
        time.sleep(1)

        # Make a request to the server
        response = requests.get('http://localhost:8000/')
        assert response.status_code == 200
        assert response.text == 'Hello, World!'

if __name__ == '__main__':
    asyncio.run(TestTangerine.start_tangerine())
