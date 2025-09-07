#!/usr/bin/env python3
"""
命令行任务管理器 - 第一周综合项目
综合运用：OOP、装饰器、生成器、闭包、上下文管理器、异常处理
"""

import json
import os
import uuid
import logging
import contextlib
import functools
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Generator, Any, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum, auto

# =============================================================================
# 1. 数据模型定义 (使用 @dataclass 和枚举)
# =============================================================================

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Priority(Enum):
    """优先级枚举"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class Task:
    """任务数据模型"""
    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def __post_init__(self):
        """数据验证和处理"""
        if not self.title.strip():
            raise ValueError("任务标题不能为空")
        
        # 确保枚举类型正确
        if isinstance(self.priority, str):
            self.priority = Priority[self.priority.upper()]
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status.lower())
    
    def update_timestamp(self):
        """更新修改时间"""
        self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """检查是否过期"""
        if self.due_date and self.status != TaskStatus.COMPLETED:
            return datetime.now() > self.due_date
        return False
    
    def to_dict(self) -> dict:
        """转换为字典（用于序列化）"""
        data = asdict(self)
        # 处理特殊类型
        data['priority'] = self.priority.name
        data['status'] = self.status.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.due_date:
            data['due_date'] = self.due_date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """从字典创建任务对象"""
        # 处理时间字段
        if 'created_at' in data:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        if 'due_date' in data and data['due_date']:
            data['due_date'] = datetime.fromisoformat(data['due_date'])
        
        return cls(**data)

# =============================================================================
# 2. 装饰器定义 (权限控制、日志记录、性能监控)
# =============================================================================

def log_operation(operation_name: str):
    """操作日志装饰器"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            logger = logging.getLogger(__name__)
            
            try:
                logger.info(f"开始执行: {operation_name}")
                result = func(*args, **kwargs)
                duration = datetime.now() - start_time
                logger.info(f"操作完成: {operation_name} (耗时: {duration.total_seconds():.3f}秒)")
                return result
            except Exception as e:
                duration = datetime.now() - start_time
                logger.error(f"操作失败: {operation_name} - {e} (耗时: {duration.total_seconds():.3f}秒)")
                raise
        return wrapper
    return decorator

def validate_task_exists(func: Callable) -> Callable:
    """验证任务存在的装饰器"""
    @functools.wraps(func)
    def wrapper(self, task_id: str, *args, **kwargs):
        if task_id not in self.tasks:
            raise ValueError(f"任务不存在: {task_id}")
        return func(self, task_id, *args, **kwargs)
    return wrapper

def auto_save(func: Callable) -> Callable:
    """自动保存装饰器"""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        # 如果方法修改了数据，自动保存
        if hasattr(self, 'auto_save_enabled') and self.auto_save_enabled:
            self.save_tasks()
        return result
    return wrapper

# =============================================================================
# 3. 上下文管理器 (数据持久化管理)
# =============================================================================

class DataStorageContext:
    """数据存储上下文管理器"""
    
    def __init__(self, storage_path: str, backup_enabled: bool = True):
        self.storage_path = storage_path
        self.backup_enabled = backup_enabled
        self.backup_path = f"{storage_path}.backup"
        self.temp_path = f"{storage_path}.tmp"
    
    def __enter__(self):
        """进入时创建备份"""
        if self.backup_enabled and os.path.exists(self.storage_path):
            import shutil
            shutil.copy2(self.storage_path, self.backup_path)
            logging.info(f"创建数据备份: {self.backup_path}")
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """退出时清理临时文件"""
        # 清理临时文件
        if os.path.exists(self.temp_path):
            os.remove(self.temp_path)
        
        if exc_type is not None:
            # 发生异常时恢复备份
            if self.backup_enabled and os.path.exists(self.backup_path):
                import shutil
                shutil.copy2(self.backup_path, self.storage_path)
                logging.warning("数据操作失败，已恢复备份")
        else:
            # 成功时删除备份（可选）
            if os.path.exists(self.backup_path):
                logging.info("数据操作成功")
        
        return False  # 不抑制异常

@contextlib.contextmanager
def task_batch_operation(task_manager: 'TaskManager'):
    """批量操作上下文管理器"""
    original_auto_save = getattr(task_manager, 'auto_save_enabled', True)
    task_manager.auto_save_enabled = False
    
    try:
        logging.info("开始批量操作")
        yield task_manager
        # 批量操作完成后统一保存
        task_manager.save_tasks()
        logging.info("批量操作完成，数据已保存")
    except Exception as e:
        logging.error(f"批量操作失败: {e}")
        raise
    finally:
        task_manager.auto_save_enabled = original_auto_save

