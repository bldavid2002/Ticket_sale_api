FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim as runner

RUN useradd -m workeruser

USER workeruser
WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]