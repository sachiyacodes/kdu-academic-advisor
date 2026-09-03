"""
Train the ML enhancement model.
Wrapper script for ml/train_model.py.

Usage: python scripts/train_model.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ml.train_model import train_model

if __name__ == "__main__":
    train_model()
