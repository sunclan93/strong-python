# MRO (Method Resolution Order) 方法解析顺序深度理解

import inspect
from typing import Type, List, Set

# =============================================================================
# 1. C3线性化算法理解
# =============================================================================

class MROAnalyzer:
    """MRO分析器 - 理解C3线性化算法"""
    
    @staticmethod
    def show_mro(cls: Type) -> None:
        """显示类的MRO"""
        print(f"\n=== {cls.__name__} 的 MRO ===")
        for i, c in enumerate(cls.__mro__):
            print(f"{i}: {c.__name__} ({c.__module__})")
    
    @staticmethod
    def analyze_inheritance_tree(cls: Type) -> None:
        """分析继承树结构"""
        print(f"\n=== {cls.__name__} 继承树分析 ===")
        
        def print_tree(c: Type, level: int = 0):
            indent = "  " * level
            print(f"{indent}{c.__name__}")
            for base in c.__bases__:
                print_tree(base, level + 1)
        
        print("继承树结构:")
        print_tree(cls)
        
        print(f"\nC3线性化结果: {' -> '.join(c.__name__ for c in cls.__mro__)}")
    
    @staticmethod
    def compare_mro_methods(cls: Type, method_name: str) -> None:
        """比较MRO中各类的同名方法"""
        print(f"\n=== 方法 '{method_name}' 在MRO中的分布 ===")
        
        for i, c in enumerate(cls.__mro__):
            if hasattr(c, method_name):
                method = getattr(c, method_name)
                if method_name in c.__dict__:  # 直接定义在这个类中
                    print(f"{i}: {c.__name__}.{method_name} ✓ (直接定义)")
                else:
                    print(f"{i}: {c.__name__}.{method_name} (继承)")
            else:
                print(f"{i}: {c.__name__} (无此方法)")

# =============================================================================
# 2. 简单继承示例
# =============================================================================

class A:
    def method(self):
        return "A.method"
    
    def a_only(self):
        return "A.a_only"

class B(A):
    def method(self):
        return "B.method"
    
    def b_only(self):
        return "B.b_only"

class C(A):
    def method(self):
        return "C.method"
    
    def c_only(self):
        return "C.c_only"

class D(B, C):  # 多重继承
    def d_only(self):
        return "D.d_only"

def demonstrate_simple_mro():
    """演示简单MRO情况"""
    print("=== 简单MRO演示 ===")
    
    MROAnalyzer.show_mro(D)
    MROAnalyzer.analyze_inheritance_tree(D)
    MROAnalyzer.compare_mro_methods(D, 'method')
    
    # 测试方法调用
    d = D()
    print(f"\nd.method() 调用结果: {d.method()}")
    print("解释: 根据MRO，D -> B -> C -> A，所以调用B.method")

# =============================================================================
# 3. 复杂继承：钻石继承问题
# =============================================================================

class Animal:
    """动物基类"""
    def __init__(self, name):
        self.name = name
        print(f"Animal.__init__: {name}")
    
    def speak(self):
        return f"{self.name} makes a sound"
    
    def move(self):
        return f"{self.name} moves"

class Mammal(Animal):
    """哺乳动物"""
    def __init__(self, name, fur_color="brown"):
        print(f"Mammal.__init__: {name}, fur_color={fur_color}")
        super().__init__(name)
        self.fur_color = fur_color
    
    def speak(self):
        return f"{self.name} makes mammal sounds"
    
    def nurse_young(self):
        return f"{self.name} nurses young"

class Flyer(Animal):
    """飞行动物"""
    def __init__(self, name, wing_span=1.0):
        print(f"Flyer.__init__: {name}, wing_span={wing_span}")
        super().__init__(name)
        self.wing_span = wing_span
    
    def speak(self):
        return f"{self.name} makes flying sounds"
    
    def fly(self):
        return f"{self.name} flies with {self.wing_span}m wingspan"

class Bat(Mammal, Flyer):
    """蝙蝠：既是哺乳动物又是飞行动物"""
    def __init__(self, name, fur_color="black", wing_span=0.3):
        print(f"Bat.__init__: {name}")
        # 注意：这里的super()调用顺序很重要
        super().__init__(name, fur_color=fur_color)
        self.wing_span = wing_span  # 重新设置翼展
    
    def speak(self):
        return f"{self.name} screeches"
    
    def echolocate(self):
        return f"{self.name} uses echolocation"

def demonstrate_diamond_inheritance():
    """演示钻石继承问题"""
    print("\n=== 钻石继承演示 ===")
    
    MROAnalyzer.show_mro(Bat)
    MROAnalyzer.analyze_inheritance_tree(Bat)
    
    print("\n创建蝙蝠实例:")
    try:
        bat = Bat("Batman", fur_color="dark", wing_span=0.5)
        print(f"蝙蝠创建成功: {bat.name}")
        print(f"毛色: {bat.fur_color}")
        print(f"翼展: {bat.wing_span}")
        
        print(f"\n能力测试:")
        print(f"发声: {bat.speak()}")
        print(f"飞行: {bat.fly()}")
        print(f"哺育: {bat.nurse_young()}")
        print(f"回声定位: {bat.echolocate()}")
        
    except Exception as e:
        print(f"创建失败: {e}")
        print("这说明了多重继承中__init__方法调用的复杂性")

# =============================================================================
# 4. MRO冲突和解决方案
# =============================================================================

class Base:
    def method(self):
        return "Base"

