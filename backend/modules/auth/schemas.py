from shared.base_schema import BaseSchema


class LoginSchema(BaseSchema):
    username: str
    password: str
    captcha_key: str | None = None
    captcha_code: str | None = None
