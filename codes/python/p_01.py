# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/01 13:51:47
@Author  :   47bwy
@Desc    :   None
'''


numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # 输出: [1, 4, 9, 16, 25]

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # 输出：[2, 4, 6, 8]

from functools import reduce

numbers = [1, 2, 3, 4, 5]
# 使用 reduce() 和 lambda 函数计算乘积
product = reduce(lambda x, y: x * y, numbers)
print(product)  # 输出：120


def decorator1(func):
    def wrapper():
        print("Decorator 1")
        func()
    return wrapper

def decorator2(func):
    def wrapper():
        print("Decorator 2")
        func()
    return wrapper

@decorator1
@decorator2
def say_hello():
    print("Hello!")

say_hello()


scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'David': 95}
# 按键排序
sorted_by_key = dict(sorted(scores.items()))
print(f"按键排序: {sorted_by_key}")  # 输出: 按键排序: {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'David': 95}

# 按值排序(降序)
sorted_by_value = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
print(f"按值排序(降序): {sorted_by_value}")  # 输出: 按值排序(降序): {'David': 95, 'Bob': 92, 'Alice': 85, 'Charlie': 78}

r = sorted(zip(scores.values(), scores.keys()))
print(r)

min_price = min(zip(scores.values(), scores.keys()))
max_price = max(zip(scores.values(), scores.keys()))
print(min_price)  # 输出: (78, 'Charlie')
print(max_price)  # 输出: (95, 'David')

print(f"round(1627731, -2) = {round(1627731, -2)}") 