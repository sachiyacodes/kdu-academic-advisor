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
RF_MODEL_PATH = MODEL_DIR / "random_forest.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"


def load_synthetic_data():
    """Load synthetic student data and compute features per student with neutral baseline imputation."""
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
        all_completed_marks = []
        for course in courses:
            if course.get("status") == "completed":
                try:
                    mark = float(course["mark"])
                    area_marks[course["subject_area"]].append(mark)
                    all_completed_marks.append(mark)
                except (ValueError, KeyError):
                    continue

        # Neutral student baseline: student's own transcript mean across completed subjects
        student_mean = float(np.mean(all_completed_marks)) if all_completed_marks else 65.0

        # Build feature vector (one dimension per subject area)
        feature_vec = []
        for area in SUBJECT_AREA_ORDER:
            marks = area_marks.get(area, [])
            if marks:
                feature_vec.append(np.mean(marks))
            else:
                # Impute missing subjects with student transcript mean (not failing 0.0)
                feature_vec.append(student_mean)

        features.append(feature_vec)
        labels.append(spec_label)

    return np.array(features), np.array(labels)


def train_model():
    """Train multiple classifiers (DT, RF, GBDT) with 5-fold CV and save best models."""
    from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
    from sklearn.metrics import (
        accuracy_score,
        classification_report,
        confusion_matrix,
        f1_score,
    )
    from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
    from sklearn.tree import DecisionTreeClassifier

    print("=" * 60)
    print("ML Enhancement: Competitive Multi-Model Benchmark & Training")
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

    # 5-Fold Stratified Cross-Validation Benchmarking
    print("\n" + "-" * 50)
    print("Running 5-Fold Stratified Cross-Validation Benchmark...")
    print("-" * 50)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=ML_RANDOM_STATE)
    candidate_models = {
        "Decision Tree": DecisionTreeClassifier(
            max_depth=7, min_samples_leaf=4, random_state=ML_RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, max_depth=8, min_samples_leaf=2, random_state=ML_RANDOM_STATE
        ),
        "Gradient Boosting": HistGradientBoostingClassifier(
            max_iter=100, random_state=ML_RANDOM_STATE
        ),
    }

    benchmark_results = {}
    for name, model in candidate_models.items():
        cv_res = cross_validate(
            model, X, y, cv=cv,
            scoring=["accuracy", "f1_macro", "f1_weighted"]
        )
        acc_mean = float(np.mean(cv_res["test_accuracy"]))
        acc_std = float(np.std(cv_res["test_accuracy"]))
        f1_mean = float(np.mean(cv_res["test_f1_macro"]))
        f1_std = float(np.std(cv_res["test_f1_macro"]))
        benchmark_results[name] = {
            "cv_accuracy_mean": round(acc_mean, 4),
            "cv_accuracy_std": round(acc_std, 4),
            "cv_macro_f1_mean": round(f1_mean, 4),
            "cv_macro_f1_std": round(f1_std, 4),
        }
        print(f"  {name:18}: Acc = {acc_mean:.4f} (+/- {acc_std:.4f}), F1 = {f1_mean:.4f}")

    # Train / Test split for holdout evaluation and serialization
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=ML_TEST_SIZE, random_state=ML_RANDOM_STATE, stratify=y
    )

    # Train Decision Tree (for explainable rule pathways)
    dt_clf = DecisionTreeClassifier(
        max_depth=7, min_samples_leaf=4, random_state=ML_RANDOM_STATE
    )
    dt_clf.fit(X_train, y_train)
    dt_pred = dt_clf.predict(X_test)
    dt_acc = float(accuracy_score(y_test, dt_pred))

    # Train Random Forest (for robust ensemble predictions)
    rf_clf = RandomForestClassifier(
        n_estimators=100, max_depth=8, min_samples_leaf=2, random_state=ML_RANDOM_STATE
    )
    rf_clf.fit(X_train, y_train)
    rf_pred = rf_clf.predict(X_test)
    rf_acc = float(accuracy_score(y_test, rf_pred))
    rf_report = classification_report(y_test, rf_pred, output_dict=True)
    rf_conf = confusion_matrix(y_test, rf_pred).tolist()

    print(f"\nHoldout Test Accuracy:")
    print(f"  Decision Tree: {dt_acc:.4f}")
    print(f"  Random Forest: {rf_acc:.4f}")

    # Feature importance from Random Forest (much more reliable across all features)
    importances = rf_clf.feature_importances_
    feature_importance = {
        area: round(float(imp), 4)
        for area, imp in zip(SUBJECT_AREA_ORDER, importances)
    }

    # Save models
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(dt_clf, f)
    with open(RF_MODEL_PATH, "wb") as f:
        pickle.dump(rf_clf, f)

    # Save metrics
    metrics = {
        "accuracy": round(rf_acc, 4),
        "dt_accuracy": round(dt_acc, 4),
        "rf_accuracy": round(rf_acc, 4),
        "primary_model": "Random Forest Classifier",
        "benchmark_comparison": benchmark_results,
        "classification_report": rf_report,
        "confusion_matrix": rf_conf,
        "feature_importance": feature_importance,
        "feature_names": SUBJECT_AREA_ORDER,
        "class_labels": sorted(set(y)),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "cv_folds": 5,
        "random_state": ML_RANDOM_STATE,
        "disclaimer": SYNTHETIC_DATA_DISCLAIMER,
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nArtifacts saved in {MODEL_DIR}")
    print("[OK] Multi-model training and cross-validation complete!")
    return rf_clf, metrics


if __name__ == "__main__":
    train_model()
