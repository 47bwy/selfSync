# 

### 🍞迭代器和生成器

**（可迭代对象、迭代器、生成器）**

#### 🎯 概念和关系
一、可迭代对象（Iterable）

**定义**：实现了 `__iter__()` 方法的对象，或者可以被 `iter()` 函数作用的对象。

**特点**：

- 可以用 `for x in obj:` 来遍历。
- 调用 `iter(obj)` 会返回一个 **迭代器（iterator）**。

**常见的可迭代对象**：
```python
list, tuple, str, dict, set, range, file, 等等
```

**示例**：
```python
lst = [1, 2, 3]
it = iter(lst)  # 得到一个迭代器
```

二、迭代器（Iterator）

**定义**：实现了 `__iter__()` 和 `__next__()` 方法的对象。

**特点**：

- `__iter__()` 返回自身（`return self`）。
- `__next__()` 每次返回一个元素，直到抛出 `StopIteration` 异常。
- 只能往前走，不能回头（一次性消费）。

**示例**：
```python
lst = [1, 2, 3]
it = iter(lst)  # it 是一个迭代器
print(next(it))  # 输出 1
print(next(it))  # 输出 2
```

三、生成器（Generator）

生成器是**一种特殊的迭代器**，有两种创建方式：

- 生成器函数（使用 `yield`）
```python
def my_gen():
    yield 1
    yield 2
    yield 3

g = my_gen()  # g 是一个生成器，也就是迭代器
```

- 生成器表达式（generator expression）
```python
g = (x * x for x in range(3))  # g 是一个生成器
```

**特点**：

- 省内存，懒加载。
- 遇到 `yield` 暂停执行，下一次 `next()` 从暂停点继续。

**关系图解：**

```lua
           +-----------------------+
           |    Iterable           |   ← 可以用 for 循环遍历它
           |  (__iter__ method)    |
           +-----------------------+
                     |
                     |  iter()
                     ↓
           +-----------------------+
           |    Iterator           |   ← 可以手动调用 next()
           | (__iter__, __next__)  |
           +-----------------------+
                     ^
                     |
      +---------------------------+
      |     Generator             |   ← 特殊的 Iterator（自动实现了）
      |   (使用 yield 创建的)       |
      +---------------------------+
```

#### 🎯 使用生成器创建新的迭代模式
```python
def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment
```
为了使用这个函数， 可以用for循环迭代它或者使用其他接受一个可迭代对象的函数(比如 sum() , list() 等)。示例如下：
```python
>>> for n in frange(0, 4, 0.5):
...     print(n)
...
0
0.5
1.0
1.5
2.0
2.5
3.0
3.5
>>> list(frange(0, 1, 0.125))
[0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
>>>
```
一个函数中需要有一个 `yield` 语句即可将其转换为一个生成器。 跟普通函数不同的是，生成器只能用于迭代操作。


#### 🎯 在对象上实现迭代
在一个对象上实现迭代最简单的方式是使用一个生成器函数。 
```python
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

# Example
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    for ch in root.depth_first():
        print(ch)
    # Outputs Node(0), Node(1), Node(3), Node(4), Node(2), Node(5)
```

在上面代码中， `__iter__()` 方法只是简单的将迭代请求传递给内部的 `_children` 属性。

Python的迭代器协议需要 `__iter__()` 方法返回一个实现了 `__next__()` 方法的迭代器对象。

这里的 `iter()` 函数的使用简化了代码， `iter(s)` 只是简单的通过调用 `s.__iter__()` 方法来返回对应的迭代器对象， 就跟 `len(s)` 会调用 `s.__len__()` 原理是一样的。

`depth_first()` 方法简单直观。 它首先返回自己本身并迭代每一个子节点并 通过调用子节点的 `depth_first()` 方法(使用 `yield from` 语句)返回对应元素。


#### 🎯 反向迭代
通过在自定义类上实现 `__reversed__()` 方法来实现反向迭代。比如：
```python
class Countdown:
    def __init__(self, start):
        self.start = start

    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # Reverse iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1

for rr in reversed(Countdown(30)):
    print(rr)
for rr in Countdown(30):
    print(rr)
```

