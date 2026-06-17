from typing import Optional, Tuple, List

from tortoise.expressions import Q

from shared.base_repository import BaseRepository
from modules.log.models import OperationLog


class OperationLogRepository(BaseRepository[OperationLog]):
    model_class = OperationLog

    async def list_paginated(
        self,
        current: int = 1,
        size: int = 10,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        module: Optional[str] = None,
        operation: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Tuple[List[OperationLog], int]:
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
        return list(logs), total


operation_log_repo = OperationLogRepository(OperationLog)
