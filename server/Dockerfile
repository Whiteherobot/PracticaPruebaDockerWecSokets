# server/Dockerfile
FROM python:3.11-slim

# Variables para evitar buffers en logs
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copiar requirements y luego instalar
COPY app/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copiar app
COPY app /app

# Exponer puerto
EXPOSE 8000

# Comando por defecto: uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "asyncio" ]
