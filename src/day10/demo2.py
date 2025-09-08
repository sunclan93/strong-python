# Protocol类型提示系统

from typing import Protocol, runtime_checkable, Union, Any, List, Dict
from abc import ABC, abstractmethod

# =============================================================================
# 1. Protocol基础概念
# =============================================================================

class Drawable(Protocol):
    """可绘制对象的协议
    
    Protocol定义了一个"结构化类型"接口
    任何实现了这些方法的类都自动符合这个协议
    """
    
    def draw(self) -> str:
        """绘制方法 - 必须实现"""
        ...
    
    def get_area(self) -> float:
        """获取面积 - 必须实现"""
        ...
    
    # Protocol可以有属性要求
    width: float
    height: float

class Resizable(Protocol):
    """可调整大小对象的协议"""
    
    def resize(self, factor: float) -> None:
        """调整大小"""
        ...
    
    def get_dimensions(self) -> tuple[float, float]:
        """获取尺寸"""
        ...

# =============================================================================
# 2. 实现Protocol的类（鸭子类型）
# =============================================================================

class Rectangle:
    """矩形类 - 自动实现Drawable协议
    
    注意：没有显式继承Drawable，但实现了所需方法
    """
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        """实现Drawable.draw"""
        return f"绘制矩形: {self.width} x {self.height}"
    
    def get_area(self) -> float:
        """实现Drawable.get_area"""
        return self.width * self.height
    
    def resize(self, factor: float) -> None:
        """实现Resizable.resize"""
        self.width *= factor
        self.height *= factor
    
    def get_dimensions(self) -> tuple[float, float]:
        """实现Resizable.get_dimensions"""
        return (self.width, self.height)

class Circle:
    """圆形类 - 也实现了Drawable协议"""
    
    def __init__(self, radius: float):
        self.radius = radius
        # Protocol要求width和height属性
        self.width = radius * 2
        self.height = radius * 2
    
    def draw(self) -> str:
        """实现Drawable.draw"""
        return f"绘制圆形: 半径 {self.radius}"
    
    def get_area(self) -> float:
        """实现Drawable.get_area"""
        return 3.14159 * self.radius ** 2
    
    def resize(self, factor: float) -> None:
        """实现Resizable.resize"""
        self.radius *= factor
        self.width = self.radius * 2
        self.height = self.radius * 2
    
    def get_dimensions(self) -> tuple[float, float]:
        """实现Resizable.get_dimensions"""
        return (self.width, self.height)

class Triangle:
    """三角形类 - 只实现部分协议"""
    
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height
        self.width = base  # 满足Protocol的属性要求
    
    def draw(self) -> str:
        return f"绘制三角形: 底 {self.base}, 高 {self.height}"
    
    def get_area(self) -> float:
        return 0.5 * self.base * self.height
    
    # 注意：Triangle没有实现resize和get_dimensions
    # 所以它符合Drawable协议，但不符合Resizable协议

# =============================================================================
# 3. 使用Protocol进行类型检查的函数
# =============================================================================

def draw_shape(shape: Drawable) -> str:
    """绘制形状函数
    
    参数类型使用Protocol，任何实现了Drawable协议的对象都可以传入
    """
    print(f"形状信息: 宽={shape.width}, 高={shape.height}")
    print(f"面积: {shape.get_area()}")
    return shape.draw()

def resize_shape(shape: Resizable, factor: float) -> tuple[float, float]:
    """调整形状大小
    
    只接受实现了Resizable协议的对象
    """
    print(f"调整前尺寸: {shape.get_dimensions()}")
    shape.resize(factor)
    new_dimensions = shape.get_dimensions()
    print(f"调整后尺寸: {new_dimensions}")
    return new_dimensions

def process_drawable_and_resizable(shape: Union[Drawable, Resizable]) -> Dict[str, Any]:
    """处理既可绘制又可调整大小的形状
    
    这里使用Union类型，展示Protocol的组合使用
    """
    result = {"type": type(shape).__name__}
    
    # 检查是否实现了Drawable协议
    if hasattr(shape, 'draw') and hasattr(shape, 'get_area'):
        result["drawable"] = True
        result["drawing"] = shape.draw()
        result["area"] = shape.get_area()
    else:
        result["drawable"] = False
    
    # 检查是否实现了Resizable协议
    if hasattr(shape, 'resize') and hasattr(shape, 'get_dimensions'):
        result["resizable"] = True
        result["dimensions"] = shape.get_dimensions()
    else:
        result["resizable"] = False
    
    return result

# =============================================================================
# 4. runtime_checkable Protocol
# =============================================================================

@runtime_checkable
class Serializable(Protocol):
    """可序列化协议 - 支持运行时检查
    
    @runtime_checkable 让Protocol支持isinstance()检查
    """
    
    def serialize(self) -> str:
        """序列化为字符串"""
        ...
    
    def deserialize(self, data: str) -> 'Serializable':
        """从字符串反序列化"""
        ...

