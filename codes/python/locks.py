# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/25 11:36:49
@Author  :   47bwy
@Desc    :   None
'''

import threading
import time
from contextlib import contextmanager

# Thread-local state to stored information on locks already acquired
_local = threading.local()

@contextmanager
def acquire(*locks):
    # Sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))

    # Make sure lock order of previously acquired locks is not violated
    acquired = getattr(_local,'acquired',[])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]




x_lock = threading.Lock()
y_lock = threading.Lock()

def thread_1():
    while True:
        time.sleep(0.1)
        with acquire(x_lock, y_lock):
            print('Thread-1')

def thread_2():
    while True:
        time.sleep(0.1)
        with acquire(y_lock, x_lock):
            print('Thread-2')


def thread_1():
    while True:
        time.sleep(0.1)
        with acquire(x_lock):
            with acquire(y_lock):
                print('Thread-1')

def thread_2():
    while True:
        time.sleep(0.1)
        with acquire(y_lock):
            with acquire(x_lock):
                print('Thread-2')

            

# The philosopher thread
def philosopher(left, right):
    while True:
        time.sleep(0.5)
        with acquire(left, right):
             print(threading.currentThread(), 'eating')




if __name__ == "__main__":
    thread_1()

    t1 = threading.Thread(target=thread_1)
    t1.daemon = True
    t1.start()


    t2 = threading.Thread(target=thread_2)
    t2.daemon = True
    t2.start()

    time.sleep(1)

    # The chopsticks (represented by locks)
    # NSTICKS = 5
    # chopsticks = [threading.Lock() for n in range(NSTICKS)]

    # # Create all of the philosophers
    # for n in range(NSTICKS):
    #     t = threading.Thread(target=philosopher,
    #                         args=(chopsticks[n],chopsticks[(n+1) % NSTICKS]))
    #     t.start()