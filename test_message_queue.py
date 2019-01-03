import threading
import time

from .message_queue import MessageQueue

def dequeue_action(msg_q, start_event, end_event):
    """
    perform the blocking dequeue action except sets the events
    """
    start_event.set()
    msg_q.dequeue()
    end_event.set()

def test_basic_enqueue():
    # arrange
    msg_q = MessageQueue()
    test_entry = (1, 2)
    
    # assume
    assert(len(msg_q) == 0)

    # act
    msg_q.enqueue(test_entry)

    # assert
    assert(len(msg_q) == 1)
    assert(msg_q.dequeue() == test_entry)

def test_signal_termination():
    # arrange
    msg_q = MessageQueue()
    start_event = threading.Event()
    end_event = threading.Event()
    thread_deq_empty = threading.Thread(target=dequeue_action, args=(msg_q, start_event, end_event))
    thread_deq_empty.start()
    time.sleep(0.1)

    # assume
    assert(start_event.is_set())
    assert(not end_event.is_set())

    # act
    msg_q.signal_termination()

    # assert
    thread_deq_empty.join(timeout=2)
    assert(not thread_deq_empty.is_alive())
    assert(end_event.is_set())

