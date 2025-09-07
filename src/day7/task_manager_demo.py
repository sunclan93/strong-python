#!/usr/bin/env python3
"""
任务管理器演示和测试脚本
展示所有高级特性的综合应用
"""

import os
import time
import tempfile
from datetime import datetime, timedelta
from task_manager_project import (
    TaskManager, Task, TaskStatus, Priority,
    task_batch_operation, DataStorageContext
)

def demo_basic_operations():
    """演示基础CRUD操作"""
    print("=" * 60)
    print("🔸 基础操作演示")
    print("=" * 60)
    
    # 使用临时文件避免影响主数据
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        manager = TaskManager(temp_path)
        
        print("1. 创建任务:")
        task1 = manager.create_task(
            title="学习设计模式",
            description="深入理解23种设计模式",
            priority=Priority.HIGH,
            tags=["学习", "设计模式"]
        )
        print(f"   ✅ 创建任务: {task1.id} - {task1.title}")
        
        task2 = manager.create_task(
            title="写技术博客",
            description="分享Python学习心得",
            priority=Priority.MEDIUM,
            due_date=datetime.now() + timedelta(days=7),
            tags=["写作", "分享"]
        )
        print(f"   ✅ 创建任务: {task2.id} - {task2.title}")
        
        print(f"\n2. 当前任务总数: {len(manager.get_all_tasks())}")
        
        print("\n3. 更新任务状态:")
        manager.update_task(task1.id, status=TaskStatus.IN_PROGRESS)
        print(f"   ✅ 任务 {task1.id} 状态更新为: IN_PROGRESS")
        
        print("\n4. 查询任务:")
        task = manager.get_task(task1.id)
        print(f"   📋 任务详情: {task.title} - {task.status.value}")
        
        print("\n5. 删除任务:")
        manager.delete_task(task2.id)
        print(f"   🗑️  删除任务: {task2.id}")
        
        print(f"\n✅ 基础操作演示完成，剩余任务数: {len(manager.get_all_tasks())}")
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def demo_advanced_features():
    """演示高级特性：生成器、闭包、装饰器"""
    print("\n" + "=" * 60)
    print("🔸 高级特性演示")
    print("=" * 60)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        manager = TaskManager(temp_path)
        
        # 创建测试数据
        test_tasks = [
            {"title": "高优先级任务1", "priority": Priority.HIGH, "tags": ["重要"]},
            {"title": "中优先级任务1", "priority": Priority.MEDIUM, "tags": ["日常"]},
            {"title": "紧急任务", "priority": Priority.URGENT, "tags": ["紧急", "重要"]},
            {"title": "低优先级任务1", "priority": Priority.LOW, "tags": ["可选"]},
            {"title": "高优先级任务2", "priority": Priority.HIGH, "tags": ["重要"]},
        ]
        
        print("1. 批量创建任务:")
        created_tasks = manager.batch_create_tasks(test_tasks)
        print(f"   ✅ 批量创建 {len(created_tasks)} 个任务")
        
        print("\n2. 生成器过滤演示:")
        # 使用生成器过滤高优先级任务
        high_priority_tasks = list(manager.filter_tasks(priority=Priority.HIGH))
        print(f"   🔍 高优先级任务数量: {len(high_priority_tasks)}")
        for task in high_priority_tasks:
            print(f"      - {task.title}")
        
        # 使用生成器搜索任务
        search_results = list(manager.search_tasks("任务"))
        print(f"\n   🔍 搜索结果 ('任务'): {len(search_results)} 个")
        
        print("\n3. 闭包统计演示:")
        # 创建统计计算器（闭包）
        stats_calc = manager.create_stats_calculator()
        
        # 多次调用，观察计算次数变化
        for i in range(3):
            stats = stats_calc()
            print(f"   📊 第 {i+1} 次统计 - 总任务: {stats['total']}, 计算次数: {stats['calculation_count']}")
        
        print("\n4. 装饰器功能演示:")
        print("   🎯 观察日志输出中的装饰器效果:")
        print("      - @log_operation: 记录操作日志")
        print("      - @validate_task_exists: 验证任务存在")
        print("      - @auto_save: 自动保存数据")
        
        # 触发装饰器
        task_id = created_tasks[0].id
        try:
            manager.update_task("不存在的ID", status=TaskStatus.COMPLETED)
        except ValueError as e:
            print(f"   ❌ 验证装饰器生效: {e}")
        
        manager.update_task(task_id, status=TaskStatus.COMPLETED)
        print(f"   ✅ 成功更新任务状态")
        
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def demo_context_managers():
    """演示上下文管理器的使用"""
    print("\n" + "=" * 60)
    print("🔸 上下文管理器演示")
    print("=" * 60)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        manager = TaskManager(temp_path)
        
        print("1. 数据存储上下文管理器:")
        # DataStorageContext 在保存时自动创建备份
        with DataStorageContext(temp_path, backup_enabled=True) as storage:
            print("   📁 进入存储上下文，备份已创建")
            
            # 创建一些任务
            manager.create_task("测试任务1", priority=Priority.HIGH)
            manager.create_task("测试任务2", priority=Priority.MEDIUM)
            
            print("   💾 数据修改完成")
        print("   ✅ 退出存储上下文，备份管理完成")
        
        print("\n2. 批量操作上下文管理器:")
        with task_batch_operation(manager) as batch_manager:
            print("   🔄 进入批量操作模式（禁用自动保存）")
            
            # 批量更新状态
            all_tasks = batch_manager.get_all_tasks()
            task_ids = [task.id for task in all_tasks[:2]]
            
            updated_count = batch_manager.batch_update_status(
                task_ids, TaskStatus.IN_PROGRESS
            )
            print(f"   ✅ 批量更新 {updated_count} 个任务状态")
            
        print("   💾 退出批量操作，统一保存数据")
        
        print("\n3. 异常安全演示:")
        try:
            with DataStorageContext(temp_path, backup_enabled=True) as storage:
                print("   ⚠️  模拟操作异常...")
                manager.create_task("这个任务会因异常被回滚")
                raise Exception("模拟的数据操作异常")
        except Exception as e:
            print(f"   🔄 异常被捕获: {e}")
            print("   📁 数据已从备份恢复")
    
    finally:
        # 清理所有临时文件
        for ext in ['', '.backup', '.tmp']:
            file_path = temp_path + ext
            if os.path.exists(file_path):
                os.unlink(file_path)

