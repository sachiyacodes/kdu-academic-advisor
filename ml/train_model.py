"""
ML Enhancement — Decision Tree Classifier (FIX-4, section 25).

MANDATORY-BUT-SCOPED: This is one small, well-tested ML component serving
as an experimental cross-check against the rule/weighted-sum engine.
It is NOT a replacement for the three core AI techniques.

Model: Decision Tree (most explainable, easiest to defend in a viva).
Question: Predict a student's most likely successful specialization from
          their academic profile.

Limitations:
- Trained on SYNTHETIC data — results cannot establish real-world effectiveness.
- Always shown as "Experimental comparison / enhancement."
- Never silently replaces the explainable recommendation engine.
"""

import csv
import os
import sys
import json
import pickle
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config.settings import (
    ML_RANDOM_STATE,
    ML_TEST_SIZE,
    SPECIALIZATION_WEIGHTS,
    SUBJECT_AREA_ORDER,
    SYNTHETIC_DATA_DISCLAIMER,
    SubjectArea,
)


DATA_FILE = PROJECT_ROOT / "data" / "synthetic_students.csv"
MODEL_DIR = PROJECT_ROOT / "ml" / "models"
MODEL_PATH = MODEL_DIR / "decision_tree.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"


def load_synthetic_data():
    """Load synthetic student data and compute features per student."""
    if not DATA_FILE.exists():
        print(f"ERROR: {DATA_FILE} not found. Run scripts/generate_dataset.py first.")
        return None, None

    # Read all records
    records = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    # Group by student
    students = defaultdict(list)
    student_archetypes = {}
    for record in records:
        sid = int(record["student_id"])
        students[sid].append(record)
        student_archetypes[sid] = record.get("archetype", "balanced")

    # Build feature vectors: average mark per subject area
    features = []
    labels = []

    # Map archetype to specialization label for supervised learning
    archetype_to_spec = {
        "data_science": "Data Science",
        "ai_ml": "Artificial Intelligence / Machine Learning",
        "cyber_security": "Cyber Security",
        "software_engineering": "Software Engineering",
        "networking_cloud": "Networking & Cloud Computing",
        "database_engineering": "Database & Data Engineering",
        "balanced": None,  # Skip — no clear target
        "struggling": None,  # Skip — no clear target
    }

    for sid, courses in students.items():
        archetype = student_archetypes.get(sid, "balanced")
        spec_label = archetype_to_spec.get(archetype)

        if spec_label is None:
            continue  # Skip ambiguous archetypes

        # Compute features: average mark per subject area
        area_marks = defaultdict(list)
        for course in courses:
            if course.get("status") == "completed":
                try:
                    mark = float(course["mark"])
                    area_marks[course["subject_area"]].append(mark)
                except (ValueError, KeyError):
                    continue

        # Build feature vector (one dimension per subject area)
        feature_vec = []
        for area in SUBJECT_AREA_ORDER:
            marks = area_marks.get(area, [])
            if marks:
                feature_vec.append(np.mean(marks))
            else:
                feature_vec.append(0.0)  # No data for this area

        features.append(feature_vec)
        labels.append(spec_label)

    return np.array(features), np.array(labels)


def train_model():
    """Train a Decision Tree classifier and save it."""
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import (
        accuracy_score,
        classification_report,
        confusion_matrix,
    )

    print("=" * 60)
    print("ML Enhancement: Decision Tree Classifier Training")
    print("=" * 60)
    print(f"\n{SYNTHETIC_DATA_DISCLAIMER}\n")

    # Load data
    X, y = load_synthetic_data()
    if X is None:
        return

    print(f"Dataset: {len(X)} students with clear specialization archetypes")
    print(f"Features: {len(SUBJECT_AREA_ORDER)} subject area average marks")
    print(f"Classes: {len(set(y))} specializations")

    # Class distribution
    print("\nClass distribution:")
    for label, count in sorted(Counter(y).items()):
        print(f"  {label}: {count}")

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=ML_TEST_SIZE, random_state=ML_RANDOM_STATE, stratify=y
    )
    print(f"\nTrain/Test split: {len(X_train)}/{len(X_test)} "
          f"(test_size={ML_TEST_SIZE}, random_state={ML_RANDOM_STATE})")

    # Train
    clf = DecisionTreeClassifier(
        max_depth=8,
        min_samples_leaf=5,
        random_state=ML_RANDOM_STATE,
    )
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()

    print(f"\nAccuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Feature importance
    importances = clf.feature_importances_
    feature_importance = {
        area: round(float(imp), 4)
        for area, imp in zip(SUBJECT_AREA_ORDER, importances)
        if imp > 0.01
    }
    print("Feature Importance (top features):")
    for area, imp in sorted(feature_importance.items(), key=lambda x: -x[1]):
        print(f"  {area}: {imp:.4f}")

    # Save model
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
    print(f"\nModel saved: {MODEL_PATH}")

    # Save metrics
    metrics = {
        "accuracy": round(accuracy, 4),
        "classification_report": report,
        "confusion_matrix": conf_matrix,
        "feature_importance": feature_importance,
        "feature_names": SUBJECT_AREA_ORDER,
        "class_labels": sorted(set(y)),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "max_depth": 8,
        "min_samples_leaf": 5,
        "random_state": ML_RANDOM_STATE,
        "disclaimer": SYNTHETIC_DATA_DISCLAIMER,
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved: {METRICS_PATH}")

    print("\n[OK] Training complete!")
    return clf, metrics


if __name__ == "__main__":
    train_model()
