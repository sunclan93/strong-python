"""
第一课练习：SmartDict 智能字典实现
学习目标：深入理解 Python 对象模型和魔术方法

要求：
1. 实现点号访问：obj.key = value, value = obj.key  
2. 支持链式操作：obj.set('a', 1).set('b', 2)
3. 自动类型转换：字符串数字自动转为 int/float
4. 访问历史记录：记录每次访问的 key
5. 使用魔术方法实现优雅的接口
"""

from gettext import install
from smtplib import SMTPDataError
from typing import Any, List, Union
from datetime import datetime
import json
from xmlrpc.client import Boolean


class SmartDict:
    """
    智能字典类 - 演示 Python 对象模型的强大特性
    
    这个类展示了：
    - __getattr__ 和 __setattr__ 的使用
    - __getitem__ 和 __setitem__ 的实现  
    - __str__ 和 __repr__ 的区别
    - 类型转换和数据验证
    - 方法链式调用设计
    """
    
    def __init__(self, **kwargs):
        # 使用 object.__setattr__ 避免递归调用
        object.__setattr__(self, '_data', {}) # 这么写是为了不让他调用52行的代码，如果写成self._data = {}的话就会调用52行代码
        object.__setattr__(self, '_access_history', [])
        object.__setattr__(self, '_auto_convert', True)
        
        # 初始化数据
        for key, value in kwargs.items(): 
            self[key] = value # 触发__setitem__
    
    def __eq__(self, other) -> Boolean:
        # 1. check if the input is smartdict
        if not isinstance(other, SmartDict):
            return False
        # 2. check if the value is same
        return self._data == other._data
    
    def __lt__(self, other):
        if not isinstance(other, SmartDict):
            return NotImplemented  # 不知道怎么比较，让对方试试
        # compare by the len of data
        return len(self._data) < len(other._data)

    def __getattr__(self, key: str) -> Any:
        """
        点号访问实现：obj.key
        
        注意：只有当属性不存在时才会调用此方法
        这就是为什么我们使用 _data 存储实际数据

        🎯 嵌套访问的关键实现
        当访问 obj.user 时：
        1. 如果 user 存在，返回它
        2. 如果不存在，创建新的 SmartDict 并返回
        """
        if key.startswith('_'):  # 私有属性直接抛出异常
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
        if key not in self._data:
            self._data[key] = SmartDict()
            self._access_history.append({
                'action': 'auto_create',
                'key': key,
                'timestamp': datetime.now().isoformat()
            })
        # 记录访问历史
        self._access_history.append({
            'action': 'get',
            'key': key,
            'timestamp': datetime.now().isoformat()
        })
        
        return self._data[key]
        
    
    def __setattr__(self, key: str, value: Any) -> None:
        """
        点号赋值实现：obj.key = value
        
        为了避免递归，私有属性使用 object.__setattr__
        """
        if key.startswith('_'):
            object.__setattr__(self, key, value)
        else:
            self._set_value(key, value)
    
    def __getitem__(self, key: str) -> Any: 
        """字典式访问：obj['key']""" 
        # return self._get_value(key) 复用 __getattr__ 的嵌套逻辑
        return self.__getattr__(key)
    
    def __setitem__(self, key: str, value: Any) -> None:
        """字典式赋值：obj['key'] = value"""
        self._set_value(key, value)
    
    def __iter__(self):
        return iter(self._data) # 方法必须返回迭代器，不能返回可迭代对象本身。函数把可迭代对象转换为迭代器。
    
    def _get_value(self, key: str) -> Any:
        """获取值的内部实现"""
        # 记录访问历史
        self._access_history.append({
            'action': 'get',
            'key': key,
            'timestamp': datetime.now().isoformat()
        })
        
        if key not in self._data:
            raise KeyError(f"Key '{key}' not found")
        
        return self._data[key]
    
    def _set_value(self, key: str, value: Any) -> None:
        """设置值的内部实现"""
        # 记录访问历史
        self._access_history.append({
            'action': 'set', 
            'key': key,
            'value': str(value),
            'timestamp': datetime.now().isoformat()
        })
        
        # 自动类型转换
        if self._auto_convert:
            value = self._auto_type_conversion(value)
        
        self._data[key] = value
    def _to_dict(self):
        """递归转换为普通字典，便于显示"""
        result = {}
        for key, value in self._data.items():
            if isinstance(value, SmartDict):
                result[key] = value._to_dict()  # 递归处理嵌套
            else:
                result[key] = value
        return result
    
    def _auto_type_conversion(self, value: Any) -> Any:
        """
        自动类型转换实现
        
        演示了 Python 的动态类型特性和异常处理
        """
        if not isinstance(value, str):
            return value
        
        # 尝试转换为整数
        try:
            if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                return int(value)
        except ValueError:
            pass
        
        # 尝试转换为浮点数
        try:
            if '.' in value:
                return float(value)
        except ValueError:
            pass
        
        # 尝试转换为布尔值
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        return value
    
    def set(self, key: str, value: Any) -> 'SmartDict': # 调用__setattr__
        """
        支持链式调用的设置方法
        
        返回 self 是链式调用的关键
        """
        
        self[key] = value
        return self
    
    def get(self, key: str, default: Any = None) -> Any:
        """安全获取值"""
        try:
            return self[key]
        except KeyError:
            return default
    
    def keys(self):
        """获取所有键"""
        return self._data.keys()
    
    def values(self):
        """获取所有值"""
        return self._data.values()
    
    def items(self):
        """获取所有键值对"""
        return self._data.items()
    
    def get_access_history(self) -> List[dict]:
        """获取访问历史"""
        return self._access_history.copy() # 使用前拷贝
    
    def clear_history(self) -> 'SmartDict':
        """清除历史记录"""
        self._access_history.clear()
        return self
    
    def toggle_auto_convert(self) -> 'SmartDict':
        """切换自动类型转换"""
        self._auto_convert = not self._auto_convert
        return self
    
    def __str__(self):
        """美化显示，支持嵌套结构"""
        return json.dumps(self._to_dict(), indent=2, ensure_ascii=False)
    
    def __repr__(self) -> str:
        """开发者友好的字符串表示"""
        return f"SmartDict({self._data})"
    
    def __len__(self) -> int:
        """支持 len() 函数"""
        return len(self._data)
    
    def __contains__(self, key: str) -> bool:
        """支持 in 操作符"""
        return key in self._data
    
    def __bool__(self) -> bool:
        """支持布尔值判断"""
        return bool(self._data)
