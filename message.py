import json
from enum import Enum

class MessageType(Enum):
    Unknown = -1
    Info = 0
    Echo = 1

class Message:
    def __init__(self, _msg_type, _payload):
        self.msg_type = _msg_type
        self.payload = _payload
    
    def encode(self):
        """
        description: encode the message
        returns: encoded message if successful, empty string otherwise
        """
        e_payload = self.payload.encode("utf-8")
        e_header = json.dumps([self.msg_type, len(e_payload)]).encode("utf-8")
        e_header_len = len(e_header)
        return str(e_header_len).encode("utf-8").zfill(2)+e_header+e_payload if e_header_len < 100 else ""