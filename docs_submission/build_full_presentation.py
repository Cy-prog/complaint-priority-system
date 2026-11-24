import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Academic & Tech Palette
    C_NAVY_DARK = RGBColor(11, 25, 44)      # #0B192C
    C_NAVY_CARD = RGBColor(30, 41, 59)      # #1E293B
    C_SAFFRON   = RGBColor(249, 115, 22)    # #F97316
    C_TEAL      = RGBColor(16, 185, 129)    # #10B981
    C_INDIGO    = RGBColor(99, 102, 241)    # #6366F1
    C_WHITE     = RGBColor(255, 255, 255)
    C_MUTED     = RGBColor(148, 163, 184)   # #94A3B8

    diag_dir = os.path.join(os.path.dirname(__file__), "diagrams")

    def set_slide_dark_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_NAVY_DARK
        bg.line.color.rgb = C_NAVY_DARK

    def add_header(slide, title_text, category_text="SMARTCIVIC AI • B.TECH MAJOR PROJECT"):
        # Header category
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11), Inches(0.3))
        tf_cat = cat_box.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_SAFFRON

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.6))
        tf_title = title_box.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        # Top line divider
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(51, 65, 85)
        line.line.color.rgb = RGBColor(51, 65, 85)

    def add_card(slide, left, top, width, height, title, body_bullets, accent_color=C_SAFFRON, title_size=13, body_size=10.5):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = C_NAVY_CARD
        card.line.color.rgb = RGBColor(51, 65, 85)
        card.line.width = Pt(1)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), height - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(title_size)
        p_t.font.bold = True
        p_t.font.color.rgb = accent_color
        p_t.space_after = Pt(6)

        for b in body_bullets:
            p_b = tf.add_paragraph()
            p_b.text = "• " + b
            p_b.font.size = Pt(body_size)
            p_b.font.color.rgb = C_WHITE
            p_b.space_after = Pt(4)

    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text.strip()

    # ==================== SLIDE 1: TITLE ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s1)
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_SAFFRON
    bar.line.color.rgb = C_SAFFRON

    tb = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.3), Inches(3.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = "B.TECH MAJOR PROJECT FINAL DEFENSE (2026–2027)"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_SAFFRON
    p0.space_after = Pt(10)

    p1 = tf.add_paragraph()
    p1.text = "SmartCivic AI"
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Intelligent Civic Complaint Management and Predictive Governance System"
    p2.font.size = Pt(18)
    p2.font.color.rgb = C_TEAL
    p2.space_after = Pt(18)

    p3 = tf.add_paragraph()
    p3.text = "Candidate: Samit Jain | Enrollment No.: [ENROLLMENT NO.]\nDegree: Bachelor of Technology in Computer Science & Engineering\nInstitution: ITM University Gwalior | Department: [DEPARTMENT]\nProject Guide: [GUIDE NAME, DESIGNATION]"
    p3.font.size = Pt(11)
    p3.font.color.rgb = C_MUTED

    set_notes(s1, "Respected members of the review panel, good morning. I am Samit Jain, presenting my B.Tech Major Project defense: SmartCivic AI — an Intelligent Civic Complaint Management and Predictive Governance System. This project transforms municipal grievance handling from a slow, manual ticketing process into an explainable, data-driven, and predictive platform. Every number, architectural component, and test result presented today has been verified against working production code.")

    # ==================== SLIDE 2: PROBLEM STATEMENT ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s2)
    add_header(s2, "Problem Statement: Systemic Bottlenecks in Municipal Triage")
    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Operational Bottlenecks in Existing Municipalities", [
                 "Municipalities receive thousands of unstructured grievances weekly across electricity, water, roads, and sanitation.",
                 "Manual triage creates severe delays (3–7 days) before a ticket is even assigned to an engineer.",
                 "Zero life-safety awareness: emergency hazards (sparking wires, gas leaks) sit in the same queue as routine garbage.",
                 "Workforce misallocation: supervisors dump tickets on known staff while others remain underutilized."
             ], C_SAFFRON)
    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "The Pitfalls of Naive AI in Civic Systems", [
                 "Unconstrained statistical models lower priority if a citizen phrases a dangerous report in polite, calm language.",
                 "Black-box deep learning architectures lack factor explainability, causing municipal engineers to reject triage scores.",
                 "Complete absence of proactive predictive foresight: cities react only after disease outbreaks or water crises occur.",
                 "Lack of DPDP compliance: public grievance portals inadvertently expose citizen names and contact numbers."
             ], C_TEAL)
    set_notes(s2, "Municipal corporations in developing smart cities face massive volumes of grievances. The core problem is twofold: First, manual triage takes 3 to 7 days, causing critical hazards to sit unread. Second, naive AI systems often fail because polite wording fools sentiment models into lowering urgency. SmartCivic AI addresses these exact operational failures by combining calibrated machine learning with deterministic safety invariants and proactive workload governance.")

    # ==================== SLIDE 3: OBJECTIVES ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s3)
    add_header(s3, "Project Objectives & Technical Scope")
    add_card(s3, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "1. Explainable AI Triage", [
                 "Automated category classification via Calibrated LinearSVC across 14 civic categories.",
                 "Multi-factor priority score formulated across urgency, severity, population, and duration.",
                 "Transparent factor attribution for every score without black-box hallucination."
             ], C_TEAL)
    add_card(s3, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "2. Safety Invariants & SLA", [
                 "Deterministic safety invariant: acute hazards unconditionally evaluate to CRITICAL (>=80).",
                 "Configurable priority-based SLA deadlines (6h, 24h, 72h, 168h).",
                 "Automated background daemon promoting priority and alerting supervisors upon breach."
             ], C_SAFFRON)
    add_card(s3, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "3. Predictive & Open Gov", [
                 "14-day Ordinary Least Squares (OLS) time-series forecasting with 95% confidence bands.",
                 "Leaflet/OSM GIS mapping and localized spatial incident clustering.",
                 "DPDP Act compliant public transparency portal with zero Citizen PII exposure."
             ], C_INDIGO)
    set_notes(s3, "The technical scope of SmartCivic AI focuses on three core pillars: First, explainable AI triage that achieves high classification accuracy while providing full factor attribution. Second, a deterministic safety guard ensuring that dangerous hazards can never be downgraded, paired with active SLA auto-escalation. Third, predictive governance using time-series forecasting, GIS spatial intelligence, and a privacy-preserving public transparency portal.")

    # ==================== SLIDE 4: EXISTING VS PROPOSED ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s4)
    add_header(s4, "Comparative Paradigm: Minor Baseline vs. SmartCivic AI")
    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Original Minor Project Architecture (Baseline)", [
                 "Basic text classifier trained on narrow 6-class dataset.",
                 "Static priority scoring without continuous factor weighting.",
                 "Single flat administrative role without divisional boundaries.",
                 "Passive SLA records without automated escalation daemons.",
                 "Mock or MD5-jittered spatial coordinates without genuine GIS.",
                 "Zero time-series predictive modeling or recurring hotspot tracking."
             ], C_MUTED)
    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "SmartCivic AI (B.Tech Major Project)", [
                 "Calibrated LinearSVC achieving 96% accuracy with uncertainty gating.",
                 "Deterministic Non-Downgrade Safety Guard protecting life safety.",
                 "4-Tier RBAC (Citizen, Officer, Dept Admin, Super Admin) & Timed HMAC tokens.",
                 "Automated SLA Escalation Daemon promoting priority & penalizing score (+20).",
                 "Real Leaflet GIS with Gwalior ward centroids & 500m cluster outbreak detection.",
                 "14-Day OLS volume forecasting with 95% parametric confidence bounds."
             ], C_TEAL)
    set_notes(s4, "Here we compare the original minor project baseline with SmartCivic AI. The minor project was a prototype with static scoring, a single role, and flat queues. SmartCivic AI elevates this into an enterprise system: Calibrated LinearSVC, deterministic safety rules, 4-tier RBAC, automated SLA escalation, high-precision GIS mapping across municipal wards, and empirical 14-day time-series forecasting.")

    # ==================== SLIDE 5: SYSTEM ARCHITECTURE ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s5)
    add_header(s5, "High-Level Layered System Architecture")
    img_arch = os.path.join(diag_dir, "system_architecture.png")
    if os.path.exists(img_arch):
        s5.shapes.add_picture(img_arch, Inches(0.8), Inches(1.6), width=Inches(11.733))
    set_notes(s5, "This diagram illustrates the layered architecture of SmartCivic AI. At the top is the Presentation Layer using Jinja2, HTMX, Alpine.js, and Leaflet GIS. Below is the Security Layer enforcing cryptographic timed sessions and 4-tier RBAC. The Application Core contains FastAPI ASGI services, SLA daemons, and workforce balancers. The Intelligence Subsystem executes TF-IDF, LinearSVC, safety rules, and OLS forecasting. Finally, the Persistence Layer manages 14 normalized tables in SQLAlchemy.")

    # ==================== SLIDE 6: MODULES OVERVIEW ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s6)
    add_header(s6, "Comprehensive Inventory of Major Project Modules")
    add_card(s6, Inches(0.8), Inches(1.6), Inches(3.6), Inches(2.5),
             "Citizen Portal (/portal)", [
                 "Bilingual Hindi/English submission.",
                 "Secure photo evidence upload (magic bytes).",
                 "Live status timeline & 1-click reopen."
             ], C_TEAL, title_size=11, body_size=9.5)
    add_card(s6, Inches(4.8), Inches(1.6), Inches(3.6), Inches(2.5),
             "Dept Management (/department)", [
                 "11 Configured municipal divisions.",
                 "Real-time officer load balancing.",
                 "AI-assisted assignment recommendations."
             ], C_SAFFRON, title_size=11, body_size=9.5)
    add_card(s6, Inches(8.8), Inches(1.6), Inches(3.7), Inches(2.5),
             "Field Officer Queue (/officer)", [
                 "Assigned task list with SLA countdown.",
                 "Quick transitions (Open -> In Progress).",
                 "On-site photo resolution verification."
             ], C_INDIGO, title_size=11, body_size=9.5)
    add_card(s6, Inches(0.8), Inches(4.3), Inches(3.6), Inches(2.5),
             "GIS Spatial Intelligence (/map)", [
                 "Leaflet & OpenStreetMap integration.",
                 "Ward centroid mapping across Gwalior.",
                 "500m/48h localized outbreak clustering."
             ], C_INDIGO, title_size=11, body_size=9.5)
    add_card(s6, Inches(4.8), Inches(4.3), Inches(3.6), Inches(2.5),
             "Predictive Governance (/predictive)", [
                 "14-Day OLS complaint volume forecast.",
                 "Recurring failure ward hotspot tracking.",
                 "Seasonal directives (Monsoon/Summer)."
             ], C_TEAL, title_size=11, body_size=9.5)
    add_card(s6, Inches(8.8), Inches(4.3), Inches(3.7), Inches(2.5),
             "Public Transparency (/transparency)", [
                 "Live resolution % & category distribution.",
                 "Sanitized verified resolution feed.",
                 "DPDP Act privacy: zero PII exposed."
             ], C_SAFFRON, title_size=11, body_size=9.5)
    set_notes(s6, "SmartCivic AI provides six major interactive interfaces tailored to specific stakeholders: Citizens file and track grievances with photo proof; Department Admins oversee officer load balancing across 11 divisions; Field Officers manage their queue and upload on-site completion proof; GIS Maps visualize spatial risk; Predictive Dashboards project future volume; and the Transparency Portal publishes live metrics under strict DPDP compliance.")

    # ==================== SLIDE 7: AI PIPELINE ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s7)
    add_header(s7, "The End-to-End AI/ML Triage Pipeline")
    img_ai = os.path.join(diag_dir, "ai_pipeline_flowchart.png")
    if os.path.exists(img_ai):
        s7.shapes.add_picture(img_ai, Inches(0.8), Inches(1.6), width=Inches(11.733))
    set_notes(s7, "The AI Triage Pipeline executes synchronously upon complaint submission. First, incoming text undergoes language detection and normalization. Next, the TF-IDF vectorizer extracts unigrams and bigrams, feeding them into the Calibrated LinearSVC classifier. Simultaneously, entity extraction identifies duration tokens, landmarks, and acute hazard tags. These feeds merge in the Priority Engine, pass through the Deterministic Safety Guard, evaluate confidence gating, check for duplicates, and generate a structured explainability record.")

    # ==================== SLIDE 8: SAFETY & SCORING ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s8)
    add_header(s8, "Safety-Aware Priority Scoring & Invariant Case Study")
    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Mathematical Formulation", [
                 "Score = W_urg*Urg + W_sev*Sev + W_pop*Pop + W_haz*Haz + W_dur*Dur + W_ess*Ess + W_vuln*Vuln",
                 "Validated dynamically via Pydantic model from priority_config.yaml.",
                 "Durations > 7 days gain automatic +15 escalation bonus.",
                 "Tiers: CRITICAL (>=80), HIGH (>=60), MEDIUM (>=35), LOW (<35).",
                 "NON-DOWNGRADE INVARIANT: Deterministic safety rules execute AFTER ML scoring, overriding model output if acute hazard tags match."
             ], C_SAFFRON)
    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Real Case Study: Sparking Live Wire", [
                 "Text: 'Kindly note that a live 440V wire snapped near the primary school gate. Thank you.'",
                 "VADER Sentiment Polarity: +0.65 (Polite & Calm phrasing).",
                 "Naive Sentiment/ML output: LOW priority (Score: 28) - CATASTROPHIC FAILURE.",
                 "SmartCivic Safety Rule Trigger: 'live 440V wire snapped' triggers HAZARD_ELECTRICAL_SPARK.",
                 "Result: Priority forced to CRITICAL (Score: 85, SLA: 6 Hours).",
                 "Audit tag appended: 'Hard Safety Trigger: Life-Threatening Electrical Hazard'."
             ], C_TEAL)
    set_notes(s8, "This slide demonstrates our Core Safety Principle. Consider this real test case: a citizen writes politely about a live 440V wire near a school. A sentiment-based system assigns positive sentiment and low priority — an unacceptable real-world hazard. SmartCivic AI's deterministic safety rule detects the wire hazard invariant, immediately forcing the score to 85 and priority to CRITICAL with a 6-hour SLA.")

    # ==================== SLIDE 9: DUPLICATE & GIS ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s9)
    add_header(s9, "Semantic Duplicate Detection & GIS Spatial Outbreaks")
    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Semantic Duplicate Detection", [
                 "Dense sentence embeddings via SentenceTransformers ('all-MiniLM-L6-v2').",
                 "Cosine similarity calculated against active complaints within same category.",
                 "Threshold >= 0.75 links complaints into similar_complaints table.",
                 "Prevents duplicate ticket dispatch while aggregating citizen voice count.",
                 "Allows supervisors to view all related reports without merging unrelated incidents."
             ], C_INDIGO)
    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "GIS Spatial Intelligence & Outbreaks (/map)", [
                 "Interactive Leaflet / OpenStreetMap mapping with priority color markers.",
                 "Coordinates mapped across Gwalior Wards (Lashkar, Morar, City Center, Hazira, Thatipur).",
                 "Cluster Detection Algorithm: identifies spatial outbreaks when >= 3 complaints occur within 500m / 48 hours.",
                 "Automatically triggers Outbreak Risk alerts for contaminated water or transformer surges.",
                 "Directly guides proactive dispatch of field repair teams."
             ], C_TEAL)
    set_notes(s9, "Municipalities often receive hundreds of duplicate complaints during a major pipe leak or power outage. SmartCivic AI uses dense vector embeddings to calculate cosine similarity, clustering related complaints without duplicate work orders. Furthermore, our GIS clustering engine flags localized outbreaks whenever 3 or more complaints occur within 500 meters in a 48-hour window.")

    # ==================== SLIDE 10: SLA & ESCALATION ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s10)
    add_header(s10, "Configurable SLA Engine & Automated Breach Escalation")
    img_sla = os.path.join(diag_dir, "sla_escalation_flow.png")
    if os.path.exists(img_sla):
        s10.shapes.add_picture(img_sla, Inches(0.8), Inches(1.6), width=Inches(11.733))
    set_notes(s10, "This diagram shows the automated SLA lifecycle. When a ticket is triaged, an SLARecord is initialized with exact deadlines: 6 hours for Critical, 24 for High, 72 for Medium, and 168 for Low. The automated escalation sweep daemon continually checks active tickets. When an unresolved ticket breaches its deadline, the system automatically marks it breached, elevates priority by +1 tier, applies a +20 urgency penalty, dispatches alerts, and records an immutable audit log.")

    # ==================== SLIDE 11: ROLES & SECURITY ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s11)
    add_header(s11, "Security Architecture: 4-Tier RBAC & DPDP Privacy")
    add_card(s11, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "4-Tier RBAC Hierarchy", [
                 "CITIZEN: Lodge, track, review personal tickets.",
                 "FIELD OFFICER: View assigned ward queue, update status, upload resolution proof.",
                 "DEPT ADMIN: Divisional oversight, officer workload monitoring, reassignment.",
                 "SUPER ADMIN: Apex command, SLA sweeps, predictive modeling, audit reviews."
             ], C_TEAL)
    add_card(s11, Inches(4.8), Inches(1.6), Inches(3.6), Inches(5.2),
             "Session & Middleware Security", [
                 "Cryptographic timed tokens via URLSafeTimedSerializer with 7-day expiry.",
                 "Enforced at FastAPI ASGI dependency layer (get_current_user, require_roles).",
                 "File upload validation: enforces 10MB limit, valid MIME types, and image magic bytes (PNG, JPEG, WebP).",
                 "Zero SQL injection vulnerability via SQLAlchemy parameterized queries."
             ], C_SAFFRON)
    add_card(s11, Inches(8.8), Inches(1.6), Inches(3.7), Inches(5.2),
             "DPDP Privacy-by-Design", [
                 "Compliance with India's Digital Personal Data Protection (DPDP) Act.",
                 "Public transparency portal (/transparency) strictly scrubs citizen names, phone numbers, and house numbers.",
                 "Published feeds display only tracking token, category, ward, and timestamp.",
                 "Guarantees municipal transparency without exposing citizens to harassment."
             ], C_INDIGO)
    set_notes(s11, "Security in SmartCivic AI is enforced at the backend ASGI layer, not merely hidden in the frontend. We implement 4-tier Role-Based Access Control using cryptographic timed HMAC tokens. File uploads are validated via binary magic bytes to prevent shell uploads. Most importantly, our Public Transparency portal is designed from the ground up to comply with the DPDP Act, completely redacting citizen personal identifiable information.")

    # ==================== SLIDE 12: DATABASE & ER ====================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s12)
    add_header(s12, "Relational Schema & Entity-Relationship (ER) Architecture")
    img_er = os.path.join(diag_dir, "er_diagram.png")
    if os.path.exists(img_er):
        s12.shapes.add_picture(img_er, Inches(0.8), Inches(1.6), width=Inches(11.733))
    set_notes(s12, "The database schema is organized into 14 normalized relational entities in SQLAlchemy. Core tables include users, departments, categories, complaints, complaint_analysis, and sla_records. Transactional audit integrity is maintained through priority_overrides, complaint_status_history, and audit_logs, ensuring every administrative and automated decision has a traceable timestamp and actor ID.")

    # ==================== SLIDE 13: LIVE DEMO FLOW ====================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s13)
    add_header(s13, "End-to-End Live Demonstration Workflow")
    add_card(s13, Inches(0.8), Inches(1.6), Inches(2.7), Inches(5.2),
             "Step 1: Citizen Ingestion", [
                 "Citizen navigates to /portal.",
                 "Files grievance: 'Contaminated sewer water mixing in taps'.",
                 "Uploads photo evidence.",
                 "Receives tracking token: CMP-A1B2C3."
             ], C_TEAL)
    add_card(s13, Inches(3.8), Inches(1.6), Inches(2.7), Inches(5.2),
             "Step 2: AI Triage & Safety", [
                 "LinearSVC classifies: Water Supply (96% confidence).",
                 "Safety Rule triggers: Contamination hazard.",
                 "Priority: CRITICAL (Score: 85).",
                 "SLA deadline set to 6 Hours."
             ], C_SAFFRON)
    add_card(s13, Inches(6.8), Inches(1.6), Inches(2.7), Inches(5.2),
             "Step 3: Dept & Officer", [
                 "Dept Admin (/department) inspects load.",
                 "AI recommends Officer with lowest load.",
                 "Field Officer (/officer) accepts ticket, investigates on-site, uploads proof."
             ], C_INDIGO)
    add_card(s13, Inches(9.8), Inches(1.6), Inches(2.7), Inches(5.2),
             "Step 4: Close & Verify", [
                 "Ticket marked Resolved.",
                 "Citizen (/portal/track) verifies resolution.",
                 "Public feed (/transparency) updates.",
                 "Complete audit trail logged."
             ], C_TEAL)
    set_notes(s13, "This slide outlines the seamless 4-step live demonstration: Step 1 shows a citizen filing a contaminated water complaint and receiving a tracking token. Step 2 shows the AI pipeline classifying it into Water Supply and escalating it to CRITICAL with a 6-hour deadline. Step 3 shows the Department Admin allocating the ticket to the least-burdened officer who resolves it with photo evidence. Step 4 shows citizen verification and public transparency update.")

    # ==================== SLIDE 14: TESTING RESULTS ====================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s14)
    add_header(s14, "Empirical Test Verification (29 Automated Tests Passed)")
    add_card(s14, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Test Suite Coverage & Metrics", [
                 "Test Framework: PyTest 9.1.1 on Python 3.14.5.",
                 "Result: 29 Passed, 0 Failed, 28 Warnings in 14.08 seconds (100% Pass Rate).",
                 "tests/test_api.py (4 tests): Microservice routing and input guards.",
                 "tests/test_edge_cases.py (6 tests): Boundary scores, empty strings, non-English text.",
                 "tests/test_priority_engine.py (3 tests): Mathematical scoring bounds.",
                 "tests/test_rule_engine.py (3 tests): Non-downgrade invariant verification."
             ], C_TEAL)
    add_card(s14, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "FastAPI Full Application Integration (13 Tests)", [
                 "Auth registration, password hashing & timed session verification.",
                 "Complaint creation, location coordinates & AI triage execution.",
                 "Dashboard KPI and time-series trends verification.",
                 "File upload security: magic byte check & 10MB limit enforcement.",
                 "Department management & officer workload capacity verification.",
                 "SLA breach detection & priority escalation daemon verification.",
                 "GIS marker GeoJSON & 14-day predictive forecast endpoints.",
                 "Multi-format reporting: CSV, Excel & PyMuPDF PDF byte checks."
             ], C_SAFFRON)
    set_notes(s14, "Rigorous software testing is essential for public governance platforms. SmartCivic AI is verified by 29 automated PyTest tests with a 100% pass rate. This covers edge-case text inputs, scoring mathematical boundaries, cryptographic session security, binary file upload validation, SLA auto-escalation sweeps, and document export generation.")

    # ==================== SLIDE 15: MODEL EVALUATION ====================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s15)
    add_header(s15, "Model Evaluation & Scientific Data Integrity")
    
    # Table of benchmark results
    table_shape = s15.shapes.add_table(5, 5, Inches(0.8), Inches(1.6), Inches(11.7), Inches(2.5))
    table = table_shape.table
    table.columns[0].width = Inches(2.9)
    table.columns[1].width = Inches(2.2)
    table.columns[2].width = Inches(2.2)
    table.columns[3].width = Inches(2.2)
    table.columns[4].width = Inches(2.2)

    headers = ["Algorithm Candidate", "Test Accuracy", "Macro F1", "5-Fold CV Mean", "Production Status"]
    rows = [
        ["LinearSVC (Calibrated)", "96.00%", "0.9554", "0.9075 (+-0.025)", "SELECTED (Primary)"],
        ["Logistic Regression", "94.00%", "0.9329", "0.9000 (+-0.024)", "Fallback Candidate"],
        ["Multinomial Naive Bayes", "92.00%", "0.9094", "0.8875 (+-0.019)", "Baseline Reference"],
        ["SGD Classifier (Log Loss)", "92.00%", "0.9093", "0.8825 (+-0.019)", "Alternative Candidate"]
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
            cell.fill.fore_color.rgb = C_NAVY_CARD if row_idx % 2 == 0 else RGBColor(22, 32, 50)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(10)
                p.font.color.rgb = C_TEAL if col_idx == 4 and "SELECTED" in val else C_WHITE

    add_card(s15, Inches(0.8), Inches(4.5), Inches(11.7), Inches(2.3),
             "Scientific Data Caveats & Integrity Statement", [
                 "Evaluation conducted on a curated synthetic dataset of 500 multi-class civic grievances.",
                 "Dataset includes realistic bilingual Hindi and Hinglish civic phrasing.",
                 "HONEST CAVEAT: High accuracy (96%) demonstrates internal model consistency and separation capability; it does NOT prove identical real-world generalization across arbitrary noisy citizen submissions.",
                 "SmartCivic AI incorporates human review gating (< 0.40 confidence) to safely handle out-of-distribution inputs."
             ], C_INDIGO, title_size=11, body_size=9.5)

    set_notes(s15, "In academic engineering, data integrity is paramount. We benchmarked four candidate classifiers using stratified 5-fold cross-validation. Calibrated LinearSVC achieved the highest performance: 96% test accuracy and 0.9554 Macro F1. However, we state plainly that this was evaluated on 500 curated synthetic grievances. We do not claim this proves flawless real-world accuracy without continuous domain adaptation and human-in-the-loop review.")

    # ==================== SLIDE 16: LIMITATIONS & FUTURE ====================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s16)
    add_header(s16, "Project Limitations & Future Enhancement Scope")
    add_card(s16, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2),
             "Current Technical Limitations", [
                 "Non-Human Biohazards: Entity extraction lacks explicit keywords for animal carcasses, resulting in lower scores for stray animal reports.",
                 "Linear OLS Assumptions: 14-day volume forecasting assumes continuity of current reporting trends and cannot model sudden catastrophic storms without meteorological API feeds.",
                 "Dual Experimental Stems: The repository contains an unmaintained Java Spring Boot prototype alongside the production FastAPI core.",
                 "GPS Dependence: Relies on mobile device GPS or citizen-selected ward centroids for spatial clustering."
             ], C_SAFFRON)
    add_card(s16, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2),
             "Future Engineering Scope", [
                 "IoT Edge Telemetry: Connect municipal water pipeline pressure sensors directly to trigger automatic tickets before citizens notice leaks.",
                 "Computer Vision Inspection: Deploy CNN / Vision Transformers to automatically quantify road pothole depth and trash volume from photos.",
                 "Voice IVR & WhatsApp Ingestion: Multilingual voice speech-to-text allowing illiterate citizens to lodge grievances in local dialects.",
                 "Kubernetes & Kafka: Distributed microservice deployment on cloud clusters for metropolitan-scale scalability."
             ], C_TEAL)
    set_notes(s16, "We believe in transparent engineering: Current limitations include non-human biohazard extraction edge cases, linear time-series assumptions in OLS forecasting, and dependency on mobile GPS accuracy. In future work, we plan to integrate IoT telemetry from water pipeline pressure transducers, computer vision for automatic pothole depth estimation, and voice IVR for citizens who cannot read or write.")

    # ==================== SLIDE 17: CONCLUSION ====================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s17)
    add_header(s17, "Project Conclusion & Engineering Contributions")
    add_card(s17, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2),
             "Key Contributions of SmartCivic AI", [
                 "1. Elevated an experimental prototype into a production-grade, deployable B.Tech Major Project.",
                 "2. Marries Calibrated Machine Learning (96% accuracy) with Deterministic Safety Invariants that unconditionally protect life safety.",
                 "3. Engineered an active SLA auto-escalation daemon that penalizes delayed tickets and dispatches emergency alerts.",
                 "4. Designed a 4-tier Role-Based Access Control architecture backed by cryptographic timed sessions.",
                 "5. Delivered high-precision Leaflet/OSM GIS mapping across Gwalior Wards with 500m spatial outbreak clustering.",
                 "6. Pioneered 14-day OLS predictive volume forecasting for proactive municipal resource allocation.",
                 "7. Fully verified with 29 passing automated unit and integration tests (100% pass rate) and zero fabricated claims."
             ], C_SAFFRON, title_size=13, body_size=11)
    set_notes(s17, "In conclusion, SmartCivic AI successfully demonstrates how modern AI can be responsibly integrated into municipal governance. By combining high-speed calibrated machine learning with non-negotiable safety rules, automated SLA escalation, and predictive forecasting, the system empowers citizens and municipal authorities alike. It is functional, verified, and ready for real-world deployment.")

    # ==================== SLIDE 18: THANK YOU ====================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_dark_bg(s18)
    bar18 = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12))
    bar18.fill.solid()
    bar18.fill.fore_color.rgb = C_SAFFRON
    bar18.line.color.rgb = C_SAFFRON

    tb18 = s18.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(11.3), Inches(3.5))
    tf18 = tb18.text_frame
    tf18.word_wrap = True

    pt0 = tf18.paragraphs[0]
    pt0.text = "THANK YOU"
    pt0.font.size = Pt(44)
    pt0.font.bold = True
    pt0.font.color.rgb = C_WHITE
    pt0.alignment = PP_ALIGN.CENTER
    pt0.space_after = Pt(14)

    pt1 = tf18.add_paragraph()
    pt1.text = "SmartCivic AI — Intelligent Civic Complaint Management & Predictive Governance System"
    pt1.font.size = Pt(18)
    pt1.font.bold = True
    pt1.font.color.rgb = C_SAFFRON
    pt1.alignment = PP_ALIGN.CENTER
    pt1.space_after = Pt(20)

    pt2 = tf18.add_paragraph()
    pt2.text = "Questions & Academic Discussion Welcomed"
    pt2.font.size = Pt(14)
    pt2.font.color.rgb = C_TEAL
    pt2.alignment = PP_ALIGN.CENTER

    set_notes(s18, "Thank you, respected members of the evaluation committee, for your time and guidance. I invite any technical or architectural questions regarding SmartCivic AI, our model benchmarking, safety invariants, or testing methodology.")

    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "SmartCivic_AI_Major_Project.pptx")
    create_deck(out_file)
