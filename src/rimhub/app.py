from pathlib import Path

from rimhub.core.config import load_config


class RimHubApp:
    def __init__(self, config_path: str | Path):
        self.config = load_config(config_path)

    def run(self):
        pass
