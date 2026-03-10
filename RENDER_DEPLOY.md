# Deploy to Render.com - Step by Step

## Step 1: Create Render Account
1. Go to https://render.com
2. Click "Sign Up"
3. Choose "GitHub" to sign up (easiest)
4. Authorize Render to access your GitHub

## Step 2: Connect Repository
1. Once logged in, click "New +" button
2. Select "Web Service"
3. Search for your repository: `rural-literacy-ai`
4. Click "Connect"

## Step 3: Configure Deployment
Fill in these settings:

| Setting | Value |
|---------|-------|
| Name | `rural-literacy-ai` |
| Region | `Oregon` (or closest to you) |
| Branch | `main` |
| Runtime | `Python` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app --bind 0.0.0.0:$PORT` |

## Step 4: Select Free Tier
1. Under "Plan", select "Free"
2. Click "Create Web Service"

## Step 5: Wait for Deployment
- It will take 2-5 minutes to build
- You'll see logs in the console
- Once deployed, you'll get a URL like: `https://rural-literacy-ai.onrender.com`

## Step 6: Test Your App
- Backend API: `https://rural-literacy-ai.onrender.com/`
- Test with: `https://rural-literacy-ai.onrender.com/chat`

## Troubleshooting:
- If build fails, check the logs
- Make sure requirements.txt path is correct
- The free tier sleeps after 15 minutes of inactivity (wakes up on next request)

