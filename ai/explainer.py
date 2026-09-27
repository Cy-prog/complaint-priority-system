class Explainer:
    def generate_reasons(self, analysis: dict) -> list[str]:
        """Generate structured machine-readable reasons list based on detected signals."""
        reasons = []
        entities = analysis.get('entities', {})
        priority = analysis.get('priority', 'LOW')
        incident_type = entities.get('incident_type', 'GENERAL')
        
        # 1. Injuries and life threats
        if entities.get('injury_reported'):
            reasons.append("injury reported")
            
        if incident_type == "HIT_AND_RUN":
            reasons.append("active hit-and-run incident")
            reasons.append("vehicle fled the scene")
        elif incident_type == "FIRE":
            reasons.append("active fire outbreak")
        elif incident_type == "THEFT":
            reasons.append("reported theft/burglary")
        elif incident_type == "ASSAULT":
            reasons.append("ongoing violent clash")
            
        # 2. Safety hazards
        safety_hazards = entities.get('safety_hazards', [])
        for sh in safety_hazards:
            reasons.append(f"safety hazard: {sh}")
            
        # 3. Essential service disruptions
        if entities.get('essential_service_disrupted') or analysis.get('is_essential_service'):
            durations = entities.get('durations', [])
            if durations:
                reasons.append(f"essential service disrupted for {durations[0]['raw']}")
            else:
                reasons.append("essential municipal service disrupted")
                
        # 4. Population impact
        if entities.get('people_affected'):
            reasons.append(f"affects {entities['people_affected']}")
            
        # 5. Vulnerable groups
        vulnerable = entities.get('vulnerable_groups', [])
        if vulnerable:
            reasons.append(f"vulnerable location/population: {', '.join(vulnerable)}")
            
        # 6. Hard safety rules applied
        rules_applied = analysis.get('rules_applied', [])
        for r in rules_applied:
            if r not in reasons:
                reasons.append(r)
                
        # Fallback if empty
        if not reasons:
            category = analysis.get('category', 'civic issue')
            reasons.append(f"standard triage for {category} with priority {priority}")
            
        return reasons

    def generate_explanation(self, analysis: dict) -> str:
        parts = []
        category = analysis.get('category', 'civic matter')
        subcategory = analysis.get('subcategory')
        if subcategory:
            parts.append(f"The complaint reports a {subcategory} issue regarding {category}.")
        else:
            parts.append(f"The complaint reports an issue regarding {category}.")
        
        entities = analysis.get('entities', {})
        reasons = self.generate_reasons(analysis)
        if reasons:
            parts.append(f"Key signals: {'; '.join(reasons[:4])}.")
            
        v_info = entities.get('vehicle', {})
        if v_info.get('type') or v_info.get('plate'):
            v_desc = f"Vehicle identified: {v_info.get('color', '')} {v_info.get('type', 'vehicle')}".strip()
            if v_info.get('plate'):
                v_desc += f" (Plate: {v_info.get('plate')})"
            parts.append(f"{v_desc}.")
            
        if entities.get('direction_of_travel'):
            parts.append(f"Suspect fled toward {entities['direction_of_travel']}.")
            
        return " ".join(parts)

    def generate_recommended_action(self, analysis: dict) -> str:
        priority = analysis.get('priority', 'LOW')
        category = analysis.get('category', 'relevant department')
        incident_type = analysis.get('entities', {}).get('incident_type', 'GENERAL')
        
        if incident_type == "HIT_AND_RUN":
            return "Alert Traffic Police & local PCR units immediately. Secure CCTV footage and dispatch emergency medical aid."
        elif incident_type == "FIRE":
            return "Dispatch Fire Services (101) immediately and evacuate surrounding premises."
        elif priority == 'CRITICAL':
            return f"Escalate immediately to {category} rapid response team. Field intervention required within 1 hour."
        elif priority == 'HIGH':
            return f"Assign to {category} department for urgent inspection and remediation within 4 hours."
        elif priority == 'MEDIUM':
            return f"Route to {category} department for scheduled workflow resolution."
        else:
            return "Log into regular maintenance queue."
