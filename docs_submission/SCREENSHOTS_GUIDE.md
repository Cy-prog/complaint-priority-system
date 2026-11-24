# SmartCivic AI — UI Screenshots & Demonstration Guide
**Project:** SmartCivic AI – Intelligent Civic Complaint Management and Predictive Governance System  
**Document:** System Demonstration & Interface Inspection Manual  
**Academic Year:** 2026–2027  

This document details every screen, its local URL/route, required user authentication role, key visual components, and corresponding placeholder tag inserted in the Major Project Report and Presentation.

---

## Screenshot Inventory & Capture Matrix

| ID | Interface / Page | Route / URL | Persona / Role Required | Key UI Elements to Capture | Report Insertion Tag |
|:---|:---|:---|:---|:---|:---|
| **SS-01** | **Apex Command Dashboard** | `http://127.0.0.1:8000/` | `admin` (Super Admin) | KPI summary tiles, active outbreak alert banners, recent grievances queue, quick action navigation | `[INSERT SCREENSHOT: SS-01 Apex Command Center Dashboard]` |
| **SS-02** | **Citizen Grievance Submission** | `http://127.0.0.1:8000/portal` | Public / `citizen` | Bilingual header, text description input, ward selector, GPS location picker, photo attachment button | `[INSERT SCREENSHOT: SS-02 Citizen Complaint Submission Portal]` |
| **SS-03** | **Citizen Receipt & Token View** | `http://127.0.0.1:8000/portal/receipt/<id>` | Public / `citizen` | Formatted tracking token badge (e.g. `CMP-A1B2C3`), estimated SLA countdown, emergency advisory | `[INSERT SCREENSHOT: SS-03 Citizen Grievance Receipt & Tracking Token]` |
| **SS-04** | **Citizen Live Tracking & Feedback** | `http://127.0.0.1:8000/portal/track` | Public / `citizen` | Token search bar, chronological status timeline, officer resolution proof display, satisfaction verification & reopen button | `[INSERT SCREENSHOT: SS-04 Citizen Tracking Timeline & Reopen Interface]` |
| **SS-05** | **Grievance Detail & AI Triage** | `http://127.0.0.1:8000/complaints/<id>` | `admin` or `operator` | AI triage card (LinearSVC prediction, confidence gauge, priority score 0-100), factor attribution bars, safety invariant reason tag | `[INSERT SCREENSHOT: SS-05 Complaint Detail & Explainable AI Triage Dossier]` |
| **SS-06** | **Human Priority Override Modal** | `http://127.0.0.1:8000/complaints/<id>` | `admin` or `operator` | Override dropdown, mandatory justification rationale textarea, warning banner indicating audit log entry | `[INSERT SCREENSHOT: SS-06 Human-in-the-Loop Priority Override Interface]` |
| **SS-07** | **Municipal Department Workspace** | `http://127.0.0.1:8000/department` | `deptadmin` or `admin` | Department switcher, divisional SLA compliance rate, field officer capacity indicators (Available/Busy/Overloaded), division queue | `[INSERT SCREENSHOT: SS-07 Department Administration & Workforce Balancing Workspace]` |
| **SS-08** | **Field Officer Workspace** | `http://127.0.0.1:8000/officer` | `operator` (Field Officer) | Active workload capacity meter, assigned complaints queue, quick status transitions (`In Progress`, `Resolved`), photo proof upload | `[INSERT SCREENSHOT: SS-08 Field Officer Mobile-Optimized Queue & Resolution Proof]` |
| **SS-09** | **GIS Spatial Intelligence Map** | `http://127.0.0.1:8000/map` | `admin` or `operator` | Leaflet/OSM map, color-coded priority markers, ward boundary centroid pins, category filter controls, spatial cluster alert circles | `[INSERT SCREENSHOT: SS-09 GIS Spatial Intelligence & Ward Incident Map]` |
| **SS-10** | **Predictive Volume Forecasting** | `http://127.0.0.1:8000/predictive` | `admin` or `deptadmin` | 14-day OLS time-series line chart with upper/lower 95% confidence intervals, recurring failure ward hotspots, seasonal directives | `[INSERT SCREENSHOT: SS-10 14-Day OLS Predictive Volume Forecast & Recurring Hotspots]` |
| **SS-11** | **Public Civic Transparency Portal** | `http://127.0.0.1:8000/transparency` | Public (No auth) | Live municipal resolution percentage, category doughnut chart, sanitized real-time resolution feed, DPDP privacy compliance badge | `[INSERT SCREENSHOT: SS-11 Public Civic Transparency Portal (DPDP Act Compliance)]` |
| **SS-12** | **Jan Sunwai / Gram Sabha Report** | `http://127.0.0.1:8000/reports/gram-sabha`| `admin` (Super Admin) | Ward-wise audit aggregation, unresolved grievance breakdown, public hearing printable layout, digital commissioner sign-off block | `[INSERT SCREENSHOT: SS-12 Gram Sabha & Jan Sunwai Social Audit Report]` |

---

## Instructions for Live Capture

1. Start the local server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```
2. Open a Chromium-based browser (Chrome, Edge, Brave) and navigate to `http://127.0.0.1:8000`.
3. To switch between demo personas, use the **Persona Switcher** dropdown in the top navigation bar:
   - **Super Admin**: Switch to Apex Admin (`admin` / `admin123`)
   - **Dept Admin**: Switch to Department Admin (`deptadmin` / `admin123`)
   - **Field Officer**: Switch to Field Officer (`operator` / `operator123`)
   - **Citizen**: Switch to Citizen Portal (`/portal` or `/transparency`)
4. Capture each screen at full 1080p ($1920 \times 1080$) resolution using browser Developer Tools (`Ctrl+Shift+P` -> "Capture full size screenshot" or Windows `Win + Shift + S`).
5. Save captured images into `/docs_submission/screenshots/` matching filenames `SS-01_apex_command.png` through `SS-12_gram_sabha.png`.
