# SmartCivic AI — Empirical Evidence Pack
**Project:** SmartCivic AI – Intelligent Civic Complaint Management and Predictive Governance System  
**Institution:** ITM University Gwalior | Department of Computer Science & Engineering  
**Academic Session:** 2026–2027  
**Verification Date:** November 2026  
**Status:** Authenticated against live source code, test execution, and empirical training outputs.

---

## 1. Executive Summary & Verification Statement
All data, metrics, database schemas, and architectural components documented herein have been directly extracted from the running codebase in `C:\Users\Samit\.gemini\antigravity\scratch\complaint-priority-system`. Zero metrics, accuracy figures, or test cases have been fabricated.

- **Automated Tests:** 29 passed, 0 failed, 28 warnings across unit, integration, and security suites.
- **Primary AI Model:** Calibrated LinearSVC (`MODEL_VERSION = "2.0.0-SmartCivic"`).
- **Test Accuracy (14 Civic Classes):** 96.00% on stratified 80/20 test split ($N=100$).
- **Macro F1-Score:** 0.9554 | **Mean 5-Fold Stratified Cross-Validation:** 0.9075 (± 0.0245).
- **Baseline Classifier (6 Core Classes):** 99.00% accuracy, 0.9940 5-fold CV.
- **Relational Tables:** 14 normalized SQLAlchemy entities with foreign key constraints.
- **API Endpoints:** 44 registered routes across REST and server-rendered endpoints.

---

## 2. Technology Stack & Environment Specifications

| Component | Technology / Library | Version | Role in SmartCivic AI |
|:---|:---|:---|:---|
| **Runtime Environment** | Python (CPython) | 3.14.5 (win32) | Core backend language |
| **Web Framework** | FastAPI | 0.136.1 | Asynchronous ASGI REST API & routing engine |
| **ASGI Server** | Uvicorn | 0.34.0 | High-concurrency async web server |
| **ORM & Database Engine** | SQLAlchemy | 2.0.52 | Relational object-relational mapping |
| **Database Engines** | SQLite (Dev) / PostgreSQL (Prod) | 3.x / 15+ | Relational persistence with foreign keys |
| **Machine Learning Core** | Scikit-Learn | 1.9.0 | TF-IDF Vectorization & Calibrated LinearSVC |
| **Array & Matrix Processing** | NumPy | 2.5.2 | Feature array transformations |
| **Semantic Embeddings** | Sentence-Transformers | 3.3.1 | Dense vector similarity & duplicate detection |
| **Lexicon Sentiment** | NLTK (VADER) | 3.9.1 | Emotional intensity scoring |
| **Template Engine** | Jinja2 | 3.1.5 | Server-rendered HTML pages |
| **Reactive Frontend Micro-lib** | HTMX | 2.0.4 | Dynamic AJAX partial updates without full reloads |
| **Client-Side State** | Alpine.js | 3.x.x | Declarative frontend modal and toggle reactivity |
| **CSS Design System** | Tailwind CSS (CDN Theme) | 3.x | Smart-city command center visual identity |
| **GIS Mapping** | Leaflet.js + OpenStreetMap | 1.9.4 | Interactive municipal ward and incident mapping |
| **Chart Visualizations** | Chart.js | 4.x | Real-time analytical and predictive trendlines |
| **Document Generation** | python-docx / reportlab / pymupdf | 1.2.0 / 5.1.1 / 1.28.2 | DOCX, PDF, and executive dossier compilation |
| **Presentation Compilation** | python-pptx | 1.0.2 | Widescreen presentation generation |
| **Automated Testing** | PyTest + pytest-asyncio | 9.1.1 / 1.4.0 | Automated unit and integration test runner |

---

## 3. Module Inventory & Architectural Responsibilities

