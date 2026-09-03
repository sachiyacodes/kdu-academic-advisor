# Architecture

## System Overview

The AI-Based IT Specialization & Course Recommendation System is a student-facing academic decision-support prototype built with Python and Streamlit.

## Architecture Diagram

The system follows a layered architecture:

```
+------------------------------------------------------------------+
|                     STREAMLIT UI LAYER                            |
|  app.py (Dashboard) | pages/01-06 (Multi-page navigation)       |
|  src/ui/components.py | src/ui/styles.py                        |
+------------------------------------------------------------------+
                              |
+------------------------------------------------------------------+
|                    AI ENGINE LAYER                                |
|  src/ai/rule_engine.py          (AI Concept 1: Rules)           |
|  src/ai/weighted_scoring.py     (AI Concept 2: Weights)         |
|  src/ai/interest_matching.py    (AI Concept 3: Interests)       |
|  src/ai/recommendation_engine.py (Hybrid 70/30 Combiner)        |
|  src/ai/explanations.py        (Explainable Recommendations)    |
+------------------------------------------------------------------+
                              |
+------------------------------------------------------------------+
|                  ACADEMIC ENGINE LAYER                            |
|  src/academic/grading.py   (Mark -> Grade -> Grade Point)       |
|  src/academic/gpa.py       (GPA Calculation)                    |
|  src/academic/profile.py   (Profile Construction)               |
+------------------------------------------------------------------+
                              |
+------------------------------------------------------------------+
|                    DATA ACCESS LAYER                              |
|  src/data/database.py      (SQLite queries, parameterized)      |
|  src/config/settings.py    (Constants, enums, weights)          |
|  src/models/schemas.py     (Data models)                        |
+------------------------------------------------------------------+
                              |
+------------------------------------------------------------------+
|                   PERSISTENCE LAYER                               |
|  data/*.csv                (Source of truth - static data)       |
|  database/academic.db      (SQLite - runtime queries)           |
|  scripts/seed_database.py  (CSV -> SQLite ETL)                  |
+------------------------------------------------------------------+
                              |
+------------------------------------------------------------------+
|                ML ENHANCEMENT (EXPERIMENTAL)                      |
|  ml/train_model.py         (Decision Tree training)             |
|  ml/predict.py             (Prediction interface)               |
|  ml/models/                (Saved model + metrics)              |
+------------------------------------------------------------------+
```

## Recommendation Pipeline (Section 22)

```
Student Input (degree, year, semester, courses, interests)
      |
Input Validation (Pydantic models, range checks)
      |
Academic Profile Construction (aggregate by subject area)
      |
GPA / Grade Calculation (mark -> grade -> grade point -> GPA)
      |
Academic Stage Detection (credit-based stage classification)
      |
Rule-Based Eligibility (prerequisites + stage checks)
      |
Weighted Academic Scoring (specialization-specific weights, renormalization)
      |
Content-Based Interest Matching (cosine similarity over taxonomy)
      |
Hybrid Compatibility Calculation (70/30 configurable split)
      |
Evidence-Level Calculation (Limited/Moderate/Strong)
      |
Ranking (by final compatibility score, descending)
      |
Explainable Recommendations (dynamic text from calculations)
      |
Course Recommendations (Recommended Now / Later / Low Priority)
      |
Visual Analysis (Plotly charts: comparison, strengths, breakdown)
```

## Data Flow

```
                CSV Files (data/)
                     |
              seed_database.py
                     |
               SQLite Database
                     |
    +----------------+----------------+
    |                                 |
  database.py                   generate_dataset.py
  (runtime queries)             (synthetic students)
    |                                 |
  Academic Engine                train_model.py
  (grading, GPA, profile)       (Decision Tree)
    |                                 |
  AI Engine                     predict.py
  (rules, scoring,             (ML predictions)
   interests, hybrid)                |
    |                                 |
  Recommendation Engine -------> ML Enhancement
  (combine + rank)              (experimental cross-check)
    |
  Explanations Engine
  (dynamic text generation)
    |
  Streamlit UI
  (dashboard, pages, charts)
```

## Key Design Decisions

1. **CSV as source of truth** — Easy to hand-edit for viva demonstrations
2. **SQLite as runtime store** — Single query path, no dual-source ambiguity
3. **Single SubjectArea enum** — Canonical taxonomy enforced everywhere
4. **Configurable weights** — 70/30 split and all thresholds in one settings file
5. **Renormalization for missing data** — Never treats absent evidence as zero
6. **Cosine similarity for interests** — Handles different vector magnitudes
7. **Decision Tree for ML** — Most explainable, easiest to defend in viva
