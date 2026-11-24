"""
SmartCivic AI — Machine Learning Model Comparison & Evaluation Suite
Compares 4 ML text classification algorithms on stratified civic complaint dataset:
1. LinearSVC with CalibratedClassifierCV (Production Primary)
2. Logistic Regression (Probabilistic Baseline)
3. Multinomial Naive Bayes (Standard NLP Baseline)
4. SGDClassifier (Hinged loss linear model)

Outputs real, reproducible metrics (Accuracy, Macro F1, Weighted F1, Precision, Recall).
Zero data fabrication. Zero data leakage.
"""

import sys
import io
import json
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_recall_fscore_support
)

from ai.training.dataset import load_dataset

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATASET_PATH = BASE_DIR / "data" / "complaints_500.csv"
OUTPUT_METRICS_PATH = BASE_DIR / "data" / "model_comparison_results.json"

def run_model_comparison(seed: int = 42) -> dict:
    print("=" * 70)
    print("SMARTCIVIC AI — MULTI-MODEL ALGORITHM BENCHMARK & EVALUATION")
    print("=" * 70)
    
    texts, labels = load_dataset(str(DATASET_PATH))
    total_samples = len(texts)
    print(f"Loaded dataset: {total_samples} samples across {len(set(labels))} civic categories.")

    # Stratified 80/20 train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, stratify=labels, random_state=seed
    )
    print(f"Training set: {len(X_train)} samples | Test set: {len(X_test)} samples (strictly held out)\n")

    candidates = {
        "LinearSVC (Calibrated)": Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000, sublinear_tf=True)),
            ('clf', CalibratedClassifierCV(LinearSVC(C=1.0, random_state=seed, class_weight='balanced', dual='auto'), cv=3))
        ]),
        "Logistic Regression": Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000, sublinear_tf=True)),
            ('clf', LogisticRegression(C=1.0, max_iter=1000, class_weight='balanced', random_state=seed))
        ]),
        "Multinomial Naive Bayes": Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
            ('clf', MultinomialNB(alpha=0.1))
        ]),
        "SGD Classifier": Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000, sublinear_tf=True)),
            ('clf', SGDClassifier(loss='modified_huber', max_iter=1000, random_state=seed, class_weight='balanced'))
        ])
    }

    results = {}
    categories = sorted(list(set(labels)))

    for name, pipeline in candidates.items():
        print(f"Training & Evaluating: {name} ...")
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        w_prec, w_rec, w_f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted', zero_division=0)
        m_prec, m_rec, m_f1, _ = precision_recall_fscore_support(y_test, y_pred, average='macro', zero_division=0)

        # 5-fold cross-validation on training set
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='accuracy')

        per_cat = {}
        p, r, f, s = precision_recall_fscore_support(y_test, y_pred, labels=categories, zero_division=0)
        for cat, pr, re, f1, sup in zip(categories, p, r, f, s):
            per_cat[cat] = {
                "precision": round(float(pr), 4),
                "recall": round(float(re), 4),
                "f1": round(float(f1), 4),
                "support": int(sup)
            }

        cm = confusion_matrix(y_test, y_pred, labels=categories).tolist()

        results[name] = {
            "test_accuracy": round(float(acc), 4),
            "cv_accuracy_mean": round(float(cv_scores.mean()), 4),
            "cv_accuracy_std": round(float(cv_scores.std()), 4),
            "weighted_precision": round(float(w_prec), 4),
            "weighted_recall": round(float(w_rec), 4),
            "weighted_f1": round(float(w_f1), 4),
            "macro_precision": round(float(m_prec), 4),
            "macro_recall": round(float(m_rec), 4),
            "macro_f1": round(float(m_f1), 4),
            "per_category": per_cat,
            "confusion_matrix": cm
        }
        print(f"   -> Test Acc: {acc:.4f} | Macro F1: {m_f1:.4f} | 5-Fold CV Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # Save benchmark metrics
    benchmark_payload = {
        "metadata": {
            "dataset": "complaints_500.csv",
            "total_samples": total_samples,
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "categories": categories,
            "random_seed": seed
        },
        "models": results
    }

    OUTPUT_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(benchmark_payload, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Model comparison report saved to: {OUTPUT_METRICS_PATH}")
    print("=" * 70)
    return benchmark_payload

if __name__ == "__main__":
    run_model_comparison()
