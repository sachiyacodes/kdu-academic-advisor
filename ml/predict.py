"""
ML Prediction module — uses the trained Decision Tree to predict specialization.

This is an EXPERIMENTAL cross-check against the core recommendation engine.
It is shown alongside (not instead of) the explainable rule/weighted-sum results.

Limitations:
- Trained on synthetic data — cannot establish real-world effectiveness.
- "Experimental comparison" label must always be visible.
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from src.config.settings import SUBJECT_AREA_ORDER, SYNTHETIC_DATA_DISCLAIMER

MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "decision_tree.pkl"
RF_MODEL_PATH = MODEL_DIR / "random_forest.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"


def is_model_available() -> bool:
    """Check if trained models exist."""
    return MODEL_PATH.exists() or RF_MODEL_PATH.exists()


def load_model(model_name: str = "random_forest"):
    """Load the trained model (Random Forest by default, or Decision Tree)."""
    target_path = RF_MODEL_PATH if model_name == "random_forest" and RF_MODEL_PATH.exists() else MODEL_PATH
    if not target_path.exists():
        return None
    with open(target_path, "rb") as f:
        return pickle.load(f)


def load_metrics() -> Optional[Dict]:
    """Load saved training metrics."""
    if not METRICS_PATH.exists():
        return None
    with open(METRICS_PATH, "r") as f:
        return json.load(f)


def predict_specialization(
    subject_area_averages: Dict[str, float],
    model_name: str = "random_forest",
) -> Optional[Tuple[str, Dict[str, float]]]:
    """
    Predict the most likely specialization using trained machine learning.
    Uses transcript-mean imputation for uncompleted subjects rather than failing 0.0.

    Args:
        subject_area_averages: {subject_area_name: average_mark} from student profile.
        model_name: "random_forest" (primary ensemble) or "decision_tree" (rule-based).

    Returns:
        Tuple of (predicted_specialization, class_probabilities) or None if model unavailable.
    """
    model = load_model(model_name)
    if model is None:
        model = load_model("decision_tree")
    if model is None:
        return None

    # Calculate student baseline mean across available subjects
    valid_marks = [m for m in subject_area_averages.values() if m is not None and m > 0]
    student_mean = float(np.mean(valid_marks)) if valid_marks else 65.0

    # Build feature vector: impute missing subjects with student mean (not 0.0)
    feature_vec = []
    for area in SUBJECT_AREA_ORDER:
        feature_vec.append(subject_area_averages.get(area, student_mean))

    X = np.array([feature_vec])

    # Predict
    prediction = str(model.predict(X)[0])

    # Get probabilities
    probabilities = model.predict_proba(X)[0]
    class_labels = [str(c) for c in model.classes_]
    prob_dict = {
        label: round(float(prob), 4)
        for label, prob in zip(class_labels, probabilities)
    }

    return prediction, prob_dict


def predict_with_consensus(
    subject_area_averages: Dict[str, float],
) -> Optional[Dict[str, Any]]:
    """
    Generate predictions from both Random Forest and Decision Tree to evaluate consensus.
    Also computes a confidence flag (e.g., Preliminary for sparse data or low probabilities).
    """
    rf_res = predict_specialization(subject_area_averages, model_name="random_forest")
    dt_res = predict_specialization(subject_area_averages, model_name="decision_tree")

    if not rf_res:
        return None

    rf_pred, rf_probs = rf_res
    dt_pred = dt_res[0] if dt_res else rf_pred

    # Confidence check
    top_prob = max(rf_probs.values()) if rf_probs else 0.0
    known_subject_count = len([m for m in subject_area_averages.values() if m is not None and m > 0])

    is_preliminary = known_subject_count < 3 or top_prob < 0.35
    confidence_label = "Preliminary / Limited" if is_preliminary else ("High Confidence" if top_prob >= 0.50 else "Moderate Confidence")

    return {
        "prediction": rf_pred,
        "probabilities": rf_probs,
        "dt_prediction": dt_pred,
        "consensus": rf_pred == dt_pred,
        "top_probability": top_prob,
        "confidence_label": confidence_label,
        "is_preliminary": is_preliminary,
        "known_subject_count": known_subject_count,
    }
