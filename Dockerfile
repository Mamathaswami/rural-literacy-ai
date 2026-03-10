# Rural Literacy AI Tool - Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt/dependencies.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r dependencies.txt

# Install gunicorn for production
RUN pip install --no-cache-dir gunicorn

# Copy application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY data/ ./data/
COPY models/ ./models/

# Create necessary directories
RUN mkdir -p /app/data

# Expose ports
EXPOSE 8000 3001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run both backend and frontend
CMD python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 & \
    python frontend/server.py

