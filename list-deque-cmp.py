#coding:utf-8


import time
from collections import deque
from array import array

BASE_NUM = 1000000


def timeit(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time() - start_time
        print "Total spend time:%s" % end_time
    return wrap


@timeit
def test_list():
    queue = list()
    for n in xrange(BASE_NUM):
        if n % 2 == 0:
            queue.insert(0, n)
        elif n % 2 == 1:
            queue.append(n)

@timeit
def test_deque():
    queue = deque()
    for n in xrange(BASE_NUM):
        if n % 2 == 0:
            queue.appendleft(n)
        elif n % 2 == 1:
            queue.append(n)

@timeit
def test_array():
    arr = array("i")
    for n in xrange(BASE_NUM):
        if n % 2 == 0:
            arr.insert(0, n)
        elif n % 2 == 1:
            arr.append(n)


test_deque()
test_array()
test_list()
