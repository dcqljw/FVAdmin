import json
from typing import Any, Optional

from redis.asyncio import Redis, ConnectionPool

from core.settings import settings
from core.log_config import cache_logger


class RedisCache:
    """异步 Redis 缓存客户端，支持自动降级"""

    _instance: Optional["RedisCache"] = None
    _redis: Optional[Redis] = None
    _enabled: bool = True

    def __new__(cls) -> "RedisCache":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self) -> bool:
        """初始化 Redis 连接池"""
        if not settings.REDIS_ENABLED:
            self._enabled = False
            cache_logger.warning("Redis 已禁用（REDIS_ENABLED=False）")
            return False

        try:
            pool = ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                db=settings.REDIS_DB,
                decode_responses=True,
            )
            self._redis = Redis(connection_pool=pool)
            # 测试连接
            await self._redis.ping()
            self._enabled = True
            cache_logger.info(
                f"Redis 连接成功: {settings.REDIS_HOST}:{settings.REDIS_PORT}"
            )
            return True
        except Exception as e:
            self._enabled = False
            self._redis = None
            cache_logger.warning(f"Redis 连接失败，启用降级模式: {str(e)}")
            return False

    async def close(self) -> None:
        """关闭 Redis 连接"""
        if self._redis:
            await self._redis.close()
            self._redis = None
            cache_logger.info("Redis 连接已关闭")

    def _serialize(self, value: Any) -> str:
        """序列化值为 JSON 字符串"""
        return json.dumps(value)

    def _deserialize(self, value: Optional[str]) -> Any:
        """反序列化 JSON 字符串"""
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    # ========== 基础操作 ==========

    async def get(self, key: str) -> Any:
        """获取缓存值"""
        if not self._enabled or not self._redis:
            return None
        try:
            value = await self._redis.get(key)
            return self._deserialize(value)
        except Exception as e:
            cache_logger.error(f"Redis GET 失败: {key}, {str(e)}")
            return None

    async def set(
        self, key: str, value: Any, ttl: Optional[int] = None
    ) -> bool:
        """设置缓存值"""
        if not self._enabled or not self._redis:
            return False
        try:
            serialized = self._serialize(value)
            if ttl:
                await self._redis.setex(key, ttl, serialized)
            else:
                await self._redis.set(key, serialized)
            return True
        except Exception as e:
            cache_logger.error(f"Redis SET 失败: {key}, {str(e)}")
            return False

    async def delete(self, key: str) -> bool:
        """删除缓存"""
        if not self._enabled or not self._redis:
            return False
        try:
            await self._redis.delete(key)
            return True
        except Exception as e:
            cache_logger.error(f"Redis DELETE 失败: {key}, {str(e)}")
            return False

    async def exists(self, key: str) -> bool:
        """检查键是否存在"""
        if not self._enabled or not self._redis:
            return False
        try:
            return await self._redis.exists(key) > 0
        except Exception as e:
            cache_logger.error(f"Redis EXISTS 失败: {key}, {str(e)}")
            return False

    async def expire(self, key: str, seconds: int) -> bool:
        """设置过期时间"""
        if not self._enabled or not self._redis:
            return False
        try:
            return await self._redis.expire(key, seconds)
        except Exception as e:
            cache_logger.error(f"Redis EXPIRE 失败: {key}, {str(e)}")
            return False

    async def ttl(self, key: str) -> int:
        """获取剩余过期时间（秒）"""
        if not self._enabled or not self._redis:
            return -1
        try:
            return await self._redis.ttl(key)
        except Exception as e:
            cache_logger.error(f"Redis TTL 失败: {key}, {str(e)}")
            return -1

    # ========== 批量操作 ==========

    async def get_many(self, keys: list[str]) -> dict[str, Any]:
        """批量获取"""
        if not self._enabled or not self._redis:
            return {}
        try:
            values = await self._redis.mget(keys)
            return {
                key: self._deserialize(value)
                for key, value in zip(keys, values)
                if value is not None
            }
        except Exception as e:
            cache_logger.error(f"Redis MGET 失败: {str(e)}")
            return {}

    async def set_many(
        self, mapping: dict[str, Any], ttl: Optional[int] = None
    ) -> bool:
        """批量设置"""
        if not self._enabled or not self._redis:
            return False
        try:
            serialized_map = {k: self._serialize(v) for k, v in mapping.items()}
            await self._redis.mset(serialized_map)
            if ttl:
                for key in mapping:
                    await self._redis.expire(key, ttl)
            return True
        except Exception as e:
            cache_logger.error(f"Redis MSET 失败: {str(e)}")
            return False

    async def delete_many(self, keys: list[str]) -> int:
        """批量删除"""
        if not self._enabled or not self._redis:
            return 0
        try:
            return await self._redis.delete(*keys)
        except Exception as e:
            cache_logger.error(f"Redis 批量删除失败: {str(e)}")
            return 0

    # ========== 高级操作 ==========

    async def incr(self, key: str, amount: int = 1) -> int:
        """自增"""
        if not self._enabled or not self._redis:
            return 0
        try:
            return await self._redis.incrby(key, amount)
        except Exception as e:
            cache_logger.error(f"Redis INCR 失败: {key}, {str(e)}")
            return 0

    async def decr(self, key: str, amount: int = 1) -> int:
        """自减"""
        if not self._enabled or not self._redis:
            return 0
        try:
            return await self._redis.decrby(key, amount)
        except Exception as e:
            cache_logger.error(f"Redis DECR 失败: {key}, {str(e)}")
            return 0

    async def set_if_not_exists(
        self, key: str, value: Any, ttl: Optional[int] = None
    ) -> bool:
        """仅当键不存在时设置（NX 操作）"""
        if not self._enabled or not self._redis:
            return False
        try:
            serialized = self._serialize(value)
            result = await self._redis.setnx(key, serialized)
            if result and ttl:
                await self._redis.expire(key, ttl)
            return result
        except Exception as e:
            cache_logger.error(f"Redis SETNX 失败: {key}, {str(e)}")
            return False

    # ========== 辅助方法 ==========

    async def keys(self, pattern: str) -> list[str]:
        """查找匹配模式的键"""
        if not self._enabled or not self._redis:
            return []
        try:
            return await self._redis.keys(pattern)
        except Exception as e:
            cache_logger.error(f"Redis KEYS 失败: {pattern}, {str(e)}")
            return []

    async def clear_all(self) -> bool:
        """清空当前数据库（慎用）"""
        if not self._enabled or not self._redis:
            return False
        try:
            await self._redis.flushdb()
            cache_logger.warning("Redis 数据库已清空")
            return True
        except Exception as e:
            cache_logger.error(f"Redis FLUSHDB 失败: {str(e)}")
            return False

    def is_enabled(self) -> bool:
        """检查 Redis 是否可用"""
        return self._enabled and self._redis is not None


# 全局单例实例
redis_cache = RedisCache()