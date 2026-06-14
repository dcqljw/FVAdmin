import importlib
from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.db import register_mysql
from core.exceptions import CustomException, custom_exception_handler
from core.middleware import LoggingMiddleware
from shared.log_config import setup_logging, app_logger
from shared.redis_client import redis_cache
from init_core import init_data

# 业务模块路由：显式列出，启动时不做文件系统扫描
ROUTER_MODULES = (
    "modules.auth.router",
    "modules.system.router",
    "modules.log.router",
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    app_logger.info("应用启动")

    await redis_cache.connect()  # 初始化 Redis
    if not redis_cache.is_enabled():
        raise RuntimeError("Redis 连接失败，程序无法启动")
    async with register_mysql(_app):
        await init_data()
        yield
    await redis_cache.close()    # 关闭 Redis

    app_logger.info("应用关闭")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan, root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 中间件通过依赖注入解耦：在 main.py（组合根）注入 log_handler
from modules.log.service import operation_log_service
app.add_middleware(LoggingMiddleware, log_handler=operation_log_service.create_log)

app.add_exception_handler(CustomException, custom_exception_handler)

# 注册业务模块路由
for module_path in ROUTER_MODULES:
    app.include_router(importlib.import_module(module_path).router)

if __name__ == "__main__":
    uvicorn.run(app)
