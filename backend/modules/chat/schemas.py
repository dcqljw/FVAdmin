from typing import Optional

from shared.base_schema import BaseSchema


# ========== Chat Session Schemas ==========

class ChatSessionCreateSchema(BaseSchema):
    title: Optional[str] = None


class ChatSessionRenameSchema(BaseSchema):
    id: int
    title: str


# ========== Chat Message Schemas ==========

class ChatMessageSendSchema(BaseSchema):
    session_id: int
    content: str