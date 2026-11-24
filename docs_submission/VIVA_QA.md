# SmartCivic AI — Comprehensive Viva Voce Examination Guide
**Project:** SmartCivic AI – Intelligent Civic Complaint Management and Predictive Governance System  
**Document:** 30 Core Technical & Architectural Examination Questions & Model Answers  
**Degree:** Bachelor of Technology in Computer Science & Engineering  
**Academic Session:** 2026–2027  

---

### Q1. What is the fundamental problem SmartCivic AI addresses that existing municipal portals (like CPGRAMS or CM Helpline) fail to solve?
**Answer:** Existing municipal grievance platforms are passive digital repositories. They suffer from severe triage latency (taking 3 to 7 days before manual dispatchers route a complaint), have zero life-safety awareness, and treat all tickets equally in FIFO queues. Furthermore, naive AI attempts fail because polite citizen wording often lowers urgency scores, causing lethal emergencies (gas leaks, live wires) to languish in backlogs. SmartCivic AI automates sub-second category classification, enforces deterministic safety overrides, balances field officer workloads, monitors real-time SLAs with automated escalation, and provides 14-day time-series forecasting.

---

### Q2. Why did you choose LinearSVC over Deep Learning or Large Language Models (LLMs) for the primary category classifier?
**Answer:** In civic municipal systems, response latency, deterministic inference costs, and model interpretability are critical constraints. LinearSVC (Support Vector Classification with linear kernel) is computationally lightweight ($\approx 15$ ms inference latency), runs on low-cost municipal servers without dedicated GPUs, and avoids the hallucination risks and high API expenses of cloud-hosted LLMs. Combined with sublinear TF-IDF vectorization, LinearSVC provides hyperplanes with clear feature weight coefficients, allowing municipal engineers to see exactly which lexical features determined a category.

---

### Q3. LinearSVC outputs uncalibrated decision distances, not probabilities. How does SmartCivic AI generate valid confidence scores?
**Answer:** We wrap the base LinearSVC estimator with scikit-learn's `CalibratedClassifierCV` utilizing Platt Scaling (`method='sigmoid'`). Platt scaling fits a logistic regression model on the support vector machine's raw decision margins using internal cross-validation. This transforms raw signed geometric distances into calibrated posterior class probabilities $P(y=k \mid x) \in [0, 1]$, enabling true confidence score estimation and uncertainty gating.

---

### Q4. What is the "Non-Downgrade Safety Invariant", and how is it architecturally enforced?
**Answer:** The Non-Downgrade Safety Invariant is a core architectural rule: statistical machine learning models must never be permitted to lower the priority of an acute life-safety hazard. The `SafetyRuleEngine` executes strictly *after* machine learning scoring. If deterministic pattern matching detects critical hazard indicators (e.g., exposed 440V live wires, LPG gas leaks, structural building collapse, contaminated water supply), the priority is unconditionally locked to `CRITICAL` ($\ge 80$), and a mandatory audit reason tag is attached. Downstream sentiment or statistical adjustments are mathematically barred from lowering this tier.

---

### Q5. Can you explain the mathematical formulation of the Multi-Factor Priority Scoring Engine?
**Answer:** The priority score $P \in [0, 100]$ is computed via a weighted additive linear combination:
$$P = \min\left(100, \, \sum_{i} W_i \cdot S_i + B_{\text{duration}} + B_{\text{essential}}\right)$$
Where factors include Urgency ($W_{\text{urg}} = 0.25$), Severity ($W_{\text{sev}} = 0.25$), Population Impact ($W_{\text{pop}} = 0.20$), Safety Hazard ($W_{\text{haz}} = 0.20$), Duration ($W_{\text{dur}} = 0.10$), and Vulnerable Populations. Duration escalation adds a $+15$ point bonus for issues persisting $>7$ days, while essential municipal disruptions (drinking water, primary electricity) receive categorical baseline bonuses.

---

### Q6. How does the system detect and handle uncertain AI predictions?
**Answer:** SmartCivic AI implements an uncertainty threshold gate: if the maximum posterior class probability from the calibrated classifier is below $0.40$ ($\text{confidence} < 0.40$), the pipeline flags the record with `needs_human_review = True`. The ticket is placed in a dedicated supervisory triage queue, allowing human administrators to verify the classification before field dispatch.

---

