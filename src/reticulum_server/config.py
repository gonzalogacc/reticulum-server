from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    APP_NAME: str = "example_utilities"
    IDENTITY_PATH: Path = Path("/home/gonza/sources/fast-ret/test-server")
    ANNOUNCE_INTERVAL_SECONDS: int = 10


settings = Settings()