### 3.1 AI / Machine Learning Engine (`/ai`)
1. **`ai/classifier.py`**:
   - Class: `CategoryClassifier`
   - Model Version: `2.0.0-SmartCivic`
   - Mechanism: `TfidfVectorizer(ngram_range=(1,2), max_features=5000, sublinear_tf=True)` + `CalibratedClassifierCV(LinearSVC(C=1.0, max_iter=2000), method='sigmoid')`.
   - Capabilities: `predict()`, `predict_with_metadata()` returning posterior probability confidence, top-3 candidates, feature importances, and `needs_human_review = True` if confidence $< 0.40$.
2. **`ai/priority_engine.py`**:
   - Class: `PriorityEngine`
   - Formulation: Weighted linear combination across urgency, severity, population impact, hazard index, duration escalation, and essential service disruption.
   - Outputs: Categorical priority (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), numerical score ($0–100$), and sub-scores.
3. **`ai/rule_engine.py`**:
   - Class: `SafetyRuleEngine`
   - Invariant: Deterministic hard rules that *can only escalate* priority (never downgrade).
   - Acute Hazard Triggers: Exposed electrical wires, gas leaks, structural building collapse, fire emergencies, open manholes, contaminated water supply.
4. **`ai/entity_extractor.py`**:
   - Class: `EntityExtractor`
   - Capabilities: Regex and dictionary-based extraction of municipal landmarks (hospitals, schools, railway stations), duration tokens ('5 days', 'पिछले 3 दिन से'), population indicators, and hit-and-run vehicle descriptors (type, color, license plate).
5. **`ai/sentiment_analyzer.py`**:
   - Class: `SentimentAnalyzer`
   - Mechanism: VADER lexicon sentiment analysis scoring compound polarity (`positive`, `negative`, `neutral`).
6. **`ai/similarity_service.py`**:
   - Class: `SimilarityService`
   - Mechanism: Cosine similarity on TF-IDF vectors or dense sentence embeddings. Flags potential duplicates if similarity $\ge 0.75$.
7. **`ai/explainer.py`**:
   - Class: `ExplainerEngine`
   - Method: `explain_decision()` generates structured human-readable and machine-readable explanations distinguishing probabilistic ML contributions from deterministic safety overrides.
8. **`ai/language_detector.py`**:
   - Class: `LanguageDetector`
   - Detects Devanagari Hindi vs English script.
9. **`ai/confidence.py`**:
   - Class: `ConfidenceEstimator`
   - Evaluates prediction margin between top-1 and top-2 candidate classes.
10. **`ai/pipeline.py`**:
    - Class: `ComplaintAnalysisPipeline`
    - Singleton orchestrator executing preprocessing -> classification -> entity extraction -> sentiment -> priority scoring -> safety rule invariant -> duplicate detection -> explanation.

### 3.2 Core Services (`/app/services`)
1. **`app/services/complaint_service.py`**: CRUD operations, search filters, priority overrides, and duplicate linking.
2. **`app/services/auth_service.py`**: Citizen self-registration, credential verification (PBKDF2/bcrypt hashing), timed session token creation (`URLSafeTimedSerializer`), and session revocation.
3. **`app/services/sla_service.py`**: SLA deadline calculation, compliance tracking, and `check_and_escalate_slas()` which automatically flags breaches, promotes priority (+1 level), applies +20 urgency penalty, and dispatches alerts.
4. **`app/services/department_service.py`**: Department workforce capacity tracking, officer load rating (Available $<5$, Busy $5-11$, Overloaded $12+$), and AI-assisted assignment recommendations.
5. **`app/services/gis_service.py`**: GeoJSON marker generator mapping verified GPS coordinates and Gwalior Municipal Ward centroids (Lashkar, Morar, City Center, Hazira, Thatipur, Maharaj Bada).
6. **`app/services/predictive_service.py`**: 14-day Ordinary Least Squares (OLS) time-series forecasting with parametric 95% confidence bands, recurring ward failure hotspots, and seasonal meteorological directives.
7. **`app/services/notification_service.py`**: In-app notifications and safe background SMTP email dispatch.
8. **`app/services/report_service.py`**: CSV streaming, multi-tab Excel spreadsheet generation (`xlsxwriter`), and executive PDF dossiers (`fitz`/PyMuPDF).
9. **`app/services/cluster_service.py`**: Spatial cluster detector identifying localized civic outbreaks (e.g., contaminated water pipelines) within 500m / 48hr window.
10. **`app/services/analytics_service.py`**: Database-backed time-series analytics, SLA compliance percentages, and AI override tracking.