def demo_error_handling():
    """演示异常处理"""
    print("\n" + "=" * 60)
    print("🔸 异常处理演示")
    print("=" * 60)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        manager = TaskManager(temp_path)
        
        print("1. 数据验证异常:")
        try:
            # 空标题应该抛出异常
            Task(title="", description="测试")
        except ValueError as e:
            print(f"   ❌ 捕获验证异常: {e}")
        
        print("\n2. 任务不存在异常:")
        try:
            manager.get_task("不存在的ID")
        except ValueError as e:
            print(f"   ❌ 捕获业务异常: {e}")
        
        print("\n3. 批量操作错误处理:")
        # 包含无效数据的批量创建
        invalid_tasks = [
            {"title": "正常任务", "priority": Priority.HIGH},
            {"title": "", "description": "无效任务"},  # 空标题
            {"title": "另一个正常任务", "priority": Priority.LOW}
        ]
        
        created_tasks = manager.batch_create_tasks(invalid_tasks)
        print(f"   ✅ 批量创建结果: {len(created_tasks)} 个成功, {len(invalid_tasks) - len(created_tasks)} 个失败")
        
        print("\n4. 文件操作异常处理:")
        # 尝试保存到无权限目录
        readonly_manager = TaskManager("/root/readonly.json")  # 通常无权限
        readonly_manager.create_task("测试任务")
        try:
            readonly_manager.save_tasks()
        except Exception as e:
            print(f"   ❌ 文件操作异常被处理: {type(e).__name__}")
    
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def demo_performance_and_memory():
    """演示性能和内存效率"""
    print("\n" + "=" * 60)
    print("🔸 性能和内存效率演示")
    print("=" * 60)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        manager = TaskManager(temp_path)
        
        print("1. 大量数据创建:")
        start_time = time.time()
        
        # 创建大量任务进行测试
        large_batch = []
        for i in range(100):
            large_batch.append({
                "title": f"任务 {i+1:03d}",
                "description": f"这是第 {i+1} 个测试任务",
                "priority": Priority.MEDIUM if i % 2 == 0 else Priority.HIGH,
                "tags": [f"batch_{i//10}", "test"]
            })
        
        created_tasks = manager.batch_create_tasks(large_batch)
        creation_time = time.time() - start_time
        
        print(f"   ⏱️  创建 {len(created_tasks)} 个任务耗时: {creation_time:.3f}秒")
        
        print("\n2. 生成器内存效率演示:")
        start_time = time.time()
        
        # 使用生成器遍历，节省内存
        count = 0
        for task in manager.filter_tasks(priority=Priority.HIGH):
            count += 1
            # 只处理前几个，演示生成器的懒加载特性
            if count >= 5:
                break
        
        filter_time = time.time() - start_time
        print(f"   🔍 生成器过滤前5个高优先级任务耗时: {filter_time:.6f}秒")
        
        print("\n3. 统计计算性能:")
        stats_calc = manager.create_stats_calculator()
        
        start_time = time.time()
        stats = stats_calc()
        stats_time = time.time() - start_time
        
        print(f"   📊 统计计算耗时: {stats_time:.6f}秒")
        print(f"   📈 任务完成率: {stats['completion_rate']:.1f}%")
        print(f"   📋 按状态分布: {stats['by_status']}")
        
        print("\n4. 数据持久化性能:")
        start_time = time.time()
        manager.save_tasks()
        save_time = time.time() - start_time
        
        print(f"   💾 保存 {len(manager.get_all_tasks())} 个任务耗时: {save_time:.6f}秒")
        
        # 测试加载性能
        new_manager = TaskManager(temp_path)
        start_time = time.time()
        new_manager.load_tasks()
        load_time = time.time() - start_time
        
        print(f"   📂 加载 {len(new_manager.get_all_tasks())} 个任务耗时: {load_time:.6f}秒")
    
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def demo_real_world_scenarios():
    """演示真实世界的使用场景"""
    print("\n" + "=" * 60)
    print("🔸 真实场景演示")
    print("=" * 60)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
        temp_path = temp_file.name
    
    try:
        manager = TaskManager(temp_path)
        
        print("1. 项目管理场景:")
        project_tasks = [
            {
                "title": "需求分析",
                "description": "收集和分析用户需求",
                "priority": Priority.HIGH,
                "tags": ["项目", "分析"],
                "due_date": datetime.now() + timedelta(days=3)
            },
            {
                "title": "系统设计",
                "description": "设计系统架构和数据库",
                "priority": Priority.HIGH,
                "tags": ["项目", "设计"]
            },
            {
                "title": "编码实现",
                "description": "核心功能开发",
                "priority": Priority.MEDIUM,
                "tags": ["项目", "开发"]
            },
            {
                "title": "测试验证",
                "description": "单元测试和集成测试",
                "priority": Priority.MEDIUM,
                "tags": ["项目", "测试"]
            },
            {
                "title": "部署上线",
                "description": "生产环境部署",
                "priority": Priority.URGENT,
                "tags": ["项目", "部署"]
            }
        ]
        
        created_tasks = manager.batch_create_tasks(project_tasks)
        print(f"   📋 创建项目任务: {len(created_tasks)} 个")
        
        print("\n2. 工作流演示:")
        # 模拟任务状态变化
        task_ids = [task.id for task in created_tasks]
        
        # 开始前两个任务
        manager.update_task(task_ids[0], status=TaskStatus.IN_PROGRESS)
        manager.update_task(task_ids[1], status=TaskStatus.IN_PROGRESS)
        print("   🔄 开始需求分析和系统设计")
        
        # 完成需求分析
        manager.update_task(task_ids[0], status=TaskStatus.COMPLETED)
        print("   ✅ 需求分析完成")
        
        # 开始编码
        manager.update_task(task_ids[2], status=TaskStatus.IN_PROGRESS)
        print("   🔄 开始编码实现")
        
        print("\n3. 进度跟踪:")
        stats_calc = manager.create_stats_calculator()
        stats = stats_calc()
        
        print(f"   📊 项目进度:")
        print(f"      总任务: {stats['total']}")
        print(f"      已完成: {stats['by_status']['completed']}")
        print(f"      进行中: {stats['by_status']['in_progress']}")
        print(f"      待开始: {stats['by_status']['pending']}")
        print(f"      完成率: {stats['completion_rate']:.1f}%")
        
        print("\n4. 任务查询和过滤:")
        # 查找项目相关任务
        project_tasks = list(manager.filter_tasks(tags=["项目"]))
        print(f"   🔍 项目相关任务: {len(project_tasks)} 个")
        
        # 查找高优先级未完成任务
        high_priority_pending = []
        for task in manager.filter_tasks(priority=Priority.HIGH):
            if task.status != TaskStatus.COMPLETED:
                high_priority_pending.append(task)
        
        print(f"   🚨 高优先级待办: {len(high_priority_pending)} 个")
        for task in high_priority_pending:
            print(f"      - {task.title} ({task.status.value})")
        
        print("\n5. 过期任务检查:")
        # 模拟一个过期任务
        overdue_task = manager.create_task(
            "紧急修复",
            description="修复生产环境bug",
            priority=Priority.URGENT,
            due_date=datetime.now() - timedelta(hours=1)  # 一小时前到期
        )
        
        overdue_tasks = list(manager.filter_tasks(overdue=True))
        print(f"   ⚠️  过期任务: {len(overdue_tasks)} 个")
        for task in overdue_tasks:
            print(f"      - {task.title} (过期 {datetime.now() - task.due_date})")
    
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)

