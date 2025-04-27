# -*- encoding: utf-8 -*-
'''
@Time    :   2025/02/21 03:46:54
@Author  :   47bwy
@Desc    :   创建 Numpy 数组的不同方式
'''

# 使用Numpy内部功能函数
# 从列表等其他Python的结构进行转换
# 使用特殊的库函数

import numpy as np

a = np.arange(15).reshape(3, 5)
print(a)

b = np.arange(27).reshape(3, 3, 3)
print(b)

c = np.zeros((3, 4))
print(c)

# 从列表等其他Python的结构进行转换
d = np.array([2, 3, 4])
print(d)

# 使用特殊的库函数
e = np.linspace(0, 2, 9)
print(f'e: {e}')
f = np.random.random((2, 3))
print(f)
g = np.empty((2, 3))
print(g)
h = np.full((2, 2), 7)
print(h)
i = np.eye(2)
print(i)
j = np.ones((2, 2))
print(j)
k = np.random.randint(1, 10, 5)
print(k)
l = np.random.randn(2, 3)
print(l)
m = np.random.rand(2, 3)
print(m)
n = np.random.normal(0, 1, 5)
print(n)
o = np.random.uniform(1, 2, 5)
print(o)
p = np.random.choice(5, 3)
print(p)
q = np.random.permutation(5)
print(q)
r = np.random.shuffle([1, 2, 3, 4, 5])
print(r)
s = np.random.seed(0)
print(s)
