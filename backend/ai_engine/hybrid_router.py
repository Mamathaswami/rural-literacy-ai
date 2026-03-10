"""
Hybrid AI Router - Routes requests between online and offline AI engines
"""

import sys
import os
import logging
from enum import Enum
from typing import Dict, Any, Optional
import requests

# Add backend directory to path for imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

logger = logging.getLogger(__name__)


class Mode(Enum):
    """AI Engine Mode"""
    AUTO = "auto"       # Automatically choose between online/offline
    OFFLINE = "offline" # Force offline mode
    ONLINE = "online"   # Force online mode


class HybridAIRouter:
    """
    Routes AI requests between online and offline engines based on connectivity and mode.
    """
    
    def __init__(self):
        self.mode = Mode.AUTO
        self.online_engine = None
        self.offline_engine = None
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize both online and offline engines"""
        try:
            from ai_engine.online_engine import OnlineAIEngine
            from ai_engine.offline_engine import OfflineAIEngine
            
            self.online_engine = OnlineAIEngine()
            self.offline_engine = OfflineAIEngine()
            logger.info("Both AI engines initialized successfully")
        except ImportError as e:
            logger.error(f"Failed to initialize AI engines: {e}")
    
    def check_connectivity(self) -> bool:
        """Check internet connectivity"""
        try:
            # Try to reach a known API endpoint
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def route_request(self, message: str, user_id: str, language: str = "en") -> Dict[str, Any]:
        """
        Route the request to appropriate AI engine based on mode and connectivity.
        
        Args:
            message: User's input message
            user_id: User identifier
            language: Language code for translation
            
        Returns:
            Dict containing response and metadata
        """
        # Determine which engine to use
        if self.mode == Mode.OFFLINE:
            logger.info(f"Mode is OFFLINE, using offline engine")
            return self._process_offline(message, user_id, language)
        elif self.mode == Mode.ONLINE:
            logger.info(f"Mode is ONLINE, using online engine")
            return self._process_online(message, user_id, language)
        else:  # AUTO mode
            if self.check_connectivity():
                logger.info(f"Mode is AUTO and connected, using online engine")
                return self._process_online(message, user_id, language)
            else:
                logger.info(f"Mode is AUTO and offline, using offline engine")
                return self._process_offline(message, user_id, language)
    
    def _process_online(self, message: str, user_id: str, language: str = "en") -> Dict[str, Any]:
        """Process request using online AI engine"""
        try:
            if self.online_engine is None:
                from ai_engine.online_engine import OnlineAIEngine
                self.online_engine = OnlineAIEngine()
            
            response = self.online_engine.generate_response(message, user_id)
            
            # Apply translation if needed
            if language != "en":
                try:
                    from ai_engine.translations import translate_response
                    response = translate_response(response, language)
                except Exception as e:
                    logger.warning(f"Translation failed: {e}")
            
            return {
                "success": True,
                "response": response,
                "mode": "online"
            }
        except Exception as e:
            logger.error(f"Online engine error: {e}")
            # Fall back to offline if online fails
            return self._process_offline(message, user_id, language)
    
    def _process_offline(self, message: str, user_id: str, language: str = "en") -> Dict[str, Any]:
        """Process request using offline AI engine"""
        try:
            if self.offline_engine is None:
                from ai_engine.offline_engine import OfflineAIEngine
                self.offline_engine = OfflineAIEngine()
            
            response = self.offline_engine.generate_response(message, user_id)
            
            # Apply translation if needed
            if language != "en":
                try:
                    from ai_engine.translations import translate_response
                    response = translate_response(response, language)
                except Exception as e:
                    logger.warning(f"Translation failed: {e}")
            
            return {
                "success": True,
                "response": response,
                "mode": "offline"
            }
        except Exception as e:
            logger.error(f"Offline engine error: {e}")
            return {
                "success": False,
                "error": f"Failed to generate response: {str(e)}",
                "mode": "offline"
            }
