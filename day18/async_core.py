"""
异步编程核心概念 - 协程、任务、事件循环
"""

import asyncio
import time

# ==================== 概念1: 协程（Coroutine）====================

print("=" * 70)
print("概念1: 协程 - 可暂停的函数")
print("=" * 70)

async def simple_coroutine():
    """这是一个协程"""
    print("  开始执行")
    await asyncio.sleep(1)  # 暂停点
    print("  继续执行")
    return "完成"


# 协程的特点
print("\n协程对象:")
coro = simple_coroutine()  # 不会执行，只是创建对象
print(f"  类型: {type(coro)}")
print(f"  对象: {coro}")

# 运行协程
print("\n运行协程:")
result = asyncio.run(simple_coroutine())
print(f"  返回值: {result}")


# ==================== 概念2: 任务（Task）====================

print("\n" + "=" * 70)
print("概念2: 任务 - 被调度的协程")
print("=" * 70)

async def worker(name, delay):
    """工作协程"""
    print(f"⚙️  {name} 开始")
    await asyncio.sleep(delay)
    print(f"✅ {name} 完成")
    return f"{name} 的结果"


async def create_tasks():
    """创建任务"""
    print("创建任务（不等待）:")
    
    # 创建任务 - 立即开始执行
    task1 = asyncio.create_task(worker("任务1", 2))
    task2 = asyncio.create_task(worker("任务2", 1))
    
    print(f"  任务1 状态: {task1}")
    print(f"  任务2 状态: {task2}")
    
    # 等待所有任务完成
    print("\n等待任务完成:")
    results = await asyncio.gather(task1, task2)
    print(f"  结果: {results}")


asyncio.run(create_tasks())


# ==================== 概念3: 事件循环（Event Loop）====================

print("\n" + "=" * 70)
print("概念3: 事件循环 - 任务调度器")
print("=" * 70)

event_loop_concept = """
事件循环的工作方式：

1. 有任务队列 [任务A, 任务B, 任务C]

2. 循环执行：
   ┌─────────────────┐
   │ 取出任务A        │
   │ 执行到 await     │ ← 遇到 await 就暂停
   │ 放回队列末尾     │
   ├─────────────────┤
   │ 取出任务B        │
   │ 执行到 await     │
   │ 放回队列末尾     │
   └─────────────────┘
   
3. 所有任务完成 → 结束

关键点：
  • 单线程
  • 协作式多任务
  • 遇到 await 切换任务
"""

print(event_loop_concept)


# ==================== 并发模式对比 ====================

print("=" * 70)
print("并发执行模式对比")
print("=" * 70)

async def task_a():
    print("  A-1")
    await asyncio.sleep(1)
    print("  A-2")
    await asyncio.sleep(1)
    print("  A-3")


async def task_b():
    print("  B-1")
    await asyncio.sleep(1)
    print("  B-2")
    await asyncio.sleep(1)
    print("  B-3")


print("\n模式1: 串行（await）")
async def sequential():
    await task_a()  # 等待 A 完成
    await task_b()  # 再执行 B


print("执行顺序: A-1 → A-2 → A-3 → B-1 → B-2 → B-3")
# asyncio.run(sequential())


print("\n模式2: 并发（gather）")
async def concurrent():
    await asyncio.gather(
        task_a(),
        task_b()
    )


print("执行顺序: A-1, B-1 → A-2, B-2 → A-3, B-3")
# asyncio.run(concurrent())


# ==================== 实用工具 ====================

print("\n" + "=" * 70)
print("常用异步工具")
print("=" * 70)

async def async_tools_demo():
    """异步工具演示"""
    
    # 1. asyncio.sleep - 异步延迟
    print("1. asyncio.sleep")
    await asyncio.sleep(0.5)
    print("   等待完成")
    
    # 2. asyncio.gather - 并发执行
    print("\n2. asyncio.gather")
    results = await asyncio.gather(
        asyncio.sleep(0.5, result="A"),
        asyncio.sleep(0.3, result="B"),
        asyncio.sleep(0.4, result="C")
    )
    print(f"   结果: {results}")
    
    # 3. asyncio.wait_for - 超时控制
    print("\n3. asyncio.wait_for")
    try:
        result = await asyncio.wait_for(
            asyncio.sleep(2, result="慢任务"),
            timeout=1.0
        )
    except asyncio.TimeoutError:
        print("   ⏱️  超时！")
    
    # 4. asyncio.create_task - 后台任务
    print("\n4. asyncio.create_task")
    task = asyncio.create_task(asyncio.sleep(0.5))
    print("   任务已创建，继续执行其他代码...")
    await task
    print("   任务完成")


asyncio.run(async_tools_demo())


# ==================== 异步上下文管理器 ====================

print("\n" + "=" * 70)
print("异步上下文管理器")
print("=" * 70)

class AsyncResource:
    """异步资源"""
    
    async def __aenter__(self):
        print("  🔌 连接资源")
        await asyncio.sleep(0.5)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("  🔌 关闭资源")
        await asyncio.sleep(0.5)
    
    async def query(self, data):
        print(f"  🔍 查询: {data}")
        await asyncio.sleep(0.3)
        return f"结果: {data}"


async def use_async_resource():
    """使用异步上下文管理器"""
    async with AsyncResource() as resource:
        result = await resource.query("数据")
        print(f"  {result}")


asyncio.run(use_async_resource())


# ==================== 异步迭代器 ====================

print("\n" + "=" * 70)
print("异步迭代器")
print("=" * 70)

class AsyncCounter:
    """异步计数器"""
    
    def __init__(self, max_count):
        self.max_count = max_count
        self.current = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.max_count:
            raise StopAsyncIteration
        
        await asyncio.sleep(0.3)  # 模拟异步操作
        self.current += 1
        return self.current


async def use_async_iterator():
    """使用异步迭代器"""
    counter = AsyncCounter(5)
    
    async for num in counter:
        print(f"  计数: {num}")


asyncio.run(use_async_iterator())


# ==================== 最佳实践 ====================

print("\n" + "=" * 70)
print("异步编程最佳实践")
print("=" * 70)

best_practices = """
✅ DO（推荐）：

1. I/O 操作用异步
   await asyncio.sleep()  # 而非 time.sleep()
   await aiohttp.get()    # 而非 requests.get()

2. 用 asyncio.gather 并发
   await asyncio.gather(task1, task2, task3)

3. 设置超时
   await asyncio.wait_for(slow_task(), timeout=5)

4. 异常处理
   try:
       await risky_task()
   except Exception as e:
       logger.error(f"错误: {e}")

❌ DON'T（避免）：

1. 不要在异步函数中阻塞
   time.sleep()       # ❌ 阻塞整个事件循环
   requests.get()     # ❌ 阻塞

2. 不要忘记 await
   task()            # ❌ 返回协程对象
   await task()      # ✅ 执行并等待

3. 不要过度使用
   简单脚本不需要异步
"""

print(best_practices)


print("\n✅ 异步编程核心概念完成！")