#### 🎯 带有外部状态的生成器函数
如果要生成器暴露外部状态给用户， 可以简单的将它实现为一个类，然后把生成器函数放到 `__iter__()` 方法中过去。比如：
```python
from collections import deque

class linehistory:
    def __init__(self, lines, histlen=3):
        self.lines = lines
        self.history = deque(maxlen=histlen)

    def __iter__(self):
        for lineno, line in enumerate(self.lines, 1):
            self.history.append((lineno, line))
            yield line

    def clear(self):
        self.history.clear()


with open('somefile.txt') as f:
    lines = linehistory(f)
    for line in lines:
        if 'python' in line:
            for lineno, hline in lines.history:
                print('{}:{}'.format(lineno, hline), end='')
```

在 `__iter__()` 方法中定义生成器不会改变任何的算法逻辑。 由于它是类的一部分，所以允许定义各种属性和方法来供用户使用。


#### 🎯 迭代器切片
函数 `itertools.islice()` 正好适用于在迭代器和生成器上做切片操作。比如：
```python
>>> def count(n):
...     while True:
...         yield n
...         n += 1
...
>>> c = count(0)
>>> c[10:20]
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
TypeError: 'generator' object is not subscriptable

>>> # Now using islice()
>>> import itertools
>>> for x in itertools.islice(c, 10, 20):
...     print(x)
...
10
11
12
13
14
15
16
17
18
19
>>>
```
要着重强调的一点是 `islice()` 会消耗掉传入的迭代器中的数据，必须考虑到迭代器是不可逆的这个事实，所以如果需要之后再次访问这个迭代器的话，那么就得先将它里面的数据放入一个列表中。


#### 🎯 跳过可迭代对象的开始部分
`itertools.dropwhile()` 函数使用时，传递一个函数对象和一个可迭代对象。 它会返回一个迭代器对象，丢弃原有序列中直到函数返回Flase之前的所有元素，然后返回后面所有元素。
```python
>>> with open('/etc/passwd') as f:
... for line in f:
...     print(line, end='')
...
##
# User Database
#
# Note that this file is consulted directly only when the system is running
# in single-user mode. At other times, this information is provided by
# Open Directory.
...
##
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
...
>>>


>>> from itertools import dropwhile
>>> with open('/etc/passwd') as f:
...     for line in dropwhile(lambda line: not line.startswith('#'), f):
...         print(line, end='')
...
nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0:System Administrator:/var/root:/bin/sh
...
>>>
```

如果已经明确知道了要跳过的元素的序号的话，那么可以使用 `itertools.islice()` 来代替。比如：
```python
>>> from itertools import islice
>>> items = ['a', 'b', 'c', 1, 4, 10, 15]
>>> for x in islice(items, 3, None):
...     print(x)
...
4
10
15
>>>
```

#### 🎯 排列组合的迭代
`itertools`模块提供了三个函数来解决这类问题。 其中一个是 `itertools.permutations()` ， 它接受一个集合并产生一个元组序列，每个元组由集合中所有元素的一个可能排列组成。 也就是说通过打乱集合中元素排列顺序生成一个元组，比如：
```python
>>> items = ['a', 'b', 'c']
>>> from itertools import permutations
>>> for p in permutations(items):
...     print(p)
...
('a', 'b', 'c')
('a', 'c', 'b')
('b', 'a', 'c')
('b', 'c', 'a')
('c', 'a', 'b')
('c', 'b', 'a')
>>>
```
如果想得到指定长度的所有排列，可以传递一个可选的长度参数。就像这样：
```python
>>> for p in permutations(items, 2):
...     print(p)
...
('a', 'b')
('a', 'c')
('b', 'a')
('b', 'c')
('c', 'a')
('c', 'b')
>>>
```

使用 `itertools.combinations()` 可得到输入集合中元素的所有的组合。比如：
```python
>>> from itertools import combinations
>>> for c in combinations(items, 3):
...     print(c)
...
('a', 'b', 'c')

>>> for c in combinations(items, 2):
...     print(c)
...
('a', 'b')
('a', 'c')
('b', 'c')

>>> for c in combinations(items, 1):
...     print(c)
...
('a',)
('b',)
('c',)
>>>
```
对于` combinations()` 来讲，元素的顺序已经不重要了。 也就是说，组合 ('a', 'b') 跟 ('b', 'a') 其实是一样的(最终只会输出其中一个)。