---

## 4. API Endpoint Inventory (44 Routes)

### 4.1 Authentication & Session Management
- `POST /api/auth/register` — Citizen self-registration (`username`, `email`, `password`, `full_name`, `phone`).
- `POST /api/auth/login` — Authenticates user, issues cryptographic session cookie and Bearer token.
- `POST /api/auth/logout` — Revokes session token.
- `GET /api/auth/me` — Fetches current authenticated user profile and role.
- `GET /switch-persona/{role}` — Developer demonstration helper to instantly switch among 4 personas (`citizen`, `operator`, `dept_admin`, `admin`).

### 4.2 Complaint Ingestion & Management
- `POST /api/complaints` — Submits new complaint with location, description, and contact info.
- `GET /api/complaints` — Paginated complaint registry with multi-column filtering.
- `GET /api/complaints/{id}` — Full complaint record including AI analysis and SLA deadlines.
- `PUT /api/complaints/{id}` — Updates complaint metadata.
- `DELETE /api/complaints/{id}` — Soft/hard deletes complaint (Super Admin only).
- `POST /api/complaints/{id}/analyze` — Triggers complete AI pipeline analysis on complaint text.
- `POST /api/complaints/{id}/override` — Human operator priority override with mandatory rationale.
- `POST /api/complaints/{id}/reprioritize` — Recalculates priority score based on updated factors.
- `GET /api/complaints/{id}/similar` — Queries semantic duplicates using vector distance.
- `GET /api/complaints/{id}/recommend-assignment` — AI recommends optimal department and officer based on active workload.
- `POST /api/complaints/{id}/assign` — Assigns complaint to department and field officer.
- `POST /api/complaints/{id}/feedback` — Records citizen feedback or category/priority correction.

### 4.3 Municipal Operations & Workspaces
- `GET /api/categories` — Lists active civic categories and mapped departments.
- `GET /api/departments` — Lists municipal departments and operational codes.
- `GET /api/departments/{id}/officers` — Fetches department officers with live workload metrics.
- `GET /api/departments/{id}/sla-metrics` — Computes department-specific SLA compliance rate and average resolution latency.
- `POST /api/sla/check-breaches` (alias `/api/sla/check-escalations`) — Automated daemon sweeping overdue complaints, escalating priority, and generating alerts.
- `GET /api/sla/{id}` — Fetches countdown and breach status for specific ticket.

### 4.4 Spatial & Predictive Governance
- `GET /api/gis/markers` — Returns GeoJSON FeatureCollection of complaint coordinates filtered by priority and category.
- `GET /api/gis/wards` — Aggregates complaint volume and risk index per municipal ward.
- `GET /api/predictive/forecast` — Returns 14-day OLS projected complaint volume with upper and lower 95% confidence intervals.
- `GET /api/predictive/hotspots` — Returns recurring infrastructure failure hotspots grouped by ward and category.
- `GET /api/predictive/seasonal` — Returns active seasonal directives based on current meteorological calendar.

### 4.5 Reporting & Transparency
- `GET /api/reports/csv` — Streams complete grievance dataset in CSV format.
- `GET /api/reports/excel` — Downloads formatted multi-tab Excel analytics workbook.
- `GET /api/reports/pdf` — Generates vector-rendered executive PDF dossier.
- `GET /api/public/transparency-summary` (alias `/api/transparency/metrics`) — Returns privacy-safe public governance statistics (Zero Citizen PII exposed).

### 4.6 Notifications & System Health
- `GET /api/health` — Returns system status (`{"status": "ok"}`).
- `GET /api/notifications` — Fetches current user notifications.
- `GET /api/notifications/unread-count` — Returns unread notification count badge.
- `POST /api/notifications/{id}/read` — Marks notification as read.
- `POST /api/notifications/read-all` — Marks all notifications as read for current user.