### Q7. How does semantic duplicate detection work, and how does it prevent duplicate work orders?
**Answer:** Duplicate detection is powered by `SentenceTransformer` dense vector embeddings (using model `all-MiniLM-L6-v2`) and cosine similarity. When a new complaint arrives, its 384-dimensional dense vector is compared against active grievances within the same category and geographical ward. If cosine similarity $\ge 0.75$, the complaints are linked into the `similar_complaints` relational table. The field officer receives a single unified work order while the citizen tracking count is incremented, preventing dispatch of multiple redundant repair crews.

---

### Q8. What happens when a service level agreement (SLA) deadline is breached?
**Answer:** The background escalation daemon (`/api/sla/check-breaches`) continuously checks active tickets where $\text{current\_time} > \text{sla\_deadline}$ and $\text{is\_breached} = \text{False}$. Upon breach:
1. `SLARecord.is_breached` is set to `True`.
2. The complaint's priority is automatically promoted by $+1$ tier (e.g., `MEDIUM` $\to$ `HIGH`, or `HIGH` $\to$ `CRITICAL`).
3. An automatic $+20$ urgency penalty is added to `priority_score`.
4. High-priority in-app and SMTP email breach notifications are dispatched to department supervisors.
5. A transition entry is written to `complaint_status_history` with the system actor ID.

---

### Q9. What are the configured SLA resolution deadlines across priority tiers?
**Answer:** 
- **CRITICAL:** 6 Hours (Immediate emergency response for life-safety hazards).
- **HIGH:** 24 Hours (Major infrastructure disruption affecting whole neighborhoods).
- **MEDIUM:** 72 Hours (Standard localized civic repairs).
- **LOW:** 168 Hours / 7 Days (Non-urgent civic improvements and beautification).

---

### Q10. What is the Four-Tier Role-Based Access Control (RBAC) structure in SmartCivic AI?
**Answer:**
1. **CITIZEN:** Can self-register, submit complaints with photos, track own grievances via tokens, verify resolutions, and view public transparency metrics.
2. **FIELD OFFICER:** Can access assigned ward queues (`/officer`), update operational status (`in_progress`, `resolved`), and upload photographic resolution proof.
3. **DEPARTMENT ADMIN:** Can access divisional workspaces (`/department`), inspect officer workload capacities, reassign field personnel, and review department SLA metrics.
4. **SUPER ADMIN:** Apex municipal authority with full access to all departments, manual priority overrides, SLA escalation triggers, predictive modeling, and system configurations.

---

### Q11. How are user authentication sessions secured against hijacking and forgery?
**Answer:** We use cryptographic timed HMAC tokens generated via `itsdangerous.URLSafeTimedSerializer`. The token encodes the user ID, session creation timestamp, and a cryptographic signature using the application secret key. Tokens are transmitted in `HttpOnly`, `SameSite=Lax` cookies with a 7-day expiration lifespan. Signature validation and timestamp verification occur at the FastAPI ASGI dependency layer (`get_current_user`).

---

### Q12. How does SmartCivic AI protect citizen data privacy under the Digital Personal Data Protection (DPDP) Act?
**Answer:** Under DPDP compliance, the public transparency portal (`/transparency`) strictly enforces privacy-by-design. All public endpoints and views scrub Complainant Names, Phone Numbers, Email Addresses, and exact residential street addresses. Complaints are identified publicly only by random tracking tokens (e.g. `CMP-A1B2C3`), broad municipal wards, and service categories.

---

### Q13. How does the Department Workforce Load Balancing algorithm operate?
**Answer:** The algorithm queries active grievances (`status in ['open', 'in_progress', 'pending']`) assigned to each active officer in the target department. Officer capacity is categorized into three tiers:
- **Available:** $< 5$ active tickets.
- **Busy:** $5 - 11$ active tickets.
- **Overloaded:** $\ge 12$ active tickets.
When an incoming ticket requires routing, the service recommends the officer with the lowest current active load and highest historical SLA compliance rate.

---

### Q14. What empirical machine learning results did you obtain across candidate models?
**Answer:** Benchmarked on a stratified 80/20 split ($N=500$ across 14 civic categories) with 5-fold cross-validation:
- **LinearSVC (Calibrated):** Test Accuracy = $96.00\%$, Macro F1 = $0.9554$, 5-Fold CV Mean = $0.9075$ (±0.0245).
- **Logistic Regression:** Test Accuracy = $94.00\%$, Macro F1 = $0.9329$, 5-Fold CV Mean = $0.9000$ (±0.0235).
- **Multinomial Naive Bayes:** Test Accuracy = $92.00\%$, Macro F1 = $0.9094$, 5-Fold CV Mean = $0.8875$ (±0.0194).
- **SGD Classifier:** Test Accuracy = $92.00\%$, Macro F1 = $0.9093$, 5-Fold CV Mean = $0.8825$ (±0.0194).

