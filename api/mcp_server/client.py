import asyncio
import json
import httpx
from typing import List, Dict

from fastmcp import Client
from openai import OpenAI

from core.settings import settings


class BearerTokenAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request):
        request.headers["Authorization"] = f"{self.token}"
        yield request


class MCPPoweredAI:
    """让大模型能够调用MCP工具的AI代理"""

    def __init__(self, mcp_server_url: str, openai_api_key: str = None):
        # 初始化MCP客户端
        auth = BearerTokenAuth(openai_api_key)
        self.mcp_client = Client(mcp_server_url, auth=auth)

        # 初始化OpenAI客户端
        self.llm_client = OpenAI(
            base_url='https://api-inference.modelscope.cn/v1',
            api_key=settings.MODEL_API_KEY,  # ModelScope Token
        )

        # 缓存可用工具列表
        self.available_tools = []

    async def initialize(self):
        """初始化，获取MCP服务器提供的所有工具"""
        async with self.mcp_client as client:
            tools = await client.list_tools()
            self.available_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
                for tool in tools
            ]
        print(f"已加载 {len(self.available_tools)} 个MCP工具")
        return self

    def _format_tools_for_llm(self) -> List[Dict]:
        """将MCP工具格式化为大模型能理解的格式"""
        formatted_tools = []
        for tool in self.available_tools:
            formatted_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["parameters"]
                }
            })
        return formatted_tools

    async def process_query(self, user_query: str) -> str:
        """
        处理用户查询：让大模型决定是否需要以及如何调用MCP工具

        Args:
            user_query: 用户的问题或指令

        Returns:
            处理结果
        """
        # 步骤1：让大模型分析是否需要调用工具
        system_prompt = f"""你是一个AI助手，可以调用以下工具来帮助用户：
        
        可用工具：
        {json.dumps([f"{t['function']['name']}:{t['function']['description']}" for t in self._format_tools_for_llm()], indent=2)}
        
        分析用户请求，如果需要调用工具，请使用指定的格式。如果不需要，直接回答。
        工具调用格式：{{"action": "call_tool", "tool_name": "工具名", "arguments": {{参数}}}}
        """
        extra_body = {
            # enable thinking, set to False to disable test
            "enable_thinking": False,
            # use thinking_budget to contorl num of tokens used for thinking
            # "thinking_budget": 4096
        }
        # 与大模型对话，允许它选择调用工具
        response = self.llm_client.chat.completions.create(
            model="Qwen/Qwen3-8B",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            tools=self._format_tools_for_llm(),
            tool_choice="auto",  # 让模型自主决定是否调用工具
            extra_body=extra_body,
            stream=False,
        )

        message = response.choices[0].message
        print(message)
        # 步骤2：检查是否需要执行工具调用
        if message.tool_calls:
            results = []
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                # 执行MCP工具调用
                async with self.mcp_client as client:
                    result = await client.call_tool(tool_name, arguments)
                    results.append({
                        "tool": tool_name,
                        "result": result.content[0].text if result.content else "无返回结果"
                    })

            # 步骤3：将工具执行结果反馈给大模型，让它生成最终回复
            tools_results_str = "\n".join([
                f"- {r['tool']}: {r['result']}"
                for r in results
            ])

            final_response = self.llm_client.chat.completions.create(
                model="Qwen/Qwen3-8B",
                messages=[
                    {"role": "system", "content": "你是一个AI助手，请基于工具执行结果回答用户问题"},
                    {"role": "user", "content": user_query},
                    message,  # 包含工具调用请求的消息
                    {"role": "tool", "content": tools_results_str, "tool_call_id": tool_call.id}
                ],
                extra_body=extra_body,
                stream=False,
            )

            return final_response.choices[0].message.content

        # 如果不需调用工具，直接返回大模型的回复
        return message.content

    async def interactive_chat(self):
        """交互式聊天模式"""
        print("=" * 50)
        print("MCP增强型AI助手已启动！")
        print("我可以调用以下工具来帮助你：")
        for tool in self.available_tools:
            print(f"  - {tool['name']}: {tool['description']}")
        print("=" * 50)

        while True:
            try:
                user_input = input("\n你: ").strip()
                if user_input.lower() in ['退出', 'exit', 'quit']:
                    break

                print("AI: ", end="", flush=True)
                response = await self.process_query(user_input)
                print(response)

            except KeyboardInterrupt:
                break
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(f"错误: {str(e)}")


async def main():
    mcp_server_url = "http://127.0.0.1:8001/sse"
    ai_agent = await MCPPoweredAI(mcp_server_url, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjkwODUyNTQsInVpZCI6MX0.p_HgRLrXD1UXIqQEFstE1U-99coNVaysRkJcEh69B1c").initialize()
    await ai_agent.interactive_chat()


if __name__ == '__main__':
    asyncio.run(main())
