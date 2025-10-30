# 

### 🍞数字的操作

#### 🎯 整数(Int)操作
```python
# 基本运算
a, b = 10, 3
print(f"{a} + {b} = {a + b}")       # 输出: 10 + 3 = 13
print(f"{a} - {b} = {a - b}")       # 输出: 10 - 3 = 7
print(f"{a} * {b} = {a * b}")       # 输出: 10 * 3 = 30
print(f"{a} / {b} = {a / b}")       # 输出: 10 / 3 = 3.3333333333333335
print(f"{a} // {b} = {a // b}")     # 输出: 10 // 3 = 3 (整除)
print(f"{a} % {b} = {a % b}")       # 输出: 10 % 3 = 1 (取模)
print(f"{a} ** {b} = {a ** b}")     # 输出: 10 ** 3 = 1000 (幂运算)

# 位运算
x, y = 5, 3  # 5=0b101, 3=0b011
print(f"{x} & {y} = {x & y}")   # 输出: 5 & 3 = 1 (按位与 0b001)
print(f"{x} | {y} = {x | y}")   # 输出: 5 | 3 = 7 (按位或 0b111)
print(f"{x} ^ {y} = {x ^ y}")   # 输出: 5 ^ 3 = 6 (按位异或 0b110)
print(f"~{x} = {~x}")           # 输出: ~5 = -6 (按位取反)
print(f"{x} << 1 = {x << 1}")   # 输出: 5 << 1 = 10 (左移 0b1010)
print(f"{x} >> 1 = {x >> 1}")   # 输出: 5 >> 1 = 2 (右移 0b10)

# 进制转换
num = 255
print(f"255的二进制: {bin(num)}")       # 输出: 255的二进制: 0b11111111
print(f"255的八进制: {oct(num)}")       # 输出: 255的八进制: 0o377
print(f"255的十六进制: {hex(num)}")     # 输出: 255的十六进制: 0xff
```

#### 🎯 浮点数(Float)操作
```python
# 基本运算
f1, f2 = 3.5, 2.1
print(f"{f1} + {f2} = {f1 + f2}")  # 输出: 3.5 + 2.1 = 5.6
print(f"{f1} - {f2} = {f1 - f2}")  # 输出: 3.5 - 2.1 = 1.4
print(f"{f1} * {f2} = {f1 * f2}")  # 输出: 3.5 * 2.1 = 7.35
print(f"{f1} / {f2} = {f1 / f2}")  # 输出: 3.5 / 2.1 ≈ 1.6666666666666667

# 浮点数精度问题
print("0.1 + 0.2 =", 0.1 + 0.2)  # 输出: 0.1 + 0.2 = 0.30000000000000004

# 四舍五入
print(f"round(3.14159, 2) = {round(3.14159, 2)}")       # 输出: round(3.14159, 2) = 3.14
print(f"round(2.675, 2) = {round(2.675, 2)}")           # 输出: round(2.675, 2) = 2.67 (注意浮点数精度问题)
print(f"round(1627731, -2) = {round(1627731, -2)}")     # 输出: round(1627731, -2) = 1627700
```
精确的浮点数计算使用内置库，比如：math、decimal


#### 🎯 复数(Complex)操作
```python
c1 = 3 + 4j
c2 = 2 - 1j
print(f"{c1} + {c2} = {c1 + c2}")           # 输出: (3+4j) + (2-1j) = (5+3j)
print(f"{c1} * {c2} = {c1 * c2}")           # 输出: (3+4j) * (2-1j) = (10+5j)
print(f"{c1}的实部: {c1.real}")              # 输出: (3+4j)的实部: 3.0
print(f"{c1}的虚部: {c1.imag}")              # 输出: (3+4j)的虚部: 4.0
print(f"{c1}的共轭复数: {c1.conjugate()}")    # 输出: (3+4j)的共轭复数: (3-4j)
```

#### 🎯 无穷大与NaN
Python并没有特殊的语法来表示这些特殊的浮点值，但是可以使用 float() 来创建它们。比如：
```python
>>> a = float('inf')
>>> b = float('-inf')
>>> c = float('nan')
>>> a
inf
>>> b
-inf
>>> c
nan
>>>
```

#### 🎯 数字类型转换
```python
# 类型转换
i = 10
f = 3.14
print(f"int({f}) = {int(f)}")           # 输出: int(3.14) = 3
print(f"float({i}) = {float(i)}")       # 输出: float(10) = 10.0
print(f"complex({i}) = {complex(i)}")   # 输出: complex(10) = (10+0j)

# 字符串转数字
s1 = "123"
s2 = "3.14"
print(f"int('{s1}') = {int(s1)}")       # 输出: int('123') = 123
print(f"float('{s2}') = {float(s2)}")   # 输出: float('3.14') = 3.14
```

