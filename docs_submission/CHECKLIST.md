# SmartCivic AI — Verification & Submission Quality Checklist
**Project:** SmartCivic AI – Intelligent Civic Complaint Management and Predictive Governance System  
**Document:** Academic Submission Quality Assurance Checklist  
**Student:** Samit Jain | Enrollment No.: [ENROLLMENT NO.]  
**Institution:** ITM University Gwalior | Department of Computer Science & Engineering  
**Academic Session:** 2026–2027  

---

## 1. Metric Alignment & Evidence Verification

| Metric / Dimension | Value in `evidence.md` | Value in Major Project Report (`.docx`/`.pdf`) | Value in Presentation (`.pptx`) | Status |
|:---|:---:|:---:|:---:|:---:|
| **Test Accuracy (14 Classes)** | 96.00% | 96.00% (Table 10.1) | 96.00% (Slide 4, 15) | Verified |
| **Macro F1-Score** | 0.9554 | 0.9554 (Table 10.1) | 0.9554 (Slide 4, 15) | Verified |
| **5-Fold Cross Validation Mean** | 0.9075 (±0.0245) | 0.9075 (±0.0245) | 0.9075 (±0.025) | Verified |
| **Baseline Classifier Accuracy** | 99.00% (6 classes) | 99.00% (Chapter 3 & 10) | 99.00% (Slide 4) | Verified |
| **Automated PyTest Test Count** | 29 Passed (100%) | 29 Passed (Table 9.1) | 29 Passed (Slide 14) | Verified |
| **Test Execution Duration** | 14.08 seconds | 14.08 seconds | 14.08 seconds | Verified |
| **Total Database Tables** | 14 Relational Entities | 14 Relational Entities | 14 Relational Entities | Verified |
| **Total Registered Routes** | 44 Endpoints | 44 Endpoints (Chapter 6 & App. A) | 44 Endpoints | Verified |
| **Configured Municipal Divisions**| 11 Departments | 11 Departments (Chapter 4, 8) | 11 Departments (Slide 6) | Verified |
| **SLA Critical Deadline** | 6 Hours | 6 Hours (Table 7.1) | 6 Hours (Slide 7, 10) | Verified |
| **SLA Escalation Penalty** | +20 Score / +1 Tier | +20 Score / +1 Tier | +20 Score / +1 Tier | Verified |
| **Predictive Forecast Horizon** | 14 Days (95% CI) | 14 Days (Chapter 11) | 14 Days (Slide 9, 13) | Verified |
| **Spatial Cluster Threshold** | 500m / 48 Hours | 500m / 48 Hours | 500m / 48 Hours | Verified |

---

## 2. Diagram & Figure Cross-Reference Verification

| Figure ID | Diagram File | Referenced in Report Text? | Embedded in Report? | Embedded in Slides? | Status |
|:---|:---|:---:|:---:|:---:|:---:|
| **Figure 6.1** | `diagrams/system_architecture.png` | Yes (Chapter 4, 6) | Yes | Yes (Slide 5) | Verified |
| **Figure 6.2** | `diagrams/use_case.png` | Yes (Chapter 4, 6) | Yes | Yes (Reference) | Verified |
| **Figure 6.3** | `diagrams/dfd_level_0.png` | Yes (Chapter 6.1) | Yes | Yes (Reference) | Verified |
| **Figure 6.4** | `diagrams/dfd_level_1.png` | Yes (Chapter 6.1) | Yes | Yes (Reference) | Verified |
| **Figure 6.5** | `diagrams/dfd_level_2.png` | Yes (Chapter 6.1) | Yes | Yes (Reference) | Verified |
| **Figure 6.6** | `diagrams/er_diagram.png` | Yes (Chapter 6.2) | Yes | Yes (Slide 12) | Verified |
| **Figure 7.1** | `diagrams/ai_pipeline_flowchart.png` | Yes (Chapter 7.1) | Yes | Yes (Slide 7) | Verified |
| **Figure 8.1** | `diagrams/complaint_lifecycle_state.png` | Yes (Chapter 8.1) | Yes | Yes (Reference) | Verified |
| **Figure 9.1** | `diagrams/sla_escalation_flow.png` | Yes (Chapter 9.1) | Yes | Yes (Slide 10) | Verified |
| **Figure 11.1**| `diagrams/deployment_diagram.png` | Yes (Chapter 11.1) | Yes | Yes (Reference) | Verified |

---

## 3. Placeholders Inventory & Student Action Items

Before final institutional submission, the candidate should replace the following standardized bracketed placeholders with official department and committee details:

| Placeholder Tag | Location in Report & Slides | Recommended Replacement |
|:---|:---|:---|
| `[ENROLLMENT NO.]` | Title page, Certificate, Declaration, Slides 1 | Enter official ITM University Enrollment Number (e.g. `0901CS231...`) |
| `[DEPARTMENT]` | Title page, Certificate, Slide 1 | Department of Computer Science & Engineering (or specialized branch) |
| `[GUIDE NAME, DESIGNATION]` | Title page, Certificate, Acknowledgement, Slide 1 | Faculty Guide's full academic title (e.g. `Dr. A. K. Sharma, Professor`) |
| `[DEPARTMENT HEAD NAME]` | Acknowledgement | Name of Head of Computer Science Department |
| `[NAMES]` | Title page, Acknowledgement | Names of co-candidates if submitting as a multi-member group |
| `[INSERT SCREENSHOT: SS-01 ...]` | Chapter 8, Report Section 8.3 | Capture live screens following `SCREENSHOTS_GUIDE.md` and insert image |

---

## 4. Integrity and Compliance Checklist

- [x] Base every claim on source code actually inspected and executed.
- [x] Zero invented accuracy numbers, F1 scores, or fabricated cross-validation values.
- [x] Test counts derived directly from PyTest execution (`29 passed, 28 warnings in 14.08s`).
- [x] Data provenance explicitly noted: evaluated on curated synthetic 500-sample dataset; caveats stated.
- [x] References cite only authentic libraries, frameworks, and literature (IEEE format).
- [x] Application source code preserved without destructive alterations.
- [x] Complete documentation, presentations, and diagrams generated strictly inside `/docs_submission`.
- [x] Bugs and technical debt logged in `ISSUES.md`.
- [x] 18 widescreen presentation slides generated with 60–90 words of speaker notes on every slide.
- [x] 30 viva questions and model answers compiled in `VIVA_QA.md`.
