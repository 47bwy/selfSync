# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/22 11:02:54
@Author  :   47bwy
@Desc    :   None
'''

from functools import wraps
from inspect import signature


def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name]))
            return func(*args, **kwargs)
        return wrapper
    return decorate


@typeassert(int, int)
def add(x, y=3):
    return x + y

print(add(1, 2))  # 3
print(add(1))  # 4
# print(add(1, '2'))  # Raises TypeError


