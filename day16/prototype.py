"""
原型模式 - 通过克隆创建对象
"""

import copy

# ==================== 基础原型 ====================

class Prototype:
    """原型基类"""
    
    def clone(self):
        """浅拷贝"""
        return copy.copy(self)
    
    def deep_clone(self):
        """深拷贝"""
        return copy.deepcopy(self)


class Document(Prototype):
    """文档类"""
    
    def __init__(self, title, content, metadata=None):
        self.title = title
        self.content = content
        self.metadata = metadata or {}
    
    def __repr__(self):
        return f"Document('{self.title}')"


# 测试
print("原型模式 - 基础克隆")
doc1 = Document("报告", "这是内容", {"author": "Alice"})

# 克隆文档
doc2 = doc1.clone()
doc2.title = "报告副本"

print(f"原始: {doc1.title}")
print(f"克隆: {doc2.title}")
print(f"是同一对象吗? {doc1 is doc2}")


# ==================== 浅拷贝 vs 深拷贝 ====================

print("\n浅拷贝 vs 深拷贝")

doc3 = Document("文档3", "内容", {"tags": ["重要", "紧急"]})

# 浅拷贝
shallow = doc3.clone()
shallow.metadata["tags"].append("新标签")

print(f"原始的 tags: {doc3.metadata['tags']}")  # 被修改了！
print(f"浅拷贝的 tags: {shallow.metadata['tags']}")

# 深拷贝
doc4 = Document("文档4", "内容", {"tags": ["标签1"]})
deep = doc4.deep_clone()
deep.metadata["tags"].append("标签2")

print(f"原始的 tags: {doc4.metadata['tags']}")  # 未被修改
print(f"深拷贝的 tags: {deep.metadata['tags']}")


# ==================== 实战：游戏角色模板 ====================

class Character(Prototype):
    """游戏角色"""
    
    def __init__(self, name, level, skills, equipment):
        self.name = name
        self.level = level
        self.skills = skills.copy()  # 注意这里
        self.equipment = equipment.copy()
    
    def __repr__(self):
        return f"{self.name} (Lv.{self.level})"


print("\n实战：游戏角色克隆")

# 创建战士模板
warrior_template = Character(
    "战士模板",
    level=1,
    skills=["重击", "防御"],
    equipment=["木剑", "布甲"]
)

# 克隆创建新角色
warrior1 = warrior_template.deep_clone()
warrior1.name = "战士01"
warrior1.level = 10
warrior1.skills.append("旋风斩")

warrior2 = warrior_template.deep_clone()
warrior2.name = "战士02"
warrior2.level = 5

print(f"模板: {warrior_template}, 技能: {warrior_template.skills}")
print(f"角色1: {warrior1}, 技能: {warrior1.skills}")
print(f"角色2: {warrior2}, 技能: {warrior2.skills}")


# ==================== 原型管理器 ====================

class PrototypeManager:
    """原型管理器"""
    
    def __init__(self):
        self._prototypes = {}
    
    def register(self, name, prototype):
        """注册原型"""
        self._prototypes[name] = prototype
    
    def unregister(self, name):
        """注销原型"""
        del self._prototypes[name]
    
    def create(self, name):
        """克隆并返回"""
        prototype = self._prototypes.get(name)
        if not prototype:
            raise ValueError(f"原型 '{name}' 不存在")
        return prototype.deep_clone()


# 测试原型管理器
print("\n原型管理器")
manager = PrototypeManager()

# 注册不同职业模板
manager.register("warrior", Character("战士", 1, ["重击"], ["木剑"]))
manager.register("mage", Character("法师", 1, ["火球"], ["木杖"]))
manager.register("archer", Character("弓箭手", 1, ["射击"], ["木弓"]))

# 快速创建角色
hero1 = manager.create("warrior")
hero1.name = "英雄战士"

hero2 = manager.create("mage")
hero2.name = "魔法师"

print(f"创建: {hero1}")
print(f"创建: {hero2}")


print("\n✅ 原型模式完成！")