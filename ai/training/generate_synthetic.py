import json
import random
from pathlib import Path

def generate_complaints(n: int = 500) -> list[dict]:
    categories = ["Water Supply", "Electricity", "Roads", "Waste Management", "Public Health", "Other"]
    priorities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    locations = ["Ward 1", "Ward 2", "MG Road Area", "Civil Lines", "Green Park Colony"]
    languages = ["en", "hi", "hinglish"]
    
    complaints = []
    
    # Pre-defined edge cases
    edge_cases = [
        {"text": "Everything is fine now.", "category": "Other", "priority": "LOW"},
        {"text": "URGENT!!!", "category": "Other", "priority": "HIGH"},
        {"text": "There is a broken streetlight.", "category": "Electricity", "priority": "LOW"},
        {"text": "There is an exposed live electrical wire near a school.", "category": "Electricity", "priority": "CRITICAL"},
        {"text": "Water has been unavailable for 5 days.", "category": "Water Supply", "priority": "HIGH"},
        {"text": "Someone already reported this yesterday.", "category": "Other", "priority": "LOW"},
    ]
    
    complaints.extend(edge_cases)
    
    templates = [
        "The {category} has been an issue for {duration}. Please fix it in {location}.",
        "We are facing severe problems with {category} in {location}. {population} are affected.",
        "No {category} since {duration}!! This is the third time I am reporting. {location}.",
        "There is a major {category} problem. {safety}!! We need help in {location}.",
        "Small issue with {category} at {location}."
    ]
    
    durations = ["2 days", "5 days", "1 week", "3 hours", "1 month"]
    populations = ["50 families", "100 households", "entire society"]
    safety_hazards = ["Fire hazard", "People are getting sick", "Exposed wire", "Accident risk"]
    
    while len(complaints) < n:
        cat = random.choice(categories)
        prio = random.choice(priorities)
        loc = random.choice(locations)
        dur = random.choice(durations)
        pop = random.choice(populations)
        safe = random.choice(safety_hazards)
        lang = random.choices(languages, weights=[0.8, 0.1, 0.1])[0]
        
        template = random.choice(templates)
        text = template.format(category=cat.lower(), location=loc, duration=dur, population=pop, safety=safe)
        
        # Add some hinglish variation randomly
        if lang == "hinglish":
            text = text.replace("problem", "dikkat").replace("water", "paani").replace("electricity", "bijli")
            
        complaints.append({
            "text": text,
            "category": cat,
            "priority": prio,
            "location": {"ward": loc},
            "language": lang
        })
        
    return complaints

def save_to_json(complaints: list[dict], path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(complaints, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    out_path = Path(__file__).parent.parent.parent / "data" / "synthetic_complaints.json"
    data = generate_complaints(500)
    save_to_json(data, str(out_path))
    print(f"Generated {len(data)} synthetic complaints at {out_path}")
