"""
第一周 Day 4：生成器与迭代器深度解析
学习目标：掌握迭代器协议，理解生成器原理，学会内存高效编程

今日重点：
1. 迭代器协议的完整理解
2. 生成器函数 vs 生成器表达式
3. yield from 语法和委托
4. 协程的基础概念
5. 内存效率对比分析
"""

import sys
import time
import itertools
from typing import Iterator, Generator, Iterable
from collections.abc import Iterator as ABCIterator


# ==== 第一部分：迭代器协议深度理解 ====
print("=== 迭代器协议深度理解 ===\n")

def understand_iterator_protocol():
    """深入理解迭代器协议"""
    
    print("迭代器协议包含两个方法：__iter__ 和 __next__")
    print()
    
    # 手动实现一个迭代器
    class CountDown:
        """倒计时迭代器"""
        
        def __init__(self, start):
            self.start = start
        
        def __iter__(self):
            """返回迭代器对象本身"""
            print(f"🔄 __iter__ 被调用，开始倒计时从 {self.start}")
            return self
        
        def __next__(self):
            """返回下一个值"""
            if self.start <= 0:
                print("💥 StopIteration - 倒计时结束")
                raise StopIteration
            
            self.start -= 1
            current = self.start + 1
            print(f"⏰ __next__ 返回: {current}")
            return current
    
    print("1️⃣ 手动实现的迭代器测试:")
    countdown = CountDown(3)
    
    print("使用 for 循环:")
    for num in countdown:
        print(f"  得到: {num}")
    print()
    
    print("2️⃣ 手动调用迭代器方法:")
    countdown2 = CountDown(2)
    iterator = iter(countdown2)  # 调用 __iter__
    
    try:
        print(f"第一次 next(): {next(iterator)}")  # 调用 __next__
        print(f"第二次 next(): {next(iterator)}")
        print(f"第三次 next(): {next(iterator)}")  # 会抛出 StopIteration
    except StopIteration:
        print("捕获到 StopIteration")
    print()

understand_iterator_protocol()


# ==== 第二部分：生成器函数详解 ====
print("=== 生成器函数详解 ===\n")

def generator_function_deep_dive():
    """生成器函数深度解析"""
    
    print("生成器函数：包含 yield 关键字的函数")
    print()
    
    def simple_generator():
        """最简单的生成器"""
        print("🚀 生成器开始执行")
        yield 1
        print("⚡ 第一个 yield 后继续执行")
        yield 2
        print("✨ 第二个 yield 后继续执行")
        yield 3
        print("🏁 生成器执行结束")
    
    print("1️⃣ 生成器函数的执行过程:")
    gen = simple_generator()
    print(f"生成器对象: {gen}")
    print(f"生成器类型: {type(gen)}")
    print()
    
    print("逐步调用 next():")
    print(f"第一次: {next(gen)}")
    print(f"第二次: {next(gen)}")
    print(f"第三次: {next(gen)}")
    try:
        print(f"第四次: {next(gen)}")
    except StopIteration:
        print("第四次: StopIteration - 生成器耗尽")
    print()
    
    # 更复杂的生成器：斐波那契数列
    def fibonacci_generator(n):
        """斐波那契数列生成器"""
        print(f"🔢 生成前 {n} 个斐波那契数")
        a, b = 0, 1
        count = 0
        while count < n:
            yield a
            a, b = b, a + b
            count += 1
        print("🏁 斐波那契生成器结束")
    
    print("2️⃣ 斐波那契生成器:")
    fib_gen = fibonacci_generator(5)
    for num in fib_gen:
        print(f"  斐波那契数: {num}")
    print()

generator_function_deep_dive()


# ==== 第三部分：生成器表达式 ====
print("=== 生成器表达式 ===\n")

def generator_expressions():
    """生成器表达式详解"""
    
    print("生成器表达式：类似列表推导式，但使用 () 而不是 []")
    print()
    
    # 对比列表推导式和生成器表达式
    print("1️⃣ 列表推导式 vs 生成器表达式:")
    
    # 列表推导式 - 立即计算所有值
    list_comp = [x**2 for x in range(5)]
    print(f"列表推导式: {list_comp}")
    print(f"列表大小: {sys.getsizeof(list_comp)} 字节")
    
    # 生成器表达式 - 惰性计算
    gen_exp = (x**2 for x in range(5))
    print(f"生成器表达式: {gen_exp}")
    print(f"生成器大小: {sys.getsizeof(gen_exp)} 字节")
    print()
    
    print("2️⃣ 内存使用对比:")
    # 大数据集的内存对比
    large_range = 1000000
    
    print("创建大列表...")
    start_time = time.time()
    large_list = [x for x in range(large_range)]
    list_time = time.time() - start_time
    list_memory = sys.getsizeof(large_list)
    
    print("创建大生成器...")
    start_time = time.time()
    large_gen = (x for x in range(large_range))
    gen_time = time.time() - start_time
    gen_memory = sys.getsizeof(large_gen)
    
    print(f"列表 - 时间: {list_time:.4f}s, 内存: {list_memory:,} 字节")
    print(f"生成器 - 时间: {gen_time:.6f}s, 内存: {gen_memory} 字节")
    print(f"内存节省: {list_memory / gen_memory:.0f}x")
    print()
    
    # 生成器表达式的链式操作
    print("3️⃣ 生成器表达式的链式操作:")
    numbers = range(10)
    
    # 链式生成器操作
    squares = (x**2 for x in numbers)
    evens = (x for x in squares if x % 2 == 0)
    result = (x * 10 for x in evens)
    
    print("链式操作：numbers -> squares -> evens -> result")
    print(f"最终结果: {list(result)}")
    print()