---

### Q15. What are the scientific caveats regarding your 96% accuracy figure?
**Answer:** As an ethical engineer, I must state plainly that this 96% accuracy was evaluated on a curated synthetic dataset of 500 multi-class civic grievances. While it includes realistic bilingual Hindi and Hinglish phrasing, this performance demonstrates strong internal class separability under curated vocabulary. It cannot be assumed to generalize identically to raw, real-world citizen inputs containing misspellings, colloquial idioms, and noisy text without domain fine-tuning and active human-in-the-loop oversight.

---

### Q16. How does the 14-Day OLS Volume Forecasting model work mathematically?
**Answer:** It uses Ordinary Least Squares (OLS) linear regression over 60 days of historical daily intake:
$$\hat{y}(t) = \beta_0 + \beta_1 \cdot t$$
Where $\beta_1 = \frac{\sum (t - \bar{t})(y - \bar{y})}{\sum (t - \bar{t})^2}$ and $\beta_0 = \bar{y} - \beta_1 \bar{t}$.  
The parametric 95% confidence interval is computed as:
$$\text{CI}_{95\%}(t) = \hat{y}(t) \pm 1.96 \cdot s_e \sqrt{1 + \frac{1}{N} + \frac{(t - \bar{t})^2}{\sum (t_i - \bar{t})^2}}$$
Where $s_e$ is the standard error of regression residuals. The confidence band widens as the forecast horizon expands into the future.

---

### Q17. How does the GIS Spatial Intelligence module detect localized civic outbreaks?
**Answer:** The `ClusterService` monitors incoming complaints grouped by category and coordinates. If three or more complaints in the same category occur within a 500-meter radius within a 48-hour rolling window, the system flags a localized outbreak. This detects pipeline contamination, main transformer blowouts, or sewage overflows before they spread into city-wide crises.

---

### Q18. Why is SQLite used in development, and how does the architecture support PostgreSQL in production?
**Answer:** SQLite is embedded, serverless, zero-configuration, and ideal for local testing, rapid prototyping, and reproducible academic evaluation. However, because we use SQLAlchemy ORM with standard ANSI SQL data types, switching to PostgreSQL in production requires merely setting the `DATABASE_URL` environment variable (e.g. `postgresql+psycopg2://user:pass@host/db`). The codebase contains zero vendor-locked SQLite-specific SQL queries.

---

### Q19. How does SmartCivic AI prevent malicious file uploads when citizens attach photos?
**Answer:** In `app/core/security.py`, the `validate_and_sanitize_upload()` function implements multi-layer defense:
1. Enforces a strict 10MB file size limit.
2. Sanitizes filenames using secure alphanumeric basenames to eliminate directory traversal attacks (`../../etc/passwd`).
3. Validates MIME content types against an explicit whitelist (`image/png`, `image/jpeg`, `image/webp`).
4. Performs binary inspection of file magic bytes (e.g. `\x89PNG\r\n` for PNG, `\xFF\xD8\xFF` for JPEG) to prevent executable scripts masked with image extensions.

---

### Q20. What is the purpose of the Human-in-the-Loop Override, and how is it audited?
**Answer:** AI should assist, not blindly rule municipal operations. If a field supervisor determines that localized circumstances justify changing a priority (e.g., an upcoming religious festival on an affected street), they can submit a manual override. The system requires a mandatory text explanation, saves the override in `priority_overrides`, recalibrates the SLA deadline, and appends an immutable entry in `audit_logs` capturing the user ID, timestamp, and IP address.

---

### Q21. How many automated tests exist, and what do they verify?
**Answer:** SmartCivic AI contains 29 automated PyTest tests (100% passing rate in $\approx 14$s):
- `test_api.py` (4 tests): microservice health and classification endpoints.
- `test_edge_cases.py` (6 tests): boundary scores, empty inputs, non-English text.
- `test_priority_engine.py` (3 tests): scoring formula weights and clamping bounds.
- `test_rule_engine.py` (3 tests): non-downgrade safety rule invariants.
- `test_fastapi_app.py` (13 tests): authentication, RBAC, complaint lifecycle, SLA auto-escalation, file uploads, GIS GeoJSON markers, OLS forecast endpoints, and template rendering.

---

