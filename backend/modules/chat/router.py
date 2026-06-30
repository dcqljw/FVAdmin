from fastapi import APIRouter, Security
from fastapi.responses import StreamingResponse

from core.deps import permission_check
from shared.base_schema import SuccessResponse
from modules.system.models import User
from modules.chat.schemas import (
    ChatSessionCreateSchema, ChatSessionRenameSchema,
    ChatMessageSendSchema,
)
from modules.chat.service import chat_session_service, chat_service


# ========== 会话管理 ==========

session_router = APIRouter(prefix="/session", tags=["会话管理"])


@session_router.get("")
async def get_session_list(
        current: int = 1,
        size: int = 10,
        current_user: User = Security(permission_check, scopes=["chat:session:list"]),
):
    records, total = await chat_session_service.list_sessions(
        user_id=current_user.id, current=current, size=size,
    )
    return SuccessResponse(data={"records": records, "total": total})


@session_router.post("/add")
async def add_session(
        body: ChatSessionCreateSchema,
        current_user: User = Security(permission_check, scopes=["chat:session:create"]),
):
    session = await chat_session_service.create_session(
        user_id=current_user.id, title=body.title,
    )
    return SuccessResponse(data={"id": session.id, "message": "创建成功"})


@session_router.post("/delete")
async def delete_session(
        session_id: int,
        current_user: User = Security(permission_check, scopes=["chat:session:delete"]),
):
    await chat_session_service.delete_session(session_id, current_user.id)
    return SuccessResponse(data={"message": "删除成功"})


@session_router.post("/rename")
async def rename_session(
        body: ChatSessionRenameSchema,
        current_user: User = Security(permission_check, scopes=["chat:session:create"]),
):
    await chat_session_service.rename_session(body.id, current_user.id, body.title)
    return SuccessResponse(data={"message": "重命名成功"})


# ========== 消息 ==========

message_router = APIRouter(prefix="/message", tags=["聊天消息"])


@message_router.get("")
async def get_message_list(
        session_id: int,
        current: int = 1,
        size: int = 50,
        current_user: User = Security(permission_check, scopes=["chat:message:list"]),
):
    records, total = await chat_service.get_message_history(
        session_id=session_id, user_id=current_user.id,
        current=current, size=size,
    )
    return SuccessResponse(data={"records": records, "total": total})


@message_router.post("/send")
async def send_message(
        body: ChatMessageSendSchema,
        current_user: User = Security(permission_check, scopes=["chat:message:send"]),
):
    # 流式响应前预校验，异常可正常返回 JSON 错误
    await chat_service.validate_send(body.session_id, current_user.id)
    return StreamingResponse(
        chat_service.send_message(
            session_id=body.session_id,
            user_id=current_user.id,
            content=body.content,
        ),
        media_type="text/event-stream",
    )


# ========== 父路由 ==========

router = APIRouter(prefix="/chat")
router.include_router(session_router)
router.include_router(message_router)
