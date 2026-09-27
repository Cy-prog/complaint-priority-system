import re
import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"

class EntityExtractor:
    def __init__(self):
        self.safety_keywords = self._load_safety_keywords()
        self.word_to_num = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
            'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'एक': 1, 'दो': 2, 'तीन': 3, 'चार': 4, 'पांच': 5, 'पाँच': 5,
            'छह': 6, 'सात': 7, 'आठ': 8, 'नौ': 9, 'दस': 10
        }

    def _load_safety_keywords(self):
        try:
            with open(CONFIG_DIR / "safety_keywords.yaml", "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception:
            return {}

    def extract(self, text: str) -> dict:
        text_lower = text.lower()
        
        # 1. Incident Type
        incident_type = self._extract_incident_type(text_lower)
        
        # 2. Vehicle Details
        vehicle_info = self._extract_vehicle(text)
        
        # 3. Approximate Time
        approx_time = self._extract_time(text)
        
        # 4. Direction of Travel
        direction = self._extract_direction(text)
        
        # 5. Injury Detection
        injury_reported = self._detect_injury(text_lower)
        
        # 6. Evidence Availability
        evidence = self._detect_evidence(text_lower, vehicle_info)
        
        # 7. Locations & Landmarks
        locations = self._extract_locations(text)
        
        # 8. Durations & Numbers
        durations = self._extract_durations(text)
        numbers = self._extract_numbers(text)
        
        # 9. Safety hazards & groups
        safety_hazards = self._extract_keywords(
            text_lower,
            self.safety_keywords.get('critical_safety_keywords', []) + self.safety_keywords.get('high_safety_keywords', [])
        )
        vulnerable_groups = self._extract_keywords(
            text_lower,
            self.safety_keywords.get('vulnerable_population_keywords', [])
        )
        escalation_signals = self._extract_keywords(
            text_lower,
            self.safety_keywords.get('escalation_signal_keywords', [])
        )
        essential_disrupted = self._check_essential_service(text_lower)
        
        # Machine-readable key issues / reasons
        key_issues = []
        if injury_reported:
            key_issues.append("injury reported")
        if incident_type == "HIT_AND_RUN":
            key_issues.append("active hit-and-run")
            key_issues.append("vehicle fled the scene")
        elif incident_type == "THEFT":
            key_issues.append("reported theft/robbery")
        elif incident_type == "FIRE":
            key_issues.append("active fire emergency")
        elif incident_type == "ASSAULT":
            key_issues.append("ongoing violent incident")
            
        if safety_hazards:
            for sh in safety_hazards[:3]:
                if sh not in key_issues:
                    key_issues.append(f"safety hazard: {sh}")
                    
        if essential_disrupted:
            key_issues.append("essential service disruption")
            
        if vulnerable_groups:
            key_issues.append(f"vulnerable population affected: {', '.join(vulnerable_groups[:2])}")
            
        if durations:
            key_issues.append(f"ongoing duration: {durations[0]['raw']}")

        # Provenance markers for auditability
        provenance = {
            "incident_type": "AI-EXTRACTED",
            "vehicle": "REPORTED",
            "locations": "REPORTED" if locations else "NONE",
            "injury": "REPORTED",
            "evidence": "AI-EXTRACTED"
        }

        # Affected population estimation
        people_affected = None
        people_affected_estimate = None
        pop_words = ['people', 'families', 'households', 'citizens', 'residents', 'homes', 'houses', 
                     'लोग', 'लोगों', 'परिवार', 'परिवारों', 'घर', 'घरों', 'मकान', 'मकानों', 'दुकान', 'दुकानों', 'बच्चे', 'मरीज']
        for num in numbers:
            if any(word in num['context'] for word in pop_words):
                people_affected_estimate = num['value']
                people_affected = f"{num['value']} {num['context'].strip()}"
                break
                
        if not people_affected:
            qual_match = re.search(r'\b(several|multiple|many|numerous|all|dozens of)\s+(households|families|residents|people|homes|houses|citizens)\b', text_lower)
            if qual_match:
                people_affected = qual_match.group(0)
                people_affected_estimate = 50 if qual_match.group(1) in ['multiple', 'many', 'numerous', 'all', 'dozens of'] else 25
            elif any(w in text_lower for w in ['colony', 'society', 'neighborhood', 'village', 'entire area', 'पूरा क्षेत्र', 'मोहल्ला']):
                people_affected = "multiple households in area"
                people_affected_estimate = 40
            elif locations:
                people_affected = f"residents near {locations[0]}"
                people_affected_estimate = 20

        return {
            "locations": locations,
            "incident_type": incident_type,
            "vehicle": vehicle_info,
            "approximate_time": approx_time,
            "direction_of_travel": direction,
            "injury_reported": injury_reported,
            "evidence": evidence,
            "durations": durations,
            "numbers": numbers,
            "people_affected": people_affected,
            "people_affected_estimate": people_affected_estimate,
            "safety_hazards": safety_hazards,
            "vulnerable_groups": vulnerable_groups,
            "escalation_signals": escalation_signals,
            "essential_service_disrupted": essential_disrupted,
            "key_issues": key_issues,
            "provenance": provenance
        }

    def _extract_incident_type(self, text_lower: str) -> str:
        if any(w in text_lower for w in ["armed", "guns", "gun", "pistol", "knife", "stabbing", "weapon", "robbery", "डकैती", "हथियार", "चाकू"]):
            return "ARMED_ROBBERY"
        if any(w in text_lower for w in ["hit and run", "hit-and-run", "hit a pedestrian", "escaped toward", "knocked down and fled", "टक्कर मारकर फरार", "हिट एंड रन"]):
            return "HIT_AND_RUN"
        if any(w in text_lower for w in ["fire", "blaze", "aag", "आग", "आगजनी"]):
            return "FIRE"
        if any(w in text_lower for w in ["theft", "stolen", "burglary", "snatching", "चोरी", "लूट"]):
            return "THEFT"
        if any(w in text_lower for w in ["clash", "fight", "assault", "violence", "मारपीट", "हमला"]):
            return "ASSAULT"
        if any(w in text_lower for w in ["ambulance", "hospital emergency", "critical patient", "food poisoning", "एंबुलेंस"]):
            return "MEDICAL_EMERGENCY"
        if any(w in text_lower for w in ["accident", "collision", "crash", "हादसा", "दुर्घटना"]):
            return "ACCIDENT"
        if any(w in text_lower for w in ["live wire", "exposed wire", "open manhole", "gas leak", "collapse"]):
            return "CIVIC_HAZARD"
        return "GENERAL"

    def _extract_vehicle(self, text: str) -> dict:
        text_lower = text.lower()
        
        # Vehicle Type
        vehicle_type = None
        type_patterns = [
            (r'\b(suv|scorpio|bolero|innova|fortuner|thar|creta|harrier|safari)\b', "SUV"),
            (r'\b(sedan|honda city|verna|dzire|ciaz)\b', "SEDAN"),
            (r'\b(car|four wheeler|motorcar|गाड़ी|कार)\b', "CAR"),
            (r'\b(bike|motorcycle|pulsar|bullet|splendor|two wheeler|मोटरसाइकिल|बाइक)\b', "MOTORCYCLE"),
            (r'\b(scooter|scooty|activa|स्कूटर)\b', "SCOOTER"),
            (r'\b(truck|dumper|lorry|ट्रक|डंपर)\b', "TRUCK"),
            (r'\b(bus|minibus|बस)\b', "BUS"),
            (r'\b(auto|rickshaw|e-rickshaw|ऑटो|रिक्शा)\b', "AUTO_RICKSHAW"),
            (r'\b(tractor|ट्रैक्टर)\b', "TRACTOR"),
            (r'\b(bicycle|cycle|साइकिल)\b', "BICYCLE")
        ]
        for pattern, v_type in type_patterns:
            if re.search(pattern, text_lower):
                vehicle_type = v_type
                break

        # Vehicle Color
        vehicle_color = None
        color_patterns = [
            (r'\b(black|काली|काला)\b', "BLACK"),
            (r'\b(white|सफेद|सफ़ेद)\b', "WHITE"),
            (r'\b(red|लाल)\b', "RED"),
            (r'\b(blue|नीली|नीला)\b', "BLUE"),
            (r'\b(silver|चांदी)\b', "SILVER"),
            (r'\b(grey|gray|ग्रे)\b', "GREY"),
            (r'\b(yellow|पीली|पीला)\b', "YELLOW"),
            (r'\b(green|हरी|हरा)\b', "GREEN"),
            (r'\b(brown|भूरा)\b', "BROWN"),
            (r'\b(golden|गोल्डन)\b', "GOLDEN")
        ]
        for pattern, col in color_patterns:
            if re.search(pattern, text_lower):
                vehicle_color = col
                break

        # License Plate (Full or partial Indian plates, e.g. MP07 AB 2, MP-07-AB-1234, DL 01 AB 1234, MH 12 3456)
        plate = None
        plate_patterns = [
            # Standard or partial plate: e.g. MP07 AB 2, MP 07 AB 1234, MP-07-AB-12
            r'\b([A-Z]{2}[ -]?[0-9]{1,2}[ -]?[A-Z]{1,3}[ -]?[0-9]{1,4})\b',
            # Partial prefix with number: e.g. MP07 AB, MP-07 4521
            r'\b([A-Z]{2}[ -]?[0-9]{1,2}[ -]?[0-9]{1,4})\b',
            # Just number plate keyword followed by token: "number plate MP07 AB 2"
            r'plate\s+(?:is\s+|number\s+)?([A-Z0-9 ]{4,12})'
        ]
        for p_pat in plate_patterns:
            m = re.search(p_pat, text, re.IGNORECASE)
            if m:
                cand = m.group(1).strip()
                # Basic validation: must contain at least 2 state letters and digits
                if re.search(r'[A-Z]{2}', cand, re.IGNORECASE) and re.search(r'\d', cand):
                    plate = cand.upper()
                    break

        return {
            "type": vehicle_type,
            "color": vehicle_color,
            "plate": plate
        }

    def _extract_time(self, text: str) -> str | None:
        # Time patterns: e.g. 8:30 PM, 20:30, 8 PM, 8:30 am
        m = re.search(r'\b(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?|\d{1,2}\s*(?:am|pm|AM|PM))\b', text)
        if m:
            t_str = m.group(1).strip()
            # Normalize to 24h if e.g. 8:30 PM -> 20:30
            pm_m = re.match(r'(\d{1,2}):?(\d{2})?\s*([pP][mM])', t_str)
            if pm_m:
                hour = int(pm_m.group(1))
                mins = pm_m.group(2) or "00"
                if hour < 12:
                    hour += 12
                return f"{hour:02d}:{mins}"
            return t_str
            
        hindi_time = re.search(r'(रात|सुबह|दोपहर|शाम)\s*(\d{1,2})\s*(बजे)?', text)
        if hindi_time:
            period = hindi_time.group(1)
            hour = int(hindi_time.group(2))
            if period in ['रात', 'शाम'] and hour < 12:
                hour += 12
            return f"{hour:02d}:00"
            
        return None

    def _extract_direction(self, text: str) -> str | None:
        m = re.search(r'\b(?:escaped|headed|fled|going|ran|run|running)\s+(?:towards?|toward|to|in)?\s*(?:the\s+)?([a-zA-Z\u0900-\u097F_-]+)', text, re.IGNORECASE)
        if m:
            dest = m.group(1).strip()
            if dest.lower() not in ['a', 'an', 'the', 'his', 'her', 'their', 'toward', 'towards']:
                return dest.lower()
        # Hindi direction
        m_hi = re.search(r'([a-zA-Z\u0900-\u097F_-]+)\s*(?:की तरफ|की ओर)\s*(?:भाग|फरार)', text)
        if m_hi:
            return m_hi.group(1).strip().lower()
        return None

    def _detect_injury(self, text_lower: str) -> bool:
        injury_words = [
            'injured', 'injury', 'bleeding', 'hurt', 'wound', 'wounded', 'unconscious',
            'hospitalized', 'fracture', 'died', 'fatality', 'casualty', 'knocked down',
            'घायल', 'चोट', 'खून', 'बेहोश', 'अस्पताल भर्ती', 'मृत्यु'
        ]
        return any(w in text_lower for w in injury_words)

    def _detect_evidence(self, text_lower: str, vehicle_info: dict) -> list[str]:
        ev = []
        if any(w in text_lower for w in ['cctv', 'camera', 'footage', 'सीसीटीवी']):
            ev.append("CCTV_FOOTAGE")
        if any(w in text_lower for w in ['photo', 'picture', 'video', 'recording', 'तस्वीर', 'फोटो', 'वीडियो']):
            ev.append("DIGITAL_MEDIA")
        if any(w in text_lower for w in ['witness', 'bystander', 'crowd', 'गवाह']):
            ev.append("EYEWITNESS")
        if vehicle_info.get("plate"):
            ev.append("PARTIAL_OR_FULL_REGISTRATION_PLATE")
        return ev

    def _extract_locations(self, text: str) -> list[str]:
        locations = []
        
        # English & Hindi Ward match
        ward_match = re.search(r'ward\s*(no\.?)?\s*(\d+)', text, re.IGNORECASE)
        if ward_match:
            locations.append(ward_match.group(0))
            
        hindi_ward = re.search(r'वार्ड\s*(नं\.?|नंबर)?\s*(\d+)', text)
        if hindi_ward:
            locations.append(hindi_ward.group(0))

        # Known Gwalior Landmarks & Common landmarks
        landmarks = [
            'railway station', 'bus stand', 'bus depot', 'hospital', 'civil hospital',
            'city center', 'maharaj bada', 'thatipur', 'morar', 'hazira', 'kila gate',
            'dindayal nagar', 'pinto park', 'sarafa bazaar', 'bal bhavan', 'high court',
            'महाराज बाड़ा', 'हजीरा', 'थाटीपुर', 'सिटी सेंटर', 'मुरार', 'कंपू', 'फूलबाग', 
            'दीनदयाल नगर', 'गोविंदपुरी', 'किला गेट', 'बहोड़ापुर', 'पिंटो पार्क', 'लश्कर',
            'सराफा बाजार', 'रेलवे स्टेशन'
        ]
        for lm in landmarks:
            if lm in text.lower() and lm not in [l.lower() for l in locations]:
                locations.append(lm)

        # Contextual location: "near X", "at X", "in X", "outside X"
        area_match = re.search(r'\b(?:near|at|in|outside|around)\s+(?:the\s+)?([A-Z][a-zA-Z0-9_-]+(?:\s+[A-Z][a-zA-Z0-9_-]+){0,3})', text)
        if area_match:
            cand = area_match.group(1).strip()
            if cand.lower() not in [l.lower() for l in locations] and len(cand) > 2:
                locations.append(cand)
                
        return locations

    def _extract_numbers(self, text: str) -> list[dict]:
        numbers = []
        matches = re.finditer(r'(\d+)\s+([a-zA-Z\u0900-\u097F]+)', text)
        for match in matches:
            val = int(match.group(1))
            ctx = match.group(2)
            skip_units = ['days', 'hours', 'weeks', 'months', 'years', 'day', 'hour', 'week', 'month', 'year', 'hrs',
                          'दिन', 'घंटे', 'घंटा', 'सप्ताह', 'हफ्ते', 'महीने', 'साल', 'वर्ष']
            if ctx.lower() not in skip_units:
                numbers.append({'value': val, 'context': ctx})
        return numbers

    def _extract_durations(self, text: str) -> list[dict]:
        durations = []
        mod_text = text.lower()
        for word, num in self.word_to_num.items():
            mod_text = mod_text.replace(word, str(num))
            
        matches = re.finditer(r'(\d+)\s*(days?|hours?|weeks?|months?|years?|hrs?|din|dino|ghante|ghanto|hafte|दिन|घंटे|घंटा|सप्ताह|हफ्ते|हफ्ता|महीने|महीना|साल|वर्ष)', mod_text)
        for match in matches:
            val = int(match.group(1))
            unit_raw = match.group(2)
            unit_norm = unit_raw
            if unit_raw in ['दिन', 'din', 'dino']: unit_norm = 'days'
            elif unit_raw in ['घंटे', 'घंटा', 'hrs', 'hr', 'ghante', 'ghanto']: unit_norm = 'hours'
            elif unit_raw in ['सप्ताह', 'हफ्ते', 'हफ्ता', 'hafte']: unit_norm = 'weeks'
            elif unit_raw in ['महीने', 'महीना']: unit_norm = 'months'
            elif unit_raw in ['साल', 'वर्ष']: unit_norm = 'years'
            durations.append({
                'value': val,
                'unit': unit_norm,
                'raw': match.group(0)
            })
        if re.search(r'\b(kal raat|last night)\b', mod_text):
            durations.append({'value': 12, 'unit': 'hours', 'raw': 'since last night'})
        elif re.search(r'\b(yesterday|kal se)\b', mod_text):
            durations.append({'value': 24, 'unit': 'hours', 'raw': 'since yesterday'})

        return durations

    def _extract_keywords(self, text: str, keywords: list[str]) -> list[str]:
        found = []
        for kw in keywords:
            kw_clean = kw.strip().lower()
            if not kw_clean:
                continue
            if any('\u0900' <= char <= '\u097F' for char in kw_clean):
                if kw_clean in text:
                    found.append(kw)
            else:
                if re.search(r'\b' + re.escape(kw_clean) + r'\b', text):
                    found.append(kw)
                
        # Robust hazard patterns
        if re.search(r'\b(exposed|live|hanging|loose|broken|naked)\b.*\b(wire|wires|cable|cables)\b', text) or \
           ('तार' in text and any(w in text for w in ['लटक', 'नंगा', 'खुला', 'लाइव', 'झुक'])):
            if "live wire" not in found:
                found.append("live wire")

        if re.search(r'\b(open|uncovered|broken)\b.*\b(manhole|drain|gutter|pit)\b', text) or \
           (('मैनहोल' in text or 'चेंबर' in text) and any(w in text for w in ['खुला', 'टूटा'])):
            if "open manhole" not in found:
                found.append("open manhole")

        if re.search(r'\b(wall|bridge|ceiling|building|roof|structure)\b.*\b(collapsed?|falling|cracked)\b', text):
            if "collapse" not in found:
                found.append("collapse")

        if ('करंट' in text and any(w in text for w in ['खतरा', 'लग', 'झटका'])) or 'electrocution' in text:
            if "electrocution" not in found:
                found.append("electrocution")

        if re.search(r'\b(blast|exploded?|explosion|विस्फोट|धमाका)\b', text):
            if "explosion" not in found:
                found.append("explosion")
                
        return found
        
    def _check_essential_service(self, text: str) -> bool:
        keywords = self.safety_keywords.get('essential_service_disruption_keywords', [])
        if any(kw.lower() in text for kw in keywords):
            return True
        essential_terms = [
            'water', 'electricity', 'power', 'current', 'drainage', 'sewage', 'sanitation', 'streetlight', 'pipeline', 'tank', 'light',
            'पानी', 'बिजली', 'जल', 'सीवर', 'नाली', 'पाइपलाइन', 'करंट', 'ट्रांसफार्मर', 'पेयजल'
        ]
        disruption_terms = [
            'stop', 'stopped', 'cut', 'cutoff', 'cut off', 'outage', 'blackout', 'disrupt', 'shut', 'interrupt', 'halt', 
            'no supply', 'breakdown', 'leak', 'burst', 'overflow', 'clog', 'clogged', 'completely stopped', 'not coming',
            'blast', 'gayab', 'chali gayi', 'band', 'ठप', 'फूट', 'लीकेज', 'गुल', 'कटौती', 'उफन', 'चोक', 'गंदा', 'स्पार्किंग', 'धमाका'
        ]
        return any(t in text for t in essential_terms) and any(d in text for d in disruption_terms)
