from pydantic import BaseModel
from rimhub.models.config.logging_config import LoggingConfig


class AppConfig(BaseModel):
    logging_config: LoggingConfig = LoggingConfig()