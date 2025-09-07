# 多重继承的问题与解决方案

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
import weakref

# =============================================================================
# 1. 多重继承的经典问题
# =============================================================================

class MultipleInheritanceProblems:
    """多重继承问题演示"""
    
    def demonstrate_diamond_problem(self):
        """演示钻石继承问题"""
        print("=== 钻石继承问题 ===")
        
        class Animal:
            def __init__(self, name):
                print(f"Animal.__init__: {name}")
                self.name = name
            
            def speak(self):
                return f"{self.name} makes a sound"
        
        class Mammal(Animal):
            def __init__(self, name, warm_blooded=True):
                print(f"Mammal.__init__: {name}, warm_blooded={warm_blooded}")
                super().__init__(name)
                self.warm_blooded = warm_blooded
            
            def speak(self):
                return f"{self.name} makes mammal sounds"
        
        class Bird(Animal):
            def __init__(self, name, can_fly=True):
                print(f"Bird.__init__: {name}, can_fly={can_fly}")
                super().__init__(name)
                self.can_fly = can_fly
            
            def speak(self):
                return f"{self.name} chirps"
        
        # 问题：Bat 既是哺乳动物又像鸟类
        class Bat(Mammal, Bird):
            def __init__(self, name):
                print(f"Bat.__init__: {name}")
                # 问题：如何正确初始化两个父类？
                try:
                    super().__init__(name, warm_blooded=True)
                    # Bird的初始化会被跳过！
                except Exception as e:
                    print(f"初始化错误: {e}")
        
        print("创建蝙蝠 - 存在问题的版本:")
        try:
            bat = Bat("Batman")
            print(f"蝙蝠创建成功: {bat.name}")
            print(f"是否温血: {getattr(bat, 'warm_blooded', '未设置')}")
            print(f"是否能飞: {getattr(bat, 'can_fly', '未设置')}")
            print(f"MRO: {' -> '.join(c.__name__ for c in Bat.__mro__)}")
        except Exception as e:
            print(f"创建失败: {e}")
    
    def demonstrate_method_ambiguity(self):
        """演示方法歧义问题"""
        print("\n=== 方法歧义问题 ===")
        
        class A:
            def process(self, data):
                return f"A.process: {data}"
        
        class B:
            def process(self, data):
                return f"B.process: {data}"
        
        class C(A, B):
            # 问题：继承了两个同名方法，哪个会被调用？
            pass
        
        c = C()
        result = c.process("test")
        print(f"调用结果: {result}")
        print(f"解释: 根据MRO {' -> '.join(cls.__name__ for cls in C.__mro__)}，调用A.process")
        
        # 如果想调用B的方法怎么办？
        b_result = B.process(c, "test")
        print(f"显式调用B.process: {b_result}")

# =============================================================================
# 2. 解决方案1：使用混入(Mixin)模式
# =============================================================================

class MixinSolution:
    """混入模式解决多重继承问题"""
    
    def demonstrate_mixin_pattern(self):
        """演示混入模式"""
        print("\n=== 混入模式解决方案 ===")
        
        # 基础类
        class Animal:
            def __init__(self, name, **kwargs):
                print(f"Animal.__init__: {name}")
                super().__init__(**kwargs)
                self.name = name
            
            def speak(self):
                return f"{self.name} makes a sound"
        
        # 混入类 - 只提供功能，不定义状态
        class FlyingMixin:
            """飞行能力混入"""
            def fly(self):
                return f"{self.name} flies through the air"
            
            def land(self):
                return f"{self.name} lands gracefully"
        
        class SwimmingMixin:
            """游泳能力混入"""
            def swim(self):
                return f"{self.name} swims in the water"
            
            def dive(self):
                return f"{self.name} dives underwater"
        
        class WarmBloodedMixin:
            """温血动物混入"""
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.warm_blooded = True
            
            def regulate_temperature(self):
                return f"{self.name} maintains body temperature"
        
        # 使用混入组合功能
        class Bird(Animal, FlyingMixin, WarmBloodedMixin):
            def __init__(self, name, **kwargs):
                print(f"Bird.__init__: {name}")
                super().__init__(name=name, **kwargs)
            
            def speak(self):
                return f"{self.name} chirps and sings"
        
        class Duck(Bird, SwimmingMixin):
            def __init__(self, name, **kwargs):
                print(f"Duck.__init__: {name}")
                super().__init__(name=name, **kwargs)
            
            def speak(self):
                return f"{self.name} quacks"
        
        class Penguin(Animal, SwimmingMixin, WarmBloodedMixin):
            def __init__(self, name, **kwargs):
                print(f"Penguin.__init__: {name}")
                super().__init__(name=name, **kwargs)
            
            def speak(self):
                return f"{self.name} makes penguin sounds"
        
        print("创建鸭子:")
        duck = Duck("Donald")
        print(f"发声: {duck.speak()}")
        print(f"飞行: {duck.fly()}")
        print(f"游泳: {duck.swim()}")
        print(f"调节体温: {duck.regulate_temperature()}")
        
        print("\n创建企鹅:")
        penguin = Penguin("Pingu")
        print(f"发声: {penguin.speak()}")
        print(f"游泳: {penguin.swim()}")
        print(f"调节体温: {penguin.regulate_temperature()}")
        # 企鹅不能飞
        print(f"企鹅有飞行能力: {hasattr(penguin, 'fly')}")