# =============================================================================
# 4. 任务管理器核心类 (综合运用所有特性)
# =============================================================================

class TaskManager:
    """任务管理器核心类"""
    
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = storage_path
        self.tasks: Dict[str, Task] = {}
        self.auto_save_enabled = True
        self._setup_logging()
        self.load_tasks()
    
    def _setup_logging(self):
        """设置日志系统"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('task_manager.log'),
                logging.StreamHandler()
            ]
        )
    
    # 任务CRUD操作 =============================================================
    
    @log_operation("创建任务")
    @auto_save
    def create_task(self, title: str, description: str = "", 
                   priority: Priority = Priority.MEDIUM, 
                   due_date: Optional[datetime] = None,
                   tags: Optional[List[str]] = None) -> Task:
        """创建新任务"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tags=tags or []
        )
        
        self.tasks[task.id] = task
        logging.info(f"创建任务: {task.id} - {task.title}")
        return task
    
    @log_operation("更新任务")
    @validate_task_exists
    @auto_save
    def update_task(self, task_id: str, **updates) -> Task:
        """更新任务"""
        task = self.tasks[task_id]
        
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.update_timestamp()
        logging.info(f"更新任务: {task_id}")
        return task
    
    @log_operation("删除任务")
    @validate_task_exists
    @auto_save
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        task = self.tasks.pop(task_id)
        logging.info(f"删除任务: {task_id} - {task.title}")
        return True
    
    @validate_task_exists
    def get_task(self, task_id: str) -> Task:
        """获取单个任务"""
        return self.tasks[task_id]
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        return list(self.tasks.values())
    
    # 任务查询和过滤 (使用生成器提高内存效率) ====================================
    
    def filter_tasks(self, **criteria) -> Generator[Task, None, None]:
        """过滤任务 - 使用生成器节省内存"""
        for task in self.tasks.values():
            match = True
            
            # 状态过滤
            if 'status' in criteria:
                if task.status != criteria['status']:
                    match = False
            
            # 优先级过滤
            if 'priority' in criteria:
                if task.priority != criteria['priority']:
                    match = False
            
            # 标签过滤
            if 'tags' in criteria:
                required_tags = criteria['tags']
                if not all(tag in task.tags for tag in required_tags):
                    match = False
            
            # 过期状态过滤
            if 'overdue' in criteria:
                if task.is_overdue() != criteria['overdue']:
                    match = False
            
            if match:
                yield task
    
    def search_tasks(self, query: str) -> Generator[Task, None, None]:
        """搜索任务 - 在标题和描述中搜索"""
        query_lower = query.lower()
        for task in self.tasks.values():
            if (query_lower in task.title.lower() or 
                query_lower in task.description.lower()):
                yield task
    
    def get_tasks_by_priority(self) -> Dict[Priority, List[Task]]:
        """按优先级分组任务"""
        groups = {priority: [] for priority in Priority}
        for task in self.tasks.values():
            groups[task.priority].append(task)
        return groups
    
    # 统计和分析功能 (使用闭包保存状态) ==========================================
    
    def create_stats_calculator(self):
        """创建统计计算器 - 使用闭包"""
        calculation_count = 0
        
        def calculate_stats() -> dict:
            nonlocal calculation_count
            calculation_count += 1
            
            total_tasks = len(self.tasks)
            if total_tasks == 0:
                return {
                    'total': 0,
                    'calculation_count': calculation_count
                }
            
            # 按状态统计
            status_counts = {}
            for status in TaskStatus:
                status_counts[status.value] = len(list(
                    self.filter_tasks(status=status)
                ))
            
            # 按优先级统计
            priority_counts = {}
            for priority in Priority:
                priority_counts[priority.name] = len(list(
                    self.filter_tasks(priority=priority)
                ))
            
            # 过期任务
            overdue_count = len(list(self.filter_tasks(overdue=True)))
            
            return {
                'total': total_tasks,
                'by_status': status_counts,
                'by_priority': priority_counts,
                'overdue': overdue_count,
                'completion_rate': status_counts.get('completed', 0) / total_tasks * 100,
                'calculation_count': calculation_count
            }
        
        return calculate_stats
    
    # 数据持久化 (使用上下文管理器确保数据安全) =================================
    
    @log_operation("保存任务数据")
    def save_tasks(self):
        """保存任务到文件"""
        with DataStorageContext(self.storage_path) as storage:
            try:
                # 先写入临时文件
                temp_path = storage.temp_path
                data = {
                    'tasks': {
                        task_id: task.to_dict() 
                        for task_id, task in self.tasks.items()
                    },
                    'metadata': {
                        'saved_at': datetime.now().isoformat(),
                        'version': '1.0',
                        'task_count': len(self.tasks)
                    }
                }
                
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                # 原子性替换
                import shutil
                shutil.move(temp_path, self.storage_path)
                
                logging.info(f"任务数据已保存: {len(self.tasks)} 个任务")
                
            except Exception as e:
                logging.error(f"保存任务失败: {e}")
                raise
    
    @log_operation("加载任务数据")
    def load_tasks(self):
        """从文件加载任务"""
        if not os.path.exists(self.storage_path):
            logging.info("数据文件不存在，从空状态开始")
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 加载任务
            tasks_data = data.get('tasks', {})
            self.tasks = {}
            
            for task_id, task_data in tasks_data.items():
                try:
                    task = Task.from_dict(task_data)
                    self.tasks[task_id] = task
                except Exception as e:
                    logging.warning(f"跳过无效任务 {task_id}: {e}")
            
            # 加载元数据
            metadata = data.get('metadata', {})
            logging.info(f"加载任务数据: {len(self.tasks)} 个任务")
            logging.info(f"数据版本: {metadata.get('version', 'unknown')}")
            
        except Exception as e:
            logging.error(f"加载任务失败: {e}")
            # 不抛出异常，使用空状态
    
    # 批量操作 ================================================================
    
    def batch_create_tasks(self, tasks_data: List[dict]) -> List[Task]:
        """批量创建任务"""
        created_tasks = []
        
        with task_batch_operation(self) as manager:
            for i, task_data in enumerate(tasks_data):
                try:
                    task = manager.create_task(**task_data)
                    created_tasks.append(task)
                except Exception as e:
                    logging.warning(f"批量创建第 {i+1} 个任务失败: {e}")
        
        return created_tasks
    
    def batch_update_status(self, task_ids: List[str], 
                           new_status: TaskStatus) -> int:
        """批量更新任务状态"""
        updated_count = 0
        
        with task_batch_operation(self) as manager:
            for task_id in task_ids:
                try:
                    manager.update_task(task_id, status=new_status)
                    updated_count += 1
                except Exception as e:
                    logging.warning(f"更新任务 {task_id} 状态失败: {e}")
        
        return updated_count

