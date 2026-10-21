
FROM ghcr.io/astral-sh/uv:0.9.5 AS uvbin

FROM python:3.12-slim

COPY --from=uvbin /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first to maximize layer caching.
COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project

ENV PATH="/opt/venv/bin:$PATH"

RUN useradd --create-home --uid 10001 appuser

COPY app/ ./app/

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
