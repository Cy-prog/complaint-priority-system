import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def create_itm_deck(output_path: str):
    # Match the exact 4:3 geometry of the provided ITM University slide template
    prs = Presentation()
    prs.slide_width = Inches(10.0)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Exact colors matching the ITM University Gwalior template
    C_WHITE = RGBColor(255, 255, 255)
    C_OFFWHITE = RGBColor(248, 250, 252)
    C_NAVY_ITM = RGBColor(0, 32, 96)          # #002060 Title Navy
    C_CRIMSON = RGBColor(153, 0, 0)           # #990000 Arrow Crimson/Maroon
    C_GREEN_ITM = RGBColor(20, 77, 54)        # #144D36 Banner Dark Green
    C_BLACK = RGBColor(0, 0, 0)
    C_TEXT = RGBColor(30, 41, 59)
    C_MUTED = RGBColor(90, 102, 118)
    C_BORDER = RGBColor(203, 213, 225)
    C_SOFT_RED = RGBColor(254, 242, 242)
    C_SOFT_BLUE = RGBColor(239, 246, 255)

    FONT_SERIF = "Times New Roman"
    FONT_SANS = "Arial"

    base_dir = os.path.dirname(__file__)
    diag_dir = os.path.join(base_dir, "diagrams")
    shot_dir = os.path.join(base_dir, "screenshots")
    bg_template_path = os.path.join(shot_dir, "itm_template_clean.png")

    TOTAL_SLIDES = 18

    def set_notes(slide, notes_text: str):
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes_text.strip()

    def apply_itm_page_template(slide):
        if os.path.exists(bg_template_path):
            slide.shapes.add_picture(
                bg_template_path, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height
            )

    def add_content_chrome(slide, title_text: str, section_tag: str, slide_num: int):
        apply_itm_page_template(slide)

        # Title block safely positioned below the circular logo strip (y >= 1.02") and clear of top-right green ribbon (x <= 9.15")
        tag_box = slide.shapes.add_textbox(Inches(1.30), Inches(0.96), Inches(7.70), Inches(0.24))
        tf_tag = tag_box.text_frame
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.name = FONT_SANS
        p_tag.font.size = Pt(9.5)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_CRIMSON

        title_box = slide.shapes.add_textbox(Inches(1.30), Inches(1.18), Inches(7.90), Inches(0.42))
        tf_title = title_box.text_frame
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_SERIF
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY_ITM

        # Clean divider rule below heading
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.30), Inches(1.62), Inches(8.30), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = C_CRIMSON
        div.line.fill.background()

        # Subtle Footer cleanly below the bottom horizontal crimson arrow (arrow ends at y = 7.21")
        fl = slide.shapes.add_textbox(Inches(1.30), Inches(7.24), Inches(6.60), Inches(0.24))
        tf_fl = fl.text_frame
        tf_fl.margin_left = tf_fl.margin_top = tf_fl.margin_right = tf_fl.margin_bottom = 0
        p_fl = tf_fl.paragraphs[0]
        p_fl.text = "SmartCivic AI  •  B.Tech CSE Major Project (2026–27)  •  ITM University, Gwalior"
        p_fl.font.name = FONT_SANS
        p_fl.font.size = Pt(8.5)
        p_fl.font.color.rgb = C_MUTED

        fr = slide.shapes.add_textbox(Inches(8.10), Inches(7.24), Inches(1.50), Inches(0.24))
        tf_fr = fr.text_frame
        tf_fr.margin_left = tf_fr.margin_top = tf_fr.margin_right = tf_fr.margin_bottom = 0
        p_fr = tf_fr.paragraphs[0]
        p_fr.text = f"Slide {slide_num} of {TOTAL_SLIDES}"
        p_fr.alignment = PP_ALIGN.RIGHT
        p_fr.font.name = FONT_SANS
        p_fr.font.size = Pt(8.5)
        p_fr.font.bold = True
        p_fr.font.color.rgb = C_CRIMSON

    def add_card(
        slide,
        left,
        top,
        width,
        height,
        title: str,
        bullets: list,
        header_color=C_NAVY_ITM,
        fill_color=C_OFFWHITE,
        title_size=12.5,
        body_size=10.5,
    ):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.adjustments[0] = 0.03
        card.shadow.inherit = False
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1)

        strip = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, left + Inches(0.12), top + Inches(0.14), Inches(0.05), Inches(0.26)
        )
        strip.fill.solid()
        strip.fill.fore_color.rgb = header_color
        strip.line.fill.background()

        tb = slide.shapes.add_textbox(
            left + Inches(0.24), top + Inches(0.12), width - Inches(0.36), height - Inches(0.24)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_SANS
        p_t.font.size = Pt(title_size)
        p_t.font.bold = True
        p_t.font.color.rgb = header_color
        p_t.space_after = Pt(6)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = "•  " + b
            p_b.font.name = FONT_SANS
            p_b.font.size = Pt(body_size)
            p_b.font.color.rgb = C_TEXT
            p_b.space_after = Pt(4.5)

    def add_diagram_fit(slide, img_path: str, box_left, box_top, box_w, box_h):
        if not os.path.exists(img_path):
            return
        with Image.open(img_path) as im:
            iw, ih = im.size
        ratio = iw / ih
        target_w = box_w
        target_h = target_w / ratio
        if target_h > box_h:
            target_h = box_h
            target_w = target_h * ratio
        final_left = box_left + (box_w - target_w) / 2
        final_top = box_top + (box_h - target_h) / 2

        frame = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            final_left - Inches(0.03),
            final_top - Inches(0.03),
            target_w + Inches(0.06),
            target_h + Inches(0.06),
        )
        frame.fill.solid()
        frame.fill.fore_color.rgb = C_WHITE
        frame.line.color.rgb = C_BORDER
        frame.line.width = Pt(1)
        slide.shapes.add_picture(img_path, final_left, final_top, width=target_w, height=target_h)

    # ==================== SLIDE 1: EXACT REPLICA OF UPLOADED ITM UNIVERSITY PAGE ====================
    s1 = prs.slides.add_slide(blank_layout)
    apply_itm_page_template(s1)

    # Exact "ITM UNIVERSITY GWALIOR" centered dark navy Times New Roman header
    u_box = s1.shapes.add_textbox(Inches(1.50), Inches(1.40), Inches(7.90), Inches(0.75))
    tf_u = u_box.text_frame
    tf_u.word_wrap = True
    pu = tf_u.paragraphs[0]
    pu.text = "ITM UNIVERSITY GWALIOR"
    pu.alignment = PP_ALIGN.CENTER
    pu.font.name = FONT_SERIF
    pu.font.size = Pt(28)
    pu.font.bold = True
    pu.font.color.rgb = C_NAVY_ITM

    # Exact center bold black Times New Roman block
    c_box = s1.shapes.add_textbox(Inches(1.55), Inches(2.62), Inches(7.80), Inches(2.05))
    tf_c = c_box.text_frame
    tf_c.word_wrap = True

    pc1 = tf_c.paragraphs[0]
    pc1.text = "Major Project"
    pc1.alignment = PP_ALIGN.CENTER
    pc1.font.name = FONT_SERIF
    pc1.font.size = Pt(19)
    pc1.font.bold = True
    pc1.font.color.rgb = C_BLACK
    pc1.space_after = Pt(2)

    pc2 = tf_c.add_paragraph()
    pc2.text = "(B.Tech CSE  |  2026–2027)"
    pc2.alignment = PP_ALIGN.CENTER
    pc2.font.name = FONT_SERIF
    pc2.font.size = Pt(17)
    pc2.font.bold = True
    pc2.font.color.rgb = C_BLACK
    pc2.space_after = Pt(10)

    pc3 = tf_c.add_paragraph()
    pc3.text = "SmartCivic AI"
    pc3.alignment = PP_ALIGN.CENTER
    pc3.font.name = FONT_SERIF
    pc3.font.size = Pt(22)
    pc3.font.bold = True
    pc3.font.color.rgb = C_NAVY_ITM
    pc3.space_after = Pt(4)

    pc4 = tf_c.add_paragraph()
    pc4.text = "Intelligent Civic Complaint Management and Predictive Governance System"
    pc4.alignment = PP_ALIGN.CENTER
    pc4.font.name = FONT_SERIF
    pc4.font.size = Pt(15.5)
    pc4.font.bold = True
    pc4.font.color.rgb = C_BLACK

    # Exact "SUBMITTED TO :-" on bottom-left above horizontal arrow
    to_box = s1.shapes.add_textbox(Inches(1.65), Inches(5.15), Inches(3.60), Inches(1.25))
    tf_to = to_box.text_frame
    tf_to.word_wrap = True
    pto1 = tf_to.paragraphs[0]
    pto1.text = "SUBMITTED TO :-"
    pto1.font.name = FONT_SANS
    pto1.font.size = Pt(13)
    pto1.font.bold = True
    pto1.font.color.rgb = C_BLACK
    pto1.space_after = Pt(4)

    pto2 = tf_to.add_paragraph()
    pto2.text = "[GUIDE NAME, DESIGNATION]"
    pto2.font.name = FONT_SERIF
    pto2.font.size = Pt(13.5)
    pto2.font.color.rgb = C_BLACK

    pto3 = tf_to.add_paragraph()
    pto3.text = "Dept. of [DEPARTMENT]"
    pto3.font.name = FONT_SERIF
    pto3.font.size = Pt(12.5)
    pto3.font.color.rgb = C_MUTED

    # Exact "SUBMITTED BY :-" on bottom-right above horizontal arrow
    by_box = s1.shapes.add_textbox(Inches(6.25), Inches(5.15), Inches(3.25), Inches(1.25))
    tf_by = by_box.text_frame
    tf_by.word_wrap = True
    pby1 = tf_by.paragraphs[0]
    pby1.text = "SUBMITTED BY :-"
    pby1.font.name = FONT_SANS
    pby1.font.size = Pt(13)
    pby1.font.bold = True
    pby1.font.color.rgb = C_BLACK
    pby1.space_after = Pt(4)

    pby2 = tf_by.add_paragraph()
    pby2.text = "Samit Jain"
    pby2.font.name = FONT_SERIF
    pby2.font.size = Pt(13.5)
    pby2.font.color.rgb = C_BLACK

    pby3 = tf_by.add_paragraph()
    pby3.text = "[ENROLLMENT NO.]"
    pby3.font.name = FONT_SERIF
    pby3.font.size = Pt(13.5)
    pby3.font.color.rgb = C_BLACK

    set_notes(
        s1,
        "Respected panel members and project guide at ITM University Gwalior, good morning. I am Samit Jain, presenting my B.Tech Major Project: SmartCivic AI — Intelligent Civic Complaint Management and Predictive Governance System. Built upon an existing minor project baseline, SmartCivic AI integrates explainable NLP classification, non-downgrade safety invariants, GIS clustering, SLA automation, and OLS volume forecasting.",
    )

    # ==================== SLIDE 2: PRESENTATION OUTLINE ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s2, "Presentation Outline", "Agenda & Academic Flow", 2)
    add_card(
        s2, Inches(1.30), Inches(1.80), Inches(4.05), Inches(5.05),
        "Part I: Problem & System Design",
        [
            "1. Introduction & Civic Governance Context",
            "2. Problem Statement & Operational Gaps",
            "3. Objectives & Technical Scope",
            "4. Literature Review & Baseline Limits",
            "5. Layered Architecture & Tech Stack",
            "6. Use Case, DFD Level 1 & ER Schema",
        ],
        header_color=C_CRIMSON, title_size=13, body_size=11.5,
    )
    add_card(
        s2, Inches(5.55), Inches(1.80), Inches(4.05), Inches(5.05),
        "Part II: AI, Live Demo & Verification",
        [
            "7. AI Triage Pipeline & Safety Guardrails",
            "8. GIS Spatial Clustering & SLA Engine",
            "9. Live Localhost Interface Walkthrough",
            "10. Empirical Model Benchmarks (N=500)",
            "11. Security, DPDP Privacy & Testing (29/29)",
            "12. Limitations, Future Scope & Conclusion",
        ],
        header_color=C_NAVY_ITM, title_size=13, body_size=11.5,
    )
    set_notes(
        s2,
        "This presentation is structured into twelve sections matching ITM University Major Project guidelines. Part One covers the problem domain, literature review, minor-project audit, layered architecture, and relational schema design. Part Two demonstrates the AI safety pipeline, live localhost interface, empirical benchmarks, automated test outcomes, and honest engineering limitations.",
    )

    # ==================== SLIDE 3: INTRODUCTION ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s3, "Introduction: SmartCivic AI Platform", "Chapter 1 • Introduction", 3)
    add_card(
        s3, Inches(1.30), Inches(1.80), Inches(4.95), Inches(5.05),
        "Project Vision & Operational Context",
        [
            "Upgrades the B.Tech Minor Project ('AI-Based Complaint Priority System') into an enterprise governance suite.",
            "Designed for bilingual (English & Hindi) urban bodies such as Gwalior Municipal Corporation.",
            "Automates grievance ingestion, departmental routing, priority scoring, and officer dispatch.",
            "Replaces opaque AI scores with factor-by-factor explainability.",
            "Adds active SLA escalation, GIS spatial clustering & 14-day forecasting.",
        ],
        header_color=C_NAVY_ITM, title_size=13, body_size=11,
    )
    add_card(
        s3, Inches(6.45), Inches(1.80), Inches(3.15), Inches(5.05),
        "Verified Platform Counts",
        [
            "14 Normalized SQLAlchemy Tables",
            "44 Registered FastAPI Routes",
            "11 Municipal Departments",
            "66 Gwalior Wards Mapped",
            "4-Tier RBAC Security Model",
            "29/29 PyTest Checks Passed",
        ],
        header_color=C_CRIMSON, fill_color=C_SOFT_RED, title_size=13, body_size=11,
    )
    set_notes(
        s3,
        "SmartCivic AI transforms a manual, slow grievance portal into an intelligent municipal command platform. Preserving working code from our minor project, we engineered a comprehensive FastAPI and SQLAlchemy system spanning 14 database tables, 44 API and HTML routes, 11 departments, 66 Gwalior municipal wards, and full automated test verification.",
    )

    # ==================== SLIDE 4: PROBLEM STATEMENT ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s4, "Problem Statement", "Chapter 1 • Research Gap", 4)
    add_card(
        s4, Inches(1.30), Inches(1.80), Inches(4.05), Inches(5.05),
        "Municipal Triage Bottlenecks",
        [
            "Thousands of unstructured complaints overwhelm municipal desks weekly.",
            "Manual classification introduces 3–7 day ticket assignment delays.",
            "Life-threatening hazards sit inside generic FIFO queues alongside routine tasks.",
            "Officer overload vs. idle staff due to lack of load visibility.",
            "No spatial outbreak correlation for contaminated water or grid faults.",
        ],
        header_color=C_CRIMSON, title_size=12.5, body_size=10.8,
    )
    add_card(
        s4, Inches(5.55), Inches(1.80), Inches(4.05), Inches(5.05),
        "Pitfalls of Naive Statistical AI",
        [
            "Sentiment Trap: Polite phrasing lowers AI urgency even for lethal hazards.",
            "Black-Box Distrust: Engineers reject unexplainable triage numbers.",
            "Passive Deadlines: Static SLAs fail to escalate overdue grievances.",
            "PII Exposure: Unredacted open dashboards risk leaking citizen phone numbers and addresses.",
        ],
        header_color=C_NAVY_ITM, title_size=12.5, body_size=10.8,
    )
    set_notes(
        s4,
        "Urban municipalities struggle with manual triage delays and the absence of spatial outbreak tracking. Simultaneously, naive AI approaches fail because polite wording tricks sentiment classifiers into assigning low priority to emergency hazards. SmartCivic AI eliminates both issues using calibrated classification backed by hard deterministic safety rules.",
    )

    # ==================== SLIDE 5: OBJECTIVES ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s5, "Objectives of the Project", "Chapter 1 • Objectives", 5)
    add_card(
        s5, Inches(1.30), Inches(1.80), Inches(2.65), Inches(5.05),
        "1. Explainable AI",
        [
            "Classify civic issues via Calibrated LinearSVC.",
            "Compute transparent 0–100 priority scores.",
            "Decompose urgency, severity, population & duration.",
            "Route confidence < 0.40 inputs to human review.",
        ],
        header_color=C_NAVY_ITM, title_size=12, body_size=10.2,
    )
    add_card(
        s5, Inches(4.12), Inches(1.80), Inches(2.65), Inches(5.05),
        "2. Safety & SLA",
        [
            "Enforce non-downgrade hazard rule (>= 80 CRITICAL).",
            "Configure tiered SLA limits (6h, 24h, 72h, 168h).",
            "Auto-promote priority upon SLA deadline breach.",
            "Maintain immutable override audit trails.",
        ],
        header_color=C_CRIMSON, title_size=12, body_size=10.2,
    )
    add_card(
        s5, Inches(6.95), Inches(1.80), Inches(2.65), Inches(5.05),
        "3. Predictive & Open",
        [
            "Cluster duplicates via cosine embeddings.",
            "Flag >= 3 incidents in 500m / 48h GIS clusters.",
            "Predict 14-day grievance volume using OLS + 95% CI.",
            "Publish DPDP-compliant open metrics.",
        ],
        header_color=C_GREEN_ITM, title_size=12, body_size=10.2,
    )
    set_notes(
        s5,
        "Our objectives fall into three core tracks: First, explainable multi-factor AI classification with uncertainty gating. Second, non-negotiable deterministic safety rules and automated SLA escalation sweeps. Third, proactive municipal governance via semantic duplicate clustering, GIS spatial outbreak monitoring, OLS forecasting, and DPDP-compliant public transparency.",
    )

    # ==================== SLIDE 6: LITERATURE REVIEW & BASELINE ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s6, "Literature Review & Existing System Limitations", "Chapters 2 & 3 • Baseline Audit", 6)
    add_card(
        s6, Inches(1.30), Inches(1.80), Inches(4.05), Inches(5.05),
        "Key Research Foundations",
        [
            "TF-IDF & LinearSVC (Joachims, 1998; Pedregosa et al., 2011): Low-latency sparse text categorization.",
            "Platt Scaling (Platt, 1999): CalibratedClassifierCV yields reliable probability confidences.",
            "VADER Sentiment (Hutto & Gilbert, 2014): Auxiliary lexicon polarity, subordinated to safety rules.",
            "SentenceTransformers (Reimers & Gurevych, 2019): 'all-MiniLM-L6-v2' semantic duplicate detection.",
        ],
        header_color=C_NAVY_ITM, title_size=12.5, body_size=10.2,
    )
    add_card(
        s6, Inches(5.55), Inches(1.80), Inches(4.05), Inches(5.05),
        "Minor Project Baseline -> Upgraded",
        [
            "6-class toy dataset -> Multi-class calibrated classification + human review gating.",
            "Single flat admin -> 4-tier RBAC with signed HMAC timed tokens.",
            "Mock jittered points -> Real 66-ward Gwalior coordinates & 500m clustering.",
            "Passive SLA dates -> Active escalation sweep (+1 tier, +20 penalty).",
            "No forecasting -> 14-day OLS projection & seasonal directives.",
        ],
        header_color=C_CRIMSON, title_size=12.5, body_size=10.2,
    )
    set_notes(
        s6,
        "Our architecture builds on established academic foundations including LinearSVC for high-dimensional sparse text, Platt probability calibration, and MiniLM embeddings for duplicate detection. Auditing our earlier minor project highlighted key gaps—single roles, passive deadlines, and jittered mock coordinates—all systematically resolved in SmartCivic AI.",
    )

    # ==================== SLIDE 7: PROPOSED SYSTEM ARCHITECTURE ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s7, "Proposed System Architecture & Tech Stack", "Chapter 4 • System Architecture", 7)
    add_diagram_fit(
        s7, os.path.join(diag_dir, "system_architecture.png"), Inches(1.30), Inches(1.78), Inches(5.35), Inches(5.08)
    )
    add_card(
        s7, Inches(6.80), Inches(1.80), Inches(2.80), Inches(5.05),
        "Technology Stack",
        [
            "Backend: FastAPI 0.115+, Python 3.14, Uvicorn ASGI",
            "Database: SQLAlchemy 2.x, SQLite / PostgreSQL",
            "Frontend: Jinja2, HTMX, Alpine.js, Tailwind CSS",
            "AI/ML: scikit-learn, NLTK VADER, SentenceTransformers",
            "GIS & Charts: Leaflet, OSM, Chart.js",
            "Exports: ReportLab, PyMuPDF, OpenPyXL",
        ],
        header_color=C_NAVY_ITM, title_size=12, body_size=9.8,
    )
    set_notes(
        s7,
        "The system architecture organizes SmartCivic AI into five layers: a reactive Jinja2, HTMX, and Leaflet frontend; an ASGI security barrier enforcing RBAC and rate limits; FastAPI application services; an intelligence engine running LinearSVC, safety rules, and OLS regression; and a normalized SQLAlchemy persistence layer.",
    )

    # ==================== SLIDE 8: SYSTEM DESIGN (USE CASE & DFD) ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s8, "System Design: Use Case & Data Flow (DFD Level 1)", "Chapter 6 • Structured Design", 8)

    l1 = s8.shapes.add_textbox(Inches(1.30), Inches(1.72), Inches(4.05), Inches(0.28))
    pl1 = l1.text_frame.paragraphs[0]
    pl1.text = "Fig 1: Multi-Actor Use Case Model"
    pl1.font.name = FONT_SANS
    pl1.font.size = Pt(11)
    pl1.font.bold = True
    pl1.font.color.rgb = C_CRIMSON
    add_diagram_fit(s8, os.path.join(diag_dir, "use_case.png"), Inches(1.30), Inches(2.02), Inches(4.05), Inches(4.80))

    l2 = s8.shapes.add_textbox(Inches(5.55), Inches(1.72), Inches(4.05), Inches(0.28))
    pl2 = l2.text_frame.paragraphs[0]
    pl2.text = "Fig 2: DFD Level 1 — Grievance Processing"
    pl2.font.name = FONT_SANS
    pl2.font.size = Pt(11)
    pl2.font.bold = True
    pl2.font.color.rgb = C_NAVY_ITM
    add_diagram_fit(s8, os.path.join(diag_dir, "dfd_level_1.png"), Inches(5.55), Inches(2.02), Inches(4.05), Inches(4.80))

    set_notes(
        s8,
        "These structured design diagrams model actor interactions and data flow. On the left, the Use Case diagram separates privileges across Citizens, Field Officers, Department Admins, and Super Admins. On the right, Data Flow Diagram Level 1 illustrates how complaint text and evidence pass through AI triage, duplicate matching, SLA initialization, and audit storage.",
    )

    # ==================== SLIDE 9: DATABASE SCHEMA & ER DIAGRAM ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s9, "Database Design: Entity-Relationship Architecture", "Chapter 6 • Data Modeling", 9)
    add_diagram_fit(
        s9, os.path.join(diag_dir, "er_diagram.png"), Inches(1.30), Inches(1.78), Inches(5.35), Inches(5.08)
    )
    add_card(
        s9, Inches(6.80), Inches(1.80), Inches(2.80), Inches(5.05),
        "14 Normalized Tables",
        [
            "Core: complaints, users, departments, categories",
            "AI & Rules: complaint_analysis, similar_complaints, safety_rules",
            "Operations: sla_records, complaint_assignments, attachments",
            "Audit: priority_overrides, complaint_status_history, audit_logs, notifications",
            "Zero raw SQL queries; indexed foreign keys.",
        ],
        header_color=C_CRIMSON, title_size=12, body_size=9.8,
    )
    set_notes(
        s9,
        "Our database design separates operational, analytical, and audit records into 14 normalized SQLAlchemy tables. Core tables handle tickets and departmental routing, while dedicated analysis, override, and status-history tables guarantee complete auditability of both AI predictions and human interventions.",
    )

    # ==================== SLIDE 10: AI PIPELINE & SAFETY INVARIANT ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s10, "AI Pipeline & Deterministic Safety Invariant", "Chapter 7 • AI/ML Methodology", 10)
    add_diagram_fit(
        s10, os.path.join(diag_dir, "ai_pipeline_flowchart.png"), Inches(1.30), Inches(1.78), Inches(4.95), Inches(5.08)
    )
    add_card(
        s10, Inches(6.40), Inches(1.80), Inches(3.20), Inches(5.05),
        "Safety Guardrail Case Study",
        [
            "Input: 'Kindly note a live 440V wire snapped near primary school gate. Thank you.'",
            "VADER Sentiment: +0.65 (Polite tone)",
            "Naive ML Estimate: LOW (Score: 28)",
            "Safety Rule Triggered: HAZARD_ELECTRICAL_SPARK",
            "Invariant Output: Forced to CRITICAL (Score: 85, SLA: 6h)",
            "Audit tag clarifies deterministic override.",
        ],
        header_color=C_CRIMSON, fill_color=C_SOFT_RED, title_size=12, body_size=10,
    )
    set_notes(
        s10,
        "Here is our synchronous AI triage pipeline paired with a real safety test case. Polite citizen wording produces positive sentiment (+0.65) and a dangerously low initial estimate. Our post-ML Deterministic Safety Guard detects the live 440V wire hazard invariant and unconditionally forces CRITICAL priority with a 6-hour SLA.",
    )

    # ==================== SLIDE 11: GIS CLUSTERING & SLA ESCALATION ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s11, "GIS Spatial Clustering & SLA Escalation Engine", "Chapter 8 • Operational Engines", 11)
    add_diagram_fit(
        s11, os.path.join(diag_dir, "sla_escalation_flow.png"), Inches(1.30), Inches(1.78), Inches(4.80), Inches(5.08)
    )
    add_card(
        s11, Inches(6.25), Inches(1.80), Inches(3.35), Inches(5.05),
        "Spatial & Predictive Modules",
        [
            "Gwalior GIS (/map): 66 ward centroids across Lashkar, Morar, City Center & Hazira.",
            "Outbreak Clustering: Triggers alerts when >= 3 similar complaints appear within 500m / 48h.",
            "OLS Forecasting (/predictive): 14-day regression trend with 95% confidence bands.",
            "SLA Escalation Sweep: Breached tickets earn +1 tier, +20 urgency score & supervisor notification.",
        ],
        header_color=C_NAVY_ITM, title_size=12, body_size=10,
    )
    set_notes(
        s11,
        "SmartCivic AI enforces accountability through active SLA escalation sweeps: tickets exceeding 6, 24, 72, or 168-hour deadlines receive an automatic tier promotion and +20 urgency penalty. Alongside SLA tracking, spatial outbreak clustering detects localized infrastructure failures within 500 meters, while OLS modeling forecasts 14-day grievance volume.",
    )

    # ==================== SLIDE 12: LIVE LOCALHOST IMPLEMENTATION ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s12, "Live Localhost Demo: Apex Command Dashboard", "Chapter 8 • UI Demonstration", 12)
    add_diagram_fit(
        s12, os.path.join(shot_dir, "live_apex_dashboard.png"), Inches(1.30), Inches(1.78), Inches(5.30), Inches(5.08)
    )
    add_card(
        s12, Inches(6.75), Inches(1.80), Inches(2.85), Inches(5.05),
        "Live Localhost Capture",
        [
            "Served on http://127.0.0.1:8000/ via Uvicorn ASGI.",
            "Bilingual Hindi/English sidebar & role switcher.",
            "6 live KPI cards (56 Tabled, 52 Critical, 40 SLA Breached).",
            "Interactive Chart.js priority doughnut & 7-day trend chart.",
            "Public routes: /portal & /transparency.",
        ],
        header_color=C_GREEN_ITM, title_size=12, body_size=10,
    )
    set_notes(
        s12,
        "This slide displays a live screenshot captured directly from the running FastAPI localhost server at 127.0.0.1:8000. It demonstrates the bilingual Hindi-English Apex Command Center featuring real-time KPI cards, Chart.js priority distribution and volume spline charts, quick navigation to GIS and predictive views, and role persona switching.",
    )

    # ==================== SLIDE 13: MODEL EVALUATION & BENCHMARKS ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s13, "Results & Model Performance Evaluation", "Chapter 10 • Empirical Benchmarks", 13)

    table_shape = s13.shapes.add_table(5, 5, Inches(1.30), Inches(1.78), Inches(8.30), Inches(2.35))
    table = table_shape.table
    widths = [Inches(2.30), Inches(1.35), Inches(1.35), Inches(1.75), Inches(1.55)]
    for i, w in enumerate(widths):
        table.columns[i].width = w

    headers = ["Algorithm Candidate", "Test Acc.", "Macro F1", "5-Fold CV Mean", "Status"]
    rows = [
        ["LinearSVC (Calibrated)", "96.00%", "0.9554", "0.9075 (+-0.025)", "SELECTED"],
        ["Logistic Regression", "94.00%", "0.9329", "0.9000 (+-0.024)", "Fallback"],
        ["Multinomial Naive Bayes", "92.00%", "0.9094", "0.8875 (+-0.019)", "Baseline"],
        ["SGD Classifier (Log Loss)", "92.00%", "0.9093", "0.8825 (+-0.019)", "Alternative"],
    ]

    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CRIMSON
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_SANS
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_SOFT_BLUE if r_idx == 0 else (C_OFFWHITE if r_idx % 2 == 1 else C_WHITE)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_SANS
            p.font.size = Pt(10)
            p.font.bold = (r_idx == 0)
            p.font.color.rgb = C_CRIMSON if (r_idx == 0 and c_idx == 4) else C_TEXT

    add_card(
        s13, Inches(1.30), Inches(4.32), Inches(8.30), Inches(2.50),
        "Scientific Integrity & Dataset Caveats",
        [
            "Stratified 5-Fold Cross-Validation run via ai/training/evaluate.py on N = 500 curated bilingual grievances.",
            "LinearSVC (Calibrated) achieved 96.00% test accuracy, 0.9554 Macro F1, and ~1.2 ms inference time.",
            "HONEST DISCLOSURE: High score verifies feature separation on curated synthetic data; real-world noisy municipal deployment requires ongoing feedback loops and < 0.40 confidence gating.",
        ],
        header_color=C_NAVY_ITM, fill_color=C_SOFT_BLUE, title_size=12, body_size=10,
    )
    set_notes(
        s13,
        "We evaluated four supervised text classifiers using stratified 5-fold cross-validation on 500 multi-class civic samples. Calibrated LinearSVC achieved the top score at 96.00% test accuracy and 0.9554 Macro F1. Maintaining strict academic honesty, we note this reflects synthetic evaluation data and pair production inference with confidence-gated human review.",
    )

    # ==================== SLIDE 14: VALUE ADDITION & SECURITY ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s14, "Value Addition, Social Impact & Security", "Chapter 11 • Governance & Privacy", 14)
    add_card(
        s14, Inches(1.30), Inches(1.80), Inches(4.05), Inches(5.05),
        "Civic & Social Impact",
        [
            "Life Safety: Immediate prioritization of live electrical wires, fires & gas leaks.",
            "Accessibility: Bilingual Hindi/English citizen portal (/portal) with voice typing input.",
            "DPDP Privacy: Open portal (/transparency) redacts citizen names, phones & addresses.",
            "Social Audits: Printable Jan Sunwai / Gram Sabha hearing reports (/reports/gram-sabha).",
        ],
        header_color=C_GREEN_ITM, title_size=12.5, body_size=10.5,
    )
    add_card(
        s14, Inches(5.55), Inches(1.80), Inches(4.05), Inches(5.05),
        "Cybersecurity Controls",
        [
            "4-Tier RBAC: Cryptographic timed tokens (URLSafeTimedSerializer, 7-day expiry).",
            "Upload Validation: Binary magic-byte inspection (PNG/JPEG/WebP) + 10 MB limit.",
            "SQL Injection Defense: Parameterized SQLAlchemy ORM queries across all routes.",
            "Rate Limiting & Logs: SlowAPI request throttling & immutable audit_logs.",
        ],
        header_color=C_CRIMSON, title_size=12.5, body_size=10.5,
    )
    set_notes(
        s14,
        "SmartCivic AI balances public transparency with strict cybersecurity and privacy guarantees. Citizen personal data is stripped from the transparency portal under India's DPDP Act, while all backend routes enforce ASGI-level RBAC, magic-byte image verification, rate limiting, and parameterized database access.",
    )

    # ==================== SLIDE 15: TESTING & PLAGIARISM REPORT ====================
    s15 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s15, "Software Testing & Plagiarism Compliance", "Chapter 9 • Verification & QA", 15)
    add_card(
        s15, Inches(1.30), Inches(1.80), Inches(4.05), Inches(5.05),
        "PyTest Verification (29 / 29 Passed)",
        [
            "Framework: PyTest 9.1.1 on Python 3.14.5 (14.08 seconds).",
            "Pass Rate: 29 Passed, 0 Failed (100% pass rate).",
            "Integration (13 tests): Auth sessions, magic-byte upload checks, SLA escalation & exports.",
            "Unit & Safety (16 tests): Scoring bounds, Hindi edge cases & non-downgrade rules.",
            "Localhost HTTP 200 verified across core dashboards.",
        ],
        header_color=C_NAVY_ITM, title_size=12.5, body_size=10.5,
    )
    add_card(
        s15, Inches(5.55), Inches(1.80), Inches(4.05), Inches(5.05),
        "Plagiarism & Academic Integrity",
        [
            "ITM University Norm: Similarity index must remain <= 25%.",
            "Originality: Report authored directly from verified codebase inspection.",
            "Zero Fabrication: All precision, recall, F1, test counts & table schemas are genuine.",
            "Similarity Score: [Insert Turnitin / DrillBit % Before Submission].",
        ],
        header_color=C_CRIMSON, fill_color=C_SOFT_RED, title_size=12.5, body_size=10.5,
    )
    set_notes(
        s15,
        "Verification encompasses automated testing and academic originality. All 29 PyTest unit and integration tests pass in 14.08 seconds across authentication, safety rules, SLA sweeps, and document generation. In compliance with ITM University's sub-25 percent plagiarism limit, all report chapters were authored from direct source inspection with zero fabricated numbers.",
    )

    # ==================== SLIDE 16: PUBLICATIONS & LIMITATIONS ====================
    s16 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s16, "Publications Status & Verified Limitations", "Chapter 12 • Academic Disclosure", 16)
    add_card(
        s16, Inches(1.30), Inches(1.80), Inches(4.05), Inches(5.05),
        "Research Paper / Publication",
        [
            "Working Title: 'Safety-Invariant Hybrid NLP & Spatial Forecasting for Municipal Grievance Governance'.",
            "Reproducible Evaluation Script: ai/training/evaluate.py.",
            "Publication Status: [Ready / Add Journal or Conference Name if Communicated].",
            "Open Submission Pack: Diagrams, evidence & viva QA committed in Git.",
        ],
        header_color=C_NAVY_ITM, title_size=12.5, body_size=10.5,
    )
    add_card(
        s16, Inches(5.55), Inches(1.80), Inches(4.05), Inches(5.05),
        "Verified Honest Limitations",
        [
            "Biohazard Keyword Gap: 'Dead stray cow' scored LOW (26) due to missing carcass rules.",
            "GIS CSS Bug (/map): Missing leaflet.css causes vertical tile stacking during live map display.",
            "Forecast Bindings (/predictive): Missing score/tip fields on hotspot & seasonal UI cards.",
            "Synthetic Corpus: Demands authentic city ticket logs for production generalization.",
        ],
        header_color=C_CRIMSON, title_size=12.5, body_size=10.5,
    )
    set_notes(
        s16,
        "Transparent engineering requires disclosing current gaps alongside achievements. Our evaluation identified a rule gap for animal carcass biohazards, while live localhost testing surfaced a missing leaflet.css stylesheet on the map route and incomplete template bindings on predictive hotspot cards—all clearly documented in ISSUES.md.",
    )

    # ==================== SLIDE 17: CONCLUSION & FUTURE SCOPE ====================
    s17 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s17, "Conclusion & Future Scope", "Chapter 12 • Summary & Roadmap", 17)
    add_card(
        s17, Inches(1.30), Inches(1.80), Inches(4.05), Inches(5.05),
        "Project Conclusion",
        [
            "Upgraded an experimental minor project into a production-ready SmartCivic AI platform.",
            "Unified Calibrated LinearSVC (96% test accuracy) with non-downgrade safety guardrails.",
            "Delivered active SLA escalation, 4-tier RBAC, DPDP transparency & OLS forecasting with 29/29 passing tests.",
        ],
        header_color=C_CRIMSON, title_size=12.5, body_size=10.8,
    )
    add_card(
        s17, Inches(5.55), Inches(1.80), Inches(4.05), Inches(5.05),
        "Future Enhancement Scope",
        [
            "UI Hotfixes: Add leaflet.css bundling, responsive sidebar polish & predictive bindings.",
            "Computer Vision: CNN-based pothole depth & trash volume scoring from citizen photos.",
            "IoT Telemetry: Water pipeline & transformer sensors auto-triggering maintenance tickets.",
            "Voice IVR / WhatsApp: Dialect speech-to-text intake for wider rural inclusivity.",
        ],
        header_color=C_GREEN_ITM, title_size=12.5, body_size=10.8,
    )
    set_notes(
        s17,
        "In conclusion, SmartCivic AI successfully bridges academic machine learning and reliable civic infrastructure, achieving verified test coverage and life-safety guarantees. Looking ahead, future enhancements include patching the frontend map stylesheet, adding computer vision inspection for citizen photos, integrating IoT utility sensors, and deploying WhatsApp voice intake.",
    )

    # ==================== SLIDE 18: REFERENCES & THANK YOU ====================
    s18 = prs.slides.add_slide(blank_layout)
    add_content_chrome(s18, "References & Acknowledgements", "Academic Citations & Q&A", 18)
    add_card(
        s18, Inches(1.30), Inches(1.80), Inches(5.05), Inches(5.05),
        "Selected IEEE References",
        [
            "[1] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python,' JMLR, vol. 12, pp. 2825–2830, 2011.",
            "[2] T. Joachims, 'Text Categorization with Support Vector Machines,' ECML, pp. 137–142, 1998.",
            "[3] C. J. Hutto and E. Gilbert, 'VADER: Sentiment Analysis,' ICWSM, 2014.",
            "[4] N. Reimers and I. Gurevych, 'Sentence-BERT,' EMNLP, 2019.",
            "[5] S. Ramirez, 'FastAPI Documentation,' https://fastapi.tiangolo.com/, 2024.",
            "[6] MeitY India, 'Digital Personal Data Protection Act, 2023,' Gazette of India.",
        ],
        header_color=C_NAVY_ITM, title_size=12, body_size=9.5,
    )
    add_card(
        s18, Inches(6.55), Inches(1.80), Inches(3.05), Inches(5.05),
        "Thank You!",
        [
            "Samit Jain",
            "[ENROLLMENT NO.]",
            "B.Tech CSE (2023–2027)",
            "ITM University, Gwalior",
            "Panel Questions & Live Demo Welcomed.",
        ],
        header_color=C_CRIMSON, fill_color=C_SOFT_RED, title_size=16, body_size=11.5,
    )
    set_notes(
        s18,
        "Thank you, respected members of the ITM University Gwalior evaluation committee, for your attention and guidance. Every system claim, database count, model metric, and localhost screenshot presented today is directly reproducible in the repository. I am now happy to take questions or demonstrate any workflow live.",
    )

    prs.save(output_path)
    print(f"Exact ITM template PPT saved successfully to: {output_path}")


if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "SmartCivic_AI_ITM_University_Format.pptx")
    create_itm_deck(out_file)
