# super() 深度理解与正确使用

import functools
from typing import Any, Dict, List

# =============================================================================
# 1. super() 基础理解
# =============================================================================

class SuperBasics:
    """super() 基础概念演示"""
    
    def demonstrate_super_basics(self):
        """演示 super() 的基本概念"""
        print("=== super() 基础概念 ===")
        
        class Animal:
            def __init__(self, name, species):
                print(f"Animal.__init__: {name}, {species}")
                self.name = name
                self.species = species
            
            def speak(self):
                return f"{self.name} makes a sound"
            
            def info(self):
                return f"{self.name} is a {self.species}"
        
        class Dog(Animal):
            def __init__(self, name, breed):
                print(f"Dog.__init__: {name}, {breed}")
                # 正确使用 super()
                super().__init__(name, "Canine")
                self.breed = breed
            
            def speak(self):
                # 扩展父类方法
                base_sound = super().speak()
                return f"{base_sound} - Woof!"
            
            def info(self):
                # 组合父类信息
                base_info = super().info()
                return f"{base_info}, breed: {self.breed}"
        
        print("创建狗实例:")
        dog = Dog("Buddy", "Golden Retriever")
        print(f"发声: {dog.speak()}")
        print(f"信息: {dog.info()}")
        
        return Dog

# =============================================================================
# 2. super() 的工作原理
# =============================================================================

class SuperMechanism:
    """super() 工作机制深度分析"""
    
    @staticmethod
    def analyze_super_call(cls, method_name):
        """分析 super() 调用的解析过程"""
        print(f"\n=== 分析 {cls.__name__}.{method_name} 中的 super() ===")
        
        mro = cls.__mro__
        print(f"MRO: {' -> '.join(c.__name__ for c in mro)}")
        
        # 查找当前类在MRO中的位置
        current_index = mro.index(cls)
        print(f"当前类 {cls.__name__} 在MRO位置: {current_index}")
        
        # super() 会从下一个类开始查找
        if current_index + 1 < len(mro):
            next_cls = mro[current_index + 1]
            print(f"super() 将从 {next_cls.__name__} 开始查找 {method_name}")
            
            # 查找方法
            for i, c in enumerate(mro[current_index + 1:], current_index + 1):
                if hasattr(c, method_name) and method_name in c.__dict__:
                    print(f"找到方法: {c.__name__}.{method_name} (MRO位置: {i})")
                    break
            else:
                print(f"在剩余MRO中未找到 {method_name}")

class A:
    def method(self):
        print("A.method")
        return "A"

class B(A):
    def method(self):
        print("B.method - 调用 super()")
        result = super().method()
        print("B.method - super() 调用完成")
        return f"B -> {result}"

class C(A):
    def method(self):
        print("C.method - 调用 super()")
        result = super().method()
        print("C.method - super() 调用完成")
        return f"C -> {result}"

class D(B, C):
    def method(self):
        print("D.method - 调用 super()")
        result = super().method()
        print("D.method - super() 调用完成")
        return f"D -> {result}"

def demonstrate_super_mechanism():
    """演示 super() 机制"""
    print("\n=== super() 工作机制演示 ===")
    
    # 显示MRO
    print(f"D的MRO: {' -> '.join(c.__name__ for c in D.__mro__)}")
    
    # 分析super()调用
    SuperMechanism.analyze_super_call(D, 'method')
    SuperMechanism.analyze_super_call(B, 'method')
    
    print("\n执行 D().method():")
    d = D()
    result = d.method()
    print(f"最终结果: {result}")

# =============================================================================
# 3. super() 的常见陷阱
# =============================================================================

