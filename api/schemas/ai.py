from pydantic import BaseModel


class ApiKeyCreateSchema(BaseModel):
    baseUrl: str
    name: str
    apiKey: str
