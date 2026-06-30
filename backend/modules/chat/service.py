import json
from datetime import datetime
from typing import List, Tuple, AsyncGenerator

from openai import AsyncOpenAI

from core.exceptions import CustomException
from shared.base_service import BaseService
from shared.log_config import api_logger
from modules.chat.models import ChatSession, ChatMessage
from modules.chat.models import ChatSessionResponse, ChatMessageResponse
from modules.chat.repository import chat_session_repo, chat_message_repo
from modules.model.models import LLMModel
from modules.model.repository import llm_model_repo
from modules.mcp.repository import mcp_server_repo
from modules.mcp import mcp_client

# 上下文窗口：每次请求携带的最近消息数
_CONTEXT_WINDOW = 20

# 自动标题最大长度
_TITLE_MAX_LENGTH = 30

# 默认系统提示词
_SYSTEM_PROMPT = "你是一个有用的 AI 助手。可以使用提供的工具来帮助用户完成任务。"

# 工具调用最大轮次
_MAX_TOOL_ROUNDS = 5


# ========== Chat Session Service ==========

class ChatSessionService(BaseService):

    async def create_session(self, user_id: int, title: str | None = None) -> ChatSession:
        from modules.system.models import User
        user = await User.get(id=user_id)
        session = await chat_session_repo.create(
            user=user,
            title=title or "新对话",
        )
        return session

    async def list_sessions(
            self, user_id: int, current: int = 1, size: int = 10,
    ) -> Tuple[List[dict], int]:
        items, total = await chat_session_repo.list_user_sessions(
            user_id=user_id, current=current, size=size,
        )
        records = [
            ChatSessionResponse.model_validate(s).model_dump(mode="json")
            for s in items
        ]
        return records, total

    async def delete_session(self, session_id: int, user_id: int):
        session = await self.get_user_session_or_raise(session_id, user_id)
        await session.delete()  # CASCADE 自动删消息

    async def rename_session(self, session_id: int, user_id: int, title: str):
        session = await self.get_user_session_or_raise(session_id, user_id)
        session.title = title
        await session.save()

    async def get_user_session_or_raise(self, session_id: int, user_id: int) -> ChatSession:
        """获取用户的会话，不存在则抛异常"""
        session = await chat_session_repo.get_user_session(session_id, user_id)
        if not session:
            raise CustomException(code=400, msg="会话不存在")
        return session


# ========== Chat Service (LLM + MCP 工具调用) ==========

