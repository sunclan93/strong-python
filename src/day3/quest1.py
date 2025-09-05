"""
权限检查装饰器系统
你的任务：实现标记为 # TODO 的方法和功能
"""

import functools
from typing import List, Set, Dict, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


# ==== 第一部分：权限系统基础类 ====

class PermissionError(Exception):
    """权限不足异常"""
    pass


class Role(Enum):
    """角色枚举"""
    GUEST = "guest"
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


@dataclass
class User:
    """用户类"""
    id: int
    username: str
    roles: Set[Role]
    permissions: Set[str]
    is_active: bool = True
    
    def has_role(self, role: Role) -> bool:
        """检查用户是否有指定角色"""
        return role in self.roles
    
    def has_permission(self, permission: str) -> bool:
        """检查用户是否有指定权限"""
        # TODO: 实现权限检查逻辑
        # 提示：检查 self.permissions 中是否包含该权限
        return permission in self.permissions

        
    
    def has_any_role(self, roles: List[Role]) -> bool:
        """检查用户是否有任意一个指定角色"""
        # TODO: 实现逻辑
        # 提示：检查 roles 列表中是否有任何一个角色在 self.roles 中
        return bool(set(roles)&self.roles) # 使用集合取交集
    
    def has_all_roles(self, roles: List[Role]) -> bool:
        """检查用户是否拥有所有指定角色"""
        # TODO: 实现逻辑
        # 提示：检查 roles 列表中的所有角色是否都在 self.roles 中
        return set(roles).issubset(self.roles) # 集合操作


class PermissionRegistry:
    """权限注册表 - 管理角色和权限的映射关系"""
    
    def __init__(self):
        # 角色继承关系：高级角色继承低级角色的所有权限
        self.role_hierarchy = {
            Role.SUPER_ADMIN: [Role.ADMIN, Role.MODERATOR, Role.USER, Role.GUEST],
            Role.ADMIN: [Role.MODERATOR, Role.USER, Role.GUEST],
            Role.MODERATOR: [Role.USER, Role.GUEST],
            Role.USER: [Role.GUEST],
            Role.GUEST: []
        }
        
        # 角色默认权限
        self.role_permissions = {
            Role.GUEST: {'read_public'},
            Role.USER: {'read_public', 'read_user', 'write_user'},
            Role.MODERATOR: {'read_public', 'read_user', 'write_user', 'moderate_content'},
            Role.ADMIN: {'read_public', 'read_user', 'write_user', 'moderate_content', 'admin_panel'},
            Role.SUPER_ADMIN: {'*'}  # 所有权限
        }
    
    def get_effective_permissions(self, roles: Set[Role]) -> Set[str]:
        """获取角色的有效权限（包括继承的权限）"""
        # TODO: 实现权限继承逻辑
        # 提示：
        # 1. 遍历用户的所有角色
        # 2. 对每个角色，获取其直接权限和继承权限
        # 3. 合并所有权限
        # 4. 处理 '*' 通配符权限
        
        for role in roles:
            permissions = self.get_effective_permissions(role)
            

        pass


# ==== 第二部分：权限装饰器实现 ====

class AuthContext:
    """认证上下文 - 存储当前用户信息"""
    _current_user: Optional[User] = None
    
    @classmethod
    def set_current_user(cls, user: User):
        """设置当前用户"""
        cls._current_user = user
    
    @classmethod
    def get_current_user(cls) -> Optional[User]:
        """获取当前用户"""
        return cls._current_user
    
    @classmethod
    def clear_current_user(cls):
        """清除当前用户"""
        cls._current_user = None


