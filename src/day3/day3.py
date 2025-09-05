"""
第一周 Day 3：装饰器原理与高级应用
学习目标：深入理解装饰器的工作原理，掌握高级装饰器设计

今日重点：
1. 函数是第一类对象的深层理解
2. 装饰器的工作原理和执行时机
3. 带参数装饰器的实现
4. 类装饰器 vs 函数装饰器
5. functools.wraps 的作用和使用
"""

import time
import functools
from typing import Any, Callable, Dict, List
from datetime import datetime
import threading
import warnings


# ==== 第一部分：函数是第一类对象 ====
print("=== 函数是第一类对象 ===\n")

def demonstrate_function_as_object():
    """演示函数作为第一类对象的特性"""
    
    def greet(name):
        """一个简单的函数"""
        return f"Hello, {name}!"
    
    print("1️⃣ 函数是对象，有属性和方法")
    print(f"函数名: {greet.__name__}")
    print(f"函数文档: {greet.__doc__}")
    print(f"函数类型: {type(greet)}")
    print(f"函数模块: {greet.__module__}")
    print()
    
    print("2️⃣ 函数可以赋值给变量")
    say_hello = greet  # 函数赋值
    print(f"通过变量调用: {say_hello('张三')}")
    print(f"两个变量指向同一个函数: {greet is say_hello}")
    print()
    
    print("3️⃣ 函数可以作为参数传递")
    def call_function(func, arg):
        return func(arg)
    
    result = call_function(greet, "李四")
    print(f"作为参数传递: {result}")
    print()
    
    print("4️⃣ 函数可以作为返回值")
    def get_greeting_function():
        return greet
    
    func = get_greeting_function()
    print(f"作为返回值: {func('王五')}")
    print()
    
    print("5️⃣ 函数可以存储在数据结构中")
    function_list = [greet, say_hello]
    function_dict = {'greet': greet, 'say': say_hello}
    
    for func in function_list:
        print(f"列表中的函数: {func('赵六')}")
    
    print(f"字典中的函数: {function_dict['greet']('钱七')}")
    print()

demonstrate_function_as_object()


# ==== 第二部分：装饰器的本质 ====
print("=== 装饰器的本质 ===\n")

def understand_decorator_essence():
    """理解装饰器的本质"""
    
    print("装饰器就是一个返回函数的函数！")
    print()
    
    # 最简单的装饰器
    def my_decorator(func):
        """最基础的装饰器"""
        print(f"🔧 装饰器正在装饰函数: {func.__name__}")
        
        def wrapper(*args, **kwargs):
            print(f"⚡ 函数 {func.__name__} 调用前")
            result = func(*args, **kwargs)
            print(f"✅ 函数 {func.__name__} 调用后")
            return result
        
        return wrapper
    
    # 手动装饰（不用 @ 语法）
    def original_function():
        print("🎯 这是原始函数")
        return "原始返回值"
    
    print("1️⃣ 手动装饰过程：")
    decorated_function = my_decorator(original_function)
    result = decorated_function()
    print(f"返回值: {result}")
    print()
    
    # 使用 @ 语法糖
    print("2️⃣ 使用 @ 语法糖：")
    @my_decorator
    def auto_decorated_function():
        print("🎯 这是自动装饰的函数")
        return "装饰后的返回值"
    
    result = auto_decorated_function()
    print(f"返回值: {result}")
    print()
    
    print("3️⃣ @ 语法糖的本质：")
    print("@my_decorator")
    print("def func(): pass")
    print("等同于：")
    print("def func(): pass")
    print("func = my_decorator(func)")
    print()

understand_decorator_essence()


