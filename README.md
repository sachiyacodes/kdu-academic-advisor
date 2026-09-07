# AI-Based IT Specialization & Course Recommendation System

**KDU — IT3182 Essentials of Artificial Intelligence — Group 22**

An AI-powered academic decision-support prototype that recommends suitable IT specializations and courses based on a student's academic performance, completed courses, prerequisites, academic stage, and interests.

> **Disclaimer:** This system provides academic decision support based on the information entered by the student and the prototype's predefined rules and weighting model. Recommendations are not guaranteed outcomes and should not replace official academic guidance. The grading scale and curriculum data used in this prototype are illustrative and may not represent official KDU academic policies.

---

## Quick Start

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate (Windows)
.venv\Scripts\activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Seed the database (CSV -> SQLite)
python scripts/seed_database.py

# 5. Run tests (172 tests passing)
python -m pytest tests/ -v

# 6. Run local backend (optional)
uvicorn api.index:app --reload

# 7. Run local frontend (optional)
cd frontend
npm install
npm run dev
```

---

## AI Techniques

This system implements **three core AI concepts** plus a **mandatory-but-scoped ML enhancement**:

### AI Concept 1 — Rule-Based Reasoning
Explicit rules determine prerequisite satisfaction, academic stage eligibility, and course recommendation categories (Recommended Now / Later / Low Priority).

### AI Concept 2 — Weighted Knowledge-Based Scoring
Evaluates academic profile fit against specialization-specific subject-area weights. Uses weight renormalization when subject areas have no data (never treats missing as zero).

### AI Concept 3 — Content-Based Interest Matching
Cosine similarity between student interest vectors and specialization interest profiles, both expressed over the same 13-item subject-area taxonomy.

### ML Enhancement — Decision Tree Classifier
Experimental cross-check using scikit-learn Decision Tree trained on synthetic data. Shown alongside (never replacing) the core recommendation engine.

---

## Hybrid Recommendation Formula

```
Final Score = Academic Fit x 0.70 + Interest Alignment x 0.30
```

> **Disclosed Enhancement:** The 70/30 split is a configurable prototype default, not sourced from the proposal (see `src/config/settings.py`).

---

## Technology Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.9+ | Core language |
| Streamlit | Web UI framework |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| SQLite | Database (seeded from CSV) |
| Plotly | Interactive visualizations |
| scikit-learn | ML enhancement |
| pytest | Testing framework |

---

## Project Structure

```
project_root/
├── api/                      # FastAPI serverless backend
│   └── index.py              # REST API endpoints & SPA serving
├── frontend/                 # Vite + React Modern Web Application
│   ├── src/                  # React components, state, API client
│   └── dist/                 # Production compiled SPA
├── src/
│   ├── config/settings.py    # All constants, enums, weights
│   ├── data/database.py      # SQLite data access layer
│   ├── academic/             # Grading, GPA, stage, profile
│   ├── ai/                   # Rule engine, scoring, interest matching, recommendations
│   ├── models/schemas.py     # Data validation schemas
│   └── ui/                   # Visualization and presentation helpers
├── data/                     # CSV source-of-truth files (9 files)
├── database/                 # SQLite database (academic.db)
├── ml/                       # ML enhancement (tree ensemble + zero-dependency predict)
│   ├── models/               # model_trees.json (pure Python inference)
│   ├── predict.py            # Decision tree & random forest inference
│   └── train_model.py        # Offline training script
├── scripts/                  # Seed, generate, train, verification scripts
├── tests/                    # pytest test suite (172 tests)
├── docs/                     # Documentation & academic methodology reports
├── vercel.json               # Vercel deployment configuration
└── requirements.txt          # Serverless dependencies
```

---

## Data Architecture (FIX-1)

CSV files under `data/` are the **single source of truth** for all static/configuration data. SQLite is populated from those CSVs via `scripts/seed_database.py`. The running application reads/writes **only through SQLite**.

---

## Testing

```bash
python -m pytest tests/ -v
```

**172 tests** covering:
- Grading boundaries (every grade boundary)
- GPA calculation (normal, failed, withdrawn, zero-credit)
- Weight validation (all specializations sum to 1.0)
- Missing subject handling (never zero, renormalization)
- Interest matching (cosine similarity, vector construction)
- Prerequisite rules (satisfaction, stage eligibility)
- Recommendation ranking (all 5 manual scenarios A-E)
- CSV/SQLite seed consistency
- Full pipeline integration

---

## Disclosed Enhancements (Section 4a)

| # | Addition | Justification |
|---|----------|---------------|
| 1 | SQLite | Structured persistence without infrastructure overhead |
| 2 | scikit-learn | Powers the mandatory-but-scoped ML enhancement |
| 3 | Plotly | Interactive visualization of performance and recommendations |
| 4 | pytest | Systematic, examiner-visible testing |
| 5 | 70/30 Academic/Interest split | Simplest defensible default; fully configurable |

---

## License

Academic project — KDU Group 22, IT3182 Essentials of AI.
