# 

面向函数编程（Functional Programming，FP）

🌟 核心思想：

程序是由纯函数组成的，不依赖和修改全局状态，强调函数即一等公民（函数可以作为参数、返回值、赋值等）。

🧩 特征：

| 特征     | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| 纯函数   | 无副作用，相同输入永远产生相同输出                           |
| 不可变性 | 避免修改状态，变量尽量不变                                   |
| 高阶函数 | 接收函数作为参数，或返回函数                                 |
| 函数组合 | 函数嵌套使用，形成管道式流程（如 `map`、`filter`、`reduce`） |



面向对象编程（Object-Oriented Programming，OOP）

🌟 核心思想：

将数据和操作数据的**方法封装在一起**，通过“对象”来组织程序结构。强调“**对象即实体**”。

🧩 基本概念：

| 概念           | 说明                                   |
| -------------- | -------------------------------------- |
| 类（Class）    | 模板或蓝图，定义对象的属性和行为       |
| 对象（Object） | 类的实例，表示实际存在的实体           |
| 封装           | 把数据和方法绑定到一起，隐藏内部实现   |
| 继承           | 子类继承父类的属性和方法，代码复用     |
| 多态           | 不同对象可以调用同一接口，实现不同功能 |



🔍 对比总结：

| 特点     | OOP                               | FP                                 |
| -------- | --------------------------------- | ---------------------------------- |
| 编程方式 | 基于对象                          | 基于函数                           |
| 状态管理 | 倾向于可变状态                    | 倾向于不可变                       |
| 抽象焦点 | 实体（对象）                      | 行为（函数）                       |
| 适用场景 | GUI、游戏开发、需要管理状态的系统 | 数据处理、并发计算、逻辑清晰的任务 |
| 代码结构 | 更偏结构化                        | 更偏流程化                         |



### 🍞 函数

#### 🎯 可接受任意数量参数的函数
为了能让一个函数接受任意数量的位置参数，可以使用一个*参数。例如：
```python
def avg(first, *rest):
    return (first + sum(rest)) / (1 + len(rest))

# Sample use
avg(1, 2) # 1.5
avg(1, 2, 3, 4) # 2.5
```

为了接受任意数量的关键字参数，使用一个以**开头的参数。比如：
```python
import html

def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(
                name=name,
                attrs=attr_str,
                value=html.escape(value))
    return element

# Example
# Creates '<item size="large" quantity="6">Albatross</item>'
make_element('item', 'Albatross', size='large', quantity=6)

# Creates '<p>&lt;spam&gt;</p>'
make_element('p', '<spam>')
```
在这里，attrs是一个包含所有被传入进来的关键字参数的字典。

如果还希望某个函数能同时接受任意数量的位置参数和关键字参数，可以同时使用*和**。比如：
```python
def anyargs(*args, **kwargs):
    print(args) # A tuple
    print(kwargs) # A dict
```

使用这个函数时，所有位置参数会被放到args元组中，所有关键字参数会被放到字典kwargs中。


#### 🎯 只接受关键字参数的函数
希望函数的某些参数强制使用关键字参数传递，将强制关键字参数放到某个*参数或者单个*后面就能达到这种效果。比如：
```python
def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, True) # TypeError
recv(1024, block=True) # Ok
```
利用这种技术，我们还能在接受任意多个位置参数的函数中指定关键字参数。比如：
```python
def minimum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m

minimum(1, 5, 2, -5, 10) # Returns -5
minimum(1, 5, 2, -5, 10, clip=0) # Returns 0
```
很多情况下，使用强制关键字参数会比使用位置参数表意更加清晰，程序也更加具有可读性。 例如，考虑下如下一个函数调用：
```python
msg = recv(1024, False)
```
如果调用者对recv函数并不是很熟悉，那他肯定不明白那个False参数到底来干嘛用的。 但是，如果代码变成下面这样子的话就清楚多了：
```python
msg = recv(1024, block=False)
```
另外，使用强制关键字参数也会比使用**kwargs参数更好，因为在使用函数help的时候输出也会更容易理解：
```python
>>> help(recv)
Help on function recv in module __main__:
recv(maxsize, *, block)
    Receives a message
```
强制关键字参数在一些更高级场合同样也很有用。 例如，它们可以被用来在使用*args和**kwargs参数作为输入的函数中插入参数。

#### 🎯 给函数参数增加元信息
写好了一个函数，然后想为这个函数的参数增加一些额外的信息，这样的话其他使用者就能清楚的知道这个函数应该怎么使用。

使用函数参数注解是一个很好的办法，它能提示程序员应该怎样正确使用这个函数。 例如，下面有一个被注解了的函数：
```python
def add(x:int, y:int) -> int:
    return x + y
```
python解释器不会对这些注解添加任何的语义。它们不会被类型检查，运行时跟没有加注解之前的效果也没有任何差距。 然而，对于那些阅读源码的人来讲就很有帮助啦。第三方工具和框架可能会对这些注解添加语义。同时它们也会出现在文档中。
```python
>>> help(add)
Help on function add in module __main__:
add(x: int, y: int) -> int
>>>
```
尽管可以使用任意类型的对象给函数添加注解(例如数字，字符串，对象实例等等)，不过通常来讲使用类或者字符串会比较好点。

函数注解只存储在函数的 `__annotations__` 属性中。例如：
```python
>>> add.__annotations__
{'y': <class 'int'>, 'return': <class 'int'>, 'x': <class 'int'>}
```
尽管注解的使用方法可能有很多种，但是它们的主要用途还是文档。 因为python并没有类型声明，通常来讲仅仅通过阅读源码很难知道应该传递什么样的参数给这个函数。 这时候使用注解就能给程序员更多的提示，让他们可以正确的使用函数。


#### 🎯 返回多个值的函数
为了能返回多个值，函数直接return一个元组就行了。例如：
```python
>>> def myfun():
... return 1, 2, 3
...
>>> a, b, c = myfun()
>>> a
1
>>> b
2
>>> c
3
```
尽管`myfun()`看上去返回了多个值，实际上是先创建了一个元组然后返回的。 这个语法看上去比较奇怪，实际上我们使用的是逗号来生成一个元组，而不是用括号。比如下面的：
```python
>>> a = (1, 2) # With parentheses
>>> a
(1, 2)
>>> b = 1, 2 # Without parentheses
>>> b
(1, 2)
>>>
```

#### 🎯 定义有默认参数的函数
定义一个有可选参数的函数是非常简单的，直接在函数定义中给参数指定一个默认值，并放到参数列表最后就行了。例如：
```python
def spam(a, b=42):
    print(a, b)

spam(1) # Ok. a=1, b=42
spam(1, 2) # Ok. a=1, b=2
```
如果默认参数是一个可修改的容器比如一个列表、集合或者字典，可以使用None作为默认值，就像下面这样：
```python
# Using a list as a default value
def spam(a, b=None):
    if b is None:
        b = []
    ...
```
如果并不想提供一个默认值，而是想仅仅测试下某个默认参数是不是有传递进来，可以像下面这样写：
```python
_no_value = object()

def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')
    ...

>>> spam(1)
No b value supplied
>>> spam(1, 2) # b = 2
>>> spam(1, None) # b = None
>>>
```
仔细观察可以发现到传递一个None值和不传值两种情况是有差别的。


定义带默认值参数的函数是很简单的，但绝不仅仅只是这个，还有一些东西在这里也深入讨论下。

首先，默认参数的值仅仅在函数定义的时候赋值一次。试着运行下面这个例子：

```python
>>> x = 42
>>> def spam(a, b=x):
...     print(a, b)
...
>>> spam(1)
1 42
>>> x = 23 # Has no effect
>>> spam(1)
1 42
>>>
```

注意到当我们改变x的值的时候对默认参数值并没有影响，这是因为在函数定义的时候就已经确定了它的默认值了。

其次，默认参数的值应该是不可变的对象，比如None、True、False、数字或字符串。 特别的，千万不要像下面这样写代码：
```python
def spam(a, b=[]): # NO!
    ...
```
为了避免这种情况的发生，最好是将默认值设为None， 然后在函数里面检查它，在测试None值时使用 is 操作符是很重要的，也是这种方案的关键点。 

#### 🎯 定义匿名或内联函数
为 `sort()` 操作创建一个很短的回调函数，但又不想用 def 去写一个单行函数， 而是希望通过某个快捷方式以内联方式来创建这个函数。

当一些函数很简单，仅仅只是计算一个表达式的值的时候，就可以使用lambda表达式来代替了。比如：
```python
>>> add = lambda x, y: x + y
>>> add(2,3)
5
>>> add('hello', 'world')
'helloworld'
>>>
```
`lambda`表达式典型的使用场景是排序或数据`reduce`等：
```python
>>> names = ['David Beazley', 'Brian Jones',
...         'Raymond Hettinger', 'Ned Batchelder']
>>> sorted(names, key=lambda name: name.split()[-1].lower())
['Ned Batchelder', 'David Beazley', 'Raymond Hettinger', 'Brian Jones']
>>>
```
尽管`lambda`表达式允许定义简单函数，但是它的使用是有限制的。 只能指定单个表达式，它的值就是最后的返回值。也就是说不能包含其他的语言特性了， 包括多个语句、条件表达式、迭代以及异常处理等等。

可以不使用`lambda`表达式就能编写大部分python代码。 但是，当有人编写大量计算表达式值的短小函数或者需要用户提供回调函数的程序的时候， 就会看到`lambda`表达式的身影了。



#### 🎯 匿名函数捕获变量值

