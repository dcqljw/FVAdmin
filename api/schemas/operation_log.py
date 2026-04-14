from pydantic import BaseModel


class OperationLogListSchema(BaseModel):
    current: int = 1
    size: int = 10
    user_id: str = None
    username: str = None
    module: str = None
    operation: str = None
    start_time: str = None
    end_time: str = None
