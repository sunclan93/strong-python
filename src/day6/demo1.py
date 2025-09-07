# 自定义上下文管理器的多种实现方式

import contextlib
import threading
import time
import tempfile
import os
from typing import Generator, Any

# 方式1: 基于类的上下文管理器
class DatabaseConnection:
    """模拟数据库连接的上下文管理器"""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.connection = None
        self.transaction_started = False
    
    def __enter__(self):
        """建立连接并开始事务"""
        print(f"连接到数据库: {self.database_url}")
        self.connection = f"connection_to_{self.database_url}"
        
        print("开始事务...")
        self.transaction_started = True
        
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """清理连接和事务"""
        if self.transaction_started:
            if exc_type is None:
                print("提交事务...")
                # 模拟提交操作
            else:
                print(f"回滚事务... (原因: {exc_type.__name__})")
                # 模拟回滚操作
            
            self.transaction_started = False
        
        if self.connection:
            print("关闭数据库连接")
            self.connection = None
        
        # 不抑制异常
        return False
    
    def execute(self, query: str):
        """执行查询"""
        if not self.connection:
            raise RuntimeError("数据库未连接")
        print(f"执行查询: {query}")
        return f"结果_{query}"

# 方式2: 使用 @contextmanager 装饰器
'''
yield 之前的代码 → 相当于 __enter__ 方法
yield 的值 → 相当于 __enter__ 方法的返回值
yield 之后的代码 → 相当于 __exit__ 方法
'''
@contextlib.contextmanager
def file_manager(filename: str, mode: str = 'r'):
    """文件管理上下文管理器"""
    print(f"打开文件: {filename} (模式: {mode})")
    
    try:
        # 模拟文件对象
        file_obj = f"file_object_{filename}"
        yield file_obj  # 这里的值会传给 as 后的变量
    except Exception as e:
        print(f"文件操作异常: {e}")
        raise  # 重新抛出异常
    finally:
        print(f"关闭文件: {filename}")

@contextlib.contextmanager
def temporary_setting(setting_name: str, new_value: Any):
    """临时设置上下文管理器"""
    # 保存原始值
    original_value = globals().get(setting_name, "NOT_SET")
    
    try:
        print(f"临时设置 {setting_name} = {new_value}")
        globals()[setting_name] = new_value
        yield new_value
    finally:
        # 恢复原始值
        if original_value == "NOT_SET":
            if setting_name in globals():
                del globals()[setting_name]
        else:
            globals()[setting_name] = original_value
        print(f"恢复 {setting_name} = {original_value}")

# 方式3: 使用 contextlib.ExitStack 管理多个上下文
def dynamic_context_management():
    """动态上下文管理演示"""
    
    print("=== 动态上下文管理 ===")
    
    # 使用 ExitStack 管理多个上下文
    # 1. 执行 callback（打印"ExitStack 清理回调执行"）
    # 2. 关闭 db2 连接（如果存在）
    # 3. 关闭 db1 连接
    with contextlib.ExitStack() as stack:
        # 动态添加上下文管理器
        db1 = stack.enter_context(DatabaseConnection("db1.sqlite"))
        
        # 条件性添加上下文管理器
        if True:  # 某个条件
            db2 = stack.enter_context(DatabaseConnection("db2.sqlite"))
        
        # 添加清理函数
        stack.callback(lambda: print("ExitStack 清理回调执行"))
        
        print("执行数据库操作...")
        db1.execute("SELECT * FROM users")
        if 'db2' in locals():
            db2.execute("SELECT * FROM products")
        
# 高级上下文管理器：锁管理器
class SmartLock:
    """智能锁上下文管理器"""
    
    def __init__(self, name: str, timeout: float = 5.0):
        self.name = name
        self.timeout = timeout
        self.lock = threading.Lock()
        self.acquired = False
    
    def __enter__(self):
        print(f"尝试获取锁: {self.name}")
        
        # 尝试在超时时间内获取锁
        if self.lock.acquire(timeout=self.timeout):
            self.acquired = True
            print(f"✓ 成功获取锁: {self.name}")
            return self
        else:
            raise TimeoutError(f"获取锁超时: {self.name}")
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.acquired:
            self.lock.release()
            self.acquired = False
            print(f"✓ 释放锁: {self.name}")
        
        return False

# 嵌套上下文管理器
class NestedResource:
    """支持嵌套的资源管理器"""
    
    def __init__(self, name: str):
        self.name = name
        self.depth = 0
    
    def __enter__(self):
        self.depth += 1
        print(f"{'  ' * (self.depth-1)}进入 {self.name} (深度: {self.depth})")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(f"{'  ' * (self.depth-1)}退出 {self.name} (深度: {self.depth})")
        self.depth -= 1
        return False

