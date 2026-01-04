import httpx
from fastmcp import FastMCP

client = httpx.AsyncClient(base_url="http://127.0.0.1:8000", headers={
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjgxNDYxOTksInVpZCI6MX0.fctFeDgLJ9I4osaXxYf87bh9FrElcH5F1c4QJuPqNhw"
})
openapi_spec = httpx.get("http://127.0.0.1:8000/openapi.json").json()

mcp = FastMCP.from_openapi(
    openapi_spec=openapi_spec,
    client=client,
)
mcp_app = mcp.http_app(path='/mcp')

if __name__ == '__main__':
    mcp.run(transport="sse", host="0.0.0.0", port=8001)
