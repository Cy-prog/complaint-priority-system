import sys
from pathlib import Path
from .dataset import load_dataset, split_dataset
from ..classifier import CategoryClassifier

def main():
    print("Starting classifier training...")
    
    data_path = Path(__file__).parent.parent.parent / "data" / "synthetic_complaints.json"
    if not data_path.exists():
        print(f"Error: Dataset not found at {data_path}")
        print("Run generate_synthetic.py first.")
        sys.exit(1)
        
    texts, labels = load_dataset(str(data_path))
    print(f"Loaded {len(texts)} samples.")
    
    X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(texts, labels)
    
    if not X_train:
        print("Failed to split dataset. Exiting.")
        sys.exit(1)
        
    print(f"Training on {len(X_train)} samples...")
    
    classifier = CategoryClassifier()
    classifier.train(X_train, y_train)
    
    print("Training complete. Model saved.")
    
    # Simple eval on val set
    correct = 0
    for text, true_label in zip(X_val, y_val):
        pred, conf = classifier.predict(text)
        if pred == true_label:
            correct += 1
            
    accuracy = correct / len(X_val) if X_val else 0
    print(f"Validation Accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()
