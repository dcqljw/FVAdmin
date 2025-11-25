from pydantic import BaseModel


class RoleCreateSchema(BaseModel):
    name: str
    description: str
    status: int
