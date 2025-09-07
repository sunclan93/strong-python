# 类方法和静态方法深度理解

from datetime import datetime
from typing import Type, Any

class MethodTypesDemo:
    """演示三种方法类型的区别和用法"""
    
    # 类属性
    instance_count = 0
    created_instances = []
    
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value
        
        # 更新类属性
        MethodTypesDemo.instance_count += 1
        MethodTypesDemo.created_instances.append(self)
    
    # 1. 实例方法 - 访问实例和类
    def instance_method(self):
        """实例方法：可以访问 self 和类属性"""
        return f"实例方法: {self.name}={self.value}, 总数={self.instance_count}"
    
    # 2. 类方法 - 只访问类，常用于替代构造函数
    @classmethod  
    def from_string(cls, data_string: str):
        """类方法：替代构造函数，从字符串创建实例"""
        name, value = data_string.split('=')
        return cls(name.strip(), int(value.strip()))
    
    @classmethod
    def get_statistics(cls):
        """类方法：获取类级别的统计信息"""
        return {
            'total_instances': cls.instance_count,
            'instance_names': [inst.name for inst in cls.created_instances]
        }
    
    @classmethod
    def reset_counters(cls):
        """类方法：重置类级别的数据"""
        cls.instance_count = 0
        cls.created_instances.clear()
    
    # 3. 静态方法 - 独立功能，不访问实例或类
    @staticmethod
    def validate_name(name: str) -> bool:
        """静态方法：验证名称格式（纯函数）"""
        return isinstance(name, str) and len(name) > 0 and name.isalnum()
    
    @staticmethod
    def parse_config(config_str: str) -> dict:
        """静态方法：解析配置字符串（工具函数）"""
        result = {}
        for pair in config_str.split(','):
            if '=' in pair:
                key, value = pair.split('=', 1)
                result[key.strip()] = value.strip()
        return result

def demonstrate_method_types():
    """演示三种方法的使用场景"""
    print("=== 方法类型演示 ===\n")
    
    # 静态方法 - 可以直接通过类调用
    print("1. 静态方法使用:")
    print(f"验证名称 'test123': {MethodTypesDemo.validate_name('test123')}")
    print(f"验证名称 'test@#': {MethodTypesDemo.validate_name('test@#')}")
    
    config = MethodTypesDemo.parse_config("name=test, value=100, type=demo")
    print(f"解析配置: {config}")
    
    # 类方法 - 替代构造函数
    print(f"\n2. 类方法 - 替代构造函数:")
    obj1 = MethodTypesDemo("obj1", 10)
    obj2 = MethodTypesDemo.from_string("obj2 = 20")  # 类方法创建
    obj3 = MethodTypesDemo.from_string("obj3 = 30")
    
    print(f"创建了 {MethodTypesDemo.instance_count} 个实例")
    
    # 类方法 - 获取统计信息
    print(f"\n3. 类方法 - 获取统计:")
    stats = MethodTypesDemo.get_statistics()
    print(f"统计信息: {stats}")
    
    # 实例方法
    print(f"\n4. 实例方法:")
    print(obj1.instance_method())
    print(obj2.instance_method())

# =============================================================================
# 继承中的方法行为
# =============================================================================

class Parent:
    family_name = "Smith"
    
    @classmethod
    def get_family_info(cls):
        return f"Family: {cls.family_name}, Class: {cls.__name__}"
    
    @staticmethod
    def utility_function(x, y):
        return x + y

class Child(Parent):
    family_name = "Johnson"  # 覆盖父类属性

def demonstrate_inheritance_methods():
    """演示继承中方法的行为"""
    print("\n=== 继承中的方法行为 ===\n")
    
    # 类方法在继承中的行为
    print("类方法继承:")
    print(f"Parent: {Parent.get_family_info()}")
    print(f"Child: {Child.get_family_info()}")  # 自动使用子类的属性
    
    # 静态方法在继承中的行为
    print(f"\n静态方法继承:")
    print(f"Parent.utility: {Parent.utility_function(1, 2)}")
    print(f"Child.utility: {Child.utility_function(3, 4)}")  # 完全相同的行为

if __name__ == "__main__":
    demonstrate_method_types()
    demonstrate_inheritance_methods()