class ChatService(BaseService):

    async def _get_enabled_model(self) -> LLMModel:
        model = await llm_model_repo.get_default()
        if not model:
            raise CustomException(code=400, msg="未配置默认模型，请先在模型管理中添加")
        return model

    async def validate_send(self, session_id: int, user_id: int):
        """流式响应前的预校验"""
        await chat_session_service.get_user_session_or_raise(session_id, user_id)
        await self._get_enabled_model()

    # ---- 系统提示词 ----

    def _get_system_prompt(self) -> str:
        """构建包含当前时间的系统提示词"""
        now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        return f"{_SYSTEM_PROMPT}\n\n当前时间：{now}"

    # ---- MCP 工具相关 ----

    async def _fetch_mcp_tools(self) -> tuple[list[dict], dict[str, tuple[int, str]]]:
        """
        获取所有启用 MCP 服务器的工具。
        返回 (tools_for_llm, tool_route_map)
        tool_route_map: {qualified_name: (server_id, original_tool_name)}
        """
        servers = await mcp_server_repo.filter(status=1)
        if not servers:
            return [], {}

        tools_for_llm = []
        tool_route_map: dict[str, tuple[int, str]] = {}

        for server in servers:
            try:
                server_tools = await mcp_client.list_tools(server)
            except Exception as e:
                api_logger.warning(f"获取 MCP 工具失败 [{server.code}]: {e}")
                continue
            for tool in server_tools:
                qualified_name = f"{server.code}__{tool['name']}"
                tools_for_llm.append({
                    "type": "function",
                    "function": {
                        "name": qualified_name,
                        "description": f"[{server.name}] {tool.get('description', '')}",
                        "parameters": tool.get("inputSchema", {"type": "object", "properties": {}}),
                    },
                })
                tool_route_map[qualified_name] = (server.id, tool["name"])

        return tools_for_llm, tool_route_map

    async def _execute_tool(self, server_id: int, tool_name: str, arguments: dict) -> str:
        """执行 MCP 工具并返回文本结果"""
        try:
            result = await mcp_client.call_tool(
                await mcp_server_repo.get_by_id(server_id), tool_name, arguments,
            )
            parts = []
            for item in result.get("content", []):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
                else:
                    parts.append(json.dumps(item, ensure_ascii=False))
            return "\n".join(parts) if parts else "(工具无返回内容)"
        except Exception as e:
            api_logger.error(f"MCP 工具执行失败: {e}")
            return f"工具执行失败: {e}"

    # ---- 工具调用处理 ----

    async def _process_tool_calls(
            self, session_id: int, msg, tool_route_map: dict, llm_messages: list[dict],
    ) -> None:
        """处理 LLM 返回的工具调用：保存 assistant 消息、执行工具、保存结果"""
        tc_dicts = [tc.model_dump() for tc in msg.tool_calls]

        # 保存 assistant 工具调用消息
        await chat_message_repo.create(
            session_id=session_id, role="assistant",
            content=msg.content or "",
            tool_calls=json.dumps(tc_dicts, ensure_ascii=False),
        )
        llm_messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": tc_dicts,
        })

        # 逐个执行工具
        for tc in msg.tool_calls:
            qualified = tc.function.name
            args = json.loads(tc.function.arguments or "{}")
            server_id, real_name = tool_route_map.get(qualified, (0, qualified))

            result_text = await self._execute_tool(server_id, real_name, args)

            await chat_message_repo.create(
                session_id=session_id, role="tool",
                content=result_text,
                tool_call_id=tc.id,
                tool_name=qualified,
            )
            llm_messages.append({
                "role": "tool",
                "content": result_text,
                "tool_call_id": tc.id,
            })

    # ---- 消息构建 ----

    def _build_llm_messages(self, history: list[ChatMessage]) -> list[dict]:
        """从 DB 消息列表构建 LLM 消息数组"""
        msgs: list[dict] = [{"role": "system", "content": self._get_system_prompt()}]
        for msg in history:
            if msg.role in ("user", "system"):
                msgs.append({"role": msg.role, "content": msg.content})
            elif msg.role == "assistant":
                entry: dict = {"role": "assistant", "content": msg.content or ""}
                if msg.tool_calls:
                    entry["tool_calls"] = json.loads(msg.tool_calls)
                msgs.append(entry)
            elif msg.role == "tool":
                msgs.append({
                    "role": "tool",
                    "content": msg.content,
                    "tool_call_id": msg.tool_call_id,
                })
        return msgs

    # ---- 核心：发送消息 ----

    async def send_message(
            self, session_id: int, user_id: int, content: str,
    ) -> AsyncGenerator[str, None]:
        """发送消息，支持 MCP 工具调用，流式返回最终文本"""
        # 校验会话
        session = await chat_session_service.get_user_session_or_raise(session_id, user_id)

        # 先保存用户消息（即使后续出错也不丢失）
        await chat_message_repo.create(session_id=session_id, role="user", content=content)

        model = await self._get_enabled_model()
        client = AsyncOpenAI(api_key=model.api_key, base_url=model.base_url)

        # 获取 MCP 工具（失败时降级为无工具）
        tools, tool_route_map = [], {}
        try:
            tools, tool_route_map = await self._fetch_mcp_tools()
        except Exception as e:
            api_logger.warning(f"加载 MCP 工具失败，降级为无工具模式: {e}")

        # 构建初始上下文
        history = await chat_message_repo.get_recent_messages(session_id, limit=_CONTEXT_WINDOW)
        llm_messages = self._build_llm_messages(history)

        # 工具调用循环 + 强制总结
        final_text = ""

        try:
            for round_idx in range(_MAX_TOOL_ROUNDS + 1):
                # 最后一轮不带工具，强制 LLM 输出文本总结
                is_force_summary = (round_idx == _MAX_TOOL_ROUNDS)
                response = await client.chat.completions.create(
                    model=model.model_name,
                    messages=llm_messages,
                    max_tokens=model.max_tokens,
                    tools=None if is_force_summary else (tools or None),
                )
                if not response.choices:
                    api_logger.warning(f"LLM 返回空 choices: {response}")
                    break

                msg = response.choices[0].message

                if msg.tool_calls and not is_force_summary:
                    await self._process_tool_calls(session_id, msg, tool_route_map, llm_messages)
                else:
                    final_text = msg.content or ""
                    await chat_message_repo.create(
                        session_id=session_id, role="assistant", content=final_text,
                    )
                    break

        except Exception as e:
            api_logger.error(f"LLM 调用失败: {e}")
            yield f"data: {json.dumps({'error': f'LLM 调用失败: {e}'}, ensure_ascii=False)}\n\n"
            return

        # 自动标题
        if session.title == "新对话":
            first_user_msg = await chat_message_repo.get_first_user_message(session_id)
            if first_user_msg:
                title = first_user_msg.content[:_TITLE_MAX_LENGTH]
                if len(first_user_msg.content) > _TITLE_MAX_LENGTH:
                    title += "..."
                session.title = title
                await session.save()

        # 输出最终文本
        yield f"data: {json.dumps({'content': final_text or '(模型未返回内容)'}, ensure_ascii=False)}\n\n"
        yield "data: [DONE]\n\n"

    async def get_message_history(
            self, session_id: int, user_id: int, current: int = 1, size: int = 50,
    ) -> Tuple[List[dict], int]:
        await chat_session_service.get_user_session_or_raise(session_id, user_id)

        items, total = await chat_message_repo.get_session_messages(
            session_id=session_id, current=current, size=size,
        )
        records = [
            ChatMessageResponse.model_validate(m).model_dump(mode="json")
            for m in items
        ]
        return records, total


# 单例
chat_session_service = ChatSessionService()
chat_service = ChatService()
