import threading
import time
import random

from concurrent.futures import ThreadPoolExecutor

from .message_queue import MessageQueue

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

def test_dequeue_stress():
    # arrange
    msg_q = MessageQueue()

    TOTAL_ENTRY = 2500
    i_sum = [0] # use array as convenient integer wrapper
    i_sum_lock = threading.Lock()
    EXPECTED_SUM= (TOTAL_ENTRY - 1) * TOTAL_ENTRY / 2

    producer_pool = ThreadPoolExecutor(36)
    consumer_pool = ThreadPoolExecutor(36)

    def enqueue_action(i):
        time.sleep(random.uniform(5E-9, 8E-9))
        msg_q.enqueue(i)

    def dequeue_action():
        i = msg_q.dequeue()
        with i_sum_lock: # (O_O) += is not atomic!
            i_sum[0] += i

    # act
    for i in range(TOTAL_ENTRY):
        producer_pool.submit(enqueue_action, i)
        consumer_pool.submit(dequeue_action)

    consumer_pool.shutdown()
    producer_pool.shutdown()

    # assert
    assert(i_sum[0] == EXPECTED_SUM)


def test_signal_termination():
    # arrange
    msg_q = MessageQueue()
    start_event = threading.Event()
    end_event = threading.Event()

    def dequeue_action():
        start_event.set()
        msg_q.dequeue()
        end_event.set()

    thread_deq_empty = threading.Thread(target=dequeue_action, args=())
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
