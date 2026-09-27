FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Download NLTK data
RUN python -c "import nltk; nltk.download('vader_lexicon', quiet=True)"

# Pre-train category classifier
RUN python -m ai.training.generate_synthetic && python -m ai.training.train_classifier

# Ensure data and logs directories exist
RUN mkdir -p data/chroma logs

# Default port if not supplied by cloud orchestrator (e.g. Render)
ENV PORT=8000
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/api/health || exit 1

# Start FastAPI application with dynamic port support
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

