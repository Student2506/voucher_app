from contextvars import ContextVar
from logging import Filter, LogRecord

request_id: ContextVar[str | None] = ContextVar('request_id', default=None)
username: ContextVar[str | None] = ContextVar('username', default=None)


class RequestIdFilter(Filter):
    def __init__(self, name: str = '', default_value: str | None = 'no_value_provided'):
        super().__init__(name=name)
        self.default_value = default_value

    def filter(self, record: LogRecord) -> bool:
        record.request_id = request_id.get(self.default_value)
        record.username = username.get(self.default_value)
        return True
