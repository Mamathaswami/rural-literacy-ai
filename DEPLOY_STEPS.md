# Complete Render Deployment Guide

## Step 1: Create Render Account
1. Open browser → Go to https://render.com

2. Click **"Get Started"**
3. Choose **"GitHub"** button to sign up
4. Authorize Render to access your GitHub repositories

## Step 2: Connect Your Repository
1. After login, click **"New +"** (top right)
2. Select **"Web Service"**
3. In the search box, type: `rural-literacy-ai`
4. Click **"Connect"** on your repository

## Step 3: Configure the Service
Fill in these exact values:

| Field | Value |
|-------|-------|
| **Name** | `rural-literacy-ai` |
| **Region** | `Oregon` (or Singapore) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:$PORT` |

## Step 4: Select Free Plan
1. Scroll down to **"Plan"**
2. Select **"Free"** ($0/month)
3. Click **"Create Web Service"** button

## Step 5: Wait for Deployment
- **Build time**: 3-5 minutes
- Watch the logs (they scroll automatically)
- Look for: `INFO: Application startup complete`

## Step 6: Get Your URL
- Once deployed, you'll see a URL like:
  `https://rural-literacy-ai.onrender.com`
- **Click it to test!**

## Troubleshooting

### Build Fails?
- Check the log for errors
- Common fix: Make sure `requirements.txt` exists

### App Won't Start?
- Verify Start Command is exactly as shown above
- Check that `backend/main.py` exists

### App Loads but Chat Doesn't Work?
- Wait 30 seconds for the free instance to "wake up"
- The first request takes time on free tier

### Still Stuck?
- Check Render status: https://status.render.com
- Free tier sleeps after 15 min of inactivity

