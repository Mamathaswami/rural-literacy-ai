"""
Online AI Engine - Smart Q&A System with comprehensive knowledge base
Works completely offline without needing any external AI models
"""

import logging
import re
import random
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class OnlineAIEngine:
    """
    Smart AI Engine with comprehensive Q&A knowledge base.
    Works without internet - provides intelligent responses like ChatGPT.
    """
    
    def __init__(self):
        self.model = None
        self.model_path = "models/tinyllama-1.1b.gguf"
        self._initialize_knowledge_base()
        logger.info("Smart AI Engine initialized with comprehensive knowledge base")
    
    def _initialize_knowledge_base(self):
        """Initialize comprehensive knowledge base with smart responses"""
        
        self.knowledge_base = {
            # Greetings
            "greetings": {
                "patterns": [r"\b(hi|hello|hey|greetings|namaste|namaskar|good morning|good evening)\b"],
                "responses": [
                    "Namaste! 🙏 How can I help you today? I'm here to answer any questions about education, health, farming, government schemes, technology, or anything else!",
                    "Hello! Welcome! 😊 I'm your AI assistant. Ask me anything - I'm happy to help with learning, health, agriculture, jobs, and more!",
                    "Hey there! 👋 Great to see you! What would you like to know today?"
                ]
            },
            
            # What is AI
            "what_is_ai": {
                "patterns": [r"\bwhat is (artificial intelligence|ai)\b", r"\bai( |)(what is|means)\b"],
                "responses": [
                    "Artificial Intelligence (AI) is like a smart computer program that can learn and make decisions! Just like humans learn from experiences, AI learns from data. It can answer questions, recognize pictures, translate languages, and much more! 🤖",
                    "AI stands for Artificial Intelligence - it's technology that makes computers smart! AI can understand what you ask, learn from information, and give helpful answers. It's like having a very knowledgeable friend available 24/7!"
                ]
            },
            
            # Education
            "education": {
                "patterns": [r"\b(education|school|studying|study|learn|teacher|student|class|college|university|exam|course)\b"],
                "responses": [
                    "📚 Education is incredibly powerful! Benefits include:\n\n• Opens career opportunities\n• Improves critical thinking\n• Enables financial independence\n• Empowers decision-making\n\nIn India, free education is available for ages 6-14 under RTE. Adults can learn through:\n• National Open School (NIOS)\n• Adult Education Centers\n• Online courses (many free!)\n\nWhat would you like to learn more about?",
                    "🎓 Learning never stops! Here's how to continue educating yourself:\n\nFor Students:\n• Focus on understanding, not just memorizing\n• Practice regularly\n• Use online resources like DIKSHA, SWAYAM\n\nFor Adults:\n• Adult education programs\n• Free online courses (Swayam, YouTube)\n• Library reading programs\n\nWhat subject interests you?"
                ]
            },
            
            # Literacy
            "literacy": {
                "patterns": [r"\b(literacy|literate|read|writing|illiterate|read write)\b"],
                "responses": [
                    "📖 Learning to read and write is life-changing! Here's how to start:\n\nStep 1: Learn the alphabet (A-Z)\nStep 2: Practice writing each letter\nStep 3: Start with simple words\nStep 4: Read simple books or newspapers\n\nGet help from:\n• Local adult education center\n• Learning apps (many free!)\n• Family or friends\n\nIt's never too late to learn! 💪"
                ]
            },
            
            # Math
            "math": {
                "patterns": [r"\b(math|mathematics|calculation|add|subtract|multiply|divide|percentage)\b"],
                "responses": [
                    "🔢 Math is everywhere in daily life!\n\nBasic Shortcuts:\n• Multiplication by 9: For 9×6, subtract 1 from 6 = 5, then 9-5=4 → 54!\n• Percentage: 20% of 50 = (20×50)/100 = 10\n\nPractical Uses:\n• Shopping discounts\n• Cooking measurements\n• Budget planning\n\nLearning Resources:\n• Khan Academy (free)\n• YouTube tutorials\n\nWhat math problem can I help you with?"
                ]
            },
            
            # Health
            "health": {
                "patterns": [r"\b(health|doctor|hospital|medicine|disease|illness|sick|treatment|fever|cough|cold|headache)\b"],
                "responses": [
                    "🏥 Health is wealth! Essential tips:\n\nDaily Habits:\n🥗 Eat fresh vegetables and fruits\n🥛 Drink 8 glasses of water daily\n😴 Sleep 7-8 hours\n🏃 Exercise 30 minutes daily\n🧼 Wash hands frequently\n\nWhen to See a Doctor:\n• Fever lasting more than 2 days\n• Severe headache\n• Difficulty breathing\n• Chest pain\n\nIs there a specific health concern I can help with?"
                ]
            },
            
            # Nutrition
            "nutrition": {
                "patterns": [r"\b(food|eat|nutrition|diet|vegetables|fruits|protein|vitamin|healthy|breakfast|lunch|dinner|water)\b"],
                "responses": [
                    "🥗 A balanced diet is key to good health!\n\nDaily Food Groups:\n🥬 Vegetables - vitamins & minerals\n🍎 Fruits - energy & vitamins\n🌾 Grains - energy & fiber\n🥚 Protein - eggs, dal, meat, nuts\n🥛 Dairy - milk, curd for calcium\n\nHealthy Tips:\n• Eat breakfast like a king\n• Eat lunch like a prince\n• Eat dinner like a pauper\n• Drink water between meals\n\nWhat would you like to cook or learn about?"
                ]
            },
            
            # Government Schemes
            "government_schemes": {
                "patterns": [r"\b(scheme|government|subsidy|benefit|welfare|pmay|pmjdy|jan dhan|ayushman)\b"],
                "responses": [
                    "🏛️ Important Government Schemes in India:\n\nHousing:\n• PMAY - Affordable housing\n\nBanking:\n• PMJDY - Free bank accounts\n• Sukanya Samriddhi - Girl child savings\n\nHealth:\n• Ayushman Bharat - Free health insurance up to ₹5 lakh\n\nChildren:\n• ICDS - Nutrition for children\n• Mid-Day Meal - Free lunch in schools\n\nWomen:\n• Beti Bachao Beti Padhao\n• PM Matru Vandana Yojana\n\nHow to Apply: Visit your nearest CSC or apply online!"
                ]
            },
            
            # Aadhaar
            "aadhaar": {
                "patterns": [r"\b(aadhaar|aadhar|uidai)\b"],
                "responses": [
                    "🪪 Aadhaar is India's 12-digit unique ID!\n\nWhy Important:\n• Required for bank accounts\n• Needed for government benefits\n• Mobile SIM verification\n• Direct benefits transfer\n\nHow to Get:\n1. Visit nearest Aadhaar Seva Kendra\n2. Carry ID proof (Voter ID, Passport)\n3. Provide address proof\n4. Get biometric done\n5. Receive Aadhaar within weeks\n\nEnrollment is FREE!"
                ]
            },
            
            # Agriculture
            "agriculture": {
                "patterns": [r"\b(farmer|farming|crop|agriculture|field|harvest|wheat|rice|paddy|vegetable|soil|fertilizer|seed)\b"],
                "responses": [
                    "🌾 Farming is India's backbone! Tips:\n\nModern Techniques:\n• Use high-quality seeds\n• Crop rotation\n• Drip irrigation to save water\n• Organic fertilizers\n\nGovernment Support:\n• PM-KISAN: ₹6000/year\n• Crop insurance schemes\n• Agricultural loans at low interest\n• Kisan Credit Cards\n\nSeasonal Crops:\nKharif: Rice, cotton, maize\nRabi: Wheat, chickpeas\n\nWhat crop information do you need?"
                ]
            },
            
            # Weather
            "weather": {
                "patterns": [r"\b(weather|rain|monsoon|forecast|storm|cold|hot|temperature|climate)\b"],
                "responses": [
                    "🌤️ Weather affects daily life!\n\nIndian Monsoon:\n• Southwest: June - September\n• Northeast: October - December\n\nSeasonal Advice:\nSummer: Stay hydrated, avoid noon sun\nMonsoon: Use umbrella, avoid flooded areas\nWinter: Wear warm clothes\n\nFarmer Tips:\n• Check forecast daily\n• Don't spray pesticides before rain\n\nCheck: mausam.imd.gov.in"
                ]
            },
            
            # Digital Technology
            "digital": {
                "patterns": [r"\b(phone|mobile|smartphone|internet|wifi|computer|laptop|digital|upi|payment|gpay|paytm|phonepe)\b"],
                "responses": [
                    "📱 Digital technology makes life easier!\n\nBasic Tips:\n• Make UPI payments via GPay/PhonePe\n• Video call to see family\n• Get government services online\n• Learn from YouTube\n\nUPI Setup:\n1. Download GPay/PhonePe/Paytm\n2. Link bank account\n3. Create UPI PIN\n4. Send money using phone number!\n\nStay Safe:\n• Don't share OTP\n• Don't click suspicious links\n\nWhat digital skill to learn?"
                ]
            },
            
            # Banking
            "banking": {
                "patterns": [r"\b(bank|account|money|balance|withdraw|deposit|atm|passbook|loan|credit|savings)\b"],
                "responses": [
                    "🏦 Banking essentials:\n\nAccount Types:\n• Savings Account - earns interest\n• Current Account - for business\n• Zero Balance - under PMJDY\n\nServices:\n• Deposit/withdraw money\n• Transfer (NEFT/RTGS/UPI)\n• Pay bills\n• Get loans\n\nHow to Open:\n1. Visit bank with ID proof\n2. Fill form\n3. Submit photo\n4. Initial deposit (can be ₹0!)\n\nNeed banking help?"
                ]
            },
            
            # Women & Children
            "women_children": {
                "patterns": [r"\b(women|girl|mother|pregnant|child|children|kids|baby|women safety|violence)\b"],
                "responses": [
                    "👩 Important Contacts:\n\nHelplines:\n• Women: 1091\n• Child: 1098\n• Police: 100\n• Emergency: 112\n\nWomen Schemes:\n• Beti Bachao Beti Padhao\n• PM Matru Vandana Yojana (₹5000)\n• Sukanya Samriddhi\n\nChild Care:\n• Vaccination crucial\n• Balanced diet\n• Education early\n\nFor Safety: Report violence immediately!"
                ]
            },
            
            # Jobs
            "jobs": {
                "patterns": [r"\b(job|work|employment|career|salary|unemployment|interview|resume|vacancy)\b"],
                "responses": [
                    "💼 Job Opportunities:\n\nGovernment Jobs:\n• UPSC - upsc.gov.in\n• SSC - ssc.nic.in\n• Bank jobs (IBPS)\n\nPrivate Jobs:\n• Naukri, Indeed, LinkedIn\n• Company websites\n\nSkills to Learn:\n• Digital skills\n• Communication\n• Basic English\n\nInterview Tips:\n1. Research company\n2. Dress formally\n3. Be confident\n4. Answer honestly\n\nWhat job are you looking for?"
                ]
            },
            
            # Skills
            "skills": {
                "patterns": [r"\b(skill|training|course|certificate|iti|diploma|vocational)\b"],
                "responses": [
                    "🎓 Skill Development:\n\nFree Government Courses:\n• ITI (Industrial Training Institute)\n• Skill India Mission\n• PMKVY\n\nOnline Free Courses:\n• SWAYAM (swayam.gov.in)\n• DIKSHA\n• YouTube tutorials\n\nPopular Skills:\n• Computer/IT\n• Accounting\n• Tailoring\n• Electrical work\n• Mobile repair\n\nWhat skill interests you?"
                ]
            },
            
            # Emergency
            "emergency": {
                "patterns": [r"\b(emergency|help|accident|fire|ambulance|disaster|danger)\b"],
                "responses": [
                    "🆘 Save These Numbers!\n\nPolice: 100\nAmbulance: 102 or 108\nFire: 101\nWomen Helpline: 1091\nChild Helpline: 1098\nGeneral Emergency: 112\n\nDuring Emergency:\n1. Stay calm\n2. Explain what happened\n3. Give exact location\n4. Don't hang up\n\nFirst Aid:\n• Burns: Cold water, no ice\n• Cuts: Clean, apply pressure\n• Fever: Paracetamol, rest\n\nStay safe!"
                ]
            },
            
            # Science
            "science": {
                "patterns": [r"\b(what is|how does|why) (science|electricity|water|air|earth|sun|moon|planet)\b"],
                "responses": [
                    "🔬 Great questions!\n\nElectricity: Flow of electrons through conductors. Used for lights, fans, phones!\n\nWater: H2O - two hydrogen atoms + one oxygen. Essential for life!\n\nAir: Mix of gases (78% nitrogen, 21% oxygen). We breathe it to live!\n\nSun: A star! Gives us light and heat. Earth goes around it!\n\nMoon: Earth's satellite. Reflects sun's light. Causes tides!\n\nWhat else to explain?"
                ]
            },
            
            # Default responses
            "default": {
                "patterns": [],
                "responses": [
                    "That's a great question! 😊 I'm here to help with information about:\n\n📚 Education & Learning\n🏥 Health & Nutrition\n🌾 Farming & Agriculture\n🏛️ Government Schemes\n📱 Digital Technology\n💼 Jobs & Skills\n👩 Women & Children\n🏦 Banking & Money\n\nJust ask me anything about these topics!",
                    "I understand you're asking about that! While I don't have specific information on that topic, I can help you with:\n\n• Education and learning\n• Health and wellness\n• Government benefits\n• Digital skills\n• Job opportunities\n• And much more!\n\nWhat would you like to know?",
                    "Thank you for your question! I'm continuously learning to serve you better. Currently, I can help with:\n\n📚 Schools, colleges, courses\n🏥 Health tips, nutrition\n🌾 Farming techniques\n🏛️ Government schemes\n📱 Phone and internet\n💼 Jobs and training\n\nPlease ask me about any of these topics!"
                ]
            }
        }
    
    def generate_response(self, message: str, user_id: str) -> str:
        """Generate a smart response based on the message"""
        try:
            message_lower = message.lower().strip()
            
            # Handle short greetings specifically
            if message_lower in ['hi', 'hii', 'hiii', 'hiiii', 'hello', 'hey', 'hi!', 'hiii!', 'hello!']:
                greetings = [
                    "Namaste! 🙏 How can I help you today? I'm here to answer questions about education, health, farming, government schemes, technology, and more!",
                    "Hello! 👋 Welcome! How can I assist you today? Ask me anything!",
                    "Namaste! 😊 I'm your AI assistant. Ask me about learning, health, jobs, farming, or any topic you're curious about!"
                ]
                return random.choice(greetings)
            
            # Check each category for matching patterns
            for category, data in self.knowledge_base.items():
                if category == "default":
                    continue
                    
                patterns = data.get("patterns", [])
                for pattern in patterns:
                    if re.search(pattern, message_lower, re.IGNORECASE):
                        responses = data.get("responses", [])
                        return random.choice(responses)
            
            # Return default response if no match
            default_responses = self.knowledge_base.get("default", {}).get("responses", [])
            return random.choice(default_responses)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Namaste! I'm here to help! Please ask me about education, health, farming, government schemes, or any topic you'd like to know about."
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the engine"""
        return {
            "model_type": "smart_qa",
            "mode": "offline_knowledge_base",
            "categories": list(self.knowledge_base.keys()),
            "capabilities": [
                "conversation", "information", "education", 
                "health", "agriculture", "government", "technology",
                "employment", "general_assistance"
            ]
        }
