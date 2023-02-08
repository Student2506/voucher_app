"""Settings for the project."""

from pydantic import AmqpDsn, BaseSettings, RedisDsn


class Settings(BaseSettings):
    """Settings for worker."""

    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_url: AmqpDsn
    rabbitmq_queue: str
    rabbitmq_queue_html_to_pdf: str
    debug: bool | None = False
    rabbitmq_queue_send_email: str
    email_smtp_server: str
    email_smtp_port: int
    email_user: str
    redis_url: RedisDsn
    subject_for_email: str | None = 'Voucher are attached.'

    class Config:
        """Configuration class."""

        env_file = '.env'


settings = Settings()
