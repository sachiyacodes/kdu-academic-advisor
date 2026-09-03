# AI Methodology

## Overview

This system implements three core AI concepts and one mandatory-but-scoped ML enhancement, as required by the IT3182 Essentials of AI assignment guidelines.

> **Important:** Ordinary programming logic (if/else, arithmetic) is NOT labeled as machine learning. Each AI concept below represents a genuine application of AI methodology.

---

## AI Concept 1 — Rule-Based Reasoning

**Module:** `src/ai/rule_engine.py`

### Description
A knowledge base of explicit academic rules applied to student profiles to derive actionable conclusions about course eligibility and recommendations.

### Rules Implemented

```
Rule 1 — Prerequisite Satisfaction:
  IF all prerequisite courses for Course C are completed by the student
  AND each prerequisite has a passing mark
  THEN prerequisite requirement is satisfied
  ELSE identify specific missing prerequisites

Rule 2 — Academic Stage Eligibility:
  IF student's current year > course's required year
     THEN eligible
  IF student's current year == course's required year
     AND student's semester >= course's required semester
     THEN eligible
  ELSE not yet eligible (course is for a later stage)

Rule 3 — Course Categorization:
  IF course is relevant to top specializations
     AND prerequisites satisfied
     AND stage eligible
     THEN "Recommended Now"
  ELIF course is relevant but prerequisites/stage not met
     THEN "Recommended Later"
  ELSE "Low Priority"
```

### Input
- Student's completed courses (with marks and pass/fail status)
- Course prerequisite relationships (from `prerequisites` table)
- Student's academic stage (year, semester, completed credits)

### Output
- Course categorization: Recommended Now / Recommended Later / Low Priority
- Missing prerequisite list for each course
- Eligibility status with specific reasons

### This is NOT Machine Learning
These are explicit, deterministic, human-authored rules — a classic rule-based expert system approach. No statistical model is learned from data.

---

## AI Concept 2 — Weighted Knowledge-Based Scoring

**Module:** `src/ai/weighted_scoring.py`

### Description
Evaluates how well a student's academic profile matches each specialization using domain-expert-assigned weights per subject area.

### Formula (matches proposal Section 7)

```
AcademicFit(s) = Sum(weight_i * average_mark_i) / Sum(weight_i)
```

Where:
- `weight_i` = specialization-specific weight for subject area i
- `average_mark_i` = student's average mark in subject area i
- The sum is taken ONLY over subject areas where the student has completed courses

### Critical Missing-Data Rule (Section 16)

A missing subject area NEVER receives a score of zero. Instead:

1. Exclude the missing area from the numerator
2. Exclude its weight from the denominator
3. Renormalize remaining weights to sum to 1.0
4. Record which areas were unavailable
5. Lower evidence level where appropriate

### Specialization Weights (verified against proposal Section 7)

| Specialization | Top Weighted Areas |
|---|---|
| Data Science | Statistics 30%, Programming 25%, Database 20% |
| AI/ML | Mathematics 25%, Programming 25%, Statistics 20% |
| Cyber Security | Cyber Security 35%, Networking 25%, Programming 20% |
| Software Engineering | Programming 30%, Software Engineering 25%, Algorithms 20% |
| Networking & Cloud | Networking 40%, Systems 20%, Cloud Computing 15% |
| Database Engineering | Database 35%, Programming 20%, Data Analysis 15% |

All weight sets sum to exactly 1.0 (validated in code and tests).

### Output
- Specialization Compatibility Score (0-100) — NOT a probability
- Per-subject contribution breakdown
- Evidence level (Limited/Moderate/Strong based on relevant course count)

---

## AI Concept 3 — Content-Based Interest Matching (FIX-3)

**Module:** `src/ai/interest_matching.py`

### Description
Matches student interests against specialization interest profiles using cosine similarity, exactly as defined in proposal Section 7.

### Formula

Both vectors are expressed over the same 13-dimensional canonical subject-area taxonomy:

```
student_vector = [1 if interest selected else 0, for each subject area]
spec_vector = [interest_weight for each subject area]

InterestScore(s) = cosine_similarity(student_vector, spec_vector) * 100
```

Where cosine similarity is:
```
cos(a, b) = (a . b) / (|a| * |b|)
```

### Design Decision
- Student interests map 1:1 onto the 13-item subject-area taxonomy (not free text)
- Each specialization has a fixed interest weight vector over the same taxonomy
- This ensures the interest space and academic space are directly comparable
- Cosine similarity is used rather than dot product because it handles different vector magnitudes (student binary vs. specialization weighted)

### Output
- Interest Alignment Score (0-100)
- Per-interest contribution breakdown showing which interests matched

---

## Hybrid Recommendation Model (FIX-2)

**Module:** `src/ai/recommendation_engine.py`

### Formula

```
Final Compatibility Score = Academic Fit * 0.70 + Interest Alignment * 0.30
```

### Disclosed Enhancement
The 70/30 split is a **disclosed enhancement** (Section 4a, row 5). The proposal defines both scores but does not specify a numeric combination ratio. This is the simplest defensible default for a hybrid recommender. Both weights are:
- Defined in `src/config/settings.py` (ACADEMIC_WEIGHT, INTEREST_WEIGHT)
- Never hard-coded elsewhere in the codebase
- Disclosed in the UI with a note on every recommendation

---

## ML Enhancement — Decision Tree Classifier (FIX-4)

**Modules:** `ml/train_model.py`, `ml/predict.py`

### Scope
One small, well-tested ML component serving as an experimental cross-check against the rule/weighted-sum engine. It is NOT a replacement for the three core AI techniques.

### Model
- **Type:** Decision Tree Classifier (scikit-learn)
- **Question:** Predict a student's most likely successful specialization from their academic profile
- **Features:** Average mark per subject area (13 features)
- **Target:** Specialization category (6 classes)

### Training
- Dataset: 553 synthetic students with clear specialization archetypes
- Train/Test split: 80/20 (random_state=42)
- Max depth: 8, Min samples leaf: 5

### Results
- Accuracy: ~53% (chance = ~17%, so the model learns meaningful patterns)
- Trained on synthetic data — results cannot establish real-world effectiveness
- Always shown as "Experimental comparison / enhancement"

### Limitations
- Synthetic data only — no real student validation
- Moderate accuracy reflects the synthetic data distribution and inherent overlap between specializations
- Never silently replaces the explainable recommendation engine

---

## Evidence Level (Section 18)

| Level | Relevant Courses | Meaning |
|---|---|---|
| Limited Evidence | 0-4 | Recommendation based on limited academic data |
| Moderate Evidence | 5-9 | Reasonable data available for assessment |
| Strong Evidence | 10+ | Comprehensive academic data available |

Evidence level communicates confidence in the *amount of available evidence*, not probability.

---

## Ethical Considerations

1. **Privacy** — Student academic records are sensitive data
2. **Bias** — Weights and rules may reflect assumptions and disadvantage some students
3. **Accuracy** — Recommendations depend on rule/weight/data quality
4. **Synthetic Data** — ML results based on synthetic data cannot establish real-world effectiveness
5. **Automation** — This is decision support, not academic authority
6. **Human Responsibility** — Students and advisors remain responsible for final decisions
