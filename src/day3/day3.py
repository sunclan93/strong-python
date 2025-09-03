"""
第一周 Day 2：高级数据结构与 Collections 模块
学习目标：掌握 Python 内置的高级数据结构，并学会设计自定义数据结构

今日重点：
1. Collections 模块深入使用
2. 自定义数据结构设计思维
3. 时间复杂度分析
4. 实战：实现 LRU 缓存系统
"""

from collections import (
    defaultdict, Counter, deque, namedtuple, 
    OrderedDict, ChainMap, UserDict
)
from typing import Any, Optional, Iterator
import time


# ==== 第一部分：Collections 模块深度探索 ====
print("=== Collections 模块深度探索 ===\n")

def demonstrate_defaultdict():
    """演示 defaultdict 的强大功能"""
    print("1️⃣ defaultdict - 永不报 KeyError 的字典")
    
    # 传统方式：需要检查键是否存在
    traditional_dict = {}
    text = "hello world hello python"
    for word in text.split():
        if word in traditional_dict:
            traditional_dict[word] += 1
        else:
            traditional_dict[word] = 1
    print(f"传统方式统计词频: {traditional_dict}")
    
    # defaultdict 方式：自动初始化
    word_count = defaultdict(int)  # 默认值为 0
    for word in text.split():
        word_count[word] += 1  # 不存在时自动创建并设为 0
    print(f"defaultdict 统计词频: {dict(word_count)}")
    
    # 更复杂的例子：分组
    students = [
        ('张三', '数学', 95),
        ('李四', '数学', 87),
        ('张三', '英语', 92),
        ('王五', '数学', 78),
        ('李四', '英语', 88)
    ]
    
    # 按学科分组学生成绩
    subject_scores = defaultdict(list)
    for name, subject, score in students:
        subject_scores[subject].append((name, score))
    
    print(f"按学科分组: {dict(subject_scores)}")
    print()

def demonstrate_counter():
    """演示 Counter 的统计功能"""
    print("2️⃣ Counter - 强大的计数器")
    
    # 基本统计
    text = "abracadabra"
    char_count = Counter(text)
    print(f"字符统计: {char_count}")
    print(f"最常见的 2 个字符: {char_count.most_common(2)}")
    
    # 列表统计
    votes = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
    vote_count = Counter(votes)
    print(f"投票统计: {vote_count}")
    
    # Counter 运算
    counter1 = Counter(['a', 'b', 'c', 'a'])
    counter2 = Counter(['a', 'b', 'b', 'd'])
    print(f"Counter1: {counter1}")
    print(f"Counter2: {counter2}")
    print(f"相加: {counter1 + counter2}")
    print(f"相减: {counter1 - counter2}")
    print(f"交集: {counter1 & counter2}")
    print(f"并集: {counter1 | counter2}")
    print()

def demonstrate_deque():
    """演示 deque 的双端队列功能"""
    print("3️⃣ deque - 高效的双端队列")
    
    # 基本操作
    d = deque([1, 2, 3])
    print(f"初始 deque: {d}")
    
    # 两端添加
    d.appendleft(0)  # 左端添加
    d.append(4)      # 右端添加
    print(f"两端添加后: {d}")
    
    # 两端删除
    left = d.popleft()   # 左端删除
    right = d.pop()      # 右端删除
    print(f"删除了 {left} 和 {right}，剩余: {d}")
    
    # 旋转
    d.rotate(1)   # 向右旋转 1 位
    print(f"向右旋转 1 位: {d}")
    d.rotate(-2)  # 向左旋转 2 位
    print(f"向左旋转 2 位: {d}")
    
    # 限制长度的 deque
    limited_deque = deque(maxlen=3)
    for i in range(5):
        limited_deque.append(i)
        print(f"添加 {i}: {limited_deque}")
    print()

def demonstrate_namedtuple():
    """演示 namedtuple 的结构化数据"""
    print("4️⃣ namedtuple - 带名字的元组")
    
    # 创建 namedtuple 类
    Point = namedtuple('Point', ['x', 'y'])
    Student = namedtuple('Student', ['name', 'age', 'grade'])
    
    # 创建实例
    p1 = Point(1, 2)
    p2 = Point(x=3, y=4)
    
    print(f"点 p1: {p1}")
    print(f"p1.x = {p1.x}, p1.y = {p1.y}")
    print(f"p1[0] = {p1[0]}, p1[1] = {p1[1]}")  # 仍可按索引访问
    
    # 不可变性
    try:
        p1.x = 10
    except AttributeError as e:
        print(f"namedtuple 不可变: {e}")
    
    # 有用的方法
    student = Student('张三', 20, 'A')
    print(f"学生信息: {student}")
    print(f"转为字典: {student._asdict()}")
    
    # 替换字段（返回新对象）
    older_student = student._replace(age=21)
    print(f"年龄+1后: {older_student}")
    print()


