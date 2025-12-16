from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class UserLoginSchema(UserBase):
    pass


class UserCreateSchema(UserBase):
    nickname: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    role: list[str]


class EditPasswordSchema(BaseModel):
    old_password: str
    new_password: str
