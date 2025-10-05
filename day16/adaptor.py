"""
适配器模式 - 让不兼容的接口协同工作
"""

from abc import ABC, abstractmethod

# ==================== 场景1: 第三方库适配 ====================

# 旧的日志接口
class OldLogger:
    def log_message(self, msg):
        print(f"[OLD] {msg}")


# 新的日志接口
class Logger(ABC):
    @abstractmethod
    def info(self, msg):
        pass
    
    @abstractmethod
    def error(self, msg):
        pass


# 适配器：让旧接口符合新标准
class LoggerAdapter(Logger):
    """适配器"""
    
    def __init__(self, old_logger):
        self.old_logger = old_logger
    
    def info(self, msg):
        self.old_logger.log_message(f"INFO: {msg}")
    
    def error(self, msg):
        self.old_logger.log_message(f"ERROR: {msg}")


# 测试
print("场景1: 日志适配器")
old = OldLogger()
adapter = LoggerAdapter(old)

adapter.info("系统启动")
adapter.error("发生错误")


# ==================== 场景2: 数据格式适配 ====================

# 外部 API 返回 XML
class XMLData:
    def __init__(self, xml_string):
        self.xml = xml_string
    
    def get_xml(self):
        return self.xml


# 我们的系统需要 JSON
class JSONAdapter:
    """XML 转 JSON 适配器"""
    
    def __init__(self, xml_data):
        self.xml_data = xml_data
    
    def get_json(self):
        # 简化版：实际应该用 xml.etree 或 lxml
        xml = self.xml_data.get_xml()
        # 模拟转换
        return '{"data": "converted from xml"}'


# 测试
print("\n场景2: 数据格式适配")
xml_data = XMLData("<user><name>Alice</name></user>")
json_adapter = JSONAdapter(xml_data)
print(f"JSON: {json_adapter.get_json()}")


# ==================== 场景3: 支付接口适配 ====================

# 支付宝接口
class Alipay:
    def alipay_payment(self, amount):
        return f"支付宝支付: ¥{amount}"


# 微信接口
class WechatPay:
    def wechat_payment(self, amount):
        return f"微信支付: ¥{amount}"


# 统一支付接口
class PaymentInterface(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


# 支付宝适配器
class AlipayAdapter(PaymentInterface):
    def __init__(self):
        self.alipay = Alipay()
    
    def pay(self, amount):
        return self.alipay.alipay_payment(amount)


# 微信适配器
class WechatAdapter(PaymentInterface):
    def __init__(self):
        self.wechat = WechatPay()
    
    def pay(self, amount):
        return self.wechat.wechat_payment(amount)


# 客户端代码（统一接口）
def process_payment(payment: PaymentInterface, amount):
    print(payment.pay(amount))


# 测试
print("\n场景3: 支付接口统一")
process_payment(AlipayAdapter(), 100)
process_payment(WechatAdapter(), 200)


# ==================== 实战：多数据源适配器 ====================

# 不同的数据源
class MySQLDataSource:
    def fetch_from_mysql(self, query):
        return f"MySQL 数据: {query}"


class MongoDataSource:
    def get_from_mongo(self, collection):
        return f"MongoDB 数据: {collection}"


class APIDataSource:
    def request_api(self, endpoint):
        return f"API 数据: {endpoint}"


# 统一数据源接口
class DataSource(ABC):
    @abstractmethod
    def get_data(self, identifier):
        pass


# 各种适配器
class MySQLAdapter(DataSource):
    def __init__(self):
        self.source = MySQLDataSource()
    
    def get_data(self, identifier):
        return self.source.fetch_from_mysql(identifier)


class MongoAdapter(DataSource):
    def __init__(self):
        self.source = MongoDataSource()
    
    def get_data(self, identifier):
        return self.source.get_from_mongo(identifier)


class APIAdapter(DataSource):
    def __init__(self):
        self.source = APIDataSource()
    
    def get_data(self, identifier):
        return self.source.request_api(identifier)


# 数据处理器（不关心数据源类型）
class DataProcessor:
    def __init__(self, data_source: DataSource):
        self.data_source = data_source
    
    def process(self, identifier):
        data = self.data_source.get_data(identifier)
        print(f"处理: {data}")


# 测试
print("\n实战：多数据源统一")
processor1 = DataProcessor(MySQLAdapter())
processor1.process("SELECT * FROM users")

processor2 = DataProcessor(MongoAdapter())
processor2.process("users_collection")

processor3 = DataProcessor(APIAdapter())
processor3.process("/api/users")


print("\n✅ 适配器模式完成！")