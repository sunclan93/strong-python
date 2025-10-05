"""
单例模式 - 3种实现方式
"""

# ==================== 方式1: 元类实现（推荐）====================

class SingletonMeta(type):
    """单例元类"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("🔌 连接数据库")
        self.connection = "MySQL Connection"


# 测试
print("方式1: 元类实现")
db1 = Database()
db2 = Database()
print(f"db1 is db2: {db1 is db2}")  # True


# ==================== 方式2: 装饰器实现 ====================

def singleton(cls):
    """单例装饰器"""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance


@singleton
class Logger:
    def __init__(self):
        print("📝 初始化日志")
        self.logs = []
    
    def log(self, msg):
        self.logs.append(msg)


# 测试
print("\n方式2: 装饰器实现")
log1 = Logger()
log1.log("消息1")
log2 = Logger()
print(f"log1 is log2: {log1 is log2}")  # True
print(f"log2.logs: {log2.logs}")  # ['消息1']


# ==================== 方式3: __new__ 方法 ====================

class Cache:
    """缓存单例"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("💾 创建缓存实例")
            cls._instance = super().__new__(cls)
            cls._instance.data = {}
        return cls._instance
    
    def set(self, key, value):
        self.data[key] = value
    
    def get(self, key):
        return self.data.get(key)


# 测试
print("\n方式3: __new__ 方法")
cache1 = Cache()
cache1.set('user', 'Alice')
cache2 = Cache()
print(f"cache1 is cache2: {cache1 is cache2}")  # True
print(f"cache2.get('user'): {cache2.get('user')}")  # Alice


# ==================== 实战：配置管理器 ====================

class Config(metaclass=SingletonMeta):
    """全局配置管理器"""
    
    def __init__(self):
        self._config = {
            'debug': False,
            'host': 'localhost',
            'port': 5000
        }
    
    def get(self, key, default=None):
        return self._config.get(key, default)
    
    def set(self, key, value):
        self._config[key] = value
        print(f"⚙️  设置配置: {key} = {value}")
    
    def all(self):
        return self._config.copy()


# 测试配置管理器
print("\n实战示例：配置管理器")
config = Config()
config.set('debug', True)
config.set('port', 8000)

# 在另一个模块中获取配置
config2 = Config()
print(f"调试模式: {config2.get('debug')}")
print(f"所有配置: {config2.all()}")


print("\n✅ 单例模式学习完成！")