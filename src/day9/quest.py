# 插件系统框架实践项目
# 综合运用：元类、描述符、特殊方法、类方法

from abc import ABC, abstractmethod, ABCMeta
from typing import Dict, List, Type, Any, Optional
import weakref
import importlib
import inspect

# =============================================================================
# 1. 插件基础设施
# =============================================================================
'''
元类继承层次：
type
  ↑
ABCMeta  
  ↑
PluginMeta
'''
class PluginMeta(ABCMeta):  # 继承自 ABCMeta 解决元类冲突
    """插件元类：自动注册插件"""
    
    # 类属性：存储所有插件
    _plugins: Dict[str, Type] = {}
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # 创建类
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 自动注册插件（跳过抽象基类）
        if not inspect.isabstract(cls) and hasattr(cls, 'plugin_name'):
            mcs._plugins[cls.plugin_name] = cls
            print(f"注册插件: {cls.plugin_name} -> {name}")
        
        return cls
    
    @classmethod
    def get_plugin(mcs, name: str) -> Optional[Type]:
        """获取插件类"""
        return mcs._plugins.get(name)
    
    @classmethod
    def list_plugins(mcs) -> List[str]:
        """列出所有注册的插件"""
        return list(mcs._plugins.keys())

class PluginBase(ABC, metaclass=PluginMeta):
    """插件基类"""
    
    plugin_name: str = ""  # 子类必须设置
    plugin_version: str = "1.0"
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.is_enabled = True
    
    @abstractmethod
    def execute(self, data: Any) -> Any:
        """执行插件逻辑"""
        pass
    
    def get_info(self) -> Dict[str, Any]:
        """获取插件信息"""
        return {
            'name': self.plugin_name,
            'version': self.plugin_version,
            'enabled': self.is_enabled,
            'class': self.__class__.__name__
        }

# =============================================================================
# 2. 插件配置描述符
# =============================================================================

class ConfigProperty:
    """插件配置属性描述符"""
    
    def __init__(self, default_value, validator=None, description=""):
        self.default_value = default_value
        self.validator = validator
        self.description = description
        self.data = weakref.WeakKeyDictionary()
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.data.get(instance, self.default_value)
    
    def __set__(self, instance, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"配置验证失败: {value}")
        self.data[instance] = value
    
    def __set_name__(self, owner, name):
        self.name = name

# =============================================================================
# 3. 插件管理器
# =============================================================================

class PluginManager:
    """插件管理器：使用特殊方法实现友好接口"""
    
    def __init__(self):
        self._active_plugins: Dict[str, PluginBase] = {}
        self._plugin_results = []
    
    def __getitem__(self, plugin_name: str) -> PluginBase:
        """支持 manager[plugin_name] 语法"""
        if plugin_name not in self._active_plugins:
            raise KeyError(f"插件 {plugin_name} 未激活")
        return self._active_plugins[plugin_name]
    
    def __contains__(self, plugin_name: str) -> bool:
        """支持 plugin_name in manager 语法"""
        return plugin_name in self._active_plugins
    
    def __len__(self) -> int:
        """支持 len(manager) 语法"""
        return len(self._active_plugins)
    
    def __iter__(self):
        """支持 for plugin in manager 语法"""
        return iter(self._active_plugins.values())
    
    def load_plugin(self, plugin_name: str, config: Dict[str, Any] = None) -> bool:
        """加载并激活插件"""
        plugin_class = PluginMeta.get_plugin(plugin_name)
        if not plugin_class:
            print(f"插件 {plugin_name} 未找到")
            return False
        
        try:
            plugin_instance = plugin_class(config)
            self._active_plugins[plugin_name] = plugin_instance
            print(f"插件 {plugin_name} 加载成功")
            return True
        except Exception as e:
            print(f"插件 {plugin_name} 加载失败: {e}")
            return False
    
    def execute_all(self, data: Any) -> List[Any]:
        """执行所有激活的插件"""
        results = []
        for plugin in self._active_plugins.values():
            if plugin.is_enabled:
                try:
                    result = plugin.execute(data)
                    results.append({
                        'plugin': plugin.plugin_name,
                        'result': result,
                        'success': True
                    })
                except Exception as e:
                    results.append({
                        'plugin': plugin.plugin_name,
                        'error': str(e),
                        'success': False
                    })
        return results

# =============================================================================
# 4. 具体插件实现
# =============================================================================

class DataValidatorPlugin(PluginBase):
    """数据验证插件"""
    
    plugin_name = "data_validator"
    plugin_version = "1.0"
    
    # 使用配置描述符
    min_length = ConfigProperty(
        default_value=1,
        validator=lambda x: isinstance(x, int) and x >= 0,
        description="最小长度"
    )
    
    max_length = ConfigProperty(
        default_value=100,
        validator=lambda x: isinstance(x, int) and x > 0,
        description="最大长度"
    )
    
    def execute(self, data: Any) -> Any:
        if not isinstance(data, str):
            raise TypeError("数据必须是字符串")
        
        if len(data) < self.min_length:
            raise ValueError(f"数据长度不能小于 {self.min_length}")
        
        if len(data) > self.max_length:
            raise ValueError(f"数据长度不能大于 {self.max_length}")
        
        return {"valid": True, "length": len(data)}