generator_expressions()


# ==== 第四部分：yield from 语法 ====
print("=== yield from 语法深度解析 ===\n")

def yield_from_deep_dive():
    """yield from 语法详解"""
    
    print("yield from：优雅地委托给另一个生成器")
    print()
    
    # 不使用 yield from 的写法
    def flatten_without_yield_from(nested_list):
        """不使用 yield from 展平嵌套列表"""
        for sublist in nested_list:
            if isinstance(sublist, list):
                for item in flatten_without_yield_from(sublist):
                    yield item
            else:
                yield sublist
    
    # 使用 yield from 的写法
    def flatten_with_yield_from(nested_list):
        """使用 yield from 展平嵌套列表"""
        for sublist in nested_list:
            if isinstance(sublist, list):
                yield from flatten_with_yield_from(sublist)
            else:
                yield sublist
    
    print("1️⃣ yield from 的优雅性:")
    nested = [1, [2, 3, [4, 5]], 6, [7, [8, 9]]]
    
    print("不使用 yield from:")
    result1 = list(flatten_without_yield_from(nested))
    print(f"结果: {result1}")
    
    print("使用 yield from:")
    result2 = list(flatten_with_yield_from(nested))
    print(f"结果: {result2}")
    print()
    
    # yield from 的生成器组合
    def number_generator():
        """数字生成器"""
        print("  📊 生成数字")
        yield from range(1, 4)
    
    def letter_generator():
        """字母生成器"""
        print("  🔤 生成字母")
        yield from ['a', 'b', 'c']
    
    def combined_generator():
        """组合生成器"""
        print("🔄 开始组合生成器")
        yield from number_generator()
        yield from letter_generator()
        print("✅ 组合生成器结束")
    
    print("2️⃣ 生成器组合:")
    combined = combined_generator()
    for item in combined:
        print(f"  得到: {item}")
    print()

yield_from_deep_dive()


# ==== 第五部分：生成器的高级应用 ====
print("=== 生成器的高级应用 ===\n")

def advanced_generator_applications():
    """生成器的高级应用场景"""
    
    # 1. 无限序列生成器
    def infinite_fibonacci():
        """无限斐波那契序列"""
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b
    
    print("1️⃣ 无限序列生成器:")
    fib_infinite = infinite_fibonacci()
    print("前10个斐波那契数:")
    for i, num in enumerate(fib_infinite):
        if i >= 10:
            break
        print(f"  F({i}): {num}")
    print()
    
    # 2. 管道模式
    def read_numbers(filename):
        """读取数字文件的生成器"""
        # 模拟文件读取
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for num in numbers:
            print(f"  📖 读取: {num}")
            yield num
    
    def filter_even(numbers):
        """过滤偶数的生成器"""
        for num in numbers:
            if num % 2 == 0:
                print(f"  ✅ 偶数: {num}")
                yield num
    
    def square_numbers(numbers):
        """平方数字的生成器"""
        for num in numbers:
            squared = num ** 2
            print(f"  🔢 平方: {num} -> {squared}")
            yield squared
    
    print("2️⃣ 数据处理管道:")
    pipeline = square_numbers(filter_even(read_numbers("numbers.txt")))
    result = list(pipeline)
    print(f"最终结果: {result}")
    print()
    
    # 3. 生成器作为协程的基础
    def coroutine_example():
        """生成器作为协程的简单示例"""
        print("🚀 协程启动")
        try:
            while True:
                value = yield
                if value is not None:
                    print(f"  💬 协程收到: {value}")
                    yield f"处理了: {value}"
        except GeneratorExit:
            print("🏁 协程结束")
    
    print("3️⃣ 生成器协程基础:")
    coro = coroutine_example()
    next(coro)  # 启动协程
    
    try:
        coro.send("Hello")
        result = coro.send("World")
        print(f"协程返回: {result}")
    except StopIteration:
        pass
    
    coro.close()  # 关闭协程
    print()

