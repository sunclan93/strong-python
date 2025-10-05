"""
观察者模式 - 发布订阅机制
"""

from abc import ABC, abstractmethod

# ==================== 基础观察者模式 ====================

class Observer(ABC):
    """观察者接口"""
    
    @abstractmethod
    def update(self, subject):
        pass


class Subject:
    """主题/被观察者"""
    
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        """订阅"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"✅ {observer.__class__.__name__} 已订阅")
    
    def detach(self, observer):
        """取消订阅"""
        self._observers.remove(observer)
        print(f"❌ {observer.__class__.__name__} 已取消订阅")
    
    def notify(self):
        """通知所有观察者"""
        print(f"📢 通知 {len(self._observers)} 个观察者")
        for observer in self._observers:
            observer.update(self)
    
    def set_state(self, state):
        """改变状态并通知"""
        print(f"\n🔄 状态改变: {self._state} → {state}")
        self._state = state
        self.notify()
    
    def get_state(self):
        return self._state


# 具体观察者
class EmailObserver(Observer):
    """邮件观察者"""
    
    def update(self, subject):
        state = subject.get_state()
        print(f"  📧 邮件通知: 状态变为 {state}")


class SMSObserver(Observer):
    """短信观察者"""
    
    def update(self, subject):
        state = subject.get_state()
        print(f"  📱 短信通知: 状态变为 {state}")


class LogObserver(Observer):
    """日志观察者"""
    
    def update(self, subject):
        state = subject.get_state()
        print(f"  📝 日志记录: 状态变为 {state}")


# 测试
print("=" * 60)
print("基础观察者模式")
print("=" * 60)

subject = Subject()

# 订阅
email = EmailObserver()
sms = SMSObserver()
log = LogObserver()

subject.attach(email)
subject.attach(sms)
subject.attach(log)

# 改变状态
subject.set_state("就绪")
subject.set_state("运行中")

# 取消订阅
subject.detach(sms)
subject.set_state("完成")


# ==================== 实战：股票监控系统 ====================

class Stock:
    """股票（被观察者）"""
    
    def __init__(self, symbol, price):
        self.symbol = symbol
        self._price = price
        self._observers = []
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        old_price = self._price
        self._price = value
        change = ((value - old_price) / old_price) * 100
        print(f"\n💹 {self.symbol}: ¥{old_price} → ¥{value} ({change:+.2f}%)")
        self.notify()


class Investor(Observer):
    """投资者（观察者）"""
    
    def __init__(self, name, buy_threshold, sell_threshold):
        self.name = name
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
    
    def update(self, stock):
        if stock.price <= self.buy_threshold:
            print(f"  💰 {self.name}: 建议买入 {stock.symbol}")
        elif stock.price >= self.sell_threshold:
            print(f"  💸 {self.name}: 建议卖出 {stock.symbol}")
        else:
            print(f"  ⏸️  {self.name}: 继续观望")


# 测试
print("\n" + "=" * 60)
print("实战：股票监控系统")
print("=" * 60)

stock = Stock("AAPL", 150)

# 投资者订阅
investor1 = Investor("张三", buy_threshold=140, sell_threshold=160)
investor2 = Investor("李四", buy_threshold=145, sell_threshold=155)

stock.attach(investor1)
stock.attach(investor2)

# 价格变化
stock.price = 145  # 下跌
stock.price = 155  # 上涨
stock.price = 135  # 大跌


# ==================== 事件系统（推荐）====================

class EventManager:
    """事件管理器"""
    
    def __init__(self):
        self._listeners = {}
    
    def subscribe(self, event_type, listener):
        """订阅事件"""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)
        print(f"✅ 订阅事件: {event_type}")
    
    def unsubscribe(self, event_type, listener):
        """取消订阅"""
        self._listeners[event_type].remove(listener)
    
    def notify(self, event_type, data=None):
        """触发事件"""
        print(f"\n🔔 触发事件: {event_type}")
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener(data)


# 测试
print("\n" + "=" * 60)
print("事件系统")
print("=" * 60)

events = EventManager()

# 定义监听器
def on_user_login(data):
    print(f"  👤 用户登录: {data['username']}")

def send_welcome_email(data):
    print(f"  📧 发送欢迎邮件给: {data['username']}")

def log_login(data):
    print(f"  📝 记录登录日志: {data}")

# 订阅事件
events.subscribe("user_login", on_user_login)
events.subscribe("user_login", send_welcome_email)
events.subscribe("user_login", log_login)

# 触发事件
events.notify("user_login", {"username": "Alice", "ip": "192.168.1.1"})
events.notify("user_login", {"username": "Bob", "ip": "192.168.1.2"})


print("\n✅ 观察者模式完成！")