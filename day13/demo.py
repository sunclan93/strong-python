"""
@property 装饰器完整教程
从基础到高级应用
"""

# ==================== 1. 基础用法 ====================

print("=" * 60)
print("1. @property 基础用法")
print("=" * 60)

class Circle:
    """圆形类"""
    
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """获取半径"""
        print("  → 调用 getter")
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """设置半径（带验证）"""
        print(f"  → 调用 setter: {value}")
        if value < 0:
            raise ValueError("半径不能为负数")
        self._radius = value
    
    @radius.deleter
    def radius(self):
        """删除半径"""
        print("  → 调用 deleter")
        del self._radius
    
    @property
    def area(self):
        """计算面积（只读属性）"""
        return 3.14159 * self._radius ** 2
    
    @property
    def circumference(self):
        """计算周长（只读属性）"""
        return 2 * 3.14159 * self._radius

# 测试
circle = Circle(5)
print(f"半径: {circle.radius}")
print(f"面积: {circle.area:.2f}")
print(f"周长: {circle.circumference:.2f}")

print("\n修改半径:")
circle.radius = 10
print(f"新半径: {circle.radius}")
print(f"新面积: {circle.area:.2f}")

print("\n尝试修改只读属性:")
try:
    circle.area = 100  # 会报错
except AttributeError as e:
    print(f"❌ 错误: {e}")


# ==================== 2. 计算属性 ====================

print("\n" + "=" * 60)
print("2. 计算属性示例")
print("=" * 60)

class Rectangle:
    """矩形类"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @property
    def area(self):
        """面积（动态计算）"""
        return self.width * self.height
    
    @property
    def perimeter(self):
        """周长（动态计算）"""
        return 2 * (self.width + self.height)
    
    @property
    def diagonal(self):
        """对角线长度"""
        return (self.width ** 2 + self.height ** 2) ** 0.5
    
    @property
    def is_square(self):
        """是否是正方形"""
        return self.width == self.height

# 测试
rect = Rectangle(3, 4)
print(f"宽: {rect.width}, 高: {rect.height}")
print(f"面积: {rect.area}")
print(f"周长: {rect.perimeter}")
print(f"对角线: {rect.diagonal:.2f}")
print(f"是否正方形: {rect.is_square}")

# 修改尺寸后，所有计算属性自动更新
rect.width = 5
rect.height = 5
print(f"\n修改后:")
print(f"面积: {rect.area}")
print(f"是否正方形: {rect.is_square}")


# ==================== 3. 属性验证 ====================

print("\n" + "=" * 60)
print("3. 使用 property 进行属性验证")
print("=" * 60)

class BankAccount:
    """银行账户"""
    
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance
    
    @property
    def balance(self):
        """余额"""
        return self._balance
    
    @balance.setter
    def balance(self, value):
        """设置余额（验证）"""
        if not isinstance(value, (int, float)):
            raise TypeError("余额必须是数字")
        if value < 0:
            raise ValueError("余额不能为负数")
        self._balance = value
    
    def deposit(self, amount):
        """存款"""
        if amount <= 0:
            raise ValueError("存款金额必须大于0")
        self.balance += amount
        print(f"✓ 存款 {amount} 元，当前余额: {self.balance}")
    
    def withdraw(self, amount):
        """取款"""
        if amount <= 0:
            raise ValueError("取款金额必须大于0")
        if amount > self.balance:
            raise ValueError("余额不足")
        self.balance -= amount
        print(f"✓ 取款 {amount} 元，当前余额: {self.balance}")

# 测试
account = BankAccount("Alice", 1000)
print(f"账户所有者: {account.owner}")
print(f"初始余额: {account.balance}")

account.deposit(500)
account.withdraw(300)

try:
    account.balance = -100  # 验证失败
except ValueError as e:
    print(f"❌ 验证失败: {e}")


# ==================== 4. 缓存计算结果 ====================

print("\n" + "=" * 60)
print("4. 带缓存的 property")
print("=" * 60)

class DataProcessor:
    """数据处理器（带缓存）"""
    
    def __init__(self, data):
        self._data = data
        self._processed_cache = None
        self._stats_cache = None
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        # 数据改变时清除缓存
        self._data = value
        self._processed_cache = None
        self._stats_cache = None
    
    @property
    def processed_data(self):
        """处理后的数据（带缓存）"""
        if self._processed_cache is None:
            print("  🔄 计算 processed_data（耗时操作）")
            self._processed_cache = [x * 2 for x in self._data]
        else:
            print("  ⚡ 使用缓存的 processed_data")
        return self._processed_cache
    
    @property
    def statistics(self):
        """统计信息（带缓存）"""
        if self._stats_cache is None:
            print("  🔄 计算 statistics（耗时操作）")
            self._stats_cache = {
                'sum': sum(self._data),
                'avg': sum(self._data) / len(self._data),
                'max': max(self._data),
                'min': min(self._data)
            }
        else:
            print("  ⚡ 使用缓存的 statistics")
        return self._stats_cache

# 测试
processor = DataProcessor([1, 2, 3, 4, 5])

print("第一次访问:")
print(processor.processed_data)

print("\n第二次访问（使用缓存）:")
print(processor.processed_data)

print("\n修改数据后:")
processor.data = [10, 20, 30]
print(processor.processed_data)  # 重新计算


# ==================== 5. 类属性与实例属性 ====================

print("\n" + "=" * 60)
print("5. property 的类属性和实例属性")
print("=" * 60)

class Temperature:
    """温度转换"""
    
    _conversion_count = 0  # 类属性：转换次数统计
    
    def __init__(self, celsius):
        self._celsius = celsius
    
    @property
    def celsius(self):
        """摄氏度"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        self._celsius = value
        Temperature._conversion_count += 1
    
    @property
    def fahrenheit(self):
        """华氏度"""
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9
        Temperature._conversion_count += 1
    
    @classmethod
    def get_conversion_count(cls):
        """获取转换次数"""
        return cls._conversion_count

