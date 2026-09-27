import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"

class PriorityEngine:
    def __init__(self):
        self.config = self._load_config()
        self.weights = self.config.get('priority_weights', {
            'severity': 0.30,
            'impact': 0.20,
            'safety': 0.20,
            'service_disruption': 0.15,
            'duration': 0.10,
            'vulnerability': 0.05
        })
        self.thresholds = self.config.get('priority_thresholds', {
            'CRITICAL': 75,
            'HIGH': 55,
            'MEDIUM': 35,
            'LOW': 0
        })

    def _load_config(self):
        try:
            with open(CONFIG_DIR / "priority_config.yaml", "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return {}

    def calculate_priority(self, signals: dict) -> dict:
        severity = self._calc_severity(signals)
        impact = self._calc_impact(signals)
        safety = self._calc_safety(signals)
        disruption = self._calc_service_disruption(signals)
        duration = self._calc_duration(signals)
        vulnerability = self._calc_vulnerability(signals)
        
        # Weighted score (normalized to weights sum)
        w_sev = self.weights.get('severity', 0.30)
        w_imp = self.weights.get('impact', 0.20)
        w_safe = self.weights.get('safety', 0.20)
        w_dis = self.weights.get('service_disruption', 0.15)
        w_dur = self.weights.get('duration', 0.10)
        w_vul = self.weights.get('vulnerability', 0.05)
        total_w = w_sev + w_imp + w_safe + w_dis + w_dur + w_vul
        
        raw_score = (
            severity * w_sev +
            impact * w_imp +
            safety * w_safe +
            disruption * w_dis +
            duration * w_dur +
            vulnerability * w_vul
        ) / (total_w if total_w > 0 else 1.0)
        
        priority_score = min(max(int(round(raw_score)), 0), 100)
        
        priority = "LOW"
        if priority_score >= self.thresholds.get('CRITICAL', 75):
            priority = "CRITICAL"
        elif priority_score >= self.thresholds.get('HIGH', 55):
            priority = "HIGH"
        elif priority_score >= self.thresholds.get('MEDIUM', 35):
            priority = "MEDIUM"

        return {
            "priority": priority,
            "priority_score": priority_score,
            "severity_score": severity,
            "impact_score": impact,
            "safety_score": safety,
            "disruption_score": disruption,
            "duration_score": duration,
            "vulnerability_score": vulnerability,
            "urgency_score": max(disruption, severity) # backward compatibility
        }

    def _calc_severity(self, signals: dict) -> int:
        score = 20
        category_risk = signals.get('category_risk_level', 'low')
        if category_risk == 'critical': score += 45
        elif category_risk == 'high': score += 25
        elif category_risk == 'medium': score += 10
        
        entities = signals.get('entities', {})
        if entities.get('injury_reported'):
            score += 35
            
        incident = entities.get('incident_type', 'GENERAL')
        if incident in ['HIT_AND_RUN', 'FIRE', 'ASSAULT']:
            score += 30
        elif incident in ['THEFT', 'ACCIDENT', 'CIVIC_HAZARD']:
            score += 20
            
        if any(h in ['collapse', 'explosion', 'gas leak', 'major contamination'] for h in entities.get('safety_hazards', [])):
            score += 30

        if signals.get('is_essential_service') and entities.get('essential_service_disrupted'):
            score += 15

        if entities.get('vulnerable_groups'):
            score += 15

        durations = entities.get('durations', [])
        for d in durations:
            if 'day' in d.get('unit', '').lower() and d.get('value', 0) >= 2:
                score += 10
                break

        return min(score, 100)

    def _calc_impact(self, signals: dict) -> int:
        score = 15
        entities = signals.get('entities', {})
        pop = entities.get('people_affected_estimate')
        if pop:
            if pop >= 50: score += 55
            elif pop >= 20: score += 40
            elif pop >= 5: score += 25
            else: score += 10
        elif entities.get('people_affected'):
            score += 25
            
        if entities.get('locations'):
            score += 15
            
        return min(score, 100)

    def _calc_safety(self, signals: dict) -> int:
        score = 0
        entities = signals.get('entities', {})
        
        if entities.get('injury_reported'):
            score += 50
            
        incident = entities.get('incident_type')
        if incident in ['HIT_AND_RUN', 'FIRE', 'ASSAULT']:
            score += 45
        elif incident in ['CIVIC_HAZARD', 'ACCIDENT']:
            score += 35
            
        hazards = entities.get('safety_hazards', [])
        critical_hazards = ['fire', 'collapse', 'electrocution', 'explosion', 'gas leak', 'live wire', 'toxic', 'drowning', 'major contamination']
        if any(h in critical_hazards for h in hazards):
            score += 45
        elif hazards:
            score += 25
            
        if any(h in ['open manhole', 'broken bridge', 'sinkhole'] for h in hazards):
            score += 35
            
        return min(score, 100)

    def _calc_service_disruption(self, signals: dict) -> int:
        score = 0
        entities = signals.get('entities', {})
        is_essential = signals.get('is_essential_service', False) or entities.get('essential_service_disrupted', False)
        
        if is_essential:
            score += 40
        if entities.get('essential_service_disrupted'):
            score += 30
            
        durations = entities.get('durations', [])
        for d in durations:
            unit = d['unit'].lower()
            val = d['value']
            if 'day' in unit and val >= 2: score += 30
            elif 'week' in unit: score += 30
            elif 'hour' in unit and val >= 12: score += 20
            
        return min(score, 100)

    def _calc_duration(self, signals: dict) -> int:
        score = 10
        entities = signals.get('entities', {})
        durations = entities.get('durations', [])
        
        max_hours = 0
        for d in durations:
            val = d['value']
            unit = d['unit'].lower()
            if 'hour' in unit: max_hours = max(max_hours, val)
            elif 'day' in unit: max_hours = max(max_hours, val * 24)
            elif 'week' in unit: max_hours = max(max_hours, val * 168)
            elif 'month' in unit: max_hours = max(max_hours, val * 720)
            
        if max_hours >= 168: score = 90
        elif max_hours >= 72: score = 75
        elif max_hours >= 24: score = 55
        elif max_hours >= 6: score = 35
        elif max_hours > 0: score = 20
        
        return score

    def _calc_vulnerability(self, signals: dict) -> int:
        score = 0
        entities = signals.get('entities', {})
        vul = entities.get('vulnerable_groups', [])
        if vul:
            score += 60
            if any(w in ['hospital', 'school', 'kindergarten', 'maternity', 'अस्पताल', 'स्कूल'] for w in vul):
                score += 30
        return min(score, 100)
