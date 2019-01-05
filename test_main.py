from . import test_message_decode
from . import test_message_queue
from . import test_multicast_server

def run_tests_from(mod_obj):
    print("EXECUTING TESTS IN MODULE " + mod_obj.__name__)
    for name in dir(mod_obj):
        if name[:4] == "test":
            test = getattr(mod_obj, name)
            if callable(test):
                print("[ RUNNING ] '%s'" % (name,))
                test()
                print("[ PASSED  ] '%s'" % (name,))
    print()

if __name__ == "__main__":
    MODULES = [
        test_message_decode,
        test_message_queue,
        test_multicast_server
    ]
    for mod_obj in MODULES:
        run_tests_from(mod_obj)
