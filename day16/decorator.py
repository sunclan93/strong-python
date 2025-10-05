"""
装饰器模式 - 动态添加功能（不是 Python 的 @decorator）
"""

from abc import ABC, abstractmethod

# ==================== 基础装饰器模式 ====================

class Coffee(ABC):
    """咖啡接口"""
    
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass


class SimpleCoffee(Coffee):
    """基础咖啡"""
    
    def cost(self):
        return 10
    
    def description(self):
        return "简单咖啡"


# 装饰器基类
class CoffeeDecorator(Coffee):
    """装饰器基类"""
    
    def __init__(self, coffee):
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()


# 具体装饰器
class Milk(CoffeeDecorator):
    """牛奶装饰器"""
    
    def cost(self):
        return self._coffee.cost() + 2
    
    def description(self):
        return self._coffee.description() + " + 牛奶"


class Sugar(CoffeeDecorator):
    """糖装饰器"""
    
    def cost(self):
        return self._coffee.cost() + 1
    
    def description(self):
        return self._coffee.description() + " + 糖"


class Chocolate(CoffeeDecorator):
    """巧克力装饰器"""
    
    def cost(self):
        return self._coffee.cost() + 3
    
    def description(self):
        return self._coffee.description() + " + 巧克力"


# 测试
print("装饰器模式 - 咖啡配料")

# 简单咖啡
coffee = SimpleCoffee()
print(f"{coffee.description()}: ¥{coffee.cost()}")

# 加牛奶
coffee = Milk(coffee)
print(f"{coffee.description()}: ¥{coffee.cost()}")

# 再加糖
coffee = Sugar(coffee)
print(f"{coffee.description()}: ¥{coffee.cost()}")

# 再加巧克力
coffee = Chocolate(coffee)
print(f"{coffee.description()}: ¥{coffee.cost()}")


# ==================== 实战：文本处理器 ====================

class TextProcessor(ABC):
    """文本处理器接口"""
    
    @abstractmethod
    def process(self, text):
        pass


class PlainText(TextProcessor):
    """纯文本"""
    
    def process(self, text):
        return text


class TextDecorator(TextProcessor):
    """文本装饰器基类"""
    
    def __init__(self, processor):
        self._processor = processor
    
    def process(self, text):
        return self._processor.process(text)


class BoldDecorator(TextDecorator):
    """加粗装饰器"""
    
    def process(self, text):
        result = self._processor.process(text)
        return f"**{result}**"


class ItalicDecorator(TextDecorator):
    """斜体装饰器"""
    
    def process(self, text):
        result = self._processor.process(text)
        return f"*{result}*"


class UnderlineDecorator(TextDecorator):
    """下划线装饰器"""
    
    def process(self, text):
        result = self._processor.process(text)
        return f"_{result}_"


# 测试
print("\n实战：文本格式化")

text = PlainText()
print(f"原文: {text.process('Hello')}")

text = BoldDecorator(text)
print(f"加粗: {text.process('Hello')}")

text = ItalicDecorator(text)
print(f"加粗+斜体: {text.process('Hello')}")

text = UnderlineDecorator(text)
print(f"全部格式: {text.process('Hello')}")


# ==================== Python 风格的装饰器模式 ====================

class Component:
    """组件"""
    
    def operation(self):
        return "基础操作"


def log_decorator(component):
    """日志装饰"""
    class LogDecorator:
        def __init__(self, comp):
            self.component = comp
        
        def operation(self):
            print("📝 记录日志: 操作开始")
            result = self.component.operation()
            print("📝 记录日志: 操作结束")
            return result
    
    return LogDecorator(component)


def time_decorator(component):
    """计时装饰"""
    class TimeDecorator:
        def __init__(self, comp):
            self.component = comp
        
        def operation(self):
            import time
            start = time.time()
            result = self.component.operation()
            elapsed = time.time() - start
            print(f"⏱️  耗时: {elapsed:.4f}秒")
            return result
    
    return TimeDecorator(component)


# 测试
print("\nPython 风格装饰器")
comp = Component()
comp = log_decorator(comp)
comp = time_decorator(comp)
comp.operation()


print("\n✅ 装饰器模式完成！")