#### 🎯 数学函数
```python
# 内置函数
print(f"abs(-5) = {abs(-5)}")               # 输出: abs(-5) = 5
print(f"pow(2, 3) = {pow(2, 3)}")           # 输出: pow(2, 3) = 8
print(f"divmod(10, 3) = {divmod(10, 3)}")   # 输出: divmod(10, 3) = (3, 1)

# math模块函数
print(f"math.sqrt(16) = {math.sqrt(16)}")               # 输出: math.sqrt(16) = 4.0
print(f"math.exp(1) = {math.exp(1)}")                   # 输出: math.exp(1) ≈ 2.718281828459045
print(f"math.log(100, 10) = {math.log(100, 10)}")       # 输出: math.log(100, 10) = 2.0
print(f"math.sin(math.pi/2) = {math.sin(math.pi/2)}")   # 输出: math.sin(math.pi/2) ≈ 1.0
```

#### 🎯 数字格式化
```python
num = 1234567.89123
print(f"千分位格式化: {num:,}")     # 输出: 千分位格式化: 1,234,567.89123
print(f"保留2位小数: {num:.2f}")    # 输出: 保留2位小数: 1234567.89
print(f"科学计数法: {num:.2e}")     # 输出: 科学计数法: 1.23e+06
print(f"百分比格式: {0.256:.1%}")   # 输出: 百分比格式: 25.6%
x = 1234.56789
format(x, '>10.1f')     # '    1234.6'
format(x, '<10.1f')     # '1234.6    '
format(x, '^10.1f')     # '  1234.6  '
format(x, ',')          # '1,234.56789'
format(x, '0,.1f')      # '1,234.6'
```

#### 🎯 二八十六进制整数
将整数转换为二进制、八进制或十六进制的文本串， 可以分别使用 bin() , oct() 或 hex() 函数：
```python
>>> x = 1234
>>> bin(x)
'0b10011010010'
>>> oct(x)
'0o2322'
>>> hex(x)
'0x4d2'
>>>
```
另外，如果不想输出 0b , 0o 或者 0x 的前缀的话，可以使用 format() 函数。比如：
```python
>>> format(x, 'b')
'10011010010'
>>> format(x, 'o')
'2322'
>>> format(x, 'x')
'4d2'
>>>
```
大多数情况下处理二进制、八进制和十六进制整数是很简单的。 只要记住这些转换属于整数和其对应的文本表示之间的转换即可，永远只有一种整数类型。


#### 🎯 大整数
为了将bytes解析为整数，使用 `int.from_bytes()` 方法，并像下面这样指定字节顺序：
```python
>>> len(data)
16
>>> int.from_bytes(data, 'little')
69120565665751139577663547927094891008
>>> int.from_bytes(data, 'big')
94522842520747284487117727783387188
>>>
```
为了将一个大整数转换为一个字节字符串，使用 `int.to_bytes()` 方法，并像下面这样指定字节数和字节顺序：
```python
>>> x = 94522842520747284487117727783387188
>>> x.to_bytes(16, 'big')
b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
>>> x.to_bytes(16, 'little')
b'4\x00#\x00\x01\xef\xcd\x00\xab\x90x\x00V4\x12\x00'
>>>
```

大整数和字节字符串之间的转换操作并不常见。 然而，在一些应用领域有时候也会出现，比如密码学或者网络。 例如，IPv6网络地址使用一个128位的整数表示。 

作为一种替代方案，内置的 `struct` 模块可以用来解压字节。见内置库。

### 🍞字符串的操作

#### 🎯 简单查找

如果想匹配的是字面字符串，那么通常只需要调用基本字符串方法就行， 比如 str.find() , str.endswith() , str.startswith()
```python
>>> text = 'yeah, but no, but yeah, but no, but yeah'
>>> # Search for the location of the first occurrence
>>> text.find('no')
10
>>>
```

#### 🎯 检查开头或结尾
检查字符串开头或结尾的一个简单方法是使用 `str.startswith()` 或者是 `str.endswith()` 方法。

接收的参数必须是元组。
```python
>>> filename = 'spam.txt'
>>> filename.endswith('.txt')
True
>>> filename.startswith('file:')
False
>>> url = 'http://www.python.org'
>>> url.startswith('http:')
True
>>>

>>> import os
>>> filenames = os.listdir('.')
>>> filenames
[ 'Makefile', 'foo.c', 'bar.py', 'spam.c', 'spam.h' ]
>>> [name for name in filenames if name.endswith(('.c', '.h')) ]
['foo.c', 'spam.c', 'spam.h'
>>> any(name.endswith('.py') for name in filenames)
True

if any(name.endswith(('.c', '.h')) for name in listdir(dirname)):
...
```

