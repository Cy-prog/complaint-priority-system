import time
import yaml
from pathlib import Path
from .schemas import AnalysisResult
from .preprocessor import Preprocessor
from .language_detector import LanguageDetector
from .classifier import CategoryClassifier
from .entity_extractor import EntityExtractor
from .sentiment_analyzer import SentimentAnalyzer
from .priority_engine import PriorityEngine
from .rule_engine import RuleEngine
from .explainer import Explainer
from .confidence import ConfidenceEstimator
from .embedding_service import EmbeddingService
from .similarity_service import SimilarityService

CONFIG_DIR = Path(__file__).parent.parent / "config"
DATA_DIR = Path(__file__).parent.parent / "data"

class ComplaintAnalysisPipeline:
    def __init__(self):
        # 1-3. Preprocessing & Language
        self.preprocessor = Preprocessor()
        self.language_detector = LanguageDetector()
        
        # 4-5. Classification
        self.classifier = CategoryClassifier()
        
        # 6. Entity Extraction
        self.entity_extractor = EntityExtractor()
        
        # 7. Sentiment Analysis
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # 8-14. Priority Engine
        self.priority_engine = PriorityEngine()
        
        # 15. Safety Escalation Rules
        self.rule_engine = RuleEngine()
        
        # 16. Duplicate & Similar Incident Detection
        self.embedding_service = EmbeddingService()
        persist_dir = str(DATA_DIR / "chroma")
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.similarity_service = SimilarityService(self.embedding_service, persist_dir)
        
        # 17. Confidence Estimation
        self.confidence_estimator = ConfidenceEstimator()
        
        # 18. Explainability
        self.explainer = Explainer()
        
        self.categories_meta = self._load_categories_meta()

    def _load_categories_meta(self):
        try:
            with open(CONFIG_DIR / "categories.yaml", "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                cats = data.get("categories", [])
                return {c.get("name"): c for c in cats}
        except Exception:
            return {}

    def analyze(self, complaint_text: str, complaint_id: int | None = None) -> AnalysisResult:
        """
        Executes the full 19-step Hybrid AI Pipeline.
        """
        start_time = time.time()
        
        # Step 1: Text preprocessing
        cleaned_text = self.preprocessor.clean_text(complaint_text)
        if not cleaned_text:
            cleaned_text = "General civic grievance"

        try:
            # Step 2: Language detection
            lang = self.language_detector.detect_language(cleaned_text)
            
            # Step 3: Normalization (handled in preprocessor)
            
            # Step 4: Category classification (ML TF-IDF + LinearSVC with fallback)
            category, clf_confidence = self.classifier.predict(cleaned_text)
            cat_meta = self.categories_meta.get(category, {})
            risk_level = cat_meta.get("risk_level", "medium")
            is_essential = cat_meta.get("is_essential_service", False)
            
            # Step 5: Subcategory classification
            subcategory = self.classifier.predict_subcategory(cleaned_text, category)
            
            # Step 6: Entity extraction (location, landmarks, duration, vehicle, time, direction, injury, etc.)
            entities = self.entity_extractor.extract(cleaned_text)
            
            # Step 7: Sentiment analysis
            sentiment_res = self.sentiment_analyzer.analyze(cleaned_text)
            
            # Steps 8-14: Estimation of severity, public-impact, safety-risk, service-disruption,
            # duration, vulnerable groups, and priority score calculation
            signals = {
                "category": category,
                "category_risk_level": risk_level,
                "is_essential_service": is_essential,
                "entities": entities,
                "sentiment": sentiment_res,
                "text_length": len(cleaned_text),
                "classifier_confidence": clf_confidence
            }
            p_res = self.priority_engine.calculate_priority(signals)
            
            # Step 15: Safety escalation rules (Hard safety triggers override priority)
            analysis_dict = {
                "priority": p_res["priority"],
                "safety_score": p_res["safety_score"],
                "entities": entities,
                "is_essential_service": is_essential,
                "category": category,
                "category_risk_level": risk_level
            }
            analysis_dict = self.rule_engine.apply_rules(analysis_dict)
            final_priority = analysis_dict["priority"]
            final_priority_score = p_res["priority_score"]
            
            # Ensure priority score reflects escalations
            if final_priority == "CRITICAL" and final_priority_score < 75:
                final_priority_score = max(final_priority_score, 85)
            elif final_priority == "HIGH" and final_priority_score < 55:
                final_priority_score = max(final_priority_score, 65)
            elif final_priority == "MEDIUM" and final_priority_score < 35:
                final_priority_score = max(final_priority_score, 45)
                
            # If safety escalated to CRITICAL, ensure risk level reflects it
            if final_priority == "CRITICAL":
                risk_level = "critical"
            elif final_priority == "HIGH" and risk_level == "low":
                risk_level = "high"

            # Step 16: Duplicate / similar complaint detection
            similar_incidents = []
            similar_ids = []
            dup_prob = 0.0
            if complaint_id is not None:
                similar_incidents = self.similarity_service.find_similar(cleaned_text)
                similar_ids = [s["complaint_id"] for s in similar_incidents if s["complaint_id"] != complaint_id]
                dup_prob = self.similarity_service.calculate_duplicate_probability(cleaned_text)
                self.similarity_service.add_complaint(complaint_id, cleaned_text, {"category": category})

            # Step 17: Multi-dimensional calibrated confidence estimation
            conf_signals = {
                "classifier_confidence": clf_confidence,
                "priority_score": final_priority_score,
                "entities": entities,
                "sentiment": sentiment_res
            }
            conf_metrics = self.confidence_estimator.estimate(conf_signals)

            # Step 18: Explainability (Machine-readable reasons & human summary)
            exp_data = {
                "category": category,
                "subcategory": subcategory,
                "entities": entities,
                "priority": final_priority,
                "severity_score": p_res["severity_score"],
                "impact_score": p_res["impact_score"],
                "safety_score": p_res["safety_score"],
                "disruption_score": p_res["disruption_score"],
                "duration_score": p_res["duration_score"],
                "rules_applied": analysis_dict.get("rules_applied", []),
                "is_essential_service": is_essential
            }
            machine_reasons = self.explainer.generate_reasons(exp_data)
            reasoning_summary = self.explainer.generate_explanation(exp_data)
            recommended_action = self.explainer.generate_recommended_action(exp_data)

            # Step 19: Final structured AI response
            latency_ms = (time.time() - start_time) * 1000.0

            return AnalysisResult(
                category=category,
                subcategory=subcategory,
                priority=final_priority,
                priority_score=final_priority_score,
                urgency_score=p_res["urgency_score"],
                severity_score=p_res["severity_score"],
                impact_score=p_res["impact_score"],
                safety_score=p_res["safety_score"],
                duration_score=p_res["duration_score"],
                disruption_score=p_res["disruption_score"],
                vulnerability_score=p_res["vulnerability_score"],
                confidence=conf_metrics["overall"],
                category_confidence=conf_metrics["category"],
                priority_confidence=conf_metrics["priority"],
                sentiment_confidence=conf_metrics["sentiment"],
                entity_confidence=conf_metrics["entity"],
                sentiment=sentiment_res["sentiment"],
                risk_level=risk_level,
                entities=[entities],
                key_issues=machine_reasons,
                reasons=machine_reasons,
                incident_type=entities.get("incident_type", "GENERAL"),
                vehicle=entities.get("vehicle", {}),
                approximate_time=entities.get("approximate_time"),
                direction=entities.get("direction_of_travel"),
                injury_reported=entities.get("injury_reported", False),
                affected_population=entities.get("people_affected"),
                affected_population_estimate=entities.get("people_affected_estimate"),
                reasoning_summary=reasoning_summary,
                recommended_action=recommended_action,
                duplicate_probability=dup_prob,
                similar_complaint_ids=similar_ids,
                similar_incidents=similar_incidents,
                language=lang,
                provenance=entities.get("provenance", {}),
                analysis_model_version="1.1.0",
                analysis_latency_ms=round(latency_ms, 2)
            )

        except Exception as e:
            # Robust fallback that never crashes caller
            latency_ms = (time.time() - start_time) * 1000.0
            return AnalysisResult(
                category="Other", subcategory="General", priority="LOW",
                priority_score=30, urgency_score=30, severity_score=30, impact_score=30, safety_score=20, duration_score=20,
                confidence=0.35, category_confidence=0.35, priority_confidence=0.50, sentiment_confidence=0.50, entity_confidence=0.30,
                sentiment="neutral", risk_level="low", entities=[], key_issues=["Manual triage required"], reasons=["System fallback"],
                affected_population=None, affected_population_estimate=None,
                reasoning_summary=f"Automated analysis fallback: {str(e)}", recommended_action="Manual administrative review required",
                duplicate_probability=0.0, similar_complaint_ids=[], language="en",
                analysis_model_version="1.1.0", analysis_latency_ms=round(latency_ms, 2)
            )

_pipeline_instance = None

def get_pipeline() -> ComplaintAnalysisPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = ComplaintAnalysisPipeline()
    return _pipeline_instance
