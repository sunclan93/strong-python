# 依赖注入模式实践

from typing import Protocol, Dict, Any, Optional, Callable, TypeVar, Generic
from abc import ABC, abstractmethod
import inspect
from functools import wraps

# =============================================================================
# 1. 服务接口定义（使用Protocol）
# =============================================================================

class Logger(Protocol):
    """日志服务协议"""
    
    def log(self, level: str, message: str) -> None:
        """记录日志"""
        ...
    
    def debug(self, message: str) -> None:
        """调试日志"""
        ...
    
    def error(self, message: str) -> None:
        """错误日志"""
        ...

class Database(Protocol):
    """数据库服务协议"""
    
    def connect(self) -> bool:
        """连接数据库"""
        ...
    
    def execute(self, query: str) -> Any:
        """执行查询"""
        ...
    
    def close(self) -> None:
        """关闭连接"""
        ...

class Cache(Protocol):
    """缓存服务协议"""
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        ...
    
    def set(self, key: str, value: Any, expire: int = 300) -> None:
        """设置缓存"""
        ...
    
    def delete(self, key: str) -> bool:
        """删除缓存"""
        ...

# =============================================================================
# 2. 具体服务实现
# =============================================================================

class ConsoleLogger:
    """控制台日志实现"""
    
    def __init__(self, level: str = "INFO"):
        self.level = level
    
    def log(self, level: str, message: str) -> None:
        print(f"[{level}] {message}")
    
    def debug(self, message: str) -> None:
        if self.level == "DEBUG":
            self.log("DEBUG", message)
    
    def error(self, message: str) -> None:
        self.log("ERROR", message)

class FileLogger:
    """文件日志实现"""
    
    def __init__(self, filename: str, level: str = "INFO"):
        self.filename = filename
        self.level = level
    
    def log(self, level: str, message: str) -> None:
        # 模拟写入文件
        print(f"写入文件 {self.filename}: [{level}] {message}")
    
    def debug(self, message: str) -> None:
        if self.level == "DEBUG":
            self.log("DEBUG", message)
    
    def error(self, message: str) -> None:
        self.log("ERROR", message)

class SQLiteDatabase:
    """SQLite数据库实现"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connected = False
    
    def connect(self) -> bool:
        print(f"连接到SQLite数据库: {self.db_path}")
        self.connected = True
        return True
    
    def execute(self, query: str) -> Any:
        if not self.connected:
            raise RuntimeError("数据库未连接")
        print(f"执行SQL: {query}")
        return f"结果: {query}"
    
    def close(self) -> None:
        print("关闭SQLite连接")
        self.connected = False

class MemoryCache:
    """内存缓存实现"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
    
    def get(self, key: str) -> Optional[Any]:
        value = self._cache.get(key)
        print(f"缓存获取 {key}: {'命中' if value else '未命中'}")
        return value
    
    def set(self, key: str, value: Any, expire: int = 300) -> None:
        self._cache[key] = value
        print(f"缓存设置 {key} = {value} (过期时间: {expire}s)")
    
    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            print(f"缓存删除 {key}")
            return True
        return False

# =============================================================================
# 3. 依赖注入容器
# =============================================================================

T = TypeVar('T')

