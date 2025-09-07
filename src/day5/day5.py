# 企业级配置管理器项目
# 综合运用闭包、作用域、nonlocal/global 等概念

import json
import os
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

class ConfigurationManager:
    """企业级配置管理器 - 使用闭包实现高级功能"""
    
    def __init__(self, default_config: Dict[str, Any] = None):
        self.default_config = default_config or {}
        self.config_stack = []  # 配置栈，支持配置继承
        self.change_history = []  # 变更历史
        self.validators = {}  # 验证器
        self.watchers = {}  # 监听器
        
    def create_environment(self, env_name: str, base_config: Dict[str, Any] = None):
        """创建配置环境 - 返回闭包函数"""
        
        # 环境特定的配置
        env_config = base_config or self.default_config.copy()
        env_history = []
        env_validators = {}
        env_watchers = {}
        
        def get(key: str, default: Any = None) -> Any:
            """获取配置值 - LEGB 查找"""
            # L: 局部（函数参数）
            if default is not None:
                local_default = default
            else:
                local_default = None
            
            # E: 环境配置（Enclosing）
            if key in env_config:
                return env_config[key]
            
            # G: 全局默认配置（Global）
            if key in self.default_config:
                return self.default_config[key]
            
            # B: 内置默认值（Built-in）
            return local_default
        
        def set_value(key: str, value: Any, validate: bool = True) -> bool:
            """设置配置值"""
            nonlocal env_config  # 修改环境配置
            
            # 验证新值
            if validate and key in env_validators:
                validator = env_validators[key]
                if not validator(value):
                    raise ValueError(f"验证失败: {key} = {value}")
            
            # 记录变更历史
            old_value = env_config.get(key)
            change_record = {
                'timestamp': datetime.now().isoformat(),
                'key': key,
                'old_value': old_value,
                'new_value': value,
                'environment': env_name
            }
            env_history.append(change_record)
            
            # 更新配置
            env_config[key] = value
            
            # 触发监听器
            if key in env_watchers:
                for watcher in env_watchers[key]:
                    watcher(key, old_value, value)
            
            return True
        
        def add_validator(key: str, validator_func: Callable[[Any], bool]) -> None:
            """添加验证器"""
            env_validators[key] = validator_func
        
        def add_watcher(key: str, watcher_func: Callable[[str, Any, Any], None]) -> None:
            """添加监听器"""
            if key not in env_watchers:
                env_watchers[key] = []
            env_watchers[key].append(watcher_func)
        
        def get_history() -> List[Dict[str, Any]]:
            """获取变更历史"""
            return env_history.copy()
        
        def export_config() -> Dict[str, Any]:
            """导出配置"""
            return env_config.copy()
        
        def import_config(config_dict: Dict[str, Any], validate: bool = True) -> None:
            """导入配置"""
            for key, value in config_dict.items():
                set_value(key, value, validate)
        
        def create_nested_scope(scope_name: str):
            """创建嵌套作用域 - 支持配置继承"""
            
            # 嵌套作用域的配置（基于当前环境配置）
            nested_config = env_config.copy()
            nested_history = []
            
            def nested_get(key: str, default: Any = None) -> Any:
                """嵌套作用域的获取方法"""
                # 先查找嵌套配置
                if key in nested_config:
                    return nested_config[key]
                # 再查找父环境配置
                return get(key, default)
            
            def nested_set(key: str, value: Any) -> bool:
                """嵌套作用域的设置方法"""
                nonlocal nested_config
                
                old_value = nested_config.get(key)
                nested_config[key] = value
                
                # 记录嵌套作用域的历史
                nested_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'key': key,
                    'old_value': old_value,
                    'new_value': value,
                    'scope': f"{env_name}.{scope_name}"
                })
                
                return True
            
            def nested_export() -> Dict[str, Any]:
                """导出嵌套配置"""
                return nested_config.copy()
            
            def nested_history_get() -> List[Dict[str, Any]]:
                """获取嵌套作用域历史"""
                return nested_history.copy()
            
            # 返回嵌套作用域接口
            return {
                'get': nested_get,
                'set': nested_set,
                'export': nested_export,
                'history': nested_history_get,
                'scope_name': scope_name
            }
        
        def reset_to_default() -> None:
            """重置到默认配置"""
            nonlocal env_config
            env_config = base_config.copy() if base_config else self.default_config.copy()
            env_history.append({
                'timestamp': datetime.now().isoformat(),
                'action': 'reset_to_default',
                'environment': env_name
            })
        
        # 返回环境管理器接口
        environment = {
            'get': get,
            'set': set_value,
            'add_validator': add_validator,
            'add_watcher': add_watcher,
            'history': get_history,
            'export': export_config,
            'import': import_config,
            'create_scope': create_nested_scope,
            'reset': reset_to_default,
            'env_name': env_name
        }
        
        return environment

