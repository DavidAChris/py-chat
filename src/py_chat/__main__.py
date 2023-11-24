import sys

from py_chat.server import Server
from py_chat.client import Client

if __name__ == '__main__':
    # Get system args and start either a server or a client instance
    if 'server' in sys.argv:
        Server().run_server()
    elif 'client' in sys.argv:
        Client().run_client()
    else:
        print("Please specify a server or client instance")
