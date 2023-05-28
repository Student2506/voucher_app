"""Settings for the project."""

import logging
from ipaddress import IPv4Address
from logging import config as logging_config

from pydantic import AmqpDsn, BaseSettings, RedisDsn

from settings.logging import LOGGING


class Settings(BaseSettings):
    """Settings for worker."""

    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_url: AmqpDsn
    rabbitmq_queue_html_to_pdf: str
    rabbitmq_queue_pdf_to_zip: str
    debug: bool | None = False
    myip: IPv4Address | str = '127.0.0.1'
    threads: int | None = 5
    redis_url: RedisDsn

    class Config:
        """Configuration class."""

        env_file = '.env'


logging_config.dictConfig(LOGGING)
settings = Settings()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
