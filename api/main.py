from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastmcp import FastMCP
from fastapi.middleware.cors import CORSMiddleware

from custom_exception import custom_exception_handler, CustomException
from databases import register_mysql
from init_core import init_data
from core.settings import settings
from core.log_config import setup_logging, app_logger
from core.middleware import LoggingMiddleware
from router import auth_api, system_api, user_api, menu_api, role_api, ai_api


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # 初始化日志系统
    setup_logging()
    app_logger.info("应用启动")

    async with register_mysql(_app):
        await init_data()
        yield

    app_logger.info("应用关闭")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan, root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求日志中间件
app.add_middleware(LoggingMiddleware)

app.add_exception_handler(CustomException, custom_exception_handler)

app.include_router(auth_api.router)
app.include_router(system_api.router)
app.include_router(user_api.router)
app.include_router(menu_api.router)
app.include_router(role_api.router)
app.include_router(ai_api.router)

# mcp = FastMCP.from_fastapi(app=app)
# mcp_app = mcp.http_app("/mcp")
#
# print(app.user_middleware)
# combined_app = FastAPI(
#     routes=[
#         *mcp_app.routes,
#         *app.routes,
#     ],
#     middleware=app.user_middleware,
#     lifespan=mcp_app.lifespan,
# )
# combined_app.add_middleware(LoggingMiddleware)

if __name__ == "__main__":
    uvicorn.run(app)
