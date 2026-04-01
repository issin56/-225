FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY config.yaml ./
RUN pip install --no-cache-dir .

CMD ["python", "-m", "kanekasegi.main", "--config", "config.yaml"]
