"""
CivicPulse ML Model Training & Evaluation Pipeline
- Dataset: data/complaints_500.csv (500 synthetic labeled municipal complaints)
- Split: 80% Train (400), 10% Validation (50), 10% Test (50) - Stratified, Random Seed 42
- Zero Data Leakage: Test set is completely held out during training
- Models: TF-IDF (word n-grams 1-2 + char n-grams) + CalibratedClassifierCV(LinearSVC)
- Evaluates: Old Model vs New Model on the same 50 test records
- Output: Classification report, confusion matrix, per-category metrics, and explanation of weaknesses
"""

import sys
import io
import json
from pathlib import Path
from collections import Counter

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support
)

from ai.training.dataset import load_dataset
from ai.classifier import CategoryClassifier

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = BASE_DIR / "data" / "complaints_500.csv"
MODEL_PATH = BASE_DIR / "ai" / "models" / "category_classifier.joblib"
OLD_MODEL_BACKUP = BASE_DIR / "ai" / "models" / "category_classifier_old.joblib"
METRICS_OUTPUT_PATH = BASE_DIR / "data" / "model_evaluation_metrics.json"
CM_OUTPUT_PATH = BASE_DIR / "data" / "confusion_matrix.txt"

def load_and_split(seed=42):
    texts, labels = load_dataset(str(DATASET_PATH))
    assert len(texts) == 500, f"Expected 500 records, found {len(texts)}"
    
    # 80% train+val (450), 10% test (50)
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        texts, labels, test_size=0.10, stratify=labels, random_state=seed
    )
    
    # Split train_val (450) into 400 train and 50 val (50/450 = 1/9 ~ 0.1111)
    val_ratio = 50 / len(X_train_val)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, stratify=y_train_val, random_state=seed
    )
    
    assert len(X_train) == 400, f"Expected 400 train samples, got {len(X_train)}"
    assert len(X_val) == 50, f"Expected 50 val samples, got {len(X_val)}"
    assert len(X_test) == 50, f"Expected 50 test samples, got {len(X_test)}"
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def build_improved_pipeline():
    """
    Builds an improved NLP feature extractor and classifier:
    - Word n-grams (1, 2) to capture domain terms ('live wire', 'hit and run')
    - Sublinear term frequency scaling
    - Calibrated LinearSVC with balanced class weights
    """
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10000,
        sublinear_tf=True,
        min_df=1
    )
    base_svc = LinearSVC(C=1.0, random_state=42, class_weight='balanced', dual='auto')
    calibrated_clf = CalibratedClassifierCV(base_svc, cv=3)
    
    return Pipeline([
        ('tfidf', vectorizer),
        ('clf', calibrated_clf)
    ])

def evaluate_predictions(y_true, y_pred, labels_list):
    acc = accuracy_score(y_true, y_pred)
    w_prec, w_rec, w_f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    m_prec, m_rec, m_f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro', zero_division=0)
    
    per_cat = {}
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=labels_list, zero_division=0)
    for cat, pr, re, f1, sup in zip(labels_list, p, r, f, s):
        per_cat[cat] = {
            "precision": round(float(pr), 4),
            "recall": round(float(re), 4),
            "f1": round(float(f1), 4),
            "support": int(sup)
        }
        
    cm = confusion_matrix(y_true, y_pred, labels=labels_list)
    return {
        "accuracy": round(float(acc), 4),
        "weighted_precision": round(float(w_prec), 4),
        "weighted_recall": round(float(w_rec), 4),
        "weighted_f1": round(float(w_f1), 4),
        "macro_precision": round(float(m_prec), 4),
        "macro_recall": round(float(m_rec), 4),
        "macro_f1": round(float(m_f1), 4),
        "per_category": per_cat,
        "confusion_matrix": cm.tolist()
    }

def format_confusion_matrix(cm, labels):
    col_width = max(len(l[:8]) for l in labels) + 2
    row_width = max(len(l) for l in labels) + 2
    
    header = f"{'True \\ Pred':<{row_width}}" + "".join([f"{l[:8]:>{col_width}}" for l in labels])
    lines = [header, "-" * len(header)]
    for idx, row in enumerate(cm):
        r_str = f"{labels[idx]:<{row_width}}" + "".join([f"{val:>{col_width}}" for val in row])
        lines.append(r_str)
    return "\n".join(lines)

