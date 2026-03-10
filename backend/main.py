# backend/main.py

import sys
import os

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import logging

from ai_engine.hybrid_router import HybridAIRouter, Mode
from storage.database import OfflineDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Rural Literacy AI Tool")

# Get the project root directory
project_root = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(os.path.dirname(project_root), 'frontend')

# Serve static files from frontend
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
ai_router = HybridAIRouter()
db = OfflineDatabase()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    mode: Optional[str] = "auto"  # auto, offline, online
    language: Optional[str] = "en"  # en, hi, ta, te, bn, mr, gu, kn, ml


class ChatResponse(BaseModel):
    response: str
    mode: str
    synced: bool = False


class SyncRequest(BaseModel):
    force_sync: bool = False


# Routes
@app.get("/")
async def root():
    index_path = os.path.join(frontend_path, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "name": "Rural Literacy AI Tool",
        "version": "1.0.0",
        "status": "running",
        "connectivity": ai_router.check_connectivity()
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - handles both online and offline"""
    
    # Set mode
    if request.mode == "offline":
        ai_router.mode = Mode.OFFLINE
    elif request.mode == "online":
        ai_router.mode = Mode.ONLINE
    else:
        ai_router.mode = Mode.AUTO
    
    # Get AI response with language support
    result = ai_router.route_request(request.message, request.user_id, request.language or "en")
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error"))
    
    # Save to local database
    db.save_chat(
        user_id=request.user_id,
        message=request.message,
        response=result["response"],
        mode=result["mode"]
    )
    
    return ChatResponse(
        response=result["response"],
        mode=result["mode"],
        synced=False  # Will be synced when online
    )


@app.get("/history/{user_id}")
async def get_history(user_id: str, limit: int = 50):
    """Get user's chat history"""
    return db.get_chat_history(user_id, limit)


@app.post("/sync")
async def sync_data(request: SyncRequest):
    """Sync offline data when online"""
    
    if not ai_router.check_connectivity():
        return {
            "success": False,
            "message": "No internet connection",
            "pending_sync": len(db.get_unsynced_data())
        }
    
    # Get unsynced data
    unsynced = db.get_unsynced_data()
    
    if not unsynced:
        return {
            "success": True,
            "message": "Nothing to sync",
            "synced_count": 0
        }
    
    # Import sync manager
    from storage.sync_manager import SyncManager
    sync_manager = SyncManager(db)
    
    # Sync the data
    result = sync_manager.sync_chats(unsynced, force=request.force_sync)
    
    if result.get("success"):
        return {
            "success": True,
            "message": f"Successfully synced {result.get('synced_count', 0)} items",
            "synced_count": result.get("synced_count", 0)
        }
    else:
        return {
            "success": False,
            "message": result.get("message", "Sync failed"),
            "synced_count": 0,
            "pending_sync": len(unsynced)
        }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
