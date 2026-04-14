from typing import Tuple, List

from tortoise.expressions import Q

from models.operation_log_model import OperationLog, OperationLogResponse


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
        await OperationLog.create(
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
        q = Q()
        if user_id:
            q &= Q(user_id=user_id)
        if username:
            q &= Q(username__icontains=username)
        if module:
            q &= Q(module=module)
        if operation:
            q &= Q(operation=operation)
        if start_time:
            q &= Q(created_at__gte=start_time)
        if end_time:
            q &= Q(created_at__lte=end_time)

        total = await OperationLog.filter(q).count()
        logs = await OperationLog.filter(q).order_by("-created_at").offset((current - 1) * size).limit(size)

        records = []
        for log in logs:
            data = {
                "id": log.id,
                "user_id": log.user_id,
                "username": log.username,
                "module": log.module,
                "operation": log.operation,
                "method": log.method,
                "path": log.path,
                "query_params": log.query_params,
                "request_body": log.request_body,
                "ip": log.ip,
                "status_code": log.status_code,
                "response_body": log.response_body,
                "cost_time": log.cost_time,
                "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else None,
            }
            records.append(OperationLogResponse(**data))
        return records, total


operation_log_service = OperationLogService()
