"""Setting for the project."""

import logging
from logging import config as logging_config

from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.logging import LOGGING


class Settings(BaseSettings):
    """Settings for worker."""

    debug: bool | None = False
    redis_url: RedisDsn
    port_to_listen: int | None = 8080
    chunk_size: int | None = 1 * 1024 * 1024
    model_config = SettingsConfigDict(env_file='.env')


logging_config.dictConfig(LOGGING)
settings = Settings()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
