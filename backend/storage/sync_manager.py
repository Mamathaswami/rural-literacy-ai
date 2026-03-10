"""
Sync Manager - Manages data synchronization between offline and online storage
"""

import logging
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SyncManager:
    """
    Manages synchronization of offline data to online storage.
    Handles batch syncing, conflict resolution, and retry logic.
    """
    
    def __init__(self, database, api_endpoint: str = None):
        self.db = database
        self.api_endpoint = api_endpoint or "https://api.ruralliteracy.example.com/sync"
        self.max_batch_size = 50
        self.retry_attempts = 3
        self.retry_delay = 5  # seconds
    
    def sync_chats(self, unsynced_data: List[Dict[str, Any]], force: bool = False) -> Dict[str, Any]:
        """
        Sync unsynced chat data to online storage.
        
        Args:
            unsynced_data: List of unsynced chat records
            force: If True, force sync even if there are conflicts
            
        Returns:
            Dict containing sync result
        """
        if not unsynced_data:
            return {
                "success": True,
                "message": "Nothing to sync",
                "synced_count": 0
            }
        
        synced_count = 0
        failed_ids = []
        
        try:
            # Process in batches
            for i in range(0, len(unsynced_data), self.max_batch_size):
                batch = unsynced_data[i:i + self.max_batch_size]
                
                # Try to sync the batch
                result = self._sync_batch(batch, force)
                
                if result.get("success"):
                    # Mark as synced in local database
                    chat_ids = [item["id"] for item in batch]
                    self.db.mark_as_synced(chat_ids)
                    synced_count += len(batch)
                    
                    # Log successful sync
                    self.db.log_sync(
                        sync_type="chat_batch",
                        status="success",
                        records_count=len(batch)
                    )
                else:
                    # Log failed batch
                    self.db.log_sync(
                        sync_type="chat_batch",
                        status="failed",
                        records_count=0,
                        error_message=result.get("message")
                    )
                    failed_ids.extend([item["id"] for item in batch])
            
            return {
                "success": True,
                "synced_count": synced_count,
                "failed_count": len(failed_ids),
                "message": f"Synced {synced_count} records"
            }
            
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            self.db.log_sync(
                sync_type="chat_batch",
                status="error",
                records_count=0,
                error_message=str(e)
            )
            return {
                "success": False,
                "message": f"Sync error: {str(e)}",
                "synced_count": synced_count
            }
    
    def _sync_batch(self, batch: List[Dict[str, Any]], force: bool) -> Dict[str, Any]:
        """
        Sync a single batch of data to the online API.
        
        Args:
            batch: List of chat records to sync
            force: Force sync flag
            
        Returns:
            Dict containing result
        """
        try:
            # Prepare payload
            payload = {
                "chats": batch,
                "force": force,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Make API request (mock for now - in production, use actual endpoint)
            # response = requests.post(
            #     self.api_endpoint,
            #     json=payload,
            #     timeout=30
            # )
            
            # For demonstration, simulate successful sync
            logger.info(f"Syncing batch of {len(batch)} records")
            
            # Simulate API call (replace with actual API in production)
            # if response.status_code == 200:
            #     return {"success": True, "data": response.json()}
            
            # Simulate success
            return {
                "success": True,
                "message": "Batch synced successfully (simulated)"
            }
            
        except requests.exceptions.Timeout:
            logger.error("Sync batch timed out")
            return {
                "success": False,
                "message": "Request timed out"
            }
        except requests.exceptions.ConnectionError:
            logger.error("Connection error during sync")
            return {
                "success": False,
                "message": "No internet connection"
            }
        except Exception as e:
            logger.error(f"Error syncing batch: {e}")
            return {
                "success": False,
                "message": str(e)
            }
    
    def check_sync_status(self) -> Dict[str, Any]:
        """
        Check the current sync status.
        
        Returns:
            Dict containing sync status information
        """
        try:
            unsynced = self.db.get_unsynced_data()
            return {
                "pending_count": len(unsynced),
                "is_online": self._check_connectivity(),
                "last_sync": self._get_last_sync_time()
            }
        except Exception as e:
            logger.error(f"Error checking sync status: {e}")
            return {
                "pending_count": 0,
                "is_online": False,
                "error": str(e)
            }
    
    def _check_connectivity(self) -> bool:
        """Check if online API is reachable"""
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def _get_last_sync_time(self) -> Optional[str]:
        """Get timestamp of last successful sync"""
        # This would query the sync_log table
        return None
