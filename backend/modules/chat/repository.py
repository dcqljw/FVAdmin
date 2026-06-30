from typing import Optional, List, Tuple

from shared.base_repository import BaseRepository
from modules.chat.models import ChatSession, ChatMessage


# ========== Chat Session Repository ==========

class ChatSessionRepository(BaseRepository[ChatSession]):
    model_class = ChatSession

    async def list_user_sessions(
            self, user_id: int, current: int = 1, size: int = 10,
    ) -> Tuple[List[ChatSession], int]:
        query = ChatSession.filter(user_id=user_id).order_by("-updated_at")
        total = await query.count()
        items = await query.offset((current - 1) * size).limit(size).all()
        return list(items), total

    async def get_user_session(self, session_id: int, user_id: int) -> Optional[ChatSession]:
        return await ChatSession.get_or_none(id=session_id, user_id=user_id)


# ========== Chat Message Repository ==========

class ChatMessageRepository(BaseRepository[ChatMessage]):
    model_class = ChatMessage

    async def get_session_messages(
            self, session_id: int, current: int = 1, size: int = 50,
    ) -> Tuple[List[ChatMessage], int]:
        query = ChatMessage.filter(session_id=session_id).order_by("created_at")
        total = await query.count()
        items = await query.offset((current - 1) * size).limit(size).all()
        return list(items), total

    async def get_recent_messages(
            self, session_id: int, limit: int = 20,
    ) -> List[ChatMessage]:
        """获取最近 N 条消息（按时间正序，用于构建 LLM 上下文）"""
        messages = await ChatMessage.filter(session_id=session_id).order_by("-created_at").limit(limit).all()
        return list(reversed(messages))

    async def get_first_user_message(self, session_id: int) -> Optional[ChatMessage]:
        """获取会话中第一条用户消息（用于自动生成标题）"""
        return await ChatMessage.filter(session_id=session_id, role="user").order_by("created_at").first()


# 单例
chat_session_repo = ChatSessionRepository(ChatSession)
chat_message_repo = ChatMessageRepository(ChatMessage)