FROM python:3.12.7-slim

WORKDIR /app

RUN pip install uv
COPY pyproject.toml pyproject.toml
RUN uv sync

COPY . .

CMD ["uv", "run", "gunicorn", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "backend.main:app", "--bind", "0.0.0.0:8000"]