#### 🎯 复杂查找
`fnmatch()` 函数匹配能力介于简单的字符串方法和强大的正则表达式之间。如果在数据处理操作中只需要简单的通配符就能完成的时候，这通常是一个比较合理的方案。

如果代码需要做文件名的匹配，最好使用 `glob` 模块。

```python
>>> from fnmatch import fnmatch, fnmatchcase
>>> fnmatch('foo.txt', '*.txt')
True
>>> fnmatch('foo.txt', '?oo.txt')
True
>>> fnmatch('Dat45.csv', 'Dat[0-9]*')
True
>>> names = ['Dat1.csv', 'Dat2.csv', 'config.ini', 'foo.py']
>>> [name for name in names if fnmatch(name, 'Dat*.csv')]
['Dat1.csv', 'Dat2.csv']
>>>

import glob
pyfiles = glob.glob('*.py')
print(pyfiles)  # 输出当前目录下所有的 Python 文件
```

#### 🎯 正则表达式查找
见 re 使用方法。


#### 🎯 分割
`string` 对象的 `split()` 方法只适应于非常简单的字符串分割情形， 它并不允许有多个分隔符或者是分隔符周围不确定的空格。 当需要更加灵活的切割字符串的时候，最好使用 `re.split()` 方法：
```python
>>> line = 'asdf fjdk; afed, fjek,asdf, foo'
>>> import re
>>> re.split(r'[;,\s]\s*', line)
['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']


>>> fields = re.split(r'(;|,|\s)\s*', line)
>>> fields
['asdf', ' ', 'fjdk', ';', 'afed', ',', 'fjek', ',', 'asdf', ',', 'foo']
>>>


>>> values = fields[::2]
>>> delimiters = fields[1::2] + ['']
>>> values
['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
>>> delimiters
[' ', ';', ',', ',', ',', '']
>>> # Reform the line using the same delimiters
>>> ''.join(v+d for v,d in zip(values, delimiters))
'asdf fjdk;afed,fjek,asdf,foo'


>>> re.split(r'(?:,|;|\s)\s*', line)
['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']
```


#### 🎯 替换
对于简单的字面模式，直接使用 `str.replace()` 方法即可，对于复杂的模式，使用 re 模块中的 sub() 函数。

#### 🎯 删除
`strip()` 方法能用于删除开始或结尾的字符。 `lstrip()` 和 `rstrip()` 分别从左和从右执行删除操作。

#### 🎯 清理
在非常简单的情形下，可能会选择使用字符串函数(比如`str.upper()`和 `str.lower()`)将文本转为标准格式。 使用`str.replace()`或者`re.sub()`的简单替换操作能删除或者改变指定的字符序列，同样还可以使用`unicodedata.normalize()`函数将 unicode 文本标准化。

使用 str.translate() 批量处理。

清理一个最主要的问题应该是运行的性能。一般来讲，代码越简单运行越快。 对于简单的替换操作，`str.replace()`方法通常是最快的，甚至需要多次调用的时候。如果要执行任何复杂字符对字符的重新映射或者删除操作的话，`translate()` 方法会非常的快。
```python
>>> s = 'pýtĥöñ\fis\tawesome\r\n'
>>> remap = {
...     ord('\t') : ' ',
...     ord('\f') : ' ',
...     ord('\r') : None # Deleted
... }
>>> a = s.translate(remap)
>>> a
'pýtĥöñ is awesome\n'
>>>
>>> import unicodedata
>>> import sys
>>> cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode)
...                         if unicodedata.combining(chr(c)))
...
>>> b = unicodedata.normalize('NFD', a)
>>> b
'pýtĥöñ is awesome\n'
>>> b.translate(cmb_chrs)
'python is awesome\n'
>>>
```

#### 🎯 格式化
函数`format()`可以用来很容易的对齐字符串。使用 `<`,`>` 或者`^`字符后面紧跟一个指定的宽度。
```python
>>> format(text, '>20')
'         Hello World'
>>> format(text, '<20')
'Hello World         '
>>> format(text, '^20')
'    Hello World     '
>>>
>>> format(text, '=>20s')
'=========Hello World'
>>> format(text, '*^20s')
'****Hello World*****'
>>>
```
其他对齐方式：

| 符号 | 对齐方式        | 示例          |
| :--- | :-------------- | :-------------------------- |
| `<`  | 左对齐          | `'Hello '`（填充右边）      |
| `>`  | 右对齐          | `' Hello'`（填充左边）      |
| `^`  | 居中对齐        | `' Hello '`（填充两边）     |
| `=`  | 填充符号 + 对齐 | `'====Hello'`（需配合 `>`） |


