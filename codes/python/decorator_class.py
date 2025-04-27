# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/23 14:07:29
@Author  :   47bwy
@Desc    :   None
'''

import types
from functools import wraps


class Profiled:

    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y


class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)


if __name__ == "__main__":
    print(add(1, 2))
    print(add(3, 4))
    print(add.ncalls)

    s = Spam()
    s.bar(1)
    s.bar(2)
    print(s.bar.ncalls)
