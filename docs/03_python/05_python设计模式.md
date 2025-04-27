# 

| 模式名     | 简要说明                   |
| ---------- | -------------------------- |
| 单例模式   | 保证一个类只有一个实例     |
| 工厂模式   | 用工厂函数根据参数创建对象 |
| 策略模式   | 可切换算法或行为           |
| 观察者模式 | 一对多，发布-订阅模型      |
| 装饰器模式 | 动态增强功能（函数包装）   |
| 适配器模式 | 旧接口兼容新系统           |
| 代理模式   | 控制访问（权限、懒加载等） |


### 单例模式 Singleton
```python
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print("a is b:", a is b)  # True，同一个实例
```

### 工厂模式 Factory
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪"

class Cat(Animal):
    def speak(self):
        return "喵喵"

def animal_factory(kind):
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()

animal = animal_factory("dog")
print("Dog says:", animal.speak())  # 汪汪
```

### 策略模式 Strategy
```python
class StrategyA:
    def execute(self):
        return "策略 A"

class StrategyB:
    def execute(self):
        return "策略 B"

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def run(self):
        return self.strategy.execute()

ctx = Context(StrategyA())
print("使用策略 A:", ctx.run())  # 策略 A
ctx.strategy = StrategyB()
print("使用策略 B:", ctx.run())  # 策略 B
```

### 观察者模式 Observer
```python
class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, fn):
        self.subscribers.append(fn)

    def notify(self, msg):
        for fn in self.subscribers:
            fn(msg)

def listener(msg):
    print("收到消息:", msg)

pub = Publisher()
pub.subscribe(listener)
pub.notify("更新发布啦")  # 收到消息: 更新发布啦
```

### 装饰器模式 Decorator
```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@logger
def add(x, y):
    return x + y

print("add(3, 4):", add(3, 4))  
# 调用函数: add
# 7
```

### 适配器模式 Adapter
```python
class OldSystem:
    def specific_request(self):
        return "旧系统返回的数据"

class Adapter:
    def __init__(self, old_system):
        self.old = old_system

    def request(self):
        return self.old.specific_request()

old = OldSystem()
adapter = Adapter(old)
print("适配器调用:", adapter.request())  # 旧系统返回的数据
```

### 代理模式 Proxy
```python
class RealSubject:
    def request(self):
        return "真实请求结果"

class Proxy:
    def __init__(self):
        self.real = RealSubject()

    def request(self):
        print("代理检查权限...")
        return self.real.request()

proxy = Proxy()
print("代理调用:", proxy.request())  
# 代理检查权限...
# 真实请求结果
```