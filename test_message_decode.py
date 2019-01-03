from .message import Message
from .message_decode import MessageDecode

def test_single_empty_msg():
    # arrange
    msg_decode = MessageDecode()
    test_msg_empty = Message(1234, "")
    expected_msg = list()

    # act
    for y_msg in msg_decode.handlebuffer(test_msg_empty.encode()):
        expected_msg.append(y_msg)

    # assert
    assert(not msg_decode.is_corrupted())
    assert(len(expected_msg) == 1)
    assert(expected_msg[0] == test_msg_empty)

def test_single_msg_decoding():
    """
    description: simulates how actual bytes are going to be received through
    network buffer
    """
    # arrange
    msg_decode = MessageDecode()
    test_msg = Message(98, "1234567890-=QWERTYUIOP[]\\ASDFGHJKAHWHJKLZXCVBNM,./;'@@@@@@@@")
    test_msg_encoded = test_msg.encode()
    CAP1 = 5 # index for capping first incoming buffer
    CAP2 = 7
    expected_msg = list() # message produced by msg_decode

    # act
    # first byte string incoming
    for y_msg in msg_decode.handlebuffer(test_msg_encoded[:CAP1]):
        expected_msg.append(y_msg)
    assert(len(expected_msg) == 0)

    # second byte string incoming
    for y_msg in msg_decode.handlebuffer(test_msg_encoded[CAP1:CAP2]):
        expected_msg.append(y_msg)
    assert(len(expected_msg) == 0)

    # third byte string incoming
    for y_msg in msg_decode.handlebuffer(test_msg_encoded[CAP2:]):
        expected_msg.append(y_msg)
    assert(len(expected_msg) == 1)

    # assert
    assert(not msg_decode.is_corrupted())
    assert(expected_msg[0] == test_msg)

def test_batch_decoding():
    # arrange
    msg_decode = MessageDecode()
    test_msgs = [
        Message(0, "test1"),
        Message(1, "asdfghjkasdfghjkasdfghjkasdfghjk"),
        Message(8, "asdfghjkl;'sfghjklqwertyuiop"),
        Message(111, "j^^^^^^^^^^^^^$#@@@@!!)(*&*()(***&&^%%%$$$%&*_++_==")
    ]

    # act
    bufsum = b''
    for msg in test_msgs:
        bufsum += msg.encode()

    expected_msgs = set()
    for y_msg in msg_decode.handlebuffer(bufsum):
        expected_msgs.add(y_msg)

    # assert
    assert(not msg_decode.is_corrupted())
    for msg in test_msgs:
        assert(msg in expected_msgs)
        expected_msgs.remove(msg)

def test_corrupted_msg():
    # arrange
    msg_decode = MessageDecode()
    bad_msgs_encoded = [
        b"096[2, 8]sdfadsf'", # bad header and bad json
        b"06[21, 8]sdfadsf'", # bad json length
        b"06[2, 8]ssdfadsf'", # bad payload length
        b"/////////////////////////////////////////", # just bad
    ]
    expected_msgs = list()

    # act
    for bad_bstring in bad_msgs_encoded:
        msg_decode.reset_state()
        for y_msg in msg_decode.handlebuffer(bad_bstring):
            expected_msgs.append(y_msg)

        assert(len(expected_msgs) == 0)
        assert(msg_decode.is_corrupted())