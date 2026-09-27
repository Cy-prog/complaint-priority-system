class ConfidenceEstimator:
    def estimate(self, signals: dict) -> dict:
        """
        Calculates multi-dimensional calibrated confidence metrics:
        - categoryConfidence: from model posterior / decision margin
        - priorityConfidence: based on signal agreement and threshold margin
        - sentimentConfidence: from sentiment polarity confidence
        - entityConfidence: from extraction completeness
        - overallConfidence: harmonic balance
        """
        # 1. Category Confidence
        clf_conf = float(signals.get('classifier_confidence', 0.80))
        cat_conf = min(max(clf_conf, 0.20), 0.99)
        
        # 2. Priority Confidence
        # Higher when multiple factors agree and score is well separated from boundary
        p_score = signals.get('priority_score', 50)
        dist_to_boundary = min(abs(p_score - 75), abs(p_score - 55), abs(p_score - 35))
        p_conf = min(0.65 + (dist_to_boundary / 60.0) * 0.30, 0.98)
        
        # If hard safety rule was triggered, priority confidence is high
        entities = signals.get('entities', {})
        if entities.get('injury_reported') or entities.get('incident_type') == 'HIT_AND_RUN':
            p_conf = max(p_conf, 0.94)
            
        # 3. Sentiment Confidence
        sentiment_data = signals.get('sentiment', {})
        sent_conf = float(sentiment_data.get('confidence', 0.75))
        
        # 4. Entity Confidence
        entity_count = (
            (1 if entities.get('locations') else 0) +
            (1 if entities.get('durations') else 0) +
            (1 if entities.get('people_affected') else 0) +
            (1 if entities.get('safety_hazards') else 0) +
            (1 if entities.get('vehicle', {}).get('type') else 0) +
            (1 if entities.get('incident_type') != 'GENERAL' else 0)
        )
        ent_conf = min(0.40 + (entity_count * 0.12), 0.96)
        
        # Overall Confidence
        overall = 0.40 * cat_conf + 0.30 * p_conf + 0.15 * ent_conf + 0.15 * sent_conf
        
        return {
            "overall": round(float(overall), 4),
            "category": round(float(cat_conf), 4),
            "priority": round(float(p_conf), 4),
            "sentiment": round(float(sent_conf), 4),
            "entity": round(float(ent_conf), 4)
        }
