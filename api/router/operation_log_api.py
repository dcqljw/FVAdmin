from fastapi import APIRouter, Depends

from models.user_model import User
from router.deps import get_current_user, permission_check
from schemas.operation_log import OperationLogListSchema
from schemas.response import SuccessResponse
from services.operation_log_service import operation_log_service

router = APIRouter(prefix="/operation-log", tags=["操作日志管理"])


@router.get("/list")
async def get_operation_log_list(
    current: int = 1,
    size: int = 10,
    user_id: str = None,
    username: str = None,
    module: str = None,
    operation: str = None,
    start_time: str = None,
    end_time: str = None,
    current_user: User = Depends(get_current_user),
):
    logs, total = await operation_log_service.list_logs(
        current=current,
        size=size,
        user_id=user_id,
        username=username,
        module=module,
        operation=operation,
        start_time=start_time,
        end_time=end_time,
    )
    return SuccessResponse(data={"records": logs, "total": total})
