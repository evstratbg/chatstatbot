# syntax=docker/dockerfile:experimental
FROM evstrat/chatstats-backend:python-base as builder

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-dev --no-interaction \
 && find /app/.venv \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' \+

# Stage 2 - Copy only necessary files to the runner stage
FROM python:3.8-slim

WORKDIR /app

COPY --from=builder /app /app
COPY . .

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]