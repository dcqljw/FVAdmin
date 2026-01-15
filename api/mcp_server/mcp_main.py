from typing import Any

import httpx
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware, MiddlewareContext, CallNext
from fastmcp.tools.tool import ToolResult
from fastmcp.utilities.openapi import HTTPRoute
from mcp import types as mt

class CustomHTTPClient:
    """自定义 HTTP 客户端，可以添加请求头"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def send_request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """发送 HTTP 请求，自动添加自定义头"""

        # 添加自定义请求头
        headers = kwargs.get('headers', {})
        custom_headers = {
            'X-Custom-Header': 'my-custom-value',
            'X-Request-ID': f'req-{id(self)}',
            'X-Timestamp': str(asyncio.get_event_loop().time()),
        }
        headers.update(custom_headers)

        # 更新 kwargs 中的 headers
        kwargs['headers'] = headers

        # 发送请求
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        print(f"发送请求到: {url}")
        print(f"请求头: {headers}")

        response = await self.client.request(method, path, **kwargs)
        return response


# 使用自定义客户端
custom_client = CustomHTTPClient("http://127.0.0.1:8000")


client = httpx.AsyncClient(base_url="http://127.0.0.1:8000")
openapi_spec = httpx.get("http://127.0.0.1:8000/openapi.json").json()


# def customize_components(
#         route: HTTPRoute,
#         component: OpenAPITool | OpenAPIResource | OpenAPIResourceTemplate,
# ):
#     print(route)
#     print(component)


class CustomMiddleWare(Middleware):
    async def on_message(
            self,
            context: MiddlewareContext[Any],
            call_next: CallNext[Any, Any],
    ) -> Any:
        return await call_next(context)

    async def on_call_tool(
            self,
            context: MiddlewareContext[mt.CallToolRequestParams],
            call_next: CallNext[mt.CallToolRequestParams, ToolResult],
    ) -> ToolResult:
        print(context)
        return await call_next(context)

    async def on_request(
            self,
            context: MiddlewareContext[mt.Request[Any, Any]],
            call_next: CallNext[mt.Request[Any, Any], Any],
    ) -> Any:
        print(context)
        try:
            print(context.fastmcp_context.request_context.request.headers)
        except:
            pass
        return await call_next(context)


mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
)
mcp_app = mcp.http_app(path='/mcp')
mcp.add_middleware(CustomMiddleWare())

if __name__ == '__main__':
    mcp.run(transport="sse", host="0.0.0.0", port=8001)