# =============================================================================
# 3. 解决方案2：组合优于继承
# =============================================================================

class CompositionSolution:
    """组合模式解决方案"""
    
    def demonstrate_composition_pattern(self):
        """演示组合模式"""
        print("\n=== 组合模式解决方案 ===")
        
        # 定义能力接口
        @runtime_checkable
        class Flyable(Protocol):
            def fly(self) -> str: ...
            def land(self) -> str: ...
        
        @runtime_checkable
        class Swimmable(Protocol):
            def swim(self) -> str: ...
            def dive(self) -> str: ...
        
        # 能力实现类
        class FlyingAbility:
            def __init__(self, owner_name):
                self.owner_name = owner_name
            
            def fly(self):
                return f"{self.owner_name} soars through the sky"
            
            def land(self):
                return f"{self.owner_name} touches down gently"
        
        class SwimmingAbility:
            def __init__(self, owner_name):
                self.owner_name = owner_name
            
            def swim(self):
                return f"{self.owner_name} glides through water"
            
            def dive(self):
                return f"{self.owner_name} plunges deep"
        
        # 使用组合的动物类
        class CompositeAnimal:
            def __init__(self, name, species):
                self.name = name
                self.species = species
                self._abilities = {}
            
            def add_ability(self, ability_name, ability_instance):
                """添加能力"""
                self._abilities[ability_name] = ability_instance
                
                # 动态添加方法
                for method_name in dir(ability_instance):
                    if not method_name.startswith('_'):
                        method = getattr(ability_instance, method_name)
                        if callable(method):
                            setattr(self, method_name, method)
            
            def has_ability(self, ability_type):
                """检查是否具有某种能力"""
                for ability in self._abilities.values():
                    if isinstance(ability, ability_type):
                        return True
                return False
            
            def speak(self):
                return f"{self.name} the {self.species} makes a sound"
            
            def get_abilities(self):
                return list(self._abilities.keys())
        
        print("创建具有飞行和游泳能力的鸭子:")
        duck = CompositeAnimal("Donald", "Duck")
        duck.add_ability("flying", FlyingAbility(duck.name))
        duck.add_ability("swimming", SwimmingAbility(duck.name))
        
        print(f"鸭子能力: {duck.get_abilities()}")
        print(f"发声: {duck.speak()}")
        print(f"飞行: {duck.fly()}")
        print(f"游泳: {duck.swim()}")
        print(f"是否可飞行: {duck.has_ability(FlyingAbility)}")
        
        print("\n创建只有游泳能力的企鹅:")
        penguin = CompositeAnimal("Pingu", "Penguin")
        penguin.add_ability("swimming", SwimmingAbility(penguin.name))
        
        print(f"企鹅能力: {penguin.get_abilities()}")
        print(f"游泳: {penguin.swim()}")
        print(f"是否可飞行: {penguin.has_ability(FlyingAbility)}")

# =============================================================================
# 4. 解决方案3：抽象基类和接口
# =============================================================================

