FROM python:3.10.13-slim-bookworm

LABEL maintener='Pavel Zakharov <pzakharov83@gmail.com>'

ARG BUILD_TYPE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.7.1

RUN python3 -m pip install -U pip
RUN pip install "poetry==${POETRY_VERSION}"
WORKDIR /opt/app
COPY pyproject.toml poetry.lock /opt/app/
RUN poetry config virtualenvs.create false \
    && poetry install $(test "${BUILD_TYPE}" = "production" && echo "--without dev") --only=file_storage --no-interaction --no-ansi --no-root

COPY . .
ENTRYPOINT [ "gunicorn", "file_storage:webapp", "--bind", "0.0.0.0:8080", "--worker-class", "aiohttp.GunicornUVLoopWebWorker", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "DEBUG", "--disable-redirect-access-to-syslog"]