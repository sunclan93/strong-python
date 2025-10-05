"""
代理模式 - 为对象提供访问控制
"""

from abc import ABC, abstractmethod

# ==================== 虚拟代理（懒加载）====================

class Image(ABC):
    """图片接口"""
    
    @abstractmethod
    def display(self):
        pass


class RealImage(Image):
    """真实图片（加载耗时）"""
    
    def __init__(self, filename):
        self.filename = filename
        self._load_from_disk()
    
    def _load_from_disk(self):
        print(f"📥 加载图片: {self.filename}（耗时操作）")
    
    def display(self):
        print(f"🖼️  显示图片: {self.filename}")


class ImageProxy(Image):
    """图片代理（懒加载）"""
    
    def __init__(self, filename):
        self.filename = filename
        self._real_image = None
    
    def display(self):
        # 只在需要时才加载真实图片
        if self._real_image is None:
            self._real_image = RealImage(self.filename)
        self._real_image.display()


# 测试
print("虚拟代理 - 图片懒加载")
print("创建代理对象（不加载图片）")
image1 = ImageProxy("photo1.jpg")
image2 = ImageProxy("photo2.jpg")

print("\n第一次显示 image1（触发加载）")
image1.display()

print("\n第二次显示 image1（直接显示）")
image1.display()

print("\n显示 image2（触发加载）")
image2.display()


# ==================== 保护代理（权限控制）====================

class BankAccount(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass
    
    @abstractmethod
    def withdraw(self, amount):
        pass
    
    @abstractmethod
    def get_balance(self):
        pass


class RealBankAccount(BankAccount):
    """真实账户"""
    
    def __init__(self, balance=0):
        self._balance = balance
    
    def deposit(self, amount):
        self._balance += amount
        print(f"💰 存款: ¥{amount}, 余额: ¥{self._balance}")
    
    def withdraw(self, amount):
        if amount > self._balance:
            print(f"❌ 余额不足")
            return
        self._balance -= amount
        print(f"💸 取款: ¥{amount}, 余额: ¥{self._balance}")
    
    def get_balance(self):
        return self._balance


class ProtectedBankAccount(BankAccount):
    """保护代理（权限控制）"""
    
    def __init__(self, account, password):
        self._account = account
        self._password = password
        self._is_authenticated = False
    
    def authenticate(self, password):
        """验证密码"""
        if password == self._password:
            self._is_authenticated = True
            print("✅ 验证成功")
        else:
            print("❌ 密码错误")
    
    def deposit(self, amount):
        self._account.deposit(amount)
    
    def withdraw(self, amount):
        if not self._is_authenticated:
            print("🔒 请先验证身份")
            return
        self._account.withdraw(amount)
    
    def get_balance(self):
        if not self._is_authenticated:
            print("🔒 请先验证身份")
            return None
        return self._account.get_balance()


# 测试
print("\n\n保护代理 - 银行账户权限控制")
real_account = RealBankAccount(1000)
protected = ProtectedBankAccount(real_account, "123456")

print("尝试取款（未验证）")
protected.withdraw(100)

print("\n使用错误密码验证")
protected.authenticate("wrong")

print("\n使用正确密码验证")
protected.authenticate("123456")

print("\n再次尝试取款")
protected.withdraw(100)

print(f"\n查询余额: ¥{protected.get_balance()}")


# ==================== 缓存代理 ====================

class DataService(ABC):
    @abstractmethod
    def get_data(self, key):
        pass


class RealDataService(DataService):
    """真实数据服务（慢）"""
    
    def get_data(self, key):
        print(f"🔍 从数据库查询: {key}（慢）")
        # 模拟数据库查询
        return f"数据_{key}"


class CachedDataService(DataService):
    """缓存代理"""
    
    def __init__(self, service):
        self._service = service
        self._cache = {}
    
    def get_data(self, key):
        if key in self._cache:
            print(f"⚡ 从缓存返回: {key}")
            return self._cache[key]
        
        # 缓存未命中，查询真实服务
        data = self._service.get_data(key)
        self._cache[key] = data
        return data


# 测试
print("\n\n缓存代理")
real_service = RealDataService()
cached_service = CachedDataService(real_service)

print("第一次查询 user_1:")
cached_service.get_data("user_1")

print("\n第二次查询 user_1:")
cached_service.get_data("user_1")

print("\n查询 user_2:")
cached_service.get_data("user_2")


# ==================== 日志代理 ====================

class Calculator(ABC):
    @abstractmethod
    def add(self, a, b):
        pass
    
    @abstractmethod
    def multiply(self, a, b):
        pass


class SimpleCalculator(Calculator):
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b


class LoggingCalculator(Calculator):
    """日志代理"""
    
    def __init__(self, calculator):
        self._calculator = calculator
    
    def add(self, a, b):
        print(f"📝 调用 add({a}, {b})")
        result = self._calculator.add(a, b)
        print(f"📝 返回 {result}")
        return result
    
    def multiply(self, a, b):
        print(f"📝 调用 multiply({a}, {b})")
        result = self._calculator.multiply(a, b)
        print(f"📝 返回 {result}")
        return result


# 测试
print("\n\n日志代理")
calc = SimpleCalculator()
logged_calc = LoggingCalculator(calc)

logged_calc.add(5, 3)
logged_calc.multiply(4, 7)


print("\n✅ 代理模式完成！")