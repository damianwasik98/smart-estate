FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.6.10 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY uv.lock pyproject.toml README.md ./
COPY src ./src

RUN uv sync --frozen

EXPOSE 8000

ENTRYPOINT [ "uv", "run", "fastapi", "run", "/app/src/asari_automation_api/api/main.py" ]