def test_edge_cases():
    """测试边界情况"""
    print("=== 边界情况测试 ===\n")
    
    obj = SmartDict()
    
    print("1️⃣ 覆盖嵌套对象")
    obj.user.name = "张三"
    print(f"设置嵌套: {obj}")
    
    obj.user = "现在是字符串"  # 覆盖整个 user 对象
    print(f"覆盖后: {obj}")
    print()
    
    print("2️⃣ 混合数据类型")
    obj.data.numbers = [1, 2, 3]
    obj.data.config.enabled = True
    print(f"混合类型: {obj}")
    print()
    
    print("3️⃣ 检查类型")
    print(f"obj.data 是 SmartDict: {isinstance(obj.data, SmartDict)}")
    print(f"obj.data.numbers 是 list: {isinstance(obj.data.numbers, list)}")

def test_smart_dict():
    """
    测试函数 - 演示 SmartDict 的各种功能
    同时展示了单元测试的基本思想
    """
    print("=== SmartDict 功能测试 ===\n")
    
    # 1. 基本创建和访问
    print("1. 基本功能测试")
    sd = SmartDict(name="张三", age="25")
    print(f"创建: {sd}")
    print(f"点号访问 sd.name: {sd.name}")
    print(f"字典访问 sd['age']: {sd['age']} (类型: {type(sd['age'])})")
    print()
    
    # 2. 链式操作
    print("2. 链式操作测试")
    result = sd.set('city', '北京').set('salary', '15000.5').set('married', 'false')
    print(f"链式设置后: {result}")
    print(f"salary 类型: {type(sd.salary)}")
    print(f"married 类型: {type(sd.married)}")
    print()
    
    # 3. 访问历史
    print("3. 访问历史测试")
    history = sd.get_access_history()
    print("访问历史:")
    for record in history[-3:]:  # 显示最后3条记录
        print(f"  {record}")
    print()
    
    # 4. 异常处理
    print("4. 异常处理测试")
    try:
        print(sd.nonexistent)
    except KeyError as e:
        print(f"预期异常: {e}")
    
    print(f"安全访问不存在的键: {sd.get('nonexistent', '默认值')}")
    print()
    
    # 5. 其他魔术方法
    print("5. 其他功能测试")
    print(f"长度: {len(sd)}")
    print(f"包含 'name': {'name' in sd}")
    print(f"布尔值: {bool(sd)}")
    
    # 6. 测试比较
    a = SmartDict(x=1)
    b=  SmartDict(x=1,y=2)
    print(f"a<b: {a < b}")

    # 7. 测试iter
    print("start to iterate 'a'")
    for i in b:
        print(f"the value is {i} ")
    

