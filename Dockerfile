FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir poetry==2.3.4 && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi

ENV PYTHONPATH=/app/src

CMD ["/bin/sh", "-c", "uvicorn myvelocity_ai_chatbot.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
