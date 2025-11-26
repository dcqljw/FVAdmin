from fastapi import APIRouter

from schemas.role import RoleCreateSchema
from models.role_model import Role

router = APIRouter(prefix="/system", tags=["系统管理"])
