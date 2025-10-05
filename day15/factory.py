"""
工厂模式 - 从简单到抽象
"""

from abc import ABC, abstractmethod

# ==================== 简单工厂 ====================

class Button:
    """按钮基类"""
    def render(self):
        pass


class WindowsButton(Button):
    def render(self):
        return "🖱️ Windows 风格按钮"


class MacButton(Button):
    def render(self):
        return "🖱️ Mac 风格按钮"


class LinuxButton(Button):
    def render(self):
        return "🖱️ Linux 风格按钮"


class ButtonFactory:
    """按钮工厂（简单工厂）"""
    
    @staticmethod
    def create_button(os_type):
        if os_type == 'windows':
            return WindowsButton()
        elif os_type == 'mac':
            return MacButton()
        elif os_type == 'linux':
            return LinuxButton()
        else:
            raise ValueError(f"不支持的系统: {os_type}")


# 测试简单工厂
print("简单工厂模式")
button = ButtonFactory.create_button('mac')
print(button.render())


# ==================== 工厂方法 ====================

class Dialog(ABC):
    """对话框抽象类"""
    
    @abstractmethod
    def create_button(self):
        """工厂方法：子类实现"""
        pass
    
    def render(self):
        """使用工厂方法创建按钮"""
        button = self.create_button()
        return f"对话框显示: {button.render()}"


class WindowsDialog(Dialog):
    def create_button(self):
        return WindowsButton()


class MacDialog(Dialog):
    def create_button(self):
        return MacButton()


# 测试工厂方法
print("\n工厂方法模式")
dialog = MacDialog()
print(dialog.render())


# ==================== 抽象工厂 ====================

class GUIFactory(ABC):
    """GUI 抽象工厂"""
    
    @abstractmethod
    def create_button(self):
        pass
    
    @abstractmethod
    def create_checkbox(self):
        pass


class Checkbox(ABC):
    @abstractmethod
    def check(self):
        pass


class WindowsCheckbox(Checkbox):
    def check(self):
        return "☑️ Windows 复选框"


class MacCheckbox(Checkbox):
    def check(self):
        return "☑️ Mac 复选框"


class WindowsFactory(GUIFactory):
    def create_button(self):
        return WindowsButton()
    
    def create_checkbox(self):
        return WindowsCheckbox()


class MacFactory(GUIFactory):
    def create_button(self):
        return MacButton()
    
    def create_checkbox(self):
        return MacCheckbox()


# 客户端代码
def render_ui(factory: GUIFactory):
    """使用工厂创建 UI 组件"""
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    
    print(button.render())
    print(checkbox.check())


# 测试抽象工厂
print("\n抽象工厂模式")
print("Mac 风格:")
render_ui(MacFactory())

print("\nWindows 风格:")
render_ui(WindowsFactory())


# ==================== 实战：数据库连接器 ====================

class Database(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def query(self, sql):
        pass


class MySQL(Database):
    def connect(self):
        return "🔌 连接到 MySQL"
    
    def query(self, sql):
        return f"MySQL 执行: {sql}"


class PostgreSQL(Database):
    def connect(self):
        return "🔌 连接到 PostgreSQL"
    
    def query(self, sql):
        return f"PostgreSQL 执行: {sql}"


class MongoDB(Database):
    def connect(self):
        return "🔌 连接到 MongoDB"
    
    def query(self, sql):
        return f"MongoDB 执行: {sql}"


class DatabaseFactory:
    """数据库工厂"""
    
    _creators = {
        'mysql': MySQL,
        'postgresql': PostgreSQL,
        'mongodb': MongoDB,
    }
    
    @classmethod
    def create(cls, db_type):
        creator = cls._creators.get(db_type)
        if not creator:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        return creator()
    
    @classmethod
    def register(cls, name, creator):
        """注册新的数据库类型"""
        cls._creators[name] = creator


# 测试数据库工厂
print("\n实战：数据库连接器")
db = DatabaseFactory.create('mysql')
print(db.connect())
print(db.query("SELECT * FROM users"))


print("\n✅ 工厂模式学习完成！")