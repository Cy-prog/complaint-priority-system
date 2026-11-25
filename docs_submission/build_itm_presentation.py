import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def create_itm_deck(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ITM University Gwalior Academic Palette (White canvas, Maroon/Rust primary, Navy secondary, Gold accent)
    C_WHITE = RGBColor(255, 255, 255)
    C_OFFWHITE = RGBColor(248, 250, 252)     # #F8FAFC card fill
    C_MAROON = RGBColor(139, 30, 36)         # #8B1E24 ITM University Rust/Maroon
    C_NAVY = RGBColor(15, 41, 74)            # #0F294A Deep Academic Navy
    C_GOLD = RGBColor(200, 138, 30)          # #C88A1E Warm Gold Accent
    C_TEXT = RGBColor(30, 41, 59)            # #1E293B Dark Slate Body Text
    C_MUTED = RGBColor(100, 116, 139)        # #64748B Caption Text
    C_BORDER = RGBColor(203, 213, 225)       # #CBD5E1 Light Card Border
    C_TEAL = RGBColor(15, 118, 110)          # #0F766E Subtle Positive Indicator
    C_SOFT_MAROON = RGBColor(254, 242, 242)  # #FEF2F2 Highlight Tint
    C_SOFT_NAVY = RGBColor(239, 246, 255)    # #EFF6FF Info Tint

    FONT_FAMILY = "Arial"
    base_dir = os.path.dirname(__file__)
    diag_dir = os.path.join(base_dir, "diagrams")
    shot_dir = os.path.join(base_dir, "screenshots")

    TOTAL_SLIDES = 18

    def set_notes(slide, notes_text: str):
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = notes_text.strip()

    def add_master_chrome(slide, title_text: str, section_tag: str, slide_num: int):
        # Clean white background
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_WHITE
        bg.line.fill.background()

        # Top institutional dual-stripe (Maroon + Gold)
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.10))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_MAROON
        top_bar.line.fill.background()

        gold_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.10), prs.slide_width, Inches(0.035))
        gold_bar.fill.solid()
        gold_bar.fill.fore_color.rgb = C_GOLD
        gold_bar.line.fill.background()

        # Section Tag
        tag_box = slide.shapes.add_textbox(Inches(0.65), Inches(0.24), Inches(8.8), Inches(0.28))
        tf_tag = tag_box.text_frame
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = section_tag.upper()
        p_tag.font.name = FONT_FAMILY
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_MAROON

        # Slide Title (24pt Bold Navy per ITM guidelines)
        title_box = slide.shapes.add_textbox(Inches(0.65), Inches(0.48), Inches(9.2), Inches(0.55))
        tf_title = title_box.text_frame
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = FONT_FAMILY
        p_title.font.size = Pt(23)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY

        # Top-Right ITM University Institutional Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.05), Inches(0.26), Inches(2.65), Inches(0.68))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_MAROON
        badge.line.color.rgb = C_GOLD
        badge.line.width = Pt(1.5)
        tf_b = badge.text_frame
        tf_b.word_wrap = True
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        pb1 = tf_b.paragraphs[0]
        pb1.text = "ITM UNIVERSITY"
        pb1.alignment = PP_ALIGN.CENTER
        pb1.font.name = FONT_FAMILY
        pb1.font.size = Pt(11)
        pb1.font.bold = True
        pb1.font.color.rgb = C_WHITE
        pb2 = tf_b.add_paragraph()
        pb2.text = "GWALIOR (M.P.) • SOET"
        pb2.alignment = PP_ALIGN.CENTER
        pb2.font.name = FONT_FAMILY
        pb2.font.size = Pt(8.5)
        pb2.font.bold = True
        pb2.font.color.rgb = RGBColor(253, 230, 138)

        # Header divider rule
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(1.12), Inches(12.03), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = C_BORDER
        div.line.fill.background()

        # Footer divider rule
        f_div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.65), Inches(7.02), Inches(12.03), Inches(0.015))
        f_div.fill.solid()
        f_div.fill.fore_color.rgb = C_BORDER
        f_div.line.fill.background()

        # Footer Left
        fl = slide.shapes.add_textbox(Inches(0.65), Inches(7.08), Inches(4.2), Inches(0.3))
        p_fl = fl.text_frame.paragraphs[0]
        p_fl.text = "SmartCivic AI | B.Tech CSE Major Project (2026–27)"
        p_fl.font.name = FONT_FAMILY
        p_fl.font.size = Pt(9.5)
        p_fl.font.color.rgb = C_MUTED

        # Footer Center
        fc = slide.shapes.add_textbox(Inches(4.6), Inches(7.08), Inches(4.6), Inches(0.3))
        p_fc = fc.text_frame.paragraphs[0]
        p_fc.text = "Dept. of Computer Science & Engineering, ITM University Gwalior"
        p_fc.alignment = PP_ALIGN.CENTER
        p_fc.font.name = FONT_FAMILY
        p_fc.font.size = Pt(9.5)
        p_fc.font.color.rgb = C_NAVY
        p_fc.font.bold = True

        # Footer Right
        fr = slide.shapes.add_textbox(Inches(10.8), Inches(7.08), Inches(1.88), Inches(0.3))
        p_fr = fr.text_frame.paragraphs[0]
        p_fr.text = f"Slide {slide_num} of {TOTAL_SLIDES}"
        p_fr.alignment = PP_ALIGN.RIGHT
        p_fr.font.name = FONT_FAMILY
        p_fr.font.size = Pt(9.5)
        p_fr.font.bold = True
        p_fr.font.color.rgb = C_MAROON

    def add_card(
        slide,
        left,
        top,
        width,
        height,
        title: str,
        bullets: list,
        header_color=C_NAVY,
        fill_color=C_OFFWHITE,
        title_size=14,
        body_size=12.5,
    ):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = C_BORDER
        card.line.width = Pt(1)

        # Left accent strip inside card area
        strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.14), top + Inches(0.16), Inches(0.06), Inches(0.32))
        strip.fill.solid()
        strip.fill.fore_color.rgb = header_color
        strip.line.fill.background()

        tb = slide.shapes.add_textbox(left + Inches(0.28), top + Inches(0.14), width - Inches(0.46), height - Inches(0.28))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_FAMILY
        p_t.font.size = Pt(title_size)
        p_t.font.bold = True
        p_t.font.color.rgb = header_color
        p_t.space_after = Pt(8)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = "•  " + b
            p_b.font.name = FONT_FAMILY
            p_b.font.size = Pt(body_size)
            p_b.font.color.rgb = C_TEXT
            p_b.space_after = Pt(6)

    def add_diagram_fit(slide, img_path: str, box_left, box_top, box_w, box_h):
        if not os.path.exists(img_path):
            return
        from PIL import Image
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
        # Add subtle crisp border frame
        frame = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            final_left - Inches(0.04),
            final_top - Inches(0.04),
            target_w + Inches(0.08),
            target_h + Inches(0.08),
        )
        frame.fill.solid()
        frame.fill.fore_color.rgb = C_WHITE
        frame.line.color.rgb = C_BORDER
        frame.line.width = Pt(1)
        slide.shapes.add_picture(img_path, final_left, final_top, width=target_w, height=target_h)

    # ==================== SLIDE 1: OFFICIAL ITM UNIVERSITY TITLE SLIDE ====================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_WHITE
    bg1.line.fill.background()

    # Left vertical Maroon pillar + Gold trim
    left_pillar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.45), prs.slide_height)
    left_pillar.fill.solid()
    left_pillar.fill.fore_color.rgb = C_MAROON
    left_pillar.line.fill.background()

    left_gold = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.45), 0, Inches(0.08), prs.slide_height)
    left_gold.fill.solid()
    left_gold.fill.fore_color.rgb = C_GOLD
    left_gold.line.fill.background()

    # University Banner Header
    univ_box = s1.shapes.add_textbox(Inches(0.95), Inches(0.45), Inches(9.2), Inches(0.95))
    tf_u = univ_box.text_frame
    tf_u.word_wrap = True
    pu1 = tf_u.paragraphs[0]
    pu1.text = "ITM UNIVERSITY, GWALIOR (M.P.)"
    pu1.font.name = FONT_FAMILY
    pu1.font.size = Pt(22)
    pu1.font.bold = True
    pu1.font.color.rgb = C_MAROON

    pu2 = tf_u.add_paragraph()
    pu2.text = "SCHOOL OF ENGINEERING & TECHNOLOGY  •  DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING"
    pu2.font.name = FONT_FAMILY
    pu2.font.size = Pt(11)
    pu2.font.bold = True
    pu2.font.color.rgb = C_NAVY

    # Crest Placeholder Box (top-right)
    crest = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.55), Inches(0.40), Inches(2.25), Inches(1.05))
    crest.fill.solid()
    crest.fill.fore_color.rgb = C_OFFWHITE
    crest.line.color.rgb = C_MAROON
    crest.line.width = Pt(1.5)
    tf_cr = crest.text_frame
    tf_cr.word_wrap = True
    tf_cr.vertical_anchor = MSO_ANCHOR.MIDDLE
    pcr = tf_cr.paragraphs[0]
    pcr.text = "ITM UNIVERSITY\nGWALIOR\n[Insert Official Crest]"
    pcr.alignment = PP_ALIGN.CENTER
    pcr.font.name = FONT_FAMILY
    pcr.font.size = Pt(9.5)
    pcr.font.bold = True
    pcr.font.color.rgb = C_MAROON

    # Divider
    d1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.95), Inches(1.58), Inches(11.85), Inches(0.025))
    d1.fill.solid()
    d1.fill.fore_color.rgb = C_GOLD
    d1.line.fill.background()

    # Major Project Title Block
    title_area = s1.shapes.add_textbox(Inches(0.95), Inches(1.85), Inches(11.8), Inches(2.5))
    tf_t1 = title_area.text_frame
    tf_t1.word_wrap = True

    pt_label = tf_t1.paragraphs[0]
    pt_label.text = "MAJOR PROJECT PRESENTATION (ACADEMIC SESSION 2026–2027)"
    pt_label.font.name = FONT_FAMILY
    pt_label.font.size = Pt(12)
    pt_label.font.bold = True
    pt_label.font.color.rgb = C_MAROON
    pt_label.space_after = Pt(10)

    pt_main = tf_t1.add_paragraph()
    pt_main.text = "SmartCivic AI"
    pt_main.font.name = FONT_FAMILY
    pt_main.font.size = Pt(38)
    pt_main.font.bold = True
    pt_main.font.color.rgb = C_NAVY
    pt_main.space_after = Pt(6)

    pt_sub = tf_t1.add_paragraph()
    pt_sub.text = "Intelligent Civic Complaint Management and Predictive Governance System"
    pt_sub.font.name = FONT_FAMILY
    pt_sub.font.size = Pt(19)
    pt_sub.font.bold = True
    pt_sub.font.color.rgb = C_TEXT
    pt_sub.space_after = Pt(14)

    pt_ful = tf_t1.add_paragraph()
    pt_ful.text = "Submitted in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering"
    pt_ful.font.name = FONT_FAMILY
    pt_ful.font.size = Pt(12.5)
    pt_ful.font.italic = True
    pt_ful.font.color.rgb = C_MUTED

    # Student & Guide Metadata Cards
    add_card(
        s1, Inches(0.95), Inches(4.75), Inches(5.7), Inches(2.05),
        "Submitted By",
        [
            "Student Name: Samit Jain",
            "Enrollment No.: [ENROLLMENT NO.]",
            "Program: B.Tech CSE (Batch 2023–2027)",
            "Department: [DEPARTMENT]",
        ],
        header_color=C_MAROON, fill_color=C_OFFWHITE, title_size=13.5, body_size=12,
    )
    add_card(
        s1, Inches(6.95), Inches(4.75), Inches(5.85), Inches(2.05),
        "Under the Supervision Of",
        [
            "Project Guide: [GUIDE NAME, DESIGNATION]",
            "Institution: ITM University, Gwalior (M.P.)",
            "Project Domain: AI/ML Governance & Full-Stack Web",
            "Repository: Cy-prog/complaint-priority-system",
        ],
        header_color=C_NAVY, fill_color=C_OFFWHITE, title_size=13.5, body_size=12,
    )
    set_notes(s1, "Respected Chairperson, Guide, and members of the evaluation panel at ITM University Gwalior, good morning. I am Samit Jain, presenting my B.Tech CSE Major Project titled SmartCivic AI: Intelligent Civic Complaint Management and Predictive Governance System. Built upon an existing minor project baseline, this system introduces explainable AI triage, deterministic safety invariants, GIS clustering, SLA escalation, and time-series governance.")

    # ==================== SLIDE 2: PRESENTATION OUTLINE ====================
    s2 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s2, "Presentation Outline", "Agenda & Academic Flow", 2)
    add_card(
        s2, Inches(0.65), Inches(1.4), Inches(5.85), Inches(5.3),
        "Part I: Problem, Research & Architecture",
        [
            "1. Introduction & Civic Governance Context",
            "2. Problem Statement & Core Operational Gaps",
            "3. Objectives & Technical Scope",
            "4. Literature Review & Minor Project Limitations",
            "5. Proposed System Architecture & Methodology",
            "6. System Design (Use Case, DFD & ER Schema)",
        ],
        header_color=C_MAROON, body_size=14,
    )
    add_card(
        s2, Inches(6.83), Inches(1.4), Inches(5.85), Inches(5.3),
        "Part II: Implementation, Results & Verification",
        [
            "7. Core AI Pipeline & Safety Invariants",
            "8. GIS Spatial Intelligence & SLA Automation",
            "9. Live Localhost Interface Demonstration",
            "10. Model Benchmarks & Evaluation Metrics",
            "11. Security, DPDP Privacy, Testing & Plagiarism Check",
            "12. Publications, Limitations, Conclusion & Q&A",
        ],
        header_color=C_NAVY, body_size=14,
    )
    set_notes(s2, "Our presentation follows the standard ITM University Major Project structure across two parts. In Part One, we cover the municipal problem context, literature review, limitations of our earlier minor project, and the new system design including DFD and ER schemas. In Part Two, we demonstrate the live localhost interface, AI safety guarantees, empirical model benchmarks, and verification test outcomes.")

    # ==================== SLIDE 3: INTRODUCTION ====================
    s3 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s3, "Introduction: SmartCivic AI Platform", "Chapter 1 • Introduction", 3)
    add_card(
        s3, Inches(0.65), Inches(1.4), Inches(7.3), Inches(5.3),
        "Project Vision & Operational Domain",
        [
            "Upgrades the B.Tech Minor Project ('AI-Based Complaint Priority System') into an enterprise municipal platform.",
            "Designed for bilingual (English & Hindi) urban governance such as Gwalior Municipal Corporation workflows.",
            "Automates grievance ingestion, category routing, urgency quantification, and field dispatch.",
            "Replaces opaque black-box scoring with factor-by-factor explainable AI triage.",
            "Integrates proactive SLA enforcement, GIS spatial clustering, and 14-day forecasting.",
        ],
        header_color=C_NAVY, body_size=13.5,
    )
    add_card(
        s3, Inches(8.25), Inches(1.4), Inches(4.43), Inches(5.3),
        "Key Platform Metrics (Verified)",
        [
            "14 Normalized Database Tables",
            "44 Registered FastAPI Routes",
            "11 Municipal Departments Seeded",
            "66 Gwalior Wards Mapped",
            "4-Tier Role-Based Access Control",
            "29 Automated PyTest Checks (100% Pass)",
        ],
        header_color=C_MAROON, fill_color=C_SOFT_MAROON, body_size=13.5,
    )
    set_notes(s3, "SmartCivic AI bridges the gap between citizen grievance portals and predictive municipal administration. Preserving working foundations from our minor project, we engineered a comprehensive FastAPI and SQLAlchemy platform featuring 14 database tables, 44 API and page routes, bilingual English and Hindi citizen support across 66 Gwalior municipal wards, and full end-to-end automated testing.")

    # ==================== SLIDE 4: PROBLEM STATEMENT ====================
    s4 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s4, "Problem Statement", "Chapter 1 • Research Gap", 4)
    add_card(
        s4, Inches(0.65), Inches(1.4), Inches(5.85), Inches(5.3),
        "Manual Municipal Triage Failures",
        [
            "Thousands of unstructured citizen complaints overwhelm municipal helpdesks weekly.",
            "Manual classification causes 3–7 day delays before a ticket reaches the right engineer.",
            "Life-threatening emergencies sit idle beside routine sanitation requests in FIFO queues.",
            "Uneven workload distribution causes field officer burnout while others stay idle.",
            "Zero spatial outbreak detection delays response to contaminated water or grid failures.",
        ],
        header_color=C_MAROON, body_size=13,
    )
    add_card(
        s4, Inches(6.83), Inches(1.4), Inches(5.85), Inches(5.3),
        "Risks of Unconstrained Statistical AI",
        [
            "Sentiment Trap: Calm, polite wording lowers urgency score even for lethal electrical hazards.",
            "Black-Box Distrust: Municipal officers reject arbitrary AI scores lacking factor explanations.",
            "Passive SLAs: Static due dates fail to escalate tickets automatically upon deadline breach.",
            "Privacy Leaks: Unsanitized open dashboards risk exposing citizen PII (names, phone numbers).",
        ],
        header_color=C_NAVY, body_size=13,
    )
    set_notes(s4, "Municipalities face two compounding problems. First, manual routing introduces days of delay and lacks outbreak correlation. Second, naive machine learning models suffer from the sentiment trap—if a citizen calmly reports a snapped 440V wire near a school, sentiment polarity appears neutral or positive and lowers urgency. SmartCivic AI eliminates both risks through deterministic safety guards.")

    # ==================== SLIDE 5: OBJECTIVES ====================
    s5 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s5, "Objectives of the Project", "Chapter 1 • Objectives", 5)
    add_card(
        s5, Inches(0.65), Inches(1.4), Inches(3.8), Inches(5.3),
        "1. Explainable Classification",
        [
            "Classify civic complaints across 14 categories via Calibrated LinearSVC.",
            "Compute transparent multi-factor priority scores (0–100 scale).",
            "Decompose every score into Urgency, Severity, Population, Hazard & Duration.",
            "Gate low-confidence (< 0.40) inputs for human supervisor review.",
        ],
        header_color=C_NAVY, body_size=12.5,
    )
    add_card(
        s5, Inches(4.76), Inches(1.4), Inches(3.8), Inches(5.3),
        "2. Safety & SLA Enforcement",
        [
            "Enforce a non-downgrade safety invariant forcing hazards to CRITICAL (>= 80).",
            "Track priority-tiered SLA deadlines (6h, 24h, 72h, 168h).",
            "Run automated escalation sweeps promoting breached complaints.",
            "Log immutable audit trails for every AI and human override decision.",
        ],
        header_color=C_MAROON, body_size=12.5,
    )
    add_card(
        s5, Inches(8.88), Inches(1.4), Inches(3.8), Inches(5.3),
        "3. Spatial & Predictive Gov",
        [
            "Detect semantic duplicates via dense embeddings & cosine similarity.",
            "Identify GIS outbreaks (>= 3 complaints within 500m / 48 hours).",
            "Project 14-day grievance volume using OLS regression & 95% CI.",
            "Publish anonymized live metrics compliant with India's DPDP Act.",
        ],
        header_color=C_TEAL, body_size=12.5,
    )
    set_notes(s5, "Our project objectives span three engineering pillars. First, build an explainable classification and priority model with human-review gating. Second, guarantee life safety with non-downgrade deterministic rules and active SLA escalation daemons. Third, deliver proactive governance using spatial GIS outbreak detection, OLS forecasting, and privacy-compliant public transparency.")

    # ==================== SLIDE 6: LITERATURE REVIEW & EXISTING SYSTEM ====================
    s6 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s6, "Literature Review & Existing System Limitations", "Chapters 2 & 3 • Baseline Audit", 6)
    add_card(
        s6, Inches(0.65), Inches(1.4), Inches(5.85), Inches(5.3),
        "Academic Literature Foundations",
        [
            "TF-IDF & LinearSVC (Joachims, 1998; Pedregosa et al., 2011): High-dimensional sparse text classification with low latency.",
            "Platt Scaling (Platt, 1999): CalibratedClassifierCV converts SVM margins into calibrated probabilities.",
            "VADER Sentiment (Hutto & Gilbert, 2014): Lexicon-based polarity extracted as auxiliary signal, never sole safety gate.",
            "SentenceTransformers (Reimers & Gurevych, 2019): 'all-MiniLM-L6-v2' embeddings for semantic duplicate clustering.",
        ],
        header_color=C_NAVY, body_size=12.5,
    )
    add_card(
        s6, Inches(6.83), Inches(1.4), Inches(5.85), Inches(5.3),
        "Minor Project Limitations Addressed",
        [
            "Narrow 6-class classifier -> Upgraded to multi-class evaluation & calibrated probabilities.",
            "Single admin role -> Upgraded to 4-tier RBAC with signed HMAC timed tokens.",
            "MD5-jittered mock coordinates -> Upgraded to Gwalior 66-ward geospatial coordinates & clustering.",
            "Passive SLA timestamps -> Upgraded to automated breach promotion & +20 urgency penalty.",
            "Zero forecasting -> Added 14-day OLS trend projection & seasonal directives.",
        ],
        header_color=C_MAROON, body_size=12.5,
    )
    set_notes(s6, "Our design draws from established NLP and machine learning literature, notably LinearSVC for sparse text, Platt scaling for probability calibration, and MiniLM embeddings for semantic similarity. Auditing our original minor project revealed major limitations—single flat user roles, passive SLAs, and jittered mock coordinates—all systematically resolved in SmartCivic AI.")

    # ==================== SLIDE 7: PROPOSED SYSTEM ARCHITECTURE ====================
    s7 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s7, "Proposed System Architecture & Tech Stack", "Chapter 4 • System Architecture", 7)
    add_diagram_fit(s7, os.path.join(diag_dir, "system_architecture.png"), Inches(0.65), Inches(1.30), Inches(8.6), Inches(5.5))
    add_card(
        s7, Inches(9.45), Inches(1.35), Inches(3.23), Inches(5.4),
        "Core Tech Stack",
        [
            "Backend: FastAPI 0.115+, Python 3.14, Uvicorn ASGI",
            "ORM / DB: SQLAlchemy 2.x, SQLite / PostgreSQL",
            "Frontend: Jinja2, HTMX, Alpine.js, Tailwind CSS",
            "ML / NLP: scikit-learn, NLTK VADER, SentenceTransformers",
            "Mapping & Viz: Leaflet, OpenStreetMap, Chart.js",
            "Exports: ReportLab, PyMuPDF, OpenPyXL",
        ],
        header_color=C_NAVY, title_size=13, body_size=11.5,
    )
    set_notes(s7, "This layered architecture diagram presents SmartCivic AI across five cohesive tiers: the Presentation Layer powered by Jinja2, HTMX, Tailwind, and Leaflet; an ASGI Security Layer enforcing RBAC and rate limiting; the FastAPI Application Core handling routing and SLA daemons; the Intelligence Subsystem running NLP and forecasting; and SQLAlchemy managing 14 normalized database tables.")

    # ==================== SLIDE 8: SYSTEM DESIGN (USE CASE & DFD) ====================
    s8 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s8, "System Design: Use Case & Data Flow (DFD Level 1)", "Chapter 6 • Structured Design", 8)
    # Left title + diagram
    lbl1 = s8.shapes.add_textbox(Inches(0.65), Inches(1.25), Inches(5.85), Inches(0.32))
    p_l1 = lbl1.text_frame.paragraphs[0]
    p_l1.text = "Fig 1: Multi-Actor Use Case Model (4 RBAC Roles)"
    p_l1.font.name = FONT_FAMILY
    p_l1.font.size = Pt(12)
    p_l1.font.bold = True
    p_l1.font.color.rgb = C_MAROON
    add_diagram_fit(s8, os.path.join(diag_dir, "use_case.png"), Inches(0.65), Inches(1.62), Inches(5.85), Inches(5.15))

    # Right title + diagram
    lbl2 = s8.shapes.add_textbox(Inches(6.83), Inches(1.25), Inches(5.85), Inches(0.32))
    p_l2 = lbl2.text_frame.paragraphs[0]
    p_l2.text = "Fig 2: DFD Level 1 — Grievance & Triage Data Flow"
    p_l2.font.name = FONT_FAMILY
    p_l2.font.size = Pt(12)
    p_l2.font.bold = True
    p_l2.font.color.rgb = C_NAVY
    add_diagram_fit(s8, os.path.join(diag_dir, "dfd_level_1.png"), Inches(6.83), Inches(1.62), Inches(5.85), Inches(5.15))

    set_notes(s8, "These design diagrams define system interactions and data movement. On the left, the Use Case model delineates boundaries across Citizens, Field Officers, Department Admins, and the Super Admin. On the right, Data Flow Diagram Level 1 traces how raw citizen text and photos flow through AI triage, duplicate filtering, SLA scheduling, and audit persistence.")

    # ==================== SLIDE 9: DATABASE SCHEMA & ER DIAGRAM ====================
    s9 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s9, "Database Design: Entity-Relationship Architecture", "Chapter 6 • Data Modeling", 9)
    add_diagram_fit(s9, os.path.join(diag_dir, "er_diagram.png"), Inches(0.65), Inches(1.30), Inches(8.6), Inches(5.5))
    add_card(
        s9, Inches(9.45), Inches(1.35), Inches(3.23), Inches(5.4),
        "14 Normalized Entities",
        [
            "Core: complaints, users, departments, categories",
            "AI & Telemetry: complaint_analysis, similar_complaints, safety_rules",
            "Operations: sla_records, complaint_assignments, attachments",
            "Governance: priority_overrides, complaint_status_history, audit_logs, notifications",
            "Foreign-key indexed for zero SQL injection & O(log N) lookups.",
        ],
        header_color=C_MAROON, title_size=13, body_size=11.5,
    )
    set_notes(s9, "Our Entity-Relationship architecture normalizes operational and audit state into 14 relational tables. Separating raw complaints from complaint_analysis, sla_records, and priority_overrides ensures strict separation of concerns. Every status transition and administrative priority override writes to immutable history tables with actor attribution and timestamps.")

    # ==================== SLIDE 10: AI PIPELINE & SAFETY INVARIANT ====================
    s10 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s10, "AI Pipeline & Deterministic Safety Invariant", "Chapter 7 • AI/ML Methodology", 10)
    add_diagram_fit(s10, os.path.join(diag_dir, "ai_pipeline_flowchart.png"), Inches(0.65), Inches(1.30), Inches(7.5), Inches(5.5))
    add_card(
        s10, Inches(8.35), Inches(1.35), Inches(4.33), Inches(5.45),
        "Safety Guardrail Case Study",
        [
            "Input: 'Kindly note a live 440V wire snapped near primary school gate. Thank you.'",
            "VADER Sentiment: +0.65 (Polite/Positive)",
            "Naive ML Estimate: LOW (Score: 28) -> Risk!",
            "Rule Trigger: HAZARD_ELECTRICAL_SPARK",
            "Invariant Action: Priority forced >= CRITICAL (Score: 85, SLA: 6h)",
            "Explanation: ML factors displayed separately from deterministic safety override.",
        ],
        header_color=C_MAROON, fill_color=C_SOFT_MAROON, title_size=13, body_size=12,
    )
    set_notes(s10, "This flowchart shows our synchronous AI pipeline alongside a critical safety case study. A polite report about a live 440V wire near a school tricks statistical sentiment into predicting low urgency. Our post-ML Deterministic Safety Guard detects the acute electrical hazard token, unconditionally overriding priority to CRITICAL with a 6-hour SLA and logging the trigger clearly.")

    # ==================== SLIDE 11: GIS CLUSTERING & SLA ESCALATION ====================
    s11 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s11, "GIS Spatial Clustering & Automated SLA Escalation", "Chapter 8 • Operational Engines", 11)
    add_diagram_fit(s11, os.path.join(diag_dir, "sla_escalation_flow.png"), Inches(0.65), Inches(1.32), Inches(7.2), Inches(5.45))
    add_card(
        s11, Inches(8.05), Inches(1.35), Inches(4.63), Inches(5.4),
        "Spatial & Predictive Engines",
        [
            "Gwalior Ward GIS (/map): 66 ward centroids across Lashkar, Morar, City Center & Hazira.",
            "Outbreak Clustering: Flags spatial emergencies when >= 3 related grievances occur within 500m / 48h.",
            "OLS Forecasting (/predictive): 14-day linear trend projection with parametric 95% confidence intervals.",
            "SLA Escalation Sweep: Breached tickets receive +1 priority tier, +20 score penalty & alert dispatch.",
        ],
        header_color=C_NAVY, title_size=13, body_size=12,
    )
    set_notes(s11, "SmartCivic AI prevents grievances from stagnating silently. Our SLA engine assigns tiered deadlines—6 hours for Critical down to 168 hours for Low—and runs escalation sweeps that automatically bump priority and notify supervisors upon breach. Simultaneously, the GIS engine monitors 500-meter spatial clusters while OLS time-series modeling projects 14-day complaint volumes.")

    # ==================== SLIDE 12: LIVE LOCALHOST UI SNAPSHOT ====================
    s12 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s12, "Live Localhost Implementation: Apex Command Center", "Chapter 8 • UI Demonstration", 12)
    add_diagram_fit(s12, os.path.join(shot_dir, "live_apex_dashboard.png"), Inches(0.65), Inches(1.32), Inches(8.35), Inches(5.45))
    add_card(
        s12, Inches(9.20), Inches(1.35), Inches(3.48), Inches(5.4),
        "Observed Live Capabilities",
        [
            "Served live at http://127.0.0.1:8000/ via Uvicorn ASGI.",
            "Bilingual Hindi/English navigation with role persona switcher.",
            "Real-time KPI summary cards (56 Tabled, 52 Critical, 40 Breached).",
            "Interactive Chart.js doughnuts & 7-day spline trends.",
            "Dedicated routes: /portal, /transparency, /map, /predictive, /department, /officer.",
        ],
        header_color=C_TEAL, title_size=13, body_size=11.5,
    )
    set_notes(s12, "Here is an actual live screenshot captured directly from the locally running SmartCivic AI server at 127.0.0.1:8000. Notice the bilingual Hindi-English administrative interface, the fixed dark navigation sidebar, live KPI summary metrics tracking critical hazards and SLA breaches, and real-time Chart.js visualizations. Citizens access the public portal at /portal without authentication.")

    # ==================== SLIDE 13: MODEL EVALUATION & BENCHMARKS ====================
    s13 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s13, "Results & Model Evaluation Metrics", "Chapter 10 • Empirical Benchmarks", 13)

    table_shape = s13.shapes.add_table(5, 5, Inches(0.65), Inches(1.38), Inches(12.03), Inches(2.7))
    table = table_shape.table
    widths = [Inches(3.2), Inches(2.1), Inches(2.1), Inches(2.4), Inches(2.23)]
    for i, w in enumerate(widths):
        table.columns[i].width = w

    headers = ["Model Candidate", "Test Accuracy", "Macro F1-Score", "5-Fold CV Mean (+/- SD)", "Selection Status"]
    rows = [
        ["LinearSVC (Calibrated)", "96.00%", "0.9554", "0.9075 (+/- 0.0245)", "PRIMARY MODEL"],
        ["Logistic Regression", "94.00%", "0.9329", "0.9000 (+/- 0.0235)", "Runner-Up Fallback"],
        ["Multinomial Naive Bayes", "92.00%", "0.9094", "0.8875 (+/- 0.0194)", "Baseline Benchmark"],
        ["SGD Classifier (Log Loss)", "92.00%", "0.9093", "0.8825 (+/- 0.0194)", "Alternative Linear"],
    ]

    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_MAROON
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_FAMILY
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_SOFT_NAVY if r_idx == 0 else (C_OFFWHITE if r_idx % 2 == 1 else C_WHITE)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_FAMILY
            p.font.size = Pt(11.5)
            p.font.bold = (r_idx == 0)
            p.font.color.rgb = C_MAROON if (r_idx == 0 and c_idx == 4) else C_TEXT

    add_card(
        s13, Inches(0.65), Inches(4.32), Inches(12.03), Inches(2.45),
        "Dataset Transparency & Scientific Integrity Caveat",
        [
            "Evaluated using scikit-learn Stratified 5-Fold Cross-Validation on N = 500 curated multi-class bilingual civic grievances.",
            "LinearSVC (Calibrated) outperformed all candidates at 96.00% test accuracy, 0.9554 Macro F1, and ~1.2 ms inference latency.",
            "HONEST DISCLOSURE: High benchmark accuracy on curated synthetic data verifies class separation; real-world noisy municipal deployment requires ongoing domain retraining and confidence-gated human review (< 0.40 threshold).",
        ],
        header_color=C_NAVY, fill_color=C_SOFT_NAVY, title_size=13, body_size=12,
    )
    set_notes(s13, "We rigorously benchmarked four supervised NLP classifiers using stratified 5-fold cross-validation on 500 multi-class samples. Calibrated LinearSVC achieved 96.00% test accuracy and 0.9554 Macro F1 with sub-2ms inference. In keeping with strict academic honesty, we explicitly disclose that this benchmark reflects curated synthetic data and relies on confidence gating for noisy real-world text.")

    # ==================== SLIDE 14: VALUE ADDITION & SECURITY ====================
    s14 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s14, "Value Addition, Social Impact & Cybersecurity", "Chapter 11 • Security & Impact", 14)
    add_card(
        s14, Inches(0.65), Inches(1.4), Inches(5.85), Inches(5.3),
        "Municipal & Social Value Addition",
        [
            "Life-Safety Protection: Immediate hazard prioritization reduces response latency for fires, gas leaks & live wires.",
            "Civic Inclusion: Bilingual English/Hindi submission and voice-typing ready fields support non-technical citizens.",
            "DPDP Privacy-by-Design: Public transparency portal (/transparency) strictly scrubs names, phone numbers & addresses.",
            "Accountability: Printable Jan Sunwai / Gram Sabha social audit reports bridge digital logs with public hearings.",
        ],
        header_color=C_TEAL, body_size=12.5,
    )
    add_card(
        s14, Inches(6.83), Inches(1.4), Inches(5.85), Inches(5.3),
        "Cybersecurity & Access Controls",
        [
            "4-Tier ASGI RBAC: Cryptographic timed session tokens via URLSafeTimedSerializer (7-day TTL).",
            "Upload Hardening: Binary magic-byte inspection (PNG/JPEG/WebP) + 10 MB payload limit blocks shell uploads.",
            "SQL Injection Defense: Exclusive SQLAlchemy ORM parameterized queries across all 44 routes.",
            "Rate Limiting & Audit Trail: SlowAPI throttling and immutable audit_logs for administrative overrides.",
        ],
        header_color=C_MAROON, body_size=12.5,
    )
    set_notes(s14, "Beyond algorithmic accuracy, SmartCivic AI delivers tangible civic value and defense-in-depth security. It protects citizen privacy under India's DPDP Act by scrubbing personal identifiers from public transparency feeds. Technically, every endpoint enforces server-side RBAC, binary magic-byte checks on uploaded photos, rate limiting, and parameterized ORM queries.")

    # ==================== SLIDE 15: TESTING & PLAGIARISM REPORT ====================
    s15 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s15, "Software Testing & Plagiarism Compliance Report", "Chapter 9 • Verification & QA", 15)
    add_card(
        s15, Inches(0.65), Inches(1.4), Inches(5.85), Inches(5.3),
        "Automated PyTest Verification (29 / 29 Passed)",
        [
            "Execution Environment: PyTest 9.1.1 on Python 3.14.5 (14.08 seconds).",
            "Result: 29 Passed, 0 Failed (100% pass rate across unit & integration tests).",
            "API & Security (13 tests): Auth sessions, magic-byte file checks, PDF/CSV/Excel exports.",
            "AI & Safety (10 tests): Priority math bounds, edge-case Hindi/empty inputs, non-downgrade rules.",
            "Live Localhost Audit: Verified HTTP 200 across /, /portal, /transparency, /map, /predictive, /department.",
        ],
        header_color=C_NAVY, body_size=12.5,
    )
    add_card(
        s15, Inches(6.83), Inches(1.4), Inches(5.85), Inches(5.3),
        "Academic Plagiarism & Originality Status",
        [
            "University Threshold: ITM University Gwalior mandates <= 25% similarity index on Turnitin/Urkund.",
            "Report Writing Standard: Written in original technical prose grounded strictly in repository source code.",
            "Zero Fabricated Data: Every F1 score, DB count & test result is directly reproducible.",
            "Status: [Insert Final Turnitin / DrillBit Similarity % Prior to Binding].",
        ],
        header_color=C_MAROON, fill_color=C_SOFT_MAROON, body_size=12.5,
    )
    set_notes(s15, "Quality assurance covers both automated test coverage and academic integrity. All 29 PyTest unit and full-stack integration tests execute in 14.08 seconds with zero failures, alongside live localhost verification across core dashboards. In accordance with ITM University norms requiring under 25 percent plagiarism, the entire report was authored originally directly from repository code.")

    # ==================== SLIDE 16: PUBLICATIONS & VERIFIED LIMITATIONS ====================
    s16 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s16, "Publications Status & Verified System Limitations", "Chapter 12 • Academic Disclosure", 16)
    add_card(
        s16, Inches(0.65), Inches(1.4), Inches(5.85), Inches(5.3),
        "Research Paper / Publication Status",
        [
            "Manuscript Scope: 'Safety-Invariant Hybrid NLP & Spatial Forecasting for Municipal Grievance Governance'.",
            "Empirical Artifact: Complete reproducible evaluation pipeline (ai/training/evaluate.py).",
            "Status: [Ready for Submission / Specify Conference or Journal Details if Communicated].",
            "Open Repository: Codebase, architecture diagrams & reproducible evidence pack published on GitHub.",
        ],
        header_color=C_NAVY, body_size=12.5,
    )
    add_card(
        s16, Inches(6.83), Inches(1.4), Inches(5.85), Inches(5.3),
        "Verified Honest Technical Limitations",
        [
            "Biohazard Keyword Gap: 'Dead stray cow' evaluated to LOW (26) due to missing animal carcass rules.",
            "GIS CSS Dependency (/map): Missing leaflet.css causes vertical tile stacking during live map render.",
            "Forecast Template Binding (/predictive): Minor missing field bindings on hotspot counters & seasonal copy.",
            "Synthetic Training Corpus: Model generalization requires authentic municipal ticket feedback loops.",
        ],
        header_color=C_MAROON, body_size=12.5,
    )
    set_notes(s16, "Per ITM University evaluation standards, we record both research communication status and honest technical limitations discovered during testing. Specifically, our evaluation caught a keyword gap for animal carcass biohazards, a missing Leaflet stylesheet on the GIS map page, and minor template field gaps in predictive hotspot cards—all clearly logged in ISSUES.md.")

    # ==================== SLIDE 17: CONCLUSION & FUTURE SCOPE ====================
    s17 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s17, "Conclusion & Future Scope", "Chapter 12 • Summary & Roadmap", 17)
    add_card(
        s17, Inches(0.65), Inches(1.4), Inches(5.85), Inches(5.3),
        "Project Conclusion",
        [
            "Successfully transformed a minor-project prototype into an end-to-end SmartCivic AI platform.",
            "Proved that Calibrated LinearSVC (96% test accuracy) paired with Deterministic Safety Guards delivers reliable civic triage.",
            "Automated SLA escalation, RBAC security, DPDP transparency & OLS forecasting within a testable FastAPI codebase.",
        ],
        header_color=C_MAROON, body_size=13,
    )
    add_card(
        s17, Inches(6.83), Inches(1.4), Inches(5.85), Inches(5.3),
        "Future Enhancement Scope",
        [
            "UI Polish: Bundle local leaflet.css/tiles and bind seasonal predictive database rules.",
            "Computer Vision Module: CNN-based automated pothole severity and garbage volume estimation from photos.",
            "IoT & Telemetry Integration: Real-time water pressure & transformer sensors generating proactive tickets.",
            "Voice IVR / WhatsApp Bot: Speech-to-text grievance filing for regional dialects.",
        ],
        header_color=C_TEAL, body_size=13,
    )
    set_notes(s17, "In conclusion, SmartCivic AI achieves every primary objective set for this B.Tech Major Project: explainable ML classification, unbreakable safety invariants, active SLA governance, and verified testing. Future enhancements will patch the frontend stylesheet bug, integrate computer vision for automated pothole inspection, and add WhatsApp voice intake for rural and urban inclusivity.")

    # ==================== SLIDE 18: REFERENCES & THANK YOU ====================
    s18 = prs.slides.add_slide(blank_layout)
    add_master_chrome(s18, "References & Acknowledgements", "Academic Citations & Q&A", 18)
    add_card(
        s18, Inches(0.65), Inches(1.38), Inches(7.35), Inches(5.35),
        "Selected IEEE References",
        [
            "[1] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python,' JMLR, vol. 12, pp. 2825–2830, 2011.",
            "[2] T. Joachims, 'Text Categorization with Support Vector Machines,' ECML, pp. 137–142, 1998.",
            "[3] C. J. Hutto and E. Gilbert, 'VADER: A Parsimonious Rule-Based Model for Sentiment Analysis,' ICWSM, 2014.",
            "[4] N. Reimers and I. Gurevych, 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks,' EMNLP, 2019.",
            "[5] S. Ramirez, 'FastAPI Framework Documentation,' Tiangolo, 2024. [Online]. Available: https://fastapi.tiangolo.com/",
            "[6] Ministry of Electronics & IT (India), 'The Digital Personal Data Protection Act, 2023,' Gazette of India.",
        ],
        header_color=C_NAVY, title_size=13, body_size=11,
    )
    add_card(
        s18, Inches(8.25), Inches(1.38), Inches(4.43), Inches(5.35),
        "Thank You!",
        [
            "Candidate: Samit Jain",
            "Enrollment No.: [ENROLLMENT NO.]",
            "B.Tech CSE (2023–2027)",
            "ITM University, Gwalior (M.P.)",
            "Questions & Live Code Demonstration Welcomed by the Panel.",
        ],
        header_color=C_MAROON, fill_color=C_SOFT_MAROON, title_size=18, body_size=13,
    )
    set_notes(s18, "Thank you, respected members of the ITM University Gwalior evaluation committee, for your patience and valuable feedback. All empirical results, FastAPI routes, and diagrams are verified directly against our repository. I am now happy to answer your technical questions or walk through the live localhost application.")

    prs.save(output_path)
    print(f"ITM University format presentation saved to: {output_path}")


if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "SmartCivic_AI_ITM_University_Format.pptx")
    create_itm_deck(out_file)