# 测试
temp1 = Temperature(0)
print(f"0°C = {temp1.fahrenheit}°F")

temp2 = Temperature(100)
print(f"100°C = {temp2.fahrenheit}°F")

temp2.fahrenheit = 212
print(f"212°F = {temp2.celsius}°C")

print(f"总转换次数: {Temperature.get_conversion_count()}")


# ==================== 6. 动态 property ====================

print("\n" + "=" * 60)
print("6. 动态创建 property")
print("=" * 60)

def make_property(attribute_name, validator=None):
    """工厂函数：动态创建 property"""
    
    private_name = f'_{attribute_name}'
    
    def getter(self):
        return getattr(self, private_name)
    
    def setter(self, value):
        if validator:
            validator(value)
        setattr(self, private_name, value)
    
    return property(getter, setter)


# 验证器
def positive_validator(value):
    if value <= 0:
        raise ValueError("必须是正数")


def string_validator(value):
    if not isinstance(value, str):
        raise TypeError("必须是字符串")


# 动态创建类
class Product:
    name = make_property('name', string_validator)
    price = make_property('price', positive_validator)
    stock = make_property('stock', positive_validator)
    
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

# 测试
product = Product("笔记本", 5000, 10)
print(f"商品: {product.name}, 价格: {product.price}, 库存: {product.stock}")

try:
    product.price = -100
except ValueError as e:
    print(f"❌ 验证失败: {e}")


# ==================== 7. property 原理剖析 ====================

print("\n" + "=" * 60)
print("7. property 的底层实现原理")
print("=" * 60)

class MyProperty:
    """手动实现 property 的简化版本"""
    
    def __init__(self, fget=None, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("无法读取属性")
        return self.fget(instance)
    
    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("无法设置属性")
        self.fset(instance, value)
    
    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("无法删除属性")
        self.fdel(instance)
    
    def setter(self, fset):
        """支持装饰器语法"""
        return type(self)(self.fget, fset, self.fdel)


class TestClass:
    def __init__(self, value):
        self._value = value
    
    def get_value(self):
        print("  → 调用 get_value")
        return self._value
    
    def set_value(self, value):
        print(f"  → 调用 set_value: {value}")
        self._value = value
    
    # 使用自定义 property
    value = MyProperty(get_value, set_value)

# 测试
obj = TestClass(100)
print(f"obj.value = {obj.value}")
obj.value = 200
print(f"obj.value = {obj.value}")


# ==================== 总结 ====================

print("\n" + "=" * 60)
print("@property 最佳实践")
print("=" * 60)

best_practices = """
✅ 使用场景：
  • 需要对属性进行验证
  • 需要计算属性值
  • 需要保持向后兼容（方法→属性）
  • 需要只读属性

✅ 命名约定：
  • 公开属性：name
  • 私有存储：_name
  • 特殊属性：__name（名称改写）

✅ 性能考虑：
  • 避免在 property 中执行耗时操作
  • 考虑使用缓存
  • 简单属性直接使用公开属性

❌ 避免：
  • property 中修改其他属性
  • property 中有副作用
  • 过度使用 property
"""

print(best_practices)