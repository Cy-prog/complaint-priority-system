import sys
from pathlib import Path
import json

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

try:
    from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
    from sklearn.model_selection import cross_val_score, StratifiedKFold
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from ..classifier import CategoryClassifier
from ..pipeline import get_pipeline
from .dataset import load_dataset, split_dataset

def evaluate_classifier(model_path, test_data_path):
    print("==================================================")
    print("EVALUATING HYBRID CATEGORY CLASSIFIER")
    print("==================================================")
    if not SKLEARN_AVAILABLE:
        print("scikit-learn required for detailed evaluation.")
        return {}
        
    texts, labels = load_dataset(test_data_path)
    X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(texts, labels, test_size=0.2, val_size=0.1)
    
    if not X_test:
        print("No test data found.")
        return {}
        
    classifier = CategoryClassifier()
    
    predictions = []
    confidences = []
    for text in X_test:
        pred, conf = classifier.predict(text)
        predictions.append(pred)
        confidences.append(conf)
        
    acc = accuracy_score(y_test, predictions)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, predictions, average='weighted', zero_division=0)
    
    unique_labels = sorted(list(set(y_test + predictions)))
    cm = confusion_matrix(y_test, predictions, labels=unique_labels)
    
    print("\n--- CLASSIFICATION REPORT (Test Set, N={}) ---".format(len(y_test)))
    print(classification_report(y_test, predictions, zero_division=0))
    
    print("\n--- CONFUSION MATRIX ---")
    header = f"{'True \\ Pred':<16}" + "".join([f"{l[:6]:>8}" for l in unique_labels])
    print(header)
    print("-" * len(header))
    for idx, row in enumerate(cm):
        row_str = f"{unique_labels[idx]:<16}" + "".join([f"{val:>8}" for val in row])
        print(row_str)

    print(f"\nAverage Model Confidence on Test Set: {sum(confidences)/len(confidences):.4f}")

    # 5-Fold Cross Validation on the entire dataset
    print("\n--- 5-FOLD STRATIFIED CROSS-VALIDATION ---")
    if classifier.model:
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        cv_scores = cross_val_score(classifier.model, texts, labels, cv=skf, scoring='accuracy')
        print(f"Fold Accuracies: {[round(s, 4) for s in cv_scores]}")
        print(f"Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "test_samples": len(y_test),
        "total_samples": len(texts)
    }

def evaluate_hit_and_run_benchmark():
    print("\n==================================================")
    print("HIT-AND-RUN BENCHMARK TEST CASE")
    print("==================================================")
    pipeline = get_pipeline()
    
    query = (
        "A black SUV hit a pedestrian near the railway station around 8:30 PM and escaped "
        "toward the highway. The person appears to be injured. I could only see part of the number plate MP07 AB 2."
    )
    print(f"Input Complaint: \"{query}\"\n")
    
    res = pipeline.analyze(query)
    ent = res.entities[0] if res.entities else {}
    
    print(f"Predicted Category: {res.category} (Confidence: {res.confidence:.2f})")
    print(f"Predicted Priority: {res.priority} (Score: {res.priority_score})")
    print(f"Incident Type: {ent.get('incident_type')}")
    print(f"Vehicle Type: {ent.get('vehicle', {}).get('type')}")
    print(f"Vehicle Color: {ent.get('vehicle', {}).get('color')}")
    print(f"Vehicle Plate: {ent.get('vehicle', {}).get('plate')}")
    print(f"Location: {ent.get('locations')}")
    print(f"Approximate Time: {ent.get('approximate_time')}")
    print(f"Direction of Travel: {ent.get('direction_of_travel')}")
    print(f"Injury Reported: {ent.get('injury_reported')}")
    print(f"Safety Risk Level: {res.risk_level}")
    print(f"Machine-Readable Reasons: {res.key_issues}")
    print(f"Reasoning Summary: {res.reasoning_summary}\n")
    
    # Assertions
    checks = [
        ("Category == Public Safety", res.category == "Public Safety"),
        ("Incident == HIT_AND_RUN", ent.get('incident_type') == "HIT_AND_RUN"),
        ("Vehicle Type == SUV", ent.get('vehicle', {}).get('type') == "SUV"),
        ("Vehicle Color == BLACK", ent.get('vehicle', {}).get('color') == "BLACK"),
        ("Vehicle Plate == MP07 AB 2", ent.get('vehicle', {}).get('plate') == "MP07 AB 2"),
        ("Injury Reported == True", ent.get('injury_reported') is True),
        ("Priority == CRITICAL", res.priority == "CRITICAL")
    ]
    
    all_passed = True
    for name, passed in checks:
        status = "PASSED" if passed else "FAILED"
        if not passed:
            all_passed = False
        print(f"  [{status}] {name}")
        
    return all_passed