def main():
    print("==================================================================")
    print("CIVICPULSE ML PIPELINE TRAINING & HELD-OUT EVALUATION (PHASE 7-9)")
    print("==================================================================")
    
    # 1. Split data
    print(f"Loading dataset from: {DATASET_PATH}")
    X_train, X_val, X_test, y_train, y_val, y_test = load_and_split(seed=42)
    print(f"Train samples: {len(X_train)} (80%)")
    print(f"Val samples  : {len(X_val)} (10%)")
    print(f"Test samples : {len(X_test)} (10% held-out)\n")
    
    all_categories = sorted(list(set(y_train + y_val + y_test)))
    print(f"Categories ({len(all_categories)}): {', '.join(all_categories)}\n")
    
    # 2. Evaluate OLD model on test set if available
    old_results = None
    if MODEL_PATH.exists():
        print(f"Evaluating existing (OLD) model on 50 held-out test records...")
        try:
            old_model = joblib.load(MODEL_PATH)
            # Backup old model
            joblib.dump(old_model, OLD_MODEL_BACKUP)
            
            # Predict
            old_preds = [str(old_model.predict([t])[0]) for t in X_test]
            old_results = evaluate_predictions(y_test, old_preds, all_categories)
            print(f"OLD Model Test Accuracy : {old_results['accuracy']:.4f}")
            print(f"OLD Model Weighted F1   : {old_results['weighted_f1']:.4f}")
            print(f"OLD Model Macro F1      : {old_results['macro_f1']:.4f}\n")
        except Exception as e:
            print(f"Could not evaluate old model: {e}\n")

    # 3. Train NEW improved model on X_train (400 records)
    print("Training NEW Calibrated LinearSVC model on 400 training samples...")
    new_pipeline = build_improved_pipeline()
    new_pipeline.fit(X_train, y_train)
    print("Training completed successfully.")

    # 4. Evaluate on Validation Set (50 records)
    val_preds = [str(new_pipeline.predict([t])[0]) for t in X_val]
    val_results = evaluate_predictions(y_val, val_preds, all_categories)
    print(f"\nValidation Set Accuracy : {val_results['accuracy']:.4f}")
    print(f"Validation Set Weighted F1: {val_results['weighted_f1']:.4f}")

    # 5. Evaluate on Held-Out Test Set (50 records)
    print("\n------------------------------------------------------------------")
    print("EVALUATING NEW MODEL ON 50 HELD-OUT TEST SAMPLES")
    print("------------------------------------------------------------------")
    new_preds = [str(new_pipeline.predict([t])[0]) for t in X_test]
    new_results = evaluate_predictions(y_test, new_preds, all_categories)
    
    print(f"NEW Model Test Accuracy : {new_results['accuracy']:.4f}")
    print(f"NEW Model Weighted Prec : {new_results['weighted_precision']:.4f}")
    print(f"NEW Model Weighted Rec  : {new_results['weighted_recall']:.4f}")
    print(f"NEW Model Weighted F1   : {new_results['weighted_f1']:.4f}")
    print(f"NEW Model Macro F1      : {new_results['macro_f1']:.4f}\n")

    print("--- Per-Category Classification Report ---")
    print(classification_report(y_test, new_preds, target_names=all_categories, zero_division=0))

    cm_formatted = format_confusion_matrix(np.array(new_results['confusion_matrix']), all_categories)
    print("--- Confusion Matrix (Held-out Test Set) ---")
    print(cm_formatted)
    
    # Save Confusion Matrix to file
    CM_OUTPUT_PATH.write_text(cm_formatted, encoding="utf-8")
    print(f"\nSaved confusion matrix to: {CM_OUTPUT_PATH}")

    # 6. Save newly trained model
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(new_pipeline, MODEL_PATH)
    print(f"Saved new model to: {MODEL_PATH}")

    # 7. Identify weak categories
    print("\n--- Model Error Analysis & Weak Categories ---")
    weak_categories = []
    for cat, metrics in new_results['per_category'].items():
        if metrics['support'] > 0 and (metrics['f1'] < 0.70 or metrics['recall'] < 0.60):
            weak_categories.append((cat, metrics))
            print(f"  [WEAK] {cat}: F1={metrics['f1']:.2f}, Recall={metrics['recall']:.2f}, Support={metrics['support']}")
    
    if not weak_categories:
        print("  All categories in test set achieved >= 0.70 F1 score.")

    # 8. Comparison summary
    print("\n==================================================================")
    print("MODEL PERFORMANCE COMPARISON (TEST SET N=50)")
    print("==================================================================")
    if old_results:
        print(f"Metric               | Old Model | New Model | Delta")
        print(f"---------------------|-----------|-----------|-------")
        print(f"Accuracy             | {old_results['accuracy']:<9.4f} | {new_results['accuracy']:<9.4f} | {new_results['accuracy'] - old_results['accuracy']:+.4f}")
        print(f"Weighted Precision   | {old_results['weighted_precision']:<9.4f} | {new_results['weighted_precision']:<9.4f} | {new_results['weighted_precision'] - old_results['weighted_precision']:+.4f}")
        print(f"Weighted Recall      | {old_results['weighted_recall']:<9.4f} | {new_results['weighted_recall']:<9.4f} | {new_results['weighted_recall'] - old_results['weighted_recall']:+.4f}")
        print(f"Weighted F1-Score    | {old_results['weighted_f1']:<9.4f} | {new_results['weighted_f1']:<9.4f} | {new_results['weighted_f1'] - old_results['weighted_f1']:+.4f}")
        print(f"Macro F1-Score       | {old_results['macro_f1']:<9.4f} | {new_results['macro_f1']:<9.4f} | {new_results['macro_f1'] - old_results['macro_f1']:+.4f}")
    else:
        print(f"New Model Test Accuracy: {new_results['accuracy']:.4f}")
        print(f"New Model Weighted F1  : {new_results['weighted_f1']:.4f}")

    # 9. Save metrics JSON
    output_data = {
        "dataset": {
            "total_records": 500,
            "train_records": 400,
            "val_records": 50,
            "test_records": 50,
            "seed": 42
        },
        "old_model": old_results,
        "new_model": new_results,
        "weak_categories": [w[0] for w in weak_categories]
    }
    with open(METRICS_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)
    print(f"\nSaved evaluation metrics to: {METRICS_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