class DIContainer:
    """依赖注入容器
    
    管理服务的注册、创建和生命周期
    """
    
    def __init__(self):
        self._services: Dict[str, Any] = {}  # 服务实例
        self._factories: Dict[str, Callable] = {}  # 服务工厂函数
        self._singletons: Dict[str, Any] = {}  # 单例服务
    
    def register(self, name: str, implementation: Any, singleton: bool = True) -> None:
        """注册服务
        
        Args:
            name: 服务名称
            implementation: 服务实现（类或实例）
            singleton: 是否为单例
        """
        if inspect.isclass(implementation):
            # 如果是类，创建工厂函数
            self._factories[name] = implementation
        else:
            # 如果是实例，直接注册
            self._services[name] = implementation
        
        if singleton and name not in self._singletons:
            self._singletons[name] = None
        
        print(f"注册服务: {name} -> {implementation}")
    
    def register_factory(self, name: str, factory: Callable[[], T]) -> None:
        """注册工厂函数"""
        self._factories[name] = factory
        print(f"注册工厂: {name}")
    
    def get(self, name: str) -> Any:
        """获取服务实例"""
        # 1. 检查已注册的实例
        if name in self._services:
            return self._services[name]
        
        # 2. 检查单例
        if name in self._singletons and self._singletons[name] is not None:
            return self._singletons[name]
        
        # 3. 使用工厂创建
        if name in self._factories:
            factory = self._factories[name]
            instance = factory()
            
            # 如果是单例，缓存实例
            if name in self._singletons:
                self._singletons[name] = instance
            
            return instance
        
        raise ValueError(f"服务 '{name}' 未注册")
    
    def resolve_dependencies(self, func: Callable) -> Callable:
        """自动解析函数的依赖注入"""
        sig = inspect.signature(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 检查参数是否需要注入
            bound_args = sig.bind_partial(*args, **kwargs)
            
            for param_name, param in sig.parameters.items():
                if param_name not in bound_args.arguments:
                    # 尝试从容器获取服务
                    try:
                        service = self.get(param_name)
                        bound_args.arguments[param_name] = service
                    except ValueError:
                        # 如果没有对应的服务，跳过
                        pass
            
            bound_args.apply_defaults()
            return func(*bound_args.args, **bound_args.kwargs)
        
        return wrapper

# =============================================================================
# 4. 使用依赖注入的业务类
# =============================================================================

class UserService:
    """用户服务 - 使用依赖注入"""
    
    def __init__(self, logger: Logger, database: Database, cache: Cache):
        self.logger = logger
        self.database = database
        self.cache = cache
        
        # 初始化时连接数据库
        self.database.connect()
        self.logger.log("INFO", "UserService 初始化完成")
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """获取用户信息"""
        self.logger.debug(f"获取用户: {user_id}")
        
        # 1. 先检查缓存
        cache_key = f"user:{user_id}"
        cached_user = self.cache.get(cache_key)
        
        if cached_user:
            self.logger.log("INFO", f"从缓存获取用户 {user_id}")
            return cached_user
        
        # 2. 从数据库查询
        query = f"SELECT * FROM users WHERE id = '{user_id}'"
        db_result = self.database.execute(query)
        
        user_data = {
            "id": user_id,
            "name": f"User_{user_id}",
            "email": f"user{user_id}@example.com"
        }
        
        # 3. 缓存结果
        self.cache.set(cache_key, user_data, expire=600)
        self.logger.log("INFO", f"用户 {user_id} 已缓存")
        
        return user_data
    
    def create_user(self, user_data: Dict[str, Any]) -> bool:
        """创建用户"""
        user_id = user_data.get("id")
        self.logger.log("INFO", f"创建用户: {user_id}")
        
        try:
            # 插入数据库
            query = f"INSERT INTO users VALUES ('{user_id}', '{user_data.get('name')}')"
            self.database.execute(query)
            
            # 清除相关缓存
            cache_key = f"user:{user_id}"
            self.cache.delete(cache_key)
            
            self.logger.log("INFO", f"用户 {user_id} 创建成功")
            return True
            
        except Exception as e:
            self.logger.error(f"创建用户失败: {e}")
            return False

class NotificationService:
    """通知服务 - 依赖于UserService和Logger"""
    
    def __init__(self, user_service: UserService, logger: Logger):
        self.user_service = user_service
        self.logger = logger
        self.logger.log("INFO", "NotificationService 初始化完成")
    
    def send_notification(self, user_id: str, message: str) -> bool:
        """发送通知"""
        self.logger.debug(f"发送通知给用户 {user_id}")
        
        # 获取用户信息
        user = self.user_service.get_user(user_id)
        
        if user:
            # 模拟发送通知
            email = user.get("email")
            self.logger.log("INFO", f"通知已发送到 {email}: {message}")
            return True
        else:
            self.logger.error(f"用户 {user_id} 不存在，无法发送通知")
            return False

# =============================================================================
# 5. 依赖注入装饰器
# =============================================================================

def inject(container: DIContainer):
    """依赖注入装饰器
    
    自动注入函数参数中的依赖服务
    """
    def decorator(func: Callable) -> Callable:
        return container.resolve_dependencies(func)
    
    return decorator

# =============================================================================
# 6. 演示函数
# =============================================================================

def demonstrate_basic_di():
    """演示基础依赖注入"""
    print("=== 基础依赖注入演示 ===\n")
    
    # 1. 创建容器并注册服务
    container = DIContainer()
    
    # 注册服务（单例模式）
    container.register("logger", ConsoleLogger("DEBUG"), singleton=True)
    container.register("database", SQLiteDatabase("app.db"), singleton=True)
    container.register("cache", MemoryCache(), singleton=True)
    
    print("1. 手动依赖注入:")
    
    # 2. 手动获取依赖并创建服务
    logger = container.get("logger")
    database = container.get("database")
    cache = container.get("cache")
    
    user_service = UserService(logger, database, cache)
    
    # 3. 测试业务功能
    user_data = {"id": "001", "name": "Alice", "email": "alice@test.com"}
    user_service.create_user(user_data)
    
    retrieved_user = user_service.get_user("001")
    print(f"获取的用户: {retrieved_user}")
    
    # 再次获取，应该命中缓存
    cached_user = user_service.get_user("001")

def demonstrate_factory_injection():
    """演示工厂注入模式"""
    print(f"\n=== 工厂注入演示 ===\n")
    
    container = DIContainer()
    
    # 使用工厂函数注册服务
    container.register_factory("file_logger", lambda: FileLogger("app.log", "DEBUG"))
    container.register_factory("sqlite_db", lambda: SQLiteDatabase("factory.db"))
    container.register_factory("memory_cache", lambda: MemoryCache())
    
    print("1. 工厂模式创建服务:")
    logger1 = container.get("file_logger")
    logger2 = container.get("file_logger")  # 每次都创建新实例
    
    print(f"logger1 == logger2: {logger1 is logger2}")  # False，不是单例
    
    # 注册为单例
    container.register("singleton_logger", FileLogger, singleton=True)
    
    logger3 = container.get("singleton_logger")
    logger4 = container.get("singleton_logger")  # 返回同一实例
    
    print(f"logger3 == logger4: {logger3 is logger4}")  # True，是单例

def demonstrate_automatic_injection():
    """演示自动依赖注入"""
    print(f"\n=== 自动依赖注入演示 ===\n")
    
    container = DIContainer()
    
    # 注册所有需要的服务
    container.register("logger", ConsoleLogger("INFO"))
    container.register("database", SQLiteDatabase("auto.db"))
    container.register("cache", MemoryCache())
    
    # 注册UserService（会自动注入依赖）
    def create_user_service():
        logger = container.get("logger")
        database = container.get("database")
        cache = container.get("cache")
        return UserService(logger, database, cache)
    
    container.register_factory("user_service", create_user_service)
    
    # 使用装饰器自动注入
    @inject(container)
    def process_user_notification(user_id: str, message: str, user_service: UserService, logger: Logger):
        """自动注入 user_service 和 logger"""
        logger.log("INFO", f"处理用户 {user_id} 的通知")
        
        user = user_service.get_user(user_id)
        if user:
            logger.log("INFO", f"向 {user['email']} 发送: {message}")
            return True
        return False
    
    print("1. 自动依赖注入测试:")
    
    # 创建测试用户
    user_service = container.get("user_service")
    user_service.create_user({"id": "002", "name": "Bob", "email": "bob@test.com"})
    
    # 调用自动注入的函数（不需要手动传入依赖）
    success = process_user_notification("002", "欢迎使用我们的服务！")
    print(f"通知发送成功: {success}")

def demonstrate_service_composition():
    """演示服务组合"""
    print(f"\n=== 服务组合演示 ===\n")
    
    container = DIContainer()
    
    # 注册基础服务
    container.register("logger", ConsoleLogger("INFO"))
    container.register("database", SQLiteDatabase("compose.db"))
    container.register("cache", MemoryCache())
    
    # 注册复合服务
    def create_user_service():
        return UserService(
            container.get("logger"),
            container.get("database"),
            container.get("cache")
        )
    
    def create_notification_service():
        return NotificationService(
            container.get("user_service"),
            container.get("logger")
        )
    
    container.register_factory("user_service", create_user_service)
    container.register_factory("notification_service", create_notification_service)
    
    print("1. 服务组合测试:")
    
    # 获取组合服务
    notification_service = container.get("notification_service")
    
    # 创建用户
    user_service = container.get("user_service")
    user_service.create_user({"id": "003", "name": "Charlie", "email": "charlie@test.com"})
    
    # 发送通知
    success = notification_service.send_notification("003", "系统维护通知")
    print(f"通知服务结果: {success}")

if __name__ == "__main__":
    demonstrate_basic_di()
    demonstrate_factory_injection()
    demonstrate_automatic_injection()
    demonstrate_service_composition()