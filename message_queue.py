import threading
import collections

class MessageQueue:
    def __init__(self, upper_cap = 1500):
        self.q = collections.deque()
        self.qcv = threading.Condition()
        self.upper_cap = upper_cap
        self.running = True

    def signal_termination(self):
        with self.qcv:
            self.running = False
            self.qcv.notify_all()

    def enqueue(self, msg):
        with self.qcv:
            if len(self.q) > self.upper_cap:
                return False
            self.q.append(msg)
            self.qcv.notify_all()
        return True

    def dequeue(self):
        with self.qcv:
            while self.running and len(self.q) == 0:
                self.qcv.wait()
            return self.q.pop() if self.running else None

    def clear(self):
        with self.qcv:
            self.q.clear()
