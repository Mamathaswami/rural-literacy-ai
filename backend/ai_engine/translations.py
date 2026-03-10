"""
Multilingual Translation Module for Rural Literacy AI Tool
Provides translations for responses in multiple Indian languages
"""

# Dictionary of translations for key responses
TRANSLATIONS = {
    # Greetings
    "greetings": {
        "hi": ["नमस्ते! 🙏 मैं आज आपकी कैसे मदद कर सकता हूं?", "हेलो! स्वागत है! 😊 मैं आपका AI सहायक हूं।"],
        "ta": ["வணக்கம்! 🙏 இன்று நான் உங்களுக்கு எப்படி உதவி செய்ய முடியும்?", "வரவேற்கிறோம்! 😊"],
        "te": ["నమస్కారం! 🙏 ఈరోజు నేను మీకు ఎలా సహాయం చేయగలను?", "స్వాగతం! 😊"],
        "bn": ["নমস্কার! 🙏 আমি আজ আপনাকে কীভাবে সাহায্য করতে পারি?", "স্বাগতম! 😊"],
        "mr": ["नमस्कार! 🙏 मी आज तुम्हाला कशी मदत करू शकतो?", "स्वागत आहे! 😊"],
        "gu": ["નમસ્તે! 🙏 આજે હું તમને કેવી રીતે મદદ કરી શકું?", "સ્વાગત છે! 😊"],
        "kn": ["ನಮಸ್ಕಾರ! 🙏 ಇಂದು ನಾನು ನಿಮಗೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು?", "ಸ್ವಾಗತ! 😊"],
        "ml": ["നമസ്കാരം! 🙏 ഞാന്‍ ഇന്ന് നിങ്ങള്‍ക്ക് എങ്ങനെ സഹായിക്കാന്‍ കഴിയും?", "സ്വാഗതം! 😊"]
    },
    
    # Education
    "education": {
        "hi": ["📚 शिक्षा अत्यंत शक्तिशाली है! भारत में 6-14 वर्ष के बच्चों के लिए निःशुल्क शिक्षा उपलब्ध है। वयस्क शिक्षा केंद्रों से सीख सकते हैं।"],
        "ta": ["📚 கல்வி மிகவும் சக்திவாய்ந்தது! இந்தியாவில் 6-14 வயது குழந்தைகளுக்கு இலவச கல்வி கிடைக்கிறது."],
        "te": ["📚 చదువు చాలా శక్తివంతం! భారతదేశంలో 6-14 سِن_objects బిడ్డలకు ఉచిత शिक्षा"],
        "bn": ["📚 শিক্ষা অত্যন্ত শক্তিশালী! ভারতে 6-14 বছর বয়সী শিশুদের জন্য বিনামূল্যে শিক্ষা পাওয়া যায়।"],
        "mr": ["📚 शिक्षा खूप शक्तिशाली आहे! भारतात 6-14 वर्षे वयाच्या मुलांसाठी मोफत शिक्षण उपलब्ध आहे."],
        "gu": ["📚 શિક્ષા ખૂબ શક્તિશાળી છે! ભારતમાં 6-14 વર્ષના બાળકોને મફત શિક્ષા મળે છે."],
        "kn": ["📚 ಶಿಕ್ಷಣವು ಬಹಳ ಶಕ್ತಿಶಾಲಿಯಾಗಿದೆ! ಭಾರತದಲ್ಲಿ 6-14 ವರ್ಷ ವಯಸ್ಸಿನ ಮಕ್ಕಳಿಗೆ ಉಚಿತ ಶಿಕ್ಷಣ ಲಭ್ಯವಿದೆ."],
        "ml": ["📚 വിദ്യാഭ്യാസം വളരെ ശക്തിയേറിയതാണ്! ഇന്ത്യയില്‍ 6-14 വയസ്സിനുള്ള കുട്ടികള്‍ക്ക് സൗജന്യ വിദ്യാഭ്യാസം ലഭ്യമാണ്."]
    },
    
    # Health
    "health": {
        "hi": ["🏥 स्वास्थ्य ही संपत्ति है! प्रतिदिन 8 गिलास पानी पिएं, 7-8 घंटे सोएं, और ताजा सब्जियां खाएं।"],
        "ta": ["🏥 ஆரோக்கியம் செல்வம்! தினமும் 8 டம்ப்ளர் தண்ணீர் குடியுங்கள், 7-8 மணி நேரம் uykusu."],
        "te": ["🏥 ఆరోగ్యం ధనం! रोज़ 8 గlasses waterతెలుగు, 7-8 గंटेల uykusu."],
        "bn": ["🏥 স্বাস্থ্য হলো সম্পদ! প্রতিদিন ৮ গ্লাস পানি পান করুন এবং ৭-৮ ঘণ্টা ঘুমান।"],
        "mr": ["🏥 आरोग्य हे धन आहे! दररोज 8 ग्लास पाणी प्या, 7-8 तास झोपा घे."],
        "gu": ["🏥 સ્વાસ્થ્ય એ સંપત્તિ છે! દરરોજ 8 ગ્લાસ પાણી પીઓ, 7-8 કલાક સૂઈ જાઓ."],
        "kn": ["🏥 ಆರೋಗ್ಯವು ಸಂಪತ್ತಾಗಿದೆ! ಪ್ರತಿದಿನ 8 ಗ್ಲಾಸ್ ನೀರು ಕುಡಿಯಿರಿ, 7-8 ಗಂಟೆ ನಿದ್ರಿಸಿ."],
        "ml": ["🏥 ആരോഗ്യമാണ് സമ്പത്ത്! ദിവസവും 8 ഗ്ലാസ് വെള്ളം കുടിക്കുക, 7-8 മണിക്കൂറ്റ്  uykusu."]
    },
    
    # Agriculture
    "agriculture": {
        "hi": ["🌾 खेती भारत की रीढ़ है! PM-KISAN योजना से किसानों को ₹6000/वर्ष मिलते हैं।"],
        "ta": ["🌾 விவசாயம் இந்தியாவின் முதுகெலும்பு! PM-KISAN திட்டத்தின் கீழ் விவசாயிகளுக்கு ஆண்டுக்கு ₹6000 கிடைக்கிறது."],
        "te": ["🌾 telugu భారతదేశం వెనుకబడి tractor!"],
        "bn": ["🌾 কৃষি ভারতের মেরুদণ্ড! PM-KISAN প্রকল্পের অধীনে কৃষকরা বছরে ₹6000 পান।"],
        "mr": ["🌾 शेती भारताची रीड आहे! PM-KISAN योजनेअंतर्गत शेतकऱ्यांना वर्षाला ₹6000 मिळतात."],
        "gu": ["🌾 ખેતી ભારતની રીઢ છે! PM-KISAN યોજના હેઠળ ખેતરોને વર્ષે ₹6000 મળે છે."],
        "kn": ["🌾 ಕೃಷಿ ಭಾರತದ ಬೆನ್ನೆಲು! PM-KISAN ಯೋಜನೆಯ ಅಡಿಯಲ್ಲಿ ರೈತರಿಗೆ ವರ್ಷಕ್ಕೆ ₹6000 ಸಿಗುತ್ತದೆ."],
        "ml": ["🌾 കാര്‍ഷികം ഇന്ത്യയുടെ അടിസ്ഥാനമാണ്! PM-KISAN പദ്ധതിയില്‍ കര്‍ഷകര്‍ക്ക് വര്‍ഷത്തില്‍ ₹6000 ലഭിക്കും."]
    },
    
    # Government Schemes
    "government_schemes": {
        "hi": ["🏛️ भारत सरकार की प्रमुख योजनाएं: आयुष्मान भारत (₹5 लाख तक मुफ्त इलाज), PMAY (सस्ता घर), PMJDY (मुफ्त बैंक खाते)।"],
        "ta": ["🏛️ முக்கிய அரசு திட்டங்கள்: ஆயுஷ்மான் பாரத் (₹5 லட்சம் வரை இலவச சிகிச்சை), PMAY (மலிவு வீடு), PMJDY (இலவச வங்கி கணக்கு)."],
        "te": ["🏛️ प्रमुख Government Schemes: Ayushman Bharat (₹5 లక్షలు), PMAY, PMJDY."],
        "bn": ["🏛️ গুরুত্বপূর্ণ সরকারি প্রকল্প: আয়ুষ্মান ভারত (৫ লক্ষ টাকা পর্যন্ত বিনামূল্যে চিকিৎসা), PMAY, PMJDY।"],
        "mr": ["🏛️ महत्वाच्या सरकारी योजना: आयुष्मान भारत (₹5 लाखांपर्यंत मोफत उपचार), PMAY, PMJDY."],
        "gu": ["🏛️ મહત્વની સરકારી યોજનાઓ: આયુષ્માન ભારત (₹5 લાખ સુધી), PMAY, PMJDY."],
        "kn": ["🏛️ ಮುಖ್ಯ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು: ಆಯುಷ್ಮಾನ್ ಭಾರತ (₹5 ಲಕ್ಷ), PMAY, PMJDY."],
        "ml": ["🏛️ പ്രധാന സര്‍ക്കാര്‍ പദ്ധതികള്‍: ആയുഷ്മാന്‍ ഭാരത് (₹5 ലക്ഷം വരെ), PMAY, PMJDY."]
    },
    
    # Digital
    "digital": {
        "hi": ["📱 डिजिटल तकनीक जीवन को आसान बनाती है! GPay/PhonePe से UPI पेमेंट करें। OTP किसी को न दें।"],
        "ta": ["📱 டிஜிடல் தொழில்நுட்பம் வாழ்க்கைக்கு எளிதாக்குகிறது! GPay/PhonePe மூலம் UPI பணம் அனுப்பவும்."],
        "te": ["📱 Digital technology life ni aisayam chestundi! GPay/PhonePe lo UPI payments."],
        "bn": ["📱 ডিজিটাল প্রযুক্তি জীবনকে সহজ করে! GPay/PhonePe দিয়ে UPI পেমেন্ট করুন।"],
        "mr": ["📱 डिजिटल तंत्रज्ञान जीवन सोपे करते! GPay/PhonePe ने UPI पेमेंट करा."],
        "gu": ["📱 ડિજિટલ ટેકનોલોજી જીવનને સરળ બનાવે છે! GPay/PhonePe થી UPI પેમેન્ટ કરો."],
        "kn": ["📱 ಡಿಜಿಟಲ್ ತಂತ್ರಜ್ಞಾನವು ಜೀವನವನ್ನು ಸುಲಭಗೊಳಿಸುತ್ತದೆ! GPay/PhonePe ನಿಂದ UPI ಪಾವತಿ ಮಾಡಿ."],
        "ml": ["📱 ഡിജിറ്റല്‍ ടെക്നോളജി ജീവിതത്തെ എളുപ്പമാക്കുന്നു! GPay/PhonePe വഴി UPI പേമെന്റ് ചെയ്യുക."]
    },
    
    # Emergency
    "emergency": {
        "hi": ["🆘 आपातकालीन नंबर: पुलिस 100, एम्बुलेंस 102/108, महिला हेल्पलाइन 1091, बाल हेल्पलाइन 1098।"],
        "ta": ["🆘 அவசர எண்கள்: போலீஸ் 100, ஆம்புலன்ஸ் 102/108, பெண்கள் உதவி எண் 1091."],
        "te": ["🆘 Emergency numbers: Police 100, Ambulance 102/108, Women Helpline 1091."],
        "bn": ["🆘 জরুরি নম্বর: পুলিশ ১০০, অ্যাম্বুলেন্স ১০২/১০৮, মহিলা হেল্পলাইন ১০৯১।"],
        "mr": ["🆘 आणीबाणी क्रमांक: पोलिस 100, रुग्णवाहिका 102/108, महिला हेल्पलाईन 1091."],
        "gu": ["🆘 અસરકારક નંબરો: પોલીસ 100, એમ્બ્યુલંસ 102/108, મહિલા હેલ્પલાઈન 1091."],
        "kn": ["🆘 ತುರ್ತು ಸಂಖ್ಯೆಗಳು: ಪೊಲೀಸ್ 100, ಆಂಬುಲೆನ್ಸ್ 102/108, ಮಹಿಳಾ ಹೆಲ್ಪ್‌ಲೈನ್ 1091."],
        "ml": ["🆘 അടിയന്തര നമ്പറുകള്‍: പോലീസ് 100, ആംബുലന്‍സ് 102/108, വനിതാ ഹെല്‍പ് ലൈന്‍ 1091."]
    },
    
    # Default
    "default": {
        "hi": ["मैं शिक्षा, स्वास्थ्य, खेती, सरकारी योजनाओं, डिजिटल कौशल, नौकरी और अन्य विषयों में मदद कर सकता हूं।"],
        "ta": ["நான் கல்வி, ஆரோக்கியம், விவசாயம், அரசு திட்டங்கள், டிஜிடல் திறமைகள், வேலைவாய்ப்பு ஆகியவற்றில் உதவ முடியும்."],
        "te": ["నేను విద్య, ఆరోగ్యం, వ్యవసాయం, Government Schemes, Digital Skills, Jobs లో help cheyyali."],
        "bn": ["আমি শিক্ষা, স্বাস্থ্য, কৃষি, সরকারি প্রকল্প, ডিজিটাল দক্ষতা, চাকরি ইত্যাদিতে সাহায্য করতে পারি।"],
        "mr": ["मी शिक्षा, आरोग्य, शेती, सरकारी योजना, डिजिटल स्किल्स, नोकरी यात मदत करू शकतो."],
        "gu": ["હું શિક્ષા, સ્વાસ્થ્ય, ખેતી, સરકારી યોજનાઓ, ડિજિટલ સ્કિલ્સ, નોકરી વગેરેમાં મદદ કરી શકું."],
        "kn": ["ನಾನು ಶಿಕ್ಷಣ, ಆರೋಗ್ಯ, ಕೃಷಿ, ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು, ಡಿಜಿಟಲ್ ಕೌಶಲ್ಯಗಳು, ಉದ್ಯೋಗ ಇತ್ಯಾದಿಗಳಲ್ಲಿ ಸಹಾಯ ಮಾಡಬಹುದು."],
        "ml": ["ഞാന്‍ വിദ്യാഭ്യാസം, ആരോഗ്യം, കാര്‍ഷികം, സര്‍ക്കാര്‍ പദ്ധതികള്‍, ഡിജിറ്റല്‍ കഴിവുകള്‍, ജോലി എന്നിവയില്‍ സഹായിക്കാന്‍ കഴിയും."]
    }
}


