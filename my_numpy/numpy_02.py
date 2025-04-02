# -*- encoding: utf-8 -*-
'''
@Time    :   2025/02/21 02:28:08
@Author  :   47bwy
@Desc    :   NumPy 简单入门教程
'''

import numpy as np

# 1D Array
a = np.array([1, 2, 3, 4, 5])
b = np.array((1, 2, 3, 4, 5))
c = np.arange(5)
d = np.linspace(0, 2*np.pi, 5)
print(a)
print(b)
print(c)
print(d)

# 2D array
x = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])
print(x)

# 3D array
y = np.array([[[1, 2, 3],
               [4, 5, 6]],
              [[7, 8, 9],
               [10, 11, 12]]])
print(y)
print(y.shape)

print("#" * 100)
# multi-dimensional array
z = np.array([1, 2, 3, 4], ndmin=5)
print(z)
print(z.ndim)

print("#" * 100)
# multi-dimensional array
a = np.array([[11, 12, 13, 14, 15],
              [16, 17, 18, 19, 20],
              [21, 22, 23, 24, 25],
              [26, 27, 28 ,29, 30],
              [31, 32, 33, 34, 35]])
print(a[0, 1])
print(a[0, 1:4])
print(a[::2, ::2])
print(a[:, 1])

print("#" * 100)
# array properties
print(a.shape)  # (5, 5)    5 rows and 5 columns
print(a.ndim)   # 2   2D array
print(a.size)   # 25  5*5 = 25  total number of elements  
print(a.dtype)  # int32  data type of elements
print(a.dtype.name)  # int32
print(a.itemsize)   # 4  size in bytes of each element
print(a.data)   # <memory at 0x0000020D3D3D3D00>  memory location
print(a.nbytes) # 100  total bytes consumed by the elements of the array
print(a.strides)    # (20, 4)  number of bytes to step in each dimension when traversing an array


print("#" * 100)
# basic operations
a = np.arange(25)
print(a)
b = a.reshape(5, 5)
print(b)
c = np.array([10, 62, 1, 14, 2, 56, 79, 2, 1, 45,
              4, 92, 5, 55, 63, 43, 35, 6, 53, 24,
              56, 3, 56, 44, 78])
d = c.reshape(5, 5)
print(b + d)
print(b - d)
print(b * d)
print(b / d)
print(b ** 2)
print(a < c)
print(b < d)
print(np.dot(b, d))
print(np.add(b, d))
print(np.subtract(b, d))
print(np.multiply(b, d))
print(np.divide(b, d))
print(np.sqrt(a))
print(np.sin(a))
print(np.cos(a))
print(np.log(a))
print(np.sum(a))
print(np.min(a))
print(np.max(a))
print(np.cumsum(a))
print(np.mean(a))
print(np.median(a))
print(np.corrcoef(a))
print(np.std(a))
print(np.percentile(a, 75))
print(np.any(a))

print("#" * 100)
#fancy indexing
a = np.arange(0, 100, 10)
indices = [1, 5, -1]
b = a[indices]
print(a)
print(b)

print("#" * 100)
# boolean maskin
import matplotlib.pyplot as plt

a = np.linspace(0, 2*np.pi, 50)
print(a)
b = np.sin(a)
print(b)
plt.plot(a, b)
mask = b >= 0
plt.plot(a[mask], b[mask], 'bo')
mask = (b >= 0) & (a <= np.pi/2)
plt.plot(a[mask], b[mask], 'go')
# plt.show()

print("#" * 100)
# incomplete indexing
a = np.arange(0, 100, 10)
print(a)
b = a[:5]
c = a[a >= 50]
print(b)
print(c)

print("#" * 100)
# where function
a = np.arange(0, 100, 10)
b = np.where(a < 50)
c = np.where(a >= 50)[0]
print(a)
print(b)
print(c)
