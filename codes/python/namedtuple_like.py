# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/24 16:20:56
@Author  :   47bwy
@Desc    :   None
'''

import operator


class StructTupleMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required'.format(len(cls._fields)))
        return super().__new__(cls,args)
    

class Stock(StructTuple):
    _fields = ['name', 'shares', 'price']

class Point(StructTuple):
    _fields = ['x', 'y']


print(Stock)
s = Stock('ACME', 50, 91.1)
print(s)
print(s.name)  # 输出：ACME