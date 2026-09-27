class RuleEngine:
    def __init__(self):
        self.priority_order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}

    def apply_rules(self, analysis: dict) -> dict:
        rules_applied = []
        current_priority = analysis.get('priority', 'LOW')
        entities = analysis.get('entities', {})
        is_essential = analysis.get('is_essential_service', False) or entities.get('essential_service_disrupted', False)
        
        safety_hazards = entities.get('safety_hazards', [])
        incident_type = entities.get('incident_type', 'GENERAL')
        injury_reported = entities.get('injury_reported', False)
        safety_score = analysis.get('safety_score', 0)
        durations = entities.get('durations', [])
        
        max_hours = 0
        for d in durations:
            val = d['value']
            unit = d['unit'].lower()
            if 'hour' in unit: max_hours = max(max_hours, val)
            elif 'day' in unit: max_hours = max(max_hours, val * 24)
            elif 'week' in unit: max_hours = max(max_hours, val * 168)
            elif 'month' in unit: max_hours = max(max_hours, val * 720)
            
        vulnerable = entities.get('vulnerable_groups', [])
        pop_estimate = entities.get('people_affected_estimate', 0)

        def escalate_to(target_prio: str, rule_name: str):
            nonlocal current_priority
            if self.priority_order[target_prio] > self.priority_order[current_priority]:
                current_priority = target_prio
                rules_applied.append(rule_name)

        # ─── HARD SAFETY ESCALATION RULES ────────────────────────
        # 1. Injury reported in incident
        if injury_reported:
            escalate_to("CRITICAL", "Hard Safety Trigger: Physical injury/casualty reported")

        # 2. Active Hit-and-Run incident
        if incident_type == "HIT_AND_RUN":
            escalate_to("CRITICAL", "Hard Safety Trigger: Active Hit-and-Run incident")

        # 3. Active fire emergency
        if incident_type == "FIRE" or any(h in ['fire', 'आग', 'आगजनी'] for h in safety_hazards):
            escalate_to("CRITICAL", "Hard Safety Trigger: Active fire hazard")

        # 4. Active electrical hazard / live wire
        if any(h in ['live wire', 'exposed wire', 'electrocution', 'करंट', 'नंगा तार'] for h in safety_hazards):
            escalate_to("CRITICAL", "Rule 4: Active high-voltage electrical hazard")

        # 5. Toxic gas leak or explosion threat
        if any(h in ['gas leak', 'explosion', 'toxic', 'गैस रिसाव'] for h in safety_hazards):
            escalate_to("CRITICAL", "Hard Safety Trigger: Hazardous gas leak or explosion threat")

        # 6. Structural collapse / open manhole
        if any(h in ['collapse', 'open manhole', 'खुला मैनहोल'] for h in safety_hazards):
            escalate_to("CRITICAL", "Hard Safety Trigger: Fall or structural collapse hazard")

        # 7. Ongoing violent incident or armed robbery
        if incident_type in ["ASSAULT", "ARMED_ROBBERY"]:
            escalate_to("CRITICAL", "Hard Safety Trigger: Ongoing violent incident / armed crime")

        # 8. Critical Medical Emergency
        if incident_type == "MEDICAL_EMERGENCY":
            escalate_to("CRITICAL", "Hard Safety Trigger: Life-threatening medical emergency")

        # 9. Vulnerable population with essential service disruption
        if is_essential and vulnerable and (max_hours >= 24 or entities.get('essential_service_disrupted')):
            escalate_to("CRITICAL", "Rule 3b: Essential service disruption affecting vulnerable population")

        # 10. Vulnerable population with active safety risk
        if vulnerable and (safety_hazards or safety_score > 40):
            escalate_to("CRITICAL", "Rule: Vulnerable population exposed to safety hazard")

        # 11. Extended essential service disruption (>= 24h)
        if is_essential and max_hours >= 24:
            escalate_to("HIGH", "Rule: Essential service disrupted > 24 hours")

        # 12. Large population affected (>= 50 people)
        if is_essential and pop_estimate and pop_estimate >= 50:
            escalate_to("HIGH", "Rule: Large population essential service disruption")

        analysis['priority'] = current_priority
        analysis['rules_applied'] = rules_applied
        return analysis