用lambda定义了一个匿名函数，并想在定义时捕获到某些变量的值。
```python
>>> x = 10
>>> a = lambda y: x + y
>>> x = 20
>>> b = lambda y: x + y
>>>
```
现在我问，a(10)和b(10)返回的结果是什么？如果认为结果是20和30，那么就错了：
```python
>>> a(10)
30
>>> b(10)
30
>>>
```
这其中的奥妙在于lambda表达式中的x是一个自由变量， 在运行时绑定值，而不是定义时就绑定，这跟函数的默认值参数定义是不同的。 因此，在调用这个lambda表达式的时候，x的值是执行时的值。例如：
```python
>>> x = 15
>>> a(10)
25
>>> x = 3
>>> a(10)
13
>>>
```
如果想让某个匿名函数在定义时就捕获到值，可以将那个参数值定义成默认参数即可，就像下面这样：
```python
>>> x = 10
>>> a = lambda y, x=x: x + y
>>> x = 20
>>> b = lambda y, x=x: x + y
>>> a(10)
20
>>> b(10)
30
>>>
```
在这里列出来的问题是新手很容易犯的错误，有些新手可能会不恰当的使用lambda表达式。 比如，通过在一个循环或列表推导中创建一个lambda表达式列表，并期望函数能在定义时就记住每次的迭代值。例如：
```python
>>> funcs = [lambda x: x+n for n in range(5)]
>>> for f in funcs:
... print(f(0))
...
4
4
4
4
4
>>>
```
但是实际效果是运行是n的值为迭代的最后一个值。现在我们用另一种方式修改一下：
```python
>>> funcs = [lambda x, n=n: x+n for n in range(5)]
>>> for f in funcs:
... print(f(0))
...
0
1
2
3
4
>>>
```
通过使用函数默认值参数形式，lambda函数在定义时就能绑定到值。(因为默认值参数在定义是就确定了)


#### 🎯 减少可调用对象的参数个数

有一个被其他python代码使用的callable对象，可能是一个回调函数或者是一个处理器， 但是它的参数太多了，导致调用时出错。

如果需要减少某个函数的参数个数，可以使用 `functools.partial()` 。 `partial()` 函数允许给一个或多个参数设置固定的值，减少接下来被调用时的参数个数。 有下面这样的函数：
```python
def spam(a, b, c, d):
    print(a, b, c, d)
```
使用 partial() 函数来固定某些参数值：
```python
>>> from functools import partial
>>> s1 = partial(spam, 1) # a = 1
>>> s1(2, 3, 4)
1 2 3 4
>>> s1(4, 5, 6)
1 4 5 6
>>> s2 = partial(spam, d=42) # d = 42
>>> s2(1, 2, 3)
1 2 3 42
>>> s2(4, 5, 5)
4 5 5 42
>>> s3 = partial(spam, 1, 2, d=42) # a = 1, b = 2, d = 42
>>> s3(3)
1 2 3 42
>>> s3(4)
1 2 4 42
>>> s3(5)
1 2 5 42
>>>
```
可以看出 `partial()`固定某些参数并返回一个新的callable对象。这个新的callable接受未赋值的参数， 然后跟之前已经赋值过的参数合并起来，最后将所有参数传递给原始函数。



#### 🎯 将单方法的类转换为函数（闭包）

🧠 闭包的定义

> **闭包是一个函数，它“记住了”它被创建时的作用域，即使外层函数已经结束。**

也就是说：**内部函数可以访问外部函数的变量，即使外部函数已经返回！**



✅ 形成闭包的三个必要条件：

1. 有一个**嵌套函数**（函数中定义函数）
2. 外层函数返回内层函数
3. 内层函数引用了外层函数的变量



🌰：有一个除 `__init__()` 方法外只定义了一个方法的类。为了简化代码，将它转换成一个函数。

大多数情况下，可以使用闭包来将单个方法的类转换成函数。 举个例子，下面示例中的类允许使用者根据某个模板方案来获取到URL链接地址。

```python
from urllib.request import urlopen

class UrlTemplate:
    def __init__(self, template):
        self.template = template

    def open(self, **kwargs):
        return urlopen(self.template.format_map(kwargs))

# Example use. Download stock data from yahoo
yahoo = UrlTemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo.open(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))
```

这个类可以被一个更简单的函数来代替：
```python
def urltemplate(template):
    def opener(**kwargs):
        return urlopen(template.format_map(kwargs))
    return opener

# Example use
yahoo = urltemplate('http://finance.yahoo.com/d/quotes.csv?s={names}&f={fields}')
for line in yahoo(names='IBM,AAPL,FB', fields='sl1c1v'):
    print(line.decode('utf-8'))
```

大部分情况下，拥有一个单方法类的原因是需要存储某些额外的状态来给方法使用。 比如，定义UrlTemplate类的唯一目的就是先在某个地方存储模板值，以便将来可以在`open()`方法中使用。

使用一个内部函数或者闭包的方案通常会更优雅一些。简单来讲，一个闭包就是一个函数， 只不过在函数内部带上了一个额外的变量环境。闭包关键特点就是它会记住自己被定义时的环境。 因此，在我们的解决方案中，`opener()` 函数记住了 `template` 参数的值，并在接下来的调用中使用它。

任何时候只要碰到需要给某个函数增加额外的状态信息的问题，都可以考虑使用闭包。 相比将的函数转换成一个类而言，闭包通常是一种更加简洁和优雅的方案。


#### 🎯 带额外状态信息的回调函数

代码中需要依赖到回调函数的使用(比如事件处理器、等待后台任务完成后的回调等)， 并且还需要让回调函数拥有额外的状态值，以便在它的内部使用到。

这里主要讨论的是那些出现在很多函数库和框架中的回调函数的使用——特别是跟异步处理有关的。 为了演示与测试，先定义如下一个需要调用回调函数的函数：

```python
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)


>>> def print_result(result):
...     print('Got:', result)
...
>>> def add(x, y):
...     return x + y
...
>>> apply_async(add, (2, 3), callback=print_result)
Got: 5
>>> apply_async(add, ('hello', 'world'), callback=print_result)
Got: helloworld
>>>
```

注意到 `print_result()` 函数仅仅只接受一个参数 `result` 。不能再传入其他信息。 而当想让回调函数访问其他变量或者特定环境的变量值的时候就会遇到麻烦。

为了让回调函数访问外部信息，一种方法是使用一个绑定方法来代替一个简单函数。 比如，下面这个类会保存一个内部序列号，每次接收到一个 `result` 的时候序列号加1：

```python
class ResultHandler:

    def __init__(self):
        self.sequence = 0

    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))

>>> r = ResultHandler()
>>> apply_async(add, (2, 3), callback=r.handler)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=r.handler)
[2] Got: helloworld
>>>
```

第二种方式，作为类的替代，可以使用一个闭包捕获状态值，例如：

如果使用闭包，需要注意对那些可修改变量的操作。在下面的方案中， nonlocal 声明语句用来指示接下来的变量会在回调函数中被修改。如果没有这个声明，代码会报错。
```python
def make_handler():
    sequence = 0
    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler


>>> handler = make_handler()
>>> apply_async(add, (2, 3), callback=handler)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=handler)
[2] Got: helloworld
>>>
```

还有另外一个更高级的方法，可以使用协程来完成同样的事情：
```python
def make_handler():
    sequence = 0
    while True:
        result = yield
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))


>>> handler = make_handler()
>>> next(handler) # Advance to the yield
>>> apply_async(add, (2, 3), callback=handler.send)
[1] Got: 5
>>> apply_async(add, ('hello', 'world'), callback=handler.send)
[2] Got: helloworld
>>>
```

基于回调函数的软件通常都有可能变得非常复杂。一部分原因是回调函数通常会跟请求执行代码断开。 因此，请求执行和处理结果之间的执行环境实际上已经丢失了。如果想让回调函数连续执行多步操作， 那就必须去解决如何保存和恢复相关的状态信息了。


#### 🎯 内联回调函数

编写使用回调函数的代码的时候，担心很多小函数的扩张可能会弄乱程序控制流。希望找到某个方法来让代码看上去更像是一个普通的执行序列。

通过使用生成器和协程可以使得回调函数内联在某个函数中。
```python
def apply_async(func, args, *, callback):
    # Compute the result
    result = func(*args)

    # Invoke the callback with the result
    callback(result)

from queue import Queue
from functools import wraps

class Async:
    def __init__(self, func, args):
        self.func = func
        self.args = args

def inlined_async(func):
    @wraps(func)
    def wrapper(*args):
        f = func(*args)
        result_queue = Queue()
        result_queue.put(None)
        while True:
            result = result_queue.get()
            try:
                a = f.send(result)
                apply_async(a.func, a.args, callback=result_queue.put)
            except StopIteration:
                break
    return wrapper

def add(x, y):
    return x + y

@inlined_async
def test():
    r = yield Async(add, (2, 3))
    print(r)
    r = yield Async(add, ('hello', 'world'))
    print(r)
    for n in range(10):
        r = yield Async(add, (n, n))
        print(r)
    print('Goodbye')
```
发现除了那个特别的装饰器和 `yield` 语句外，其他地方并没有出现任何的回调函数(其实是在后台定义的)。

将复杂的控制流隐藏到生成器函数背后的例子在标准库和第三方包中都能看到。 比如，在 `contextlib` 中的 `@contextmanager` 装饰器使用了一个令人费解的技巧， 通过一个 `yield` 语句将进入和离开上下文管理器粘合在一起。 另外非常流行的 `Twisted` 包中也包含了非常类似的内联回调。



