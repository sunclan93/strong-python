"""
异步编程基础 - 理解同步 vs 异步
"""

import time
import asyncio

# ==================== 同步代码示例 ====================

print("=" * 70)
print("1. 同步代码（阻塞）")
print("=" * 70)

def sync_task(name, duration):
    """同步任务"""
    print(f"⏳ 开始 {name}")
    time.sleep(duration)  # 阻塞
    print(f"✅ 完成 {name}")
    return f"{name}结果"


def run_sync():
    """串行执行"""
    start = time.time()
    
    result1 = sync_task("任务1", 2)
    result2 = sync_task("任务2", 3)
    result3 = sync_task("任务3", 1)
    
    elapsed = time.time() - start
    print(f"\n⏱️  总耗时: {elapsed:.2f}秒")


# 运行同步版本
run_sync()


# ==================== 异步代码示例 ====================

print("\n" + "=" * 70)
print("2. 异步代码（非阻塞）")
print("=" * 70)

async def async_task(name, duration):
    """异步任务"""
    print(f"⏳ 开始 {name}")
    await asyncio.sleep(duration)  # 不阻塞，让出控制权
    print(f"✅ 完成 {name}")
    return f"{name}结果"


async def run_async():
    """并发执行"""
    start = time.time()
    
    # 三个任务同时运行
    results = await asyncio.gather(
        async_task("任务A", 2),
        async_task("任务B", 3),
        async_task("任务C", 1)
    )
    
    elapsed = time.time() - start
    print(f"\n⏱️  总耗时: {elapsed:.2f}秒")
    print(f"📊 结果: {results}")


# 运行异步版本
asyncio.run(run_async())


# ==================== 核心概念讲解 ====================

print("\n" + "=" * 70)
print("3. 异步编程核心概念")
print("=" * 70)

concepts = """
🔑 关键字：

async def func():
    → 定义协程函数（coroutine）
    → 不能直接调用 func()，要用 await

await func():
    → 等待协程完成
    → 只能在 async 函数内使用
    → 让出控制权，允许其他任务运行

asyncio.run():
    → 运行异步主函数
    → 创建事件循环

asyncio.gather():
    → 并发运行多个协程
    → 等待所有完成
"""

print(concepts)


# ==================== 实战：并发下载 ====================

print("=" * 70)
print("4. 实战：模拟并发下载")
print("=" * 70)

async def download_file(url, size):
    """模拟下载文件"""
    print(f"📥 开始下载: {url}")
    
    # 模拟下载过程
    for i in range(size):
        await asyncio.sleep(0.5)  # 模拟网络延迟
        print(f"  {url}: {(i+1)*20}%")
    
    print(f"✅ {url} 下载完成")
    return f"文件_{url}"


async def download_multiple():
    """并发下载多个文件"""
    start = time.time()
    
    files = await asyncio.gather(
        download_file("file1.zip", 3),
        download_file("file2.pdf", 2),
        download_file("file3.mp4", 4)
    )
    
    elapsed = time.time() - start
    print(f"\n⏱️  总耗时: {elapsed:.2f}秒")
    print(f"📦 下载的文件: {files}")


# 运行
asyncio.run(download_multiple())


# ==================== 异步 vs 多线程 ====================

print("\n" + "=" * 70)
print("5. 异步 vs 多线程 vs 多进程")
print("=" * 70)

comparison = """
异步（asyncio）
  ✅ 适合：I/O 密集型（网络、文件）
  ✅ 优势：低开销、高并发
  ❌ 限制：单线程、不适合 CPU 密集

多线程（threading）
  ✅ 适合：I/O 密集 + 需要共享内存
  ❌ 限制：GIL 限制、竞态条件

多进程（multiprocessing）
  ✅ 适合：CPU 密集型（计算）
  ❌ 限制：开销大、通信成本高

选择建议：
  • 网络请求、文件 I/O → asyncio ⭐
  • 数据处理、科学计算 → multiprocessing
  • 混合场景 → asyncio + 线程池
"""

print(comparison)


# ==================== 常见陷阱 ====================

print("=" * 70)
print("6. 常见错误")
print("=" * 70)

print("\n❌ 错误1: 忘记 await")
print("async def wrong():")
print("    result = async_task()  # 错误！返回协程对象")
print("    print(result)  # <coroutine object>")
print()
print("✅ 正确:")
print("async def correct():")
print("    result = await async_task()  # 正确")

print("\n❌ 错误2: 在同步函数中 await")
print("def wrong():")
print("    await async_task()  # SyntaxError!")
print()
print("✅ 正确:")
print("async def correct():")
print("    await async_task()")

print("\n❌ 错误3: 阻塞事件循环")
print("async def wrong():")
print("    time.sleep(1)  # 阻塞！其他任务无法运行")
print()
print("✅ 正确:")
print("async def correct():")
print("    await asyncio.sleep(1)  # 非阻塞")


# ==================== 简单示例 ====================

print("\n" + "=" * 70)
print("7. 实用示例：异步 HTTP 请求（概念）")
print("=" * 70)

async def fetch_data(url):
    """模拟异步 HTTP 请求"""
    print(f"🌐 请求: {url}")
    await asyncio.sleep(1)  # 模拟网络延迟
    return f"{url} 的数据"


async def fetch_all():
    """并发请求多个 URL"""
    urls = [
        "https://api1.com/data",
        "https://api2.com/data",
        "https://api3.com/data"
    ]
    
    # 并发请求
    results = await asyncio.gather(
        *[fetch_data(url) for url in urls]
    )
    
    for result in results:
        print(f"  📦 {result}")


asyncio.run(fetch_all())


print("\n✅ 异步编程基础完成！")