def evaluate_domain_test_cases():
    print("\n==================================================")
    print("DOMAIN & RISK LEVEL COMPREHENSIVE TESTS")
    print("==================================================")
    pipeline = get_pipeline()
    
    test_cases = [
        # (Category, Text, Expected Priority, Description)
        ("Public Safety", "There is a massive fire near the hospital. Send fire brigade immediately!", "CRITICAL", "Fire Emergency (High Risk)"),
        ("Public Safety", "Armed robbery at jewelry store, suspects had guns and fled toward highway.", "CRITICAL", "Armed Robbery (High Risk)"),
        ("Electricity", "Exposed live 440V electrical wire snapped and hanging low near school gate.", "CRITICAL", "Active Live Wire Hazard"),
        ("Water Supply", "Pipes leaking potable water from tap for 2 hours on private lawn.", "LOW", "Minor Water Leakage (Low Risk)"),
        ("Water Supply", "Severe sewage mixing in drinking water, children vomiting blood and hospitalized.", "CRITICAL", "Severe Water Contamination"),
        ("Electricity", "No electricity in the entire colony for 5 days. We are struggling in heat.", "HIGH", "Prolonged Power Cut (5 days)"),
        ("Garbage/Waste", "Dead stray cow lying on street for 4 days, unbearable stench and flies.", "HIGH", "Dead Animal Hazard"),
        ("Sanitation", "Open manhole on main road with no cover, deep pit.", "CRITICAL", "Open Manhole Safety Hazard"),
        ("Parks", "Swing in colony park is rusty and grass is slightly long.", "LOW", "Park Maintenance (Low Risk)"),
        ("Public Safety (Hindi)", "काले रंग की गाड़ी ने टक्कर मार दी और भाग गया, व्यक्ति गंभीर रूप से घायल है।", "CRITICAL", "Hindi Hit-and-Run"),
        ("Water Supply (Hindi)", "हमारे मोहल्ले में 4 दिन से पीने का पानी नहीं आया है।", "HIGH", "Hindi Water Supply 4 Days"),
        ("Electricity (Hinglish)", "Sir transformer blast ho gaya hai, light kal raat se gayab hai.", "CRITICAL", "Hinglish Transformer Blast Hazard"),
        ("Other", "I am angry that my birth certificate application status is still pending.", "LOW", "Routine Administrative Delay"),
    ]
    
    passed = 0
    for cat, text, expected_prio, desc in test_cases:
        res = pipeline.analyze(text)
        match = res.priority == expected_prio
        if match:
            passed += 1
        status = "PASS" if match else "FAIL"
        print(f"[{status}] {desc}")
        print(f"       Text: \"{text[:70]}...\"")
        print(f"       Expected: {expected_prio}, Got: {res.priority} (Category: {res.category}, Score: {res.priority_score})\n")
        
    print(f"Domain & Risk Test Results: {passed}/{len(test_cases)} passed.")
    return passed == len(test_cases)

if __name__ == "__main__":
    data_path = str(Path(__file__).parent.parent.parent / "data" / "synthetic_complaints.json")
    model_path = str(Path(__file__).parent.parent / "models" / "category_classifier.joblib")
    
    metrics = evaluate_classifier(model_path, data_path)
    evaluate_hit_and_run_benchmark()
    evaluate_domain_test_cases()
