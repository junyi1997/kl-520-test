"""
This is the example for soft reset.
"""
import ctypes
from python_wrapper import kdp_wrapper

def user_test_reset(dev_idx, user_id):
    """User test soft reset"""
    print("starting soft reset ...\n")
    ret = kdp_wrapper.kdp_reset_sys(dev_idx)
    if ret:
        print("could not reset sys..\n")
        return -1

    print("sys reset mode succeeded...\n")

    return 0

def user_test_soft_reset(dev_idx, user_id):
    """User test soft reset"""
    user_test_reset(dev_idx, user_id)

    return 0
