import socket
import random

from .multicast_server import BaseServer
from .message import Message

class EchoServer(BaseServer):
    def __init__(self, _addr):
        super(EchoServer, self).__init__(_addr)

    def process_messages(self, key, msg):
        sock = key.fileobj
        sock.sendall(msg.encode())

def test_single_client_sanity():
    # arrange
    echo = EchoServer((LOCALHOST, 0)) # any port would do
    echo.serve_background()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg_encoded = Message(2, "1@1#2$@%^7%^$98&^&*^&*($%#$&%^&").encode()

    # assume
    assert(echo.addr[1] > 0)

    # act
    client.connect(echo.addr)
    client.sendall(msg_encoded)

    # assert
    assert(client.recv(len(msg_encoded) * 2) == msg_encoded)

    client.close()
    assert(echo.deinit())

def test_multi_client_sanity():
    # arrange
    echo = EchoServer((LOCALHOST, 0)) # any port would do
    echo.serve_background()

    msg_encoded = Message(199, "82734832748723142jsakdfjdskafjkdsafj").encode()
    NUM_OF_CLIENTS= 10
    clients = list()

    for i in range(NUM_OF_CLIENTS):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(echo.addr)
        clients.append(client)

    # act
    for client in clients:
        client.sendall(msg_encoded)

    # assert
    for client in clients:
        assert(client.recv(128) == msg_encoded)

    for client in clients:
        client.close()
    assert(echo.deinit())

LOCALHOST = "127.0.0.1"