### Q22. How does the bilingual NLP support work for Hindi and Hinglish complaints?
**Answer:** The `LanguageDetector` inspects Unicode character blocks to detect Devanagari script. The `EntityExtractor` and `SafetyRuleEngine` maintain bilingual dictionaries mapping Hindi tokens (e.g., `"बिजली का तार"`, `"पानी गंदा है"`, `"आग लग गई"`) and transliterated Hinglish phrases (`"transformer blast ho gaya"`, `"light gayab hai"`) to canonical English hazard classifications.

---

### Q23. What is the difference between a Complaint and an Incident in your database schema?
**Answer:** A `Complaint` represents a single grievance filed by an individual citizen. An `Incident` is a higher-level municipal event that groups multiple related complaints (via the many-to-many junction table `incident_complaints`). For example, 45 individual citizen complaints regarding low water pressure on Ward 12 are grouped under one single Incident: `"Main Feeder Pipe Leakage - Ward 12"`.

---

### Q24. How does the citizen verification and ticket reopening process work?
**Answer:** When an officer marks a complaint `RESOLVED` and uploads resolution photo evidence, the citizen can inspect the photo on `/portal/track`. If satisfied, the citizen closes the ticket. If the work was incomplete, the citizen clicks "Reopen Ticket" with comments. The system changes status to `in_progress`, increments `reopen_count`, elevates priority for immediate supervisor attention, and logs the reopening in `complaint_status_history`.

---

### Q25. What multi-format report exports does SmartCivic AI provide?
**Answer:**
1. **CSV Export (`/api/reports/csv`):** Raw tabular streaming of complaints for external data analysis.
2. **Excel Workbook (`/api/reports/excel`):** Formatted multi-tab spreadsheet compiled via `xlsxwriter`, featuring executive KPIs, department performance, and category breakdowns.
3. **Executive PDF Dossier (`/api/reports/pdf`):** Vector-rendered official municipal dossier generated via `PyMuPDF`/`fitz`, designed for administrative reviews.

---

### Q26. What was the "Dead Animal Hazard" bug identified during evaluation?
**Answer:** In `ai/training/evaluate.py`, the test case `"Dead stray cow lying on street for 4 days"` received `LOW` priority (score 26) instead of `HIGH`. The root cause was that our rule engine had explicit keyword triggers for structural, fire, electrical, and gas hazards, but lacked explicit triggers for biological decay and animal carcasses. We have documented this defect in `docs_submission/ISSUES.md` and flagged it as an open limitation to be resolved by adding biowaste keyword rules.

---

### Q27. What is HTMX, and why was it chosen over a heavy single-page application (SPA) framework like React or Angular?
**Answer:** HTMX allows building modern, dynamic user interfaces directly with server-rendered HTML attributes (`hx-get`, `hx-post`, `hx-target`, `hx-swap`). By avoiding a decoupled SPA architecture:
1. We eliminate client-side JavaScript bundle bloat and client-side state synchronization bugs.
2. The entire application logic remains unified in Python and FastAPI.
3. Pages render instantaneously on low-spec municipal hardware and mobile devices.
4. Server-rendered templates allow instant SEO and accessibility without complex SSR node servers.

---

### Q28. How does the system handle class imbalance during model training?
**Answer:** In `ai/training/train_classifier.py` and `compare_models.py`, we implement class weight balancing (`class_weight='balanced'`). This automatically adjusts weights inversely proportional to class frequencies in the training data, preventing majority classes (like Electricity and Water) from dominating smaller municipal categories (like Environment or Public Transport).

---

### Q29. What are the key hardware and software requirements for running SmartCivic AI?
**Answer:**
- **Minimum Server:** 2 CPU Cores, 4 GB RAM, 20 GB SSD Storage (runs efficiently on standard low-cost cloud instances or municipal server hardware).
- **Operating System:** Linux (Ubuntu 22.04 LTS recommended) or Windows 10/11 / Server 2022.
- **Software Dependencies:** Python 3.10+, Docker & Docker Compose (optional for containerized deployment).
- **Client Requirements:** Any standard HTML5 web browser (Chrome, Firefox, Safari, Edge) on mobile or desktop.

---

### Q30. If given another six months to enhance SmartCivic AI, what would be your top three development priorities?
**Answer:**
1. **IoT Telemetry Integration:** Connecting municipal SCADA sensors and water pipeline pressure transducers directly into the FastAPI ingestion pipeline, generating tickets automatically before citizens experience water cuts.
2. **Computer Vision Damage Assessment:** Deploying lightweight vision models to assess citizen photos, automatically estimating pothole volume and road repair urgency.
3. **Voice IVR & WhatsApp Ingestion:** Building an automated voice hotline with Hindi speech-to-text to empower illiterate and elderly citizens who cannot type on smartphones.
