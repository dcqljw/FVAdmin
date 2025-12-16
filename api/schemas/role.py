from pydantic import BaseModel


class RoleCreateSchema(BaseModel):
    name: str
    code: str
    description: str
    enabled: bool


class RoleMenuCreateSchema(BaseModel):
    role_id: int
    menu_id: list[int]
