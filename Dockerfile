FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

COPY pyproject.toml ./
COPY data/data.csv data/data.csv

RUN uv sync --no-dev --no-install-project

COPY fitness_assistant .

RUN uv sync --no-dev

EXPOSE 5000

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
