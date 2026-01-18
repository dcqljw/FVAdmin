from pydantic import BaseModel


class ApiKeyCreateSchema(BaseModel):
    name: str
    key: str
