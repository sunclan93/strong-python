# LEGB 作用域解析规则演示

# Built-in 作用域 (内置)
# print, len, str 等都在这里

# Global 作用域 (全局)
global_var = "我是全局变量"

def outer_function():
    """外层函数 - Enclosing 作用域"""
    enclosing_var = "我是嵌套作用域变量"
    
    def inner_function():
        """内层函数 - Local 作用域"""
        local_var = "我是局部变量"
        
        # LEGB 查找顺序演示
        print("=== LEGB 查找演示 ===")
        print(f"Local: {local_var}")           # L - 局部
        print(f"Enclosing: {enclosing_var}")   # E - 嵌套
        print(f"Global: {global_var}")         # G - 全局
        print(f"Built-in: {len([1,2,3])}")     # B - 内置
        
        # 变量遮蔽演示
        global_var = "局部变量遮蔽了全局变量"  # 这会创建新的局部变量
        print(f"被遮蔽的全局变量: {global_var}")
    
    return inner_function

# 作用域查看工具
def scope_inspector():
    """作用域检查器"""
    import builtins
    
    x = "local_x"
    
    def nested():
        y = "nested_y"
        
        print("=== 作用域分析 ===")
        print("Local 变量:", [var for var in locals().keys() if not var.startswith('__')])
        print("Global 变量:", [var for var in globals().keys() if not var.startswith('__')])
        print("Built-in 变量数量:", len(dir(builtins)))
        
        # 变量查找过程
        print(f"\n变量 'x' 的查找:")
        if 'x' in locals():
            print(f"  ✓ 在 Local 找到: {locals()['x']}")
        elif 'x' in globals():
            print(f"  ✓ 在 Global 找到: {globals()['x']}")
        else:
            print("  ✗ 在 Local 和 Global 都未找到")
            
        return y
    
    return nested()

# 运行演示
if __name__ == "__main__":
    print("1. LEGB 查找顺序演示:")
    inner_func = outer_function()
    inner_func()
    
    print("\n2. 作用域检查:")
    scope_inspector()
    
    print(f"\n3. 全局变量未被修改: {global_var}")  # 全局变量保持不变