# 资源池管理器
class ResourcePool:
    """资源池上下文管理器"""
    
    def __init__(self, max_size: int = 5):
        self.max_size = max_size
        self.pool = []
        self.in_use = set()
        self.lock = threading.Lock()
        
        # 初始化资源池
        for i in range(max_size):
            self.pool.append(f"Resource_{i}")
    
    @contextlib.contextmanager
    def get_resource(self):
        """获取资源的上下文管理器"""
        resource = None
        
        try:
            with self.lock:
                if not self.pool:
                    raise RuntimeError("资源池已耗尽")
                
                resource = self.pool.pop()
                self.in_use.add(resource)
                print(f"从池中获取资源: {resource}")
            
            yield resource
            
        finally:
            if resource:
                with self.lock:
                    self.in_use.discard(resource)
                    self.pool.append(resource)
                    print(f"归还资源到池: {resource}")

# 异步上下文管理器（Python 3.5+）
class AsyncContextManager:
    """异步上下文管理器演示"""
    
    def __init__(self, name: str):
        self.name = name
    
    async def __aenter__(self):
        print(f"异步进入: {self.name}")
        # 模拟异步操作
        await self.async_setup()
        return self
    
    async def __aexit__(self, exc_type, exc_value, traceback):
        print(f"异步退出: {self.name}")
        # 模拟异步清理
        await self.async_cleanup()
        return False
    
    async def async_setup(self):
        """模拟异步设置"""
        print("执行异步设置...")
        # 在实际应用中，这里可能是网络请求、数据库连接等
    
    async def async_cleanup(self):
        """模拟异步清理"""
        print("执行异步清理...")

# 上下文管理器的装饰器模式
def context_manager_decorator(setup_func, cleanup_func):
    """将函数转换为上下文管理器的装饰器"""
    
    def decorator(func):
        @contextlib.contextmanager
        def wrapper(*args, **kwargs):
            # 设置阶段
            resource = setup_func() if setup_func else None
            
            try:
                # 执行被装饰的函数
                if resource:
                    yield func(resource, *args, **kwargs)
                else:
                    yield func(*args, **kwargs)
            finally:
                # 清理阶段
                if cleanup_func and resource:
                    cleanup_func(resource)
        
        return wrapper
    return decorator

# 运行演示
def demonstrate_custom_context_managers():
    """演示各种自定义上下文管理器"""
    
    print("=== 自定义上下文管理器演示 ===")
    
    print("\n1. 基于类的数据库连接:")
    try:
        with DatabaseConnection("postgresql://localhost/mydb") as db:
            db.execute("CREATE TABLE users...")
            db.execute("INSERT INTO users...")
            # 模拟异常
            # raise ValueError("数据验证失败")
    except Exception as e:
        print(f"数据库操作异常: {e}")
    
    print("\n2. 基于生成器的文件管理:")
    with file_manager("data.txt", "w") as f:
        print(f"使用文件对象: {f}")
    
    print("\n3. 临时设置管理:")
    DEBUG = True
    print(f"原始 DEBUG = {DEBUG}")
    
    with temporary_setting("DEBUG", False):
        print(f"临时 DEBUG = {DEBUG}")
    
    print(f"恢复后 DEBUG = {DEBUG}")
    
    print("\n4. 智能锁管理:")
    lock = SmartLock("critical_section")
    
    with lock:
        print("在锁保护的代码块中执行...")
        time.sleep(0.1)
    
    print("\n5. 嵌套资源管理:")
    resource = NestedResource("主资源")
    
    with resource:
        print("在第一层...")
        with resource:
            print("在第二层...")
            with resource:
                print("在第三层...")
    
    print("\n6. 资源池管理:")
    pool = ResourcePool(max_size=3)
    
    with pool.get_resource() as res1:
        print(f"使用资源: {res1}")
        
        with pool.get_resource() as res2:
            print(f"同时使用资源: {res2}")
    
    print("\n7. 动态上下文管理:")
    dynamic_context_management()

# 高级技巧：上下文管理器的链式组合
class ChainableContext:
    """可链式组合的上下文管理器"""
    
    def __init__(self, name: str):
        self.name = name
        self.next_context = None
    
    def __enter__(self):
        print(f"进入: {self.name}")
        if self.next_context:
            self.next_context.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.next_context:
            result = self.next_context.__exit__(exc_type, exc_value, traceback)
        print(f"退出: {self.name}")
        return False
    
    def chain(self, other):
        """链式组合"""
        self.next_context = other
        return self

if __name__ == "__main__":
    demonstrate_custom_context_managers()
    
    print("\n" + "="*50)
    print("\n8. 链式上下文管理器:")
    
    ctx1 = ChainableContext("Context1")
    ctx2 = ChainableContext("Context2")
    ctx3 = ChainableContext("Context3")
    
    with ctx1.chain(ctx2).chain(ctx3):
        print("在链式上下文中执行...")