#### 🎯 拼接
如果要合并的字符串是在一个序列或者`iterable`中，那么最快的方式就是使用`join()`方法。

当我们使用加号(+)操作符去连接大量的字符串的时候是非常低效率的， 因为加号连接会引起内存复制以及垃圾回收操作。 特别的，永远都不应像下面这样写字符串连接代码：
```python
s = ''
for p in parts:
    s += p
```
同样还得注意不必要的字符串连接操作。有时候程序员在没有必要做连接操作的时候仍然多此一举。比如在打印的时候：
```python
print(a + ':' + b + ':' + c) # Ugly
print(':'.join([a, b, c])) # Still ugly
print(a, b, c, sep=':') # Better
```

当混合使用I/O操作和字符串连接操作的时候，有时候需要仔细研究。 比如，考虑下面的两端代码片段：
```python
# Version 1 (string concatenation)
f.write(chunk1 + chunk2)

# Version 2 (separate I/O operations)
f.write(chunk1)
f.write(chunk2)
```
如果两个字符串很小，那么第一个版本性能会更好些，因为I/O系统调用天生就慢。 另外一方面，如果两个字符串很大，那么第二个版本可能会更加高效， 因为它避免了创建一个很大的临时结果并且要复制大量的内存块数据。

#### 🎯 插入
Python并没有对在字符串中简单替换变量值提供直接的支持。 但是通过使用字符串的 `format()` 方法来解决这个问题。比如：
```python
>>> s = '{name} has {n} messages.'
>>> s.format(name='Guido', n=37)
'Guido has 37 messages.'
>>>
```
或者，如果要被替换的变量能在变量域中找到， 那么可以结合使用 `format_map()` 和 `vars()` 。就像下面这样：
```python
>>> name = 'Guido'
>>> n = 37
>>> s.format_map(vars())
'Guido has 37 messages.'
>>>
```
`format()` 和 `format_map()` 的一个缺陷就是它们并不能很好的处理变量缺失的情况，比如：
```python
>>> s.format(name='Guido')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'n'
>>>

class safesub(dict):
"""防止key找不到"""
def __missing__(self, key):
    return '{' + key + '}'

>>> del n # Make sure n is undefined
>>> s.format_map(safesub(vars()))
'Guido has {n} messages.'
>>>
```

#### 🎯 命名切片
如果程序包含了大量无法直视的硬编码切片，可以这样这样命名切片：
```python
######    0123456789012345678901234567890123456789012345678901234567890'
record = '....................100 .......513.25 ..........'
cost = int(record[20:23]) * float(record[31:37])

# 命名切片
SHARES = slice(20, 23)
PRICE = slice(31, 37)
cost = int(record[SHARES]) * float(record[PRICE])


>>> a = slice(5, 50, 2)
>>> a.start
5
>>> a.stop
50
>>> a.step
2
>>>
```


### 🍞列表的操作
```python
# 创建列表
lst = [1, 2, 3, 4, 5]
print(f"初始列表: {lst}")  # 输出: 初始列表: [1, 2, 3, 4, 5]

# 访问元素
print(f"第一个元素: {lst[0]}")  # 输出: 第一个元素: 1
print(f"最后一个元素: {lst[-1]}")  # 输出: 最后一个元素: 5
print(f"切片(1-3): {lst[1:3]}")  # 输出: 切片(1-3): [2, 3]

# 修改列表
lst[0] = 10
print(f"修改第一个元素后: {lst}")  # 输出: 修改第一个元素后: [10, 2, 3, 4, 5]

# 添加元素
lst.append(6)
print(f"追加元素后: {lst}")  # 输出: 追加元素后: [10, 2, 3, 4, 5, 6]

lst.insert(1, 1.5)
print(f"插入元素后: {lst}")  # 输出: 插入元素后: [10, 1.5, 2, 3, 4, 5, 6]

# 删除元素
del lst[0]
print(f"删除第一个元素后: {lst}")  # 输出: 删除第一个元素后: [1.5, 2, 3, 4, 5, 6]

popped = lst.pop()
print(f"弹出最后一个元素: {popped}, 剩余列表: {lst}")  # 输出: 弹出最后一个元素: 6, 剩余列表: [1.5, 2, 3, 4, 5]

lst.remove(3)
print(f"移除元素3后: {lst}")  # 输出: 移除元素3后: [1.5, 2, 4, 5]

# 列表操作
lst.extend([6, 7])
print(f"扩展列表后: {lst}")  # 输出: 扩展列表后: [1.5, 2, 4, 5, 6, 7]

lst.reverse()
print(f"反转列表后: {lst}")  # 输出: 反转列表后: [7, 6, 5, 4, 2, 1.5]

lst.sort()
print(f"排序后列表: {lst}")  # 输出: 排序后列表: [1.5, 2, 4, 5, 6, 7]

# 列表推导式
squares = [x**2 for x in lst]
print(f"列表推导式(平方): {squares}")  # 输出: 列表推导式(平方): [2.25, 4, 16, 25, 36, 49]

# 其他常用方法
print(f"列表长度: {len(lst)}")  # 输出: 列表长度: 6
print(f"元素5的索引: {lst.index(5)}")  # 输出: 元素5的索引: 3
print(f"元素2出现次数: {lst.count(2)}")  # 输出: 元素2出现次数: 1
```

