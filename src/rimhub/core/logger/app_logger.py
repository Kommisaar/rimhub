import logging
from logging import FileHandler
from logging import StreamHandler
from pathlib import Path

from rimhub.core import setup_basic_logger
from rimhub.models import FileHandlerConfig
from rimhub.models import LoggingConfig

logger = setup_basic_logger(__name__)


def clean_old_logs(config: FileHandlerConfig):
    logs_dir = Path(config.logs_dir)
    for file in logs_dir.glob("*.log"):
        if file.stat().st_mtime < (file.stat().st_ctime + config.rotation.backup_limit):
            file.unlink()
            print(f"Deleted old log file: {file}")


def setup_file_handler(config: LoggingConfig) -> FileHandler:
    logs_dir: Path = Path(config.handlers.file.logs_dir)
    logs_dir.mkdir(parents=True, exist_ok=True)

    clean_old_logs(config.handlers.file)


def setup_console_handler(console: LoggingConfig) -> StreamHandler:
    pass


def setup_app_logger(config: LoggingConfig, name: str):
    logger = logging.getLogger(name)
    logger.setLevel(config.level)


    if config.handlers.file.enabled:
        file_handler = setup_file_handler(config)
    if config.handlers.console.enabled:
        console_handler = setup_console_handler(config)
