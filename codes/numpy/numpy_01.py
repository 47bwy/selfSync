# -*- encoding: utf-8 -*-
'''
@Time    :   2025/02/21 01:50:54
@Author  :   47bwy
@Desc    :   理解 NumPy
'''

import numpy as np

my_array = np.array([1, 2, 3, 4, 5])
print(my_array)
print(my_array.shape)
print(my_array[0])
print(my_array[1])
print(my_array[2])

my_new_array = np.zeros(5)
print(my_new_array)

my_new_array = np.ones(5)
print(my_new_array)

my_radom_array = np.random.random(5)
print(my_radom_array)

my_2d_array = np.zeros((2, 3))
print(my_2d_array)

my_array = np.array([[4, 5], [6, 1]])
print(my_array[0][1])
print(my_array[:, 1])
print(my_array.shape)
print(my_array.size)
print(my_array.dtype)


a = np.array([[1, 2], [3, 4]])
b = np.array([[5, 6], [7, 8]])
sum = a + b
difference = a - b
product = a * b
quotient = a / b
a = np.array([[1, 2], [3, 4], [5, 6]])
matrix_product = a.dot(b)
print("Sum = ", sum)
print("Difference = ", difference)
print("Product = ", product)
print("Quotient = ", quotient)
print("Matrix Product = ", matrix_product)