#### 🎯 访问闭包中定义的变量

想要扩展函数中的某个闭包，允许它能访问和修改函数的内部变量。

通常来讲，闭包的内部变量对于外界来讲是完全隐藏的。 但是，可以通过编写访问函数并将其作为函数属性绑定到闭包上来实现这个目的。例如：
```python
def sample():
    n = 0
    # Closure function
    def func():
        print('n=', n)

    # Accessor methods for n
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    # Attach as function attributes
    func.get_n = get_n
    func.set_n = set_n
    return func
```
下面是使用的例子:
```python
>>> f = sample()
>>> f()
n= 0
>>> f.set_n(10)
>>> f()
n= 10
>>> f.get_n()
10
>>>
```

首先，nonlocal 声明可以让我们编写函数来修改内部变量的值。 其次，函数属性允许我们用一种很简单的方式将访问方法绑定到闭包函数上，这个跟实例方法很像(尽管并没有定义任何类)。

还可以进一步的扩展，让闭包模拟类的实例。



### 🍞 类与对象

#### 🎯 封装、继承、多态

- **封装 (Encapsulation):** 这指的是将数据（属性）和操作数据的方法捆绑到一个单元（即一个类）中。在 Python 中，可以通过将属性声明为私有（以两个下划线开头）来隐藏对象的内部状态，只允许通过对象的方法进行访问和修改。这有助于保护数据不被意外更改。

  

- **继承 (Inheritance):** 继承是一种机制，一个类（称为子类或派生类）可以继承另一个类（称为父类或基类）的属性和方法。这使得子类可以重用父类的代码，并可以添加自己独特的功能或覆盖父类的方法以满足特定需求。

  

- **多态 (Polymorphism):** 多态意味着不同类的对象可以对相同的方法名做出不同的响应。简单来说，就是允许我们以同样的方式处理不同类型的对象。例如，一个函数可以接受任何具有特定方法（如 `fly()`）的对象，而不管这个对象是鸟还是飞机，调用该方法时会执行各自类的实现。

  

#### 🎯 改变对象的字符串显示

要改变一个实例的字符串表示，可重新定义它的 `__str__()` 和 `__repr__()` 方法。例如：
```python
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Pair({0.x!r}, {0.y!r})'.format(self)

    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)
```
`__repr__()` 方法返回一个实例的代码表示形式，通常用来重新构造这个实例。 内置的 repr() 函数返回这个字符串，跟我们使用交互式解释器显示的值是一样的。` __str__()` 方法将实例转换为一个字符串，使用 `str()` 或 `print()` 函数会输出这个字符串。比如：

```python
>>> p = Pair(3, 4)
>>> p
Pair(3, 4) # __repr__() output
>>> print(p)
(3, 4) # __str__() output
>>>
```
我们在这里还演示了在格式化的时候怎样使用不同的字符串表现形式。 特别来讲，`!r` 格式化代码指明输出使用 `__repr__()` 来代替默认的 `__str__()` 。 可以用前面的类来试着测试下：
```python
>>> p = Pair(3, 4)
>>> print('p is {0!r}'.format(p))
p is Pair(3, 4)
>>> print('p is {0}'.format(p))
p is (3, 4)
>>>
```
上面的 `format()` 方法的使用看上去很有趣，格式化代码 `{0.x}` 对应的是第1个参数的x属性。 因此，在下面的函数中，0实际上指的就是 `self` 本身：
```python
def __repr__(self):
    return 'Pair({0.x!r}, {0.y!r})'.format(self)
```
作为这种实现的一个替代，也可以使用`%` 操作符，就像下面这样：
```python
def __repr__(self):
    return 'Pair(%r, %r)' % (self.x, self.y)
```


#### 🎯 自定义字符串的格式化

通过 `format()` 函数和字符串方法使得一个对象能支持自定义的格式化。

为了自定义字符串的格式化，我们需要在类上面定义 `__format__()` 方法。例如：
```python
_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
    }

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)
```
现在 `Date` 类的实例可以支持格式化操作了，如同下面这样：
```python
>>> d = Date(2012, 12, 21)
>>> format(d)
'2012-12-21'
>>> format(d, 'mdy')
'12/21/2012'
>>> 'The date is {:ymd}'.format(d)
'The date is 2012-12-21'
>>> 'The date is {:mdy}'.format(d)
'The date is 12/21/2012'
>>>
```

#### 🎯 让对象支持上下文管理协议
为了让一个对象兼容 `with` 语句，需要实现 `__enter__()` 和 `__exit__()` 方法。 例如，考虑如下的一个类，它能为我们创建一个网络连接：
```python
from socket import socket, AF_INET, SOCK_STREAM

class LazyConnection:
    def __init__(self, address, family=AF_INET, type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.type = type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('Already connected')
        self.sock = socket(self.family, self.type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None
```
这个类的关键特点在于它表示了一个网络连接，但是初始化的时候并不会做任何事情(比如它并没有建立一个连接)。 连接的建立和关闭是使用 `with` 语句自动完成的，例如：
```python
from functools import partial

conn = LazyConnection(('www.python.org', 80))
# Connection closed
with conn as s:
    # conn.__enter__() executes: connection open
    s.send(b'GET /index.html HTTP/1.0\r\n')
    s.send(b'Host: www.python.org\r\n')
    s.send(b'\r\n')
    resp = b''.join(iter(partial(s.recv, 8192), b''))
    # conn.__exit__() executes: connection closed
```

编写上下文管理器的主要原理是的代码会放到 `with` 语句块中执行。 当出现 `with` 语句的时候，对象的 `__enter__()` 方法被触发， 它返回的值(如果有的话)会被赋值给 `as` 声明的变量。然后，`with` 语句块里面的代码开始执行。 最后，`__exit__()` 方法被触发进行清理工作。

不管 `with` 代码块中发生什么，上面的控制流都会执行完，就算代码块中发生了异常也是一样的。 事实上，`__exit__()` 方法的三个参数包含了异常类型、异常值和追溯信息(如果有的话)。 `__exit__()` 方法能自己决定怎样利用这个异常信息，或者忽略它并返回一个None值。 如果 `__exit__()` 返回 `True` ，那么异常会被清空，就好像什么都没发生一样， `with` 语句后面的程序继续在正常执行。


#### 🎯 创建大量对象时节省内存方法
对于主要是用来当成简单的数据结构的类而言，可以通过给类添加 `__slots__` 属性来极大的减少实例所占的内存。比如：
```python
class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
```
当定义 `__slots__` 后，Python就会为实例使用一种更加紧凑的内部表示。 实例通过一个很小的固定大小的数组来构建，而不是为每个实例定义一个字典，这跟元组或列表很类似。 在 `__slots__` 中列出的属性名在内部被映射到这个数组的指定小标上。 使用slots一个不好的地方就是我们不能再给实例添加新的属性了，只能使用在 `__slots__` 中定义的那些属性名。

关于 `__slots__` 的一个常见误区是它可以作为一个封装工具来防止用户给实例增加新的属性。 尽管使用slots可以达到这样的目的，但是这个并不是它的初衷。 `__slots__` 更多的是用来作为一个内存优化工具。


#### 🎯 在类中封装属性名
Python不去依赖语言特性去封装数据，而是通过遵循一定的属性和方法命名规约来达到这个效果。 第一个约定是任何以单下划线`_`开头的名字都应该是内部实现。比如：
```python
class A:
    def __init__(self):
        self._internal = 0 # An internal attribute
        self.public = 1 # A public attribute

    def public_method(self):
        '''A public method
        '''
        pass

    def _internal_method(self):
        pass
```
Python并不会真的阻止别人访问内部名称。但是如果这么做肯定是不好的，可能会导致脆弱的代码。 同时还要注意到，使用下划线开头的约定同样适用于模块名和模块级别函数。

例如，如果看到某个模块名以单下划线开头(比如_socket)，那它就是内部实现。类似的，模块级别函数比如 `sys._getframe()` 在使用的时候就得加倍小心了。

还可能会遇到在类定义中使用两个下划线(__)开头的命名。比如：
```python
class B:
    def __init__(self):
        self.__private = 0

    def __private_method(self):
        pass

    def public_method(self):
        pass
        self.__private_method()
```
使用双下划线开始会导致访问名称变成其他形式。 比如，在前面的类B中，私有属性会被分别重命名为 `_B__private` 和 `_B__private_method`。

这时候可能会问这样重命名的目的是什么，答案就是继承——这种属性通过继承是无法被覆盖的。比如：
```python
class C(B):
    def __init__(self):
        super().__init__()
        self.__private = 1 # Does not override B.__private

    # Does not override B.__private_method()
    def __private_method(self):
        pass
```
这里，私有名称 `__private` 和 `__private_method` 被重命名为 `_C__private` 和 `_C__private_method` ，这个跟父类B中的名称是完全不同的。


#### 🎯 创建可管理的属性
想给某个实例 attribute 增加除访问与修改之外的其他处理逻辑，比如类型检查或合法性验证。

自定义某个属性的一种简单方法是将它定义为一个 property。 

⚠️注意：一个 property 其实是 `getter`、`setter` 和 `deleter` 方法的集合，而不是单个方法。
```python
class Person:
    def __init__(self, first_name):
        self._first_name = first_name

    # Getter function
    @property
    def first_name(self):
        return self._first_name

    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
```

上述代码中有三个相关联的方法，这三个方法的名字都必须一样。 第一个方法是一个 `getter` 函数，它使得 `first_name` 成为一个属性。 其他两个方法给 `first_name` 属性添加了 `setter` 和 `deleter` 函数。 需要强调的是只有在 `first_name` 属性被创建后， 后面的两个装饰器 `@first_name.setter` 和 `@first_name.deleter` 才能被定义。