class User:
    """用户类 - 实现Serializable协议"""
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def serialize(self) -> str:
        """实现序列化"""
        import json
        return json.dumps({"name": self.name, "age": self.age})
    
    def deserialize(self, data: str) -> 'User':
        """实现反序列化"""
        import json
        user_data = json.loads(data)
        return User(user_data["name"], user_data["age"])
    
    def __str__(self):
        return f"User(name={self.name}, age={self.age})"

class Product:
    """产品类 - 没有实现Serializable协议"""
    
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

def handle_serializable_object(obj: Serializable) -> str:
    """处理可序列化对象
    
    使用runtime_checkable Protocol进行运行时检查
    """
    # 运行时检查对象是否符合Protocol
    if isinstance(obj, Serializable):
        print(f"✅ {type(obj).__name__} 实现了Serializable协议")
        return obj.serialize()
    else:
        print(f"❌ {type(obj).__name__} 未实现Serializable协议")
        return ""

# =============================================================================
# 5. Protocol vs ABC对比
# =============================================================================

# ABC方式 - 显式继承
class DrawableABC(ABC):
    """ABC版本的Drawable"""
    
    @abstractmethod
    def draw(self) -> str:
        pass
    
    @abstractmethod
    def get_area(self) -> float:
        pass

class RectangleABC(DrawableABC):
    """必须显式继承DrawableABC"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"ABC矩形: {self.width} x {self.height}"
    
    def get_area(self) -> float:
        return self.width * self.height

# Protocol方式 - 结构化类型（已在上面定义）

def demonstrate_abc_vs_protocol():
    """演示ABC vs Protocol的区别"""
    print("=== ABC vs Protocol 对比 ===\n")
    
    # ABC方式
    abc_rect = RectangleABC(5, 3)
    print(f"ABC矩形: {abc_rect.draw()}")
    print(f"是DrawableABC的实例: {isinstance(abc_rect, DrawableABC)}")
    
    # Protocol方式
    protocol_rect = Rectangle(5, 3)
    print(f"Protocol矩形: {protocol_rect.draw()}")
    print(f"符合Drawable协议: {hasattr(protocol_rect, 'draw') and hasattr(protocol_rect, 'get_area')}")
    
    # 关键区别：Protocol不需要显式继承
    print(f"\nABC需要显式继承: {issubclass(RectangleABC, DrawableABC)}")
    print(f"Protocol基于结构: Rectangle没有继承任何抽象基类")

# =============================================================================
# 6. 演示函数
# =============================================================================

def demonstrate_protocol_basics():
    """演示Protocol基础用法"""
    print("=== Protocol基础演示 ===\n")
    
    # 1. 创建符合协议的对象
    rect = Rectangle(4, 3)
    circle = Circle(2.5)
    triangle = Triangle(4, 3)
    
    shapes = [rect, circle, triangle]
    
    print("1. 测试Drawable协议:")
    for shape in shapes:
        result = draw_shape(shape)  # 所有形状都符合Drawable协议
        print(f"  {result}\n")
    
    # 2. 测试Resizable协议
    print("2. 测试Resizable协议:")
    resizable_shapes = [rect, circle]  # triangle不支持resize
    
    for shape in resizable_shapes:
        print(f"  调整 {type(shape).__name__}:")
        resize_shape(shape, 1.5)
        print()
    
    # 3. 尝试调整不支持resize的形状
    print("3. 尝试调整不支持resize的形状:")
    try:
        resize_shape(triangle, 1.5)  # 这在类型检查时会警告
    except AttributeError as e:
        print(f"  ❌ 错误: {e}")

def demonstrate_runtime_checkable():
    """演示runtime_checkable Protocol"""
    print(f"\n=== Runtime Checkable Protocol演示 ===\n")
    
    user = User("Alice", 25)
    product = Product("Laptop", 999.99)
    
    print("1. 运行时协议检查:")
    objects = [user, product]
    
    for obj in objects:
        print(f"  检查 {type(obj).__name__}:")
        result = handle_serializable_object(obj)
        if result:
            print(f"    序列化结果: {result}")
        print()
    
    # 2. isinstance检查
    print("2. isinstance检查结果:")
    print(f"  user instanceof Serializable: {isinstance(user, Serializable)}")
    print(f"  product instanceof Serializable: {isinstance(product, Serializable)}")

def demonstrate_complex_protocols():
    """演示复杂Protocol用法"""
    print(f"\n=== 复杂Protocol用法演示 ===\n")
    
    rect = Rectangle(4, 3)
    triangle = Triangle(4, 3)
    
    shapes = [rect, triangle]
    
    print("1. 综合协议检查:")
    for shape in shapes:
        result = process_drawable_and_resizable(shape)
        print(f"  {result['type']}:")
        print(f"    可绘制: {result['drawable']}")
        print(f"    可调整: {result['resizable']}")
        if result['drawable']:
            print(f"    绘制: {result['drawing']}")
            print(f"    面积: {result['area']}")
        if result['resizable']:
            print(f"    尺寸: {result['dimensions']}")
        print()

if __name__ == "__main__":
    demonstrate_protocol_basics()
    demonstrate_runtime_checkable()
    demonstrate_complex_protocols()
    demonstrate_abc_vs_protocol()