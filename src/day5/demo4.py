# 静态作用域 vs 动态作用域对比演示

def static_scope_demo():
    """静态作用域（词法作用域）演示 - Python的方式"""
    
    x = "全局 x"
    
    def outer():
        x = "outer 中的 x"
        
        def inner():
            # 在静态作用域中，这里的 x 在定义时就确定了
            # 它会查找定义时所在作用域链中的 x
            print(f"inner 中看到的 x: {x}")  # outer 中的 x
        
        return inner
    
    def another_function():
        x = "another_function 中的 x"
        # 调用从 outer 返回的 inner 函数
        inner_func = outer()
        inner_func()  # 仍然是 "outer 中的 x"，不是 "another_function 中的 x"
    
    print("=== 静态作用域演示 ===")
    print("1. 直接调用:")
    inner_func = outer()
    inner_func()
    
    print("2. 在不同函数中调用:")
    another_function()

def simulate_dynamic_scope():
    """模拟动态作用域的行为（Python实际不支持）"""
    
    # 使用字典模拟调用栈和作用域
    call_stack = []
    
    def push_scope(scope_vars):
        """压入作用域"""
        call_stack.append(scope_vars)
    
    def pop_scope():
        """弹出作用域"""
        if call_stack:
            call_stack.pop()
    
    def lookup_var(var_name):
        """查找变量 - 从最近的调用开始查找"""
        for i in range(len(call_stack) - 1, -1, -1):
            if var_name in call_stack[i]:
                return call_stack[i][var_name]
        return None
    
    def func_a():
        push_scope({'x': 'func_a 中的 x'})
        print(f"func_a 看到的 x: {lookup_var('x')}")
        func_b()  # 调用 func_b
        pop_scope()
    
    def func_b():
        push_scope({'y': 'func_b 中的 y'})
        print(f"func_b 看到的 x: {lookup_var('x')}")  # 会找到 func_a 的 x
        print(f"func_b 看到的 y: {lookup_var('y')}")
        func_c()  # 调用 func_c
        pop_scope()
    
    def func_c():
        push_scope({'x': 'func_c 中的 x'})
        print(f"func_c 看到的 x: {lookup_var('x')}")  # 会找到自己的 x
        print(f"func_c 看到的来自 func_a 的变量: {lookup_var('y')}")  # 来自 func_b
        pop_scope()
    
    print("=== 模拟动态作用域 ===")
    push_scope({'x': '全局 x'})
    func_a()
    pop_scope()

def closure_vs_class_example():
    """闭包与类的实际对比 - 实现相同功能"""
    
    # 使用闭包实现
    def create_bank_account_closure(initial_balance=0):
        balance = initial_balance
        transaction_history = []
        
        def deposit(amount):
            nonlocal balance
            balance += amount
            transaction_history.append(f"存入: {amount}, 余额: {balance}")
            return balance
        
        def withdraw(amount):
            nonlocal balance
            if balance >= amount:
                balance -= amount
                transaction_history.append(f"取出: {amount}, 余额: {balance}")
                return balance
            else:
                transaction_history.append(f"余额不足，无法取出: {amount}")
                return balance
        
        def get_balance():
            return balance
        
        def get_history():
            return transaction_history.copy()
        
        # 返回接口字典
        return {
            'deposit': deposit,
            'withdraw': withdraw,
            'balance': get_balance,
            'history': get_history
        }
    
    # 使用类实现
    class BankAccount:
        def __init__(self, initial_balance=0):
            self._balance = initial_balance
            self._transaction_history = []
        
        def deposit(self, amount):
            self._balance += amount
            self._transaction_history.append(f"存入: {amount}, 余额: {self._balance}")
            return self._balance
        
        def withdraw(self, amount):
            if self._balance >= amount:
                self._balance -= amount
                self._transaction_history.append(f"取出: {amount}, 余额: {self._balance}")
            else:
                self._transaction_history.append(f"余额不足，无法取出: {amount}")
            return self._balance
        
        @property
        def balance(self):
            return self._balance
        
        @property
        def history(self):
            return self._transaction_history.copy()
    
    return create_bank_account_closure, BankAccount

def advanced_closure_patterns():
    """高级闭包模式"""
    
    # 模式1: 工厂函数
    def create_validator(rules):
        """创建验证器"""
        def validate(data):
            results = {}
            for field, rule_func in rules.items():
                if field in data:
                    results[field] = rule_func(data[field])
                else:
                    results[field] = False
            return results
        return validate
    
    # 模式2: 记忆化装饰器（使用闭包）
    def memoize(func):
        """记忆化装饰器"""
        cache = {}
        
        def wrapper(*args, **kwargs):
            # 创建缓存键
            key = str(args) + str(sorted(kwargs.items()))
            
            if key not in cache:
                cache[key] = func(*args, **kwargs)
                print(f"缓存未命中，计算结果: {cache[key]}")
            else:
                print(f"缓存命中: {cache[key]}")
            
            return cache[key]
        
        # 添加缓存清理功能
        wrapper.clear_cache = lambda: cache.clear()
        wrapper.cache_info = lambda: f"缓存大小: {len(cache)}"
        
        return wrapper
    
    # 模式3: 配置管理器
    def create_config_manager(default_config):
        """创建配置管理器"""
        config = default_config.copy()
        
        def get(key, default=None):
            return config.get(key, default)
        
        def set_config(updates):
            nonlocal config
            config.update(updates)
        
        def reset():
            nonlocal config
            config = default_config.copy()
        
        return get, set_config, reset
    
    return create_validator, memoize, create_config_manager

# 运行演示
if __name__ == "__main__":
    print("1. 静态作用域演示:")
    static_scope_demo()
    
    print("\n2. 动态作用域模拟:")
    simulate_dynamic_scope()
    
    print("\n3. 闭包 vs 类对比:")
    create_closure_account, BankAccount = closure_vs_class_example()
    
    # 闭包版本
    closure_account = create_closure_account(100)
    closure_account['deposit'](50)
    closure_account['withdraw'](30)
    print(f"闭包账户余额: {closure_account['balance']()}")
    
    # 类版本
    class_account = BankAccount(100)
    class_account.deposit(50)
    class_account.withdraw(30)
    print(f"类账户余额: {class_account.balance}")
    
    print("\n4. 高级闭包模式:")
    create_validator, memoize, create_config_manager = advanced_closure_patterns()
    
    # 验证器示例
    email_rules = {
        'email': lambda x: '@' in x and '.' in x,
        'age': lambda x: isinstance(x, int) and 0 < x < 150
    }
    validator = create_validator(email_rules)
    print("验证结果:", validator({'email': 'test@example.com', 'age': 25}))
    
    # 记忆化示例
    @memoize
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n-1) + fibonacci(n-2)
    
    print(f"fibonacci(5) = {fibonacci(5)}")
    print(f"fibonacci(5) = {fibonacci(5)}")  # 第二次调用会使用缓存