# 类的创建过程和内部机制详解

import sys
import inspect
from typing import Any, Dict, List, Type

# =============================================================================
# 1. 类的创建过程分步演示
# =============================================================================

def demonstrate_class_creation():
    """演示类的创建过程"""
    print("=== 类的创建过程演示 ===")
    
    # Python 中类的创建实际上是调用 type() 函数
    print("1. 动态创建类:")
    
    # 方式1: 使用 class 语句（常规方式）
    class RegularClass:
        class_var = "我是类变量"
        
        def __init__(self, value):
            self.instance_var = value
        
        def method(self):
            return f"实例方法: {self.instance_var}"
        
        @classmethod
        def class_method(cls):
            return f"类方法: {cls.class_var}"
        
        @staticmethod
        def static_method():
            return "静态方法"
    
    # 方式2: 使用 type() 动态创建（等效方式）
    def init_method(self, value):
        self.instance_var = value
    
    def instance_method(self):
        return f"实例方法: {self.instance_var}"
    
    @classmethod
    def class_method(cls):
        return f"类方法: {cls.class_var}"
    
    @staticmethod
    def static_method():
        return "静态方法"
    
    # type(name, bases, dict) 创建类
    DynamicClass = type(
        'DynamicClass',  # 类名
        (),              # 基类元组
        {                # 类字典
            'class_var': "我是类变量",
            '__init__': init_method,
            'method': instance_method,
            'class_method': class_method,
            'static_method': static_method,
        }
    )
    
    print(f"常规类: {RegularClass}")
    print(f"动态类: {DynamicClass}")
    print(f"两者相等: {type(RegularClass) == type(DynamicClass)}")
    
    # 测试功能等效性
    obj1 = RegularClass("测试1")
    obj2 = DynamicClass("测试2")
    
    print(f"常规对象方法: {obj1.method()}")
    print(f"动态对象方法: {obj2.method()}")

class ClassCreationMonitor(type):
    """监控类创建过程的元类"""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        print(f"\n--- 创建类 {name} ---")
        print(f"元类: {mcs.__name__}")
        print(f"基类: {[base.__name__ for base in bases]}")
        print(f"命名空间键: {list(namespace.keys())}")
        print(f"额外参数: {kwargs}")
        
        # 在类创建前可以修改命名空间
        if 'auto_timestamp' in kwargs and kwargs['auto_timestamp']:
            import datetime
            namespace['created_at'] = datetime.datetime.now()
        
        # 调用父元类的 __new__ 创建类
        cls = super().__new__(mcs, name, bases, namespace)
        
        print(f"类创建完成: {cls}")
        return cls
    
    def __init__(cls, name, bases, namespace, **kwargs):
        print(f"初始化类 {name}")
        super().__init__(name, bases, namespace)
        
        # 类创建后的初始化工作
        cls._creation_order = getattr(cls, '_creation_order', 0) + 1
        print(f"类 {name} 创建顺序: {cls._creation_order}")

def demonstrate_metaclass_creation():
    """演示元类控制的类创建"""
    print("\n=== 元类控制的类创建过程 ===")
    
    class MonitoredClass(metaclass=ClassCreationMonitor, auto_timestamp=True):
        """被监控的类"""
        class_attr = "监控类属性"
        
        def __init__(self, value):
            self.value = value
        
        def get_info(self):
            return {
                'value': self.value,
                'class_attr': self.class_attr,
                'created_at': getattr(self, 'created_at', 'N/A'),
                'creation_order': getattr(self, '_creation_order', 'N/A')
            }
    
    print(f"\n创建实例:")
    obj = MonitoredClass("测试值")
    print(f"实例信息: {obj.get_info()}")

# =============================================================================
# 2. 类的内部结构分析
# =============================================================================

class ClassInspector:
    """类结构检查器"""
    
    @staticmethod
    def analyze_class(cls: Type) -> Dict[str, Any]:
        """分析类的内部结构"""
        analysis = {
            'class_info': {
                'name': cls.__name__,
                'module': cls.__module__,
                'qualname': getattr(cls, '__qualname__', 'N/A'),
                'doc': cls.__doc__,
            },
            'hierarchy': {
                'bases': [base.__name__ for base in cls.__bases__],
                'mro': [c.__name__ for c in cls.__mro__],
                'metaclass': type(cls).__name__,
            },
            'attributes': {},
            'methods': {},
            'properties': {},
            'special_methods': {},
        }
        
        # 分析所有属性
        for name, obj in inspect.getmembers(cls):
            if name.startswith('__') and name.endswith('__'):
                # 特殊方法
                if callable(obj):
                    analysis['special_methods'][name] = {
                        'type': type(obj).__name__,
                        'defined_in': obj.__qualname__.split('.')[-2] if '.' in obj.__qualname__ else cls.__name__
                    }
            elif inspect.ismethod(obj) or inspect.isfunction(obj):
                # 方法
                analysis['methods'][name] = {
                    'type': 'method' if inspect.ismethod(obj) else 'function',
                    'is_classmethod': isinstance(inspect.getattr_static(cls, name), classmethod),
                    'is_staticmethod': isinstance(inspect.getattr_static(cls, name), staticmethod),
                    'defined_in': obj.__qualname__.split('.')[-2] if '.' in obj.__qualname__ else cls.__name__
                }
            elif isinstance(inspect.getattr_static(cls, name), property):
                # 属性
                prop = inspect.getattr_static(cls, name)
                analysis['properties'][name] = {
                    'has_getter': prop.fget is not None,
                    'has_setter': prop.fset is not None,
                    'has_deleter': prop.fdel is not None,
                    'doc': prop.__doc__,
                }
            else:
                # 类属性
                analysis['attributes'][name] = {
                    'type': type(obj).__name__,
                    'value': repr(obj) if len(repr(obj)) < 50 else f"{repr(obj)[:47]}...",
                }
        
        return analysis
    
    @staticmethod
    def print_analysis(cls: Type):
        """打印类分析结果"""
        analysis = ClassInspector.analyze_class(cls)
        
        print(f"\n=== 类 {analysis['class_info']['name']} 分析报告 ===")
        
        # 基本信息
        print(f"模块: {analysis['class_info']['module']}")
        print(f"完整名称: {analysis['class_info']['qualname']}")
        print(f"文档: {analysis['class_info']['doc'] or '无'}")
        
        # 继承层次
        print(f"\n继承信息:")
        print(f"  直接基类: {analysis['hierarchy']['bases']}")
        print(f"  MRO: {' -> '.join(analysis['hierarchy']['mro'])}")
        print(f"  元类: {analysis['hierarchy']['metaclass']}")
        
        # 属性统计
        print(f"\n成员统计:")
        print(f"  类属性: {len(analysis['attributes'])}")
        print(f"  方法: {len(analysis['methods'])}")
        print(f"  属性(property): {len(analysis['properties'])}")
        print(f"  特殊方法: {len(analysis['special_methods'])}")
        
        # 详细信息
        if analysis['attributes']:
            print(f"\n类属性:")
            for name, info in analysis['attributes'].items():
                print(f"  {name}: {info['type']} = {info['value']}")
        
        if analysis['methods']:
            print(f"\n方法:")
            for name, info in analysis['methods'].items():
                method_type = []
                if info['is_classmethod']:
                    method_type.append('classmethod')
                elif info['is_staticmethod']:
                    method_type.append('staticmethod')
                else:
                    method_type.append('instance method')
                
                print(f"  {name}: {', '.join(method_type)} (定义在: {info['defined_in']})")

