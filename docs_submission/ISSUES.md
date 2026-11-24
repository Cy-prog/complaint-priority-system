# SmartCivic AI — Technical Audit & Issue Report
**Project:** SmartCivic AI – Intelligent Civic Complaint Management and Predictive Governance System  
**Document:** System Issues, Edge-Case Anomalies & Technical Debt Log  
**Verification Date:** November 2026  

---

## 1. Resolved Defects & Remediated Architecture

### ISSUE-01: SQLite Relative Path Resolution Failure
- **Severity:** High (Functional Blocker)
- **Component:** `app/core/database.py`
- **Symptom:** When running scripts or test suites from subdirectories (e.g. `tests/` or `ai/training/`), SQLite resolved the database relative to `.` rather than project root, creating empty ghost database files without schema tables.
- **Resolution:** Re-anchored database URL resolution against `PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent`, constructing absolute path `sqlite:///{PROJECT_ROOT}/data/complaints.db`.

### ISSUE-02: Microservice Module Name Shadowing in Test Suite
- **Severity:** High (Build & Verification Blocker)
- **Component:** `tests/test_api.py` vs `ai-service/app.py`
- **Symptom:** The legacy experimental Flask microservice (`ai-service/app.py`) was dynamically inserted into `sys.path[0]`, clobbering Python's import system and preventing `app.main` (FastAPI) from being loaded across subsequent pytest test modules.
- **Resolution:** Refactored `tests/test_api.py` to use `importlib.util.spec_from_file_location("ai_microservice_app", ...)` under an explicit isolated module alias, preserving the top-level `app` namespace.

### ISSUE-03: Pydantic Configuration Validation Crash on Custom Factor Weights
- **Severity:** Medium
- **Component:** `app/core/config_loader.py` & `config/priority_config.yaml`
- **Symptom:** `PriorityWeights` Pydantic model lacked default fields for extended factors (`urgency`, `severity`, `duration`), throwing validation runtime exceptions during startup if YAML keys differed.
- **Resolution:** Updated `PriorityWeights` model with explicit default values and aligned YAML field definitions with mathematical formulas.

### ISSUE-04: Automated SLA Escalation Foreign Key Integrity Constraint
- **Severity:** Medium
- **Component:** `app/services/sla_service.py`
- **Symptom:** During automated background SLA breach escalation, `ComplaintStatusHistory` records were instantiated without `changed_by_user_id`, violating SQLite table's `NOT NULL` foreign key constraint.
- **Resolution:** Explicitly assigned actor ID `changed_by_user_id = 1` (System Administrator ID) for all automated daemon escalation transactions.

---

## 2. Identified Limitations & Open Technical Debt

### ISSUE-05: Non-Human Biological Hazard Extraction Failure
- **Severity:** Low to Medium (Edge-Case NLP Limitation)
- **Component:** `ai/entity_extractor.py` & `ai/rule_engine.py`
- **Observed Behavior:** In `ai/training/evaluate.py`, the test case `"Dead stray cow lying on street for 4 days, unbearable stench and flies"` evaluated to `LOW` priority (Score: 26) instead of `HIGH`.
- **Root Cause:** The rule engine contains explicit keyword triggers for chemical, structural, fire, and human casualties, but lacks explicit triggers for decomposing animal carcasses and biowaste vectors.
- **Recommended Remediation:** Expand `SafetyRuleEngine` keyword taxonomy with `RISK_BIOHAZARD` rules checking `["dead animal", "carcass", "stench", "rot"]`.

### ISSUE-06: Python 3.14 Standard Library Deprecation Warnings
- **Severity:** Low (Non-blocking Warnings)
- **Component:** Standard Library `datetime` usage across `app/services/`
- **Observed Behavior:** PyTest logs 28 warnings regarding `datetime.datetime.utcnow()`:
  `DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects: datetime.datetime.now(datetime.UTC).`
- **Recommended Remediation:** Refactor all `datetime.utcnow()` invocations to `datetime.now(datetime.UTC)`.

### ISSUE-07: NumPy 2.5 Pickled Shape Assignment Warning
- **Severity:** Low (Upstream Deprecation Warning)
- **Component:** `joblib/numpy_pickle.py` during scikit-learn model deserialization
- **Observed Behavior:** Warning: `Setting the shape on a NumPy array has been deprecated in NumPy 2.5. As an alternative, you can create a new view using np.reshape.`
- **Recommended Remediation:** Re-serialize trained pipeline weights with updated `joblib >= 1.4` and NumPy 2.5+.

### ISSUE-08: Dual Experimental Backend Stems
- **Severity:** Low (Architectural Hygiene)
- **Component:** Repository Root (`backend/` Spring Boot & `ai-service/` Flask)
- **Observed Behavior:** The repository contains an unmaintained, incomplete Java Spring Boot prototype (`backend/`) alongside the production-grade FastAPI application (`app/`).
- **Recommended Remediation:** Retain FastAPI as primary major project codebase; migrate or archive the Java prototype to `/legacy` to avoid confusion.
