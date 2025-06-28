from typing import Literal
from typing import Type

from pydantic import BaseModel
from pydantic import ValidationInfo
from pydantic import field_validator

from rimhub.core import setup_basic_logger

LOG_LEVELS: Type[str] = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
LOG_COLORS: Type[str] = Literal["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "bold_red"]
DEFAULT_LEVEL = "INFO"
DEFAULT_COLOR = {"DEBUG": "cyan", "INFO": "green", "WARNING": "yellow", "ERROR": "red", "CRITICAL": "bold_red"}

logger = setup_basic_logger(__name__)


class LogFormatterConfig(BaseModel):
    base: str = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    console: str = "%(log_color)s[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s%(reset)s"


class LogColorsConfig(BaseModel):
    DEBUG: LOG_COLORS = DEFAULT_COLOR["DEBUG"]
    INFO: LOG_COLORS = DEFAULT_COLOR["INFO"]
    WARNING: LOG_COLORS = DEFAULT_COLOR["WARNING"]
    ERROR: LOG_COLORS = DEFAULT_COLOR["ERROR"]
    CRITICAL: LOG_COLORS = DEFAULT_COLOR["CRITICAL"]

    @field_validator("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", mode="before")
    def validate_log_colors(cls, value: LOG_COLORS, info: ValidationInfo) -> LOG_COLORS:
        if value not in LOG_COLORS:
            logger.warning(
                f"{info.field_name}的颜色无效，使用{info.field_name}的默认颜色：{DEFAULT_COLOR[info.field_name]}")
            return DEFAULT_COLOR[info.field_name]
        return value


class ConsoleHandlerConfig(BaseModel):
    enabled: bool = True
    level: LOG_LEVELS = "DEBUG"
    formatter_name: str = "console"
    colorized: bool = True


class FileRotationConfig(BaseModel):
    max_size: int = 1024 * 1024 * 5
    backup_limit: int = 5


class FileHandlerConfig(BaseModel):
    enabled: bool = True
    level: LOG_LEVELS = "DEBUG"
    formatter_name: str = "base"
    logs_dir: str = "logs"
    keep_last: int = 5
    log_prefix: str = "rimhub"
    log_suffix: str = ".log"
    file_name_format: str = "{prefix}_{date}.{suffix}"
    rotation: FileRotationConfig = FileRotationConfig()


class LogHandlersConfig(BaseModel):
    console: ConsoleHandlerConfig = ConsoleHandlerConfig()
    file: FileHandlerConfig = FileHandlerConfig()


class LoggingConfig(BaseModel):
    level: LOG_LEVELS = "DEBUG"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    formatters: LogFormatterConfig = LogFormatterConfig()
    colors: LogColorsConfig = LogColorsConfig()
    handlers: LogHandlersConfig = LogHandlersConfig()

    @field_validator("level")
    def validate_level(cls, value: LOG_LEVELS):
        if value not in LOG_LEVELS:
            logger.warning(f"无效的日志级别: {value}，使用默认级别：{DEFAULT_LEVEL}")
            return DEFAULT_LEVEL
        return value
