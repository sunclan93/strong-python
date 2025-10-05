"""
设计模式总结 - 综合应用示例
整合多个模式构建一个完整系统
"""

from abc import ABC, abstractmethod
from typing import List
import copy

# ==================== 综合项目：通知系统 ====================

# 1. 单例模式 - 通知管理器
class NotificationManager:
    """通知管理器（单例）"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._observers = []
            self._strategy = None
            self._initialized = True
    
    # 观察者模式
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self, message):
        print(f"\n📢 通知 {len(self._observers)} 个观察者")
        for observer in self._observers:
            observer.update(message)
    
    # 策略模式
    def set_priority_strategy(self, strategy):
        self._strategy = strategy
    
    def send(self, message):
        if self._strategy:
            priority = self._strategy.calculate_priority(message)
            print(f"🎯 消息优先级: {priority}")
        self.notify(message)


# 2. 观察者模式 - 不同的通知渠道
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


class EmailNotifier(Observer):
    def update(self, message):
        print(f"  📧 邮件: {message}")


class SMSNotifier(Observer):
    def update(self, message):
        print(f"  📱 短信: {message}")


class PushNotifier(Observer):
    def update(self, message):
        print(f"  🔔 推送: {message}")


# 3. 策略模式 - 优先级计算
class PriorityStrategy(ABC):
    @abstractmethod
    def calculate_priority(self, message):
        pass


class UrgentStrategy(PriorityStrategy):
    def calculate_priority(self, message):
        return "🔴 紧急" if "紧急" in message else "🟢 普通"


class LengthStrategy(PriorityStrategy):
    def calculate_priority(self, message):
        return "🔴 高" if len(message) > 20 else "🟢 低"


# 4. 工厂模式 - 创建通知器
class NotifierFactory:
    @staticmethod
    def create_notifier(notifier_type):
        notifiers = {
            'email': EmailNotifier,
            'sms': SMSNotifier,
            'push': PushNotifier
        }
        notifier_class = notifiers.get(notifier_type)
        if not notifier_class:
            raise ValueError(f"未知的通知类型: {notifier_type}")
        return notifier_class()


# 5. 建造者模式 - 构建复杂通知
class Notification:
    def __init__(self):
        self.title = ""
        self.content = ""
        self.receivers = []
        self.attachments = []
    
    def __repr__(self):
        return f"Notification(title='{self.title}', receivers={self.receivers})"


class NotificationBuilder:
    def __init__(self):
        self.notification = Notification()
    
    def set_title(self, title):
        self.notification.title = title
        return self
    
    def set_content(self, content):
        self.notification.content = content
        return self
    
    def add_receiver(self, receiver):
        self.notification.receivers.append(receiver)
        return self
    
    def add_attachment(self, attachment):
        self.notification.attachments.append(attachment)
        return self
    
    def build(self):
        return self.notification


# 6. 命令模式 - 可撤销的操作
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass


class SendNotificationCommand(Command):
    def __init__(self, manager, message):
        self.manager = manager
        self.message = message
    
    def execute(self):
        print(f"\n✅ 执行发送命令")
        self.manager.send(self.message)
    
    def undo(self):
        print(f"↩️  撤销发送（模拟）")


# 7. 装饰器模式 - 增强通知功能
class NotificationDecorator(Observer):
    def __init__(self, notifier):
        self._notifier = notifier
    
    def update(self, message):
        self._notifier.update(message)


class LoggingDecorator(NotificationDecorator):
    """添加日志功能"""
    
    def update(self, message):
        print(f"    📝 [日志] 发送通知: {message[:20]}...")
        super().update(message)


class RetryDecorator(NotificationDecorator):
    """添加重试功能"""
    
    def __init__(self, notifier, max_retries=3):
        super().__init__(notifier)
        self.max_retries = max_retries
    
    def update(self, message):
        print(f"    🔄 [重试] 最多重试 {self.max_retries} 次")
        super().update(message)


# ==================== 测试综合系统 ====================

print("=" * 70)
print("设计模式综合应用 - 通知系统")
print("=" * 70)

# 1. 获取单例管理器
manager = NotificationManager()

# 2. 使用工厂创建通知器
email = NotifierFactory.create_notifier('email')
sms = NotifierFactory.create_notifier('sms')
push = NotifierFactory.create_notifier('push')

# 3. 使用装饰器增强功能
email_with_log = LoggingDecorator(email)
sms_with_retry = RetryDecorator(sms)

# 4. 注册观察者
manager.attach(email_with_log)
manager.attach(sms_with_retry)
manager.attach(push)

# 5. 设置策略
manager.set_priority_strategy(UrgentStrategy())

# 6. 使用建造者创建复杂通知
notification = (NotificationBuilder()
    .set_title("系统维护通知")
    .set_content("系统将于今晚进行维护")
    .add_receiver("user@example.com")
    .add_receiver("admin@example.com")
    .build())

print(f"\n📋 创建通知: {notification}")

# 7. 使用命令模式发送
command = SendNotificationCommand(manager, "紧急：系统故障，请立即处理！")
command.execute()

# 8. 切换策略
print("\n" + "=" * 70)
print("切换到长度策略")
print("=" * 70)
manager.set_priority_strategy(LengthStrategy())
manager.send("短消息")
manager.send("这是一条很长很长很长很长的消息，应该被标记为高优先级")


# ==================== 设计模式对比表 ====================

print("\n" + "=" * 70)
print("设计模式总结")
print("=" * 70)

patterns_summary = """
创建型模式 (How to create objects)
├─ 单例 Singleton       → 全局唯一实例
├─ 工厂 Factory         → 解耦对象创建
├─ 建造者 Builder       → 分步骤构建复杂对象
└─ 原型 Prototype       → 克隆对象

结构型模式 (How to compose objects)
├─ 适配器 Adapter       → 接口转换
├─ 装饰器 Decorator     → 动态添加功能
└─ 代理 Proxy           → 控制访问

行为型模式 (How objects interact)
├─ 观察者 Observer      → 一对多通知
├─ 策略 Strategy        → 算法替换
└─ 命令 Command         → 请求封装
"""

print(patterns_summary)


# ==================== 模式组合使用指南 ====================

print("=" * 70)
print("常见模式组合")
print("=" * 70)

combinations = """
1. 单例 + 观察者
   → 全局事件管理器
   
2. 工厂 + 策略
   → 根据配置创建不同策略
   
3. 建造者 + 装饰器
   → 构建后增强功能
   
4. 命令 + 观察者
   → 可撤销的事件系统
   
5. 策略 + 适配器
   → 统一不同算法接口
"""

print(combinations)


# ==================== 实践建议 ====================

print("=" * 70)
print("设计模式使用建议")
print("=" * 70)

advice = """
✅ 何时使用设计模式：
  • 代码有明显的重复
  • 需要高扩展性
  • 团队协作的大型项目
  • 框架/库的设计

❌ 何时不用设计模式：
  • 简单的一次性脚本
  • 过度设计（YAGNI原则）
  • 团队不熟悉模式
  • 为了模式而模式

💡 学习路径：
  1. 先理解问题（不要急着套模式）
  2. 识别模式的适用场景
  3. 实现最简单的版本
  4. 逐步重构优化
  5. 阅读优秀开源代码
"""

print(advice)


print("\n✅ 设计模式总结完成！")