# =============================================================================
# 3. 类属性 vs 实例属性
# =============================================================================

class AttributeDemo:
    """演示类属性和实例属性的区别"""
    
    # 类属性
    class_counter = 0
    shared_list = []  # 危险：可变类属性
    
    def __init__(self, name):
        # 实例属性
        self.name = name
        self.instance_id = AttributeDemo.class_counter
        
        # 修改类属性
        AttributeDemo.class_counter += 1
        
        # 危险操作：修改可变类属性
        AttributeDemo.shared_list.append(name)
    
    @classmethod
    def get_class_info(cls):
        """获取类信息"""
        return {
            'class_name': cls.__name__,
            'instance_count': cls.class_counter,
            'shared_list': cls.shared_list.copy()
        }
    
    def get_instance_info(self):
        """获取实例信息"""
        return {
            'name': self.name,
            'instance_id': self.instance_id,
            'class_counter': self.class_counter,  # 通过实例访问类属性
        }

def demonstrate_attribute_differences():
    """演示属性差异"""
    print("\n=== 类属性 vs 实例属性演示 ===")
    
    print("初始状态:")
    print(f"类信息: {AttributeDemo.get_class_info()}")
    
    print("\n创建实例:")
    obj1 = AttributeDemo("对象1")
    obj2 = AttributeDemo("对象2")
    obj3 = AttributeDemo("对象3")
    
    print(f"创建后类信息: {AttributeDemo.get_class_info()}")
    print(f"对象1信息: {obj1.get_instance_info()}")
    print(f"对象2信息: {obj2.get_instance_info()}")
    
    print("\n属性访问优先级演示:")
    print(f"obj1.class_counter (通过实例访问类属性): {obj1.class_counter}")
    
    # 给实例添加同名属性
    obj1.class_counter = 999
    print(f"obj1.class_counter = 999 后:")
    print(f"  obj1.class_counter: {obj1.class_counter}")  # 实例属性
    print(f"  AttributeDemo.class_counter: {AttributeDemo.class_counter}")  # 类属性
    print(f"  obj2.class_counter: {obj2.class_counter}")  # 其他实例仍访问类属性

# =============================================================================
# 4. 类装饰器
# =============================================================================

def add_debugging(cls):
    """类装饰器：为类添加调试功能"""
    original_init = cls.__init__
    
    def debug_init(self, *args, **kwargs):
        print(f"创建 {cls.__name__} 实例: args={args}, kwargs={kwargs}")
        original_init(self, *args, **kwargs)
        print(f"{cls.__name__} 实例创建完成: {id(self)}")
    
    cls.__init__ = debug_init
    cls._debug_enabled = True
    
    return cls

def singleton(cls):
    """单例模式类装饰器"""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@add_debugging
class DebuggedClass:
    """被调试装饰的类"""
    def __init__(self, value):
        self.value = value

@singleton
class SingletonClass:
    """单例类"""
    def __init__(self, config):
        self.config = config

def demonstrate_class_decorators():
    """演示类装饰器"""
    print("\n=== 类装饰器演示 ===")
    
    print("1. 调试装饰器:")
    obj1 = DebuggedClass("测试值1")
    obj2 = DebuggedClass("测试值2")
    
    print("\n2. 单例装饰器:")
    singleton1 = SingletonClass("配置1")
    singleton2 = SingletonClass("配置2")  # 应该返回同一个实例
    
    print(f"singleton1 is singleton2: {singleton1 is singleton2}")
    print(f"singleton1.config: {singleton1.config}")
    print(f"singleton2.config: {singleton2.config}")

# =============================================================================
# 运行演示
# =============================================================================

if __name__ == "__main__":
    # 类创建过程演示
    demonstrate_class_creation()
    
    # 元类演示
    demonstrate_metaclass_creation()
    
    # 类结构分析
    ClassInspector.print_analysis(AttributeDemo)
    
    # 属性差异演示
    demonstrate_attribute_differences()
    
    # 类装饰器演示
    demonstrate_class_decorators()