在计算组合的时候，一旦元素被选取就会从候选中剔除掉(比如如果元素’a’已经被选取了，那么接下来就不会再考虑它了)。 而函数 `itertools.combinations_with_replacement()` 允许同一个元素被选择多次，比如：
```python
>>> for c in combinations_with_replacement(items, 3):
...     print(c)
...
('a', 'a', 'a')
('a', 'a', 'b')
('a', 'a', 'c')
('a', 'b', 'b')
('a', 'b', 'c')
('a', 'c', 'c')
('b', 'b', 'b')
('b', 'b', 'c')
('b', 'c', 'c')
('c', 'c', 'c')
>>>
```

#### 🎯 enumerate()迭代器
`enumerate()` 函数返回的是一个 enumerate 对象实例， 它是一个迭代器，返回连续的包含一个计数和一个值的元组， 元组中的值通过在传入序列上调用 `next()` 返回。

将一个文件中出现的单词映射到它出现的行号上去，可以很容易的利用` enumerate()` 来完成：
```python
word_summary = defaultdict(list)

with open('myfile.txt', 'r') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    # Create a list of words in current line
    words = [w.strip().lower() for w in line.split()]
    for word in words:
        word_summary[word].append(idx)
```
处理完文件后打印 `word_summary` ，对于每个单词有一个 `key` ，每个 `key` 对应的值是一个由这个单词出现的行号组成的列表。 如果某个单词在一行中出现过两次，那么这个行号也会出现两次， 同时也可以作为文本的一个简单统计。


#### 🎯 zip()迭代器
`zip(a, b)` 会生成一个可返回元组 `(x, y)` 的迭代器，其中x来自a，y来自b。 一旦其中某个序列到底结尾，迭代宣告结束。 因此迭代长度跟参数中最短序列长度一致。
```python
>>> a = [1, 2, 3]
>>> b = ['w', 'x', 'y', 'z']
>>> for i in zip(a,b):
...     print(i)
...
(1, 'w')
(2, 'x')
(3, 'y')
>>>
```
若要对齐长度，则可使用 `itertools.zip_longest()` 函数来代替。比如：
```python
>>> from itertools import zip_longest
>>> for i in zip_longest(a,b):
...     print(i)
...
(1, 'w')
(2, 'x')
(3, 'y')
(None, 'z')

>>> for i in zip_longest(a, b, fillvalue=0):
...     print(i)
...
(1, 'w')
(2, 'x')
(3, 'y')
(0, 'z')
>>>
```

#### 🎯 不同集合上元素的迭代
`itertools.chain() `方法可以用来简化这个任务。 它接受一个可迭代对象列表作为输入，并返回一个迭代器，有效的屏蔽掉在多个容器中迭代细节。
```python
>>> from itertools import chain
>>> a = [1, 2, 3, 4]
>>> b = ['x', 'y', 'z']
>>> for x in chain(a, b):
... print(x)
...
1
2
3
4
x
y
z
>>>
```
`itertools.chain()` 接受一个或多个可迭代对象作为输入参数。 然后创建一个迭代器，依次连续的返回每个可迭代对象中的元素。 这种方式要比先将序列合并再迭代要高效的多。

#### 🎯 创建数据处理管道
```
foo/
    access-log-012007.gz
    access-log-022007.gz
    access-log-032007.gz
    ...
    access-log-012008
bar/
    access-log-092007.bz2
    ...
    access-log-022008

124.115.6.12 - - [10/Jul/2012:00:18:50 -0500] "GET /robots.txt ..." 200 71
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /ply/ ..." 200 11875
210.212.209.67 - - [10/Jul/2012:00:18:51 -0500] "GET /favicon.ico ..." 404 369
61.135.216.105 - - [10/Jul/2012:00:20:04 -0500] "GET /blog/atom.xml ..." 304 -
...
```
为了处理这些文件，定义一个由多个执行特定任务独立任务的简单生成器函数组成的容器。
```python
import os
import fnmatch
import gzip
import bz2
import re

def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line
```

可以很容易的将这些函数连起来创建一个处理管道。 比如，为了查找包含单词python的所有日志行。
```python
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)
```

甚至可以在生成器表达式中包装数据。 比如，下面这个版本计算出传输的字节数并计算其总和。
```python
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))
```

