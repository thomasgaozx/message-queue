from . import test_message_decode
from . import test_message_queue

def run_tests_from(mod_obj):
    print("EXECUTING TESTS IN MODULE " + mod_obj.__name__)
    for name in dir(mod_obj):
        if name[:4] == "test":
            test = getattr(mod_obj, name)
            if callable(test):
                test()
                print("[PASSED] '%s'" % (name,))

if __name__ == "__main__":
    MODULES = [
        test_message_decode,
        test_message_queue
    ]
    for mod_obj in MODULES:
        run_tests_from(mod_obj)
