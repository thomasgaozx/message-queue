import enum
import json
from .constants import MAX_HEADER_SIZE
from .message import Message, MessageType

class MessageDecodeStatus(enum.Enum):
    Pending = 0 # no buffer
    DecodingPrefix = 1 # received buffer, decoding prefix
    DecodingHeader = 2
    DecodingPayload = 3
    Corrupted = 9 # e.g. exceptions, missing segments, timeout ... socket should be closed then

class MessageDecode:
    def __init__(self):
        self.state = MessageDecodeStatus.Pending
        self.prefix = -1
        self.header = list()
        self.payload = ""
        self.buffer = ""

    def handlebuffer(self, buf):
        """
        description: continue stepping through each decoding process
        yields: Message objects for each decoded message
        """
        if buf == "":
            return

        self.buffer += buf

        if self.state == MessageDecodeStatus.Pending:
            self.state = MessageDecodeStatus.DecodingPrefix

        while True: # continue decoding if each step makes progress
            if self.state == MessageDecodeStatus.DecodingPrefix and not self.parse_prefix():
                return
            if self.state == MessageDecodeStatus.DecodingHeader and not self.parse_header():
                return
            if self.state == MessageDecodeStatus.DecodingPayload and not self.parse_payload():
                return
            yield Message(self._get_msg_type(),self.payload)

    def _get_payload_len(self):
        if len(self.header) == 2:
            return self.header[1]
        return -1

    def _get_msg_type(self):
        try:
            return MessageType(self.header[0])
        except:
            return MessageType.Unknown

    def reset_state(self):
        if len(self.buffer) > 0:
            self.state = MessageDecodeStatus.DecodingPrefix
        else:
            self.state = MessageDecodeStatus.Pending

    def parse_prefix(self):
        """
        assumptions: self in DecodingPrefix state
        returns: `True` if state is updated, `False` otherwise
        """
        try:
            if len(self.buffer) >= MAX_HEADER_SIZE:
                self.prefix = int(self.buffer[:MAX_HEADER_SIZE])
                self.buffer = self.buffer[MAX_HEADER_SIZE:]
                self.state = MessageDecodeStatus.DecodingHeader
                return True
        except ValueError as e:
            self.state = MessageDecodeStatus.Corrupted
        return False

    def parse_header(self):
        try:
            if len(self.buffer) >= self.prefix:
                self.header = json.loads(self.buffer[:self.prefix])
                self.buffer = self.buffer[self.prefix:]
                self.state = MessageDecodeStatus.DecodingPayload
                return True
        except json.JSONDecodeError as e:
            self.state = MessageDecodeStatus.Corrupted
        return False
    
    def parse_payload(self):
        """
        description: parse payload
        """
        try:
            if len(self.buffer) >= self._get_payload_len():
                self.payload = self.buffer[:self._get_payload_len()].decode("utf-8")
                self.buffer = self.buffer[self._get_payload_len():]
                self.reset_state()
                return True
        except json.JSONDecodeError as e:
            self.state = MessageDecodeStatus.Corrupted
        return False