FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/root/.cache/huggingface

# Only what is needed for Python packages that may require compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip and install CPU-only PyTorch first
RUN pip install --upgrade pip && \
    pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install application dependencies
RUN pip install -r requirements.txt

# Copy application
COPY app ./app
COPY data ./data

# Do NOT download Hugging Face models during build.
# They will be downloaded once when the application starts.

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]