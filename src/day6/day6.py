# 上下文管理器基础原理与工作机制

import sys
from datetime import datetime

class ContextManagerDemo:
    """上下文管理器协议演示"""
    
    def __init__(self, name):
        self.name = name
        print(f"[创建] {self.name} 上下文管理器")
    
    def __enter__(self):
        """进入上下文时调用"""
        print(f"[进入] {self.name} 上下文 - __enter__ 方法调用")
        print(f"[时间] {datetime.now().strftime('%H:%M:%S')}")
        # 返回值会赋给 as 后的变量
        return f"{self.name}_resource"
    
    def __exit__(self, exc_type, exc_value, traceback):
        """退出上下文时调用"""
        print(f"[退出] {self.name} 上下文 - __exit__ 方法调用")
        print(f"[时间] {datetime.now().strftime('%H:%M:%S')}")
        
        # 异常信息分析
        if exc_type is None:
            print("[状态] 正常退出，无异常")
        else:
            print(f"[异常] 类型: {exc_type.__name__}")
            print(f"[异常] 值: {exc_value}")
            print(f"[异常] 追踪: {traceback}")
            
        # 返回 True 表示异常已处理，False 或 None 表示异常继续传播
        return False  # 让异常继续传播

def with_statement_lifecycle():
    """with 语句的完整生命周期演示"""
    
    print("=== with 语句生命周期演示 ===")
    
    print("\n1. 正常执行流程:")
    try:
        with ContextManagerDemo("正常流程") as resource:
            print(f"[使用] 获得资源: {resource}")
            print("[执行] 在 with 块中进行操作")
            # 正常执行完毕
    except Exception as e:
        print(f"[捕获] 异常: {e}")
    
    print("\n2. 异常处理流程:")
    try:
        with ContextManagerDemo("异常流程") as resource:
            print(f"[使用] 获得资源: {resource}")
            print("[执行] 即将抛出异常...")
            raise ValueError("模拟业务异常")
            print("[执行] 这行代码不会执行")
    except Exception as e:
        print(f"[捕获] 异常: {e}")

class DetailedContextManager:
    """详细的上下文管理器，展示各种场景"""
    
    def __init__(self, name, suppress_exceptions=False):
        self.name = name
        self.suppress_exceptions = suppress_exceptions
        self.start_time = None
        self.resource_acquired = False
    
    def __enter__(self):
        print(f"\n--- {self.name} 开始 ---")
        self.start_time = datetime.now()
        
        # 模拟资源获取
        try:
            print("正在获取资源...")
            self.resource_acquired = True
            print("✓ 资源获取成功")
            return self
        except Exception as e:
            print(f"✗ 资源获取失败: {e}")
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        # 计算执行时间
        if self.start_time:
            duration = datetime.now() - self.start_time
            print(f"执行耗时: {duration.total_seconds():.3f}秒")
        
        # 资源清理
        if self.resource_acquired:
            print("正在释放资源...")
            self.resource_acquired = False
            print("✓ 资源释放完成")
        
        # 异常处理逻辑
        if exc_type:
            print(f"处理异常: {exc_type.__name__}: {exc_value}")
            
            if self.suppress_exceptions:
                print("✓ 异常已被抑制")
                return True  # 抑制异常
            else:
                print("✗ 异常将继续传播")
                return False  # 异常继续传播
        
        print(f"--- {self.name} 结束 ---\n")
        return False

def demonstrate_exception_handling():
    """演示异常处理的不同策略"""
    
    print("=== 异常处理策略演示 ===")
    
    print("1. 不抑制异常的情况:")
    try:
        with DetailedContextManager("不抑制异常") as cm:
            print("执行一些操作...")
            raise RuntimeError("模拟运行时错误")
    except Exception as e:
        print(f"外部捕获到异常: {e}")
    
    print("\n2. 抑制异常的情况:")
    try:
        with DetailedContextManager("抑制异常", suppress_exceptions=True) as cm:
            print("执行一些操作...")
            raise RuntimeError("这个异常会被抑制")
        print("这行会执行，因为异常被抑制了")
    except Exception as e:
        print(f"外部捕获到异常: {e}")

# 多个上下文管理器的组合使用
class ResourceA:
    def __enter__(self):
        print("获取资源 A")
        return "Resource_A"
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("释放资源 A")
        return False

class ResourceB:
    def __enter__(self):
        print("获取资源 B")
        return "Resource_B"
    
    def __exit__(self, exc_type, exc_value, traceback):
        print("释放资源 B")
        return False

def multiple_context_managers():
    """多个上下文管理器的使用"""
    
    print("=== 多个上下文管理器演示 ===")
    
    print("1. 嵌套使用:")
    with ResourceA() as res_a:
        with ResourceB() as res_b:
            print(f"同时使用 {res_a} 和 {res_b}")
    
    print("\n2. 平行使用 (Python 3.1+):")
    with ResourceA() as res_a, ResourceB() as res_b:
        print(f"同时使用 {res_a} 和 {res_b}")
    
    print("\n3. 异常情况下的资源释放:")
    try:
        with ResourceA() as res_a, ResourceB() as res_b:
            print(f"使用 {res_a} 和 {res_b}")
            raise ValueError("模拟异常")
    except ValueError as e:
        print(f"捕获异常: {e}")

# 上下文管理器的实际应用场景
class TimingContext:
    """计时上下文管理器"""
    
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        print(f"开始执行: {self.operation_name}")
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        if exc_type:
            print(f"执行失败: {self.operation_name} (耗时: {duration.total_seconds():.3f}秒)")
        else:
            print(f"执行完成: {self.operation_name} (耗时: {duration.total_seconds():.3f}秒)")
        
        return False

def practical_examples():
    """实际应用示例"""
    
    print("=== 实际应用示例 ===")
    
    import time
    
    # 计时器应用
    with TimingContext("数据处理任务"):
        print("正在处理数据...")
        time.sleep(0.1)  # 模拟处理时间
        print("数据处理完成")
    
    # 异常情况下的计时
    try:
        with TimingContext("可能失败的任务"):
            print("正在执行任务...")
            time.sleep(0.05)
            raise Exception("任务执行失败")
    except Exception as e:
        print(f"任务异常: {e}")

# 运行演示
if __name__ == "__main__":
    # 基础生命周期演示
    with_statement_lifecycle()
    
    print("\n" + "="*50 + "\n")
    
    # 异常处理演示
    demonstrate_exception_handling()
    
    print("\n" + "="*50 + "\n")
    
    # 多个上下文管理器演示
    multiple_context_managers()
    
    print("\n" + "="*50 + "\n")
    
    # 实际应用演示
    practical_examples()