# =============================================================================
# 5. 命令行界面 (用户交互)
# =============================================================================

class TaskManagerCLI:
    """命令行界面"""
    
    def __init__(self):
        self.manager = TaskManager()
        self.stats_calculator = self.manager.create_stats_calculator()
    
    def display_help(self):
        """显示帮助信息"""
        help_text = """
任务管理器命令:
  create    - 创建新任务
  list      - 列出所有任务
  show      - 显示任务详情
  update    - 更新任务
  delete    - 删除任务
  complete  - 标记任务完成
  search    - 搜索任务
  stats     - 显示统计信息
  help      - 显示帮助
  quit      - 退出程序
        """
        print(help_text)
    
    def display_task(self, task: Task):
        """显示单个任务信息"""
        status_emoji = {
            TaskStatus.PENDING: "⏳",
            TaskStatus.IN_PROGRESS: "🔄",
            TaskStatus.COMPLETED: "✅",
            TaskStatus.CANCELLED: "❌"
        }
        
        priority_emoji = {
            Priority.LOW: "🟢",
            Priority.MEDIUM: "🟡",
            Priority.HIGH: "🟠",
            Priority.URGENT: "🔴"
        }
        
        print(f"\n{status_emoji[task.status]} [{task.id}] {task.title}")
        print(f"   {priority_emoji[task.priority]} 优先级: {task.priority.name}")
        print(f"   📝 描述: {task.description or '无'}")
        print(f"   🏷️  标签: {', '.join(task.tags) if task.tags else '无'}")
        print(f"   📅 创建: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        if task.due_date:
            due_str = task.due_date.strftime('%Y-%m-%d %H:%M')
            if task.is_overdue():
                print(f"   ⚠️  截止: {due_str} (已过期)")
            else:
                print(f"   📆 截止: {due_str}")
    
    def run(self):
        """运行命令行界面"""
        print("=== 任务管理器 ===")
        print("输入 'help' 查看可用命令")
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == 'quit' or command == 'exit':
                    print("再见！")
                    break
                elif command == 'help':
                    self.display_help()
                elif command == 'create':
                    self.handle_create()
                elif command == 'list':
                    self.handle_list()
                elif command == 'stats':
                    self.handle_stats()
                elif command.startswith('show'):
                    self.handle_show(command)
                elif command.startswith('search'):
                    self.handle_search(command)
                else:
                    print("未知命令，输入 'help' 查看帮助")
                    
            except KeyboardInterrupt:
                print("\n程序被中断")
                break
            except Exception as e:
                print(f"错误: {e}")
    
    def handle_create(self):
        """处理创建任务命令"""
        title = input("任务标题: ").strip()
        if not title:
            print("标题不能为空")
            return
        
        description = input("任务描述 (可选): ").strip()
        
        print("优先级选择: 1-低, 2-中, 3-高, 4-紧急")
        priority_input = input("优先级 [2]: ").strip() or "2"
        priority_map = {
            "1": Priority.LOW,
            "2": Priority.MEDIUM, 
            "3": Priority.HIGH,
            "4": Priority.URGENT
        }
        priority = priority_map.get(priority_input, Priority.MEDIUM)
        
        task = self.manager.create_task(
            title=title,
            description=description,
            priority=priority
        )
        
        print(f"✅ 任务创建成功: {task.id}")
        self.display_task(task)
    
    def handle_list(self):
        """处理列表命令"""
        tasks = self.manager.get_all_tasks()
        if not tasks:
            print("暂无任务")
            return
        
        # 按优先级和创建时间排序
        sorted_tasks = sorted(
            tasks, 
            key=lambda t: (t.priority.value, t.created_at),
            reverse=True
        )
        
        print(f"\n共 {len(tasks)} 个任务:")
        for task in sorted_tasks:
            self.display_task(task)
    
    def handle_stats(self):
        """处理统计命令"""
        stats = self.stats_calculator()
        
        print(f"\n📊 任务统计:")
        print(f"总任务数: {stats['total']}")
        print(f"完成率: {stats['completion_rate']:.1f}%")
        print(f"过期任务: {stats['overdue']}")
        
        print(f"\n按状态分布:")
        for status, count in stats['by_status'].items():
            print(f"  {status}: {count}")
        
        print(f"\n按优先级分布:")
        for priority, count in stats['by_priority'].items():
            print(f"  {priority}: {count}")
        
        print(f"\n统计次数: {stats['calculation_count']}")
    
    def handle_show(self, command):
        """处理显示任务详情命令"""
        parts = command.split()
        if len(parts) < 2:
            print("请提供任务ID: show <task_id>")
            return
        
        task_id = parts[1]
        try:
            task = self.manager.get_task(task_id)
            self.display_task(task)
        except ValueError as e:
            print(f"错误: {e}")
    
    def handle_search(self, command):
        """处理搜索命令"""
        parts = command.split(maxsplit=1)
        if len(parts) < 2:
            print("请提供搜索关键词: search <keyword>")
            return
        
        query = parts[1]
        results = list(self.manager.search_tasks(query))
        
        if not results:
            print(f"未找到包含 '{query}' 的任务")
            return
        
        print(f"\n搜索结果 ('{query}'):")
        for task in results:
            self.display_task(task)

# =============================================================================
# 6. 主程序入口和测试数据
# =============================================================================

def create_sample_data(manager: TaskManager):
    """创建示例数据"""
    sample_tasks = [
        {
            "title": "学习Python高级特性",
            "description": "深入学习装饰器、生成器、闭包等",
            "priority": Priority.HIGH,
            "tags": ["学习", "Python"]
        },
        {
            "title": "完成项目文档",
            "description": "编写API文档和用户手册",
            "priority": Priority.MEDIUM,
            "tags": ["文档", "项目"]
        },
        {
            "title": "代码审查",
            "description": "审查团队成员提交的代码",
            "priority": Priority.HIGH,
            "tags": ["代码审查", "团队"]
        },
        {
            "title": "备份数据库",
            "description": "定期备份生产环境数据库",
            "priority": Priority.URGENT,
            "tags": ["运维", "数据库"]
        }
    ]
    
    return manager.batch_create_tasks(sample_tasks)

def main():
    """主程序"""
    print("正在初始化任务管理器...")
    
    # 检查是否需要创建示例数据
    manager = TaskManager()
    if not manager.get_all_tasks():
        print("创建示例数据...")
        create_sample_data(manager)
        print("示例数据创建完成")
    
    # 启动命令行界面
    cli = TaskManagerCLI()
    cli.run()

if __name__ == "__main__":
    main()