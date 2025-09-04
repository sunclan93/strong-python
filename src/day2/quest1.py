"""
智能词频统计器框架
你的任务：实现所有标记为 # TODO 的方法
"""

from collections import Counter, defaultdict
import re
import string
from typing import List, Tuple, Dict, Set


class SmartWordCounter:
    """智能词频统计器"""
    
    def __init__(self, 
                 ignore_case: bool = True,
                 ignore_punctuation: bool = True,
                 min_word_length: int = 1,
                 stop_words: Set[str] = None):
        """
        初始化词频统计器
        
        Args:
            ignore_case: 是否忽略大小写
            ignore_punctuation: 是否忽略标点符号
            min_word_length: 最小词长度
            stop_words: 停用词集合
        """
        self.ignore_case = ignore_case
        self.ignore_punctuation = ignore_punctuation
        self.min_word_length = min_word_length
        self.stop_words = stop_words or set()
        
        # 统计数据
        self.word_counts = Counter()
        self.total_words = 0
        self.unique_words = 0
        
        # 默认英文停用词
        self.default_english_stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        预处理文本，提取词汇
        
        Args:
            text: 输入文本
            
        Returns:
            List[str]: 处理后的词汇列表
        """
        # TODO: 实现文本预处理
        # 提示：
        # 1. 处理大小写
        if self.ignore_case:
            text = text.lower()
        # 2. 去除标点符号
        if self.ignore_punctuation:
            translator = str.maketrans("","",string.punctuation)
            text = text.translate(translator)
        # 3. 分割成词汇
        words = text.split() ## 自动处理所有空白字符（包括\n, \t等）
        # 4. 过滤停用词和短词
        filtered_words = []
        for word in words:
            # 过滤短词
            if len(word) < self.min_word_length:
                continue
            # 过滤停用词
            if word in self.stop_words:
                continue
            filtered_words.append(word)
        return filtered_words

    
    def add_text(self, text: str) -> 'SmartWordCounter':
        """
        添加文本进行统计
        
        Args:
            text: 要分析的文本
            
        Returns:
            SmartWordCounter: 返回自身支持链式调用
        """
        # TODO: 实现文本添加功能
        # 提示：
        # 1. 调用 preprocess_text 处理文本
        processed_words = self.preprocess_text(text)
        # 2. 更新 word_counts
        self.word_counts.update(processed_words)
        # 3. 更新统计信息
        self.total_words = sum(self.word_counts.values())
        self.unique_words = len(self.word_counts)
        return self
        
        
    
    def get_top_words(self, n: int = 10) -> List[Tuple[str, int]]:
        """
        获取最常见的 N 个词
        
        Args:
            n: 返回的词汇数量
            
        Returns:
            List[Tuple[str, int]]: (词汇, 频次) 的列表
        """
        # TODO: 实现获取热门词汇
        # 提示：使用 Counter.most_common()
        return self.word_counts.most_common(n)
    
    def get_word_frequency(self, word: str) -> int:
        """
        获取特定词汇的频次
        
        Args:
            word: 要查询的词汇
            
        Returns:
            int: 词汇出现次数
        """
        # TODO: 实现词汇频次查询
        if self.ignore_case:
            word = word.lower()
        return self.word_counts[word]
        
    
    
    def get_statistics(self) -> Dict[str, any]:
        """
        获取统计分析报告
        
        Returns:
            Dict: 包含各种统计信息的字典
        """
        # TODO: 实现统计报告
        # 提示：计算总词数、唯一词数、平均词长等
        res = {}
        res["total_words"] = self.total_words
        res["unique_words"] = self.unique_words
        if self.total_words > 0:
            total_chars = sum(len(word) * count for word, count in self.word_counts.items())
            res["average_word_length"] = total_chars / self.total_words
        else:
            res["average_word_length"] = 0
        return res
        
    
    def filter_by_frequency(self, min_freq: int = 2) -> Dict[str, int]:
        """
        按频次过滤词汇
        
        Args:
            min_freq: 最小频次
            
        Returns:
            Dict[str, int]: 过滤后的词汇统计
        """
        # TODO: 实现频次过滤
        res = {}
        for k,v in self.word_counts.items():
            if v >= min_freq:
                res[k] = v
        return res
        

    
    def clear(self) -> 'SmartWordCounter':
        """清除所有统计数据"""
        # TODO: 实现数据清除
        self.word_counts.clear()
        self.total_words = 0
        self.unique_words = 0
        return self
    
    def __str__(self) -> str:
        """返回统计摘要"""
        return f"SmartWordCounter(总词数: {self.total_words}, 唯一词数: {self.unique_words})"


def test_word_counter():
    """测试函数 - 用来验证你的实现"""
    print("=== 智能词频统计器测试 ===\n")
    
    # 测试文本
    text1 = """
    Python is a powerful programming language. 
    Python is easy to learn and Python is widely used.
    Many developers love Python because Python is versatile.
    """
    
    text2 = """
    Machine learning is revolutionizing technology.
    Deep learning, a subset of machine learning, uses neural networks.
    Learning these technologies is essential for modern developers.
    """
    
    print("1️⃣ 基础功能测试")
    counter = SmartWordCounter()
    counter.add_text(text1)
    
    print(f"统计器状态: {counter}")
    print(f"Top 5 词汇: {counter.get_top_words(5)}")
    print(f"'python' 出现次数: {counter.get_word_frequency('python')}")
    print()
    
    print("2️⃣ 链式调用测试")
    counter.clear().add_text(text1).add_text(text2)
    print(f"添加两个文本后: {counter}")
    print(f"Top 10 词汇: {counter.get_top_words(10)}")
    print()
    
    print("3️⃣ 高级功能测试")
    # 测试停用词过滤
    counter_with_stopwords = SmartWordCounter(
        stop_words={'is', 'a', 'to', 'and', 'of'}
    )
    counter_with_stopwords.add_text(text1)
    print(f"过滤停用词后的 Top 5: {counter_with_stopwords.get_top_words(5)}")
    
    # 测试频次过滤
    print(f"出现2次以上的词: {counter.filter_by_frequency(2)}")
    
    # 统计报告
    print(f"统计报告: {counter.get_statistics()}")


if __name__ == "__main__":
    print("🎯 你的任务：")
    print("1. 实现所有标记为 # TODO 的方法")
    print("2. 运行 test_word_counter() 验证功能")
    print("3. 思考还能添加什么有趣的功能")
    print()
    print("💡 实现提示：")
    print("- 使用 Counter 进行词频统计")
    print("- 使用 re 模块处理文本")
    print("- 注意链式调用要返回 self")
    print("- 考虑边界情况（空文本、特殊字符等）")
    print()
    
    # 取消注释来测试你的实现
    test_word_counter()