class AbstractBaseSolution:
    """抽象基类解决方案"""
    
    def demonstrate_abc_pattern(self):
        """演示抽象基类模式"""
        print("\n=== 抽象基类解决方案 ===")
        
        # 定义抽象基类
        class Animal(ABC):
            def __init__(self, name, species):
                self.name = name
                self.species = species
            
            @abstractmethod
            def speak(self):
                """动物发声 - 必须实现"""
                pass
            
            @abstractmethod
            def move(self):
                """动物移动 - 必须实现"""
                pass
            
            def info(self):
                """通用信息方法"""
                return f"{self.name} is a {self.species}"
        
        # 定义能力接口
        class Flyable(ABC):
            @abstractmethod
            def fly(self):
                pass
            
            @abstractmethod
            def land(self):
                pass
        
        class Swimmable(ABC):
            @abstractmethod
            def swim(self):
                pass
        
        # 具体实现类
        class Bird(Animal, Flyable):
            def __init__(self, name, wing_span):
                super().__init__(name, "Bird")
                self.wing_span = wing_span
            
            def speak(self):
                return f"{self.name} chirps"
            
            def move(self):
                return self.fly()
            
            def fly(self):
                return f"{self.name} flies with {self.wing_span}cm wingspan"
            
            def land(self):
                return f"{self.name} lands on a branch"
        
        class Fish(Animal, Swimmable):
            def __init__(self, name, water_type="freshwater"):
                super().__init__(name, "Fish")
                self.water_type = water_type
            
            def speak(self):
                return f"{self.name} blows bubbles"
            
            def move(self):
                return self.swim()
            
            def swim(self):
                return f"{self.name} swims in {self.water_type}"
        
        class Duck(Animal, Flyable, Swimmable):
            def __init__(self, name):
                super().__init__(name, "Duck")
            
            def speak(self):
                return f"{self.name} quacks"
            
            def move(self):
                return "Can both fly and swim"
            
            def fly(self):
                return f"{self.name} flies low over water"
            
            def land(self):
                return f"{self.name} lands on water"
            
            def swim(self):
                return f"{self.name} paddles in water"
        
        print("创建各种动物:")
        bird = Bird("Robin", 15)
        fish = Fish("Goldfish")
        duck = Duck("Mallard")
        
        animals = [bird, fish, duck]
        
        for animal in animals:
            print(f"\n{animal.info()}")
            print(f"发声: {animal.speak()}")
            print(f"移动: {animal.move()}")
            
            # 检查特定能力
            if isinstance(animal, Flyable):
                print(f"飞行: {animal.fly()}")
            if isinstance(animal, Swimmable):
                print(f"游泳: {animal.swim()}")

# =============================================================================
# 5. 解决方案4：依赖注入模式
# =============================================================================

class DependencyInjectionSolution:
    """依赖注入解决方案"""
    
    def demonstrate_dependency_injection(self):
        """演示依赖注入模式"""
        print("\n=== 依赖注入解决方案 ===")
        
        # 定义服务接口
        class MovementService(ABC):
            @abstractmethod
            def move(self, entity_name):
                pass
        
        class SoundService(ABC):
            @abstractmethod
            def make_sound(self, entity_name):
                pass
        
        # 服务实现
        class FlyingService(MovementService):
            def move(self, entity_name):
                return f"{entity_name} soars through the air"
        
        class SwimmingService(MovementService):
            def move(self, entity_name):
                return f"{entity_name} glides through water"
        
        class WalkingService(MovementService):
            def move(self, entity_name):
                return f"{entity_name} walks on land"
        
        class BirdSoundService(SoundService):
            def make_sound(self, entity_name):
                return f"{entity_name} chirps melodiously"
        
        class DuckSoundService(SoundService):
            def make_sound(self, entity_name):
                return f"{entity_name} quacks loudly"
        
        # 使用依赖注入的动物类
        class InjectableAnimal:
            def __init__(self, name, species, 
                         movement_service: MovementService,
                         sound_service: SoundService):
                self.name = name
                self.species = species
                self._movement_service = movement_service
                self._sound_service = sound_service
            
            def speak(self):
                return self._sound_service.make_sound(self.name)
            
            def move(self):
                return self._movement_service.move(self.name)
            
            def info(self):
                return f"{self.name} is a {self.species}"
        
        # 创建不同的动物实例
        print("使用依赖注入创建动物:")
        
        bird = InjectableAnimal(
            "Robin", "Bird",
            FlyingService(),
            BirdSoundService()
        )
        
        duck = InjectableAnimal(
            "Donald", "Duck", 
            SwimmingService(),  # 鸭子主要游泳
            DuckSoundService()
        )
        
        animals = [bird, duck]
        
        for animal in animals:
            print(f"\n{animal.info()}")
            print(f"发声: {animal.speak()}")
            print(f"移动: {animal.move()}")

