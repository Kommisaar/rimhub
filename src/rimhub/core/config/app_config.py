from pathlib import Path

from pydantic import ValidationError
from ruamel.yaml import YAML
from ruamel.yaml import YAMLError

from rimhub.models import AppConfig
from rimhub.core import setup_basic_logger

logger = setup_basic_logger(__name__)
def load_config(config_path: str | Path) -> AppConfig:
    try:
        logger.info("正在载入配置文件中...")
        yaml = YAML(typ="safe")
        config = yaml.load(Path(config_path))
        AppConfig.model_validate(config)
        logger.info("配置文件载入成功")
        return config
    except FileNotFoundError as e:
        logger.error(f"未找到配置文件: {e}")
        raise
    except (PermissionError, OSError) as e:
        logger.error(f"无法打开配置文件: {e}")
        raise
    except YAMLError as e:
        logger.error(f"YAML 解析时发生错误: {e}")
        raise
    except ValidationError as e:
        logger.error("配置文件结构校验失败，请检查字段名和类型是否正确。")
        raise
    except Exception as e:
        logger.error(f"读取配置文件时发生未知错误: {e}")
        raise