property的一个关键特征是它看上去跟普通的attribute没什么两样， 但是访问它的时候会自动触发 `getter` 、`setter` 和 `deleter` 方法。例如：
```python
>>> a = Person('Guido')
>>> a.first_name # Calls the getter
'Guido'
>>> a.first_name = 42 # Calls the setter
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "prop.py", line 14, in first_name
        raise TypeError('Expected a string')
TypeError: Expected a string
>>> del a.first_name
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
AttributeError: can`t delete attribute
>>>
```
只有当确实需要对 attribute 执行其他额外的操作的时候才应该使用到 property，不要写没有做任何其他额外操作的property。

不要像下面这样写有大量重复代码的 property 定义：
```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Repeated property code, but for a different name (bad!)
    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._last_name = value
```
重复代码会导致臃肿、易出错和丑陋的程序。好消息是，通过使用装饰器或闭包，有很多种更好的方法来完成同样的事情。


#### 🎯 调用父类方法（MRO列表）
为了调用父类(超类)的一个方法，可以使用 `super()` 函数，比如：
```python
class A:
    def spam(self):
        print('A.spam')

class B(A):
    def spam(self):
        print('B.spam')
        super().spam()  # Call parent spam()
```
`super()` 函数的一个常见用法是在 `__init__()` 方法中确保父类被正确的初始化了：
```python
class A:
    def __init__(self):
        self.x = 0

class B(A):
    def __init__(self):
        super().__init__()
        self.y = 1
```

多继承 方法解析顺序(MRO)列表（C3算法）
```python
# class Base:
#     def __init__(self):
#         print('Base.__init__')

# class A(Base):
#     def __init__(self):
#         Base.__init__(self)
#         print('A.__init__')

# class B(Base):
#     def __init__(self):
#         Base.__init__(self)
#         print('B.__init__')

# class C(A,B):
#     def __init__(self):
#         A.__init__(self)
#         B.__init__(self)
#         print('C.__init__')


class Base:
    def __init__(self):
        print('Base.__init__')

class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')

class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')

class C(A,B):
    def __init__(self):
        super().__init__()  # Only one call to super() here
        print('C.__init__')
```
对于定义的每一个类，Python会计算出一个所谓的方法解析顺序(MRO)列表。 这个MRO列表就是一个简单的所有基类的线性顺序表。例如：
```python
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,
<class '__main__.Base'>, <class 'object'>)
>>>
```
为了实现继承，Python会在MRO列表上从左到右开始查找基类，直到找到第一个匹配这个属性的类为止。

而这个MRO列表的构造是通过一个C3线性化算法来实现的。 我们不去深究这个算法的数学原理，它实际上就是合并所有父类的MRO列表并遵循如下三条准则：

- 子类会先于父类被检查
- 多个父类会根据它们在列表中的顺序被检查
- 如果对下一个类存在两个合法的选择，选择第一个父类

`super()` 有个令人吃惊的地方是它并不一定去查找某个类在MRO中下一个直接父类，甚至可以在一个没有直接父类的类中使用它。例如，考虑如下这个类：
```python
class A:
    def spam(self):
        print('A.spam')
        super().spam()

# >>> a = A()
# >>> a.spam()
# A.spam
# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
#     File "<stdin>", line 4, in spam
# AttributeError: 'super' object has no attribute 'spam'
# >>>

>>> class B:
...     def spam(self):
...         print('B.spam')
...
>>> class C(A,B):
...     pass
...
>>> c = C()
>>> c.spam()
A.spam
B.spam
>>>
```

可以看到在类A中使用 `super().spam()` 实际上调用的是跟类A毫无关系的类B中的 `spam()` 方法。 这个用类C的MRO列表就可以完全解释清楚了：
```python
>>> C.__mro__
(<class '__main__.C'>, <class '__main__.A'>, <class '__main__.B'>,
<class 'object'>)
>>>
```
最后，在定义混入类的时候这样使用 `super()` 是很普遍的。


#### 🎯 子类中扩展property

在子类中，扩展定义在父类中的 property 的功能。
```python
class Person:
    def __init__(self, name):
        self.name = name

    # Getter function
    @property
    def name(self):
        return self._name

    # Setter function
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._name = value

    # Deleter function
    @name.deleter
    def name(self):
        raise AttributeError("Can't delete attribute")


class SubPerson(Person):
    @property
    def name(self):
        print('Getting name')
        return super().name

    @name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)
```
使用这个新类：
```python
>>> s = SubPerson('Guido')
Setting name to Guido
>>> s.name
Getting name
'Guido'
>>> s.name = 'Larry'
Setting name to Larry
>>> s.name = 42
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "example.py", line 16, in name
        raise TypeError('Expected a string')
TypeError: Expected a string
>>>
```
如果仅仅只想扩展 property 的某一个方法，那么可以像下面这样写：
```python
class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name

class SubPerson(Person):
    @Person.name.setter
    def name(self, value):
        print('Setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self, value)
```

在子类中扩展一个 property 可能会引起很多不易察觉的问题， 因为一个property其实是 `getter`、`setter` 和 `deleter` 方法的集合，而不是单个方法。 因此，扩展一个 property 的时候，需要先确定是否要重新定义所有的方法还是说只修改其中某一个。



在第一个例子中，所有的 property 方法都被重新定义。 在每一个方法中，使用了 `super()` 来调用父类的实现。



 在 `setter` 函数中使用 `super(SubPerson, SubPerson).name.__set__(self, value)` 的语句是没有错的。 为了委托给之前定义的setter方法，需要将控制权传递给之前定义的name属性的 `__set__()` 方法。 不过，获取这个方法的唯一途径是使用类变量而不是实例变量来访问它。 这也是为什么我们要使用 `super(SubPerson, SubPerson)` 的原因。



另外，如果只想重定义其中一个方法，那只使用 @property 本身是不够的。
```python
class SubPerson(Person):
    @property  # Doesn't work
    def name(self):
        print('Getting name')
        return super().name

# >>> s = SubPerson('Guido')
# Traceback (most recent call last):
#     File "<stdin>", line 1, in <module>
#     File "example.py", line 5, in __init__
#         self.name = name
# AttributeError: can't set attribute
# >>>

class SubPerson(Person):
    @Person.name.getter
    def name(self):
        print('Getting name')
        return super().name
```


#### 🎯 创建新的类或实例属性（描述器）

创建一个全新的实例属性，可以通过一个描述器类的形式来定义它的功能。下面是一个例子：
```python
# Descriptor attribute for an integer type-checked attribute
class Integer:
    def __init__(self, name):
        self.name = name

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Expected an int')
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]
```

一个描述器就是一个实现了三个核心的属性访问操作(get, set, delete)的类， 分别为 `__get__()` 、`__set__()` 和 `__delete__()` 这三个特殊的方法。 这些方法接受一个实例作为输入，之后相应的操作实例底层的字典。

为了使用一个描述器，需将这个描述器的实例作为类属性放到一个类的定义中。例如：
```python
class Point:
    x = Integer('x')
    y = Integer('y')

    def __init__(self, x, y):
        self.x = x
        self.y = y
```
这样做后，所有对描述器属性(比如x或y)的访问会被 `__get__()` 、`__set__()` 和 `__delete__()` 方法捕获到。例如：
```python
>>> p = Point(2, 3)
>>> p.x # Calls Point.x.__get__(p,Point)
2
>>> p.y = 5 # Calls Point.y.__set__(p, 5)
>>> p.x = 2.3 # Calls Point.x.__set__(p, 2.3)
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "descrip.py", line 12, in __set__
        raise TypeError('Expected an int')
TypeError: Expected an int
>>>
```
作为输入，描述器的每一个方法会接受一个操作实例。 为了实现请求操作，会相应的操作实例底层的字典(__dict__属性)。 描述器的 `self.name` 属性存储了在实例字典中被实际使用到的key。

描述器可实现大部分Python类特性中的底层魔法， 包括 `@classmethod` 、`@staticmethod` 、`@property` ，甚至是 `__slots__`特性。

通过定义一个描述器，可以在底层捕获核心的实例操作(get, set, delete)，并且可完全自定义它们的行为。 这是一个强大的工具，有了它可以实现很多高级功能，并且它也是很多高级库和框架中的重要工具之一。

描述器的一个比较困惑的地方是它只能在类级别被定义，而不能为每个实例单独定义。因此，下面的代码是无法工作的：
```python
# Does NOT work
class Point:
    def __init__(self, x, y):
        self.x = Integer('x') # No! Must be a class variable
        self.y = Integer('y')
        self.x = x
        self.y = y
```
原因是：实例字典中的属性不会触发描述器协议，描述器仅在类属性中生效。保持类的统一接口。

同时，`__get__()` 方法实现起来比看上去要复杂得多：
```python
# Descriptor attribute for an integer type-checked attribute
class Integer:

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
```
`__get__()` 看上去有点复杂的原因归结于实例变量和类变量的不同。 如果一个描述器被当做一个类变量来访问，那么 `instance`参数被设置成 None 。这种情况下，标准做法就是简单的返回这个描述器本身即可(尽管还可以添加其他的自定义操作)。例如：
```python
>>> p = Point(2,3)
>>> p.x # Calls Point.x.__get__(p, Point)
2
>>> Point.x # Calls Point.x.__get__(None, Point)
<__main__.Integer object at 0x100671890>
>>>
```

高级用法：
```python
# Descriptor for a type-checked attribute
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('Expected ' + str(self.expected_type))
        instance.__dict__[self.name] = value
    def __delete__(self, instance):
        del instance.__dict__[self.name]