# =============================================================================
# 6. 解决方案5：策略模式
# =============================================================================

class StrategyPatternSolution:
    """策略模式解决方案"""
    
    def demonstrate_strategy_pattern(self):
        """演示策略模式"""
        print("\n=== 策略模式解决方案 ===")
        
        # 策略接口
        class MovementStrategy(ABC):
            @abstractmethod
            def execute(self, entity_name):
                pass
        
        class SoundStrategy(ABC):
            @abstractmethod
            def execute(self, entity_name):
                pass
        
        # 具体策略
        class FlyStrategy(MovementStrategy):
            def execute(self, entity_name):
                return f"{entity_name} flies high in the sky"
        
        class SwimStrategy(MovementStrategy):
            def execute(self, entity_name):
                return f"{entity_name} swims gracefully"
        
        class HybridMovementStrategy(MovementStrategy):
            def __init__(self, strategies):
                self.strategies = strategies
            
            def execute(self, entity_name):
                results = [strategy.execute(entity_name) for strategy in self.strategies]
                return " and ".join(results)
        
        class ChirpStrategy(SoundStrategy):
            def execute(self, entity_name):
                return f"{entity_name} chirps sweetly"
        
        class QuackStrategy(SoundStrategy):
            def execute(self, entity_name):
                return f"{entity_name} quacks"
        
        # 上下文类
        class StrategyAnimal:
            def __init__(self, name, species):
                self.name = name
                self.species = species
                self._movement_strategy = None
                self._sound_strategy = None
            
            def set_movement_strategy(self, strategy: MovementStrategy):
                self._movement_strategy = strategy
            
            def set_sound_strategy(self, strategy: SoundStrategy):
                self._sound_strategy = strategy
            
            def move(self):
                if self._movement_strategy:
                    return self._movement_strategy.execute(self.name)
                return f"{self.name} doesn't know how to move"
            
            def speak(self):
                if self._sound_strategy:
                    return self._sound_strategy.execute(self.name)
                return f"{self.name} is silent"
        
        print("使用策略模式创建动物:")
        
        # 创建鸟
        bird = StrategyAnimal("Eagle", "Bird")
        bird.set_movement_strategy(FlyStrategy())
        bird.set_sound_strategy(ChirpStrategy())
        
        # 创建鸭子（具有多种移动能力）
        duck = StrategyAnimal("Mallard", "Duck")
        duck.set_movement_strategy(
            HybridMovementStrategy([FlyStrategy(), SwimStrategy()])
        )
        duck.set_sound_strategy(QuackStrategy())
        
        animals = [bird, duck]
        
        for animal in animals:
            print(f"\n{animal.name} the {animal.species}:")
            print(f"移动: {animal.move()}")
            print(f"发声: {animal.speak()}")
        
        # 运行时切换策略
        print(f"\n切换鸭子的移动策略为仅游泳:")
        duck.set_movement_strategy(SwimStrategy())
        print(f"新的移动方式: {duck.move()}")

# =============================================================================
# 7. 多重继承最佳实践总结
# =============================================================================

