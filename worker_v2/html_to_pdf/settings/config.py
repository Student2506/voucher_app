"""Settings for the project."""

from ipaddress import IPv4Address

from pydantic import AmqpDsn, BaseSettings


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

    class Config:
        """Configuration class."""

        env_file = '.env'


settings = Settings()
