from logging import CRITICAL
from logging import DEBUG
from logging import ERROR
from logging import Formatter
from logging import INFO
from logging import Logger
from logging import StreamHandler
from logging import WARNING
from logging import getLogger
from typing import Literal

# 定义合法的日志级别字符串类型（用于类型提示）
LOG_LEVELS = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# 映射字符串到 logging 模块的实际值
LEVEL_MAP = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL,
}


def setup_basic_logger(name: str, level: LOG_LEVELS = "INFO") -> Logger:
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logger = getLogger(name)

    if not logger.handlers:
        logger.setLevel(LEVEL_MAP[level] if isinstance(level, str) else level)
        formatter = Formatter(log_format, date_format)
        handler = StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # 避免重复输出
        logger.info(f"基础日志已启动")

    return logger