class MultipleInheritanceBestPractices:
    """多重继承最佳实践总结"""
    
    def demonstrate_best_practices(self):
        """演示最佳实践"""
        print("\n=== 多重继承最佳实践 ===")
        
        # 1. 使用混入模式
        class TimestampMixin:
            """时间戳混入 - 只提供功能，不维护状态"""
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                import datetime
                self.created_at = datetime.datetime.now()
            
            def age_in_seconds(self):
                import datetime
                return (datetime.datetime.now() - self.created_at).total_seconds()
        
        class LoggingMixin:
            """日志混入"""
            def log(self, message):
                print(f"[{self.__class__.__name__}] {message}")
        
        # 2. 明确的继承顺序
        class Entity(TimestampMixin, LoggingMixin):
            """实体基类 - 混入在前，基类在后"""
            def __init__(self, name, **kwargs):
                super().__init__(**kwargs)
                self.name = name
                self.log(f"Entity {name} created")
        
        # 3. 协作继承模式
        class ProcessorMixin:
            """处理器混入"""
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self._processed_count = 0
            
            def process(self, data):
                self.log(f"Processing: {data}")
                self._processed_count += 1
                return f"processed_{data}"
            
            def get_process_count(self):
                return self._processed_count
        
        class SmartEntity(Entity, ProcessorMixin):
            """智能实体 - 组合多个混入"""
            def __init__(self, name, **kwargs):
                super().__init__(name=name, **kwargs)
                self.log("SmartEntity initialization complete")
            
            def process(self, data):
                result = super().process(data)
                self.log(f"Processed result: {result}")
                return result
        
        print("创建智能实体:")
        entity = SmartEntity("TestEntity")
        
        print(f"实体年龄: {entity.age_in_seconds():.2f} 秒")
        
        result1 = entity.process("data1")
        result2 = entity.process("data2")
        
        print(f"处理次数: {entity.get_process_count()}")
        
        # 4. 避免钻石继承的正确方式
        print(f"\nMRO检查: {' -> '.join(c.__name__ for c in SmartEntity.__mro__)}")
        
        # 5. 使用类型检查
        print(f"\n类型检查:")
        print(f"是否有时间戳功能: {isinstance(entity, TimestampMixin)}")
        print(f"是否有日志功能: {isinstance(entity, LoggingMixin)}")
        print(f"是否有处理功能: {isinstance(entity, ProcessorMixin)}")

# =============================================================================
# 8. 多重继承设计原则
# =============================================================================

class DesignPrinciples:
    """多重继承设计原则"""
    
    @staticmethod
    def print_design_principles():
        """打印设计原则"""
        print("\n=== 多重继承设计原则 ===")
        
        principles = [
            "1. 优先使用组合而非继承",
            "2. 混入类应该是无状态的",
            "3. 明确继承顺序，混入在前，基类在后",
            "4. 使用抽象基类定义接口",
            "5. 避免深层次的多重继承",
            "6. 所有类都应该调用super().__init__()",
            "7. 使用**kwargs处理参数传递",
            "8. 文档化MRO和依赖关系",
            "9. 优先使用依赖注入",
            "10. 考虑使用策略模式替代继承"
        ]
        
        for principle in principles:
            print(f"  {principle}")
        
        print("\n选择指南:")
        print("  - 简单功能增强 → 混入模式")
        print("  - 复杂行为组合 → 组合模式")
        print("  - 运行时行为切换 → 策略模式")
        print("  - 强制接口实现 → 抽象基类")
        print("  - 松耦合设计 → 依赖注入")

# =============================================================================
# 运行演示
# =============================================================================

if __name__ == "__main__":
    # 问题演示
    problems = MultipleInheritanceProblems()
    problems.demonstrate_diamond_problem()
    problems.demonstrate_method_ambiguity()
    
    # 解决方案1：混入模式
    mixin_solution = MixinSolution()
    mixin_solution.demonstrate_mixin_pattern()
    
    # 解决方案2：组合模式
    composition_solution = CompositionSolution()
    composition_solution.demonstrate_composition_pattern()
    
    # 解决方案3：抽象基类
    abc_solution = AbstractBaseSolution()
    abc_solution.demonstrate_abc_pattern()
    
    # 解决方案4：依赖注入
    di_solution = DependencyInjectionSolution()
    di_solution.demonstrate_dependency_injection()
    
    # 解决方案5：策略模式
    strategy_solution = StrategyPatternSolution()
    strategy_solution.demonstrate_strategy_pattern()
    
    # 最佳实践
    best_practices = MultipleInheritanceBestPractices()
    best_practices.demonstrate_best_practices()
    
    # 设计原则
    DesignPrinciples.print_design_principles()