"""
第一阶段知识回顾与测试
涵盖：对象模型、魔术方法、OOP、元编程
"""

print("=" * 70)
print("第一阶段知识回顾测试")
print("=" * 70)

# ==================== 测试 1: 魔术方法理解 ====================

print("\n【测试 1】魔术方法理解")
print("-" * 70)

class Vector:
    """二维向量类 - 测试魔术方法"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        """字符串表示"""
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other):
        """向量加法"""
        if not isinstance(other, Vector):
            raise TypeError("只能与 Vector 相加")
        return Vector(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        """标量乘法"""
        return Vector(self.x * scalar, self.y * scalar)
    
    def __eq__(self, other):
        """相等判断"""
        if not isinstance(other, Vector):
            return False
        return self.x == other.x and self.y == other.y
    
    def __len__(self):
        """向量长度（模）"""
        return int((self.x ** 2 + self.y ** 2) ** 0.5)
    
    def __bool__(self):
        """布尔值（非零向量为 True）"""
        return self.x != 0 or self.y != 0
    
    def __getitem__(self, index):
        """索引访问"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("索引超出范围")
    
    def __iter__(self):
        """可迭代"""
        yield self.x
        yield self.y

# 测试
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")
print(f"v2 = {v2}")
print(f"v1 + v2 = {v1 + v2}")
print(f"v1 * 2 = {v1 * 2}")
print(f"v1 == v2: {v1 == v2}")
print(f"len(v1): {len(v1)}")
print(f"bool(v1): {bool(v1)}")
print(f"v1[0]: {v1[0]}, v1[1]: {v1[1]}")
print(f"list(v1): {list(v1)}")

print("\n✅ 测试1通过：掌握常用魔术方法")


# ==================== 测试 2: 上下文管理器 ====================

print("\n【测试 2】上下文管理器")
print("-" * 70)

