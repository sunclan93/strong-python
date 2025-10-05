"""
设计模式组合应用：HTTP请求处理系统
整合：责任链模式 + 策略模式 + 观察者模式
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Callable
from datetime import datetime
import json

# ========== 1. 责任链模式：请求处理链 ==========

class Request:
    """HTTP请求对象"""
    def __init__(self, method: str, path: str, headers: Dict = None, body: str = ""):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body
        self.user = None  # 认证后设置
        self.validated = False


class Response:
    """HTTP响应对象"""
    def __init__(self, status: int = 200, body: str = "", headers: Dict = None):
        self.status = status
        self.body = body
        self.headers = headers or {}


class Handler(ABC):
    """处理器抽象基类（责任链）"""
    
    def __init__(self):
        self._next: Optional[Handler] = None
    
    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next = handler
        return handler
    
    def handle(self, request: Request) -> Optional[Response]:
        result = self._process(request)
        if result:
            return result
        
        if self._next:
            return self._next.handle(request)
        return None
    
    @abstractmethod
    def _process(self, request: Request) -> Optional[Response]:
        pass


class AuthHandler(Handler):
    """认证处理器"""
    
    def _process(self, request: Request) -> Optional[Response]:
        token = request.headers.get('Authorization')
        
        if not token:
            print("  ❌ [认证] 缺少认证令牌")
            return Response(401, "Unauthorized")
        
        if token != "Bearer valid_token":
            print("  ❌ [认证] 无效的令牌")
            return Response(403, "Forbidden")
        
        request.user = "authenticated_user"
        print("  ✅ [认证] 用户已认证")
        return None  # 继续传递


class ValidationHandler(Handler):
    """请求验证处理器"""
    
    def _process(self, request: Request) -> Optional[Response]:
        if request.method == "POST" and not request.body:
            print("  ❌ [验证] POST请求缺少请求体")
            return Response(400, "Bad Request: Missing body")
        
        request.validated = True
        print("  ✅ [验证] 请求格式有效")
        return None


class RateLimitHandler(Handler):
    """限流处理器"""
    
    def __init__(self, max_requests: int = 10):
        super().__init__()
        self.max_requests = max_requests
        self.request_count = 0
    
    def _process(self, request: Request) -> Optional[Response]:
        self.request_count += 1
        
        if self.request_count > self.max_requests:
            print(f"  ⚠️ [限流] 超过限制 ({self.request_count}/{self.max_requests})")
            return Response(429, "Too Many Requests")
        
        print(f"  ✅ [限流] 请求通过 ({self.request_count}/{self.max_requests})")
        return None


# ========== 2. 策略模式：响应格式化 ==========

class ResponseFormatter(ABC):
    """响应格式化策略"""
    
    @abstractmethod
    def format(self, data: Dict) -> str:
        pass


class JSONFormatter(ResponseFormatter):
    """JSON格式化"""
    
    def format(self, data: Dict) -> str:
        return json.dumps(data, ensure_ascii=False)


class XMLFormatter(ResponseFormatter):
    """XML格式化"""
    
    def format(self, data: Dict) -> str:
        xml = '<?xml version="1.0"?>\n<response>\n'
        for key, value in data.items():
            xml += f'  <{key}>{value}</{key}>\n'
        xml += '</response>'
        return xml


class PlainTextFormatter(ResponseFormatter):
    """纯文本格式化"""
    
    def format(self, data: Dict) -> str:
        return '\n'.join(f"{k}: {v}" for k, v in data.items())


# ========== 3. 观察者模式：请求日志 ==========

class RequestObserver(ABC):
    """请求观察者"""
    
    @abstractmethod
    def on_request(self, request: Request, response: Response):
        pass


class AccessLogger(RequestObserver):
    """访问日志"""
    
    def on_request(self, request: Request, response: Response):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"  📝 [日志] {timestamp} | {request.method} {request.path} | {response.status}")


class MetricsCollector(RequestObserver):
    """指标收集器"""
    
    def __init__(self):
        self.request_count = 0
        self.status_counts = {}
    
    def on_request(self, request: Request, response: Response):
        self.request_count += 1
        status = response.status
        self.status_counts[status] = self.status_counts.get(status, 0) + 1
        print(f"  📊 [指标] 总请求: {self.request_count}, 状态分布: {self.status_counts}")


# ========== 4. 整合：HTTP服务器 ==========

class HTTPServer:
    """HTTP服务器（整合所有模式）"""
    
    def __init__(self):
        # 责任链
        self.handler_chain = self._build_handler_chain()
        
        # 策略
        self.formatter: ResponseFormatter = JSONFormatter()
        
        # 观察者
        self.observers: List[RequestObserver] = []
    
    def _build_handler_chain(self) -> Handler:
        """构建处理链"""
        auth = AuthHandler()
        validation = ValidationHandler()
        rate_limit = RateLimitHandler(max_requests=5)
        
        auth.set_next(validation).set_next(rate_limit)
        return auth
    
    def add_observer(self, observer: RequestObserver):
        """添加观察者"""
        self.observers.append(observer)
    
    def set_formatter(self, formatter: ResponseFormatter):
        """设置响应格式化策略"""
        self.formatter = formatter
    
    def handle_request(self, request: Request) -> Response:
        """处理请求"""
        print(f"\n🌐 处理请求: {request.method} {request.path}")
        
        # 通过责任链处理
        response = self.handler_chain.handle(request)
        
        # 如果链中没有返回响应，生成成功响应
        if not response:
            data = {
                "status": "success",
                "user": request.user,
                "path": request.path,
                "timestamp": datetime.now().isoformat()
            }
            body = self.formatter.format(data)
            response = Response(200, body)
            print("  ✅ [响应] 请求处理成功")
        
        # 通知观察者
        for observer in self.observers:
            observer.on_request(request, response)
        
        return response


# ========== 5. 测试代码 ==========

def main():
    print("="*70)
    print("设计模式组合应用：HTTP请求处理系统")
    print("="*70)
    
    # 创建服务器
    server = HTTPServer()
    
    # 添加观察者
    server.add_observer(AccessLogger())
    server.add_observer(MetricsCollector())
    
    # 测试1: 成功的请求
    print("\n【测试1：正常请求 - JSON格式】")
    request1 = Request(
        "GET", 
        "/api/users",
        headers={"Authorization": "Bearer valid_token"}
    )
    response1 = server.handle_request(request1)
    print(f"响应: {response1.status}\n{response1.body}")
    
    # 测试2: 切换为XML格式
    print("\n" + "="*70)
    print("【测试2：切换为XML格式】")
    server.set_formatter(XMLFormatter())
    request2 = Request(
        "GET",
        "/api/products",
        headers={"Authorization": "Bearer valid_token"}
    )
    response2 = server.handle_request(request2)
    print(f"响应: {response2.status}\n{response2.body}")
    
    # 测试3: 认证失败
    print("\n" + "="*70)
    print("【测试3：认证失败】")
    request3 = Request("GET", "/api/admin")
    response3 = server.handle_request(request3)
    print(f"响应: {response3.status}")
    
    # 测试4: 触发限流
    print("\n" + "="*70)
    print("【测试4：触发限流】")
    for i in range(6):
        request = Request(
            "GET",
            f"/api/test{i}",
            headers={"Authorization": "Bearer valid_token"}
        )
        response = server.handle_request(request)


if __name__ == "__main__":
    main()