# ABC抽象基类深度应用

from abc import ABC, abstractmethod, abstractproperty, abstractclassmethod, abstractstaticmethod
from typing import Any, Dict, List, Optional, Union
import inspect

# =============================================================================
# 1. 基础抽象类定义
# =============================================================================

class DataProcessor(ABC):
    """数据处理器抽象基类
    
    定义了所有数据处理器必须实现的接口
    """
    
    def __init__(self, name: str):
        self.name = name
        self._processed_count = 0
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """抽象方法：处理数据
        
        Args:
            data: 要处理的数据
            
        Returns:
            处理后的数据
            
        子类必须实现这个方法，否则无法实例化
        """
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """抽象方法：验证数据
        
        Args:
            data: 要验证的数据
            
        Returns:
            验证结果
        """
        pass
    
    # 抽象属性 - Python 3.9+ 推荐使用 @property + @abstractmethod
    @property
    @abstractmethod
    def supported_types(self) -> List[type]:
        """抽象属性：支持的数据类型
        
        子类必须实现这个属性
        """
        pass
    
    @property
    @abstractmethod
    def max_size(self) -> int:
        """抽象属性：最大处理大小"""
        pass
    
    # 具体方法 - 子类可以直接使用
    def get_stats(self) -> Dict[str, Any]:
        """获取处理统计信息
        
        这是具体方法，子类可以直接使用或重写
        """
        return {
            'name': self.name,
            'processed_count': self._processed_count,
            'supported_types': [t.__name__ for t in self.supported_types]
        }
    
    def safe_process(self, data: Any) -> Optional[Any]:
        """安全处理方法
        
        先验证再处理，提供通用的错误处理逻辑
        """
        try:
            if not self.validate(data):
                raise ValueError(f"数据验证失败: {data}")
            
            result = self.process(data)
            self._processed_count += 1
            return result
            
        except Exception as e:
            print(f"处理失败 [{self.name}]: {e}")
            return None

# =============================================================================
# 2. 具体实现类
# =============================================================================

class TextProcessor(DataProcessor):
    """文本处理器 - DataProcessor的具体实现
    
    专门处理字符串数据
    """
    
    def __init__(self, name: str, transform_type: str = "upper"):
        super().__init__(name)
        self.transform_type = transform_type
    
    def process(self, data: Any) -> Any:
        """实现抽象方法：处理文本数据"""
        if not isinstance(data, str):
            raise TypeError(f"TextProcessor只能处理字符串，得到: {type(data)}")
        
        # 根据转换类型处理文本
        transforms = {
            "upper": data.upper,
            "lower": data.lower,
            "title": data.title,
            "reverse": lambda: data[::-1]
        }
        
        transform_func = transforms.get(self.transform_type, data.upper)
        return transform_func()
    
    def validate(self, data: Any) -> bool:
        """实现抽象方法：验证是否为字符串"""
        return isinstance(data, str) and len(data) <= self.max_size
    
    @property
    def supported_types(self) -> List[type]:
        """实现抽象属性：支持的类型"""
        return [str]
    
    @property  
    def max_size(self) -> int:
        """实现抽象属性：最大字符串长度"""
        return 1000

class NumberProcessor(DataProcessor):
    """数字处理器 - DataProcessor的另一个实现
    
    专门处理数字数据
    """
    
    def __init__(self, name: str, operation: str = "square"):
        super().__init__(name)
        self.operation = operation
    
    def process(self, data: Any) -> Any:
        """实现抽象方法：处理数字数据"""
        if not isinstance(data, (int, float)):
            raise TypeError(f"NumberProcessor只能处理数字，得到: {type(data)}")
        
        operations = {
            "square": lambda x: x ** 2,
            "sqrt": lambda x: x ** 0.5,
            "double": lambda x: x * 2,
            "negate": lambda x: -x
        }
        
        operation_func = operations.get(self.operation, lambda x: x)
        return operation_func(data)
    
    def validate(self, data: Any) -> bool:
        """实现抽象方法：验证是否为数字"""
        return isinstance(data, (int, float)) and abs(data) <= self.max_size
    
    @property
    def supported_types(self) -> List[type]:
        """实现抽象属性：支持的类型"""
        return [int, float]
    
    @property
    def max_size(self) -> int:
        """实现抽象属性：最大数字大小"""
        return 1000000