### 🍞元组的操作
```python
# 创建元组
tup = (1, 2, 3, 4, 5)
print(f"初始元组: {tup}")  # 输出: 初始元组: (1, 2, 3, 4, 5)

# 访问元素
print(f"第一个元素: {tup[0]}")  # 输出: 第一个元素: 1
print(f"最后一个元素: {tup[-1]}")  # 输出: 最后一个元素: 5
print(f"切片(1-3): {tup[1:3]}")  # 输出: 切片(1-3): (2, 3)

# 元组是不可变的，以下操作会报错
# tup[0] = 10  # TypeError: 'tuple' object does not support item assignment

# 元组操作
print(f"元组长度: {len(tup)}")  # 输出: 元组长度: 5
print(f"元素3的索引: {tup.index(3)}")  # 输出: 元素3的索引: 2
print(f"元素2出现次数: {tup.count(2)}")  # 输出: 元素2出现次数: 1

# 元组解包
a, b, c, d, e = tup
print(f"解包结果: a={a}, b={b}, c={c}")  # 输出: 解包结果: a=1, b=2, c=3

# 元组连接
new_tup = tup + (6, 7)
print(f"连接后的新元组: {new_tup}")  # 输出: 连接后的新元组: (1, 2, 3, 4, 5, 6, 7)

# 元组与列表转换
lst_from_tup = list(tup)
print(f"元组转列表: {lst_from_tup}")  # 输出: 元组转列表: [1, 2, 3, 4, 5]

tup_from_lst = tuple(lst)
print(f"列表转元组: {tup_from_lst}")  # 输出: 列表转元组: (1.5, 2, 4, 5, 6, 7)
```

### 🍞列表和元组的区别

1. 列表是可变的(mutable)，元组是不可变的(immutable)
2. 列表使用方括号[]，元组使用圆括号()
3. 列表有更多内置方法(如append, remove等)
4. 元组通常用于异构数据，列表用于同构数据
5. 元组可以作为字典的键，列表不能


### 🍞将序列分解为单独的变量
任何的序列（或者是可迭代对象）可以通过一个简单的赋值操作来分解为单独的变量。 唯一的要求就是变量的总数和结构必须与序列相吻合。
```python
>>> p = (4, 5)
>>> x, y = p
>>> x
4
>>> y
5
>>>
>>> data = [ 'ACME', 50, 91.1, (2012, 12, 21) ]
>>> name, shares, price, date = data
>>> name
'ACME'
>>> date
(2012, 12, 21)
>>> name, shares, price, (year, mon, day) = data
>>> name
'ACME'
>>> year
2012
>>> mon
12
>>> day
21
>>>

>>> record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
>>> name, email, *phone_numbers = record
>>> name
'Dave'
>>> email
'dave@example.com'
>>> phone_numbers
['773-555-1212', '847-555-1212']
>>>
```

### 🍞删除序列相同元素并保持顺序
如果序列上的值都是`hashable`类型，那么可以很简单的利用集合或者生成器来解决这个问题。比如：
```python
def my_dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
```
使用方法：
```python
>>> a = [1, 5, 2, 1, 9, 1, 5, 10]
>>> list(my_dedupe(a))
[1, 5, 2, 9, 10]
>>>
```
这个方法仅仅在序列中元素为`hashable`的时候才管用。 如果想消除元素不可哈希（比如`dict`类型）的序列中重复元素的话，需要将上述代码稍微改变一下，就像这样：
```python
def my_dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)
```
使用方法：
```python
>>> a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
>>> list(my_dedupe(a, key=lambda d: (d['x'],d['y'])))
[{'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 4}]
>>> list(my_dedupe(a, key=lambda d: d['x']))
[{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
>>>
```

### 🍞过滤序列元素
有一个数据序列，想利用一些规则从中提取出需要的值或者是缩短序列