class PermissionChecker:
    """权限检查器"""
    
    def __init__(self):
        self.registry = PermissionRegistry()
        self.audit_log = []  # 审计日志
    
    def require_permission(self, 
                         permission: str = None,
                         roles: List[Role] = None,
                         require_all_roles: bool = False,
                         allow_owner: bool = False,
                         custom_check: Callable = None):
        """
        权限检查装饰器
        
        Args:
            permission: 需要的权限
            roles: 需要的角色列表
            require_all_roles: 是否需要所有角色
            allow_owner: 是否允许资源所有者访问
            custom_check: 自定义检查函数
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                user = AuthContext.get_current_user()
                
                # 检查用户是否已登录
                if not user:
                    self._log_access_attempt(func.__name__, None, False, "用户未登录")
                    raise PermissionError("请先登录")
                
                # 检查用户是否激活
                if not user.is_active:
                    self._log_access_attempt(func.__name__, user.username, False, "用户账户已禁用")
                    raise PermissionError("账户已禁用")
                
                # TODO: 实现权限检查逻辑
                # 提示：
                # 1. 如果指定了 permission，检查用户是否有该权限
                # 2. 如果指定了 roles，检查用户是否有相应角色
                # 3. 如果指定了 custom_check，执行自定义检查
                # 4. 记录访问日志
                # 5. 权限不足时抛出 PermissionError
                
                pass
            
            return wrapper
        return decorator
    
    def require_login(self, func):
        """只需要登录的装饰器"""
        # TODO: 实现只检查登录状态的装饰器
        pass
    
    def require_role(self, *roles: Role, require_all: bool = False):
        """角色检查装饰器"""
        # TODO: 实现角色检查装饰器
        # 提示：可以复用 require_permission 装饰器
        pass
    
    def _log_access_attempt(self, function_name: str, username: str, success: bool, reason: str = ""):
        """记录访问尝试"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'function': function_name,
            'username': username,
            'success': success,
            'reason': reason
        }
        self.audit_log.append(log_entry)
        
        # 保留最近1000条记录
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def get_audit_log(self, username: str = None, function_name: str = None) -> List[Dict]:
        """获取审计日志"""
        logs = self.audit_log
        
        if username:
            logs = [log for log in logs if log['username'] == username]
        
        if function_name:
            logs = [log for log in logs if log['function'] == function_name]
        
        return logs


# ==== 第三部分：测试系统 ====

def test_permission_system():
    """测试权限系统"""
    print("=== 权限系统测试 ===\n")
    
    # 创建权限检查器
    checker = PermissionChecker()
    
    # 创建测试用户
    guest_user = User(
        id=1, 
        username="guest", 
        roles={Role.GUEST}, 
        permissions=set()
    )
    
    admin_user = User(
        id=2, 
        username="admin", 
        roles={Role.ADMIN}, 
        permissions=set()
    )
    
    # 定义受保护的函数
    @checker.require_permission(permission="admin_panel")
    def admin_only_function():
        return "这是管理员专用功能"
    
    @checker.require_role(Role.USER, Role.MODERATOR, require_all=False)
    def user_or_moderator_function():
        return "用户或版主可以访问"
    
    @checker.require_login
    def logged_in_user_function():
        return "任何登录用户都可以访问"
    
    # 测试未登录访问
    print("1️⃣ 测试未登录访问")
    try:
        admin_only_function()
    except PermissionError as e:
        print(f"❌ 预期错误: {e}")
    
    # 测试普通用户访问管理员功能
    print("\n2️⃣ 测试普通用户访问管理员功能")
    AuthContext.set_current_user(guest_user)
    try:
        admin_only_function()
    except PermissionError as e:
        print(f"❌ 预期错误: {e}")
    
    # 测试管理员访问
    print("\n3️⃣ 测试管理员访问")
    AuthContext.set_current_user(admin_user)
    try:
        result = admin_only_function()
        print(f"✅ 管理员访问成功: {result}")
    except PermissionError as e:
        print(f"❌ 意外错误: {e}")
    
    # 查看审计日志
    print("\n4️⃣ 审计日志")
    logs = checker.get_audit_log()
    for log in logs[-5:]:  # 显示最后5条记录
        status = "✅" if log['success'] else "❌"
        print(f"{status} {log['timestamp'][:19]} - {log['username']} 访问 {log['function']} - {log['reason']}")


def advanced_permission_examples():
    """高级权限示例"""
    print("\n=== 高级权限示例 ===\n")
    
    checker = PermissionChecker()
    
    # 自定义权限检查
    def owner_check(*args, **kwargs):
        """检查是否是资源所有者"""
        user = AuthContext.get_current_user()
        resource_owner_id = kwargs.get('owner_id')
        return user and user.id == resource_owner_id
    
    @checker.require_permission(
        permission="edit_post",
        custom_check=owner_check
    )
    def edit_post(post_id: int, owner_id: int, content: str):
        return f"编辑帖子 {post_id}: {content}"
    
    # 组合权限检查
    @checker.require_role(Role.MODERATOR)
    @checker.require_permission("moderate_content")
    def moderate_post(post_id: int):
        return f"审核帖子 {post_id}"
    
    print("高级权限示例定义完成")


if __name__ == "__main__":
    print("🎯 你的任务：")
    print("1. 实现 User 类的权限检查方法")
    print("2. 实现 PermissionRegistry 的权限继承逻辑")
    print("3. 实现 PermissionChecker 的核心装饰器")
    print("4. 测试各种权限场景")
    print()
    print("💡 实现提示：")
    print("- 先实现简单的权限检查")
    print("- 再实现角色继承")
    print("- 最后实现复杂的组合权限")
    print("- 记得处理边界情况")
    print()
    
    # 取消注释来测试你的实现
    test_permission_system()
    # advanced_permission_examples()