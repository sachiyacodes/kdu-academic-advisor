# Testing Documentation

## Overview

The test suite uses **pytest** and contains **135 tests** covering unit tests, integration tests, seed consistency verification, and manual scenario validation.

**Synthetic data seed value: 42** (documented in `src/config/settings.py` as `SYNTHETIC_SEED`).

## Running Tests

```bash
python -m pytest tests/ -v
```

## Test Files

| File | Tests | What it covers |
|------|-------|---------------|
| `test_grading.py` | 39 | Every grade boundary, decimals, out-of-range, pass/fail |
| `test_gpa.py` | 13 | Normal, failed, withdrawn, in-progress, zero-credit, classification |
| `test_scoring.py` | 14 | Weight sums, renormalization, missing subjects, evidence levels, scenarios |
| `test_interests.py` | 14 | Vector construction, cosine similarity, overlap, scenarios |
| `test_rules.py` | 11 | Prerequisite checking, stage eligibility |
| `test_recommendations.py` | 15 | 70/30 combination, configurability, ranking, all 5 scenarios |
| `test_seed_consistency.py` | 13 | CSV/SQLite row counts, taxonomy, weight sums, Data Science proposal match |
| `test_integration.py` | 5 | Full pipeline, no-interests, single-course, deterministic reproducibility |
| `conftest.py` | - | Fixtures for Students A-E (Section 38) |

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