#### 🎯 展开嵌套的序列
可以写一个包含 yield from 语句的递归生成器来轻松解决这个问题。比如：
```python
from collections import Iterable

def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]
# Produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x)
```

语句 `yield from` 在想在生成器中调用其他生成器作为子例程的时候非常有用。

最后要注意的一点是， `yield from` 在涉及到基于协程和生成器的并发编程中扮演着更加重要的角色。 


#### 🎯 迭代器代替while无限循环
一个常见的IO操作程序可能会想下面这样：
```python
CHUNKSIZE = 8192

def reader(s):
    while True:
        data = s.recv(CHUNKSIZE)
        if data == b'':
            break
        process_data(data)
```
这种代码通常可以使用 `iter()` 来代替，如下所示：
```python
def reader2(s):
    for chunk in iter(lambda: s.recv(CHUNKSIZE), b''):
        pass
        # process_data(data)
```

`iter` 函数一个鲜为人知的特性是它接受一个可选的 `callable` 对象和一个标记(结尾)值作为输入参数。 当以这种方式使用的时候，它会创建一个迭代器， 这个迭代器会不断调用 `callable` 对象直到返回值和标记值相等为止。

这种特殊的方法对于一些特定的会被重复调用的函数很有效果，比如涉及到I/O调用的函数。 举例来讲，如果想从套接字或文件中以数据块的方式读取数据，通常得要不断重复的执行 `read()` 或 `recv()` ， 并在后面紧跟一个文件结尾测试来决定是否终止。这节中的方案使用一个简单的 `iter()` 调用就可以将两者结合起来了。 其中 `lambda` 函数参数是为了创建一个无参的 `callable` 对象，并为 `recv` 或 `read()` 方法提供了 `size` 参数。


### 🍞文件与IO

#### 🎯 读写文本数据

尽量使用 with 上下文管理器。使用带有 rt 模式的 open() 函数读取文本文件。如下所示：
```python
# Read the entire file as a single string
with open('somefile.txt', 'rt') as f:
    data = f.read()

# Iterate over the lines of the file
with open('somefile.txt', 'rt') as f:
    for line in f:
        # process line
        ...
```
类似的，为了写入一个文本文件，使用带有 wt 模式的 open() 函数， 如果之前文件内容存在则清除并覆盖掉。如下所示：
```python
# Write chunks of text data
with open('somefile.txt', 'wt') as f:
    f.write(text1)
    f.write(text2)
    ...

# Redirected print statement
with open('somefile.txt', 'wt') as f:
    print(line1, file=f)
    print(line2, file=f)
    ...
```

文件的读写操作默认使用系统编码，可以通过调用 `sys.getdefaultencoding()` 来得到。 在大多数机器上面都是utf-8编码。

Python支持非常多的文本编码。几个常见的编码是ascii, latin-1, utf-8和utf-16。 在web应用程序中通常都使用的是UTF-8。 ascii对应从U+0000到U+007F范围内的7位字符。 latin-1是字节0-255到U+0000至U+00FF范围内Unicode字符的直接映射。 当读取一个未知编码的文本时使用latin-1编码永远不会产生解码错误。 使用latin-1编码读取一个文件的时候也许不能产生完全正确的文本解码数据， 但是它也能从中提取出足够多的有用数据。同时，如果之后将数据回写回去，原先的数据还是会保留的。

#### 🎯 使用其他分隔符或行终止符打印

可以使用在 `print()` 函数中使用 `sep` 和 `end` 关键字参数，以想要的方式输出。比如：
```python
>>> print('ACME', 50, 91.5)
ACME 50 91.5
>>> print('ACME', 50, 91.5, sep=',')
ACME,50,91.5
>>> print('ACME', 50, 91.5, sep=',', end='!!\n')
ACME,50,91.5!!
>>>
```
使用 `end` 参数也可以在输出中禁止换行。比如：
```python
>>> for i in range(5):
...     print(i)
...
0
1
2
3
4
>>> for i in range(5):
...     print(i, end=' ')
...
0 1 2 3 4 >>>
```

