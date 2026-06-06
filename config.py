

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Settings:
    APP_NAME = "example_utilities"
    IDENTITY_PATH = Path("/home/gonza/sources/fast-ret/test-server")


settings = Settings()