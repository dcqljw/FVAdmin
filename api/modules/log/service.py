from typing import Tuple, List

from modules.log.models import OperationLog, OperationLogResponse
from modules.log.repository import operation_log_repo


class OperationLogService:
    """操作日志服务"""

    @staticmethod
    async def create_log(
            user_id: str = None,
            username: str = None,
            module: str = "",
            operation: str = "",
            method: str = "",
            path: str = "",
            query_params: str = None,
            request_body: str = None,
            ip: str = "",
            status_code: int = 0,
            response_body: str = None,
            cost_time: float = 0.0,
    ):
        await operation_log_repo.create(
            user_id=user_id,
            username=username,
            module=module,
            operation=operation,
            method=method,
            path=path,
            query_params=query_params,
            request_body=request_body,
            ip=ip,
            status_code=status_code,
            response_body=response_body,
            cost_time=cost_time,
        )

    @staticmethod
    async def list_logs(
            current: int = 1,
            size: int = 10,
            user_id: str = None,
            username: str = None,
            module: str = None,
            operation: str = None,
            start_time: str = None,
            end_time: str = None,
    ) -> Tuple[List[dict], int]:
        logs, total = await operation_log_repo.list_paginated(
            current=current,
            size=size,
            user_id=user_id,
            username=username,
            module=module,
            operation=operation,
            start_time=start_time,
            end_time=end_time,
        )

        records = [OperationLogResponse.model_validate(log) for log in logs]
        return records, total


operation_log_service = OperationLogService()
