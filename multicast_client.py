"""
This is a sample multicast client for testing.
"""

import selectors
import socket

def start_conn(sel, target_addrs):
    """
    initialize the connections against multiple target addresses.
    sel is the selector object.
    target_addrs is a list of tuple (target_ip, target_port).
    """
    for target_addr in target_addrs:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(target_addr)
        event_mask = selectors.EVENT_WRITE
        sel.register(sock, event_mask)

def broadcast_message(sel, msg): # example 1
    """
    one-time broadcast.
    returns the number of targets broadcasted.
    """
    events = sel.select()
    for key, mask in events:
        sock = key.fileobj
        sock.sendall(msg)
        key.events
        sel.modify(sock, selectors.EVENT_READ)
    return len(events)

def service_conn(sel, msg_queue): # example 2
    """
    continuously send message and receive response
    msg_queue is a thread safe queue whose pop method is blocking
    """
    while True:
        events = sel.select()
        for key, mask in events:
            sock = key.fileobj
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)
                if recv_data:
                    print(recv_data.decode("utf-8"))
                else:
                    sel.unregister(sock)
            if mask & selectors.EVENT_WRITE:
                sock = key.fileobj
                sock.sendall(msg_queue.dequeue())
                sock.modify(sock, selectors.EVENT_READ)