"""
策略模式 - 算法可替换
"""

from abc import ABC, abstractmethod

# ==================== 基础策略模式 ====================

class PaymentStrategy(ABC):
    """支付策略接口"""
    
    @abstractmethod
    def pay(self, amount):
        pass


class AlipayStrategy(PaymentStrategy):
    """支付宝策略"""
    
    def pay(self, amount):
        print(f"💰 使用支付宝支付: ¥{amount}")


class WechatStrategy(PaymentStrategy):
    """微信策略"""
    
    def pay(self, amount):
        print(f"💚 使用微信支付: ¥{amount}")


class CreditCardStrategy(PaymentStrategy):
    """信用卡策略"""
    
    def __init__(self, card_number):
        self.card_number = card_number
    
    def pay(self, amount):
        print(f"💳 使用信用卡支付: ¥{amount} (卡号: {self.card_number[-4:]})")


class ShoppingCart:
    """购物车（上下文）"""
    
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append((item, price))
        print(f"➕ 添加商品: {item} - ¥{price}")
    
    def set_payment_strategy(self, strategy):
        """设置支付策略"""
        self.payment_strategy = strategy
    
    def checkout(self):
        """结账"""
        total = sum(price for _, price in self.items)
        print(f"\n🛒 总计: ¥{total}")
        
        if self.payment_strategy:
            self.payment_strategy.pay(total)
        else:
            print("❌ 请选择支付方式")


# 测试
print("=" * 60)
print("策略模式 - 支付方式")
print("=" * 60)

cart = ShoppingCart()
cart.add_item("笔记本", 5000)
cart.add_item("鼠标", 100)

# 使用支付宝
cart.set_payment_strategy(AlipayStrategy())
cart.checkout()

# 换成微信支付
print()
cart.set_payment_strategy(WechatStrategy())
cart.checkout()

# 换成信用卡
print()
cart.set_payment_strategy(CreditCardStrategy("1234567890123456"))
cart.checkout()


# ==================== 实战：图片压缩策略 ====================

class CompressionStrategy(ABC):
    """压缩策略"""
    
    @abstractmethod
    def compress(self, file_path):
        pass


class JPEGCompression(CompressionStrategy):
    def compress(self, file_path):
        return f"🖼️  JPEG 压缩 {file_path} (有损，高压缩比)"


class PNGCompression(CompressionStrategy):
    def compress(self, file_path):
        return f"🖼️  PNG 压缩 {file_path} (无损，保持质量)"


class WebPCompression(CompressionStrategy):
    def compress(self, file_path):
        return f"🖼️  WebP 压缩 {file_path} (现代格式，平衡)"


class ImageCompressor:
    """图片压缩器"""
    
    def __init__(self, strategy):
        self.strategy = strategy
    
    def set_strategy(self, strategy):
        self.strategy = strategy
    
    def compress_file(self, file_path):
        result = self.strategy.compress(file_path)
        print(result)


# 测试
print("\n" + "=" * 60)
print("实战：图片压缩策略")
print("=" * 60)

compressor = ImageCompressor(JPEGCompression())
compressor.compress_file("photo.jpg")

compressor.set_strategy(PNGCompression())
compressor.compress_file("logo.png")

compressor.set_strategy(WebPCompression())
compressor.compress_file("banner.webp")


# ==================== 实战：排序策略 ====================

class SortStrategy(ABC):
    """排序策略"""
    
    @abstractmethod
    def sort(self, data):
        pass


class QuickSort(SortStrategy):
    def sort(self, data):
        print(f"⚡ 快速排序 (平均 O(n log n))")
        return sorted(data)  # 简化版


class BubbleSort(SortStrategy):
    def sort(self, data):
        print(f"🫧 冒泡排序 (O(n²))")
        result = data.copy()
        n = len(result)
        for i in range(n):
            for j in range(0, n-i-1):
                if result[j] > result[j+1]:
                    result[j], result[j+1] = result[j+1], result[j]
        return result


class Sorter:
    """排序器"""
    
    def __init__(self, strategy):
        self.strategy = strategy
    
    def sort(self, data):
        return self.strategy.sort(data)


# 测试
print("\n" + "=" * 60)
print("实战：排序策略")
print("=" * 60)

data = [64, 34, 25, 12, 22, 11, 90]

sorter = Sorter(QuickSort())
result = sorter.sort(data)
print(f"结果: {result}")

print()
sorter.strategy = BubbleSort()
result = sorter.sort(data)
print(f"结果: {result}")


# ==================== Python 风格：函数式策略 ====================

class DiscountStrategy:
    """折扣策略"""
    
    def __init__(self, discount_func):
        self.discount_func = discount_func
    
    def calculate(self, price):
        return self.discount_func(price)


# 定义不同的折扣函数
def no_discount(price):
    return price


def percentage_discount(percentage):
    """返回一个折扣函数"""
    def discount(price):
        return price * (1 - percentage / 100)
    return discount


def fixed_discount(amount):
    """固定金额折扣"""
    def discount(price):
        return max(0, price - amount)
    return discount


# 测试
print("\n" + "=" * 60)
print("Python 风格：函数式策略")
print("=" * 60)

original_price = 1000

# 无折扣
strategy = DiscountStrategy(no_discount)
print(f"原价: ¥{strategy.calculate(original_price)}")

# 9折
strategy = DiscountStrategy(percentage_discount(10))
print(f"9折后: ¥{strategy.calculate(original_price)}")

# 减100
strategy = DiscountStrategy(fixed_discount(100))
print(f"减100后: ¥{strategy.calculate(original_price)}")


print("\n✅ 策略模式完成！")