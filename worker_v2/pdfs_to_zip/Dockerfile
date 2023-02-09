FROM python:3.10

ARG BUILD_TYPE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.3.2

RUN python3 -m pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
RUN apt update
RUN apt install -y zip
WORKDIR /opt/app
COPY poetry.lock pyproject.toml /opt/app/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_TYPE" = "production" && echo "--without dev") --no-interaction --no-ansi --no-root

COPY . .
ENTRYPOINT [ "python3", "zip_worker.py" ]