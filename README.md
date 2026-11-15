# AI-Based IT Specialization & Course Recommendation System

**KDU — IT3182 Essentials of Artificial Intelligence — Group 22**

An AI-powered academic decision-support prototype that recommends suitable IT specializations and courses based on a student's academic performance, completed courses, prerequisites, academic stage, and interests.

> **Disclaimer:** This system provides academic decision support based on the information entered by the student and the prototype's predefined rules and weighting model. Recommendations are not guaranteed outcomes and should not replace official academic guidance. The grading scale and curriculum data used in this prototype are illustrative and may not represent official KDU academic policies.

---

## Quick Start

Use Python 3.12 and Node.js 24. In PowerShell, from the repository root:

```powershell
# 1. Create virtual environment
python -m venv .venv

# 2. Install the tested development dependency set
.\.venv\Scripts\python.exe -m pip install -r requirements-dev-lock.txt

# 3. Seed the database (CSV -> SQLite)
.\.venv\Scripts\python.exe scripts/seed_database.py

# 4. Run tests
.\.venv\Scripts\python.exe -m pytest tests/ -q

# 5. Run local backend (optional)
.\.venv\Scripts\python.exe -m uvicorn api.index:app --reload

```

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open http://localhost:5173. The production demo is [KDU Academic Advisor](https://magical-carson-gamma.vercel.app). API documentation is available locally at http://127.0.0.1:8000/docs.

`requirements.txt` stays limited to the serverless runtime. `requirements-dev.txt` lists local test/server tools and legacy UI test dependencies; `requirements-dev-lock.txt` pins the tested development set. Model inference uses the committed JSON trees without installing scikit-learn. Offline model training requires its existing scientific Python dependencies separately.

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
| Python 3.12 | Backend language |
| FastAPI / Pydantic | API and input validation |
| React / Vite | Current web interface and build tooling |
| SQLite | Database (seeded from CSV) |
| Streamlit / Plotly | Legacy presentation helpers retained in regression tests |
| scikit-learn | Offline ML training; JSON trees support lightweight serving |
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
├── tests/                    # pytest regression and integration suite
├── docs/                     # Documentation & academic methodology reports
├── vercel.json               # Vercel deployment configuration
└── requirements.txt          # Serverless dependencies
```

---

## Data Architecture

CSV files under `data/` are the **single source of truth** for all static/configuration data. SQLite is populated from those CSVs via `scripts/seed_database.py`. The running application reads/writes **only through SQLite**.

---

## Testing

```bash
python -m pytest tests/ -v
```

The suite covers:
- Grading boundaries (every grade boundary)
- GPA calculation (normal, failed, withdrawn, zero-credit)
- Weight validation (all specializations sum to 1.0)
- Missing subject handling (never zero, renormalization)
- Interest matching (cosine similarity, vector construction)
- Prerequisite rules (satisfaction, stage eligibility)
- Recommendation ranking (all 5 manual scenarios A-E)
- CSV/SQLite seed consistency
- Full pipeline integration
- Earned-credit status, catalog metadata, duplicate courses, request weights, and graduation eligibility

CI runs backend tests and dependency checks plus frontend grade-preview tests, lint, and production build. Tests use a temporary copy of the bundled database, so feedback and schema checks do not change the repository database. Use `python -m pytest tests --collect-only -q` for the current test count.

## Input and graduation rules

The API normalizes course codes and rejects duplicates and unsupported statuses. Catalog identity, credits, type, and subject metadata come from the bundled catalog rather than caller overrides. Custom courses may use 0–30 credits and cannot impersonate catalog prerequisite IDs. Zero-credit catalog modules remain valid but add no earned credits.

Completed marks below the configured passing threshold become failed attempts. Withdrawn and in-progress records earn no credits. Only passed, completed courses count toward graduation or prerequisite completion; failed core courses block the prototype's eligibility flag. The prototype uses `is_passing` and the grading configuration consistently, including rounding and the current pass mark of 40. These are illustrative rules, not an official graduation determination.

Academic and interest weights must be finite, nonnegative, no greater than one, and sum to one. The backend recalculates grades and GPA; browser labels are previews.

Interest intensities must be finite values from zero to five, matching the browser slider; zero represents no selected interest.

---

## Disclosed Enhancements (Section 4a)

| # | Addition | Justification |
|---|----------|---------------|
| 1 | SQLite | Structured persistence without infrastructure overhead |
| 2 | scikit-learn | Powers the mandatory-but-scoped ML enhancement |
| 3 | Plotly | Legacy presentation helpers covered by regression tests |
| 4 | pytest | Systematic, examiner-visible testing |
| 5 | 70/30 Academic/Interest split | Simplest defensible default; fully configurable |

---

## License

Academic project — KDU Group 22, IT3182 Essentials of AI.

No project license has been selected. Contact the project contributors before reuse; this repair does not choose a license on their behalf.