### 4.7 Server-Rendered UI Pages
- `GET /` — Apex Command Center Dashboard (`dashboard.html`).
- `GET /complaints` — Grievance Registry Queue (`complaint_list.html`).
- `GET /complaints/new` — Grievance submission form (`complaint_new.html`).
- `GET /complaints/{id}` — Detailed grievance dossier & triage breakdown (`complaint_detail.html`).
- `GET /department` — Department Head Workspace (`department_dashboard.html`).
- `GET /officer` — Field Officer Assigned Queue (`officer_workspace.html`).
- `GET /map` — GIS Spatial Intelligence Map (`map.html`).
- `GET /predictive` — Predictive Analytics & Forecasting Dashboard (`predictive.html`).
- `GET /transparency` — Public Civic Transparency Portal (`transparency.html`).
- `GET /portal` — Citizen Grievance Portal (`citizen_portal.html`).
- `GET /portal/track` — Citizen Live Tracking Interface (`citizen_track.html`).
- `GET /analytics` — Administrative Analytics Dashboard (`analytics.html`).
- `GET /reports/gram-sabha` — Gram Sabha & Jan Sunwai Report (`gram_sabha_report.html`).
- `GET /settings` — Priority Weights & Safety Thresholds Settings (`settings.html`).

---

## 5. Database Schema & Relational Architecture (14 Tables)

```
users (id, username, email, password_hash, full_name, role, phone, department_id, is_active, created_at, updated_at)
  └── departments.id (FK: department_id)

departments (id, name, description, contact_email, is_active, created_at)

categories (id, name, description, risk_level, is_essential_service, department_id, is_active, created_at)
  └── departments.id (FK: department_id)

complaints (id, complaint_id, complaint_text, complainant_name, complainant_contact, language, status, state, city, district, ward, area, pincode, latitude, longitude, category_id, assigned_department_id, assigned_user_id, created_by_user_id, created_at, updated_at, resolved_at, evidence_photo, resolution_photo, resolution_notes, citizen_feedback_status, reopen_count)
  ├── categories.id (FK: category_id)
  ├── departments.id (FK: assigned_department_id)
  ├── users.id (FK: assigned_user_id)
  └── users.id (FK: created_by_user_id)

complaint_analysis (id, complaint_id, priority, priority_score, urgency_score, severity_score, impact_score, safety_score, duration_score, confidence, sentiment, risk_level, entities, key_issues, affected_population, affected_population_estimate, reasoning_summary, recommended_action, duplicate_probability, analysis_model_version, analysis_latency_ms, analyzed_at)
  └── complaints.id (FK: complaint_id)

sla_records (id, complaint_id, priority, sla_deadline, is_breached, response_at, resolved_at, response_time_minutes, resolution_time_minutes)
  └── complaints.id (FK: complaint_id)

priority_overrides (id, complaint_id, original_priority, original_score, new_priority, new_score, changed_by_user_id, reason, changed_at)
  ├── complaints.id (FK: complaint_id)
  └── users.id (FK: changed_by_user_id)

complaint_status_history (id, complaint_id, old_status, new_status, changed_by_user_id, notes, changed_at)
  ├── complaints.id (FK: complaint_id)
  └── users.id (FK: changed_by_user_id)

complaint_feedback (id, complaint_id, feedback_type, original_value, corrected_value, reason, submitted_by_user_id, used_for_training, created_at)
  ├── complaints.id (FK: complaint_id)
  └── users.id (FK: submitted_by_user_id)

incidents (id, incident_id, title, description, status, category_id, area, complaint_count, first_reported, last_updated)
  └── categories.id (FK: category_id)

incident_complaints (id, incident_id, complaint_id, linked_at)
  ├── incidents.id (FK: incident_id)
  └── complaints.id (FK: complaint_id)

similar_complaints (id, complaint_id, similar_complaint_id, similarity_score, detected_at)
  ├── complaints.id (FK: complaint_id)
  └── complaints.id (FK: similar_complaint_id)

notifications (id, user_id, title, message, notification_type, reference_id, is_read, created_at)
  └── users.id (FK: user_id)

audit_logs (id, user_id, action, resource_type, resource_id, old_value, new_value, ip_address, created_at)
  └── users.id (FK: user_id)
```

