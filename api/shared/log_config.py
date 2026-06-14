import logging
import os
from contextvars import ContextVar
from logging.handlers import TimedRotatingFileHandler

from core.config import settings

# 请求追踪 ID，由中间件在每次请求开始时设置
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    """从 ContextVar 注入 request_id 到日志记录"""

    def filter(self, record):
        record.request_id = request_id_var.get()
        return True


class NoErrorFilter(logging.Filter):
    """过滤掉 ERROR 及以上级别，避免 general_handler 重复记录错误"""

    def filter(self, record):
        return record.levelno < logging.ERROR


def _build_format():
    if settings.LOG_FORMAT_TYPE == "json":
        try:
            from pythonjsonlogger import jsonlogger
            return jsonlogger.JsonFormatter(
                "%(asctime)s %(name)s %(levelname)s %(filename)s %(lineno)d %(funcName)s %(message)s %(request_id)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        except ImportError:
            pass  # 降级为文本格式
    fmt = settings.LOG_FORMAT
    # 确保格式中包含 request_id 占位符
    if settings.LOG_INCLUDE_REQUEST_ID and "%(request_id)s" not in fmt:
        fmt = "%(request_id)s - " + fmt
    return logging.Formatter(fmt)


def setup_logging():
    """配置日志系统"""
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_level = getattr(logging, settings.LOG_LEVEL.upper())
    formatter = _build_format()

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 添加 request_id 过滤器
    request_id_filter = RequestIdFilter()

    if settings.LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(request_id_filter)
        root_logger.addHandler(console_handler)

    if settings.LOG_TO_FILE:
        backup_count = settings.LOG_FILE_BACKUP_COUNT

        # 错误日志 - 仅记录 ERROR 及以上
        error_handler = TimedRotatingFileHandler(
            os.path.join(logs_dir, "error.log"),
            when="midnight",
            backupCount=backup_count,
            encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        error_handler.addFilter(request_id_filter)
        root_logger.addHandler(error_handler)

        # 一般日志 - 记录配置级别及以下，排除 ERROR
        general_handler = TimedRotatingFileHandler(
            os.path.join(logs_dir, "general.log"),
            when="midnight",
            backupCount=backup_count,
            encoding="utf-8"
        )
        general_handler.setLevel(log_level)
        general_handler.setFormatter(formatter)
        general_handler.addFilter(request_id_filter)
        general_handler.addFilter(NoErrorFilter())
        root_logger.addHandler(general_handler)

    # 设置 tortoise ORM 日志级别
    logging.getLogger("tortoise").setLevel(log_level)

    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成")

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """获取指定名称的日志记录器"""
    return logging.getLogger(name)


# 预定义的常用日志记录器（精简为 4 个）
app_logger = get_logger("app")
db_logger = get_logger("database")
api_logger = get_logger("api")
cache_logger = get_logger("cache")