# =============================================================================
# 3. 抽象类的高级用法
# =============================================================================

class ConfigurableProcessor(DataProcessor):
    """可配置处理器 - 演示抽象类的高级用法"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        super().__init__(name)
        self.config = config
        
        # 验证必需的配置项
        required_configs = self.get_required_configs()
        missing = [key for key in required_configs if key not in config]
        if missing:
            raise ValueError(f"缺少必需配置: {missing}")
    
    @abstractmethod
    def get_required_configs(self) -> List[str]:
        """抽象方法：获取必需的配置项
        
        每个子类都必须声明自己需要哪些配置
        """
        pass
    
    @abstractmethod
    def process(self, data: Any) -> Any:
        """仍然是抽象方法，子类必须实现"""
        pass
    
    def validate(self, data: Any) -> bool:
        """默认验证逻辑，子类可以重写"""
        return data is not None

class EmailProcessor(ConfigurableProcessor):
    """邮件处理器 - ConfigurableProcessor的实现"""
    
    def get_required_configs(self) -> List[str]:
        """实现抽象方法：声明需要的配置"""
        return ["smtp_server", "port", "username"]
    
    def process(self, data: Any) -> Any:
        """实现抽象方法：发送邮件"""
        if not isinstance(data, dict) or "to" not in data:
            raise ValueError("邮件数据必须包含'to'字段")
        
        # 模拟发送邮件
        smtp_server = self.config["smtp_server"]
        port = self.config["port"]
        
        result = {
            "status": "sent",
            "to": data["to"],
            "server": f"{smtp_server}:{port}",
            "subject": data.get("subject", "No Subject")
        }
        
        return result
    
    def validate(self, data: Any) -> bool:
        """重写验证逻辑"""
        return (isinstance(data, dict) and 
                "to" in data and 
                "@" in str(data["to"]))
    
    @property
    def supported_types(self) -> List[type]:
        return [dict]
    
    @property
    def max_size(self) -> int:
        return 10000  # 10KB 邮件大小限制

# =============================================================================
# 4. 抽象类注册机制
# =============================================================================

class ProcessorRegistry:
    """处理器注册表
    
    管理所有DataProcessor的子类
    """
    
    _processors: Dict[str, type] = {}
    
    @classmethod
    def register(cls, name: str, processor_class: type):
        """注册处理器类"""
        if not issubclass(processor_class, DataProcessor):
            raise TypeError(f"{processor_class} 必须是 DataProcessor 的子类")
        
        if inspect.isabstract(processor_class):
            raise TypeError(f"{processor_class} 是抽象类，无法注册")
        
        cls._processors[name] = processor_class
        print(f"注册处理器: {name} -> {processor_class.__name__}")
    
    @classmethod
    def create_processor(cls, name: str, *args, **kwargs) -> DataProcessor:
        """创建处理器实例"""
        if name not in cls._processors:
            raise ValueError(f"未注册的处理器: {name}")
        
        processor_class = cls._processors[name]
        return processor_class(*args, **kwargs)
    
    @classmethod
    def list_processors(cls) -> List[str]:
        """列出所有注册的处理器"""
        return list(cls._processors.keys())
    
    @classmethod
    def get_processor_info(cls, name: str) -> Dict[str, Any]:
        """获取处理器信息"""
        if name not in cls._processors:
            raise ValueError(f"未注册的处理器: {name}")
        
        processor_class = cls._processors[name]
        
        # 通过创建临时实例获取信息（如果有默认构造参数）
        try:
            # 尝试创建实例来获取属性信息
            temp_instance = processor_class("temp")
            supported_types = temp_instance.supported_types
            max_size = temp_instance.max_size
        except:
            supported_types = "Unknown"
            max_size = "Unknown"
        
        return {
            "name": name,
            "class": processor_class.__name__,
            "module": processor_class.__module__,
            "supported_types": supported_types,
            "max_size": max_size,
            "is_abstract": inspect.isabstract(processor_class)
        }

# =============================================================================
# 5. 演示函数
# =============================================================================

def demonstrate_abstract_classes():
    """演示抽象基类的使用"""
    print("=== ABC抽象基类演示 ===\n")
    
    # 1. 尝试实例化抽象类（会失败）
    print("1. 尝试实例化抽象类:")
    try:
        processor = DataProcessor("test")  # 这会报错
    except TypeError as e:
        print(f"❌ 预期错误: {e}")
    
    # 2. 创建具体实现
    print(f"\n2. 创建具体实现:")
    text_proc = TextProcessor("文本处理器", "upper")
    number_proc = NumberProcessor("数字处理器", "square")
    
    print(f"✅ 创建成功: {text_proc.name}")
    print(f"✅ 创建成功: {number_proc.name}")
    
    # 3. 测试抽象方法的实现
    print(f"\n3. 测试处理功能:")
    
    # 文本处理
    text_result = text_proc.safe_process("hello world")
    print(f"文本处理结果: '{text_result}'")
    
    # 数字处理
    number_result = number_proc.safe_process(5)
    print(f"数字处理结果: {number_result}")
    
    # 4. 测试抽象属性
    print(f"\n4. 抽象属性信息:")
    print(f"文本处理器支持类型: {text_proc.supported_types}")
    print(f"文本处理器最大大小: {text_proc.max_size}")
    print(f"数字处理器支持类型: {number_proc.supported_types}")
    print(f"数字处理器最大大小: {number_proc.max_size}")
    
    # 5. 测试类型检查
    print(f"\n5. 类型检查:")
    print(f"text_proc 是 DataProcessor: {isinstance(text_proc, DataProcessor)}")
    print(f"number_proc 是 DataProcessor: {isinstance(number_proc, DataProcessor)}")

def demonstrate_configurable_processor():
    """演示可配置处理器"""
    print(f"\n=== 可配置处理器演示 ===\n")
    
    # 1. 正确配置
    print("1. 正确配置:")
    email_config = {
        "smtp_server": "smtp.gmail.com",
        "port": 587,
        "username": "test@gmail.com"
    }
    
    email_proc = EmailProcessor("邮件处理器", email_config)
    print(f"✅ 邮件处理器创建成功")
    
    # 2. 测试邮件处理
    email_data = {
        "to": "user@example.com",
        "subject": "测试邮件",
        "body": "这是一个测试邮件"
    }
    
    result = email_proc.safe_process(email_data)
    print(f"邮件发送结果: {result}")
    
    # 3. 缺少配置的情况
    print(f"\n2. 缺少配置的情况:")
    try:
        bad_config = {"smtp_server": "smtp.gmail.com"}  # 缺少 port 和 username
        bad_proc = EmailProcessor("错误处理器", bad_config)
    except ValueError as e:
        print(f"❌ 预期错误: {e}")

def demonstrate_processor_registry():
    """演示处理器注册机制"""
    print(f"\n=== 处理器注册机制演示 ===\n")
    
    # 1. 注册处理器
    print("1. 注册处理器:")
    ProcessorRegistry.register("text", TextProcessor)
    ProcessorRegistry.register("number", NumberProcessor)
    
    # 2. 列出注册的处理器
    print(f"\n2. 已注册的处理器:")
    processors = ProcessorRegistry.list_processors()
    for proc_name in processors:
        print(f"  - {proc_name}")
    
    # 3. 动态创建处理器
    print(f"\n3. 动态创建处理器:")
    dynamic_text_proc = ProcessorRegistry.create_processor("text", "动态文本处理器", "title")
    dynamic_number_proc = ProcessorRegistry.create_processor("number", "动态数字处理器", "sqrt")
    
    # 测试动态创建的处理器
    result1 = dynamic_text_proc.safe_process("hello world")
    result2 = dynamic_number_proc.safe_process(16)
    
    print(f"动态文本处理结果: '{result1}'")
    print(f"动态数字处理结果: {result2}")
    
    # 4. 获取处理器信息
    print(f"\n4. 处理器详细信息:")
    for proc_name in processors:
        try:
            info = ProcessorRegistry.get_processor_info(proc_name)
            print(f"  {proc_name}: {info}")
        except Exception as e:
            print(f"  {proc_name}: 信息获取失败 - {e}")

if __name__ == "__main__":
    demonstrate_abstract_classes()
    demonstrate_configurable_processor()
    demonstrate_processor_registry()