#### 🎯 读写字节数据
使用模式为 `rb` 或 `wb` 的 `open()` 函数来读取或写入二进制数据。比如：
```python
# Read the entire file as a single byte string
with open('somefile.bin', 'rb') as f:
    data = f.read()

# Write binary data to a file
with open('somefile.bin', 'wb') as f:
    f.write(b'Hello World')
```
在读取二进制数据时，需要指明的是所有返回的数据都是字节字符串格式的，而不是文本字符串。 类似的，在写入的时候，必须保证参数是以字节形式对外暴露数据的对象(比如字节字符串，字节数组对象等)。

在读取二进制数据的时候，字节字符串和文本字符串的语义差异可能会导致一个潜在的陷阱。 特别需要注意的是，索引和迭代动作返回的是字节的值而不是字节字符串。比如：
```python
>>> # Text string
>>> t = 'Hello World'
>>> t[0]
'H'
>>> for c in t:
...     print(c)
...
H
e
l
l
o
...
>>> # Byte string
>>> b = b'Hello World'
>>> b[0]
72
>>> for c in b:
...     print(c)
...
72
101
108
108
111
...
>>>
```

如果想从二进制模式的文件中读取或写入文本数据，必须确保要进行解码和编码操作。比如：
```python
with open('somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')

with open('somefile.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))
```

#### 🎯 文件不存在才能写入

向一个文件中写入数据，但是前提必须是这个文件在文件系统上不存在。 也就是不允许覆盖已存在的文件内容。可以在 `open()` 函数中使用 `x` 模式来代替 `w` 模式的方法来解决这个问题。比如：
```python
>>> with open('somefile', 'wt') as f:
...     f.write('Hello\n')
...
>>> with open('somefile', 'xt') as f:
...     f.write('Hello\n')
...
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
FileExistsError: [Errno 17] File exists: 'somefile'
>>>
```
如果文件是二进制的，使用 `xb` 来代替 `xt`

#### 🎯 字符串的I/O操作
使用操作类文件对象的程序来操作文本或二进制字符串。使用 `io.StringIO()` 和 `io.BytesIO()` 类来创建类文件对象操作字符串数据。比如：
```python
>>> s = io.StringIO()
>>> s.write('Hello World\n')
12
>>> print('This is a test', file=s)
15
>>> # Get all of the data written so far
>>> s.getvalue()
'Hello World\nThis is a test\n'
>>>

>>> # Wrap a file interface around an existing string
>>> s = io.StringIO('Hello\nWorld\n')
>>> s.read(4)
'Hell'
>>> s.read()
'o\nWorld\n'
>>>
```

`io.StringIO` 只能用于文本。如果要操作二进制数据，要使用 `io.BytesIO` 类来代替。比如：
```python
>>> s = io.BytesIO()
>>> s.write(b'binary data')
>>> s.getvalue()
b'binary data'
>>>
```
当想模拟一个普通的文件的时候 `StringIO` 和 `BytesIO` 类是很有用的。 比如，在单元测试中，可以使用 `StringIO `来创建一个包含测试数据的类文件对象， 这个对象可以被传给某个参数为普通文件对象的函数。


#### 🎯 读写压缩文件
读写一个 gzip 或 bz2 格式的压缩文件。`gzip` 和 `bz2` 模块可以很容易的处理这些文件。 两个模块都为 `open()` 函数提供了另外的实现来解决这个问题。 比如，为了以文本形式读取压缩文件，可以这样做：
```python
# gzip compression
import gzip
with gzip.open('somefile.gz', 'rt') as f:
    text = f.read()

# bz2 compression
import bz2
with bz2.open('somefile.bz2', 'rt') as f:
    text = f.read()
```

类似的，为了写入压缩数据，可以这样做：
```python
# gzip compression
import gzip
with gzip.open('somefile.gz', 'wt') as f:
    f.write(text)

# bz2 compression
import bz2
with bz2.open('somefile.bz2', 'wt') as f:
    f.write(text)
```

如上，所有的I/O操作都使用文本模式并执行Unicode的编码/解码。 类似的，如果想操作二进制数据，使用 `rb` 或者 `wb` 文件模式即可。


大部分情况下读写压缩数据都是很简单的。但是要注意的是选择一个正确的文件模式是非常重要的。 如果不指定模式，那么默认的就是二进制模式，如果这时候程序想要接受的是文本数据，那么就会出错。 `gzip.open()` 和 `bz2.open()` 接受跟内置的 `open()` 函数一样的参数， 包括 `encoding`，`errors`，`newline` 等等。

