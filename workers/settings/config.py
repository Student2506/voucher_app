"""Settings for the project."""

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
    rabbitmq_queue: str

    class Config:
        """Configuration class."""

        env_file = '.env'


settings = Settings()
