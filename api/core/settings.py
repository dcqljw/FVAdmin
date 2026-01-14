from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env", BASE_DIR / ".env.dev"),
        env_ignore_empty=True,
        extra="ignore",
    )
    LOG_LEVEL: str = "INFO"
    LOG_FILE_MAX_SIZE: str = "10MB"  # 日志文件最大大小
    LOG_FILE_BACKUP_COUNT: int = 5  # 保留的日志文件备份数量
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"  # 日志格式
    LOG_TO_CONSOLE: bool = True  # 是否输出到控制台
    LOG_TO_FILE: bool = True  # 是否输出到文件
    PROJECT_NAME: str = ""
    MYSQL_HOST: str = ""
    MYSQL_PORT: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = ""
    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    OSS_URL: str = ""
    OSS_KEY: str = ""
    OSS_SECRET: str = ""
    OSS_BUCKET: str = ""
    MODEL_API_KEY: str = ""


settings = Settings()
