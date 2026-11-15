# Testing Documentation

## Overview

The test suite uses **pytest** for unit tests, API integration tests, seed consistency verification, and manual scenario validation. Use `python -m pytest tests --collect-only -q` to see the current count rather than relying on a fixed documentation total.

**Synthetic data seed value: 42** (documented in `src/config/settings.py` as `SYNTHETIC_SEED`).

## Running Tests

```bash
python -m pip install -r requirements-dev-lock.txt
python -m pytest tests/ -v
```

The development lock includes FastAPI TestClient's HTTPX dependency, the local Uvicorn server, and Streamlit/Plotly for existing legacy presentation tests. These tools are separate from the lean serverless requirements. Tests copy the bundled database into a temporary directory; feedback tests never write into the tracked database.

Frontend checks run from `frontend`: `npm ci`, `npm test`, `npm run lint`, and `npm run build`. Grade-preview tests check the backend's prototype bands and half-to-even rounding boundaries. CI runs these checks and backend tests for every push and pull request.

## Test Files

| File | What it covers |
|------|---------------|
| `test_grading.py` | Every grade boundary, decimals, out-of-range, pass/fail |
| `test_gpa.py` | Normal, failed, withdrawn, in-progress, zero-credit, NGPA, classification |
| `test_api.py` | Catalog, demo, GPA, recommendation, elective, and graduation endpoints |
| `test_api_validation.py` | Duplicate records, catalog authority, failed/withdrawn credits, prerequisite status, and weight validation |
| `test_scoring.py` | Weight sums, renormalization, missing subjects, evidence levels, scenarios |
| `test_interests.py` | Vector construction, cosine similarity, overlap, scenarios |
| `test_rules.py` | Prerequisite checking, stage eligibility |
| `test_recommendations.py` | 70/30 combination, configurability, ranking, all 5 scenarios |
| `test_seed_consistency.py` | CSV/SQLite row counts, taxonomy, weight sums, Data Science proposal match |
| `test_integration.py` | Full pipeline, no-interests, single-course, deterministic reproducibility |
| `test_*_remediation.py` | Previously corrected scoring, interest, explanation, and ML behavior |
| `conftest.py` | Student fixtures and isolated test database |

## Manual Test Scenarios (Section 38)

### Student A — Data Science
- **Input:** Statistics 88, Programming 84, Database 80, Mathematics 76; interests: Data Analysis, Statistics
- **Expected:** Data Science ranks in top 2
- **Result:** PASS — Data Science consistently ranks #1

### Student B — Cyber Security
- **Input:** Cyber Security 91, Networking 86, Programming 78, Systems 84; interests: Cyber Security, Networking
- **Expected:** Cyber Security ranks #1
- **Result:** PASS — Cyber Security ranks #1

### Student C — Software Engineering
- **Input:** Programming 92, Software Engineering 88, Algorithms 84, Database 75; interest: Programming
- **Expected:** Software Engineering ranks in top 2
- **Result:** PASS — Software Engineering ranks in top 2

### Student D — Conflicting Profile
- **Input:** Programming 90, Statistics 85, Cyber Security 70; interests: AI, Data Analysis, Cyber Security
- **Expected:** Meaningful ranked result with explanations
- **Result:** PASS — All 6 specializations ranked with distinct scores

### Student E — Early Academic Stage
- **Input:** Programming 72 (single course); no interests
- **Expected:** Limited Evidence, no overconfident recommendations
- **Result:** PASS — All specializations show "Limited Evidence"

## Edge Cases Tested

- No courses entered
- No interests selected
- Only failed courses
- Single completed course
- Missing subject areas (renormalization)
- Equal specialization scores
- Invalid marks (boundary testing: 0, 100, -1, 101)
- Zero-credit courses
- Withdrawn/in-progress courses excluded from GPA

## Seed Consistency Tests (FIX-1)

Verifies CSV source-of-truth matches SQLite:
- Row counts match for all tables
- Subject area names match canonical taxonomy
- All specialization weights sum to 1.0
- All interest vectors sum to 1.0
- Data Science weights match proposal exactly (Section 11)

## Deterministic Reproducibility

- Synthetic data seed: 42
- ML train/test split seed: 42
- Running the pipeline twice produces identical results (tested)