def main():
    """主演示程序"""
    print("🎯 任务管理器综合演示")
    print("展示第一周学习的所有高级特性")
    print("\n" + "=" * 80)
    
    # 运行所有演示
    demo_basic_operations()
    demo_advanced_features()
    demo_context_managers()
    demo_error_handling()
    demo_performance_and_memory()
    demo_real_world_scenarios()
    
    print("\n" + "=" * 80)
    print("🎊 演示完成！")
    print("\n📚 本项目综合运用的技术:")
    print("   ✅ 面向对象编程 (OOP)")
    print("   ✅ 装饰器模式 (@log_operation, @validate_task_exists, @auto_save)")
    print("   ✅ 生成器和迭代器 (filter_tasks, search_tasks)")
    print("   ✅ 闭包 (create_stats_calculator)")
    print("   ✅ 上下文管理器 (DataStorageContext, task_batch_operation)")
    print("   ✅ 异常处理 (自定义异常体系，优雅错误处理)")
    print("   ✅ 数据持久化 (JSON序列化，原子性操作)")
    print("   ✅ 类型提示 (Type hints)")
    print("   ✅ 数据类 (@dataclass)")
    print("   ✅ 枚举 (Enum)")
    
    print("\n🚀 项目特色:")
    print("   🎯 模块化设计，职责清晰")
    print("   🔒 异常安全，数据可靠")
    print("   ⚡ 内存高效，性能优良")
    print("   🛠️ 易于扩展，维护友好")
    print("   📝 完整日志，便于调试")

if __name__ == "__main__":
    main()