---

## 6. User Roles & Permission Matrix (4 Tiers)

| Feature / Action | CITIZEN | FIELD OFFICER | DEPT ADMIN | SUPER ADMIN |
|:---|:---:|:---:|:---:|:---:|
| Lodge Complaint & Upload Evidence | Yes | Yes | Yes | Yes |
| Track Personal Complaints via Token | Yes | Yes | Yes | Yes |
| View Public Transparency Metrics | Yes | Yes | Yes | Yes |
| View Assigned Work Queue (`/officer`) | No | Yes | Yes | Yes |
| Update Status (`in_progress`, `resolved`) | No | Yes | Yes | Yes |
| Upload Resolution Proof Photo | No | Yes | Yes | Yes |
| View Department Queue (`/department`) | No | No | Yes | Yes |
| Reassign Officer within Division | No | No | Yes | Yes |
| Inspect Officer Workload Capacity | No | No | Yes | Yes |
| Trigger Manual Priority Override | No | Yes (Self) | Yes | Yes |
| Trigger SLA Escalation Sweep | No | No | No | Yes |
| View Predictive Volume Forecast | No | No | Yes | Yes |
| Configure System Weights & Rules | No | No | No | Yes |
| Export CSV / Excel / PDF Dossiers | No | No | Yes | Yes |
| Access Full Immutable Audit Logs | No | No | No | Yes |

---

## 7. Empirical Test Suite Execution

Executed via `python -m pytest tests/ -v`:

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Samit\.gemini\antigravity\scratch\complaint-priority-system
collected 29 items

tests/test_api.py::test_flask_health_check PASSED                       [  3%]
tests/test_api.py::test_flask_classify_route PASSED                     [  6%]
tests/test_api.py::test_flask_analyze_route PASSED                      [ 10%]
tests/test_api.py::test_flask_empty_payload PASSED                      [ 13%]
tests/test_edge_cases.py::test_empty_complaint PASSED                   [ 17%]
tests/test_edge_cases.py::test_short_complaint PASSED                   [ 20%]
tests/test_edge_cases.py::test_repeated_characters PASSED               [ 24%]
tests/test_edge_cases.py::test_non_english_characters PASSED           [ 27%]
tests/test_edge_cases.py::test_boundary_priority_scores PASSED         [ 31%]
tests/test_edge_cases.py::test_high_impact_keywords PASSED              [ 34%]
tests/test_fastapi_app.py::test_fastapi_health PASSED                   [ 37%]
tests/test_fastapi_app.py::test_admin_login PASSED                      [ 41%]
tests/test_fastapi_app.py::test_citizen_registration_and_login PASSED   [ 44%]
tests/test_fastapi_app.py::test_complaint_creation_and_ai_analysis PASSED [ 48%]
tests/test_fastapi_app.py::test_dashboard_summary_and_trends PASSED    [ 51%]
tests/test_fastapi_app.py::test_file_upload_security_validation PASSED [ 55%]
tests/test_fastapi_app.py::test_department_and_workload_apis PASSED    [ 58%]
tests/test_fastapi_app.py::test_sla_escalation_api PASSED              [ 62%]
tests/test_fastapi_app.py::test_gis_markers_api PASSED                  [ 65%]
tests/test_fastapi_app.py::test_predictive_forecast_api PASSED         [ 68%]
tests/test_fastapi_app.py::test_transparency_api PASSED                 [ 72%]
tests/test_fastapi_app.py::test_report_exports PASSED                  [ 75%]
tests/test_fastapi_app.py::test_html_pages_render PASSED               [ 79%]
tests/test_priority_engine.py::test_priority_calculation PASSED         [ 82%]
tests/test_priority_engine.py::test_score_bounds PASSED                 [ 86%]
tests/test_priority_engine.py::test_high_urgency_escalation PASSED     [ 89%]
tests/test_rule_engine.py::test_rule_match PASSED                       [ 93%]
tests/test_rule_engine.py::test_priority_escalation PASSED              [ 96%]
tests/test_rule_engine.py::test_reason_generation PASSED                [100%]