最简单的过滤序列元素的方法就是使用列表推导。比如：
```python
>>> mylist = [1, 4, -5, 10, -7, 2, 3, -1]
>>> [n for n in mylist if n > 0]
[1, 4, 10, 2, 3]
>>> [n for n in mylist if n < 0]
[-5, -7, -1]
>>>
```
使用列表推导的一个潜在缺陷就是如果输入非常大的时候会产生一个非常大的结果集，占用大量内存。 如果对内存比较敏感，那么可以使用生成器表达式迭代产生过滤的元素。比如：
```python
>>> pos = (n for n in mylist if n > 0)
>>> pos
<generator object <genexpr> at 0x1006a0eb0>
>>> for x in pos:
... print(x)
...
1
4
10
2
3
>>>
```
有时候，过滤规则比较复杂，不能简单的在列表推导或者生成器表达式中表达出来。 比如，假设过滤的时候需要处理一些异常或者其他复杂情况。这时候可以将过滤代码放到一个函数中， 然后使用内建的`filter()`函数。示例如下：
```python
values = ['1', '2', '-3', '-', '4', 'N/A', '5']
def is_int(val):
    try:
        x = int(val)
        return True
    except ValueError:
        return False
ivals = list(filter(is_int, values))
print(ivals)
# Outputs ['1', '2', '-3', '4', '5']
```

`itertools.compress()` 见内置模块


### 🍞转换并同时计算数据
在数据序列上执行聚集函数（比如 `sum()` , `min()` , `max()` ）， 但是首先需要先转换或者过滤数据。这种情况下一个非常优雅的方式去结合数据计算与转换就是使用一个生成器表达式参数。
```python
nums = [1, 2, 3, 4, 5]
s = sum(x * x for x in nums)
```
比 `sum((x * x for x in nums))` 优雅。


### 🍞解压可迭代对象赋值给多个变量
如果一个可迭代对象的元素个数超过变量个数时，会抛出一个`ValueError`。Python 的星号表达式可以用来解决这个问题。
```python
>>> record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
>>> name, email, *phone_numbers = record
>>> name
'Dave'
>>> email
'dave@example.com'
>>> phone_numbers
['773-555-1212', '847-555-1212']
>>>
```
星号表达式在迭代元素为可变长元组的序列时是很有用的。
```python
records = [
    ('foo', 1, 2),
    ('bar', 'hello'),
    ('foo', 3, 4),
]

def do_foo(x, y):
    print('foo', x, y)

def do_bar(s):
    print('bar', s)

for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
    elif tag == 'bar':
        do_bar(*args)
```

### 🍞集合的操作
#### 🎯 基本操作
```python
# 创建集合
s1 = {1, 2, 3, 4, 5}
s2 = {4, 5, 6, 7, 8}
print(f"集合s1: {s1}")  # 输出: 集合s1: {1, 2, 3, 4, 5}
print(f"集合s2: {s2}")  # 输出: 集合s2: {4, 5, 6, 7, 8}

# 添加元素
s1.add(6)
print(f"添加元素6后s1: {s1}")  # 输出: 添加元素6后s1: {1, 2, 3, 4, 5, 6}

# 删除元素
s1.remove(6)  # 如果元素不存在会报KeyError
print(f"删除元素6后s1: {s1}")  # 输出: 删除元素6后s1: {1, 2, 3, 4, 5}

s1.discard(10)  # 安全删除，元素不存在不会报错
print(f"尝试删除不存在的元素10后s1: {s1}")  # 输出: 尝试删除不存在的元素10后s1: {1, 2, 3, 4, 5}

popped = s1.pop()  # 随机删除并返回一个元素
print(f"弹出元素: {popped}, 剩余集合: {s1}")  # 输出示例: 弹出元素: 1, 剩余集合: {2, 3, 4, 5}

# 清空集合
s1.clear()
print(f"清空后的s1: {s1}")  # 输出: 清空后的s1: set()
```

#### 🎯 运算操作 
```python
s1 = {1, 2, 3, 4, 5}
s2 = {4, 5, 6, 7, 8}

# 并集
print(f"并集(s1 | s2): {s1 | s2}")  # 输出: 并集(s1 | s2): {1, 2, 3, 4, 5, 6, 7, 8}
print(f"并集(s1.union(s2)): {s1.union(s2)}")  # 同上

# 交集
print(f"交集(s1 & s2): {s1 & s2}")  # 输出: 交集(s1 & s2): {4, 5}
print(f"交集(s1.intersection(s2)): {s1.intersection(s2)}")  # 同上

# 差集
print(f"差集(s1 - s2): {s1 - s2}")  # 输出: 差集(s1 - s2): {1, 2, 3}
print(f"差集(s1.difference(s2)): {s1.difference(s2)}")  # 同上

# 对称差集(仅在其中一个集合中存在的元素)
print(f"对称差集(s1 ^ s2): {s1 ^ s2}")  # 输出: 对称差集(s1 ^ s2): {1, 2, 3, 6, 7, 8}
print(f"对称差集(s1.symmetric_difference(s2)): {s1.symmetric_difference(s2)}")  # 同上
```

