# SmartCivic AI
## Intelligent Civic Complaint Management and Predictive Governance System

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-LinearSVC%20(96%25)-F7931E.svg?logo=scikitlearn)](https://scikit-learn.org/)
[![PyTest Status](https://img.shields.io/badge/PyTest-29%2F29%20Passing%20(100%25)-brightgreen.svg?logo=pytest)](https://docs.pytest.org/)
[![Data Privacy](https://img.shields.io/badge/DPDP%20Act-Privacy--Safe%20Zero%20PII-teal.svg)](#public-transparency-portal)

An enterprise-grade, explainable, and predictive municipal governance platform built for smart cities, municipal corporations, and district administrations. Developed with **FastAPI**, **SQLAlchemy**, **Scikit-Learn**, **Leaflet / OpenStreetMap GIS**, **Tailwind CSS**, **HTMX**, and **Alpine.js**.

---

## 🏛️ Executive Summary

Traditional municipal grievance portals function as passive digital registries. Incoming citizen complaints sit in backlogs for days without urgency triage, while naive AI systems risk hallucinating or downgrading fatal hazards because of polite wording.

**SmartCivic AI** solves this operational bottleneck by integrating **explainable machine learning**, **deterministic safety invariants**, **GIS spatial intelligence**, **automated SLA breach escalation**, and **14-day empirical time-series volume forecasting**.

---

## 🎯 Core Capabilities & Major Project Modules

### 1. Advanced Citizen Portal & Resolution Verification (`/portal`)
- Bilingual Hindi and English grievance lodgment.
- Photographic evidence upload secured with MIME and image magic byte validation.
- Instant unique tracking tokens (e.g., `CMP-A1B2C3`).
- Transparent AI triage breakdown displayed to citizens without technical obfuscation.
- Citizen satisfaction feedback and one-click **Reopen Ticket** functionality with audit trail.

### 2. Multi-Model AI Classification & Benchmark (96.00% Accuracy)
- Linear Support Vector Classifier (LinearSVC) wrapped with `CalibratedClassifierCV` (Platt Scaling).
- Benchmarked against Logistic Regression, Multinomial Naive Bayes, and SGD Classifier across 9 civic categories with 5-fold cross-validation.
- Uncertainty gating: predictions with confidence `< 0.40` flag `needs_human_review = True`.
- Versioned model pipeline (`MODEL_VERSION = "2.0.0-SmartCivic"`).

### 3. Explainable Multi-Factor Priority Scoring Engine
- Priority score computed in range `[0, 100]` with factor attribution:
  $$\text{Score} = W_{\text{urg}} \times \text{Urg} + W_{\text{sev}} \times \text{Sev} + W_{\text{pop}} \times \text{Pop} + W_{\text{haz}} \times \text{Haz} + W_{\text{dur}} \times \text{Dur} + W_{\text{ess}} \times \text{Ess} + W_{\text{vuln}} \times \text{Vuln}$$
- Dynamic duration escalation (+15 bonus for issues persisting $> 7$ days).

### 4. Deterministic Non-Downgrade Safety Rule Engine
- **Non-Negotiable Safety Invariant**: Deterministic rules execute *after* machine learning scoring.
- Acute life hazards (gas leaks, sparking transformers, live wires, building collapses, open manholes) unconditionally evaluate to **CRITICAL** ($\ge 80$).
- Statistical models and sentiment classifiers are mathematically barred from downgrading hazardous issues.

### 5. Municipal Department Management & Load Balancing (`/department`)
- Division hierarchy across 11 municipal departments (Water Supply, Sanitation, Roads, Electricity, etc.).
- Real-time officer capacity tracking: **Available** ($<5$ active), **Busy** ($5-11$), and **Overloaded** ($12+$).
- Intelligent AI assignment recommendation based on minimal active load and historical SLA compliance.

### 6. Active SLA Governance & Automated Escalation Engine
- Configurable priority-based resolution deadlines:
  - **CRITICAL**: 6 Hours
  - **HIGH**: 24 Hours
  - **MEDIUM**: 72 Hours
  - **LOW**: 168 Hours (7 Days)
- Automated escalation daemon (`/api/sla/check-breaches`):
  - Automatically flags overdue tickets and elevates priority by +1 tier.
  - Applies a +20 priority score increment.
  - Dispatches high-priority in-app and SMTP email breach notifications.

### 7. GIS Spatial Intelligence & Incident Clustering (`/map`)
- Interactive Leaflet.js and OpenStreetMap interface.
- High-precision municipal coordinates across Gwalior Wards.
- Spatial cluster detection: flags localized outbreaks (e.g. contaminated water pipeline bursts) when $\ge 3$ complaints cluster within 500m / 48 hours.

### 8. Predictive Governance: 14-Day OLS Volume Forecasting (`/predictive`)
- 14-day projection using Ordinary Least Squares (OLS) regression over 60-day historical time-series.
- Parametric 95% Confidence Interval band factoring residual variance and horizon growth.
- Recurring failure hotspot detection and seasonal meteorological directives (Monsoon drain desilting, Summer water tanker prepositioning).

### 9. Public Civic Transparency Portal (`/transparency`)
- Live public resolution percentages, category distributions, and sanitized resolution feeds.
- **DPDP Act Compliance**: Zero citizen PII (names, phone numbers, exact house numbers) exposed on public endpoints.

### 10. Four-Tier Role-Based Access Control (RBAC) & Security
- Cryptographic timed session tokens (`URLSafeTimedSerializer`).
- Strict backend role enforcement across **CITIZEN**, **OFFICER**, **DEPARTMENT_ADMIN**, and **SUPER_ADMIN**.
- Secure upload validation blocking directory traversal, oversize files ($>10$ MB), and malicious file extensions.

---

## 🔬 Multi-Model Benchmark Results

| Model Candidate | Test Accuracy | Macro F1-Score | 5-Fold CV Mean | Status |
|:---|:---:|:---:|:---:|:---|
| **LinearSVC (Calibrated)** | **96.00%** | **0.9554** | **0.9075 (±0.038)** | **SELECTED (Primary)** |
| Logistic Regression | 94.00% | 0.9329 | 0.9000 (±0.037) | Fallback Candidate |
| Multinomial Naive Bayes | 92.00% | 0.9094 | 0.8875 (±0.031) | Baseline Reference |
| SGD Classifier (Log Loss) | 92.00% | 0.9093 | 0.8825 (±0.030) | Alternative Candidate |

*Evaluated on stratified 80/20 train/test split. Cross-validation results saved in `data/model_comparison_results.json`.*

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Presentation ["Presentation Layer (Jinja2 + HTMX + Tailwind + Leaflet)"]
        CP["Citizen Portal (/portal)"]
        AP["Admin Apex Command Hub (/)"]
        DP["Department Workspace (/department)"]
        OF["Field Officer Queue (/officer)"]
        GIS["GIS Map (/map)"]
        PG["Predictive Dashboard (/predictive)"]
        TP["Public Transparency (/transparency)"]
    end

    subgraph Security ["Security & Middleware Layer"]
        AUTH["Timed Cryptographic Sessions (URLSafeTimedSerializer)"]
        RBAC["4-Tier RBAC (Citizen / Officer / DeptAdmin / SuperAdmin)"]
        UPL["Upload Validation (Magic Bytes + MIME + 10MB Limit)"]
    end

    subgraph CoreEngine ["Application & Core Services"]
        API["FastAPI High-Concurrency ASGI Core"]
        SLA["SLA Escalation Engine & Breach Alerts"]
        BAL["Workforce Load Balancer & Recommendations"]
        NOTIF["Notification Center (In-App + SMTP)"]
        REP["Reporting Suite (CSV + Excel + PyMuPDF)"]
    end

    subgraph AI ["AI / ML & Intelligence Subsystem"]
        VEC["TF-IDF Vectorizer (Unigram + Bigram)"]
        SVC["Calibrated LinearSVC Classifier (96% Acc)"]
        ENT["Entity & Hazard Extractor (Hindi / English)"]
        PRIO["Multi-Factor Scoring Engine (0-100)"]
        RULE["Deterministic Safety Invariant Guard"]
        OLS["14-Day OLS Time-Series Forecaster (95% CI)"]
        SIM["SentenceTransformer Duplicate Detection"]
    end

    subgraph Persistence ["Persistence Layer"]
        DB[("SQLAlchemy ORM (SQLite / PostgreSQL) - 14 Tables")]
        AUDIT[("Transactional Immutable Audit Trail")]
    end

    Presentation --> Security
    Security --> CoreEngine
    CoreEngine --> AI
    CoreEngine --> Persistence
```

---

## 🚀 Quickstart & Setup

### Prerequisites
- Python 3.10+ (Tested on Python 3.14 on Windows)
- pip & virtualenv

### 1. Installation
```bash
git clone https://github.com/Cy-prog/complaint-priority-system.git
cd complaint-priority-system
pip install -r requirements.txt
```

### 2. Run Comprehensive Test Suite (29 Tests)
```bash
python -m pytest tests/ -v
```
*Expected: `29 passed in ~21s`.*

### 3. Start Application Server
```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
Navigate to **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

### 4. Demo Role Switching
The platform includes 4 pre-seeded personas accessible from the navbar switcher:
- **Apex Admin**: Username `admin` | Password `admin123` (Access `/`)
- **Department Admin**: Username `deptadmin` | Password `admin123` (Access `/department`)
- **Field Officer**: Username `operator` | Password `operator123` (Access `/officer`)
- **Citizen**: Direct open portal at `/portal` or `/transparency`

---

## 📑 Project Artifacts & Documentation

| Artifact | File Name | Description |
|:---|:---|:---|
| **Presentation Deck** | [`smartcivic_ai_presentation.pptx`](./smartcivic_ai_presentation.pptx) | Complete 12-slide executive presentation for B.Tech project review. |
| **Comprehensive Report (PDF)** | [`smartcivic_ai_major_project_report.pdf`](./smartcivic_ai_major_project_report.pdf) | Academic Major Project report covering all chapters. |
| **Comprehensive Report (DOCX)** | [`smartcivic_ai_major_project_report.docx`](./smartcivic_ai_major_project_report.docx) | Fully editable Word document formatted to academic guidelines. |
| **Audit Dossier** | [`repository_audit_report.md`](file:///C:/Users/Samit/.gemini/antigravity/brain/21acb7ed-e920-4dfd-ab71-c583de30acbe/repository_audit_report.md) | Exhaustive line-by-line initial repository audit. |

To regenerate presentation slides or project reports:
```bash
python generate_presentation.py
python generate_report.py
```

---

## 🛡️ License & Academic Integrity

Developed for the degree of Bachelor of Technology in Computer Science & Engineering. All benchmarks and metrics are empirically calculated from live project data with zero fabricated claims.
