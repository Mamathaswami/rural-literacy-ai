# Deployment Guide - Rural Literacy AI Tool

## Quick Deploy Options

### Option 1: Local Production Run
```bash
# Install production server
pip install gunicorn

# Run backend with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:8000

# Run frontend (separate terminal)
python frontend/server.py
```

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY data/ ./data/

# Expose ports
EXPOSE 8000 3001

# Run both servers
CMD python -m uvicorn backend.main:app --host 0.0.0.0:8000 & \
    python frontend/server.py
```

#### Build and Run
```bash
docker build -t rural-literacy-ai .
docker run -p 8000:8000 -p 3001:3001 rural-literacy-ai
```

### Option 3: Cloud Deployment (Render/Heroku/Railway)

**Required Environment Variables:**
- None required (uses SQLite for offline storage)

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:$PORT
```

### Option 4: Production with Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3001;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Production Checklist

- [ ] Update CORS settings in `backend/main.py` to restrict origins
- [ ] Set up PostgreSQL for production (optional)
- [ ] Configure logging
- [ ] Set up health checks
- [ ] Enable HTTPS/SSL

## Recommended: Render.com Free Deployment

1. Push code to GitHub
2. Create account on render.com
3. Create new Web Service
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:$PORT`
5. Deploy!

## Frontend-Only Alternative

For static hosting (Netlify/Vercel), update `frontend/index.html` to point directly to backend:

```javascript
// Change this line in frontend/index.html:
const API_BASE = "http://127.0.0.1:8000";

// To your production backend URL:
// const API_BASE = "https://your-backend-api.com";
```