# ==== 第三部分：装饰器的执行时机 ====
print("=== 装饰器的执行时机 ===\n")
'''
理解执行的时机：
1. 装饰器函数执行：在你写 @my_decorator 这行代码时
2. wrapper 函数执行：在你调用 hello() 时
'''
def demonstrate_execution_timing():
    """演示装饰器的执行时机"""
    
    print("装饰器在函数定义时执行，不是调用时！")
    print()
    
    def timing_decorator(func):
        print(f"🕐 装饰器在定义时执行: {func.__name__}")
        
        def wrapper(*args, **kwargs):
            print(f"🚀 wrapper 在调用时执行: {func.__name__}")
            return func(*args, **kwargs)
        
        return wrapper
    
    print("定义函数时：")
    @timing_decorator
    def example_function():
        print("🎯 函数体执行")
        return "结果"
    
    print("\n第一次调用时：")
    result1 = example_function()
    
    print("\n第二次调用时：")
    result2 = example_function()
    print()

demonstrate_execution_timing()


# ==== 第四部分：preserving 函数信息 ====
print("=== 保持函数信息：functools.wraps ===\n")

def demonstrate_functools_wraps():
    """演示 functools.wraps 的重要性"""
    
    # 没有使用 wraps 的装饰器
    def bad_decorator(func):
        def wrapper(*args, **kwargs):
            """这是 wrapper 的文档"""
            return func(*args, **kwargs)
        return wrapper
    
    # 使用 wraps 的装饰器
    def good_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """这是 wrapper 的文档"""
            return func(*args, **kwargs)
        return wrapper
    
    @bad_decorator
    def bad_function():
        """这是原始函数的文档"""
        pass
    
    @good_decorator
    def good_function():
        """这是原始函数的文档"""
        pass
    
    print("❌ 没有使用 @functools.wraps:")
    print(f"函数名: {bad_function.__name__}")
    print(f"函数文档: {bad_function.__doc__}")
    print()
    
    print("✅ 使用了 @functools.wraps:")
    print(f"函数名: {good_function.__name__}")
    print(f"函数文档: {good_function.__doc__}")
    print()
    '''
    functools.wraps 的解决方案
    @functools.wraps 会复制原函数的元信息：
    它复制了这些属性：
    python# functools.wraps 复制的属性
    WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__',
                        '__doc__', '__annotations__')
    WRAPPER_UPDATES = ('__dict__',)
    '''

demonstrate_functools_wraps()


# ==== 第五部分：带参数的装饰器 ====
print("=== 带参数的装饰器 ===\n")

def create_parametrized_decorators():
    """创建带参数的装饰器"""
    
    # 带参数的装饰器需要三层函数
    def repeat(times):
        """重复执行装饰器"""
        print(f"🔧 创建重复 {times} 次的装饰器")
        
        def decorator(func):
            print(f"🎯 装饰函数: {func.__name__}")
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                print(f"🔄 准备执行 {times} 次")
                results = []
                for i in range(times):
                    print(f"  第 {i+1} 次执行:")
                    result = func(*args, **kwargs)
                    results.append(result)
                return results
            
            return wrapper
        return decorator
    
    # 使用带参数的装饰器
    @repeat(times=3)
    def say_hello(name):
        message = f"Hello, {name}!"
        print(f"    {message}")
        return message
    
    print("调用被装饰的函数：")
    results = say_hello("Python")
    print(f"所有结果: {results}")
    print()

create_parametrized_decorators()


# ==== 第六部分：类装饰器 ====
print("=== 类装饰器 ===\n")

class CallCounter:
    """类装饰器：统计函数调用次数"""
    
    def __init__(self, func):
        print(f"🏗️ 初始化类装饰器，装饰: {func.__name__}")
        self.func = func
        self.count = 0
        # 保持函数信息
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"📊 函数 {self.func.__name__} 第 {self.count} 次调用")
        return self.func(*args, **kwargs)
    
    def get_count(self):
        return self.count

# 使用类装饰器
@CallCounter
def greet_with_counter(name):
    return f"Hi, {name}!"

print("测试类装饰器:")
print(greet_with_counter("Alice"))
print(greet_with_counter("Bob"))
'''
关键理解：类装饰器的本质
greet_with_counter 不再是原来的函数，而是 CallCounter 类的实例！

为什么可以像函数一样调用？
因为 __call__ 魔术方法！
class CallCounter:
    def __call__(self, *args, **kwargs):  # 这让实例可以像函数一样调用
        self.count += 1
        return self.func(*args, **kwargs)

# 所以可以这样调用：
result = greet_with_counter("Alice")  # 实际调用的是 __call__ 方法
'''
'''
总结：
1. greet_with_counter 是 CallCounter 类的实例
2. 它有 get_count 方法（因为类定义了这个方法）
3. 它仍然可以像函数一样调用（因为有 __call__ 方法）
4. 它既是函数又是对象，具有两重身份
'''
print(f"调用次数: {greet_with_counter.get_count()}")
print()


