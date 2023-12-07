"""Settings for the project."""

import logging
from logging import config as logging_config

from pydantic import AmqpDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from settings.logging import LOGGING


class Settings(BaseSettings):
    """Settings for worker."""

    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_url: AmqpDsn
    debug: bool | None = False
    rabbitmq_queue_pdf_to_zip: str
    rabbitmq_queue_send_email: str
    rabbitmq_queue_send_sharepoint: str
    volume_size: int | None = 10
    redis_url: RedisDsn
    model_config = SettingsConfigDict(env_file='.env')


logging_config.dictConfig(LOGGING)
settings = Settings()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
