# 属性描述符和Property深度应用

import weakref
from typing import Any, Dict, Optional

# =============================================================================
# 1. Property 基础和高级用法
# =============================================================================

class SmartProperty:
    """演示 property 的各种用法"""
    
    def __init__(self, initial_value: int = 0):
        self._value = initial_value
        self._access_count = 0
    
    @property
    def value(self) -> int:
        """获取值时自动计数"""
        self._access_count += 1
        print(f"访问 value，第 {self._access_count} 次")
        return self._value
    
    @value.setter  
    def value(self, new_value: int):
        """设置值时进行验证"""
        if not isinstance(new_value, int):
            raise TypeError("值必须是整数")
        if new_value < 0:
            raise ValueError("值不能为负")
        
        old_value = self._value
        self._value = new_value
        print(f"值从 {old_value} 更改为 {new_value}")
    
    @value.deleter
    def value(self):
        """删除属性时的清理工作"""
        print(f"删除值 {self._value}，访问了 {self._access_count} 次")
        self._value = 0
        self._access_count = 0

# =============================================================================
# 2. 自定义描述符类
# =============================================================================

class ValidatedAttribute:
    """验证属性描述符"""
    
    def __init__(self, validator_func, default=None):
        self.validator = validator_func
        self.default = default
        self.data = weakref.WeakKeyDictionary()  # 避免内存泄漏
    
    def __get__(self, instance, owner):
        if instance is None:
            return self  # 通过类访问时返回描述符本身
        return self.data.get(instance, self.default)
    
    def __set__(self, instance, value):
        # 验证值
        if not self.validator(value):
            raise ValueError(f"验证失败: {value}")
        self.data[instance] = value
    
    def __delete__(self, instance):
        if instance in self.data:
            del self.data[instance]

class TypedAttribute:
    """类型检查描述符"""
    
    def __init__(self, expected_type, default=None):
        self.expected_type = expected_type
        self.default = default
        self.data = weakref.WeakKeyDictionary()
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.data.get(instance, self.default)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"期望 {self.expected_type.__name__}，得到 {type(value).__name__}")
        self.data[instance] = value

# =============================================================================
# 3. 使用描述符的示例类
# =============================================================================

class Person:
    """使用描述符的人员类"""
    
    # 使用自定义描述符
    name = TypedAttribute(str, "")
    age = ValidatedAttribute(lambda x: isinstance(x, int) and 0 <= x <= 150, 0)
    email = ValidatedAttribute(lambda x: isinstance(x, str) and '@' in x, "")
    
    def __init__(self, name: str, age: int, email: str):
        self.name = name      # 触发 TypedAttribute.__set__
        self.age = age        # 触发 ValidatedAttribute.__set__ 
        self.email = email    # 触发 ValidatedAttribute.__set__
    
    def __str__(self):
        return f"Person(name={self.name}, age={self.age}, email={self.email})"

# =============================================================================
# 4. 计算属性和缓存
# =============================================================================

class CachedProperty:
    """缓存计算结果的属性描述符"""
    
    def __init__(self, func):
        self.func = func
        self.cache = weakref.WeakKeyDictionary()
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        if instance not in self.cache:
            print(f"计算 {self.func.__name__}...")
            self.cache[instance] = self.func(instance)
        else:
            print(f"使用缓存的 {self.func.__name__}")
        
        return self.cache[instance]
    
    def __set__(self, instance, value):
        # 允许手动设置缓存值
        self.cache[instance] = value
    
    def __delete__(self, instance):
        # 清除缓存
        if instance in self.cache:
            del self.cache[instance]

class DataProcessor:
    """数据处理器，演示缓存属性"""
    
    def __init__(self, data: list):
        self.data = data
    
    @CachedProperty
    def total(self):
        """计算总和（耗时操作，需要缓存）"""
        import time
        time.sleep(0.1)  # 模拟耗时计算
        return sum(self.data)
    
    @CachedProperty  
    def average(self):
        """计算平均值"""
        return self.total / len(self.data) if self.data else 0
    
    def add_data(self, value):
        """添加数据后清除缓存"""
        self.data.append(value)
        # 清除相关缓存
        del self.total
        del self.average

# =============================================================================
# 演示函数
# =============================================================================

def demonstrate_properties():
    """演示 property 用法"""
    print("=== Property 演示 ===\n")
    
    obj = SmartProperty(10)
    
    # 读取属性
    print(f"当前值: {obj.value}")
    print(f"再次读取: {obj.value}")
    
    # 设置属性
    obj.value = 20
    
    # 尝试设置无效值
    try:
        obj.value = -5
    except ValueError as e:
        print(f"验证错误: {e}")
    
    # 删除属性
    del obj.value
    print(f"删除后的值: {obj.value}")

def demonstrate_descriptors():
    """演示自定义描述符"""
    print("\n=== 自定义描述符演示 ===\n")
    
    # 创建正常的人员对象
    person = Person("Alice", 30, "alice@example.com")
    print(f"创建: {person}")
    
    # 修改属性
    person.name = "Bob"
    person.age = 25
    print(f"修改后: {person}")
    
    # 尝试设置无效值
    try:
        person.age = 200  # 超出范围
    except ValueError as e:
        print(f"年龄验证错误: {e}")
    
    try:
        person.email = "invalid-email"  # 无效邮箱
    except ValueError as e:
        print(f"邮箱验证错误: {e}")

def demonstrate_cached_properties():
    """演示缓存属性"""
    print("\n=== 缓存属性演示 ===\n")
    
    processor = DataProcessor([1, 2, 3, 4, 5])
    
    # 第一次访问 - 触发计算
    print(f"总和: {processor.total}")
    print(f"平均值: {processor.average}")
    
    # 再次访问 - 使用缓存
    print(f"再次获取总和: {processor.total}")
    
    # 添加数据并清除缓存
    processor.add_data(6)
    print(f"添加数据后的总和: {processor.total}")  # 重新计算

if __name__ == "__main__":
    demonstrate_properties()
    demonstrate_descriptors() 
    demonstrate_cached_properties()