#### 🎯 关系判断
```python
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}

# 子集判断
print(f"a是否是b的子集: {a.issubset(b)}")  # 输出: a是否是b的子集: True
print(f"a <= b: {a <= b}")  # 输出: a <= b: True

# 真子集判断
print(f"a是否是b的真子集: {a < b}")  # 输出: a是否是b的真子集: True

# 超集判断
print(f"b是否是a的超集: {b.issuperset(a)}")  # 输出: b是否是a的超集: True
print(f"b >= a: {b >= a}")  # 输出: b >= a: True

# 真超集判断
print(f"b是否是a的真超集: {b > a}")  # 输出: b是否是a的真超集: True

# 不相交判断
print(f"a和{6,7,8}是否不相交: {a.isdisjoint({6,7,8})}")  # 输出: a和{6,7,8}是否不相交: True
```

#### 🎯 其他操作
```python
# 集合长度
print(f"s1的长度: {len(s1)}")  # 输出: s1的长度: 5

# 检查元素是否存在
print(f"3是否在s1中: {3 in s1}")  # 输出: 3是否在s1中: True

# 集合推导式
squared = {x**2 for x in s1}
print(f"集合推导式(平方): {squared}")  # 输出示例: 集合推导式(平方): {16, 1, 4, 9, 25}

# 冻结集合(不可变集合)
fs = frozenset([1, 2, 3])
print(f"冻结集合: {fs}")  # 输出: 冻结集合: frozenset({1, 2, 3})
# fs.add(4)  # 报错: AttributeError: 'frozenset' object has no attribute 'add'
```

#### 🎯 集合与列表/元组转换
```python
# 列表/元组转集合(自动去重)
lst = [1, 2, 2, 3, 3, 3]
s = set(lst)
print(f"列表转集合(自动去重): {s}")  # 输出: 列表转集合(自动去重): {1, 2, 3}

# 集合转列表/元组
lst_from_set = list(s)
tup_from_set = tuple(s)
print(f"集合转列表: {lst_from_set}")  # 输出示例: 集合转列表: [1, 2, 3]
print(f"集合转元组: {tup_from_set}")  # 输出示例: 集合转元组: (1, 2, 3)
```

### 🍞字典的操作
#### 🎯 基本操作
```python
# 创建字典
d1 = {'name': 'Alice', 'age': 25, 'city': 'New York'}
d2 = dict(name='Bob', age=30, city='London')
print(f"字典d1: {d1}")  # 输出: 字典d1: {'name': 'Alice', 'age': 25, 'city': 'New York'}
print(f"字典d2: {d2}")  # 输出: 字典d2: {'name': 'Bob', 'age': 30, 'city': 'London'}

# 访问元素
print(f"获取name: {d1['name']}")  # 输出: 获取name: Alice
print(f"get方法获取age: {d1.get('age')}")  # 输出: get方法获取age: 25
print(f"获取不存在的key: {d1.get('country', 'USA')}")  # 输出: 获取不存在的key: USA

# 修改元素
d1['age'] = 26
print(f"修改age后: {d1}")  # 输出: 修改age后: {'name': 'Alice', 'age': 26, 'city': 'New York'}

# 添加元素
d1['gender'] = 'Female'
print(f"添加gender后: {d1}")  # 输出: 添加gender后: {'name': 'Alice', 'age': 26, 'city': 'New York', 'gender': 'Female'}

# 删除元素
del d1['gender']
print(f"删除gender后: {d1}")  # 输出: 删除gender后: {'name': 'Alice', 'age': 26, 'city': 'New York'}

popped = d1.pop('age')
print(f"弹出age: {popped}, 剩余字典: {d1}")  # 输出: 弹出age: 26, 剩余字典: {'name': 'Alice', 'city': 'New York'}

# 清空字典
d1.clear()
print(f"清空后的d1: {d1}")  # 输出: 清空后的d1: {}
```

#### 🎯 遍历操作
```python
d3 = {'name': 'Charlie', 'age': 35, 'city': 'Paris'}

# 遍历键
for key in d3.keys():
    print(key, end=" ")  # 输出: name age city 
print()

# 遍历值
for value in d3.values():
    print(value, end=" ")  # 输出: Charlie 35 Paris 
print()

# 遍历键值对
for key, value in d3.items():
    print(f"{key}:{value}", end=" ")  # 输出: name:Charlie age:35 city:Paris 
print()
```

