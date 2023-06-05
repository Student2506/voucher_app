FROM python:3.10

ARG BUILD_TYPE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.4.1

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y \
  unixodbc-dev \
  icu-devtools \
  libicu-dev \
  pkg-config \
  msodbcsql18 \
  mssql-tools18 \
  && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /opt/app
COPY pyproject.toml poetry.lock /opt/app/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_TYPE" = "production" && echo "--without dev") --only=api_receive --no-interaction --no-ansi --no-root

COPY . .
ENTRYPOINT [ "python3", "receive_worker.py" ]