当写入压缩数据时，可以使用 `compresslevel` 这个可选的关键字参数来指定一个压缩级别。比如：
```python
with gzip.open('somefile.gz', 'wt', compresslevel=5) as f:
    f.write(text)
```

默认的等级是9，也是最高的压缩等级。等级越低性能越好，但是数据压缩程度也越低。

最后一点， `gzip.open()` 和 `bz2.open()` 还有一个很少被知道的特性， 它们可以作用在一个已存在并以二进制模式打开的文件上。比如，下面代码是可行的：
```python
import gzip
f = open('somefile.gz', 'rb')
with gzip.open(f, 'rt') as g:
    text = g.read()
```

这样就允许 `gzip` 和 `bz2` 模块可以工作在许多类文件对象上，比如套接字，管道和内存中文件等。


#### 🎯 固定大小记录的文件迭代
在一个固定长度记录或者数据块的集合上迭代，而不是在一个文件中一行一行的迭代。
```python
from functools import partial

RECORD_SIZE = 32

with open('somefile.data', 'rb') as f:
    records = iter(partial(f.read, RECORD_SIZE), b'')
    for r in records:
        ...
```

这个例子中的 `records` 对象是一个可迭代对象，它会不断的产生固定大小的数据块，直到文件末尾。 要注意的是如果总记录大小不是块大小的整数倍的话，最后一个返回元素的字节数会比期望值少。

`iter() `函数有一个鲜为人知的特性就是，如果给它传递一个可调用对象和一个标记值，它会创建一个迭代器。 这个迭代器会一直调用传入的可调用对象直到它返回标记值为止，这时候迭代终止。

在例子中， `functools.partial` 用来创建一个每次被调用时从文件中读取固定数目字节的可调用对象。 标记值 `b''` 就是当到达文件结尾时的返回值。

最后再提一点，上面的例子中的文件时以二进制模式打开的。 如果是读取固定大小的记录，这通常是最普遍的情况。 而对于文本文件，一行一行的读取（默认的迭代行为）更普遍点。


#### 🎯 读取二进制数据到可变缓冲区中
直接读取二进制数据到一个可变缓冲区中，而不需要做任何的中间复制操作。 为了读取数据到一个可变数组中，使用文件对象的 readinto() 方法。比如：
```python
import os.path

def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf
```
下面是一个演示这个函数使用方法的例子：

```python
>>> # Write a sample file
>>> with open('sample.bin', 'wb') as f:
...     f.write(b'Hello World')
...
>>> buf = read_into_buffer('sample.bin')
>>> buf
bytearray(b'Hello World')
>>> buf[0:5] = b'HELLO'
>>> buf
bytearray(b'HELLO World')
>>> with open('newsample.bin', 'wb') as f:
...     f.write(buf)
...
11
>>>
```
文件对象的 `readinto()` 方法能被用来为预先分配内存的数组填充数据，甚至包括由 `array` 模块或 `numpy` 库创建的数组。 和普通 `read()` 方法不同的是， `readinto()` 填充已存在的缓冲区而不是为新对象重新分配内存再返回它们。 因此，可以使用它来避免大量的内存分配操作。 比如，读取一个由相同大小的记录组成的二进制文件时，可以像下面这样写：
```python
record_size = 32 # Size of each record (adjust value)

buf = bytearray(record_size)
with open('somefile', 'rb') as f:
    while True:
        n = f.readinto(buf)
        if n < record_size:
            break
        # Use the contents of buf
        ...
```

#### 🎯 序列化Python对象

对于序列化最普遍的做法就是使用 pickle 模块。为了将一个对象保存到一个文件中，可以这样做：

```python
import pickle

data = ... # Some Python object
f = open('somefile', 'wb')
pickle.dump(data, f)
```
为了将一个对象转储为一个字符串，可以使用 `pickle.dumps()` ：
```python
s = pickle.dumps(data)
```
为了从字节流中恢复一个对象，使用 `pickle.load()` 或 `pickle.loads()` 函数。比如：
```python
# Restore from a file
f = open('somefile', 'rb')
data = pickle.load(f)

# Restore from a string
data = pickle.loads(s)
```
