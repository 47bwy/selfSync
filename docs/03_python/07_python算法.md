# 

Python 作为一门通用编程语言，可以实现各种算法。

### 排序算法 (Sorting Algorithms)
```python
# 冒泡排序
def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# 快速排序
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# 归并排序
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

### 搜索算法 (Searching Algorithms)
```python
# 二分查找
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# 线性查找
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1
```

### 图算法 (Graph Algorithms)
```python
# 广度优先搜索 (BFS)
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        print(vertex, end=" ")
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

# 深度优先搜索 (DFS)
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    print(start, end=" ")
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# Dijkstra 最短路径算法
import heapq

def dijkstra(graph, start):
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]
    
    while heap:
        current_distance, current_vertex = heapq.heappop(heap)
        if current_distance > distances[current_vertex]:
            continue
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(heap, (distance, neighbor))
    return distances
```

### 动态规划 (Dynamic Programming)
```python
# 斐波那契数列 (带记忆化)
def fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)
    return memo[n]

# 0-1背包问题
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]
```

### 贪心算法 (Greedy Algorithms)
```python
# 活动选择问题
def activity_selection(activities):
    activities.sort(key=lambda x: x[1])  # 按结束时间排序
    selected = [activities[0]]
    
    for activity in activities[1:]:
        if activity[0] >= selected[-1][1]:  # 开始时间 >= 上一个活动的结束时间
            selected.append(activity)
    return selected

# 霍夫曼编码
import heapq

def huffman_coding(freq):
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
```

### 分治算法 (Divide and Conquer)
```python
# 最大子数组问题
def max_subarray(arr):
    def max_crossing_sum(arr, low, mid, high):
        left_sum = float('-inf')
        total = 0
        for i in range(mid, low-1, -1):
            total += arr[i]
            if total > left_sum:
                left_sum = total
                
        right_sum = float('-inf')
        total = 0
        for i in range(mid+1, high+1):
            total += arr[i]
            if total > right_sum:
                right_sum = total
                
        return left_sum + right_sum
    
    def max_subarray_helper(arr, low, high):
        if low == high:
            return arr[low]
        mid = (low + high) // 2
        return max(max_subarray_helper(arr, low, mid),
                  max_subarray_helper(arr, mid+1, high),
                  max_crossing_sum(arr, low, mid, high))
    
    return max_subarray_helper(arr, 0, len(arr)-1)
```

### 字符串算法 (String Algorithms)
```python
# KMP 字符串匹配算法
def kmp_search(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length-1]
                else:
                    lps[i] = 0
                    i += 1
        return lps
    
    lps = compute_lps(pattern)
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1
    return -1

# Rabin-Karp 字符串匹配算法
def rabin_karp(text, pattern):
    d = 256  # 字符集大小
    q = 101  # 质数
    m = len(pattern)
    n = len(text)
    p = t = 0
    h = 1
    
    for i in range(m-1):
        h = (h * d) % q
    
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    
    for i in range(n - m + 1):
        if p == t:
            if text[i:i+m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m]) % q
            if t < 0:
                t += q
    return -1
```

### 数学算法 (Mathematical Algorithms)
```python
# 素数筛法 (埃拉托斯特尼筛法)
def sieve_of_eratosthenes(n):
    primes = [True] * (n+1)
    primes[0] = primes[1] = False
    for i in range(2, int(n**0.5)+1):
        if primes[i]:
            for j in range(i*i, n+1, i):
                primes[j] = False
    return [i for i, is_prime in enumerate(primes) if is_prime]

# 最大公约数 (欧几里得算法)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 快速幂算法
def fast_power(a, b):
    result = 1
    while b > 0:
        if b % 2 == 1:
            result *= a
        a *= a
        b //= 2
    return result
```

### 机器学习算法 (Machine Learning Algorithms)
```python
# K-均值聚类
import numpy as np

def k_means(data, k, max_iterations=100):
    # 随机初始化中心点
    centroids = data[np.random.choice(range(len(data)), k, replace=False)]
    
    for _ in range(max_iterations):
        # 分配点到最近的聚类中心
        distances = np.sqrt(((data - centroids[:, np.newaxis])**2).sum(axis=2))
        clusters = np.argmin(distances, axis=0)
        
        # 更新聚类中心
        new_centroids = np.array([data[clusters == i].mean(axis=0) for i in range(k)])
        
        # 检查是否收敛
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    
    return clusters, centroids

# 线性回归
def linear_regression(X, y, learning_rate=0.01, iterations=1000):
    m = len(y)
    theta = np.zeros(X.shape[1])
    
    for _ in range(iterations):
        predictions = X.dot(theta)
        errors = predictions - y
        gradient = X.T.dot(errors) / m
        theta -= learning_rate * gradient
    
    return theta
```

### 其他实用算法
```python
# LRU缓存 (最近最少使用)
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# 布隆过滤器
import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, hash_num):
        self.size = size
        self.hash_num = hash_num
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)
    
    def add(self, item):
        for i in range(self.hash_num):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1
    
    def contains(self, item):
        for i in range(self.hash_num):
            index = mmh3.hash(item, i) % self.size
            if not self.bit_array[index]:
                return False
        return True
```