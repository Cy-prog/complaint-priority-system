import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palette
    C_NAVY_DARK = RGBColor(11, 25, 44)      # #0B192C
    C_NAVY_CARD = RGBColor(22, 38, 62)      # #16263E
    C_SAFFRON   = RGBColor(249, 115, 22)    # #F97316
    C_TEAL      = RGBColor(16, 185, 129)    # #10B981
    C_INDIGO    = RGBColor(99, 102, 241)    # #6366F1
    C_WHITE     = RGBColor(255, 255, 255)
    C_MUTED     = RGBColor(148, 163, 184)   # #94A3B8
    C_LIGHT_BG  = RGBColor(248, 250, 252)

    def set_slide_dark_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_NAVY_DARK
        bg.line.color.rgb = C_NAVY_DARK

    def add_header(slide, title_text, category_text="SMARTCIVIC AI • B.TECH MAJOR PROJECT"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_SAFFRON

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(30, 58, 95)
        line.line.color.rgb = RGBColor(30, 58, 95)

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=C_SAFFRON, title_size=14, body_size=11):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_NAVY_CARD
        card.line.color.rgb = RGBColor(40, 70, 105)
        card.line.width = Pt(1)

        # Content
        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(title_size)
        p_t.font.bold = True
        p_t.font.color.rgb = accent_color
        p_t.space_after = Pt(8)

        for b in body_bullets:
            p_b = tf.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(body_size)
            p_b.font.color.rgb = C_WHITE
            p_b.space_after = Pt(4)

    # ==================== SLIDE 1: TITLE ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s1)

    # Accent glow top bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_SAFFRON
    bar.line.color.rgb = C_SAFFRON

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "B.TECH MAJOR PROJECT PRESENTATION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_SAFFRON
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "SmartCivic AI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Intelligent Civic Complaint Management and Predictive Governance System"
    p2.font.size = Pt(20)
    p2.font.color.rgb = C_TEAL
    p2.space_after = Pt(24)

    p3 = tf.add_paragraph()
    p3.text = "An End-to-End Municipal Intelligence Platform with Explainable AI Triage, Deterministic Safety Invariants, GIS Clustering, and Proactive SLA Escalation"
    p3.font.size = Pt(12)
    p3.font.color.rgb = C_MUTED

    # Metadata card bottom
    mc = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.4), Inches(11.333), Inches(1.3))
    mc.fill.solid()
    mc.fill.fore_color.rgb = C_NAVY_CARD
    mc.line.color.rgb = RGBColor(40, 70, 105)

    mtb = s1.shapes.add_textbox(Inches(1.2), Inches(5.5), Inches(11.0), Inches(1.1))
    mtf = mtb.text_frame
    mtf.word_wrap = True
    mp = mtf.paragraphs[0]
    mp.text = "Project Domain: Artificial Intelligence • Applied Machine Learning • Predictive Governance • Municipal Systems"
    mp.font.size = Pt(11)
    mp.font.bold = True
    mp.font.color.rgb = C_WHITE

    mp2 = mtf.add_paragraph()
    mp2.text = "Tech Stack: FastAPI • Scikit-learn LinearSVC • SQLAlchemy • OpenStreetMap GIS • Jinja2 • Tailwind CSS • PyTest (29/29 Verified)"
    mp2.font.size = Pt(10)
    mp2.font.color.rgb = C_SAFFRON

    # ==================== SLIDE 2: MOTIVATION & PROBLEM ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s2)
    add_header(s2, "Problem Statement & Civic Governance Inefficiencies")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "1. Triage Breakdown", [
                 "Municipalities receive thousands of unstructured grievances across water, electricity, drainage, and roads.",
                 "Manual triage creates severe bottlenecks, with delays of 4-7 days before an officer even opens a ticket.",
                 "Zero real-time urgency detection causes emergency hazards (gas leaks, open live wires) to sit in backlogs.",
                 "Citizens face complete opacity and lack of live resolution visibility."
             ], C_SAFFRON)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "2. The Black-Box AI Risk", [
                 "Naive AI prototypes hallucinate or lower urgency based on polite citizen wording or negative sentiment.",
                 "Lack of deterministic safety overrides leads to dangerous classifications of life-threatening issues.",
                 "Absence of factor explainability breeds mistrust among municipal commissioners and field engineers.",
                 "Synthetic data claims fail catastrophically under real multilingual municipal conditions."
             ], C_INDIGO)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "3. The SmartCivic Solution", [
                 "Unified triage marrying TF-IDF + LinearSVC with non-downgrade deterministic safety invariants.",
                 "Granular explainability: factor breakdown (urgency, severity, duration, vulnerable population).",
                 "Multi-tier RBAC for Citizens, Officers, Department Admins, and Apex Authorities.",
                 "Active SLA deadline countdowns with automated priority escalation sweeps."
             ], C_TEAL)

    # ==================== SLIDE 3: SYSTEM ARCHITECTURE ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s3)
    add_header(s3, "High-Level Architecture & Layered System Blueprint")

    add_card(s3, Inches(0.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Presentation Layer", [
                 "Server-Rendered FastAPI with Jinja2 Templates.",
                 "Dynamic reactive UI via HTMX & Alpine.js.",
                 "Tailwind CSS Smart City Command Center identity.",
                 "Citizen Portal, Ward Queue, and Dept Workspace.",
                 "Leaflet + OpenStreetMap GIS map."
             ], C_TEAL)

    add_card(s3, Inches(3.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Application & Core", [
                 "FastAPI ASGI high-concurrency engine.",
                 "Cryptographic timed sessions & 4-tier RBAC.",
                 "SLA Breach Escalation daemon service.",
                 "Department workload load-balancing engine.",
                 "MIME & magic byte secure upload validation."
             ], C_SAFFRON)

    add_card(s3, Inches(6.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "AI & Analytics Core", [
                 "LinearSVC Calibrated Category Classifier.",
                 "Rule-based Safety Invariant Guard.",
                 "Multi-factor Explainable Priority Engine.",
                 "SentenceTransformer Cosine Duplicate Engine.",
                 "14-day OLS Time-Series Forecaster (95% CI)."
             ], C_INDIGO)

    add_card(s3, Inches(9.8), Inches(1.8), Inches(2.7), Inches(5.0),
             "Persistence & Storage", [
                 "SQLAlchemy ORM with SQLite / PostgreSQL support.",
                 "14 Normalized Tables with Foreign Key integrity.",
                 "Audit logging of all human & AI decisions.",
                 "Evidence photo storage with strict security.",
                 "Export engine: CSV, Excel & PyMuPDF Dossiers."
             ], C_WHITE)

    # ==================== SLIDE 4: ML BENCHMARK ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s4)
    add_header(s4, "AI Model Benchmarking & Multi-Algorithm Empirical Evaluation")

    # Table of benchmark results
    table_shape = s4.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.6))
    table = table_shape.table
    table.columns[0].width = Inches(2.9)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.2)
    table.columns[4].width = Inches(2.2)

    headers = ["Model Candidate", "Test Accuracy", "Macro F1-Score", "5-Fold CV Mean", "Production Status"]
    rows = [
        ["LinearSVC (Calibrated)", "96.00%", "0.9554", "0.9075 (+-0.038)", "CHOSEN PRIMARY"],
        ["Logistic Regression", "94.00%", "0.9329", "0.9000 (+-0.037)", "Fallback Candidate"],
        ["Multinomial Naive Bayes", "92.00%", "0.9094", "0.8875 (+-0.031)", "Baseline Reference"],
        ["SGD Classifier (Log Loss)", "92.00%", "0.9093", "0.8825 (+-0.030)", "Alternative Candidate"]
    ]

    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_SAFFRON
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(11)
            p.font.color.rgb = C_NAVY_DARK

    for row_idx, r in enumerate(rows):
        for col_idx, val in enumerate(r):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_NAVY_CARD if row_idx % 2 == 0 else RGBColor(18, 30, 50)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.color.rgb = C_TEAL if col_idx == 4 and "CHOSEN" in val else C_WHITE

    add_card(s4, Inches(0.8), Inches(4.7), Inches(5.7), Inches(2.2),
             "Empirical Methodology & Integrity", [
                 "Strict 80/20 train/test split with stratified class distributions.",
                 "5-fold cross-validation across 9 civic categories.",
                 "CalibratedClassifierCV enables true posterior probability estimates.",
                 "Zero data fabrication: results benchmarked directly on local dataset."
             ], C_TEAL, title_size=12, body_size=10)

    add_card(s4, Inches(6.8), Inches(4.7), Inches(5.7), Inches(2.2),
             "Inference Pipeline & Confidence Gate", [
                 "Model version tracked: 2.0.0-SmartCivic.",
                 "Confidence thresholding: predictions < 0.40 flag 'needs_human_review = True'.",
                 "Integrated Hindi/English language detection and entity extraction.",
                 "Full feature importance attribution via top linear coefficients."
             ], C_INDIGO, title_size=12, body_size=10)

    # ==================== SLIDE 5: PRIORITY ENGINE ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s5)
    add_header(s5, "Explainable Multi-Factor Priority Scoring & Safety Invariants")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Dynamic Multi-Factor Formulation", [
                 "Priority Score formula calculates a weighted sum in range [0, 100]:",
                 "Score = W_urgency * Urg + W_severity * Sev + W_population * Pop + W_hazard * Haz + W_duration * Dur + W_essential * Ess + W_vulnerable * Vuln",
                 "Weights dynamically validated via Pydantic model from config YAML.",
                 "Urgency & Severity derived from NLP entity extraction & keywords.",
                 "Duration escalation: complaints persisting > 7 days gain automatic score bonus.",
                 "Transparent factor attribution stored with every complaint analysis record."
             ], C_SAFFRON)

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Deterministic Non-Downgrade Safety Guard", [
                 "CORE SAFETY PRINCIPLE: AI must never downgrade a life-threatening incident.",
                 "Deterministic keyword rules scan for: gas leaks, sparking poles, structural collapse, fire, child peril, hospital road blockage.",
                 "Safety rules execute AFTER machine learning scoring as an immutable invariant.",
                 "If hazard is detected, priority is forced to CRITICAL (Score >= 80).",
                 "Rule triggers record auditable reason tags (e.g., 'HAZARD_ELECTRICAL_SPARK').",
                 "Prevents polite or calm phrasing from masking fatal hazards."
             ], C_TEAL)

    # ==================== SLIDE 6: DEPARTMENT MANAGEMENT ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s6)
    add_header(s6, "Municipal Department Management & Officer Load Balancing")

    add_card(s6, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Municipal Hierarchy", [
                 "11 Configured Municipal Departments (Water Supply, Sanitation, Roads, Electricity, Public Health, Drainage, Streetlighting, etc.).",
                 "Officers assigned to dedicated departmental divisions.",
                 "Department Admins possess granular view over divisional queue.",
                 "Complete operational isolation between divisions."
             ], C_TEAL)

    add_card(s6, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "AI Assignment Balancing", [
                 "Automated officer recommendation: algorithm queries active workload.",
                 "Ranks officers by current open ticket count to prevent burnout.",
                 "Officers tagged as: Available (<5), Busy (5-11), Overloaded (12+).",
                 "Manual override allows supervisor reassignment with mandatory audit notes."
             ], C_SAFFRON)

    add_card(s6, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Field Officer Queue", [
                 "Mobile-optimized officer dashboard (/officer).",
                 "Real-time list of assigned complaints sorted by urgency.",
                 "One-click status transition: Open -> In Progress -> Resolved.",
                 "On-site photo resolution evidence upload with timestamp verification."
             ], C_INDIGO)

    # ==================== SLIDE 7: SLA ESCALATION ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s7)
    add_header(s7, "Configurable SLA Engine & Automated Breach Escalation")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Priority-Based SLA Deadlines", [
                 "Configurable SLA resolution windows defined per priority:",
                 "• CRITICAL: 6 Hours (Immediate Emergency Dispatch)",
                 "• HIGH: 24 Hours (Essential Service Disruption)",
                 "• MEDIUM: 72 Hours (Standard Civic Maintenance)",
                 "• LOW: 168 Hours / 7 Days (Non-urgent Infrastructure)",
                 "Deadlines stored in SLARecord with millisecond precision.",
                 "Real-time countdown indicators displayed on administrative dashboards."
             ], C_SAFFRON)

    add_card(s7, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Automated Escalation Daemon", [
                 "Automated sweep identifies unresolved tickets past deadline.",
                 "Sets is_breached = True and computes breach latency.",
                 "Automated Priority Promotion: elevates complaint by +1 level (e.g. HIGH -> CRITICAL).",
                 "Adds +20 priority score increment up to ceiling 100.",
                 "Generates high-priority in-app and SMTP email breach alerts to supervisors.",
                 "Logs status transition in complaint_status_history with actor ID."
             ], C_TEAL)

    # ==================== SLIDE 8: GIS INTELLIGENCE ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s8)
    add_header(s8, "GIS Spatial Intelligence & Municipal Incident Clustering")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Geographic Incident Mapping", [
                 "Leaflet.js + OpenStreetMap integration at /map.",
                 "Real GPS coordinates ingested from mobile submissions.",
                 "High-precision centroid coordinates mapped across Gwalior Municipal Wards (e.g., Lashkar, Morar, City Center, Hazira, Thatipur).",
                 "Interactive color-coded markers by priority: Red (Critical), Orange (High), Blue (Medium), Slate (Low).",
                 "Zero fake spatial data: distinguishes GPS pins from ward centroids."
             ], C_INDIGO)

    add_card(s8, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Spatial Outbreak & Hotspot Detection", [
                 "Cluster detection groups complaints occurring within 500m / 48hr window.",
                 "Detects contaminated water outbreaks, sewage flooding, and power grid failures.",
                 "Spatial outbreak radar alerts municipal commissioners in real-time.",
                 "Ward-wise risk scoring highlights overburdened municipal zones.",
                 "Enables proactive deployment of sanitation and repair squads."
             ], C_TEAL)

    # ==================== SLIDE 9: PREDICTIVE GOVERNANCE ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s9)
    add_header(s9, "Predictive Governance: 14-Day OLS Volume Forecasting")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Empirical Time-Series Modeling", [
                 "14-day projection using Ordinary Least Squares (OLS) regression over historical daily complaint inflow.",
                 "Parametric 95% Confidence Interval band based on residual variance and expanding forecast horizon factor.",
                 "Trend slope and direction classification: INCREASING, DECREASING, or STABLE.",
                 "Visualized on Chart.js canvas with interactive historical and predicted series.",
                 "Methodological transparency disclaimer displayed to prevent misinterpretation."
             ], C_SAFFRON)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Recurring Hotspots & Seasonal Directives", [
                 "Recurring Failure Detection: groups repeat breakdowns within identical wards and categories.",
                 "Generates automated preventive maintenance directives (e.g., desilting, transformer inspection).",
                 "Seasonal Preparedness Rules: maps meteorological cycles to civic hazards (Monsoon waterlogging, Summer water scarcity).",
                 "Enables proactive pre-monsoon drain clearance and preventative equipment overhaul."
             ], C_TEAL)

    # ==================== SLIDE 10: CITIZEN & TRANSPARENCY ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s10)
    add_header(s10, "Citizen Empowerment & Public Privacy-Safe Transparency")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Advanced Citizen Experience (/portal)", [
                 "Simple, accessible grievance filing in Hindi & English.",
                 "Photo evidence upload with magic byte security validation.",
                 "Instant unique tracking token generation (e.g. CMP-A1B2C3).",
                 "Live status tracker with transparent AI priority reasoning.",
                 "Citizen satisfaction feedback & one-click reopen functionality.",
                 "Audit logging of all citizen reopen events."
             ], C_TEAL)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Public Civic Transparency Portal (/transparency)", [
                 "Open Governance: live municipal resolution rate & SLA compliance percentage.",
                 "Sanitized real-time resolution feed displaying category, ward, and resolution timestamp.",
                 "Zero PII Exposure: strict compliance with Digital Personal Data Protection (DPDP) Act.",
                 "Citizen names, phone numbers, and private house numbers completely redacted.",
                 "Public confidence building through verifiable civic accountability."
             ], C_SAFFRON)

    # ==================== SLIDE 11: VERIFICATION & TESTING ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s11)
    add_header(s11, "Verification, Testing Rigor & Security Audit Results")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Automated Test Suite", [
                 "29/29 Automated PyTest Unit & Integration Tests Passing (100% Green).",
                 "Health check & API routing verification.",
                 "Auth registration, token creation & 4-tier RBAC enforcement.",
                 "AI classification, priority scoring & safety overrides.",
                 "Predictive forecast & GIS marker endpoints.",
                 "CSV, Excel & PDF export byte validation."
             ], C_TEAL)

    add_card(s11, Inches(4.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Security Architecture", [
                 "Cryptographic timed session tokens (URLSafeTimedSerializer).",
                 "Strict RBAC guarding routes at ASGI middleware layer.",
                 "File upload validation: checks MIME type, max size (10MB), and image magic bytes (PNG, JPEG, WebP).",
                 "Mitigates directory traversal, path injection, and malicious script uploads."
             ], C_SAFFRON)

    add_card(s11, Inches(8.8), Inches(1.8), Inches(3.6), Inches(5.0),
             "Reporting & Multi-Format Exports", [
                 "Instant CSV export of complete grievance registry.",
                 "Multi-sheet Excel analytics workbook (xlsxwriter) with departmental breakdown.",
                 "Executive PDF dossier (fitz / PyMuPDF) for municipal commissioner meetings.",
                 "Sabha audit reports for democratic civic hearings."
             ], C_INDIGO)

    # ==================== SLIDE 12: CONCLUSION ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s12)
    add_header(s12, "Major Project Highlights & Future Roadmap")

    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Key Project Innovations", [
                 "Elevated prototype into a complete, enterprise-grade municipal platform.",
                 "Preserved working baseline while adding 8 major modules and 4-tier governance.",
                 "Engineered explainable AI with non-negotiable deterministic safety invariants.",
                 "Empirical multi-model benchmark proving 96.00% accuracy on LinearSVC.",
                 "Active SLA auto-escalation daemon preventing tickets from languishing.",
                 "Pioneered predictive governance with 14-day OLS time-series forecasting."
             ], C_SAFFRON)

    add_card(s12, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0),
             "Future Engineering Scope", [
                 "IoT Telemetry Integration: connect real-time water pipeline pressure sensors and smart electric meters directly into AI pipeline.",
                 "WhatsApp Bot & Voice IVR: enable grievance lodging via WhatsApp Business API and automated Hindi speech-to-text.",
                 "Computer Vision Hazard Assessment: CNN/Transformer image analysis to detect pothole severity and trash overflow from photos.",
                 "Distributed Microservices: container orchestration on Kubernetes with Kafka event streaming for metropolitan-scale deployment."
             ], C_TEAL)

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out = "smartcivic_ai_presentation.pptx"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    create_deck(out)
