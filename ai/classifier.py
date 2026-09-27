import re
import yaml
from pathlib import Path
import joblib

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import LinearSVC
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.pipeline import Pipeline
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

CONFIG_DIR = Path(__file__).parent.parent / "config"
MODEL_PATH = Path(__file__).parent / "models" / "category_classifier.joblib"

class CategoryClassifier:
    def __init__(self):
        self.categories = self._load_categories()
        self.model = None
        self.is_trained = False
        self._load_model()

    def _load_categories(self):
        try:
            with open(CONFIG_DIR / "categories.yaml", "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data.get("categories", [])
        except Exception:
            return []

    def _load_model(self):
        if SKLEARN_AVAILABLE and MODEL_PATH.exists():
            try:
                self.model = joblib.load(MODEL_PATH)
                self.is_trained = True
            except Exception:
                pass

    def train(self, texts: list[str], labels: list[str]):
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required for training.")
        
        base_svc = LinearSVC(C=1.0, random_state=42, class_weight='balanced', dual='auto')
        calibrated_clf = CalibratedClassifierCV(base_svc, cv=3)
        
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=8000, ngram_range=(1, 2), sublinear_tf=True)),
            ('clf', calibrated_clf)
        ])
        
        self.model.fit(texts, labels)
        self.is_trained = True
        
        MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)

    def predict(self, text: str) -> tuple[str, float]:
        if not text:
            return "Other", 0.0

        # Deterministic high-priority / safety checks override generic classifications
        text_lower = text.lower()
        if any(w in text_lower for w in ["hit and run", "hit-and-run", "hit a pedestrian", "escaped toward", "hit person", "fled the scene"]):
            return "Public Safety", 0.95
        if any(w in text_lower for w in ["टक्कर मारकर फरार", "हिट एंड रन", "पैदल यात्री को टक्कर"]):
            return "Public Safety", 0.95

        kw_cat, kw_conf = self._keyword_fallback(text)
        has_devanagari = any('\u0900' <= c <= '\u097F' for c in text)

        if self.is_trained and self.model:
            try:
                # If calibrated classifier supports predict_proba
                if hasattr(self.model, 'predict_proba'):
                    probs = self.model.predict_proba([text])[0]
                    classes = self.model.classes_
                    best_idx = probs.argmax()
                    pred = str(classes[best_idx])
                    confidence = float(probs[best_idx])
                else:
                    pred = str(self.model.predict([text])[0])
                    if hasattr(self.model.named_steps['clf'], 'decision_function'):
                        scores = self.model.decision_function([text])[0]
                        confidence = min(max(float(scores.max()) / 2.0, 0.2), 0.98)
                    else:
                        confidence = 0.80

                # If query is completely ambiguous with low model confidence and no keywords, fall back to "Other"
                if confidence < 0.30 and kw_cat == "Other":
                    return "Other", float(round(confidence, 4))

                # If model is adequately confident (>= 0.35 in a 14-class problem where base is 0.07), trust model
                if confidence >= 0.35:
                    return pred, float(round(confidence, 4))

                # If model says "Other" or confidence is very low but keywords caught a specific category
                if (pred == "Other" or confidence < 0.35) and kw_cat != "Other":
                    return kw_cat, max(kw_conf, 0.75)

                return pred, float(round(confidence, 4))
            except Exception:
                pass
                
        return kw_cat, kw_conf

    def predict_subcategory(self, text: str, category: str) -> str | None:
        text_lower = text.lower()
        if category == "Public Safety":
            if any(w in text_lower for w in ["hit and run", "hit-and-run", "hit a pedestrian", "escaped toward", "knocked down", "fled", "टक्कर", "फरार"]):
                return "Hit-and-Run"
            if any(w in text_lower for w in ["theft", "stolen", "snatch", "burglary", "robbery", "चोरी", "लूट", "डकैती"]):
                return "Theft/Robbery"
            if any(w in text_lower for w in ["fire", "smoke", "blaze", "आग", "आगजनी", "धुआं"]):
                return "Fire Emergency"
            if any(w in text_lower for w in ["weapon", "knife", "assault", "fight", "clash", "चाकू", "मारपीट", "हमला"]):
                return "Violent Incident"
            if any(w in text_lower for w in ["ambulance", "hospital emergency", "critical patient", "एंबुलेंस", "मरीज"]):
                return "Medical Emergency"
            if any(w in text_lower for w in ["accident", "collision", "crash", "हादसा", "दुर्घटना"]):
                return "Accident"
            return "General Safety"

        if category == "Roads":
            if any(w in text_lower for w in ["pothole", "crater", "गड्ढा", "गड्ढे"]):
                return "Pothole"
            if any(w in text_lower for w in ["divider", "डिवाइडर"]):
                return "Road Divider"
            if any(w in text_lower for w in ["broken", "crack", "उखड़", "टूटी सड़क"]):
                return "Broken Road"
            return "Road Maintenance"

        if category == "Water Supply":
            if any(w in text_lower for w in ["burst", "leak", "pipeline", "पाइपलाइन", "लीकेज"]):
                return "Pipeline Leakage"
            if any(w in text_lower for w in ["contaminated", "dirty", "smell", "गंदा पानी", "बदबूदार", "दूषित"]):
                return "Water Contamination"
            if any(w in text_lower for w in ["no water", "stopped", "band", "पानी नहीं"]):
                return "Supply Outage"
            return "General Supply"

        if category == "Electricity":
            if any(w in text_lower for w in ["live wire", "exposed wire", "dangling wire", "नंगा तार", "लटकता तार"]):
                return "Hazardous Wire"
            if any(w in text_lower for w in ["transformer", "spark", "blast", "ट्रांसफार्मर", "धमाका"]):
                return "Transformer Issue"
            if any(w in text_lower for w in ["blackout", "power cut", "outage", "बिजली गुल", "कटौती"]):
                return "Power Outage"
            return "Electrical Maintenance"

        if category == "Sanitation":
            if any(w in text_lower for w in ["manhole", "chamber", "मैनहोल", "चेंबर"]):
                return "Open Manhole"
            if any(w in text_lower for w in ["sewer", "gutter", "drain", "सीवर", "नाली", "नाला"]):
                return "Sewer Blockage"
            return "Sanitation"

        if category == "Garbage/Waste":
            if any(w in text_lower for w in ["dead animal", "carcass", "मृत पशु", "मवेशी"]):
                return "Dead Animal Removal"
            if any(w in text_lower for w in ["van", "vehicle", "door to door", "कचरा गाड़ी"]):
                return "Collection Irregularity"
            return "Garbage Clearance"

        if category == "Parks":
            if any(w in text_lower for w in ["swing", "slide", "झूला", "झूले"]):
                return "Playground Equipment"
            if any(w in text_lower for w in ["grass", "weed", "bush", "झाड़ियां", "घास"]):
                return "Horticulture Maintenance"
            return "Park Maintenance"

        return None

    def _keyword_fallback(self, text: str) -> tuple[str, float]:
        text_lower = text.lower()
        
        best_match = "Other"
        best_score = 0
        
        for category in self.categories:
            name = category.get("name", "Other")
            keywords = category.get("keywords", [])
            score = 0
            for kw in keywords:
                kw_l = kw.lower().strip()
                if not kw_l:
                    continue
                if any('\u0900' <= c <= '\u097F' for c in kw_l):
                    if kw_l in text_lower:
                        score += 1
                else:
                    if re.search(r'\b' + re.escape(kw_l) + r'\b', text_lower):
                        score += 1
            
            if score > best_score:
                best_score = score
                best_match = name
                
        confidence = min(0.50 + (best_score * 0.12), 0.88) if best_score > 0 else 0.35
        return best_match, round(confidence, 4)
