from fastapi import APIRouter, Security

from core.deps import permission_check
from shared.base_schema import SuccessResponse
from modules.system.models import User
from modules.log.service import operation_log_service

router = APIRouter(prefix="/system/operation-log", tags=["操作日志管理"])


@router.get("")
async def get_operation_log_list(
    current: int = 1,
    size: int = 10,
    user_id: str = None,
    username: str = None,
    module: str = None,
    operation: str = None,
    start_time: str = None,
    end_time: str = None,
    current_user: User = Security(permission_check),
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
