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
METRICS_PATH = MODEL_DIR / "metrics.json"


def is_model_available() -> bool:
    """Check if a trained model exists."""
    return MODEL_PATH.exists()


def load_model():
    """Load the trained Decision Tree model."""
    if not MODEL_PATH.exists():
        return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def load_metrics() -> Optional[Dict]:
    """Load saved training metrics."""
    if not METRICS_PATH.exists():
        return None
    with open(METRICS_PATH, "r") as f:
        return json.load(f)


def predict_specialization(
    subject_area_averages: Dict[str, float],
) -> Optional[Tuple[str, Dict[str, float]]]:
    """
    Predict the most likely specialization using the Decision Tree.

    Args:
        subject_area_averages: {subject_area_name: average_mark} from student profile.

    Returns:
        Tuple of (predicted_specialization, class_probabilities) or None if model unavailable.

    Note: This is an EXPERIMENTAL prediction. The core recommendation engine
    (rule-based + weighted scoring + interest matching) is the authoritative output.
    """
    model = load_model()
    if model is None:
        return None

    # Build feature vector
    feature_vec = []
    for area in SUBJECT_AREA_ORDER:
        feature_vec.append(subject_area_averages.get(area, 0.0))

    X = np.array([feature_vec])

    # Predict
    prediction = model.predict(X)[0]

    # Get probabilities
    probabilities = model.predict_proba(X)[0]
    class_labels = model.classes_
    prob_dict = {
        label: round(float(prob), 4)
        for label, prob in zip(class_labels, probabilities)
    }

    return prediction, prob_dict
