import selectors
import socket
import sys

HOST_IP = "127.0.0.1"
HOST_PORT = sys.argv[1]

def serve_forever():
    sel = selectors.DefaultSelector()
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST_IP, HOST_PORT))
    lsock.listen()
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data="lsock")

    # event loop
    while True:
        event_tuples = sel.select(timeout=None)
        for key, mask in event_tuples:
            if key.data == "lsock": # the listening socket
                accept_conn(key.fileobj, sel)
                # key.fileobj is the connected socket
            else: # the connected socket
                service_conn(key, mask, sel)

def accept_conn(sock, sel):
    """
    Accepts a connection and register the connected 
    socket for reading
    """
    conn, addr = sock.accept()  # Should be ready to read
    conn.setblocking(False)
    event_mask = selectors.EVENT_READ
    sel.register(conn, event_mask, data=addr)

def service_conn(key, mask, sel):
    if mask & selectors.EVENT_READ: # ready to receive
        sock = key.fileobj
        recv_data = sock.recv(1024)
        if recv_data:
            # do something with the received data
            # then send response
            pass
        else:
            sel.unregister(sock)
            sock.close()

def handle_raw_data(data):
    pass