def translate_response(text: str, target_language: str) -> str:
    """
    Translate response to target language if translation exists
    
    Args:
        text: Original English text
        target_language: Target language code (hi, ta, te, bn, mr, gu, kn, ml)
        
    Returns:
        Translated text or original if no translation available
    """
    if target_language == "en":
        return text
    
    # Check if we have translations for this category
    for category, translations in TRANSLATIONS.items():
        if target_language in translations:
            # Check if any key phrase from the original text matches
            for key_phrase in get_key_phrases(category):
                if key_phrase.lower() in text.lower():
                    # Return a random translation for this category
                    lang_translations = translations[target_language]
                    return lang_translations[len(lang_translations) % len(lang_translations)]
    
    # Return a default translation if we have one
    if "default" in TRANSLATIONS and target_language in TRANSLATIONS["default"]:
        return TRANSLATIONS["default"][target_language]
    
    return text


def get_key_phrases(category: str) -> list:
    """Get key phrases for a category to match against"""
    phrases = {
        "greetings": ["namaste", "hello", "hi", "hey", "welcome"],
        "education": ["education", "school", "study", "learn", "teacher", "student"],
        "health": ["health", "doctor", "hospital", "medicine", "disease"],
        "agriculture": ["farmer", "farming", "crop", "agriculture", "pm-kisan"],
        "government_schemes": ["scheme", "government", "subsidy", "benefit", "ayushman", "pmay", "pmjdy"],
        "digital": ["phone", "mobile", "digital", "upi", "gpay", "payment"],
        "emergency": ["emergency", "help", "ambulance", "police", "danger"],
        "default": ["ask", "question", "help"]
    }
    return phrases.get(category, [])


def get_language_name(lang_code: str) -> str:
    """Get full language name from code"""
    names = {
        "en": "English",
        "hi": "हिंदी (Hindi)",
        "ta": "தமிழ் (Tamil)",
        "te": "తెలుగు (Telugu)",
        "bn": "বাংলা (Bengali)",
        "mr": "मराठी (Marathi)",
        "gu": "ગુજરાતી (Gujarati)",
        "kn": "ಕನ್ನಡ (Kannada)",
        "ml": "മലയാളം (Malayalam)"
    }
    return names.get(lang_code, "English")

