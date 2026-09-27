import json
from collections import Counter

try:
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

def load_dataset(path: str) -> tuple[list[str], list[str]]:
    try:
        if path.endswith(".csv"):
            import csv
            texts, labels = [], []
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    txt = row.get("complaint_text") or row.get("text")
                    cat = row.get("category")
                    if txt and cat:
                        texts.append(txt)
                        labels.append(cat)
            return texts, labels

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        texts = []
        labels = []
        for item in data:
            txt = item.get("complaint_text") or item.get("text")
            cat = item.get("category")
            if txt and cat:
                texts.append(txt)
                labels.append(cat)
                
        return texts, labels
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return [], []

def split_dataset(texts: list[str], labels: list[str], test_size=0.2, val_size=0.1):
    if not SKLEARN_AVAILABLE:
        print("scikit-learn required for splitting. Returning unsplit data.")
        return texts, [], [], labels, [], []
        
    if not texts or not labels:
        return [], [], [], [], [], []

    # Simple stratified split
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        texts, labels, test_size=test_size, stratify=labels, random_state=42
    )
    
    val_ratio = val_size / (1.0 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, stratify=y_train_val, random_state=42
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def analyze_dataset(texts: list[str], labels: list[str]):
    print(f"Total samples: {len(texts)}")
    
    class_counts = Counter(labels)
    print("\nClass Distribution:")
    for cls, count in class_counts.most_common():
        print(f"  {cls}: {count} ({count/len(texts)*100:.1f}%)")
        
    lengths = [len(t.split()) for t in texts]
    if lengths:
        print(f"\nText Lengths (words):")
        print(f"  Min: {min(lengths)}")
        print(f"  Max: {max(lengths)}")
        print(f"  Avg: {sum(lengths)/len(lengths):.1f}")
        
    unique_texts = set(texts)
    print(f"\nUnique texts: {len(unique_texts)}")
    print(f"Duplicates: {len(texts) - len(unique_texts)}")
