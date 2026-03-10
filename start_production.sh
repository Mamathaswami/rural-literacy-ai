#!/bin/bash
# Production Start Script for Rural Literacy AI Tool

echo "Starting Rural Literacy AI Tool..."

# Set production environment
export PYTHONUNBUFFERED=1
export ENVIRONMENT=production

# Start backend with gunicorn (4 workers)
echo "Starting backend server..."
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:8000 --daemon

# Wait for backend to start
sleep 2

# Start frontend server
echo "Starting frontend server..."
python frontend/server.py

