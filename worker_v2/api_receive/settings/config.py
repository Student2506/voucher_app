"""Settings for the project."""

import logging
from ipaddress import IPv4Address
from logging import config as logging_config

from pydantic import AmqpDsn, BaseSettings, PostgresDsn, RedisDsn

from settings.logging import LOGGING


class Settings(BaseSettings):
    """Settings for worker."""

    mssql_host: str
    mssql_db: str
    mssql_user: str
    mssql_password: str
    mssql_url: str
    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_host: str
    postgres_url: PostgresDsn
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_url: AmqpDsn
    rabbitmq_queue_incoming: str
    rabbitmq_queue_html_to_pdf: str
    rabbitmq_queue_send_email: str
    debug: bool | None = False
    myip: IPv4Address | str = '127.0.0.1'
    background_color: str | None = 'white'
    foreground_color: str | None = 'black'
    redis_url: RedisDsn

    class Config:
        """Configuration class."""

        env_file = '.env'


logging_config.dictConfig(LOGGING)
settings = Settings()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
