FROM python:3.10

ARG BUILD_TYPE

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.3.2

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt update
RUN ACCEPT_EULA=Y apt install -y msodbcsql18
RUN ACCEPT_EULA=Y apt install -y mssql-tools18
RUN apt install -y unixodbc-dev
RUN python3 -m pip install -U pip
RUN pip install "poetry==$POETRY_VERSION"
WORKDIR /opt/app
COPY poetry.lock pyproject.toml /opt/app/
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$BUILD_TYPE" = "production" && echo "--without dev") --no-interaction --no-ansi --no-root

COPY . .
ENTRYPOINT [ "python3", "receive_worker.py" ]