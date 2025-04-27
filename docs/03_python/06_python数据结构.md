# 

### 基本数据类型

| 类型    | 示例          | 描述                 |
| ------- | ------------- | -------------------- |
| `int`   | `x = 42`      | 整数                 |
| `float` | `x = 3.14`    | 浮点数               |
| `str`   | `s = "hello"` | 字符串               |
| `bool`  | `b = True`    | 布尔值（True/False） |
| `None`  | `x = None`    | 空值                 |

### 内置容器类型

- List（列表）【有序，可变，允许重复】
- Tuple（元组）【有序，不可变，允许重复】
- Set（集合）【无序，不重复】
- Dict（字典）【键值对，无序（3.7+ 有序），键唯一】



### collections 模块中的增强结构

- `namedtuple` — 命名元组（更可读）
- `deque` — 双端队列（快速插入/删除）
- `Counter` — 计数器（元素频率统计）
- `defaultdict` — 带默认值的字典
- `OrderedDict` — 有序字典（现在 dict 也默认有序）



### 进阶

- 自定义数据结构（栈、队列、链表、堆、图）

- 使用 `heapq`、`queue`、`bisect`、`array` 等标准库模块

- 利用类 + 魔法方法打造 OOP 风格的数据容器



### 优先级队列

实现一个按优先级排序的队列，并且在这个队列上面每次`pop`操作总是返回优先级最高的那个元素

利用`heapq`模块实现了一个简单的优先级队列

```python
import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
```

使用方式：
```python
>>> class Item:
...     def __init__(self, name):
...         self.name = name
...     def __repr__(self):
...         return 'Item({!r})'.format(self.name)
...
>>> q = PriorityQueue()
>>> q.push(Item('foo'), 1)
>>> q.push(Item('bar'), 5)
>>> q.push(Item('spam'), 4)
>>> q.push(Item('grok'), 1)
>>> q.pop()
Item('bar')
>>> q.pop()
Item('spam')
>>> q.pop()
Item('foo')
>>> q.pop()
Item('grok')
>>>
```

`heappop()`函数总是返回”最小的”的元素，这就是保证队列pop操作返回正确元素的关键。 另外，由于 push 和 pop 操作时间复杂度为 O(log N)，其中 N 是堆的大小，因此就算是 N 很大的时候它们运行速度也依旧很快。

在上面代码中，队列包含了一个 `(-priority, index, item)` 的元组。 优先级为负数的目的是使得元素按照优先级从高到低排序。 这个跟普通的按优先级从低到高排序的堆排序恰巧相反。

`index` 变量的作用是保证同等优先级元素的正确排序。 通过保存一个不断增加的 `index` 下标变量，可以确保元素按照它们插入的顺序排序。 而且， `index` 变量也在相同优先级元素比较的时候起到重要作用。