class Timer:
    """计时器上下文管理器"""
    
    def __init__(self, name="操作"):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        """进入上下文"""
        import time
        self.start_time = time.time()
        print(f"⏱️  开始 {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        import time
        elapsed = time.time() - self.start_time
        print(f"⏱️  完成 {self.name}，耗时: {elapsed:.4f}秒")
        
        # 不处理异常，返回 False
        return False

# 测试
with Timer("数据处理"):
    total = sum(range(1000000))

print("\n✅ 测试2通过：理解上下文管理器协议")


# ==================== 测试 3: 迭代器协议 ====================

print("\n【测试 3】迭代器协议")
print("-" * 70)

class Fibonacci:
    """斐波那契数列迭代器"""
    
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        """返回迭代器本身"""
        return self
    
    def __next__(self):
        """返回下一个值"""
        if self.count >= self.max_count:
            raise StopIteration
        
        self.count += 1
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result

# 测试
print("前10个斐波那契数:")
fib = Fibonacci(10)
print(list(fib))

print("\n✅ 测试3通过：理解迭代器协议")


# ==================== 测试 4: 装饰器 ====================

print("\n【测试 4】装饰器理解")
print("-" * 70)

def retry(max_attempts=3):
    """重试装饰器（带参数）"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"  尝试 {attempt}/{max_attempts}")
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"  ❌ 失败: {e}")
                        raise
                    print(f"  ⚠️  重试...")
        return wrapper
    return decorator

# 测试
counter = {'attempts': 0}

@retry(max_attempts=3)
def flaky_function():
    """模拟不稳定的函数"""
    counter['attempts'] += 1
    if counter['attempts'] < 3:
        raise ValueError("临时错误")
    return "成功！"

result = flaky_function()
print(f"结果: {result}")

print("\n✅ 测试4通过：掌握装饰器（包括带参数）")


# ==================== 测试 5: 类继承与 MRO ====================

print("\n【测试 5】类继承与 MRO")
print("-" * 70)

class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B -> " + super().method()

class C(A):
    def method(self):
        return "C -> " + super().method()

class D(B, C):
    def method(self):
        return "D -> " + super().method()

# 测试
d = D()
print(f"d.method() = {d.method()}")
print(f"MRO: {[cls.__name__ for cls in D.__mro__]}")

print("\n✅ 测试5通过：理解 MRO 和 super()")


# ==================== 测试 6: 描述符 ====================

print("\n【测试 6】描述符协议")
print("-" * 70)

class Validator:
    """通用验证器描述符"""
    
    def __init__(self, validator_func, error_msg):
        self.validator_func = validator_func
        self.error_msg = error_msg
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = '_' + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, None)
    
    def __set__(self, instance, value):
        if not self.validator_func(value):
            raise ValueError(self.error_msg)
        setattr(instance, self.name, value)

class Product:
    name = Validator(
        lambda x: isinstance(x, str) and len(x) > 0,
        "名称必须是非空字符串"
    )
    price = Validator(
        lambda x: isinstance(x, (int, float)) and x > 0,
        "价格必须是正数"
    )
    
    def __init__(self, name, price):
        self.name = name
        self.price = price

# 测试
product = Product("笔记本", 5000)
print(f"商品: {product.name}, 价格: {product.price}")

try:
    product.price = -100
except ValueError as e:
    print(f"验证失败: {e}")

print("\n✅ 测试6通过：掌握描述符协议")


# ==================== 测试 7: 元类 ====================

print("\n【测试 7】元类理解")
print("-" * 70)

class SingletonMeta(type):
    """单例模式元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.settings = {}
    
    def set(self, key, value):
        self.settings[key] = value
    
    def get(self, key):
        return self.settings.get(key)

# 测试
config1 = Config()
config1.set('debug', True)

config2 = Config()
print(f"config1 is config2: {config1 is config2}")
print(f"config2.get('debug'): {config2.get('debug')}")

print("\n✅ 测试7通过：理解元类的作用")


# ==================== 测试 8: 属性访问控制 ====================

print("\n【测试 8】属性访问控制")
print("-" * 70)

class SmartDict:
    """智能字典 - 综合使用属性访问方法"""
    
    def __init__(self):
        object.__setattr__(self, '_data', {})
        object.__setattr__(self, '_access_count', {})
    
    def __getattr__(self, name):
        """获取不存在的属性"""
        if name in self._data:
            self._access_count[name] = self._access_count.get(name, 0) + 1
            return self._data[name]
        return None
    
    def __setattr__(self, name, value):
        """设置属性"""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value
    
    def get_access_count(self, name):
        """获取访问次数"""
        return self._access_count.get(name, 0)

# 测试
sd = SmartDict()
sd.x = 10
sd.y = 20

print(f"sd.x = {sd.x}")
print(f"sd.x = {sd.x}")
print(f"sd.y = {sd.y}")
print(f"x 访问次数: {sd.get_access_count('x')}")
print(f"y 访问次数: {sd.get_access_count('y')}")

print("\n✅ 测试8通过：掌握属性访问控制")


# ==================== 测试 9: property 装饰器 ====================

print("\n【测试 9】@property 装饰器")
print("-" * 70)

class Temperature:
    """温度类 - 测试 property"""
    
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self):
        return self._celsius + 273.15

# 测试
temp = Temperature(0)
print(f"0°C = {temp.fahrenheit}°F = {temp.kelvin}K")

temp.fahrenheit = 212
print(f"212°F = {temp.celsius}°C")

print("\n✅ 测试9通过：掌握 @property 装饰器")


# ==================== 知识点总结 ====================

print("\n" + "=" * 70)
print("第一阶段知识点掌握情况总结")
print("=" * 70)

knowledge_map = """
✅ Python 对象模型
   • 一切皆对象
   • 类型系统
   • 内存管理

✅ 魔术方法
   • __init__, __repr__, __str__
   • __add__, __mul__, __eq__
   • __len__, __bool__, __getitem__
   • __iter__, __next__

✅ 上下文管理器
   • __enter__, __exit__
   • 资源管理
   • 异常处理

✅ 装饰器
   • 函数装饰器
   • 类装饰器
   • 带参数的装饰器
   • functools 模块

✅ 迭代器与生成器
   • 迭代器协议
   • yield 关键字
   • 生成器表达式

✅ OOP 核心
   • 类与继承
   • MRO 解析
   • super() 使用
   • 抽象基类

✅ 元编程
   • 元类（metaclass）
   • 描述符（descriptor）
   • __getattr__, __setattr__, __getattribute__
   • @property 装饰器

✅ 设计思维
   • 封装
   • 继承
   • 多态
   • 组合优于继承
"""

print(knowledge_map)

print("\n🎉 恭喜！你已经完成了第一阶段的所有核心知识点！")