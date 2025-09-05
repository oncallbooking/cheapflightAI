# multi-stage docker to include playwright browsers for worker if needed
FROM python:3.11-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    gnupg \
    ca-certificates \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxfixes3 \
    libx11-xcb1 \
    libgbm1 \
    libpangocairo-1.0-0 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
# simple pip install to avoid needing poetry in container
RUN pip install --no-cache-dir pip setuptools wheel
RUN pip install --no-cache-dir \
    fastapi uvicorn[standard] sqlalchemy asyncpg alembic \
    aiohttp beautifulsoup4 playwright pydantic redis aioredis \
    apscheduler tenacity python-dotenv python-multipart httpx \
    pytest pytest-asyncio

# Install Playwright browsers (for worker stage)
RUN playwright install --with-deps

COPY . /app

# Web target (smaller runtime)
FROM base as web
ENV PYTHONPATH=/app
EXPOSE ${PORT:-10000}
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "10000"]

# Worker target (has playwright ready)
FROM base as worker
ENV PYTHONPATH=/app
CMD ["python", "-m", "worker.runner"]