# Class decorator that applies it to selected attributes
def typeassert(**kwargs):
    def decorate(cls):
        for name, expected_type in kwargs.items():
            # Attach a Typed descriptor to the class
            setattr(cls, name, Typed(name, expected_type))
        return cls
    return decorate

# Example use
@typeassert(name=str, shares=int, price=float)
class Stock:
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price
```
最后要指出的一点是，如果只是想简单的自定义某个类的单个属性访问的话就不用去写描述器了。 这种情况下使用 property 技术会更加容易。 

当程序中有很多重复代码的时候描述器就很有用了 (比如想在代码的很多地方使用描述器提供的功能或者将它作为一个函数库特性)。


#### 🎯 使用延迟计算属性
想将一个只读属性定义成一个property，并且只在访问的时候才会计算结果。 但是一旦被访问后，希望结果值被缓存起来，不用每次都去计算。

定义一个延迟属性的一种高效方法是通过使用一个描述器类，如下所示：
```python
class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius
```

下面在一个交互环境中演示它的使用：
```python
>>> c = Circle(4.0)
>>> c.radius
4.0
>>> c.area
Computing area
50.26548245743669
>>> c.area
50.26548245743669
>>> c.perimeter
Computing perimeter
25.132741228718345
>>> c.perimeter
25.132741228718345
>>>
```

很多时候，构造一个延迟计算属性的主要目的是为了提升性能。 例如，可以避免计算这些属性值，除非真的需要它们。 这里演示的方案就是用来实现这样的效果的， 只不过它是通过以非常高效的方式使用描述器的一个精妙特性来达到这种效果的。

当一个描述器被放入一个类的定义时， 每次访问属性时它的 `__get__()` 、`__set__()` 和 `__delete__()` 方法就会被触发。 不过，如果一个描述器仅仅只定义了一个 `__get__()` 方法的话，它比通常的具有更弱的绑定。 特别地，只有当被访问属性不在实例底层的字典中时 `__get__()` 方法才会被触发。

lazyproperty 类利用这一点，使用 `__get__()` 方法在实例中存储计算出来的值， 这个实例使用相同的名字作为它的property。 这样一来，结果值被存储在实例字典中并且以后就不需要再去计算这个property了。


#### 🎯 定义接口或者抽象基类
想定义一个接口或抽象类，并且通过执行类型检查来确保子类实现了某些特定的方法。

使用 abc 模块可以很轻松的定义抽象基类：
```python
from abc import ABCMeta, abstractmethod

class IStream(metaclass=ABCMeta):
    @abstractmethod
    def read(self, maxbytes=-1):
        pass

    @abstractmethod
    def write(self, data):
        pass
```

抽象类的一个特点是它不能直接被实例化，比如想像下面这样做是不行的：
```python
a = IStream() # TypeError: Can't instantiate abstract class
                # IStream with abstract methods read, write
```
抽象类的目的就是让别的类继承它并实现特定的抽象方法：
```python
class SocketStream(IStream):
    def read(self, maxbytes=-1):
        pass

    def write(self, data):
        pass
```
抽象基类的一个主要用途是在代码中检查某些类是否为特定类型，实现了特定接口：
```python
def serialize(obj, stream):
    if not isinstance(stream, IStream):
        raise TypeError('Expected an IStream')
    pass
```

#### 🎯 属性的代理访问

如果有大量的方法需要代理， 那么使用 `__getattr__()` 方法
```python
class B2:
    """使用__getattr__的代理，代理方法比较多时候"""

    def __init__(self):
        self._a = A()

    def bar(self):
        pass

    # Expose all of the methods defined on class A
    def __getattr__(self, name):
        """这个方法在访问的attribute不存在的时候被调用
        the __getattr__() method is actually a fallback method
        that only gets called when an attribute is not found"""
        return getattr(self._a, name)
```
`__getattr__` 方法是在访问attribute不存在的时候被调用


#### 🎯 在类中定义多个构造器

为了实现多个构造器，需要使用到类方法。例如：
```python
import time

class Date:
    """方法一：使用类方法"""
    # Primary constructor
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)
```
直接调用类方法即可，下面是使用示例：
```python
a = Date(2012, 12, 21) # Primary
b = Date.today() # Alternate
```
类方法的一个主要用途就是定义多个构造器。它接受一个 class 作为第一个参数(cls)。 应该注意到了这个类被用来创建并返回最终的实例。


#### 🎯 创建不调用init方法的实例
想创建一个实例，但是希望绕过执行 `__init__()` 方法。可以通过 `__new__()` 方法创建一个未初始化的实例。例如考虑如下这个类：
```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

>>> d = Date.__new__(Date)
>>> d
<__main__.Date object at 0x1006716d0>
>>> d.year
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
AttributeError: 'Date' object has no attribute 'year'
>>>
```

结果可以看到，这个Date实例的属性year还不存在，所以需要手动初始化：
```python
>>> data = {'year':2012, 'month':8, 'day':29}
>>> for key, value in data.items():
...     setattr(d, key, value)
...
>>> d.year
2012
>>> d.month
8
>>>
```


#### 🎯 利用Mixins扩展类功能
有很多有用的方法，想使用它们来扩展其他类的功能。但是这些类并没有任何继承的关系。 因此不能简单的将这些方法放入一个基类，然后被其他类继承。

通常当想自定义类的时候会碰上这些问题。可能是某个库提供了一些基础类， 可以利用它们来构造自己的类。

假设想扩展映射对象，给它们添加日志、唯一性设置、类型检查等等功能。下面是一些混入类：
```python
class LoggedMappingMixin:
    """
    Add logging to get/set/delete operations for debugging.
    """
    __slots__ = ()  # 混入类都没有实例变量，因为直接实例化混入类没有任何意义

    def __getitem__(self, key):
        print('Getting ' + str(key))
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        print('Setting {} = {!r}'.format(key, value))
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        print('Deleting ' + str(key))
        return super().__delitem__(key)