#### 🎯 推导式
```python
numbers = [1, 2, 3, 4, 5]
squared_dict = {x: x**2 for x in numbers}
print(f"字典推导式(平方): {squared_dict}")  # 输出: 字典推导式(平方): {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# 条件字典推导式
even_squared = {x: x**2 for x in numbers if x % 2 == 0}
print(f"偶数平方字典: {even_squared}")  # 输出: 偶数平方字典: {2: 4, 4: 16}
```
构造一个字典，它是另外一个字典的子集。
```python
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}
# Make a dictionary of all prices over 200
p1 = {key: value for key, value in prices.items() if value > 200}
# Make a dictionary of tech stocks
tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
p2 = {key: value for key, value in prices.items() if key in tech_names}
```
大多数情况下字典推导能做到的，通过创建一个元组序列然后把它传给`dict()`函数也能实现。比如：
```python
p1 = dict((key, value) for key, value in prices.items() if value > 200)
```
但是，字典推导方式表意更清晰，并且实际上也会运行的更快些 （在这个例子中，实际测试几乎比`dict()`函数方式快整整一倍）。

#### 🎯 合并与更新
```python
d4 = {'a': 1, 'b': 2}
d5 = {'b': 3, 'c': 4}

# 合并字典(Python 3.9+)
merged = d4 | d5
print(f"合并后的字典: {merged}")  # 输出: 合并后的字典: {'a': 1, 'b': 3, 'c': 4}

# 更新字典
d4.update(d5)
print(f"更新后的d4: {d4}")  # 输出: 更新后的d4: {'a': 1, 'b': 3, 'c': 4}
```

collections 中的 ChainMap 类也能合并字典，见内置库。

#### 🎯 其他操作
```python
d6 = {'apple': 3, 'banana': 5, 'orange': 2}

# 检查键是否存在
print(f"'apple'是否在字典中: {'apple' in d6}")  # 输出: 'apple'是否在字典中: True

# 字典长度
print(f"字典长度: {len(d6)}")  # 输出: 字典长度: 3

# 设置默认值
count = d6.setdefault('pear', 0)
print(f"pear的计数: {count}, 字典: {d6}")  # 输出: pear的计数: 0, 字典: {'apple': 3, 'banana': 5, 'orange': 2, 'pear': 0}

# 获取所有键/值/键值对
print(f"所有键: {d6.keys()}")  # 输出: 所有键: dict_keys(['apple', 'banana', 'orange', 'pear'])
print(f"所有值: {d6.values()}")  # 输出: 所有值: dict_values([3, 5, 2, 0])
print(f"所有键值对: {d6.items()}")  # 输出: 所有键值对: dict_items([('apple', 3), ('banana', 5), ('orange', 2), ('pear', 0)])
```

#### 🎯 字典与列表转换
```python
# 字典转列表(键/值/键值对)
keys_list = list(d6.keys())
values_list = list(d6.values())
items_list = list(d6.items())
print(f"键列表: {keys_list}")  # 输出: 键列表: ['apple', 'banana', 'orange', 'pear']
print(f"值列表: {values_list}")  # 输出: 值列表: [3, 5, 2, 0]
print(f"键值对列表: {items_list}")  # 输出: 键值对列表: [('apple', 3), ('banana', 5), ('orange', 2), ('pear', 0)]

# 列表转字典(需要特定格式)
pairs = [('a', 1), ('b', 2), ('c', 3)]
dict_from_list = dict(pairs)
print(f"列表转字典: {dict_from_list}")  # 输出: 列表转字典: {'a': 1, 'b': 2, 'c': 3}
```

#### 🎯 字典排序
```python
scores = {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'David': 95}

# 按键排序
sorted_by_key = dict(sorted(scores.items()))
print(f"按键排序: {sorted_by_key}")  # 输出: 按键排序: {'Alice': 85, 'Bob': 92, 'Charlie': 78, 'David': 95}

# 按值排序(降序)
sorted_by_value = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
print(f"按值排序(降序): {sorted_by_value}")  # 输出: 按值排序(降序): {'David': 95, 'Bob': 92, 'Alice': 85, 'Charlie': 78}

# 最小值/最大值
min_price = min(zip(scores.values(), scores.keys()))    # 输出: (78, 'Charlie')
max_price = max(zip(scores.values(), scores.keys()))    # 输出: (95, 'David')
```
需要注意的是`zip()`函数创建的是一个只能访问一次的迭代器。
```python
scores_and_names = zip(scores.values(), scores.keys())
print(min(scores_and_names)) # OK
print(max(scores_and_names)) # ValueError: max() arg is an empty sequence
```

