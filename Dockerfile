FROM python:3.10-slim AS train

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
COPY src /app/src

RUN pip install poetry \
    && poetry install
CMD ["poetry", "run", "run-train"]

FROM train AS api
COPY src /app/src
EXPOSE 5000

CMD ["poetry", "run", "uvicorn", "vif.api.main:app", "--host", "0.0.0.0", "--port", "5000"]

FROM train AS test

COPY tests /app/tests

CMD ["poetry", "run", "pytest"]
