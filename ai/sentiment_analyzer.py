import nltk

try:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    SentimentIntensityAnalyzer = None

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    TextBlob = None

class SentimentAnalyzer:
    def __init__(self):
        self.vader = None
        self._init_vader()

    def _init_vader(self):
        if NLTK_AVAILABLE:
            try:
                # Need to download vader_lexicon on first use
                try:
                    nltk.data.find('sentiment/vader_lexicon.zip')
                except LookupError:
                    nltk.download('vader_lexicon', quiet=True)
                self.vader = SentimentIntensityAnalyzer()
            except Exception:
                pass

    def analyze(self, text: str) -> dict:
        if not text:
            return {
                "sentiment": "neutral",
                "polarity": 0.0,
                "subjectivity": 0.0,
                "emotional_intensity": 0.0
            }

        compound = 0.0
        subjectivity = 0.0
        
        scores = []
        
        if self.vader:
            vader_scores = self.vader.polarity_scores(text)
            compound = vader_scores['compound']
            scores.append(compound)
            
        if TEXTBLOB_AVAILABLE:
            blob = TextBlob(text)
            tb_polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            scores.append(tb_polarity)
            
        if scores:
            final_score = sum(scores) / len(scores)
        else:
            final_score = 0.0

        if final_score >= 0.05:
            sentiment = "positive"
        elif final_score > -0.05:
            sentiment = "neutral"
        elif final_score > -0.5:
            sentiment = "negative"
        else:
            sentiment = "very_negative"
            
        emotional_intensity = abs(final_score)

        return {
            "sentiment": sentiment,
            "polarity": final_score,
            "subjectivity": subjectivity,
            "emotional_intensity": emotional_intensity
        }
