"""
命令模式 - 将请求封装成对象
"""

from abc import ABC, abstractmethod

# ==================== 基础命令模式 ====================

class Command(ABC):
    """命令接口"""
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass


class Light:
    """电灯（接收者）"""
    
    def __init__(self):
        self.is_on = False
    
    def turn_on(self):
        self.is_on = True
        print("💡 灯已打开")
    
    def turn_off(self):
        self.is_on = False
        print("🌑 灯已关闭")


class LightOnCommand(Command):
    """开灯命令"""
    
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_on()
    
    def undo(self):
        self.light.turn_off()


class LightOffCommand(Command):
    """关灯命令"""
    
    def __init__(self, light):
        self.light = light
    
    def execute(self):
        self.light.turn_off()
    
    def undo(self):
        self.light.turn_on()


class RemoteControl:
    """遥控器（调用者）"""
    
    def __init__(self):
        self.command = None
        self.history = []
    
    def set_command(self, command):
        self.command = command
    
    def press_button(self):
        if self.command:
            self.command.execute()
            self.history.append(self.command)
    
    def press_undo(self):
        if self.history:
            last_command = self.history.pop()
            last_command.undo()


# 测试
print("=" * 60)
print("基础命令模式")
print("=" * 60)

light = Light()
light_on = LightOnCommand(light)
light_off = LightOffCommand(light)

remote = RemoteControl()

# 开灯
remote.set_command(light_on)
remote.press_button()

# 关灯
remote.set_command(light_off)
remote.press_button()

# 撤销（灯重新打开）
print("\n按下撤销按钮:")
remote.press_undo()


# ==================== 实战：文本编辑器 ====================

class TextEditor:
    """文本编辑器（接收者）"""
    
    def __init__(self):
        self.text = ""
    
    def write(self, text):
        self.text += text
        print(f"✍️  写入: '{text}' → 当前: '{self.text}'")
    
    def delete(self, length):
        deleted = self.text[-length:]
        self.text = self.text[:-length]
        print(f"🗑️  删除: '{deleted}' → 当前: '{self.text}'")
        return deleted


class WriteCommand(Command):
    """写入命令"""
    
    def __init__(self, editor, text):
        self.editor = editor
        self.text = text
    
    def execute(self):
        self.editor.write(self.text)
    
    def undo(self):
        self.editor.delete(len(self.text))


class DeleteCommand(Command):
    """删除命令"""
    
    def __init__(self, editor, length):
        self.editor = editor
        self.length = length
        self.deleted_text = ""
    
    def execute(self):
        self.deleted_text = self.editor.delete(self.length)
    
    def undo(self):
        self.editor.write(self.deleted_text)


class CommandHistory:
    """命令历史管理器"""
    
    def __init__(self):
        self.history = []
        self.current = -1
    
    def execute(self, command):
        """执行命令并记录"""
        command.execute()
        # 清除当前位置之后的历史
        self.history = self.history[:self.current + 1]
        self.history.append(command)
        self.current += 1
    
    def undo(self):
        """撤销"""
        if self.current >= 0:
            self.history[self.current].undo()
            self.current -= 1
            print("↩️  已撤销")
        else:
            print("❌ 无法撤销")
    
    def redo(self):
        """重做"""
        if self.current < len(self.history) - 1:
            self.current += 1
            self.history[self.current].execute()
            print("↪️  已重做")
        else:
            print("❌ 无法重做")


# 测试
print("\n" + "=" * 60)
print("实战：文本编辑器（支持撤销/重做）")
print("=" * 60)

editor = TextEditor()
history = CommandHistory()

# 执行一系列操作
history.execute(WriteCommand(editor, "Hello"))
history.execute(WriteCommand(editor, " World"))
history.execute(WriteCommand(editor, "!"))

print("\n撤销操作:")
history.undo()
history.undo()

print("\n重做操作:")
history.redo()

print("\n继续写入:")
history.execute(WriteCommand(editor, "???"))


# ==================== 实战：任务队列 ====================

class TaskQueue:
    """任务队列"""
    
    def __init__(self):
        self.queue = []
    
    def add_command(self, command):
        """添加命令到队列"""
        self.queue.append(command)
        print(f"📋 添加任务到队列 (共 {len(self.queue)} 个)")
    
    def execute_all(self):
        """执行所有命令"""
        print(f"\n🚀 开始执行 {len(self.queue)} 个任务:")
        while self.queue:
            command = self.queue.pop(0)
            command.execute()


class EmailCommand(Command):
    """发送邮件命令"""
    
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
    
    def execute(self):
        print(f"  📧 发送邮件给 {self.to}: {self.subject}")
    
    def undo(self):
        print(f"  ↩️  撤回邮件")


class SMSCommand(Command):
    """发送短信命令"""
    
    def __init__(self, phone, message):
        self.phone = phone
        self.message = message
    
    def execute(self):
        print(f"  📱 发送短信到 {self.phone}: {self.message}")
    
    def undo(self):
        pass


# 测试
print("\n" + "=" * 60)
print("实战：任务队列")
print("=" * 60)

queue = TaskQueue()

# 添加任务
queue.add_command(EmailCommand("alice@example.com", "欢迎"))
queue.add_command(SMSCommand("138****1234", "验证码: 1234"))
queue.add_command(EmailCommand("bob@example.com", "提醒"))

# 批量执行
queue.execute_all()


# ==================== 宏命令 ====================

class MacroCommand(Command):
    """宏命令（组合多个命令）"""
    
    def __init__(self):
        self.commands = []
    
    def add(self, command):
        self.commands.append(command)
    
    def execute(self):
        print("🎯 执行宏命令:")
        for command in self.commands:
            command.execute()
    
    def undo(self):
        print("↩️  撤销宏命令:")
        for command in reversed(self.commands):
            command.undo()


# 测试
print("\n" + "=" * 60)
print("宏命令（批量操作）")
print("=" * 60)

# 创建宏命令
macro = MacroCommand()
light1 = Light()
light2 = Light()

macro.add(LightOnCommand(light1))
macro.add(LightOnCommand(light2))

print("执行宏命令（同时开两盏灯）:")
macro.execute()

print("\n撤销宏命令:")
macro.undo()


print("\n✅ 命令模式完成！")