class SetOnceMappingMixin:
    '''
    Only allow a key to be set once.
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(str(key) + ' already set')
        return super().__setitem__(key, value)


class StringKeysMappingMixin:
    '''
    Restrict keys to strings only
    '''
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError('keys must be strings')
        return super().__setitem__(key, value)
```

这些类单独使用起来没有任何意义，事实上如果去实例化任何一个类，除了产生异常外没任何作用。 它们是用来通过多继承来和其他映射对象混入使用的。例如：
```python
class LoggedDict(LoggedMappingMixin, dict):
    pass

d = LoggedDict()
d['x'] = 23
print(d['x'])
del d['x']

from collections import defaultdict

class SetOnceDefaultDict(SetOnceMappingMixin, defaultdict):
    pass


d = SetOnceDefaultDict(list)
d['x'].append(2)
d['x'].append(3)
# d['x'] = 23  # KeyError: 'x already set'
```

这个例子中，可以看到混入类跟其他已存在的类(比如dict、defaultdict和OrderedDict)结合起来使用，一个接一个。 结合后就能发挥正常功效了。

对于混入类，有几点需要记住。首先是，混入类不能直接被实例化使用。 其次，混入类没有自己的状态信息，也就是说它们并没有定义 `__init__()` 方法，并且没有实例属性。 这也是为什么我们在上面明确定义了 `__slots__ = ()`。


#### 🎯 实现状态对象或者状态机
想实现一个状态机或者是在不同状态下执行操作的对象，但是又不想在代码中出现太多的条件判断语句。

在很多程序中，有些对象会根据状态的不同来执行不同的操作。比如考虑如下的一个连接对象：
```python
class Connection:
    """普通方案，好多个判断语句，效率低下~~"""

    def __init__(self):
        self.state = 'CLOSED'

    def read(self):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('reading')

    def write(self, data):
        if self.state != 'OPEN':
            raise RuntimeError('Not open')
        print('writing')

    def open(self):
        if self.state == 'OPEN':
            raise RuntimeError('Already open')
        self.state = 'OPEN'

    def close(self):
        if self.state == 'CLOSED':
            raise RuntimeError('Already closed')
        self.state = 'CLOSED'
```

这样写有很多缺点，首先是代码太复杂了，好多的条件判断。其次是执行效率变低， 因为一些常见的操作比如read()、write()每次执行前都需要执行检查。

一个更好的办法是为每个状态定义一个对象：
```python
class Connection:
    """新方案——对每个状态定义一个类"""

    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate
        # Delegate to the state class

    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)


# Connection state base class
class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn, data):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()


# Implementation of different states
class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def write(conn, data):
        raise RuntimeError('Not open')

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError('Already closed')


class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn, data):
        print('writing')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already open')

    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)
```

使用示例：
```python
>>> c = Connection()
>>> c._state
<class '__main__.ClosedConnectionState'>
>>> c.read()
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "example.py", line 10, in read
        return self._state.read(self)
    File "example.py", line 43, in read
        raise RuntimeError('Not open')
RuntimeError: Not open
>>> c.open()
>>> c._state
<class '__main__.OpenConnectionState'>
>>> c.read()
reading
>>> c.write('hello')
writing
>>> c.close()
>>> c._state
<class '__main__.ClosedConnectionState'>
>>>
```

#### 🎯 实现访问者模式
要处理由大量不同类型的对象组成的复杂数据结构，每一个对象都需要进行不同的处理。 比如，遍历一个树形结构，然后根据每个节点的相应状态执行不同的操作。

这里遇到的问题在编程领域中是很普遍的，有时候会构建一个由大量不同对象组成的数据结构。 假设要写一个表示数学表达式的程序，那么可能需要定义如下的类：
```python
class Node:
    pass

class UnaryOperator(Node):
    def __init__(self, operand):
        self.operand = operand

class BinaryOperator(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Number(Node):
    def __init__(self, value):
        self.value = value


class Add(BinaryOperator):
    pass

class Sub(BinaryOperator):
    pass

class Mul(BinaryOperator):
    pass

class Div(BinaryOperator):
    pass

class Negate(UnaryOperator):
    pass
```

然后利用这些类构建嵌套数据结构，如下所示：
```python
# Representation of 1 + 2 * (3 - 4) / 5
t1 = Sub(Number(3), Number(4))
t2 = Mul(Number(2), t1)
t3 = Div(t2, Number(5))
t4 = Add(Number(1), t3)
```

这样做的问题是对于每个表达式，每次都要重新定义一遍，也就是说每次定义一个新的表达式时，都必须重新从头开始构建这些子表达式。这意味着必须手动创建所有的子节点，并且一旦改变某部分的结构（例如，改变操作符或操作数），可能需要重新组织整个表达式树。

有没有一种更通用的方式让它支持所有的数字和操作符呢。 这里我们使用访问者模式可以达到这样的目的：
```python
class NodeVisitor:
    def visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))
```

为了使用这个类，可以定义一个类继承它并且实现各种 `visit_Name()` 方法，其中Name是node类型。 例如，如果想求表达式的值，可以这样写：
```python
class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        return self.visit(node.left) + self.visit(node.right)

    def visit_Sub(self, node):
        return self.visit(node.left) - self.visit(node.right)

    def visit_Mul(self, node):
        return self.visit(node.left) * self.visit(node.right)

    def visit_Div(self, node):
        return self.visit(node.left) / self.visit(node.right)

    def visit_Negate(self, node):
        return -node.operand


>>> e = Evaluator()
>>> e.visit(t4)
0.6
>>>
```

⚠️使用访问者模式遍历一个很深的嵌套树形数据结构，并且因为超过嵌套层级限制而失败。 想消除递归，并同时保持访问者编程模式。

通过巧妙的使用生成器可以在树遍历或搜索算法中消除递归。 在8.21小节中，我们给出了一个访问者类。 下面我们利用一个栈和生成器重新实现这个类：
```python
import types

class Node:
    pass

class NodeVisitor:
    def visit(self, node):
        stack = [node]
        last_result = None
        while stack:
            try:
                last = stack[-1]
                if isinstance(last, types.GeneratorType):
                    stack.append(last.send(last_result))
                    last_result = None
                elif isinstance(last, Node):
                    stack.append(self._visit(stack.pop()))
                else:
                    last_result = stack.pop()
            except StopIteration:
                stack.pop()

        return last_result

    def _visit(self, node):
        methname = 'visit_' + type(node).__name__
        meth = getattr(self, methname, None)
        if meth is None:
            meth = self.generic_visit
        return meth(node)

    def generic_visit(self, node):
        raise RuntimeError('No {} method'.format('visit_' + type(node).__name__))
```

现在我们稍微修改下上面的Evaluator：
```python
class Evaluator(NodeVisitor):
    def visit_Number(self, node):
        return node.value

    def visit_Add(self, node):
        yield (yield node.left) + (yield node.right)

    def visit_Sub(self, node):
        yield (yield node.left) - (yield node.right)

    def visit_Mul(self, node):
        yield (yield node.left) * (yield node.right)

    def visit_Div(self, node):
        yield (yield node.left) / (yield node.right)

    def visit_Negate(self, node):


>>> a = Number(0)
>>> for n in range(1,100000):
...     a = Add(a, Number(n))
...
>>> e = Evaluator()
>>> e.visit(a)
4999950000
>>>
```
生成器和协程在程序控制流方面的强大功能。 避免递归的一个通常方法是使用一个栈或队列的数据结构。 例如，深度优先的遍历算法，第一次碰到一个节点时将其压入栈中，处理完后弹出栈。`visit()` 方法的核心思路就是这样。



### 🍞 元编程

#### 🎯 装饰器

🧩 一个装饰器就是一个函数，它接受一个函数作为参数并返回一个新的函数。如果想使用额外的代码（比如日志、计时等）包装一个函数，可以定义一个装饰器函数，例如：
```python
import time
from functools import wraps

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper


>>> @timethis
... def countdown(n):
...     '''
...     Counts down
...     '''
...     while n > 0:
...         n -= 1
...
>>> countdown(100000)
countdown 0.008917808532714844
>>> countdown(10000000)
countdown 0.87188299392912
>>>
```

🧩 创建装饰器时保留函数元信息。应该使用 functools 库中的 @wraps 装饰器来注解底层包装函数。例如：
```python
import time
from functools import wraps
def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper


>>> @timethis
... def countdown(n):
...     '''
...     Counts down
...     '''
...     while n > 0:
...         n -= 1
...
>>> countdown(100000)
countdown 0.008917808532714844
>>> countdown.__name__
'countdown'
>>> countdown.__doc__
'\n\tCounts down\n\t'
>>> countdown.__annotations__
{'n': <class 'int'>}
>>>
```

🧩 当需要解除一个装饰器时。可以通过访问 `__wrapped__` 属性来访问原始函数，前提是在包装器中正确使用了 `@wraps` 或者直接设置了 `__wrapped__` 属性的情况。：
```python
>>> @somedecorator
>>> def add(x, y):
...     return x + y
...
>>> orig_add = add.__wrapped__
>>> orig_add(3, 4)
7
>>>
```

🧩 定义一个带参数的装饰器。假设想写一个装饰器，给函数添加日志功能，同时允许用户指定日志的级别和其他的选项。下面是这个装饰器的定义和使用示例：
```python
from functools import wraps
import logging

def logged(level, name=None, message=None):
    """
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    """
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate

# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')
```
初看起来，这种实现看上去很复杂，但是核心思想很简单。 最外层的函数 `logged()` 接受参数并将它们作用在内部的装饰器函数上面。 内层的函数 `decorate()` 接受一个函数作为参数，然后在函数上面放置一个包装器。 这里的关键点是包装器是可以使用传递给 `logged()` 的参数的。

🧩 可自定义属性的装饰器。写一个装饰器来包装一个函数，并且允许用户提供参数在运行时控制装饰器行为。引入一个访问函数，使用 `nonlocal` 来修改内部变量。 然后这个访问函数被作为一个属性赋值给包装函数。
```python
from functools import wraps, partial
import logging
# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    '''
    Add logging to a function. level is the logging
    level, name is the logger name, and message is the
    log message. If name and message aren't specified,
    they default to the function's module and name.
    '''
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Attach setter functions
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper

    return decorate

# Example use
@logged(logging.DEBUG)
def add(x, y):
    return x + y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')


>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> add(2, 3)
DEBUG:__main__:add
5
>>> # Change the log message
>>> add.set_message('Add called')
>>> add(2, 3)
DEBUG:__main__:Add called
5
>>> # Change the log level
>>> add.set_level(logging.WARNING)
>>> add(2, 3)
WARNING:__main__:Add called
5
>>>
```
关键点在于访问函数(如 `set_message()` 和 `set_level()` )，它们被作为属性赋给包装器。 每个访问函数允许使用 `nonlocal`来修改函数内部的变量。


🧩 带可选参数的装饰器。一个装饰器，既可以不传参数给它，比如 `@decorator` ， 也可以传递可选参数给它，比如 `@decorator(x,y,z)` 。
```python
def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper

# Example use
@logged
def add(x, y):
    return x + y

@logged(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')

print(add(2, 3))
spam()
```
为了理解代码是如何工作的，需要非常熟悉装饰器是如何作用到函数上以及它们的调用规则。 对于一个像下面这样的简单装饰器：
```python
# Example use
@logged
def add(x, y):
    return x + y
```

这个调用序列跟下面等价：
```python
def add(x, y):
    return x + y

add = logged(add)
```

这时候，被装饰函数会被当做第一个参数直接传递给 `logged` 装饰器。 因此，`logged()` 中的第一个参数就是被包装函数本身。所有其他参数都必须有默认值。

而对于一个下面这样有参数的装饰器：
```python
@logged(level=logging.CRITICAL, name='example')
def spam():
    print('Spam!')
```

调用序列跟下面等价：
```python
def spam():
    print('Spam!')
spam = logged(level=logging.CRITICAL, name='example')(spam)
```

初始调用` logged()` 函数时，被包装函数并没有传递进来。 因此在装饰器内，它必须是可选的。这个反过来会迫使其他参数必须使用关键字来指定。 并且，当这些参数被传递进来后，装饰器要返回一个接受一个函数参数并包装它的函数。 为了这样做，我们使用了一个技巧，就是利用 `functools.partial` 。 它会返回一个未完全初始化的自身，除了被包装函数外其他参数都已经确定下来了。


#### 🎯 利用装饰器强制函数上的类型检查
作为某种编程规约，想在对函数参数进行强制类型检查。下面是使用装饰器技术来实现 `@typeassert` ：
```python
from inspect import signature
from functools import wraps

def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                            )
            return func(*args, **kwargs)
        return wrapper
    return decorate


>>> @typeassert(int, int)
... def add(x, y):
...     return x + y
...
>>>
>>> add(2, 3)
5
>>> add(2, 'hello')
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "contract.py", line 33, in wrapper
TypeError: Argument y must be <class 'int'>
>>>

# 可以看出这个装饰器非常灵活，既可以指定所有参数类型，也可以只指定部分。 并且可以通过位置或关键字来指定参数类型。
>>> @typeassert(int, z=int)
... def spam(x, y, z=42):
...     print(x, y, z)
...
>>> spam(1, 2, 3)
1 2 3
>>> spam(1, 'hello', 3)
1 hello 3
>>> spam(1, 'hello', 'world')
Traceback (most recent call last):
File "<stdin>", line 1, in <module>
File "contract.py", line 33, in wrapper
TypeError: Argument z must be <class 'int'>
>>>
```


#### 🎯 将装饰器定义为类的一部分

想在类中定义装饰器，并将其作用在其他函数或方法上。在类里面定义装饰器很简单，但是首先要确认它的使用方式。比如到底是作为一个实例方法还是类方法。 下面我们用例子来阐述它们的不同：
```python
from functools import wraps

class A:
    # Decorator as an instance method
    def decorator1(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 1')
            return func(*args, **kwargs)
        return wrapper

    # Decorator as a class method
    @classmethod
    def decorator2(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('Decorator 2')
            return func(*args, **kwargs)
        return wrapper


# 仔细观察可以发现一个是实例调用，一个是类调用。
# As an instance method
a = A()
@a.decorator1
def spam():
    pass
# As a class method
@A.decorator2
def grok():
    pass
```

#### 🎯 将装饰器定义为类
想使用一个装饰器去包装函数，但是希望返回一个可调用的实例。 需要让装饰器可以同时工作在类定义的内部和外部。

为了将装饰器定义成一个实例，需要确保它实现了 `__call__()` 和 `__get__()` 方法。 例如，下面的代码定义了一个类，它在其他函数上放置一个简单的记录层：
```python
import types
from functools import wraps

class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)
```

可以将它当做一个普通的装饰器来使用，在类里面或外面都可以：
```python
@Profiled
def add(x, y):
    return x + y

class Spam:
    @Profiled
    def bar(self, x):
        print(self, x)


>>> add(2, 3)
5
>>> add(4, 5)
9
>>> add.ncalls
2
>>> s = Spam()
>>> s.bar(1)
<__main__.Spam object at 0x10069e9d0> 1
>>> s.bar(2)
<__main__.Spam object at 0x10069e9d0> 2
>>> s.bar(3)
<__main__.Spam object at 0x10069e9d0> 3
>>> Spam.bar.ncalls
3
```
`__get__()` 方法是为了确保绑定方法对象能被正确的创建。 `type.MethodType()` 手动创建一个绑定方法来使用。只有当实例被使用的时候绑定方法才会被创建。 如果这个方法是在类上面来访问， 那么 `__get__()` 中的 instance 参数会被设置成 None 并直接返回 Profiled 实例本身。 这样的话我们就可以提取它的 ncalls 属性了。

如果想避免一些混乱，也可以考虑另外一个使用闭包和 nonlocal 变量实现的装饰器。例如：
```python
import types
from functools import wraps

def profiled(func):
    ncalls = 0
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal ncalls
        ncalls += 1
        return func(*args, **kwargs)
    wrapper.ncalls = lambda: ncalls
    return wrapper

# Example
@profiled
def add(x, y):
    return x + y
```

#### 🎯 为类方法和静态方法提供装饰器
给类方法或静态方法提供装饰器是很简单的，不过要确保装饰器在 `@classmethod` 或 `@staticmethod` 之前。例如：
```python
import time
from functools import wraps

# A simple decorator
def timethis(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        r = func(*args, **kwargs)
        end = time.time()
        print(end-start)
        return r
    return wrapper

# Class illustrating application of the decorator to different kinds of methods
class Spam:
    @timethis
    def instance_method(self, n):
        print(self, n)
        while n > 0:
            n -= 1

    @classmethod
    @timethis
    def class_method(cls, n):
        print(cls, n)
        while n > 0:
            n -= 1

    @staticmethod
    @timethis
    def static_method(n):
        print(n)
        while n > 0:
            n -= 1
```

#### 🎯 装饰器为被包装函数增加参数
在装饰器中给被包装函数增加额外的参数，但是不能影响这个函数现有的调用规则。可以使用关键字参数来给被包装函数增加额外参数。考虑下面的装饰器：
```python
from functools import wraps

def optional_debug(func):
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    return wrapper


>>> @optional_debug
... def spam(a,b,c):
...     print(a,b,c)
...
>>> spam(1,2,3)
1 2 3
>>> spam(1,2,3, debug=True)
Calling spam
1 2 3
>>>
```

通过装饰器来给被包装函数增加参数的做法并不常见。 尽管如此，有时候它可以避免一些重复代码。例如，如果有下面这样的代码：
```python
def a(x, debug=False):
    if debug:
        print('Calling a')

def b(x, y, z, debug=False):
    if debug:
        print('Calling b')

def c(x, y, debug=False):
    if debug:
        print('Calling c')
        
# 重构
from functools import wraps
import inspect

def optional_debug(func):
    if 'debug' in inspect.getargspec(func).args:
        raise TypeError('debug argument already defined')

    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

@optional_debug
def a(x):
    pass

@optional_debug
def b(x, y, z):
    pass

@optional_debug
def c(x, y):
    pass
```

这种实现方案之所以行得通，在于强制关键字参数很容易被添加到接受 `*args` 和 `**kwargs` 参数的函数中。 通过使用强制关键字参数，它被作为一个特殊情况被挑选出来， 并且接下来仅仅使用剩余的位置和关键字参数去调用这个函数时，这个特殊参数会被排除在外。 也就是说，它并不会被纳入到 `**kwargs` 中去。

还有一个难点就是如何去处理被添加的参数与被包装函数参数直接的名字冲突。 例如，如果装饰器 `@optional_debug` 作用在一个已经拥有一个 `debug` 参数的函数上时会有问题。 这里我们增加了一步名字检查。

⚠️最后关于被包装函数的函数签名如何重新绑定为正确的，参考内置的 `inspect` 模块。


#### 🎯 使用装饰器扩充类的功能
通过反省或者重写类定义的某部分来修改它的行为，但是又不希望使用继承或元类的方式。这种情况可能是类装饰器最好的使用场景了。例如，下面是一个重写了特殊方法 `__getattribute__` 的类装饰器， 可以打印日志：
```python
def log_getattribute(cls):
    # Get the original implementation
    orig_getattribute = cls.__getattribute__

    # Make a new definition
    def new_getattribute(self, name):
        print('getting:', name)
        return orig_getattribute(self, name)

    # Attach to the class and return
    cls.__getattribute__ = new_getattribute
    return cls

# Example use
@log_getattribute
class A:
    def __init__(self,x):
        self.x = x
    def spam(self):
        pass


>>> a = A(42)
>>> a.x
getting: x
42
>>> a.spam()
getting: spam
>>>
```

类装饰器通常可以作为其他高级技术比如混入或元类的一种非常简洁的替代方案。 比如，上面示例中的另外一种实现使用到继承：
```python
class LoggedGetattribute:
    def __getattribute__(self, name):
        print('getting:', name)
        return super().__getattribute__(name)

# Example:
class A(LoggedGetattribute):
    def __init__(self,x):
        self.x = x
    def spam(self):
        pass
```
这种方案也行得通，但是为了去理解它，就必须知道方法调用顺序、`super()` 以及其它8.7小节介绍的继承知识。 某种程度上来讲，类装饰器方案就显得更加直观，并且它不会引入新的继承体系。它的运行速度也更快一些， 因为他并不依赖 `super()` 函数。


#### 🎯 使用元类控制实例的创建

通过改变实例创建方式来实现单例、缓存或其他类似的特性。利用元类实现多种实例创建模式通常要比不使用元类的方式优雅得多。

Python程序员都知道，如果定义了一个类，就能像函数一样的调用它来创建实例，例如：
```python
class Spam:
    def __init__(self, name):
        self.name = name

a = Spam('Guido')
b = Spam('Diana')
```

如果想自定义这个步骤，可以定义一个元类并自己实现 `__call__()` 方法。

为了演示，假设不想任何人创建这个类的实例：
```python
class NoInstances(type):
    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")

# Example
class Spam(metaclass=NoInstances):
    @staticmethod
    def grok(x):
        print('Spam.grok')


# 这样的话，用户只能调用这个类的静态方法，而不能使用通常的方法来创建它的实例。例如：
>>> Spam.grok(42)
Spam.grok
>>> s = Spam()
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "example1.py", line 7, in __call__
        raise TypeError("Can't instantiate directly")
TypeError: Can't instantiate directly
>>>
```

🧩 实现单例模式（只能创建唯一实例的类），实现起来也很简单：
```python
class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance

# Example
class Spam(metaclass=Singleton):
    def __init__(self):
        print('Creating Spam')


# Usage
>>> a = Spam()
Creating Spam
>>> b = Spam()
>>> a is b
True
>>> c = Spam()
>>> a is c
True
>>>
```

🧩 实现缓存实例。下面我们可以通过元类来实现：
```python
import weakref

class Cached(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = weakref.WeakValueDictionary()

    def __call__(self, *args):
        if args in self.__cache:
            return self.__cache[args]
        else:
            obj = super().__call__(*args)
            self.__cache[args] = obj
            return obj

# Example
class Spam(metaclass=Cached):
    def __init__(self, name):
        print('Creating Spam({!r})'.format(name))
        self.name = name

# Usage
>>> a = Spam('Guido')
Creating Spam('Guido')
>>> b = Spam('Diana')
Creating Spam('Diana')
>>> c = Spam('Guido') # Cached
>>> a is b
False
>>> a is c # Cached value returned
True
>>>
```


#### 🎯 使用元类在类上强制使用编程规约

程序包含一个很大的类继承体系，希望强制执行某些编程规约（或者代码诊断）来帮助程序员保持清醒。

如果想监控类的定义，通常可以通过定义一个元类。一个基本元类通常是继承自 type 并重定义它的 `__new__()` 方法 或者是 `__init__()` 方法。比如：
```python
class MyMeta(type):
    def __new__(self, clsname, bases, clsdict):
        # clsname is name of class being defined
        # bases is tuple of base classes
        # clsdict is class dictionary
        return super().__new__(cls, clsname, bases, clsdict)

class MyMeta(type):
    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        # clsname is name of class being defined
        # bases is tuple of base classes
        # clsdict is class dictionary
```

为了使用这个元类，通常要将它放到到一个顶级父类定义中，然后其他的类继承这个顶级父类。例如：
```python
class Root(metaclass=MyMeta):
    pass

class A(Root):
    pass

class B(Root):
    pass
```

元类的一个关键特点是它允许在定义的时候检查类的内容。在重新定义 `__init__()` 方法中， 可以很轻松的检查类字典、父类等等。并且，一旦某个元类被指定给了某个类，那么就会被继承到所有子类中去。 因此，一个框架的构建者就能在大型的继承体系中通过给一个顶级父类指定一个元类去捕获所有下面子类的定义。

作为一个具体的应用例子，下面定义了一个元类，它会拒绝任何有混合大小写名字作为方法的类定义：
```python
class NoMixedCaseMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        for name in clsdict:
            if name.lower() != name:
                raise TypeError('Bad attribute name: ' + name)
        return super().__new__(cls, clsname, bases, clsdict)

class Root(metaclass=NoMixedCaseMeta):
    pass

class A(Root):
    def foo_bar(self): # Ok
        pass

class B(Root):
    def fooBar(self): # TypeError
        pass
```

作为更高级和实用的例子，下面有一个元类，它用来检测重载方法，确保它的调用参数跟父类中原始方法有着相同的参数签名。
```python
from inspect import signature
import logging

class MatchSignaturesMeta(type):

    def __init__(self, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        sup = super(self, self)
        for name, value in clsdict.items():
            if name.startswith('_') or not callable(value):
                continue
            # Get the previous definition (if any) and compare the signatures
            prev_dfn = getattr(sup,name,None)
            if prev_dfn:
                prev_sig = signature(prev_dfn)
                val_sig = signature(value)
                if prev_sig != val_sig:
                    logging.warning('Signature mismatch in %s. %s != %s',
                                    value.__qualname__, prev_sig, val_sig)

# Example
class Root(metaclass=MatchSignaturesMeta):
    pass

class A(Root):
    def foo(self, x, y):
        pass

    def spam(self, x, *, z):
        pass

# Class with redefined methods, but slightly different signatures
class B(A):
    def foo(self, a, b):
        pass

    def spam(self,x,z):
        pass
```

如果运行这段代码，就会得到下面这样的输出结果：
```python
WARNING:root:Signature mismatch in B.spam. (self, x, *, z) != (self, x, z)
WARNING:root:Signature mismatch in B.foo. (self, x, y) != (self, a, b)
```

这种警告信息对于捕获一些微妙的程序bug是很有用的。例如，如果某个代码依赖于传递给方法的关键字参数， 那么当子类改变参数名字的时候就会调用出错。

在大型面向对象的程序中，通常将类的定义放在元类中控制是很有用的。 元类可以监控类的定义，警告编程人员某些没有注意到的可能出现的问题。

有人可能会说，像这样的错误可以通过程序分析工具或IDE去做会更好些。诚然，这些工具是很有用。 但是，如果在构建一个框架或函数库供其他人使用，那么没办法去控制使用者要使用什么工具。 因此，对于这种类型的程序，如果可以在元类中做检测或许可以带来更好的用户体验。

在元类中选择重新定义 `__new__()` 方法还是 `__init__()` 方法取决于想怎样使用结果类。 `__new__()` 方法在类创建之前被调用，通常用于通过某种方式（比如通过改变类字典的内容）修改类的定义。 而 `__init__()` 方法是在类被创建之后被调用，当需要完整构建类对象的时候会很有用。 在最后一个例子中，这是必要的，因为它使用了 `super()` 函数来搜索之前的定义。 它只能在类的实例被创建之后，并且相应的方法解析顺序也已经被设置好了。

最后一个例子还演示了Python的函数签名对象的使用。 实际上，元类将每个可调用定义放在一个类中，搜索前一个定义（如果有的话）， 然后通过使用 `inspect.signature()` 来简单的比较它们的调用签名。

最后一点，代码中有一行使用了 `super(self, self)` 并不是排版错误。 当使用元类的时候，我们要时刻记住一点就是 `self` 实际上是一个类对象。 因此，这条语句其实就是用来寻找位于继承体系中构建 `self` 父类的定义。


#### 🎯 在类定义的时候初始化类的成员
在类被定义的时候就初始化一部分类的成员，而不是要等到实例被创建后，在类定义时就执行初始化或设置操作是元类的一个典型应用场景。

本质上讲，一个元类会在定义时被触发， 这时候可以执行一些额外的操作。

下面是一个例子，利用这个思路来创建类似于 `collections` 模块中的命名元组的类：
```python
import operator

class StructTupleMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, name in enumerate(cls._fields):
            setattr(cls, name, property(operator.itemgetter(n)))

class StructTuple(tuple, metaclass=StructTupleMeta):
    _fields = []
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required'.format(len(cls._fields)))
        return super().__new__(cls,args)


class Stock(StructTuple):
    _fields = ['name', 'shares', 'price']

class Point(StructTuple):
    _fields = ['x', 'y']


>>> s = Stock('ACME', 50, 91.1)
>>> s
('ACME', 50, 91.1)
>>> s[0]
'ACME'
>>> s.name
'ACME'
>>> s.shares * s.price
4555.0
>>> s.shares = 23
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
>>>
```

类 `StructTupleMeta` 获取到类属性 `_fields` 中的属性名字列表， 然后将它们转换成相应的可访问特定元组槽的方法。函数 `operator.itemgetter()` 创建一个访问器函数， 然后 `property()` 函数将其转换成一个属性。

这里最难懂的部分是知道不同的初始化步骤是什么时候发生的。 `StructTupleMeta` 中的 `__init__()` 方法只在每个类被定义时被调用一次。 `cls` 参数就是那个被定义的类。实际上，上述代码使用了 `_fields` 类变量来保存新的被定义的类， 然后给它再添加一点新的东西。

`StructTuple` 类作为一个普通的基类，供其他使用者来继承。 这个类中的 `__new__()` 方法用来构造新的实例。 这里使用 `__new__()` 并不是很常见，主要是因为我们要修改元组的调用签名， 使得我们可以像普通的实例调用那样创建实例。就像下面这样：
```python
s = Stock('ACME', 50, 91.1) # OK
s = Stock(('ACME', 50, 91.1)) # Error
```

跟 `__init__()` 不同的是，`__new__()` 方法在实例被创建之前被触发。 由于元组是不可修改的，所以一旦它们被创建了就不可能对它做任何改变。而 `__init__()` 会在实例创建的最后被触发， 这样的话我们就可以做我们想做的了。这也是为什么 `__new__()` 方法已经被定义了。

这部分需要深入思考Python类是如何被定义的，实例是如何被创建的， 还有就是元类和类的各个不同的方法究竟在什么时候被调用。



### 🍞 模块与包

🧩 构建一个模块的层级包。

封装成包是很简单的。在文件系统上组织代码，并确保每个目录都定义了一个 `__init__.py` 文件。 例如：
```python
graphics/
    __init__.py
    primitive/
        __init__.py
        line.py
        fill.py
        text.py
    formats/
        __init__.py
        png.py
        jpg.py
```
一旦做到了这一点，应该能够执行各种 `import` 语句，如下：
```pyton
import graphics.primitive.line
from graphics.primitive import line
import graphics.formats.jpg as jpg
```

🧩 控制模块被全部导入的内容。
当使用`from module import *` 语句时，希望对从模块或包导出的符号进行精确控制。在模块中定义一个变量 `__all__` 来明确地列出需要导出的内容。
```pyton
# somemodule.py
def spam():
    pass

def grok():
    pass

blah = 42
# Only export 'spam' and 'grok'
__all__ = ['spam', 'grok']
```
尽管强烈反对使用 `from module import *`, 但是在定义了大量变量名的模块中频繁使用。 如果不做任何事, 这样的导入将会导入所有不以下划线开头的。 另一方面,如果定义了 `__all__` , 那么只有被列举出的东西会被导出。

如果将 `__all__` 定义成一个空列表, 没有东西将被导入。 如果 `__all__` 包含未定义的名字, 在导入时引起`AttributeError`。

🧩 重新加载模块。
想重新加载已经加载的模块，因为源码进行了修改。使用`imp.reload()`来重新加载先前加载的模块。举个例子：
```python
>>> import spam
>>> import imp
>>> imp.reload(spam)
<module 'spam' from './spam.py'>
>>>
```
重新加载模块在开发和调试过程中常常很有用。但在生产环境中的代码使用会不安全，因为它并不总是像您期望的那样工作。

`reload()`擦除了模块底层字典的内容，并通过重新执行模块的源代码来刷新它。模块对象本身的身份保持不变。因此，该操作在程序中所有已经被导入了的地方更新了模块。

