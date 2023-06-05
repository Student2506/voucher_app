FROM python:3.10

ARG BUILD_TYPE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV POETRY_VERSION=1.4.1

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y \
  msodbcsql18 \
  mssql-tools18 \
  gcc \
  unixodbc-dev \
  && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /opt/app
ADD ca_new.cer /usr/local/share/ca-certificates/ca_new.crt
RUN chmod 644 /usr/local/share/ca-certificates/ca_new.crt && update-ca-certificates
COPY uwsgi/uwsgi.ini uwsgi.ini
COPY poetry.lock pyproject.toml /opt/app/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_TYPE" = "production" && echo "--without dev") --no-interaction --no-ansi --no-root

COPY . .
RUN mkdir -p media/uploads/
RUN chmod -R a+w media/