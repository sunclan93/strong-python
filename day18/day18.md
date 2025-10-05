Day 18：设计模式总结 + 异步编程预习🎯 今日学习目标

回顾并整合设计模式知识
完成综合项目：事件驱动的任务系统
理解异步编程的必要性
初步接触 asyncio 基础概念

二、异步编程基础💡 为什么需要异步？同步代码的问题：
python# 串行执行，总耗时 = 6秒
download_file()  # 2秒
process_data()   # 3秒
send_email()     # 1秒异步的优势：
python# 并发执行，总耗时 ≈ 3秒（最长任务的时间）
await asyncio.gather(
    download_file(),  # 同时进行
    process_data(),   # 同时进行
    send_email()      # 同时进行
)

三、异步编程核心概念
🔑 三个关键概念