====================== 29 passed, 28 warnings in 14.08s =======================
```

---

## 8. Empirical Machine Learning Model Comparison Results

Extracted directly from `data/model_comparison_results.json`:
- **Training Set:** 400 samples (Stratified 80%)
- **Test Set:** 100 samples (Stratified 20%)
- **Total Categories Evaluated:** 14 Civic Classes
- **Random Seed:** 42

### 8.1 Aggregate Performance Metrics
| Metric | LinearSVC (Calibrated) | Logistic Regression | Multinomial Naive Bayes | SGD Classifier |
|:---|:---:|:---:|:---:|:---:|
| **Test Accuracy** | **0.9600** | 0.9400 | 0.9200 | 0.9200 |
| **Macro F1-Score** | **0.9554** | 0.9329 | 0.9094 | 0.9093 |
| **Weighted F1-Score**| **0.9576** | 0.9367 | 0.9159 | 0.9158 |
| **Macro Precision** | **0.9738** | 0.9536 | 0.9348 | 0.9333 |
| **Macro Recall** | **0.9500** | 0.9286 | 0.9000 | 0.9000 |
| **5-Fold CV Mean** | **0.9075** | 0.9000 | 0.8875 | 0.8825 |
| **5-Fold CV Std Dev**| **±0.0245** | ±0.0235 | ±0.0194 | ±0.0194 |

### 8.2 Per-Category Breakdown (LinearSVC Calibrated)
| Category | Precision | Recall | F1-Score | Support ($N_{\text{test}}$) |
|:---|:---:|:---:|:---:|:---:|
| Drainage | 1.0000 | 1.0000 | 1.0000 | 4 |
| Electricity | 0.8333 | 1.0000 | 0.9091 | 10 |
| Environment | 1.0000 | 0.5000 | 0.6667 | 4 |
| Garbage/Waste | 1.0000 | 1.0000 | 1.0000 | 8 |
| Healthcare | 1.0000 | 1.0000 | 1.0000 | 7 |
| Infrastructure | 1.0000 | 1.0000 | 1.0000 | 5 |
| Other | 1.0000 | 1.0000 | 1.0000 | 4 |
| Parks | 1.0000 | 1.0000 | 1.0000 | 7 |
| Public Safety | 0.8000 | 0.8000 | 0.8000 | 10 |
| Public Transport | 1.0000 | 1.0000 | 1.0000 | 5 |
| Roads | 1.0000 | 1.0000 | 1.0000 | 10 |
| Sanitation | 1.0000 | 1.0000 | 1.0000 | 8 |
| Streetlights | 1.0000 | 1.0000 | 1.0000 | 8 |
| Water Supply | 1.0000 | 1.0000 | 1.0000 | 10 |

### 8.3 Scientific Caveat & Dataset Provenance
> [!NOTE]
> **Dataset Limitation Statement:** The evaluation was conducted on a curated synthetic dataset of 500 multi-class civic grievances. While class distributions and lexical features reflect realistic municipal phrasing (including Hindi and transliterated Hinglish), performance metrics of 96% accuracy cannot be assumed to represent arbitrary real-world noisy citizen inputs without domain adaptation and continuous human-in-the-loop validation.

---

## 9. Deployment Architecture
- **Local / Virtualenv:** Standard Python 3.10–3.14 on Linux or Windows via Uvicorn.
- **Containerized:** Multi-stage `Dockerfile` (Python 3.11-slim, non-root user `appuser`, healthcheck via `/api/health`).
- **Orchestration:** `docker-compose.yml` exposing port 8000 with volume mounts for persistent database and uploads.
- **Cloud Deployment Configs:** `render.yaml` (Render Web Service) and `netlify.toml` (Static portal proxying to backend).
