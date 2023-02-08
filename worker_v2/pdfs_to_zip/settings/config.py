"""Settings for the project."""

from pydantic import AmqpDsn, BaseSettings


class Settings(BaseSettings):
    """Settings for worker."""

    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    rabbitmq_url: AmqpDsn
    rabbitmq_queue: str
    rabbitmq_queue_html_to_pdf: str
    debug: bool | None = False
    rabbitmq_queue_pdf_to_zip: str
    rabbitmq_queue_send_email: str
    volume_size: int | None = 10240

    class Config:
        """Configuration class."""

        env_file = '.env'


settings = Settings()