# ==== 第七部分：实战项目 - 性能监控装饰器系统 ====
print("=== 实战项目：性能监控装饰器系统 ===\n")

class PerformanceMonitor:
    """性能监控装饰器系统"""
    
    def __init__(self):
        self.stats = {}
        self.lock = threading.Lock()
    
    def monitor(self, include_args=False, include_result=False):
        """性能监控装饰器工厂"""
        def decorator(func):
            func_name = func.__name__
            
            # 初始化统计信息
            with self.lock:
                if func_name not in self.stats:
                    self.stats[func_name] = {
                        'call_count': 0,
                        'total_time': 0,
                        'avg_time': 0,
                        'min_time': float('inf'),
                        'max_time': 0,
                        'errors': 0,
                        'last_called': None,
                        'call_history': []
                    }
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                call_info = {
                    'timestamp': datetime.now().isoformat(),
                    'args': args if include_args else None,
                    'kwargs': kwargs if include_args else None,
                }
                
                try:
                    result = func(*args, **kwargs)
                    call_info['result'] = result if include_result else None
                    call_info['success'] = True
                    
                except Exception as e:
                    call_info['error'] = str(e)
                    call_info['success'] = False
                    
                    with self.lock:
                        self.stats[func_name]['errors'] += 1
                    
                    raise
                
                finally:
                    # 更新统计信息
                    end_time = time.time()
                    execution_time = end_time - start_time
                    call_info['execution_time'] = execution_time
                    
                    with self.lock:
                        stats = self.stats[func_name]
                        stats['call_count'] += 1
                        stats['total_time'] += execution_time
                        stats['avg_time'] = stats['total_time'] / stats['call_count']
                        stats['min_time'] = min(stats['min_time'], execution_time)
                        stats['max_time'] = max(stats['max_time'], execution_time)
                        stats['last_called'] = datetime.now().isoformat()
                        
                        # 保留最近的调用历史（最多100条）
                        stats['call_history'].append(call_info)
                        if len(stats['call_history']) > 100:
                            stats['call_history'].pop(0)
                
                return result
            
            return wrapper
        return decorator
    
    def retry(self, max_attempts=3, delay=1, backoff=2):
        """重试装饰器"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                attempts = 0
                current_delay = delay
                
                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        if attempts >= max_attempts:
                            print(f"❌ 函数 {func.__name__} 重试 {max_attempts} 次后仍然失败")
                            raise
                        
                        print(f"⚠️  函数 {func.__name__} 第 {attempts} 次失败，{current_delay}秒后重试")
                        time.sleep(current_delay)
                        current_delay *= backoff
                
            return wrapper
        return decorator
    
    def cache(self, max_size=128, ttl=None):
        """简单的缓存装饰器"""
        def decorator(func):
            cache_dict = {}
            cache_times = {}
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # 创建缓存键
                key = str(args) + str(sorted(kwargs.items()))
                current_time = time.time()
                
                # 检查 TTL
                if ttl and key in cache_times:
                    if current_time - cache_times[key] > ttl:
                        cache_dict.pop(key, None)
                        cache_times.pop(key, None)
                
                # 缓存命中
                if key in cache_dict:
                    print(f"🎯 缓存命中: {func.__name__}")
                    return cache_dict[key]
                
                # 计算结果并缓存
                result = func(*args, **kwargs)
                
                # 检查缓存大小
                if len(cache_dict) >= max_size:
                    # 简单的 LRU：删除最旧的条目
                    oldest_key = next(iter(cache_dict))
                    cache_dict.pop(oldest_key)
                    cache_times.pop(oldest_key, None)
                
                cache_dict[key] = result
                if ttl:
                    cache_times[key] = current_time
                
                print(f"💾 结果已缓存: {func.__name__}")
                return result
            
            # 添加缓存管理方法
            wrapper.cache_info = lambda: {
                'size': len(cache_dict),
                'max_size': max_size,
                'ttl': ttl
            }
            wrapper.cache_clear = lambda: (cache_dict.clear(), cache_times.clear())
            
            return wrapper
        return decorator
    
    def get_stats(self, func_name=None):
        """获取性能统计信息"""
        with self.lock:
            if func_name:
                return self.stats.get(func_name, {})
            return self.stats.copy()
    
    def reset_stats(self, func_name=None):
        """重置统计信息"""
        with self.lock:
            if func_name:
                self.stats.pop(func_name, None)
            else:
                self.stats.clear()


def test_performance_monitor():
    """测试性能监控系统"""
    print("性能监控系统测试:")
    
    # 创建监控器实例
    monitor = PerformanceMonitor()
    
    # 定义测试函数
    @monitor.monitor(include_args=True, include_result=True)
    @monitor.cache(max_size=10, ttl=5)
    def calculate_fibonacci(n):
        """计算斐波那契数列"""
        if n <= 1:
            return n
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    
    @monitor.monitor()
    @monitor.retry(max_attempts=3, delay=0.1)
    def unreliable_function(success_rate=0.7):
        """模拟不稳定的函数"""
        import random
        if random.random() > success_rate:
            raise Exception("随机失败")
        return "成功执行"
    
    # 测试缓存功能
    print("\n1️⃣ 测试缓存功能:")
    result1 = calculate_fibonacci(10)
    print(f"第一次计算结果: {result1}")
    
    result2 = calculate_fibonacci(10)  # 应该命中缓存
    print(f"第二次计算结果: {result2}")
    
    print(f"缓存信息: {calculate_fibonacci.cache_info()}")
    
    # 测试重试功能
    print("\n2️⃣ 测试重试功能:")
    try:
        result = unreliable_function(success_rate=0.3)
        print(f"函数执行成功: {result}")
    except Exception as e:
        print(f"函数最终失败: {e}")
    
    # 查看性能统计
    print("\n3️⃣ 性能统计报告:")
    stats = monitor.get_stats()
    for func_name, stat in stats.items():
        print(f"\n函数: {func_name}")
        print(f"  调用次数: {stat['call_count']}")
        print(f"  总耗时: {stat['total_time']:.4f}s")
        print(f"  平均耗时: {stat['avg_time']:.4f}s")
        print(f"  最小耗时: {stat['min_time']:.4f}s")
        print(f"  最大耗时: {stat['max_time']:.4f}s")
        print(f"  错误次数: {stat['errors']}")
        print(f"  最后调用: {stat['last_called']}")

test_performance_monitor()


def todays_exercises():
    """今天的练习任务"""
    print("\n" + "="*60)
    print("=== 今天的练习任务 ===\n")
    
    print("🎯 任务 1: 实现日志装饰器")
    print("要求：")
    print("- 记录函数调用的详细信息")
    print("- 支持不同日志级别 (DEBUG, INFO, WARNING, ERROR)")
    print("- 支持自定义日志格式")
    print("- 支持文件和控制台输出")
    print()
    
    print("🎯 任务 2: 实现权限检查装饰器")
    print("要求：")
    print("- 检查用户权限")
    print("- 支持角色和权限的组合")
    print("- 权限不足时抛出异常或返回错误")
    print("- 支持权限继承")
    print()
    
    print("🎯 任务 3: 实现数据验证装饰器")
    print("要求：")
    print("- 验证函数参数类型和值")
    print("- 支持自定义验证规则")
    print("- 验证失败时提供详细错误信息")
    print("- 支持可选参数和默认值")
    print()
    
    print("🎯 思考题:")
    print("1. 什么时候使用函数装饰器，什么时候使用类装饰器？")
    print("2. 装饰器会对性能产生什么影响？如何优化？")
    print("3. 如何设计一个装饰器来支持装饰器的装饰器？")
    print("4. functools.wraps 的实现原理是什么？")

todays_exercises()