def test_nested_access():
    print("=== 嵌套访问测试 ===\n")
    
    print("1️⃣ 创建空的 SmartDict")
    obj = SmartDict()
    print(f"初始状态: {obj}")
    print()
    
    print("2️⃣ 嵌套赋值：obj.user.name = '张三'")
    obj.user.name = "张三"
    print(f"赋值后: {obj}")
    print()
    
    print("3️⃣ 继续嵌套：obj.user.age = 25")
    obj.user.age = 25
    print(f"继续赋值: {obj}")
    print()
    
    print("4️⃣ 多层嵌套：obj.config.database.host = 'localhost'")
    obj.config.database.host = "localhost"
    obj.config.database.port = 3306
    print(f"多层嵌套: {obj}")
    print()
    
    print("5️⃣ 访问嵌套值")
    print(f"obj.user.name = {obj.user.name}")
    print(f"obj.config.database.host = {obj.config.database.host}")
    print()
    
    print("6️⃣ 链式调用仍然有效")
    result = obj.set("version", "1.0").set("status", "active")
    print(f"链式调用结果: {result}")
    print()
    
def test_edge_cases():
    """测试边界情况"""
    print("=== 边界情况测试 ===\n")
    
    obj = SmartDict()
    
    print("1️⃣ 覆盖嵌套对象")
    obj.user.name = "张三"
    print(f"设置嵌套: {obj}")
    
    obj.user = "现在是字符串"  # 覆盖整个 user 对象
    print(f"覆盖后: {obj}")
    print()
    
    print("2️⃣ 混合数据类型")
    obj.data.numbers = [1, 2, 3]
    obj.data.config.enabled = True
    print(f"混合类型: {obj}")
    print()
    
    print("3️⃣ 检查类型")
    print(f"obj.data 是 SmartDict: {isinstance(obj.data, SmartDict)}")
    print(f"obj.data.numbers 是 list: {isinstance(obj.data.numbers, list)}")

if __name__ == "__main__":
    # test_smart_dict()
    test_nested_access()
    print("="*25+"edge case"+"="*20)
    test_edge_cases()
    
    print("\n=== 练习任务 ===")
    print("1. 运行这个代码，理解每个魔术方法的作用")
    print("2. 尝试添加 __eq__ 方法，支持两个 SmartDict 对象的比较")
    print("3. 添加 __iter__ 方法，支持 for 循环遍历")
    print("4. 思考：为什么要用 _data 而不是直接存储在对象属性中？")
    print("5. 尝试实现嵌套访问：obj.user.name = 'value'")
    