"""Settings for the project."""

from ipaddress import IPv4Address

from pydantic import AmqpDsn, BaseSettings, PostgresDsn


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

    class Config:
        """Configuration class."""

        env_file = '.env'


settings = Settings()
