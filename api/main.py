from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import RegisterTortoise

from core.settings import settings
from router import auth_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(
            app,
            db_url=settings.DATABASE_URL,
            modules={"models": ["models"]},
            generate_schemas=True,
            add_exception_handlers=True,
    ):
        yield


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_api.router)


@app.get("/menu")
async def get_menu():
    return [
        {
            "name": "dashboard",
            "path": "dashboard",
            "menu": "/dashboard",
            "meta": {
                "title": "控制台",
                "icon": "mynaui:chart-pie-two"
            },
            "component": "dashboard/DashboardView"
        }, {
            "name": "system",
            "path": "system",
            "menu": "/system",
            "meta": {
                "title": "系统管理",
                "icon": "mynaui:cog"
            },
            "children": [
                {
                    "name": "user",
                    "path": "user",
                    "menu": "/system/user",
                    "meta": {
                        "title": "用户管理",
                        "icon": "mynaui:user-circle"
                    },
                    "component": "system/UserView"
                },
                {
                    "name": "role",
                    "path": "role",
                    "menu": "/system/role",
                    "meta": {
                        "title": "角色管理",
                        "icon": "mynaui:users-group"
                    },
                    "component": "system/RoleView"
                }
            ]
        }
    ]


if __name__ == "__main__":
    uvicorn.run(app)