class DataTransformPlugin(PluginBase):
    """数据转换插件"""
    
    plugin_name = "data_transform"
    plugin_version = "2.0"
    
    transform_type = ConfigProperty(
        default_value="upper",
        validator=lambda x: x in ["upper", "lower", "title"],
        description="转换类型"
    )
    
    def execute(self, data: Any) -> Any:
        if not isinstance(data, str):
            return data  # 非字符串数据直接返回
        
        transform_map = {
            "upper": data.upper,
            "lower": data.lower,
            "title": data.title
        }
        
        transform_func = transform_map[self.transform_type]
        return transform_func()

class DataLoggerPlugin(PluginBase):
    """数据日志插件"""
    
    plugin_name = "data_logger"
    plugin_version = "1.5"
    
    log_level = ConfigProperty(
        default_value="INFO",
        validator=lambda x: x in ["DEBUG", "INFO", "WARNING", "ERROR"],
        description="日志级别"
    )
    
    def execute(self, data: Any) -> Any:
        log_message = f"[{self.log_level}] 处理数据: {data}"
        print(log_message)
        return {"logged": True, "message": log_message}

# =============================================================================
# 5. 插件链处理器
# =============================================================================

class PluginChain:
    """插件链：按顺序执行多个插件"""
    
    def __init__(self, manager: PluginManager):
        self.manager = manager
        self.chain = []
    
    def add_plugin(self, plugin_name: str) -> 'PluginChain':
        """添加插件到链中（支持链式调用）"""
        if plugin_name in self.manager:
            self.chain.append(plugin_name)
        else:
            raise ValueError(f"插件 {plugin_name} 未加载")
        return self  # 支持链式调用
    
    def execute(self, initial_data: Any) -> Dict[str, Any]:
        """执行插件链"""
        current_data = initial_data
        results = []
        
        for plugin_name in self.chain:
            plugin = self.manager[plugin_name]
            try:
                current_data = plugin.execute(current_data)
                results.append({
                    'plugin': plugin_name,
                    'result': current_data,
                    'success': True
                })
            except Exception as e:
                results.append({
                    'plugin': plugin_name,
                    'error': str(e),
                    'success': False
                })
                break  # 链中断
        
        return {
            'final_result': current_data,
            'chain_results': results,
            'success': all(r['success'] for r in results)
        }

# =============================================================================
# 6. 演示和测试
# =============================================================================

def demonstrate_plugin_system():
    """演示插件系统的使用"""
    print("=== 插件系统演示 ===\n")
    
    # 1. 查看已注册的插件
    print("1. 已注册的插件:")
    for plugin_name in PluginMeta.list_plugins():
        print(f"  - {plugin_name}")
    
    # 2. 创建插件管理器并加载插件
    print(f"\n2. 加载插件:")
    manager = PluginManager()
    
    # 加载验证插件（带配置）
    manager.load_plugin("data_validator", {
        "min_length": 2,
        "max_length": 50
    })
    
    # 加载转换插件
    manager.load_plugin("data_transform", {
        "transform_type": "title"
    })
    
    # 加载日志插件
    manager.load_plugin("data_logger", {
        "log_level": "INFO"
    })
    
    print(f"活跃插件数量: {len(manager)}")
    
    # 3. 测试单个插件
    print(f"\n3. 测试单个插件:")
    validator = manager["data_validator"]
    try:
        result = validator.execute("hello world")
        print(f"验证结果: {result}")
    except Exception as e:
        print(f"验证失败: {e}")
    
    # 4. 执行所有插件
    print(f"\n4. 执行所有插件:")
    results = manager.execute_all("hello world")
    for result in results:
        if result['success']:
            print(f"  {result['plugin']}: {result['result']}")
        else:
            print(f"  {result['plugin']}: 错误 - {result['error']}")
    
    # 5. 使用插件链
    print(f"\n5. 插件链处理:")
    chain = PluginChain(manager)
    chain.add_plugin("data_validator").add_plugin("data_transform").add_plugin("data_logger")
    
    chain_result = chain.execute("hello world")
    print(f"链处理成功: {chain_result['success']}")
    print(f"最终结果: {chain_result['final_result']}")

def demonstrate_plugin_features():
    """演示插件的高级特性"""
    print(f"\n=== 插件高级特性演示 ===\n")
    
    # 1. 配置描述符
    print("1. 配置描述符测试:")
    plugin = DataValidatorPlugin()
    print(f"默认最小长度: {plugin.min_length}")
    
    plugin.min_length = 5
    print(f"修改后最小长度: {plugin.min_length}")
    
    try:
        plugin.min_length = -1  # 触发验证
    except ValueError as e:
        print(f"配置验证: {e}")
    
    # 2. 插件信息
    print(f"\n2. 插件信息:")
    for plugin_name in PluginMeta.list_plugins():
        plugin_class = PluginMeta.get_plugin(plugin_name)
        plugin_instance = plugin_class()
        info = plugin_instance.get_info()
        print(f"  {info}")

if __name__ == "__main__":
    demonstrate_plugin_system()
    demonstrate_plugin_features()