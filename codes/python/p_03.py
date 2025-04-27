# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/01 14:38:08
@Author  :   47bwy
@Desc    :   None
'''


import heapq
import math
import re
import sys
import unicodedata
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from functools import wraps
from queue import Queue


def func_1():
    num = re.compile('\d+')
    # ASCII digits
    r1 = num.match('123')
    print(r1)  # 输出：<re.Match object; span=(0, 3), match='123'>
    r2 = num.match('\u0661\u0662\u0663')
    print(r2)


def func_2():
    comment = re.compile(r'/\*(.*?)\*/')
    comment = re.compile(r'/\*(.*?)\*/', re.DOTALL)
    # comment = re.compile(r'/\*((?:.|\n)*?)\*/')
    text1 = '/* this is a comment */'
    text2 = '''/* this is a
    multiline comment */
    '''
    print(comment.findall(text1))  # 输出：[' this is a comment ']
    print(comment.findall(text2))  # 输出：[' this is a\nmultiline comment ']


def func_3():
    nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
    print(heapq.nlargest(3, nums))  # Prints [42, 37, 23]
    print(heapq.nsmallest(3, nums))  # Prints [-4, 1, 2]


def func_4():
    portfolio = [
        {'name': 'IBM', 'shares': 100, 'price': 91.1},
        {'name': 'AAPL', 'shares': 50, 'price': 543.22},
        {'name': 'FB', 'shares': 200, 'price': 21.09},
        {'name': 'HPQ', 'shares': 35, 'price': 31.75},
        {'name': 'YHOO', 'shares': 45, 'price': 16.35},
        {'name': 'ACME', 'shares': 75, 'price': 115.65}
    ]
    cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
    expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])
    # Prints [{'name': 'YHOO', 'shares': 45, 'price': 16.35}, {'name': 'FB', 'shares': 200, 'price': 21.09}, {'name': 'HPQ', 'shares': 35, 'price': 31.75}]
    print(cheap)
    # Prints [{'name': 'AAPL', 'shares': 50, 'price': 543.22}, {'name': 'IBM', 'shares': 100, 'price': 91.1}, {'name': 'ACME', 'shares': 75, 'price': 115.65}]
    print(expensive)


def func_5():
    funcs = [lambda x, n=n: x + n for n in range(5)]
    for f in funcs:
        print(f(0))


def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)


class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args


def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper


def add(x, y):
    return x + y


@inlined_async
def func_6():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')


class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


class Persion:
    def __init__(self, first_name):
        self.first_name = first_name


def func_7():
    p = Person('John')
    print(p.first_name)  # Outputs: John
    p.first_name = 'Apri'
    print(p.first_name)  # Outputs: Jane
    # del p.first_name  # Raises AttributeError: Can't delete attribute
    # p.first_name = 123  # Raises TypeError: Expected a string


class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius
    
    @property
    def test():
        print('test')
        return 1


def func_8():
    c = Circle(4.0)
    print(c.__dict__)
    print(Circle.__dict__)
    print(c.area)  # Outputs: Computing area 50.26548245743669
    print(c.perimeter)  # Outputs: Computing perimeter 25.1327412287191
    print(c.area)  # Outputs: 50.26548245743669 (no computation this time)
    print(c.perimeter)  # Outputs: 25.1327412287191 (no computation this time)
    print(c.__dict__)


class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass

class SocketStream(IStream):
    def read(self, maxbytes=-1):
        pass

    def write(self, data):
        pass

def func_9():
    stream = SocketStream()
    if not isinstance(stream, IStream):
        raise TypeError('Expected an IStream')
    pass


class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging.
    """
    __slots__ = ()  # 混入类都没有实例变量，因为直接实例化混入类没有任何意义

    def __getitem__(self, key):
        print('Getting ' + str(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return super().__delitem__(key)


class SetOnceMappingMixin:
    '''
    Only allow a key to be set once.
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)


class StringKeysMappingMixin:
    '''
    Restrict keys to strings only
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')
        return super().__setitem__(key, value)
    

class LoggedDict(LoggedMappingMixin, dict):
    pass

def func_10():
    d = LoggedDict()
    d[23] = 23
    print(d[23])
    del d[23]



class SetOnceDefaultDict(SetOnceMappingMixin, defaultdict):
    pass

def fun_11():
    d = SetOnceDefaultDict(list)
    d['x'].append(2)
    d['x'].append(3)
    print(d['x'])  # Outputs: [2, 3]
    d['x'] = 23  # Raises KeyError: 'x already set'


class Connection1:
    """新方案——对每个状态定义一个类"""

    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate
        # Delegate to the state class

    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)


# Connection state base class
class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn, data):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()


# Implementation of different states
class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def write(conn, data):
        raise RuntimeError('Not open')

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError('Already closed')


class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn, data):
        print('writing')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already open')

    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)

def func_12():
    conn = Connection1()
    print(conn._state)  # Outputs: <class '__main__.ClosedConnectionState'>
    conn.open()
    conn.read()
    conn.write('data')
    conn.close()
    # conn.read()  # Raises RuntimeError: Not open
    # conn.write('data')  # Raises RuntimeError: Not open
    # conn.close()  # Raises RuntimeError: Already closed



if __name__ == '__main__':
    # func_1()
    # func_2()
    # func_3()
    # func_4()
    # func_5()
    # func_6()
    # func_7()
    # func_8()
    # func_9()
    # func_10()
    # fun_11()
    # func_12()
    pass