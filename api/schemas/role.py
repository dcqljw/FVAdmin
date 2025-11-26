from pydantic import BaseModel


class RoleCreateSchema(BaseModel):
    name: str
    description: str
    status: int


class RoleMenuCreateSchema(BaseModel):
    role_id: int
    menu_id: list[int]
