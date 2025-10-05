"""
建造者模式 - 分步骤构建复杂对象
"""

# ==================== 基础建造者 ====================

class Computer:
    """电脑类"""
    
    def __init__(self):
        self.cpu = None
        self.memory = None
        self.storage = None
        self.gpu = None
    
    def __str__(self):
        parts = [
            f"CPU: {self.cpu}" if self.cpu else None,
            f"内存: {self.memory}GB" if self.memory else None,
            f"存储: {self.storage}GB" if self.storage else None,
            f"显卡: {self.gpu}" if self.gpu else None,
        ]
        return "💻 " + " | ".join(p for p in parts if p)


class ComputerBuilder:
    """电脑建造者"""
    
    def __init__(self):
        self.computer = Computer()
    
    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self  # 返回 self 实现链式调用
    
    def set_memory(self, memory):
        self.computer.memory = memory
        return self
    
    def set_storage(self, storage):
        self.computer.storage = storage
        return self
    
    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self
    
    def build(self):
        return self.computer


# 测试建造者
print("建造者模式 - 链式调用")
computer = (ComputerBuilder()
    .set_cpu("Intel i7")
    .set_memory(16)
    .set_storage(512)
    .set_gpu("NVIDIA RTX 3060")
    .build())

print(computer)


# ==================== 指导者 + 建造者 ====================

class Director:
    """指导者：定义构建步骤"""
    
    def __init__(self, builder):
        self.builder = builder
    
    def build_gaming_pc(self):
        """构建游戏电脑"""
        return (self.builder
            .set_cpu("Intel i9")
            .set_memory(32)
            .set_storage(1024)
            .set_gpu("NVIDIA RTX 4090")
            .build())
    
    def build_office_pc(self):
        """构建办公电脑"""
        return (self.builder
            .set_cpu("Intel i5")
            .set_memory(8)
            .set_storage(256)
            .build())


# 测试指导者
print("\n使用指导者")
director = Director(ComputerBuilder())
gaming_pc = director.build_gaming_pc()
print(f"游戏电脑: {gaming_pc}")

office_pc = director.build_office_pc()
print(f"办公电脑: {office_pc}")


# ==================== 实战：SQL 查询构建器 ====================

class SQLQuery:
    """SQL 查询对象"""
    
    def __init__(self):
        self.select_fields = []
        self.from_table = None
        self.where_conditions = []
        self.order_by_field = None
        self.limit_count = None
    
    def __str__(self):
        """生成 SQL 语句"""
        parts = []
        
        # SELECT
        fields = ', '.join(self.select_fields) if self.select_fields else '*'
        parts.append(f"SELECT {fields}")
        
        # FROM
        if self.from_table:
            parts.append(f"FROM {self.from_table}")
        
        # WHERE
        if self.where_conditions:
            conditions = ' AND '.join(self.where_conditions)
            parts.append(f"WHERE {conditions}")
        
        # ORDER BY
        if self.order_by_field:
            parts.append(f"ORDER BY {self.order_by_field}")
        
        # LIMIT
        if self.limit_count:
            parts.append(f"LIMIT {self.limit_count}")
        
        return ' '.join(parts) + ';'


class QueryBuilder:
    """SQL 查询构建器"""
    
    def __init__(self):
        self.query = SQLQuery()
    
    def select(self, *fields):
        self.query.select_fields = list(fields)
        return self
    
    def from_table(self, table):
        self.query.from_table = table
        return self
    
    def where(self, condition):
        self.query.where_conditions.append(condition)
        return self
    
    def order_by(self, field):
        self.query.order_by_field = field
        return self
    
    def limit(self, count):
        self.query.limit_count = count
        return self
    
    def build(self):
        return self.query


# 测试 SQL 构建器
print("\n实战：SQL 查询构建器")

query1 = (QueryBuilder()
    .select('id', 'name', 'age')
    .from_table('users')
    .where('age > 18')
    .where('city = "Beijing"')
    .order_by('age DESC')
    .limit(10)
    .build())

print(query1)

query2 = (QueryBuilder()
    .from_table('products')
    .where('price < 100')
    .build())

print(query2)


# ==================== 实战：HTTP 请求构建器 ====================

class HTTPRequest:
    """HTTP 请求对象"""
    
    def __init__(self):
        self.method = 'GET'
        self.url = None
        self.headers = {}
        self.body = None
    
    def __str__(self):
        lines = [f"{self.method} {self.url}"]
        for key, value in self.headers.items():
            lines.append(f"{key}: {value}")
        if self.body:
            lines.append(f"\n{self.body}")
        return '\n'.join(lines)


class RequestBuilder:
    """HTTP 请求构建器"""
    
    def __init__(self):
        self.request = HTTPRequest()
    
    def get(self, url):
        self.request.method = 'GET'
        self.request.url = url
        return self
    
    def post(self, url):
        self.request.method = 'POST'
        self.request.url = url
        return self
    
    def header(self, key, value):
        self.request.headers[key] = value
        return self
    
    def json(self, data):
        import json
        self.request.body = json.dumps(data)
        self.header('Content-Type', 'application/json')
        return self
    
    def build(self):
        return self.request


# 测试 HTTP 构建器
print("\n实战：HTTP 请求构建器")

request = (RequestBuilder()
    .post('https://api.example.com/users')
    .header('Authorization', 'Bearer token123')
    .json({'name': 'Alice', 'age': 25})
    .build())

print(request)


print("\n✅ 建造者模式学习完成！")