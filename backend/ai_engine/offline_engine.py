"""
Offline AI Engine - Uses local knowledge base/datasets for AI responses
"""

import logging
import os
import random
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class OfflineAIEngine:
    """
    Offline AI Engine that uses local knowledge base for AI responses.
    Designed to work without internet connection.
    
    The engine can load Q&A data from external datasets:
    1. SQLite: Table qa_data with columns (question answer category)
    2. JSON: Array of objects
    
    If no external datasets are found it uses the built-in fallback knowledge base.
    """
    
    def __init__(self,
                 model_path: str = "models/tinyllama-1.1b.gguf",
                 dataset_paths: List[str] = None):
        self.model_path = model_path
        self.dataset_paths = dataset_paths or [
            "data/rural_literacy.db",
            "data/qa_dataset.json", 
            "data/qa_dataset.csv"
        ]
        
        # Initialize data storage and fallback KB
        self.all_qa_data = []
        self.default_kb = {}
        
        # Try loading from datasets first then fallback to internal KB
        try:
            success = self._load_from_datasets()
            if not success or not self.all_qa_data:
                logger.warning("No external datasets loaded - using fallback")
                self.default_kb = self._get_fallback_knowledgebase()
                logger.info("Fallback knowledgebase loaded")
            
            if not self.default_kb:
                self.default_kb = self._get_fallback_knowledgebase()
                
        except Exception as e:
            logger.error(f"Error initializing offline engine: {e}")
    
    def _load_from_datasets(self) -> bool:
        import sqlite3
        import json
        
        loaded = False
        
        for path in self.dataset_paths:
            if not os.path.exists(path):
                continue
            
            ext = os.path.splitext(path)[1].lower()
            
            try:
                if ext in ['.db', '.sqlite']:
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    try:
                        cursor.execute("SELECT question, answer, category FROM qa_data")
                        rows = cursor.fetchall()
                        for row in rows:
                            self.all_qa_data.append({
                                "question": row[0],
                                "answer": row[1],
                                "category": row[2] if len(row) > 2 else "general"
                            })
                        loaded = True
                        logger.info(f"Loaded {len(rows)} QA pairs from SQLite {path}")
                    except sqlite3.OperationalError:
                        pass
                    conn.close()
                    
                elif ext == '.json':
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            self.all_qa_data.extend(data)
                            loaded = True
                            logger.info(f"Loaded {len(data)} QA pairs from JSON {path}")
                            
                elif ext == '.csv':
                    import csv
                    with open(path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            self.all_qa_data.append(row)
                        loaded = True
                        
            except Exception as e:
                logger.warning(f"Failed to load dataset {path}: {e}")
       
        return loaded
   
    def _get_fallback_knowledgebase(self) -> Dict[str, Any]:
        return {
            "education": {
                "keywords": ["education", "school", "study", "learn", "teacher", "student"],
                "response": "Education is key to empowerment. In India, free education is provided for children aged 6-14 years under Right to Education Act."
            },
            "literacy": {
                "keywords": ["literacy", "read", "writing"],
                "response": "Literacy is the ability to read and write. You can learn at any age through adult education programs."
            },
            "health": {
                "keywords": ["health", "hospital", "doctor", "medicine"],
                "response": "For health concerns, please consult your nearest government hospital. Many services are free."
            },
            "agriculture": {
                "keywords": ["farming", "crop", "farmer", "agriculture"],
                "response": "Farmers can benefit from PM-KISAN scheme providing Rs 6000 per year. Also check local agricultural offices."
            },
            "government": {
                "keywords": ["scheme", "government", "subsidy", "benefit"],
                "response": "There are many government schemes for rural citizens including PM-JAY health insurance, MNREGA jobs, Ayushman card."
            },
            "default": {
                "keywords": [],
                "response": "Thank you! Please ask about education, health, farming, government schemes, or any topic you would like to learn about."
            }
        }
   
    def generate_response(self, message: str, user_id: str) -> str:
        try:
            message_lower = message.lower()
            
            # First check external dataset matches
            for qa in self.all_qa_data:
                question_text = qa.get("question", "").lower()
                answer_text = qa.get("answer")
                
                # If keyword found, respond
                if any(kw in message_lower for kw in question_text.split()) and answer_text:
                    return answer_text
            
            # Then check fallback KB
            if self.default_kb:
                for category_name, data_item in self.default_kb.items():
                    kw_list = data_item.get("keywords", [])
                    for keyword in kw_list:
                        if keyword in message_lower:
                            return data_item.get("response", "")
                
                default_resp = self.default_kb.get("default", {}).get("response")
                if default_resp:
                    return default_resp
            
            return "I'm here to help! Please ask me about education, health, farming, government schemes, or any topic you'd like to know about."
            
        except Exception as e:
            logger.error(f"Error generating offline response: {e}")
            return "Sorry, I encountered an error while processing your request."
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the offline engine"""
        return {
            "model_type": "offline_kb",
            "mode": "offline",
            "qa_pairs": len(self.all_qa_data),
            "categories": list(self.default_kb.keys()) if self.default_kb else []
        }