class Left(Base):
    def method(self):
        return "Left"

class Right(Base):
    def method(self):
        return "Right"

# 这会导致MRO冲突
try:
    class Conflict(Left, Right, Base):  # 错误的继承顺序
        pass
except TypeError as e:
    print(f"\nMRO冲突示例: {e}")

# 正确的解决方案
class Resolved(Left, Right):  # 移除冗余的Base
    def method(self):
        # 可以显式调用特定父类的方法
        left_result = Left.method(self)
        right_result = Right.method(self)
        return f"Resolved: {left_result} + {right_result}"

def demonstrate_mro_conflicts():
    """演示MRO冲突和解决方案"""
    print("\n=== MRO冲突和解决方案 ===")
    
    MROAnalyzer.show_mro(Resolved)
    
    resolved = Resolved()
    print(f"\nresolved.method(): {resolved.method()}")

# =============================================================================
# 5. 实际应用：混入(Mixin)模式
# =============================================================================

class LoggingMixin:
    """日志混入类"""
    def log(self, message):
        class_name = self.__class__.__name__
        print(f"[{class_name}] {message}")

class ValidatorMixin:
    """验证混入类"""
    def validate(self, data):
        # 简单验证逻辑
        if not data:
            raise ValueError("数据不能为空")
        self.log(f"验证通过: {data}")
        return True

class CacheMixin:
    """缓存混入类"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}
    
    def get_cached(self, key):
        if key in self._cache:
            self.log(f"缓存命中: {key}")
            return self._cache[key]
        return None
    
    def set_cache(self, key, value):
        self._cache[key] = value
        self.log(f"缓存设置: {key} = {value}")

class DataProcessor(LoggingMixin, ValidatorMixin, CacheMixin):
    """数据处理器 - 使用多个混入"""
    def __init__(self, name):
        super().__init__()  # 重要：调用父类初始化
        self.name = name
        self.log(f"数据处理器 {name} 初始化完成")
    
    def process(self, data):
        # 检查缓存
        cached_result = self.get_cached(data)
        if cached_result:
            return cached_result
        
        # 验证数据
        self.validate(data)
        
        # 处理数据
        result = data.upper()  # 简单处理
        self.log(f"数据处理完成: {data} -> {result}")
        
        # 缓存结果
        self.set_cache(data, result)
        
        return result

def demonstrate_mixin_pattern():
    """演示混入模式"""
    print("\n=== 混入(Mixin)模式演示 ===")
    
    MROAnalyzer.show_mro(DataProcessor)
    
    processor = DataProcessor("处理器1")
    
    print(f"\n处理数据:")
    result1 = processor.process("hello")
    print(f"结果1: {result1}")
    
    result2 = processor.process("hello")  # 应该命中缓存
    print(f"结果2: {result2}")
    
    try:
        processor.process("")  # 应该验证失败
    except ValueError as e:
        print(f"验证失败: {e}")

# =============================================================================
# 6. MRO调试工具
# =============================================================================

class MRODebugger:
    """MRO调试工具"""
    
    @staticmethod
    def find_method_source(cls: Type, method_name: str) -> None:
        """查找方法的真实来源"""
        print(f"\n=== 查找 {cls.__name__}.{method_name} 的来源 ===")
        
        if not hasattr(cls, method_name):
            print(f"类 {cls.__name__} 没有方法 {method_name}")
            return
        
        method = getattr(cls, method_name)
        
        # 在MRO中查找定义源
        for i, c in enumerate(cls.__mro__):
            if method_name in c.__dict__:
                print(f"找到定义: {c.__name__}.{method_name} (MRO位置: {i})")
                
                # 显示方法签名
                try:
                    sig = inspect.signature(c.__dict__[method_name])
                    print(f"方法签名: {method_name}{sig}")
                except (ValueError, TypeError):
                    print(f"无法获取方法签名")
                
                # 显示源码（如果可能）
                try:
                    source = inspect.getsource(c.__dict__[method_name])
                    print(f"源码:")
                    for i, line in enumerate(source.split('\n')[:5], 1):
                        print(f"  {i}: {line}")
                    if len(source.split('\n')) > 5:
                        print("  ...")
                except (OSError, TypeError):
                    print("无法获取源码")
                
                break
        else:
            print(f"在MRO中未找到 {method_name} 的定义")
    
    @staticmethod
    def method_resolution_trace(cls: Type, method_name: str) -> None:
        """跟踪方法解析过程"""
        print(f"\n=== {cls.__name__}.{method_name} 解析跟踪 ===")
        
        for i, c in enumerate(cls.__mro__):
            has_method = hasattr(c, method_name)
            defined_here = method_name in c.__dict__
            
            if defined_here:
                print(f"{i}: {c.__name__} ✓✓ (定义在此)")
                break
            elif has_method:
                print(f"{i}: {c.__name__} ✓ (继承)")
            else:
                print(f"{i}: {c.__name__} ✗ (无此方法)")

# =============================================================================
# 运行演示
# =============================================================================

if __name__ == "__main__":
    # 简单MRO演示
    demonstrate_simple_mro()
    
    # 钻石继承演示
    demonstrate_diamond_inheritance()
    
    # MRO冲突演示
    demonstrate_mro_conflicts()
    
    # 混入模式演示
    demonstrate_mixin_pattern()
    
    # MRO调试工具演示
    MRODebugger.find_method_source(DataProcessor, 'log')
    MRODebugger.method_resolution_trace(Bat, 'speak')