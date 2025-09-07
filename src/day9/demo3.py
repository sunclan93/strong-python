# 类的特殊方法深度应用

from typing import Any, Iterator
import operator

# =============================================================================
# 1. 容器类特殊方法
# =============================================================================

class SmartList:
    """智能列表：演示容器相关的特殊方法"""
    
    def __init__(self, initial_data=None):
        self._data = list(initial_data) if initial_data else []
        self._access_log = []  # 记录访问历史
    
    # 长度和包含检查
    def __len__(self):
        """支持 len(obj)"""
        return len(self._data)
    
    def __contains__(self, item):
        """支持 item in obj"""
        self._access_log.append(f"检查包含: {item}")
        return item in self._data
    
    # 索引访问
    def __getitem__(self, key):
        """支持 obj[key]"""
        self._access_log.append(f"读取索引: {key}")
        return self._data[key]
    
    def __setitem__(self, key, value):
        """支持 obj[key] = value"""
        self._access_log.append(f"设置 [{key}] = {value}")
        self._data[key] = value
    
    def __delitem__(self, key):
        """支持 del obj[key]"""
        self._access_log.append(f"删除索引: {key}")
        del self._data[key]
    
    # 迭代支持
    def __iter__(self):
        """支持 for item in obj"""
        self._access_log.append("开始迭代")
        return iter(self._data)
    
    # 字符串表示
    def __str__(self):
        return f"SmartList({self._data})"
    
    def __repr__(self):
        return f"SmartList({self._data!r})"
    
    # 获取访问日志
    def get_access_log(self):
        return self._access_log.copy()

# =============================================================================
# 2. 运算符重载
# =============================================================================

class Vector:
    """向量类：演示运算符重载"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # 算术运算符
    def __add__(self, other):
        """支持 + 运算"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        """支持 - 运算"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        """支持 * 标量乘法"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __rmul__(self, scalar):
        """支持右侧乘法：3 * vector"""
        return self.__mul__(scalar)
    
    # 比较运算符
    def __eq__(self, other):
        """支持 == 比较"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    
    def __lt__(self, other):
        """支持 < 比较（按向量长度）"""
        if isinstance(other, Vector):
            return self.magnitude() < other.magnitude()
        return NotImplemented
    
    # 辅助方法
    def magnitude(self):
        """计算向量长度"""
        return (self.x ** 2 + self.y ** 2) ** 0.5
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

# =============================================================================
# 3. 上下文管理器和调用
# =============================================================================

class TimedOperation:
    """计时操作：演示上下文管理器和可调用对象"""
    
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
        self.call_count = 0
    
    # 上下文管理器协议
    def __enter__(self):
        import time
        self.start_time = time.time()
        print(f"开始操作: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        import time
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"操作完成: {self.operation_name}，耗时: {duration:.3f}秒")
        return False  # 不抑制异常
    
    # 可调用对象
    def __call__(self, func):
        """作为装饰器使用"""
        def wrapper(*args, **kwargs):
            self.call_count += 1
            with self:
                return func(*args, **kwargs)
        return wrapper
    
    def get_stats(self):
        return {
            'operation': self.operation_name,
            'call_count': self.call_count,
            'last_duration': self.end_time - self.start_time if self.end_time else None
        }

# =============================================================================
# 4. 属性访问控制
# =============================================================================

class ConfigObject:
    """配置对象：演示属性访问控制"""
    
    def __init__(self, **kwargs):
        # 使用私有字典存储实际数据
        object.__setattr__(self, '_data', {})
        object.__setattr__(self, '_readonly', False)
        
        for key, value in kwargs.items():
            self._data[key] = value
    
    def __getattr__(self, name):
        """访问不存在的属性时调用"""
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' 没有属性 '{name}'")
    
    def __setattr__(self, name, value):
        """设置属性时调用"""
        if hasattr(self, '_readonly') and self._readonly:
            raise AttributeError("配置对象是只读的")
        
        if hasattr(self, '_data'):
            self._data[name] = value
        else:
            # 初始化阶段
            object.__setattr__(self, name, value)
    
    def __delattr__(self, name):
        """删除属性时调用"""
        if self._readonly:
            raise AttributeError("配置对象是只读的")
        
        if name in self._data:
            del self._data[name]
        else:
            raise AttributeError(f"'{name}' 属性不存在")
    
    def make_readonly(self):
        """设为只读模式"""
        self._readonly = True
    
    def __str__(self):
        return f"ConfigObject({self._data})"

# =============================================================================
# 演示函数
# =============================================================================

def demonstrate_container_methods():
    """演示容器特殊方法"""
    print("=== 容器特殊方法演示 ===\n")
    
    smart_list = SmartList([1, 2, 3])
    
    # 长度和包含
    print(f"长度: {len(smart_list)}")
    print(f"包含2: {2 in smart_list}")
    
    # 索引操作
    print(f"索引1: {smart_list[1]}")
    smart_list[1] = 99
    print(f"修改后: {smart_list}")
    
    # 迭代
    for item in smart_list:
        print(f"迭代项: {item}")
    
    print(f"访问日志: {smart_list.get_access_log()}")

def demonstrate_operator_overloading():
    """演示运算符重载"""
    print("\n=== 运算符重载演示 ===\n")
    
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    print(f"v1 + v2: {v1 + v2}")
    print(f"v1 - v2: {v1 - v2}")
    print(f"v1 * 2: {v1 * 2}")
    print(f"3 * v1: {3 * v1}")
    print(f"v1 == v2: {v1 == v2}")
    print(f"v1 < v2: {v1 < v2}")

def demonstrate_context_and_callable():
    """演示上下文管理器和可调用对象"""
    print("\n=== 上下文管理器和可调用对象演示 ===\n")
    
    # 作为上下文管理器使用
    with TimedOperation("数据处理") as timer:
        import time
        time.sleep(0.1)  # 模拟操作
    
    # 作为装饰器使用
    data_processor = TimedOperation("函数调用")
    
    @data_processor
    def slow_function():
        import time
        time.sleep(0.05)
        return "处理完成"
    
    result = slow_function()
    print(f"函数结果: {result}")
    print(f"统计信息: {data_processor.get_stats()}")

def demonstrate_attribute_control():
    """演示属性访问控制"""
    print("\n=== 属性访问控制演示 ===\n")
    
    config = ConfigObject(host="localhost", port=8080, debug=True)
    print(f"初始配置: {config}")
    
    # 动态添加属性
    config.database_url = "sqlite:///app.db"
    print(f"添加属性后: {config}")
    
    # 访问属性
    print(f"主机: {config.host}")
    print(f"端口: {config.port}")
    
    # 设为只读
    config.make_readonly()
    try:
        config.port = 9090
    except AttributeError as e:
        print(f"只读错误: {e}")

if __name__ == "__main__":
    demonstrate_container_methods()
    demonstrate_operator_overloading()
    demonstrate_context_and_callable()
    demonstrate_attribute_control()