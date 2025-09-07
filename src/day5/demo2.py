# 闭包的形成条件和原理

def closure_demo():
    """闭包形成的三个条件演示"""
    
    # 条件1: 必须有嵌套函数
    def outer_function(name):
        """外层函数"""
        message = f"Hello, {name}!"  # 外层函数的局部变量
        
        # 条件2: 内层函数必须引用外层函数的变量
        def inner_function():
            """内层函数"""
            return message  # 引用了外层函数的 message 变量
        
        # 条件3: 外层函数必须返回内层函数
        return inner_function  # 返回内层函数对象
    
    return outer_function

# 闭包的生命周期演示
def create_counter(initial=0):
    """创建计数器闭包"""
    count = initial
    
    def counter():
        nonlocal count  # 声明要修改外层变量
        count += 1
        return count
    
    # 闭包信息检查
    def get_closure_info():
        """获取闭包信息"""
        if counter.__closure__:
            print("=== 闭包信息 ===")
            print(f"闭包变量数量: {len(counter.__closure__)}")
            for i, cell in enumerate(counter.__closure__):
                print(f"  变量 {i}: {cell.cell_contents}")
        else:
            print("这不是一个闭包函数")
    
    # 为 counter 函数添加信息查看方法
    counter.get_info = get_closure_info
    counter.reset = lambda: create_counter(initial)  # 重置计数器
    
    return counter

# 多个闭包共享同一个外层变量的陷阱
def closure_trap_demo():
    """闭包陷阱演示 - 延迟绑定问题"""
    
    # 错误的做法 - 所有闭包都会引用同一个变量
    functions_wrong = []
    for i in range(3):
        functions_wrong.append(lambda: i)  # 陷阱：所有lambda都引用同一个i
    
    # 正确的做法1 - 使用默认参数
    functions_correct1 = []
    for i in range(3):
        functions_correct1.append(lambda x=i: x)  # 立即绑定
    
    # 正确的做法2 - 使用额外的作用域
    def create_func(n):
        return lambda: n
    
    functions_correct2 = []
    for i in range(3):
        functions_correct2.append(create_func(i))
    
    return functions_wrong, functions_correct1, functions_correct2

# 闭包 vs 类的比较
class CounterClass:
    """使用类实现计数器"""
    def __init__(self, initial=0):
        self.count = initial
    
    def __call__(self):
        self.count += 1
        return self.count
    
    def reset(self):
        self.count = 0

def counter_performance_test():
    """闭包 vs 类的性能比较"""
    import time
    
    # 闭包版本
    def create_closure_counter():
        count = 0
        def counter():
            nonlocal count
            count += 1
            return count
        return counter
    
    # 测试闭包性能
    closure_counter = create_closure_counter()
    start_time = time.time()
    for _ in range(100000):
        closure_counter()
    closure_time = time.time() - start_time
    
    # 测试类性能
    class_counter = CounterClass()
    start_time = time.time()
    for _ in range(100000):
        class_counter()
    class_time = time.time() - start_time
    
    return closure_time, class_time

# 运行演示
if __name__ == "__main__":
    print("1. 闭包基本演示:")
    demo_func = closure_demo()
    greet = demo_func("Python")
    print(greet())  # Hello, Python!
    
    print("\n2. 计数器闭包:")
    counter1 = create_counter(10)
    counter2 = create_counter(20)
    
    print(f"Counter1: {counter1()}, {counter1()}")  # 11, 12
    print(f"Counter2: {counter2()}, {counter2()}")  # 21, 22
    
    counter1.get_info()
    
    print("\n3. 闭包陷阱演示:")
    wrong, correct1, correct2 = closure_trap_demo()
    
    print("错误的做法结果:", [f() for f in wrong])        # [2, 2, 2] - 都是最后的值
    print("正确的做法1:", [f() for f in correct1])        # [0, 1, 2]
    print("正确的做法2:", [f() for f in correct2])        # [0, 1, 2]
    
    print("\n4. 性能比较:")
    closure_time, class_time = counter_performance_test()
    print(f"闭包时间: {closure_time:.4f}s")
    print(f"类时间: {class_time:.4f}s")
    print(f"闭包比类快 {(class_time/closure_time-1)*100:.1f}%")