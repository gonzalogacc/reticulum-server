from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    APP_NAME: str = "example_utilities"
    IDENTITY_PATH: Path = Path("test-server")
    CONFIG_FILE: Path = Path("~/.reticulum")
    ANNOUNCE_INTERVAL_SECONDS: int = 60


settings = Settings()
