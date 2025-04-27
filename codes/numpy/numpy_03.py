# -*- encoding: utf-8 -*-
'''
@Time    :   2025/02/21 03:14:22
@Author  :   47bwy
@Desc    :   Python、Numpy 教程
'''

import matplotlib.pyplot as plt
import numpy as np

c = np.full((2, 2), 7)  # Create a constant array
print(c)

d = np.eye(2)  # Create a 2x2 identity matrix
print(d)

a = np.array([[1,2,3,4], [5,6,7,8], [9,10,11,12]])
b = a[:2, 1:3]      # 前2行，第2、3列
print(b)

# math
x = np.array([[1,2],[3,4]], dtype=np.float64)
y = np.array([[5,6],[7,8]], dtype=np.float64)

print(x + y)
print(np.add(x, y))
print(x - y)
print(np.subtract(x, y))
print(x * y)
print(np.multiply(x, y))
print(x / y)
print(np.divide(x, y))
print(np.sqrt(x))


# 
x = np.array([[1,2], [3,4]])
print(x.T)

print("#" * 100)
# broadcasting
x = np.array([[1,2,3], [4,5,6], [7,8,9], [10,11,12]])
v = np.array([1,0,1])
y = np.empty_like(x)
for i in range(4):
    y[i, :] = x[i, :] + v
print(y)

vv = np.tile(v, (4, 1))
print(vv)
y = x + vv
print(y)

print("#" * 100)
# Compute the x and y coordinates for points on a sine curve
x = np.arange(0, 3 * np.pi, 0.1)
y_sin = np.sin(x)
y_cos = np.cos(x)

# Plot the points using matplotlib
plt.plot(x, y_sin)
plt.plot(x, y_cos)
plt.xlabel('x axis label')
plt.ylabel('y axis label')
plt.title('Sine and Cosine')
plt.legend(['Sine', 'Cosine'])
plt.show()
