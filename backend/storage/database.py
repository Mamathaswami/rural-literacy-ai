"""
Offline Database - SQLite-based local storage for chat data
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class OfflineDatabase:
    """
    SQLite-based offline database for storing chat history and user data.
    Designed for rural areas with limited connectivity.
    """
    
    def __init__(self, db_path: str = "data/rural_literacy.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists"""
        import os
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def _init_database(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create chats table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    synced INTEGER DEFAULT 0
                )
            """)
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    name TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    last_active DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create sync_log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sync_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    records_count INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    error_message TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info(f"Database initialized at {self.db_path}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def save_chat(self, user_id: str, message: str, response: str, mode: str) -> int:
        """
        Save a chat message to the database.
        
        Args:
            user_id: User identifier
            message: User's message
            response: AI's response
            mode: Mode used (online/offline)
            
        Returns:
            ID of the inserted record
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO chats (user_id, message, response, mode, synced)
                VALUES (?, ?, ?, ?, 0)
            """, (user_id, message, response, mode))
            
            chat_id = cursor.lastrowid
            
            # Update user's last active time
            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, last_active)
                VALUES (?, CURRENT_TIMESTAMP)
            """, (user_id,))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Chat saved for user {user_id}, chat_id: {chat_id}")
            return chat_id
            
        except Exception as e:
            logger.error(f"Failed to save chat: {e}")
            raise
    
    def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get chat history for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of records to return
            
        Returns:
            List of chat records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, user_id, message, response, mode, timestamp, synced
                FROM chats
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            chats = [dict(row) for row in rows]
            logger.info(f"Retrieved {len(chats)} chats for user {user_id}")
            return chats
            
        except Exception as e:
            logger.error(f"Failed to get chat history: {e}")
            return []
    
    def get_unsynced_data(self) -> List[Dict[str, Any]]:
        """
        Get all unsynced chat data.
        
        Returns:
            List of unsynced chat records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, user_id, message, response, mode, timestamp
                FROM chats
                WHERE synced = 0
                ORDER BY timestamp ASC
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            unsynced = [dict(row) for row in rows]
            logger.info(f"Found {len(unsynced)} unsynced records")
            return unsynced
            
        except Exception as e:
            logger.error(f"Failed to get unsynced data: {e}")
            return []
    
    def mark_as_synced(self, chat_ids: List[int]) -> bool:
        """
        Mark chats as synced.
        
        Args:
            chat_ids: List of chat IDs to mark as synced
            
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            placeholders = ','.join('?' * len(chat_ids))
            cursor.execute(f"""
                UPDATE chats
                SET synced = 1
                WHERE id IN ({placeholders})
            """, chat_ids)
            
            conn.commit()
            conn.close()
            
            logger.info(f"Marked {len(chat_ids)} chats as synced")
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark as synced: {e}")
            return False
    
    def log_sync(self, sync_type: str, status: str, records_count: int = 0, error_message: str = None):
        """Log sync operation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO sync_log (sync_type, status, records_count, error_message)
                VALUES (?, ?, ?, ?)
            """, (sync_type, status, records_count, error_message))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to log sync: {e}")
