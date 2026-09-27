import re

try:
    from langdetect import detect, LangDetectException
except ImportError:
    detect = None
    LangDetectException = Exception

class LanguageDetector:
    def detect_language(self, text: str) -> str:
        if not text or len(text.strip()) < 5:
            return 'en'
            
        if not detect:
            return 'en'

        try:
            detected = detect(text)
            
            if detected == 'hi':
                # Heuristic for Hinglish
                english_words = re.findall(r'[a-zA-Z]+', text)
                if len(english_words) > len(text.split()) * 0.3:
                    return 'hinglish'
            return detected
        except LangDetectException:
            return 'en'
        except Exception:
            return 'en'
