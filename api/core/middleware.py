import time
import json
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from core.log_config import api_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件
    记录所有API请求的详细信息
    """
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求信息
        request_method = request.method
        request_url = str(request.url)
        request_headers = dict(request.headers)
        request_client = request.client.host if request.client else "unknown"
        
        # 获取请求体内容（只记录GET和POST请求的部分内容以避免大体积数据）
        request_body = None
        if request_method in ["POST", "PUT", "PATCH"]:
            try:
                body_bytes = await request.body()
                if body_bytes:
                    # 避免读取过大的请求体
                    if len(body_bytes) <= 10240:  # 10KB 限制
                        request_body = body_bytes.decode('utf-8')
                    else:
                        request_body = f"[请求体过大，长度: {len(body_bytes)} 字节]"
            except Exception as e:
                request_body = f"[读取请求体失败: {str(e)}]"
        
        # 记录请求日志
        api_logger.info(
            f"API请求开始 - "
            f"方法: {request_method}, "
            f"路径: {request_url}, "
            f"客户端: {request_client}, "
            f"请求头: {json.dumps({k:v for k,v in request_headers.items() if k in ['user-agent', 'authorization', 'content-type']}, ensure_ascii=False)}"
        )
        
        if request_body:
            api_logger.info(f"API请求体 - {request_body}")
        
        # 处理请求
        try:
            response = await call_next(request)
            
            # 记录响应信息
            process_time = time.time() - start_time
            response_status = response.status_code
            
            # 尝试获取响应体（注意：这可能不会总是有效，取决于响应的性质）
            response_size = getattr(response, 'content_length', 0) or len(getattr(response, '_body', b''))
            
            api_logger.info(
                f"API请求结束 - "
                f"状态码: {response_status}, "
                f"处理时间: {process_time:.3f}s, "
                f"响应大小: {response_size} bytes"
            )
            
            return response
            
        except Exception as e:
            # 记录异常信息
            process_time = time.time() - start_time
            api_logger.error(
                f"API请求异常 - "
                f"错误: {str(e)}, "
                f"处理时间: {process_time:.3f}s"
            )
            raise e