advanced_generator_applications()


# ==== 第六部分：itertools 模块深入 ====
print("=== itertools 模块深入 ===\n")

def itertools_deep_dive():
    """itertools 模块的强大功能"""
    
    print("itertools：生成器和迭代器的瑞士军刀")
    print()
    
    # 1. 无限迭代器
    print("1️⃣ 无限迭代器:")
    
    # count - 无限计数
    counter = itertools.count(10, 2)  # 从10开始，步长2
    print("count(10, 2) 的前5个值:")
    for i, num in enumerate(counter):
        if i >= 5:
            break
        print(f"  {num}")
    
    # cycle - 无限循环
    colors = itertools.cycle(['red', 'green', 'blue'])
    print("cycle(['red', 'green', 'blue']) 的前8个值:")
    for i, color in enumerate(colors):
        if i >= 8:
            break
        print(f"  {color}")
    
    # repeat - 重复值
    repeated = itertools.repeat('hello', 3)
    print(f"repeat('hello', 3): {list(repeated)}")
    print()
    
    # 2. 终止迭代器
    print("2️⃣ 终止迭代器:")
    
    # takewhile - 满足条件时取值
    numbers = [1, 2, 3, 4, 5, 1, 2]
    result = itertools.takewhile(lambda x: x < 4, numbers)
    print(f"takewhile(x < 4, {numbers}): {list(result)}")
    
    # dropwhile - 满足条件时跳过
    result = itertools.dropwhile(lambda x: x < 4, numbers)
    print(f"dropwhile(x < 4, {numbers}): {list(result)}")
    
    # compress - 根据选择器过滤
    data = ['a', 'b', 'c', 'd', 'e']
    selectors = [1, 0, 1, 0, 1]
    result = itertools.compress(data, selectors)
    print(f"compress({data}, {selectors}): {list(result)}")
    print()
    
    # 3. 组合迭代器
    print("3️⃣ 组合迭代器:")
    
    # product - 笛卡尔积
    colors = ['red', 'blue']
    sizes = ['S', 'M', 'L']
    products = itertools.product(colors, sizes)
    print(f"product({colors}, {sizes}):")
    for item in products:
        print(f"  {item}")
    
    # permutations - 排列
    perms = itertools.permutations('ABC', 2)
    print(f"permutations('ABC', 2): {list(perms)}")
    
    # combinations - 组合
    combs = itertools.combinations('ABCD', 2)
    print(f"combinations('ABCD', 2): {list(combs)}")
    print()

itertools_deep_dive()


# ==== 第七部分：实战项目 - 大文件处理器 ====
print("=== 实战项目：大文件处理器 ===\n")

class BigFileProcessor:
    """大文件处理器 - 内存高效的文件处理"""
    
    def __init__(self, chunk_size=1024):
        self.chunk_size = chunk_size
        self.stats = {
            'lines_processed': 0,
            'bytes_processed': 0,
            'chunks_read': 0
        }
    
    def read_chunks(self, file_content):
        """模拟按块读取大文件"""
        # 这里模拟文件内容，实际中会是文件操作
        content = file_content
        position = 0
        
        while position < len(content):
            chunk = content[position:position + self.chunk_size]
            self.stats['chunks_read'] += 1
            self.stats['bytes_processed'] += len(chunk)
            
            print(f"  📖 读取块 {self.stats['chunks_read']}: {len(chunk)} 字节")
            yield chunk
            position += self.chunk_size
    
    def process_lines(self, file_content):
        """逐行处理大文件"""
        current_line = ""
        
        for chunk in self.read_chunks(file_content):
            lines = (current_line + chunk).split('\n')
            current_line = lines[-1]  # 保存不完整的行
            
            # 处理完整的行
            for line in lines[:-1]:
                self.stats['lines_processed'] += 1
                yield line.strip()
        
        # 处理最后一行
        if current_line:
            self.stats['lines_processed'] += 1
            yield current_line.strip()
    
    def filter_lines(self, lines, pattern):
        """过滤包含特定模式的行"""
        for line in lines:
            if pattern in line:
                print(f"  ✅ 匹配行: {line[:50]}...")
                yield line
    
    def transform_lines(self, lines, transformer):
        """转换每一行"""
        for line in lines:
            transformed = transformer(line)
            print(f"  🔄 转换: {line[:30]} -> {transformed[:30]}")
            yield transformed
    
    def count_words(self, lines):
        """统计单词数量"""
        word_count = {}
        
        for line in lines:
            words = line.lower().split()
            for word in words:
                # 简单清理
                word = word.strip('.,!?";')
                if word:
                    word_count[word] = word_count.get(word, 0) + 1
        
        return word_count
    
    def get_stats(self):
        """获取处理统计信息"""
        return self.stats.copy()