def create_advanced_config_system():
    """创建高级配置系统 - 演示复杂的闭包应用"""
    
    # 全局配置存储
    global_configs = {}
    global_watchers = []
    
    def create_config_builder():
        """配置构建器 - 使用链式调用"""
        
        builder_config = {}
        builder_validators = {}
        
        def add_config(key: str, value: Any):
            """添加配置项"""
            nonlocal builder_config
            builder_config[key] = value
            return builder  # 返回自身支持链式调用
        
        def add_validation(key: str, validator: Callable[[Any], bool]):
            """添加验证规则"""
            nonlocal builder_validators
            builder_validators[key] = validator
            return builder
        
        def build(config_name: str):
            """构建最终配置"""
            # 使用闭包保存构建好的配置
            final_config = builder_config.copy()
            final_validators = builder_validators.copy()
            
            def get_config():
                return final_config.copy()
            
            def validate_all():
                """验证所有配置项"""
                results = {}
                for key, value in final_config.items():
                    if key in final_validators:
                        results[key] = final_validators[key](value)
                    else:
                        results[key] = True
                return results
            
            def update_config(updates: Dict[str, Any]):
                """更新配置"""
                nonlocal final_config
                for key, value in updates.items():
                    if key in final_validators:
                        if not final_validators[key](value):
                            raise ValueError(f"验证失败: {key} = {value}")
                    final_config[key] = value
                
                # 通知全局监听器
                for watcher in global_watchers:
                    watcher(config_name, final_config.copy())
            
            # 保存到全局配置
            global_configs[config_name] = {
                'get': get_config,
                'validate': validate_all,
                'update': update_config
            }
            
            return global_configs[config_name]
        
        # 构建器接口
        builder = {
            'add': add_config,
            'validate': add_validation,
            'build': build
        }
        
        return builder
    
    def add_global_watcher(watcher_func: Callable[[str, Dict[str, Any]], None]):
        """添加全局监听器"""
        global_watchers.append(watcher_func)
    
    def get_config(name: str):
        """获取配置"""
        return global_configs.get(name)
    
    def list_configs():
        """列出所有配置"""
        return list(global_configs.keys())
    
    return {
        'create_builder': create_config_builder,
        'add_watcher': add_global_watcher,
        'get': get_config,
        'list': list_configs
    }

# 演示和测试
if __name__ == "__main__":
    print("=== 企业级配置管理器演示 ===")
    
    # 1. 基础配置管理器
    manager = ConfigurationManager({
        'database_url': 'localhost:5432',
        'debug': False,
        'max_connections': 100
    })
    
    # 创建开发环境
    dev_env = manager.create_environment('development', {
        'database_url': 'dev.localhost:5432',
        'debug': True
    })
    
    # 创建生产环境
    prod_env = manager.create_environment('production')
    
    print("1. 基础配置访问:")
    print(f"开发环境数据库: {dev_env['get']('database_url')}")
    print(f"生产环境数据库: {prod_env['get']('database_url')}")
    print(f"开发环境调试: {dev_env['get']('debug')}")
    print(f"生产环境调试: {prod_env['get']('debug')}")
    
    # 2. 验证器演示
    def validate_url(url):
        return isinstance(url, str) and ('localhost' in url or 'prod' in url)
    
    def validate_connections(count):
        return isinstance(count, int) and 1 <= count <= 1000
    
    dev_env['add_validator']('database_url', validate_url)
    dev_env['add_validator']('max_connections', validate_connections)
    
    print("\n2. 验证器测试:")
    try:
        dev_env['set']('database_url', 'dev.localhost:3306')
        print("✓ URL 验证通过")
    except ValueError as e:
        print(f"✗ URL 验证失败: {e}")
    
    try:
        dev_env['set']('max_connections', 2000)
        print("✓ 连接数验证通过")
    except ValueError as e:
        print(f"✗ 连接数验证失败: {e}")
    
    # 3. 监听器演示
    def config_change_logger(key, old_value, new_value):
        print(f"配置变更: {key} 从 {old_value} 改为 {new_value}")
    
    dev_env['add_watcher']('debug', config_change_logger)
    dev_env['add_watcher']('max_connections', config_change_logger)
    
    print("\n3. 监听器测试:")
    dev_env['set']('debug', False)
    dev_env['set']('max_connections', 50)
    
    # 4. 嵌套作用域演示
    print("\n4. 嵌套作用域:")
    test_scope = dev_env['create_scope']('testing')
    
    print(f"测试作用域继承的debug: {test_scope['get']('debug')}")
    test_scope['set']('test_data_size', 1000)
    print(f"测试作用域特有配置: {test_scope['get']('test_data_size')}")
    print(f"父环境看不到: {dev_env['get']('test_data_size', 'NOT_FOUND')}")
    
    # 5. 高级配置系统演示
    print("\n5. 高级配置系统:")
    advanced_system = create_advanced_config_system()
    
    # 全局监听器
    def global_change_logger(config_name, config_data):
        print(f"全局监听: {config_name} 配置已更新")
    
    advanced_system['add_watcher'](global_change_logger)
    
    # 使用构建器模式
    api_config = (advanced_system['create_builder']()
                  .add('host', 'api.example.com')
                  .add('port', 443)
                  .add('ssl', True)
                  .validate('port', lambda x: isinstance(x, int) and 1 <= x <= 65535)
                  .validate('host', lambda x: isinstance(x, str) and len(x) > 0)
                  .build('api_config'))
    
    print(f"API配置: {api_config['get']()}")
    print(f"验证结果: {api_config['validate']()}")
    
    # 更新配置触发监听器
    api_config['update']({'timeout': 30})
    
    print(f"所有配置: {advanced_system['list']()}")
    
    # 6. 历史记录演示
    print("\n6. 变更历史:")
    history = dev_env['history']()
    for record in history[-3:]:  # 显示最近3条记录
        print(f"  {record['timestamp'][:19]}: {record.get('key', 'action')} = {record.get('new_value', record.get('action'))}")
    
    print(f"\n总共 {len(history)} 条变更记录")