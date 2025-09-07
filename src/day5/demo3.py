# nonlocal 和 global 关键字深度理解

# 全局变量
counter = 0
message = "全局消息"

def global_keyword_demo():
    """global 关键字演示"""
    
    def modify_global():
        global counter, message
        counter += 1
        message = "被修改的全局消息"
        local_var = "局部变量"
        print(f"函数内 - counter: {counter}, message: {message}")
    
    def read_global():
        # 不使用 global，只读取全局变量
        print(f"只读全局 - counter: {counter}, message: {message}")
        # counter += 1  # 这会报错：UnboundLocalError
    
    print("=== global 关键字演示 ===")
    print(f"修改前 - counter: {counter}, message: {message}")
    modify_global()
    print(f"修改后 - counter: {counter}, message: {message}")
    read_global()

def nonlocal_keyword_demo():
    """nonlocal 关键字演示"""
    
    def outer():
        x = 10
        y = 20
        
        def inner1():
            nonlocal x  # 声明要修改外层函数的变量
            x += 1
            # y += 1  # 这会报错，因为没有声明 nonlocal y
            print(f"inner1 - x: {x}")
        
        def inner2():
            # 不使用 nonlocal，只能读取
            print(f"inner2 只读 - x: {x}, y: {y}")
        
        def inner3():
            x = 100  # 这会创建新的局部变量，不会影响外层的 x
            print(f"inner3 新建 - x: {x}")
        
        print(f"outer 开始 - x: {x}, y: {y}")
        inner1()
        print(f"inner1 后 - x: {x}, y: {y}")
        inner2()
        inner3()
        print(f"inner3 后 - x: {x}, y: {y}")  # x 还是 11
        
        return inner1, inner2, inner3
    
    return outer()

def scope_modification_patterns():
    """作用域修改模式总结"""
    
    global_var = "我是全局的"
    
    def pattern_demo():
        enclosing_var = "我是外层的"
        
        def inner():
            local_var = "我是局部的"
            
            # 模式1: 读取所有作用域的变量
            print("=== 读取模式 ===")
            print(f"读取局部: {local_var}")
            print(f"读取外层: {enclosing_var}")
            print(f"读取全局: {global_var}")
            
            # 模式2: 修改不同作用域的变量需要不同声明
            def modify_demo():
                nonlocal enclosing_var  # 修改外层变量
                global global_var       # 修改全局变量
                
                local_var_new = "新的局部变量"    # 创建局部变量
                enclosing_var = "修改后的外层"    # 修改外层变量
                global_var = "修改后的全局"       # 修改全局变量
                
                print("=== 修改模式 ===")
                print(f"新局部: {local_var_new}")
                print(f"修改外层: {enclosing_var}")
                print(f"修改全局: {global_var}")
            
            return modify_demo
        
        return inner()
    
    return pattern_demo()

# 实际应用：状态管理器
def create_state_manager(initial_state=None):
    """创建状态管理器 - 闭包的实际应用"""
    
    state = initial_state or {}
    history = [state.copy()]
    
    def get_state(key=None):
        """获取状态"""
        if key is None:
            return state.copy()
        return state.get(key)
    
    def set_state(key, value):
        """设置状态"""
        nonlocal state
        old_state = state.copy()
        state[key] = value
        history.append(state.copy())
        return old_state
    
    def reset_state():
        """重置状态"""
        nonlocal state
        state = initial_state.copy() if initial_state else {}
        history.clear()
        history.append(state.copy())
    
    def get_history():
        """获取历史记录"""
        return history.copy()
    
    def undo():
        """撤销操作"""
        nonlocal state
        if len(history) > 1:
            history.pop()  # 移除当前状态
            state = history[-1].copy()  # 恢复到前一个状态
        return state.copy()
    
    # 返回管理器接口
    return {
        'get': get_state,
        'set': set_state,
        'reset': reset_state,
        'history': get_history,
        'undo': undo
    }

# 运行演示
if __name__ == "__main__":
    print("1. global 关键字演示:")
    global_keyword_demo()
    
    print(f"\n全局变量最终值 - counter: {counter}, message: {message}")
    
    print("\n2. nonlocal 关键字演示:")
    inner1, inner2, inner3 = nonlocal_keyword_demo()
    
    print("\n3. 作用域修改模式:")
    modify_func = scope_modification_patterns()
    modify_func()
    
    print("\n4. 实际应用 - 状态管理器:")
    manager = create_state_manager({'name': 'Python', 'version': '3.9'})
    
    print(f"初始状态: {manager['get']()}")
    
    manager['set']('version', '3.10')
    print(f"更新后: {manager['get']()}")
    
    manager['set']('author', 'Guido')
    print(f"添加后: {manager['get']()}")
    
    print(f"历史记录: {len(manager['history']())} 个状态")
    
    manager['undo']()
    print(f"撤销后: {manager['get']()}")
    
    print(f"历史记录: {manager['history']()}")