def test_big_file_processor():
    """测试大文件处理器"""
    print("大文件处理器测试:")
    
    # 模拟大文件内容
    sample_content = """This is line 1 with some important data.
This is line 2 with more important information.
This line 3 contains regular content.
Line 4 has important details we need to extract.
Regular line 5 without special content.
Important data in line 6 for processing.
Line 7 is just normal text.
Final line 8 with important conclusions."""
    
    processor = BigFileProcessor(chunk_size=50)
    
    print("\n1️⃣ 基本文件处理:")
    lines = processor.process_lines(sample_content)
    all_lines = list(lines)
    print(f"处理了 {len(all_lines)} 行")
    print()
    
    print("2️⃣ 数据处理管道:")
    # 重新创建处理器
    processor = BigFileProcessor(chunk_size=50)
    
    # 构建处理管道
    lines = processor.process_lines(sample_content)
    filtered_lines = processor.filter_lines(lines, "important")
    transformed_lines = processor.transform_lines(
        filtered_lines, 
        lambda x: x.upper()
    )
    
    # 执行管道
    results = list(transformed_lines)
    print(f"\n处理结果 ({len(results)} 行):")
    for i, line in enumerate(results, 1):
        print(f"  {i}. {line}")
    
    # 显示统计信息
    stats = processor.get_stats()
    print(f"\n📊 处理统计:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    print("3️⃣ 词频统计:")
    processor = BigFileProcessor(chunk_size=100)
    lines = processor.process_lines(sample_content)
    word_count = processor.count_words(lines)
    
    # 显示最常见的单词
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    print("最常见的10个单词:")
    for word, count in sorted_words[:10]:
        print(f"  {word}: {count}")

test_big_file_processor()


def memory_efficiency_comparison():
    """内存效率对比测试"""
    print("\n=== 内存效率对比测试 ===\n")
    
    def process_with_list(n):
        """使用列表处理数据 - 内存密集"""
        print(f"使用列表处理 {n:,} 个数字:")
        
        start_time = time.time()
        # 生成所有数据到内存
        numbers = list(range(n))
        squares = [x**2 for x in numbers]
        evens = [x for x in squares if x % 2 == 0]
        result = sum(evens)
        
        end_time = time.time()
        memory_usage = sys.getsizeof(numbers) + sys.getsizeof(squares) + sys.getsizeof(evens)
        
        print(f"  结果: {result}")
        print(f"  时间: {end_time - start_time:.4f}s")
        print(f"  内存: {memory_usage:,} 字节")
        
        return result
    
    def process_with_generator(n):
        """使用生成器处理数据 - 内存高效"""
        print(f"使用生成器处理 {n:,} 个数字:")
        
        start_time = time.time()
        # 使用生成器链
        numbers = range(n)
        squares = (x**2 for x in numbers)
        evens = (x for x in squares if x % 2 == 0)
        result = sum(evens)
        
        end_time = time.time()
        memory_usage = sys.getsizeof(numbers) + sys.getsizeof(squares) + sys.getsizeof(evens)
        
        print(f"  结果: {result}")
        print(f"  时间: {end_time - start_time:.4f}s")
        print(f"  内存: {memory_usage} 字节")
        
        return result
    
    # 测试不同规模的数据
    test_size = 100000
    
    result1 = process_with_list(test_size)
    print()
    result2 = process_with_generator(test_size)
    print()
    
    print(f"结果一致性检查: {result1 == result2}")
    print()

memory_efficiency_comparison()


def todays_exercises():
    """今天的练习任务"""
    print("=== 今天的练习任务 ===\n")
    
    print("🎯 任务 1: 实现一个日志文件分析器")
    print("要求：")
    print("- 使用生成器逐行读取大日志文件")
    print("- 支持多种过滤条件（时间范围、日志级别、关键词）")
    print("- 统计各种日志级别的数量")
    print("- 生成报告摘要")
    print()
    
    print("🎯 任务 2: 实现数据流处理管道")
    print("要求：")
    print("- 使用生成器实现 ETL 流程")
    print("- Extract: 从多个数据源读取")
    print("- Transform: 数据清理和转换")
    print("- Load: 批量写入目标存储")
    print("- 支持错误处理和重试")
    print()
    
    print("🎯 任务 3: 实现自定义迭代器")
    print("要求：")
    print("- 实现一个树遍历迭代器")
    print("- 支持深度优先和广度优先遍历")
    print("- 支持条件过滤")
    print("- 内存效率优化")
    print()
    
    print("🎯 思考题:")
    print("1. 什么时候使用生成器，什么时候使用列表？")
    print("2. yield from 解决了什么问题？")
    print("3. 如何设计一个内存高效的大数据处理系统？")
    print("4. 生成器和协程有什么关系？")

todays_exercises()