class SuperTraps:
    """super() 常见陷阱演示"""
    
    def demonstrate_argument_trap(self):
        """演示参数传递陷阱"""
        print("\n=== super() 参数传递陷阱 ===")
        
        class Parent:
            def __init__(self, name, **kwargs):
                print(f"Parent.__init__: name={name}, kwargs={kwargs}")
                super().__init__(**kwargs)  # 重要：传递剩余参数
                self.name = name
        
        class Mixin:
            def __init__(self, mixin_param=None, **kwargs):
                print(f"Mixin.__init__: mixin_param={mixin_param}, kwargs={kwargs}")
                super().__init__(**kwargs)
                self.mixin_param = mixin_param
        
        class Child(Parent, Mixin):
            def __init__(self, name, child_param, **kwargs):
                print(f"Child.__init__: name={name}, child_param={child_param}, kwargs={kwargs}")
                super().__init__(name=name, **kwargs)
                self.child_param = child_param
        
        print("正确的参数传递:")
        try:
            child = Child("测试", "child_value", mixin_param="mixin_value")
            print("✓ 创建成功")
        except Exception as e:
            print(f"✗ 创建失败: {e}")
        
        # 展示错误用法
        class BadChild(Parent, Mixin):
            def __init__(self, name, child_param):
                # 错误：没有使用**kwargs处理额外参数
                super().__init__(name)  # 这会导致问题
                self.child_param = child_param
        
        print("\n错误的参数传递:")
        try:
            bad_child = BadChild("测试", "child_value")
            print("✓ 创建成功")
        except Exception as e:
            print(f"✗ 创建失败: {e}")
    
    def demonstrate_method_signature_trap(self):
        """演示方法签名不一致陷阱"""
        print("\n=== 方法签名不一致陷阱 ===")
        
        class Base:
            def process(self, data):
                print(f"Base.process: {data}")
                return f"base_{data}"
        
        class MiddleA(Base):
            def process(self, data, mode="default"):
                print(f"MiddleA.process: {data}, mode={mode}")
                # 错误：直接传递不兼容的参数
                try:
                    result = super().process(data, mode)  # Base.process 不接受 mode
                    return f"middleA_{result}"
                except TypeError as e:
                    print(f"参数错误: {e}")
                    # 正确做法：只传递兼容的参数
                    result = super().process(data)
                    return f"middleA_{result}_mode_{mode}"
        
        class MiddleB(Base):
            def process(self, data, extra=None):
                print(f"MiddleB.process: {data}, extra={extra}")
                result = super().process(data)
                return f"middleB_{result}_extra_{extra}"
        
        class Final(MiddleA, MiddleB):
            def process(self, data, mode="default", extra=None):
                print(f"Final.process: {data}, mode={mode}, extra={extra}")
                # 需要小心处理参数
                result = super().process(data, mode=mode)  # 只有MiddleA需要mode
                return f"final_{result}"
        
        print("测试方法签名不一致:")
        final = Final()
        result = final.process("test_data", mode="advanced", extra="extra_data")
        print(f"最终结果: {result}")

# =============================================================================
# 4. 协作继承模式
# =============================================================================

class CooperativeInheritance:
    """协作继承模式演示"""
    
    def demonstrate_cooperative_pattern(self):
        """演示协作继承的正确模式"""
        print("\n=== 协作继承模式 ===")
        
        class Shape:
            def __init__(self, **kwargs):
                print(f"Shape.__init__: {kwargs}")
                super().__init__(**kwargs)
            
            def area(self):
                return 0
            
            def description(self):
                return "Generic shape"
        
        class ColorMixin:
            def __init__(self, color="white", **kwargs):
                print(f"ColorMixin.__init__: color={color}, kwargs={kwargs}")
                super().__init__(**kwargs)
                self.color = color
            
            def description(self):
                base_desc = super().description()
                return f"{base_desc} in {self.color}"
        
        class Rectangle(Shape):
            def __init__(self, width, height, **kwargs):
                print(f"Rectangle.__init__: width={width}, height={height}, kwargs={kwargs}")
                super().__init__(**kwargs)
                self.width = width
                self.height = height
            
            def area(self):
                return self.width * self.height
            
            def description(self):
                base_desc = super().description()
                return f"{base_desc.replace('Generic shape', 'Rectangle')}"
        
        class ColoredRectangle(ColorMixin, Rectangle):
            def __init__(self, width, height, color="white", **kwargs):
                print(f"ColoredRectangle.__init__: w={width}, h={height}, color={color}")
                super().__init__(width=width, height=height, color=color, **kwargs)
            
            def description(self):
                base_desc = super().description()
                return f"{base_desc} ({self.width}x{self.height})"
        
        print("创建彩色矩形:")
        rect = ColoredRectangle(10, 5, color="red")
        print(f"面积: {rect.area()}")
        print(f"描述: {rect.description()}")
        
        # 显示MRO
        print(f"\nMRO: {' -> '.join(c.__name__ for c in ColoredRectangle.__mro__)}")

# =============================================================================
# 5. super() 的高级用法
# =============================================================================

class AdvancedSuper:
    """super() 高级用法"""
    
    def demonstrate_explicit_super(self):
        """演示显式 super() 用法"""
        print("\n=== 显式 super() 用法 ===")
        
        class A:
            def method(self):
                return "A"
        
        class B(A):
            def method(self):
                return "B"
        
        class C(A):
            def method(self):
                return "C"
        
        class D(B, C):
            def method(self):
                # 普通 super() - 按MRO顺序
                normal_super = super().method()
                
                # 显式调用特定父类
                b_result = B.method(self)
                c_result = C.method(self)
                
                # 显式 super() 调用
                explicit_super = super(D, self).method()  # 等同于 super()
                
                return {
                    'normal_super': normal_super,
                    'explicit_super': explicit_super,
                    'b_direct': b_result,
                    'c_direct': c_result,
                }
        
        d = D()
        results = d.method()
        print(f"调用结果: {results}")
        print(f"MRO: {' -> '.join(c.__name__ for c in D.__mro__)}")
    
    def demonstrate_super_in_classmethods(self):
        """演示类方法中的 super()"""
        print("\n=== 类方法中的 super() ===")
        
        class Parent:
            count = 0
            
            @classmethod
            def create(cls, name):
                cls.count += 1
                print(f"Parent.create: {name}, count={cls.count}")
                return cls(name)
            
            def __init__(self, name):
                self.name = name
        
        class Child(Parent):
            child_count = 0
            
            @classmethod
            def create(cls, name, extra=None):
                cls.child_count += 1
                print(f"Child.create: {name}, extra={extra}, child_count={cls.child_count}")
                # 在类方法中使用 super()
                instance = super().create(name)
                instance.extra = extra
                return instance
        
        print("通过类方法创建实例:")
        child1 = Child.create("child1", "extra_data")
        child2 = Child.create("child2", "more_data")
        
        print(f"Parent.count: {Parent.count}")
        print(f"Child.child_count: {Child.child_count}")

