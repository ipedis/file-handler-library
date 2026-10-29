FROM python:3.11.18-slim-trixie@sha256:ffe4b0c76963e64f05484d74dbb3f67fad1effcf3c5c22c2235f0fafc8a9c98f

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv

# Keep the virtualenv outside /app: docker-compose bind-mounts the project over /app.
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONPATH=/app

WORKDIR /app

# Install the locked dependencies first to benefit from layer caching
COPY pyproject.toml uv.lock README.md /app/
RUN uv sync --locked --no-install-project

COPY . /app
COPY demo/.env /app/.env
RUN uv sync --locked

RUN useradd --create-home --uid 1000 app && chown -R app:app /app /opt/venv
USER app

ENTRYPOINT ["/opt/venv/bin/python", "demo/main.py"]
