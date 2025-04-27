# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/23 16:39:18
@Author  :   47bwy
@Desc    :   None
'''

import types


class MyClass:
    def __init__(self, name):
        self.name = name

    # def greet(self):
    #     print(f"Hello, {self.name}!")

# 创建一个类实例
obj = MyClass("Alice")

def greet():
    print(f"Hello, greet!")

# 将 greet 方法动态绑定到 obj 上
bound_greet = types.MethodType(greet, obj)
print((obj.__dir__()))

# 调用绑定的方法
bound_greet()  # 输出: Hello, Alice!