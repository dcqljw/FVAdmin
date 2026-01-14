import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from core.settings import settings


def setup_logging():
    """
    配置日志系统
    """
    # 创建 logs 目录（如果不存在）
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # 获取根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # 清除现有的处理器，避免重复
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # 定义日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    )

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    console_handler.setFormatter(formatter)

    # 日志文件处理器 - 错误日志
    error_log_path = os.path.join(logs_dir, f"error_{datetime.now().strftime('%Y%m%d')}.log")
    error_handler = RotatingFileHandler(
        error_log_path,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # 日志文件处理器 - 一般日志
    general_log_path = os.path.join(logs_dir, f"general_{datetime.now().strftime('%Y%m%d')}.log")
    general_handler = RotatingFileHandler(
        general_log_path,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    general_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    general_handler.setFormatter(formatter)

    # 添加处理器到根日志记录器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(general_handler)

    # 特别为数据库操作设置日志级别
    db_logger = logging.getLogger('tortoise')
    db_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # 创建一个通用日志记录器
    logger = logging.getLogger(__name__)
    logger.info("日志系统初始化完成")

    return root_logger


def get_logger(name: str = None):
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称，如果不提供则返回通用日志记录器
    
    Returns:
        Logger: 日志记录器实例
    """
    if name:
        return logging.getLogger(name)
    else:
        return logging.getLogger(__name__)


# 预定义的常用日志记录器
app_logger = get_logger("app")
db_logger = get_logger("database")
api_logger = get_logger("api")
auth_logger = get_logger("auth")