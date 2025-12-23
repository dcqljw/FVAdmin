from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from custom_exception import custom_exception_handler, CustomException
from databases import register_mysql
from init_core import init_data
from core.settings import settings
from router import auth_api, system_api, user_api, menu_api, role_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with register_mysql(app):
        pass
    # await init_data()
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan, root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(CustomException, custom_exception_handler)

app.include_router(auth_api.router)
app.include_router(system_api.router)
app.include_router(user_api.router)
app.include_router(menu_api.router)
app.include_router(role_api.router)

if __name__ == "__main__":
    uvicorn.run(app)
