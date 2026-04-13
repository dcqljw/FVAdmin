# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FVAdmin API is a FastAPI-based admin backend with RBAC permissions, Redis caching, and MCP server integration for AI tools.

## Commands

```bash
# Run the development server
uv run uvicorn main:app --reload

# Run directly
uv run python main.py

# Database migrations (Aerich)
uv run aerich migrate --name "description"  # Create migration
uv run aerich upgrade                        # Apply migrations
uv run aerich downgrade                      # Rollback migration
uv run aerich history                        # View migration history

# MCP server (runs on port 8001)
uv run python mcp_server/mcp_main.py
```

## Architecture

### Entry Point
- `main.py` - FastAPI app with lifespan context manager, initializes database and bootstrap data

### Core Modules (`core/`)
- `settings.py` - Pydantic BaseSettings, loads from `.env` and `.env.dev`
- `security.py` - JWT tokens, bcrypt password hashing, Snowflake ID generator
- `cache.py` - Redis async wrapper with fallback when Redis unavailable
- `log_config.py` - Rotating file handlers for error/general logs
- `middleware.py` - Request logging middleware

### Database
- Uses Tortoise ORM with async MySQL (aiomysql)
- Configuration in `databases.py` - auto-discovery of `*_model.py` files
- Aerich migrations in `migrations/`

### Models (`models/`)
- `User` - Many-to-many relation with `Role`
- `Role` - Many-to-many relation with `Menu` (permissions)
- `Menu` - Hierarchical tree (parent_id), types: 1=menu, 2=button/permission
- Permission check uses `auth_mark` field on Menu (e.g., `user:add`, `role:edit`)

### Router Pattern (`router/`)
Each router file defines endpoints with permission guards:
```python
@router.post("/add")
async def add_user(user: UserCreateSchema, current_user: User = Security(permission_check, scopes=['user:add'])):
```

### Dependencies (`router/deps.py`)
- `verify_token_dep` - JWT validation, returns user ID
- `get_current_user` - Fetches User from database
- `permission_check` - RBAC check (admin bypasses all, others check auth_mark)
- Permissions are cached in Redis with TTL (configurable via `CACHE_PERMISSION_TTL`)

### Response Format (`schemas/response.py`)
All endpoints return `SuccessResponse` or `ErrorResponse`:
```python
{"code": 200, "message": "操作成功", "data": {...}}
{"code": 500, "message": "操作失败", "data": null}
```

### MCP Server (`mcp_server/`)
- `mcp_main.py` - FastMCP server exposing API as tools via OpenAPI spec
- Runs on SSE transport, port 8001
- Connects to main API at localhost:8000

## Key Configuration

Environment variables loaded from `.env` and `.env.dev`:
- MySQL: `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`
- Redis: `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_DB`, `REDIS_ENABLED`
- JWT: `SECRET_KEY`, `ALGORITHM`
- OSS/S3: `OSS_URL`, `OSS_KEY`, `OSS_SECRET`, `OSS_BUCKET`
- AI: `MODEL_API_KEY`
- Cache TTL: `CACHE_PERMISSION_TTL`, `CACHE_MENU_TTL`

## Bootstrap (`init_core.py`)

On startup, creates:
1. Admin user with random password (logged to console)
2. Default menu structure with permission marks
3. Admin role with all menu permissions

## Permission System

- Menu `type=2` items are permission buttons with `auth_mark`
- User's roles determine which menus/permissions they have
- `admin` username bypasses all permission checks
- Permission cache key: `user_permissions:{user_id}`