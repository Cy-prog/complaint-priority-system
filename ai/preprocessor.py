import re
import unicodedata

class Preprocessor:
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        # Normalize unicode
        text = unicodedata.normalize('NFKC', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        return text

    def normalize_text(self, text: str) -> str:
        if not text:
            return ""
        text = self.clean_text(text).lower()
        # Remove special characters but keep alphanumeric, basic punctuation, and numbers/durations
        text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
        return text

    def tokenize(self, text: str) -> list[str]:
        if not text:
            return []
        text = self.normalize_text(text)
        # Simple word tokenization using regex
        return re.findall(r'\b\w+\b', text)
