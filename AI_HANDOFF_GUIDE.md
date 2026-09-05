# KDU Academic Advisor — AI Handoff & System Architecture Guide

Welcome to the **KDU Academic Advisor** codebase. This document is written specifically for AI agents, language models, and software engineers working on this project. Read this before making any modifications.

---

## 1. Project Overview

The **KDU Academic Advisor** is a production-grade, hybrid AI-powered academic advisement platform designed for the Faculty of Computing at General Sir John Kotelawala Defence University (KDU).

The system guides undergraduate IT students through:
1. Academic profile setup (Degree, Year 1-4, Semester 1-2, Student Archetype benchmarking).
2. Course history & transcript tracking (cumulative GPA calculation, credits tracking, grade distribution).
3. Career interest calibration across 13 subject areas.
4. Hybrid AI Specialization Recommendations (70% Academic Fit + 30% Career Interest with Sensitivity Calibration & Supervised ML Cross-Check).
5. Rule-based Elective Advising & 4-Year Curriculum Roadmap (prerequisite validation, stage eligibility, specialization synergy scoring).
6. Graduation Credit Clearance Audit & Prerequisite Bottleneck Analytics (120 GPA credits + 14 NGPA credits).

---

## 2. Technical Stack

* **Backend & APIs**:
  - **FastAPI** (pi/index.py): High-performance, stateless serverless REST API (configured for local dev and Vercel serverless deployment).
  - **Streamlit** (pp.py, pages/): Companion desktop/demo UI providing multi-page legacy access.
  - **SQLite Database** (database/academic.db, src/data/database.py): In-memory and file-based relational store for degrees, courses, prerequisites, and specializations.
  - **Machine Learning** (ml/): Scikit-learn Random Forest and Decision Tree classifiers for specialization consensus predictions.
  - **Testing** (	ests/): 172 comprehensive pytest unit and integration tests.

* **Frontend**:
  - **React 19 + Vite**: Modern SPA client under rontend/.
  - **Tailwind CSS v4**: Built with @theme design tokens centralized in rontend/src/index.css.
  - **Component Architecture**: 12 reusable UI primitives in rontend/src/components/ui/.
  - **Icons**: Lucide React.

---

## 3. Critical System Invariants & Rules

When modifying this repository, you **MUST** follow these rules:

### A. Strict Design System & Token Compliance
* **Zero Purple Rule**: DO NOT re-introduce any purple, violet, indigo, or glowing violet hex codes (#7C5CFC, #8B70FF, etc.) into active CSS tokens or rendered JSX.
* **Palette Tokens**:
  - **Primary / Actions**: Ocean Blue (#3B82F6) for interactive elements, buttons, active step capsules.
  - **AI / Analytics**: Intelligence Teal (#14B8A6) for ML predictions, confidence badges, model consensus.
  - **Canvas & Surfaces**: Deep Navy #07111F (background), #0B1728 (secondary wells), #101D2E (card surfaces), #203149 (borders).
  - **Semantics**: Green (#10B981) for completed/success, Amber (#F59E0B) for bottlenecks/warnings, Red (#EF4444) for destructive/errors.
* **Primitive UI Layer**: Always reuse existing primitives in rontend/src/components/ui/ (Button, Badge, Card, Input, Select, Slider, Tabs, Progress, Skeleton, EmptyState, IconButton, Tooltip). Do not hardcode arbitrary hex values into JSX.

### B. Test Preservation Rule
* **172/172 Tests Must Pass**: Run python -m pytest after making any backend changes.
* Do NOT delete, weaken, bypass, skip, or rewrite existing tests simply to make a suite pass.

### C. Domain & Academic Curriculum Rules
* **Curriculum Structure**:
  - 120 GPA credits + 14 NGPA (Non-GPA) credits required for graduation.
  - Elective options strictly begin in **Year 3, Semester 2** and continue into Year 4. Courses in Years 1 & 2 are 100% mandatory degree core foundations.
* **Stage-Aware Student History**:
  - A student currently in Year Y, Semester S has already completed all prior semesters.
  - For example, a student enrolled in Year 2 Semester 2 has already completed Year 1 (Sem 1 & 2) and Year 2 Sem 1 (27 courses totaling 57 credits: 49 Core + 8 NGPA).

---

## 4. Developer Quickstart Commands

### Backend
`ash
# Install Python dependencies
pip install -r requirements.txt

# Run all 172 backend tests
python -m pytest

# Run FastAPI backend locally (port 8000)
uvicorn api.index:app --reload --port 8000

# Or run Streamlit UI locally
streamlit run app.py
`

### Frontend
`ash
cd frontend

# Install Node dependencies
npm install

# Start Vite dev server (port 5173)
npm run dev

# Build for production
npm run build

# Run linter
npx oxlint src
`

---

## 5. Repository File Map

`
.
├── api/
│   └── index.py            # FastAPI REST application endpoints
├── src/
│   ├── academic/           # GPA calculation, grading scales, student profile models
│   ├── ai/                 # Scoring algorithms, interest matching, rule engine, explanations
│   ├── config/             # Weight configurations, enums, global settings
│   ├── data/               # SQLite database client, stage-aware demo profiles
│   ├── models/             # Pydantic schemas and dataclasses
│   ├── ui/                 # Streamlit UI helpers & components
│   └── utils/              # General helper functions
├── ml/
│   ├── predict.py          # Supervised ML inference & model consensus
│   ├── train_model.py      # Random Forest / Decision Tree training script
│   └── models/             # Serialized models (.pkl) and metrics.json
├── data/                   # Canonical CSV datasets (courses, prerequisites, degrees, etc.)
├── database/               # Relational SQLite database (academic.db)
├── scripts/                # Database seeders, curricula validators, dataset generators
├── tests/                  # 172 pytest test suites
├── pages/                  # Streamlit multi-page interface
├── frontend/               # Modern React 19 + Tailwind v4 web application
│   ├── src/
│   │   ├── components/     # Step views (StepProfile, StepCourseHistory, etc.)
│   │   ├── components/ui/  # 12 atomic UI primitives
│   │   ├── api.js          # REST client connecting to FastAPI
│   │   ├── useAdvisorState.js # Global state, step transitions, localStorage sync
│   │   ├── index.css       # Master design tokens & Tailwind v4 @theme configuration
│   │   └── App.jsx         # Root application layout & step controller
│   └── package.json
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment configuration
└── AI_HANDOFF_GUIDE.md     # This guide
`