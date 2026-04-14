import time
import json
import asyncio
from typing import Callable, Awaitable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, Response

from core.log_config import api_logger
from core.security import verify_token
from services.operation_log_service import operation_log_service

# 不需要记录的路径模式（列表查询接口等）
SKIP_PATHS = [
    "/user/list",
    "/role/list",
    "/menu/list",
    "/operation-log/list",
    "/user/info",
]

# 路由前缀到模块名的映射
MODULE_MAP = {
    "/user": "用户管理",
    "/role": "角色管理",
    "/menu": "菜单管理",
    "/auth": "认证管理",
    "/system": "系统管理",
    "/operation-log": "操作日志管理",
}


def _get_module_name(path: str) -> str:
    """从请求路径提取模块名"""
    for prefix, name in MODULE_MAP.items():
        if path.startswith(prefix):
            return name
    return "其他"


def _get_operation_type(method: str, path: str) -> str:
    """从请求方法和路径判断操作类型"""
    if method in ("GET", "OPTIONS"):
        return "查询"
    if method in ("PUT", "PATCH"):
        return "修改"

    # POST/DELETE 根据路径关键词判断
    path_lower = path.lower()
    if "delete" in path_lower or "/del/" in path_lower or path_lower.endswith("/del"):
        return "删除"
    if "edit" in path_lower or "update" in path_lower or "reset" in path_lower:
        return "修改"
    if "add" in path_lower or "create" in path_lower or "upload" in path_lower:
        return "新增"
    if "login" in path_lower:
        return "登录"

    return "其他"


async def _read_body(body_bytes: bytes) -> str:
    """读取并截断请求体"""
    if not body_bytes:
        return None
    if len(body_bytes) > 10240:  # 10KB
        return "[请求体过大，已截断]"
    try:
        return body_bytes.decode("utf-8")
    except Exception:
        return "[请求体解码失败]"


async def _read_response_body(response: Response) -> str:
    """读取响应体并限制大小"""
    if isinstance(response, StreamingResponse):
        body_parts = []
        total_size = 0
        async for chunk in response.body_iterator:
            body_parts.append(chunk)
            total_size += len(chunk)
            if total_size > 10240:
                break
        body = b"".join(body_parts)
        response.body_iterator = _body_iterator(body_parts)
        if total_size > 10240:
            return "[响应体过大，已截断]"
        try:
            return body.decode("utf-8")
        except Exception:
            return "[响应体解码失败]"
    return None


async def _body_iterator(data):
    for chunk in data:
        yield chunk


def _extract_user_from_request(request: Request) -> tuple:
    """从请求头中解析用户信息"""
    auth_header = request.headers.get("authorization", "")

    token = auth_header
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]

    if not token:
        return None, None

    payload = verify_token(token)
    if not payload:
        return None, None

    user_id = payload.get("uid")
    username = payload.get("username")
    return str(user_id) if user_id else None, username


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    请求日志中间件
    记录所有API请求的详细信息（文件日志 + 数据库日志）
    """

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.time()

        request_method = request.method
        request_url_path = str(request.url.path)
        request_client = request.client.host if request.client else "unknown"

        query_params = dict(request.query_params) if request.query_params else None

        request_body = None
        if request_method in ["POST", "PUT", "PATCH"]:
            body_bytes = await request.body()
            request_body = await _read_body(body_bytes)

        api_logger.info(
            f"API请求开始 - "
            f"方法: {request_method}, "
            f"路径: {request_url_path}, "
            f"客户端: {request_client}"
        )

        if request_body:
            if "login" in request_url_path:
                request_body_json = json.loads(request_body)
                request_body_json['password'] = "*****"
                request_body = json.dumps(request_body_json)
            api_logger.info(f"API请求体 - {request_body}")

        response_status = 0
        response_body_str = None

        try:
            response = await call_next(request)
            response_status = response.status_code

            response_body_str = await _read_response_body(response)

            response_size = getattr(response, "content_length", 0) or len(getattr(response, "_body", b""))

            api_logger.info(
                f"API请求结束 - "
                f"状态码: {response_status}, "
                f"处理时间: {time.time() - start_time:.3f}s, "
                f"响应大小: {response_size} bytes"
            )

            return response

        except Exception as e:
            process_time = time.time() - start_time
            response_status = 500
            api_logger.error(
                f"API请求异常 - "
                f"错误: {str(e)}, "
                f"处理时间: {process_time:.3f}s"
            )
            raise e

        finally:
            # 去掉 /api 前缀
            if request_url_path.startswith("/api"):
                request_url_path = request_url_path[len("/api"):]

            # 跳过不需要记录的路径
            if request_url_path not in SKIP_PATHS:
                # 异步写入数据库操作日志（不阻塞主请求）
                try:
                    cost_time = time.time() - start_time
                    user_id, username = _extract_user_from_request(request)
                    module = _get_module_name(request_url_path)
                    operation = _get_operation_type(request_method, request_url_path)

                    asyncio.create_task(
                        operation_log_service.create_log(
                            user_id=user_id,
                            username=username,
                            module=module,
                            operation=operation,
                            method=request_method,
                            path=request_url_path,
                            query_params=json.dumps(query_params, ensure_ascii=False) if query_params else None,
                            request_body=request_body,
                            ip=request_client,
                            status_code=response_status,
                            response_body=response_body_str,
                            cost_time=round(cost_time, 3),
                        )
                    )
                except Exception as e:
                    api_logger.error(f"写入操作日志失败: {str(e)}")
