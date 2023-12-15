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
    rabbitmq_queue_send_localstorage: str
    email_smtp_server: str
    email_smtp_port: int
    email_user: str
    redis_url: RedisDsn
    subject_for_email: str | None = 'Voucher are attached.'
    username_for_email: str | None = ''
    password_for_email: str | None = ''
    folder_to_store: str | None = r'/opt/app/storage'
    folder_for_client: str | None = r'/nfs/vouchers_storage/'
    react_app_myip: str

    model_config = SettingsConfigDict(env_file='.env')


logging_config.dictConfig(LOGGING)
settings = Settings()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
