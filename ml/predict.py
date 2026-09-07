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
from typing import Any, Dict, List, Optional, Tuple

try:
    import numpy as np
except ImportError:
    np = None

from src.config.settings import SUBJECT_AREA_ORDER, SYNTHETIC_DATA_DISCLAIMER

MODEL_DIR = Path(__file__).parent / "models"
MODEL_PATH = MODEL_DIR / "decision_tree.pkl"
RF_MODEL_PATH = MODEL_DIR / "random_forest.pkl"
JSON_MODEL_PATH = MODEL_DIR / "model_trees.json"
METRICS_PATH = MODEL_DIR / "metrics.json"

_CACHED_JSON_MODEL = None


def load_json_model() -> Optional[Dict[str, Any]]:
    """Load the pre-exported lightweight tree ensemble for zero-dependency inference."""
    global _CACHED_JSON_MODEL
    if _CACHED_JSON_MODEL is not None:
        return _CACHED_JSON_MODEL
    if JSON_MODEL_PATH.exists():
        with open(JSON_MODEL_PATH, "r", encoding="utf-8") as f:
            _CACHED_JSON_MODEL = json.load(f)
            return _CACHED_JSON_MODEL
    return None


def is_model_available() -> bool:
    """Check if trained models exist."""
    return JSON_MODEL_PATH.exists() or MODEL_PATH.exists() or RF_MODEL_PATH.exists()


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


def _predict_tree(tree_data: Dict[str, Any], x: List[float]) -> List[float]:
    """Pure-Python decision tree traversal with no external C/scikit-learn dependencies."""
    node = 0
    left_children = tree_data["children_left"]
    right_children = tree_data["children_right"]
    features = tree_data["feature"]
    thresholds = tree_data["threshold"]
    values = tree_data["value"]

    while left_children[node] != right_children[node]:
        feat = features[node]
        thresh = thresholds[node]
        if x[feat] <= thresh:
            node = left_children[node]
        else:
            node = right_children[node]
    counts = values[node][0]
    total = sum(counts)
    return [c / total if total > 0 else 0.0 for c in counts]


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
    # Calculate student baseline mean across available subjects
    valid_marks = [m for m in subject_area_averages.values() if m is not None and m >= 0]
    student_mean = float(sum(valid_marks) / len(valid_marks)) if valid_marks else 65.0

    # Build feature vector: impute missing subjects with student mean (not 0.0)
    feature_vec = [
        float(subject_area_averages.get(area, student_mean))
        for area in SUBJECT_AREA_ORDER
    ]

    # 1. Zero-dependency pure Python JSON model inference
    json_model = load_json_model()
    if json_model is not None and model_name in json_model:
        classes = json_model["classes"]
        trees_or_tree = json_model[model_name]

        if model_name == "random_forest":
            all_probs = [_predict_tree(t, feature_vec) for t in trees_or_tree]
            num_trees = len(all_probs)
            num_classes = len(classes)
            avg_probs = [
                sum(p[i] for p in all_probs) / num_trees
                for i in range(num_classes)
            ]
        else:
            avg_probs = _predict_tree(trees_or_tree, feature_vec)

        best_idx = max(range(len(classes)), key=lambda i: avg_probs[i])
        prediction = str(classes[best_idx])
        prob_dict = {
            str(classes[i]): round(float(avg_probs[i]), 4)
            for i in range(len(classes))
        }
        return prediction, prob_dict

    # 2. Fallback to pickle model if JSON is not present and scikit-learn/numpy are available
    model = load_model(model_name)
    if model is None:
        model = load_model("decision_tree")
    if model is None or np is None:
        return None

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
    known_subject_count = len([m for m in subject_area_averages.values() if m is not None and m >= 0])

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
