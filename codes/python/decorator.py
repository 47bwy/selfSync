# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/22 09:53:42
@Author  :   47bwy
@Desc    :   None
'''

import inspect
import logging
import time
import types
from functools import partial, wraps


def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end - start)
        return result
    return wrapper


# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    '''
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper

    return decorate

# Example use


@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.INFO, 'example')
def spam():
    print('Spam!')


@timethis
def countdown(n):
    while n > 0:
        n -= 1


# logging.basicConfig(level=logging.DEBUG)
# print(add(2, 3))
# spam()
# countdown(10)

def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__
    print(1111)
    time.sleep(5)
    print(2222)

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper

# Example use
# @logged
# def add(x, y):
#     return x + y

# @logged(level=logging.CRITICAL, name='example')
# def spam():
#     print('Spam!')

# print(add(2, 3))
# spam()


def my_decorator(func):
    @wraps(func)
    def wrapper():
        print("Before function call")
        func()  # 调用原始函数
        print("After function call")
    return wrapper

# @my_decorator
# def my_function():
#     print("Hello, world!")



# my_function()


class MyDecorator:
    def __init__(self, func):
        self.func = func  # 保存原函数
    
    def __call__(self, *args, **kwargs):
        print("Before function call")
        result = self.func(*args, **kwargs)
        print("After function call")
        return result
    
    def __get__(self, instance, cls):
        print(1111, self, instance, cls)
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)
    


@MyDecorator
def greet(name):
    print(f"Hello, {name}!")

class MyClass:
    @MyDecorator
    def my_func(self):
        print("Hello from MyClass!")

    @staticmethod
    @MyDecorator
    def my_class_method():
        print("Hello from MyClass static method!")


# obj = MyDecorator(greet)
# print(obj)
# obj('Apri')
# greet("Alice")

my_cls = MyClass()
# print(2222, my_cls.my_func)
# # my_cls.my_func = MyDecorator(my_cls.my_func)
# # my_cls.my_func()
my_cls.my_func()

# MyClass.my_class_method()

print(inspect.signature(logged))
print(help(logged))