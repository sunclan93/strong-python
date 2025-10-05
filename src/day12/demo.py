"""
简化版 ORM 系统（修复版）
修复：每个模型类使用独立的对象存储空间
"""

from typing import Any, Dict, List, Type


# ==================== 字段描述符 ====================

class Field:
    """字段基类（描述符）"""
    
    def __init__(self, field_type, required=True, default=None):
        self.field_type = field_type
        self.required = required
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        """自动获取字段名"""
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)
    
    def __set__(self, instance, value):
        # 类型验证
        if value is not None and not isinstance(value, self.field_type):
            raise TypeError(
                f"{self.name} 必须是 {self.field_type.__name__} 类型"
            )
        
        # 必填验证
        if self.required and value is None:
            raise ValueError(f"{self.name} 是必填字段")
        
        instance.__dict__[self.name] = value
    
    def validate(self, value):
        """额外的验证逻辑"""
        pass


class IntegerField(Field):
    """整数字段"""
    
    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(int, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
    
    def __set__(self, instance, value):
        super().__set__(instance, value)
        
        if value is not None:
            if self.min_value is not None and value < self.min_value:
                raise ValueError(f"{self.name} 不能小于 {self.min_value}")
            if self.max_value is not None and value > self.max_value:
                raise ValueError(f"{self.name} 不能大于 {self.max_value}")


class StringField(Field):
    """字符串字段"""
    
    def __init__(self, max_length=None, **kwargs):
        super().__init__(str, **kwargs)
        self.max_length = max_length
    
    def __set__(self, instance, value):
        if value and self.max_length and len(value) > self.max_length:
            raise ValueError(
                f"{self.name} 长度不能超过 {self.max_length}"
            )
        super().__set__(instance, value)


class EmailField(StringField):
    """邮箱字段"""
    
    def __set__(self, instance, value):
        if value and '@' not in value:
            raise ValueError(f"{self.name} 必须是有效的邮箱地址")
        super().__set__(instance, value)


# ==================== 模型元类 ====================

class ModelMeta(type):
    """模型元类 - 控制 Model 类的创建"""
    
    # 存储所有模型类
    _models: Dict[str, Type['Model']] = {}
    
    def __new__(mcs, name, bases, attrs):
        # 跳过 Model 基类本身
        if name == 'Model':
            return super().__new__(mcs, name, bases, attrs)
        
        # 收集所有字段
        fields = {}
        for key, value in list(attrs.items()):
            if isinstance(value, Field):
                fields[key] = value
        
        # 将字段信息存储到类属性
        attrs['_fields'] = fields
        attrs['_table_name'] = name.lower()
        
        # ✅ 关键修复：为每个模型类创建独立的对象存储列表
        attrs['_objects'] = []
        
        # 创建类
        cls = super().__new__(mcs, name, bases, attrs)
        
        # 注册模型
        mcs._models[name] = cls
        
        print(f"✓ 注册模型: {name} (字段: {list(fields.keys())})")
        
        return cls


# ==================== 简单查询器 ====================

class QuerySet:
    """查询集（模拟数据库查询）"""
    
    def __init__(self, model_class):
        self.model_class = model_class
        self._filters = []
    
    def filter(self, **kwargs):
        """过滤查询"""
        new_qs = QuerySet(self.model_class)
        new_qs._filters = self._filters + [kwargs]
        return new_qs
    
    def all(self):
        """获取所有对象（从模型类自己的存储中获取）"""
        # ✅ 修复：从当前模型类的 _objects 获取，而不是从 Model._objects
        objects = self.model_class._objects
        
        # 应用过滤条件
        for filter_dict in self._filters:
            objects = [
                obj for obj in objects
                if all(
                    getattr(obj, key, None) == value
                    for key, value in filter_dict.items()
                )
            ]
        
        return objects
    
    def first(self):
        """获取第一个对象"""
        result = self.all()
        return result[0] if result else None
    
    def count(self):
        """计数"""
        return len(self.all())
    
    def get(self, **kwargs):
        """获取单个对象"""
        filtered = self.filter(**kwargs).all()
        if len(filtered) == 0:
            raise ValueError(f"未找到匹配的对象: {kwargs}")
        if len(filtered) > 1:
            raise ValueError(f"找到多个对象: {kwargs}")
        return filtered[0]


# ==================== 模型基类 ====================

class Model(metaclass=ModelMeta):
    """ORM 模型基类"""
    
    # 注意：这些会被元类为每个子类重新创建
    _objects: List['Model'] = []
    _fields: Dict[str, Field] = {}
    _table_name: str = ''
    
    def __init__(self, **kwargs):
        # 设置所有字段的值
        for field_name, field in self._fields.items():
            value = kwargs.get(field_name, field.default)
            setattr(self, field_name, value)
    
    def save(self):
        """保存对象（添加到内存存储）"""
        if self not in self.__class__._objects:
            self.__class__._objects.append(self)
            print(f"✓ 保存 {self.__class__.__name__}: {self}")
        else:
            print(f"✓ 更新 {self.__class__.__name__}: {self}")
    
    def delete(self):
        """删除对象"""
        if self in self.__class__._objects:
            self.__class__._objects.remove(self)
            print(f"✓ 删除 {self.__class__.__name__}: {self}")
    
    @classmethod
    def objects(cls):
        """返回查询集"""
        return QuerySet(cls)
    
    @classmethod
    def create(cls, **kwargs):
        """创建并保存对象"""
        obj = cls(**kwargs)
        obj.save()
        return obj
    
    def __repr__(self):
        field_strs = [
            f"{name}={getattr(self, name)!r}"
            for name in self._fields.keys()
        ]
        return f"{self.__class__.__name__}({', '.join(field_strs)})"
    
    def to_dict(self):
        """转换为字典"""
        return {
            name: getattr(self, name)
            for name in self._fields.keys()
        }


# ==================== 使用示例 ====================

if __name__ == '__main__':
    print("=" * 60)
    print("简化版 ORM 系统演示（修复版）")
    print("=" * 60)
    
    # 定义模型
    class User(Model):
        """用户模型"""
        id = IntegerField(min_value=1)
        name = StringField(max_length=50)
        email = EmailField()
        age = IntegerField(min_value=0, max_value=150, required=False)
    
    class Product(Model):
        """商品模型"""
        id = IntegerField(min_value=1)
        name = StringField(max_length=100)
        price = IntegerField(min_value=0)
        stock = IntegerField(min_value=0, default=0)
    
    print("\n--- 验证独立存储 ---")
    print(f"User._objects 的 id: {id(User._objects)}")
    print(f"Product._objects 的 id: {id(Product._objects)}")
    print(f"是否是同一个列表: {User._objects is Product._objects}")
    
    print("\n--- 创建用户 ---")
    user1 = User.create(id=1, name="Alice", email="alice@example.com", age=25)
    user2 = User.create(id=2, name="Bob", email="bob@example.com", age=30)
    user3 = User.create(id=3, name="Charlie", email="charlie@example.com", age=25)
    
    print("\n--- 创建商品 ---")
    product1 = Product.create(id=1, name="笔记本", price=5000, stock=10)
    product2 = Product.create(id=2, name="鼠标", price=100, stock=50)
    product3 = Product.create(id=3, name="键盘", price=300, stock=30)
    
    print("\n--- 验证存储隔离 ---")
    print(f"User._objects 中的对象数量: {len(User._objects)}")
    print(f"Product._objects 中的对象数量: {len(Product._objects)}")
    print(f"User._objects: {User._objects}")
    print(f"Product._objects: {Product._objects}")
    
    print("\n--- 查询所有用户 ---")
    all_users = User.objects().all()
    for user in all_users:
        print(f"  {user}")
    
    print("\n--- 过滤查询（修复后）---")
    filtered_users = User.objects().filter(age=25).all()
    print(f"年龄为25的用户: {filtered_users}")
    
    print("\n--- 查询所有商品 ---")
    all_products = Product.objects().all()
    for product in all_products:
        print(f"  {product}")
    
    print("\n--- 过滤商品 ---")
    cheap_products = Product.objects().filter(price=100).all()
    print(f"价格为100的商品: {cheap_products}")
    
    print("\n--- 获取单个对象 ---")
    try:
        user = User.objects().get(id=1)
        print(f"ID=1的用户: {user}")
        
        product = Product.objects().get(name="鼠标")
        print(f"名称为'鼠标'的商品: {product}")
    except ValueError as e:
        print(f"错误: {e}")
    
    print("\n--- 链式查询 ---")
    result = User.objects().filter(age=25).first()
    print(f"第一个年龄为25的用户: {result}")
    
    print("\n--- 统计 ---")
    user_count = User.objects().count()
    product_count = Product.objects().count()
    print(f"用户总数: {user_count}")
    print(f"商品总数: {product_count}")
    
    print("\n--- 更新对象 ---")
    user1.age = 26
    user1.save()
    
    print("\n--- 删除用户 ---")
    user3.delete()
    print(f"删除后用户数量: {User.objects().count()}")
    
    print("\n--- 转换为字典 ---")
    print(f"用户字典: {user1.to_dict()}")
    print(f"商品字典: {product1.to_dict()}")
    
    print("\n--- 字段验证测试 ---")
    try:
        bad_user = User(id="not_an_int", name="Test", email="test@example.com")
    except TypeError as e:
        print(f"✗ 类型错误: {e}")
    
    try:
        bad_user = User(id=4, name="Test", email="invalid_email")
    except ValueError as e:
        print(f"✗ 验证错误: {e}")
    
    try:
        bad_user = User(id=5, name="Test", email="test@example.com", age=200)
    except ValueError as e:
        print(f"✗ 范围错误: {e}")
    
    try:
        bad_product = Product(id=10, name="X" * 200, price=100)
    except ValueError as e:
        print(f"✗ 长度错误: {e}")
    
    print("\n--- 查看所有注册的模型 ---")
    print(f"已注册模型: {list(ModelMeta._models.keys())}")
    
    print("\n" + "=" * 60)
    print("演示完成！Bug 已修复！")
    print("=" * 60)