# =============================================================================
# 6. super() 最佳实践
# =============================================================================

class SuperBestPractices:
    """super() 最佳实践"""
    
    def demonstrate_best_practices(self):
        """演示 super() 最佳实践"""
        print("\n=== super() 最佳实践 ===")
        
        # 1. 始终使用 **kwargs 处理额外参数
        class GoodBase:
            def __init__(self, name, **kwargs):
                super().__init__(**kwargs)  # 传递剩余参数
                self.name = name
                print(f"GoodBase: {name}")
        
        # 2. 混入类也要调用 super()
        class GoodMixin:
            def __init__(self, mixin_attr=None, **kwargs):
                super().__init__(**kwargs)  # 重要：混入也要调用super
                self.mixin_attr = mixin_attr
                print(f"GoodMixin: {mixin_attr}")
        
        # 3. 方法中适当使用 super()
        class GoodChild(GoodBase, GoodMixin):
            def __init__(self, name, child_attr, **kwargs):
                super().__init__(name=name, **kwargs)
                self.child_attr = child_attr
                print(f"GoodChild: {child_attr}")
            
            def process(self):
                # 可以选择性调用父类方法
                print("GoodChild.process - 前置处理")
                # 如果父类有process方法，可以调用
                if hasattr(super(), 'process'):
                    super().process()
                print("GoodChild.process - 后置处理")
        
        print("最佳实践示例:")
        good_child = GoodChild("test", "child_value", mixin_attr="mixin_value")
        good_child.process()

# =============================================================================
# 7. super() 调试工具
# =============================================================================

def trace_super_calls(cls):
    """装饰器：跟踪类中的 super() 调用"""
    def trace_method(method_name, original_method):
        @functools.wraps(original_method)
        def wrapper(*args, **kwargs):
            print(f"TRACE: {cls.__name__}.{method_name} 调用开始")
            try:
                result = original_method(*args, **kwargs)
                print(f"TRACE: {cls.__name__}.{method_name} 调用完成")
                return result
            except Exception as e:
                print(f"TRACE: {cls.__name__}.{method_name} 调用异常: {e}")
                raise
        return wrapper
    
    # 包装所有方法
    for attr_name in dir(cls):
        if not attr_name.startswith('_') or attr_name in ['__init__']:
            attr = getattr(cls, attr_name)
            if callable(attr) and hasattr(attr, '__func__'):
                setattr(cls, attr_name, trace_method(attr_name, attr))
    
    return cls

@trace_super_calls
class TracedParent:
    def __init__(self, name):
        print(f"TracedParent.__init__: {name}")
        self.name = name
    
    def method(self):
        print("TracedParent.method")
        return "parent"

@trace_super_calls
class TracedChild(TracedParent):
    def __init__(self, name, value):
        print(f"TracedChild.__init__: {name}, {value}")
        super().__init__(name)
        self.value = value
    
    def method(self):
        print("TracedChild.method - before super")
        result = super().method()
        print("TracedChild.method - after super")
        return f"child -> {result}"

def demonstrate_super_debugging():
    """演示 super() 调试"""
    print("\n=== super() 调试演示 ===")
    
    child = TracedChild("test", 42)
    result = child.method()
    print(f"最终结果: {result}")

# =============================================================================
# 运行演示
# =============================================================================

if __name__ == "__main__":
    # 基础概念
    basics = SuperBasics()
    basics.demonstrate_super_basics()
    
    # 工作机制
    demonstrate_super_mechanism()
    
    # 常见陷阱
    traps = SuperTraps()
    traps.demonstrate_argument_trap()
    traps.demonstrate_method_signature_trap()
    
    # 协作继承
    coop = CooperativeInheritance()
    coop.demonstrate_cooperative_pattern()
    
    # 高级用法
    advanced = AdvancedSuper()
    advanced.demonstrate_explicit_super()
    advanced.demonstrate_super_in_classmethods()
    
    # 最佳实践
    best_practices = SuperBestPractices()
    best_practices.demonstrate_best_practices()
    
    # 调试工具
    demonstrate_super_debugging()