# ==== 第二部分：自定义数据结构设计 ====
print("=== 自定义数据结构设计 ===\n")

class Stack:
    """栈的实现 - LIFO (后进先出)"""
    
    def __init__(self):
        self._items = []
    
    def push(self, item):
        """入栈"""
        self._items.append(item)
    
    def pop(self):
        """出栈"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        """查看栈顶元素"""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]
    
    def is_empty(self):
        """检查是否为空"""
        return len(self._items) == 0
    
    def size(self):
        """获取栈大小"""
        return len(self._items)
    
    def __str__(self):
        return f"Stack({self._items})"

def test_stack():
    """测试栈的功能"""
    print("自定义栈测试:")
    stack = Stack()
    
    # 入栈
    for i in [1, 2, 3, 4]:
        stack.push(i)
        print(f"入栈 {i}: {stack}")
    
    # 出栈
    while not stack.is_empty():
        item = stack.pop()
        print(f"出栈 {item}: {stack}")
    print()

class CircularBuffer:
    """环形缓冲区 - 固定大小的缓冲区"""
    
    def __init__(self, capacity):
        self.capacity = capacity
        self._buffer = [None] * capacity
        self._head = 0  # 写入位置
        self._tail = 0  # 读取位置
        self._size = 0  # 当前大小
    
    def write(self, item):
        """写入数据"""
        self._buffer[self._head] = item
        self._head = (self._head + 1) % self.capacity
        
        if self._size < self.capacity:
            self._size += 1
        else:
            # 缓冲区满了，移动 tail
            self._tail = (self._tail + 1) % self.capacity
    
    def read(self):
        """读取数据"""
        if self._size == 0:
            raise IndexError("read from empty buffer")
        
        item = self._buffer[self._tail]
        self._tail = (self._tail + 1) % self.capacity
        self._size -= 1
        return item
    
    def is_empty(self):
        return self._size == 0
    
    def is_full(self):
        return self._size == self.capacity
    
    def __str__(self):
        if self.is_empty():
            return "CircularBuffer([])"
        
        items = []
        current = self._tail
        for _ in range(self._size):
            items.append(self._buffer[current])
            current = (current + 1) % self.capacity
        return f"CircularBuffer({items})"

def test_circular_buffer():
    """测试环形缓冲区"""
    print("环形缓冲区测试:")
    buffer = CircularBuffer(3)
    
    # 写入数据
    for i in [1, 2, 3]:
        buffer.write(i)
        print(f"写入 {i}: {buffer}")
    
    # 缓冲区满了，继续写入
    for i in [4, 5]:
        buffer.write(i)
        print(f"写入 {i} (覆盖): {buffer}")
    
    # 读取数据
    while not buffer.is_empty():
        item = buffer.read()
        print(f"读取 {item}: {buffer}")
    print()


# ==== 第三部分：时间复杂度分析实战 ====
print("=== 时间复杂度分析实战 ===\n")

def analyze_list_operations():
    """分析列表操作的时间复杂度"""
    print("列表操作时间复杂度分析:")
    
    # 测试数据
    data = list(range(100000))
    
    # append - O(1) 均摊
    start_time = time.time()
    test_list = []
    for i in range(10000):
        test_list.append(i)
    append_time = time.time() - start_time
    print(f"append 10000 次耗时: {append_time:.4f}s - O(1) 均摊")
    
    # insert(0, x) - O(n)
    start_time = time.time()
    test_list = []
    for i in range(1000):  # 少一些，因为很慢
        test_list.insert(0, i)
    insert_time = time.time() - start_time
    print(f"insert(0, x) 1000 次耗时: {insert_time:.4f}s - O(n)")
    
    # in 操作 - O(n)
    start_time = time.time()
    for i in range(1000):
        _ = 99999 in data
    search_time = time.time() - start_time
    print(f"线性搜索 1000 次耗时: {search_time:.4f}s - O(n)")
    print()

def analyze_dict_operations():
    """分析字典操作的时间复杂度"""
    print("字典操作时间复杂度分析:")
    
    # 创建大字典
    large_dict = {i: f"value_{i}" for i in range(100000)}
    
    # 查找 - O(1) 平均
    start_time = time.time()
    for i in range(10000):
        _ = large_dict.get(99999)
    dict_search_time = time.time() - start_time
    print(f"字典查找 10000 次耗时: {dict_search_time:.4f}s - O(1) 平均")
    
    # 插入 - O(1) 平均
    start_time = time.time()
    test_dict = {}
    for i in range(10000):
        test_dict[i] = f"value_{i}"
    dict_insert_time = time.time() - start_time
    print(f"字典插入 10000 次耗时: {dict_insert_time:.4f}s - O(1) 平均")
    print()


# ==== 第四部分：实战项目 - LRU 缓存实现 ====
print("=== 实战项目：LRU 缓存实现 ===\n")

class LRUCache:
    """
    LRU (Least Recently Used) 缓存实现
    
    使用双向链表 + 哈希表实现 O(1) 的 get 和 put 操作
    """
    
    class _Node:
        """双向链表节点"""
        def __init__(self, key=None, value=None):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None
    
    def __init__(self, capacity: int):
        """
        初始化 LRU 缓存
        
        Args:
            capacity: 缓存容量
        """
        self.capacity = capacity
        self.cache = {}  # key -> node 的映射
        
        # 创建双向链表的哨兵节点
        self.head = self._Node()  # 头哨兵
        self.tail = self._Node()  # 尾哨兵
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _add_node(self, node):
        """在头部添加节点"""
        node.prev = self.head
        node.next = self.head.next
        
        self.head.next.prev = node
        self.head.next = node
    
    def _remove_node(self, node):
        """移除节点"""
        prev_node = node.prev
        next_node = node.next
        
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _move_to_head(self, node):
        """移动节点到头部"""
        self._remove_node(node)
        self._add_node(node)
    
    def _pop_tail(self):
        """删除尾部节点"""
        last_node = self.tail.prev
        self._remove_node(last_node)
        return last_node
    
    def get(self, key: int) -> int:
        """
        获取缓存值
        
        Args:
            key: 键
            
        Returns:
            int: 值，不存在返回 -1
        """
        node = self.cache.get(key)
        
        if not node:
            return -1
        
        # 移动到头部（标记为最近使用）
        self._move_to_head(node)
        return node.value
    
    def put(self, key: int, value: int) -> None:
        """
        设置缓存值
        
        Args:
            key: 键
            value: 值
        """
        node = self.cache.get(key)
        
        if not node:
            # 新键
            new_node = self._Node(key, value)
            
            self.cache[key] = new_node
            self._add_node(new_node)
            
            # 检查容量
            if len(self.cache) > self.capacity:
                # 删除最久未使用的
                tail_node = self._pop_tail()
                del self.cache[tail_node.key]
        else:
            # 更新现有键
            node.value = value
            self._move_to_head(node)
    
    def __str__(self):
        """显示缓存内容（从最新到最旧）"""
        items = []
        current = self.head.next
        while current != self.tail:
            items.append(f"{current.key}:{current.value}")
            current = current.next
        return f"LRUCache([{', '.join(items)}])"

def test_lru_cache():
    """测试 LRU 缓存"""
    print("LRU 缓存测试:")
    cache = LRUCache(3)
    
    # 添加数据
    cache.put(1, "A")
    print(f"put(1, A): {cache}")
    
    cache.put(2, "B")
    print(f"put(2, B): {cache}")
    
    cache.put(3, "C")
    print(f"put(3, C): {cache}")
    
    # 访问数据
    value = cache.get(1)
    print(f"get(1) = {value}: {cache}")
    
    # 添加新数据（触发淘汰）
    cache.put(4, "D")
    print(f"put(4, D): {cache} (淘汰了 2)")
    
    # 测试不存在的键
    value = cache.get(2)
    print(f"get(2) = {value} (已被淘汰)")
    
    # 更新现有键
    cache.put(1, "A_updated")
    print(f"put(1, A_updated): {cache}")
    print()


# ==== 运行所有演示 ====
def run_all_demos():
    """运行所有演示"""
    demonstrate_defaultdict()
    demonstrate_counter()
    demonstrate_deque()
    demonstrate_namedtuple()
    
    test_stack()
    test_circular_buffer()
    
    analyze_list_operations()
    analyze_dict_operations()
    
    test_lru_cache()

def todays_exercises():
    """今天的练习任务"""
    print("=== 今天的练习任务 ===\n")
    
    print("🎯 任务 1: 实现一个智能的词频统计器")
    print("要求：")
    print("- 使用 Counter 统计词频")
    print("- 支持忽略大小写")
    print("- 支持忽略标点符号")
    print("- 提供最常见词汇的分析")
    print()
    
    print("🎯 任务 2: 设计一个任务队列")
    print("要求：")
    print("- 使用 deque 实现")
    print("- 支持优先级（高优先级任务先执行）")
    print("- 支持任务延迟执行")
    print("- 分析时间复杂度")
    print()
    
    print("🎯 任务 3: 优化 LRU 缓存")
    print("要求：")
    print("- 添加缓存命中率统计")
    print("- 支持设置过期时间")
    print("- 添加缓存大小监控")
    print("- 实现缓存持久化（可选）")
    print()
    
    print("🎯 思考题:")
    print("1. 什么时候使用 list，什么时候使用 deque？")
    print("2. defaultdict 和普通 dict 的性能差异？")
    print("3. LRU 缓存的哪些操作是 O(1) 的，为什么？")

if __name__ == "__main__":
    run_all_demos()
    todays_exercises()