FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml README.md AGENTS.md ./
COPY scripts ./scripts
COPY skills ./skills
COPY schemas ./schemas
COPY templates ./templates
COPY configs ./configs
COPY deploy ./deploy

RUN pip install --upgrade pip \
    && pip install -e .

VOLUME ["/data/input", "/data/models", "/data/runs"]
ENTRYPOINT ["python", "deploy/worker.py"]
