# Build stage
FROM python:3.11-slim as builder

WORKDIR /src

# Prevent Python from writing .pyc files and enable buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user for security
RUN groupadd -r mlopps && useradd -r -g mlopps mlopps
RUN mkdir -p logs && chown -R mlopps:mlopps /app

# Copy dependencies from builder
COPY --from=builder /root/.local /home/mlopps/.local
ENV PATH=/home/mlopps/.local/bin:$PATH

# Copy application code
COPY . .
RUN chown -R mlopps:mlopps /app

USER mlopps

# Environment variables
ENV PYTHONPATH=/app
ENV APP_NAME=LLM-Production-Pipeline
ENV PORT=8000

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Optimization: Use gunicorn with uvicorn workers for production-grade scaling
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]
