FROM python:3.12.6-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

RUN apt-get update -y \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY . /work/

RUN uv sync --frozen --compile-bytecode \
    && uv build

ENTRYPOINT ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
