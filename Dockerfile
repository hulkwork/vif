FROM python:3.10-slim AS train

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY src /app/src
COPY vif/data_preparation /app/vif/data_preparation

RUN pip install poetry \
    && poetry install --no-dev --no-interaction

RUN apt-get update && apt-get install -y build-essential

FROM python:3.10-slim AS api

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY src /app/src
COPY vif/data_preparation /app/vif/data_preparation
COPY vif/api /app/vif/api

RUN pip install poetry \
    && poetry install --no-dev --no-interaction

EXPOSE 5000

CMD ["poetry", "run", "uvicorn", "vif.api.main:app", "--host", "0.0.0.0", "--port", "5000"]

FROM python:3.10-slim AS test

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY src /app/src
COPY vif/data_preparation /app/vif/data_preparation
COPY vif/tests /app/vif/tests

RUN pip install poetry \
    && poetry install --no-dev --no-interaction

CMD ["poetry", "run", "pytest", "--maxfail=1", "--disable-warnings", "-q"]
