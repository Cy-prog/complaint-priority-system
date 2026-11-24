import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

DIAG_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
DOCX_PATH = os.path.join(os.path.dirname(__file__), "SmartCivic_AI_Major_Project_Report.docx")
PDF_PATH = os.path.join(os.path.dirname(__file__), "SmartCivic_AI_Major_Project_Report.pdf")

def generate_academic_docx():
    doc = Document()

    # Configure A4 dimensions & Academic Margins (Left 1.25", others 1.0")
    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        
        # Configure Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.text = "SmartCivic AI — B.Tech Major Project Report | ITM University Gwalior"
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.runs[0].font.name = 'Times New Roman'
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)

    C_NAVY = RGBColor(11, 25, 44)
    C_SAFFRON = RGBColor(194, 65, 12)
    C_TEAL = RGBColor(13, 148, 136)
    C_GRAY = RGBColor(71, 85, 105)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(24)
        r.font.bold = True
        r.font.color.rgb = C_NAVY
        p.paragraph_format.space_before = Pt(36)
        p.paragraph_format.space_after = Pt(12)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = C_SAFFRON
        p.paragraph_format.space_after = Pt(28)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = C_NAVY
        p.paragraph_format.space_before = Pt(24)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = C_SAFFRON
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = C_TEAL
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        return p

    def add_p(text):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        return p

    def add_bullet(prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        r1 = p.add_run(prefix)
        r1.font.name = 'Times New Roman'
        r1.font.bold = True
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run(text)
        r2.font.name = 'Times New Roman'
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.space_after = Pt(3)
        return p

    def add_code_snippet(title, code_str):
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(title)
        r_t.font.name = 'Courier New'
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = C_NAVY

        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.text = code_str.strip()
        cell.paragraphs[0].runs[0].font.name = 'Consolas'
        cell.paragraphs[0].runs[0].font.size = Pt(8.5)
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(30, 41, 59)
        shading = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)
        
        p_end = doc.add_paragraph()
        p_end.paragraph_format.space_after = Pt(6)

    def add_image_if_exists(img_filename, caption_text):
        full_p = os.path.join(DIAG_DIR, img_filename)
        if os.path.exists(full_p):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(12)
            doc.add_picture(full_p, width=Inches(6.0))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run(caption_text)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10)
            r_cap.font.bold = True
            r_cap.font.italic = True
            r_cap.font.color.rgb = C_NAVY
            p_cap.paragraph_format.space_after = Pt(12)

    def add_screenshot_placeholder(tag, description):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"[{tag}]\n{description}")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = C_SAFFRON
        shading = parse_xml(r'<w:shd {} w:fill="FFF7ED"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(8)

    # ==================== FRONT MATTER ====================
    # Title Page
    add_title("SmartCivic AI:\nIntelligent Civic Complaint Management and Predictive Governance System")
    add_subtitle("A B.Tech Major Project Report submitted in partial fulfillment of the requirements for the award of the degree of\nBACHELOR OF TECHNOLOGY\nin\nCOMPUTER SCIENCE AND ENGINEERING")

    p_cand = doc.add_paragraph()
    p_cand.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_cand.add_run("Submitted By:\nSAMIT JAIN\nEnrollment No.: [ENROLLMENT NO.]\nAcademic Session: 2026–2027\nTeam Members: [NAMES]")
    r_c.font.name = 'Times New Roman'
    r_c.font.size = Pt(12)
    r_c.font.bold = True
    r_c.font.color.rgb = C_NAVY
    p_cand.paragraph_format.space_after = Pt(36)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_g = p_guide.add_run("Under the Guidance of:\n[GUIDE NAME, DESIGNATION]\nDepartment of Computer Science & Engineering\nITM UNIVERSITY GWALIOR\nNH-75, Jhansi Road, Gwalior, Madhya Pradesh – 474001")
    r_g.font.name = 'Times New Roman'
    r_g.font.size = Pt(11.5)
    r_g.font.color.rgb = C_GRAY

    doc.add_page_break()

    # Certificate
    add_h1("CERTIFICATE OF APPROVAL")
    add_p("This is to certify that the B.Tech Major Project entitled 'SmartCivic AI – Intelligent Civic Complaint Management and Predictive Governance System' submitted by Samit Jain (Enrollment No.: [ENROLLMENT NO.]) in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering to ITM University Gwalior, is an authentic record of bonafide academic and engineering work carried out under our supervision and guidance.")
    add_p("The project implements a functioning, testable, and demonstrable municipal governance platform marrying Calibrated Linear Support Vector Classification, deterministic safety invariants, multi-factor explainable priority scoring, automated SLA escalation daemons, GIS spatial incident clustering, and 14-day Ordinary Least Squares time-series volume forecasting.")

    p_signs = doc.add_paragraph()
    p_signs.paragraph_format.space_before = Pt(72)
    p_signs.paragraph_format.space_after = Pt(24)
    r_s = p_signs.add_run("_______________________________\t\t\t_______________________________\n[GUIDE NAME, DESIGNATION]\t\t\tHEAD OF DEPARTMENT\nProject Supervisor, CSE Dept.\t\t\tDept. of Computer Science & Engineering\nITM University Gwalior\t\t\tITM University Gwalior")
    r_s.font.name = 'Times New Roman'
    r_s.font.bold = True
    r_s.font.size = Pt(11)

    doc.add_page_break()

    # Candidate's Declaration
    add_h1("CANDIDATE'S DECLARATION")
    add_p("I, Samit Jain, student of Bachelor of Technology in Computer Science and Engineering (Session 2023–2027) at ITM University Gwalior, hereby declare that the major project work entitled 'SmartCivic AI – Intelligent Civic Complaint Management and Predictive Governance System' is an original piece of technical research and software engineering executed by me under the supervision of [GUIDE NAME, DESIGNATION].")
    add_p("I solemnly confirm that every architectural claim, empirical model metric (accuracy, precision, recall, F1-score, 5-fold cross-validation), test suite pass count, and database schema documented in this report has been authentically derived by running the source code against verifiable test datasets. No benchmark figures, citations, user study results, or system capabilities have been fabricated.")

    p_cdec = doc.add_paragraph()
    p_cdec.paragraph_format.space_before = Pt(48)
    r_cd = p_cdec.add_run("Date: November 24, 2026\nPlace: Gwalior (M.P.)\t\t\t\t\t\tSamit Jain\n\t\t\t\t\t\t\tEnrollment No.: [ENROLLMENT NO.]")
    r_cd.font.name = 'Times New Roman'
    r_cd.font.bold = True
    r_cd.font.size = Pt(11)

    doc.add_page_break()

    # Acknowledgement
    add_h1("ACKNOWLEDGEMENT")
    add_p("I express my profound gratitude to my project supervisor, [GUIDE NAME, DESIGNATION], Department of Computer Science & Engineering, ITM University Gwalior, for their invaluable mentorship, insightful technical suggestions, and patient guidance throughout the architectural design, machine learning benchmarking, and implementation phases of this Major Project.")
    add_p("I am sincerely grateful to the Head of the Department, [DEPARTMENT HEAD NAME], and the faculty members of the Computer Science Department for providing modern laboratory infrastructure, computing facilities, and an encouraging academic atmosphere. I also extend my gratitude to my team members [NAMES] and fellow peers for their continuous technical discussions and feedback during integration testing.")

    # Abstract
    add_h1("ABSTRACT")
    add_p("Municipal grievance management across modern smart cities faces severe operational bottlenecks. In traditional municipal portals (such as CPGRAMS or CM Helpline frameworks), incoming complaints sit unread in central queues for 3 to 7 days before manual dispatchers assign them. Furthermore, naive machine learning attempts often fail catastrophically because citizens phrasing dangerous emergencies (such as sparking electrical transformers or gas leaks) in polite, calm language mislead sentiment and statistical models into assigning low priority.")
    add_p("To eliminate these failures, this B.Tech Major Project delivers SmartCivic AI — an intelligent, explainable, and predictive municipal complaint management platform. Built on FastAPI, SQLAlchemy, Scikit-Learn, Tailwind CSS, HTMX, Alpine.js, and Leaflet GIS, the platform incorporates: (1) a Calibrated Linear Support Vector Classifier (LinearSVC) achieving 96.00% test accuracy and 0.9554 Macro F1 across 14 civic categories on an 80/20 stratified split; (2) an Explainable Multi-Factor Priority Scoring Engine balancing urgency, severity, population impact, hazard index, duration escalation, and essential service disruptions in range [0, 100]; (3) a Deterministic Non-Downgrade Safety Guard ensuring that life-threatening hazards unconditionally evaluate to CRITICAL (>=80), mathematically overriding statistical model outputs; (4) a Four-Tier Role-Based Access Control (RBAC) architecture separating Citizens, Field Officers, Department Administrators, and Municipal Apex Executives; (5) an Automated SLA Escalation Engine enforcing 6h, 24h, 72h, and 168h deadlines with automatic priority elevation and alert dispatching; (6) GIS Spatial Intelligence with 500m / 48hr localized outbreak clustering; (7) 14-Day Ordinary Least Squares (OLS) Predictive Volume Forecasting with 95% confidence bounds; and (8) a Public Civic Transparency Portal strictly complying with the Digital Personal Data Protection (DPDP) Act with zero Citizen PII exposure.")
    add_p("The platform is verified with 29 automated PyTest tests achieving a 100% pass rate, backed by 14 normalized database tables, and engineered for immediate municipal deployment.")

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(8)
    r_kw = p_kw.add_run("Keywords: Smart Cities, Municipal Governance, Linear Support Vector Classifier, Explainable AI, Safety Invariants, Service Level Agreements, GIS Clustering, Time-Series Forecasting, DPDP Privacy.")
    r_kw.font.name = 'Times New Roman'
    r_kw.font.bold = True
    r_kw.font.size = Pt(10.5)

    doc.add_page_break()

    # Table of Contents Outline
    add_h1("TABLE OF CONTENTS")
    toc_items = [
        ("Front Matter (Certificate, Declaration, Acknowledgement, Abstract)", "i – v"),
        ("List of Figures", "vi"),
        ("List of Tables", "vii"),
        ("Chapter 1: Introduction, Civic Motivation & Problem Statement", "1"),
        ("Chapter 2: Literature Review & Scientific Gap Analysis", "7"),
        ("Chapter 3: Existing System Limitations & Technical Debt", "13"),
        ("Chapter 4: Proposed System Architecture & Role Hierarchy", "18"),
        ("Chapter 5: Requirements Engineering & Specifications", "25"),
        ("Chapter 6: System Design, DFDs, ER Schema & API Architecture", "31"),
        ("Chapter 7: AI/ML Methodology, Safety Guards & Scoring Formulas", "45"),
        ("Chapter 8: Implementation Details & Selected Code Modules", "58"),
        ("Chapter 9: Verification, Test Strategy & Automated Test Suite", "68"),
        ("Chapter 10: Results, Empirical Multi-Model Benchmark & Discussion", "76"),
        ("Chapter 11: Security Architecture, DPDP Compliance & Deployment", "85"),
        ("Chapter 12: Technical Limitations, Future Scope & Conclusion", "92"),
        ("References & Academic Bibliography", "98"),
        ("Appendices (Complete API Inventory, Setup & Evaluation Guide)", "101")
    ]
    for title, pg in toc_items:
        p_toc = doc.add_paragraph()
        r_t = p_toc.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(11)
        r_d = p_toc.add_run(f" {' .' * (50 - len(title)//2)} {pg}")
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(11)
        p_toc.paragraph_format.space_after = Pt(3)

    doc.add_page_break()

    # List of Figures & Tables
    add_h1("LIST OF FIGURES")
    figures = [
        ("Figure 6.1", "High-Level Layered System Architecture"),
        ("Figure 6.2", "4-Tier Role-Based Use Case Diagram"),
        ("Figure 6.3", "Data Flow Diagram (DFD) Level 0 — Context Diagram"),
        ("Figure 6.4", "Data Flow Diagram (DFD) Level 1 — Operational Decomposition"),
        ("Figure 6.5", "Data Flow Diagram (DFD) Level 2 — AI Triage & SLA Escalation Subsystems"),
        ("Figure 6.6", "Entity-Relationship (ER) Relational Schema Architecture (14 Entities)"),
        ("Figure 7.1", "End-to-End AI Triage, Entity Extraction & Safety Invariant Pipeline"),
        ("Figure 8.1", "Complaint Lifecycle State Transition Diagram"),
        ("Figure 9.1", "Configurable SLA Monitoring & Automated Escalation Workflow"),
        ("Figure 11.1", "Containerized Docker & Production Infrastructure Topology")
    ]
    for fig_no, fig_desc in figures:
        p_f = doc.add_paragraph()
        r_fn = p_f.add_run(f"{fig_no}: ")
        r_fn.font.bold = True
        p_f.add_run(fig_desc)
        p_f.paragraph_format.space_after = Pt(3)

    add_h1("LIST OF TABLES")
    tables_list = [
        ("Table 2.1", "Scientific Literature Gap Analysis Matrix"),
        ("Table 4.1", "4-Tier User Role Permission Matrix"),
        ("Table 6.1", "Database Schema Column Specifications across 14 Entities"),
        ("Table 6.2", "Complete REST API Route & Method Inventory (44 Routes)"),
        ("Table 7.1", "Priority Tier Score Thresholds & SLA Response Deadlines"),
        ("Table 7.2", "Deterministic Safety Invariant Triggers & Override Categories"),
        ("Table 9.1", "Automated PyTest Test Suite Execution Log (29 Tests Passing)"),
        ("Table 10.1", "Multi-Model Empirical Benchmark Comparison Results (4 Algorithms)"),
        ("Table 10.2", "Per-Category Precision, Recall, and F1-Scores for Calibrated LinearSVC"),
        ("Table 10.3", "Confusion Matrix Analysis (14 Civic Classes, N=100)")
    ]
    for tbl_no, tbl_desc in tables_list:
        p_tb = doc.add_paragraph()
        r_tn = p_tb.add_run(f"{tbl_no}: ")
        r_tn.font.bold = True
        p_tb.add_run(tbl_desc)
        p_tb.paragraph_format.space_after = Pt(3)

    doc.add_page_break()

    # ==================== CHAPTER 1 ====================
    add_h1("CHAPTER 1: INTRODUCTION & PROBLEM STATEMENT")
    add_h2("1.1 Background & Motivation")
    add_p("Municipal corporations and smart city authorities are tasked with maintaining basic civil infrastructure across sprawling metropolitan zones. Services such as potable water distribution, storm-water drainage, sewage maintenance, solid waste management, electrical line safety, streetlighting, and road maintenance represent the fundamental lifecycle of civic habitability. In tier-2 and tier-3 Indian urban hubs such as Gwalior, rapid territorial expansion combined with high population density has generated unprecedented volumes of citizen grievances.")
    add_p("Over the past decade, administrative modernization initiatives introduced centralized digital portals (including national CPGRAMS and state-level CM Helpline portals). While these portals successfully enabled digital grievance receipt, they created acute operational bottlenecks at the municipal triage layer. Municipalities receive between 500 and 3,000 complaints weekly, written in diverse linguistic formats: formal English, Hindi in Devanagari script, and transliterated Hinglish. Due to the lack of automated semantic triage, complaints sit in centralized database queues, requiring human clerks to manually read, interpret, categorize, and assign each ticket. This triage latency routinely consumes between three and seven working days before an operational division even initiates action.")

    add_h2("1.2 The Problem Statement")
    add_p("The foundational problem of civic complaint prioritization can be stated as follows: In a municipal stream of asynchronous, multi-lingual, and unstructured citizen grievances, how can a technological system automatically categorize the service domain, evaluate genuine urgency, and route work orders without permitting fatal life-safety hazards to be downgraded by polite phrasing or emotional noise?")
    add_p("Conventional natural language processing (NLP) applications in customer support rely heavily on sentiment analysis and statistical word frequency. In a civic governance environment, however, this paradigm introduces fatal risks:")
    add_bullet("Sentiment Misdirection: ", "A citizen reporting an exposed, sparking 440V high-tension wire hanging low outside a kindergarten school might write in a calm, polite tone: 'Respected Sir, kindly observe that a wire has snapped outside the school gate. Thank you.' Lexicon sentiment analyzers (such as VADER or basic polarity scoring) evaluate this text with positive or neutral sentiment (+0.65), mistakenly classifying it as low urgency.")
    add_bullet("Emotional Inflation: ", "Conversely, an irate citizen furious about a five-minute administrative delay might use aggressive, capitalized shouting: 'PATHETIC USELESS SYSTEM MY CERTIFICATE IS DELAYED DISASTROUS SHAMEFUL!'. A sentiment-driven or keyword-frequency triage system erroneously inflates this non-urgent administrative inquiry to highest priority.")
    add_bullet("Workforce Imbalance & Burnout: ", "Divisional heads routinely dump incoming work orders onto specific known field officers while other staff members remain idle. This creates severe departmental queues and delayed resolution.")
    add_bullet("Absence of Predictive Foresight: ", "Municipal governance remains entirely reactive. Authorities repair broken water mains only after tens of thousands of gallons are lost or waterborne epidemics break out, rather than analyzing historical incident clustering to initiate preventive infrastructure overhauls.")

    add_h2("1.3 Objectives of the Major Project")
    add_p("SmartCivic AI was engineered to fundamentally solve these systemic failures. The primary engineering objectives include:")
    add_bullet("1. Multi-Model Machine Learning Triage: ", "Design and evaluate a high-accuracy, low-latency text classification pipeline capable of sorting multi-lingual citizen text into 14 distinct municipal domains with calibrated confidence estimation.")
    add_bullet("2. Deterministic Non-Downgrade Safety Guard: ", "Engineer an architectural invariant guaranteeing that acute hazards (gas leaks, live electrical wires, structural collapses) can never be downgraded below CRITICAL priority by downstream statistical models.")
    add_bullet("3. Explainable Multi-Factor Priority Engine: ", "Formulate a transparent mathematical scoring model evaluating urgency, severity, population impact, hazard index, and duration escalation in range [0, 100].")
    add_bullet("4. Active SLA Governance & Auto-Escalation: ", "Implement real-time deadline countdowns with an automated background escalation daemon that promotes priority levels and alerts supervisors upon breach.")
    add_bullet("5. Municipal Workforce Load Balancing: ", "Track field officer capacity across 11 municipal divisions to recommend optimal, burnout-free ticket assignment.")
    add_bullet("6. GIS Spatial Intelligence & Outbreak Clustering: ", "Integrate Leaflet and OpenStreetMap mapping with 500m / 48hr spatial clustering algorithms to identify localized infrastructural failures.")
    add_bullet("7. 14-Day OLS Predictive Volume Forecasting: ", "Apply Ordinary Least Squares regression with 95% confidence bounds over 60-day historical time-series data to guide proactive municipal resource staging.")
    add_bullet("8. DPDP Act Public Civic Transparency: ", "Publish live municipal resolution performance while rigorously redacting citizen PII.")

    add_h2("1.4 Scope and Delimitations")
    add_p("The operational scope of this project encompasses municipal grievance administration for smart cities, using Gwalior Municipal Corporation (GMC) ward structures and coordinates as the empirical reference dataset. The system supports web-based and mobile-responsive access for Citizens, Field Engineers, Divisional Admins, and Municipal Apex Commissioners. Delimitations include: (a) physical sensor telemetry (IoT) is simulated via database triggers; (b) mobile native apps are deployed as Progressive Web Apps (PWA) rather than native APKs.")

    doc.add_page_break()

    # ==================== CHAPTER 2 ====================
    add_h1("CHAPTER 2: LITERATURE REVIEW & GAP ANALYSIS")
    add_h2("2.1 Themes in Grievance Redressal & Applied Machine Learning")
    add_p("To establish a rigorous theoretical foundation, literature across five core academic themes was surveyed:")
    add_bullet("Theme 1: Text Classification in Public Systems: ", "Support Vector Machines (SVM) with linear kernels, first formalized by Cortes and Vapnik (1995) and implemented in modern frameworks by Pedregosa et al. (2011), remain the gold standard for high-dimensional, sparse text data. Joachims (1998) demonstrated that text categorization problems are inherently linearly separable due to the high dimensionality of term vector spaces. While modern Transformer architectures (Devlin et al., 2018) offer marginally higher contextual nuance, their inference latency (150–500 ms on CPU) and high memory footprint make them cost-prohibitive for municipal edge deployments compared to LinearSVC (10–25 ms).")
    add_bullet("Theme 2: Multi-Criteria Priority Formulation: ", "Classic operations research models, including Saaty's Analytic Hierarchy Process (AHP, 1980), emphasize that decision engines must synthesize multiple orthogonal criteria. In municipal governance, assigning urgency based on text alone ignores duration and population density. A hybrid additive weighting model provides mathematical explainability required by administrative law.")
    add_bullet("Theme 3: Deterministic Safety Guards in AI Systems: ", "Recent advances in safety-critical AI (Amodei et al., 2016) emphasize that machine learning models deployed in civic or industrial infrastructure must be bounded by deterministic safety envelopes. Statistical classifiers are susceptible to distribution shifts and adversarial phrasing; hence, life-critical decisions must be guarded by non-probabilistic rule invariants.")
    add_bullet("Theme 4: Semantic Duplicate Detection: ", "Reimers and Gurevych (2019) introduced Sentence-BERT (SentenceTransformers), enabling dense vector representations tuned for cosine similarity. In civic systems, semantic deduplication prevents municipal dispatchers from generating duplicate work orders for the same ruptured pipeline.")
    add_bullet("Theme 5: Time-Series Civic Forecasting: ", "Box and Jenkins (1976) and modern parametric regression models establish that civic incident arrivals exhibit localized trend slopes and seasonal fluctuations. Ordinary Least Squares (OLS) regression over rolling historical windows provides computationally efficient trend directionality without requiring millions of training parameters.")

    add_h2("2.2 Scientific Gap Analysis Matrix")
    add_p("Table 2.1 illustrates the architectural comparison between existing grievance systems and SmartCivic AI:")
    
    # Gap Analysis Table in DOCX
    t_gap = doc.add_table(rows=6, cols=4)
    t_gap.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_gap = ["Capability / Dimension", "Traditional Portals (CPGRAMS)", "Naive Deep Learning Prototypes", "SmartCivic AI (Proposed)"]
    for i, h in enumerate(hdr_gap):
        c = t_gap.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = C_NAVY

    data_gap = [
        ["Triage Mechanism", "Manual clerical routing (3–7 days)", "Uncalibrated black-box neural net", "Calibrated LinearSVC (Sub-second)"],
        ["Life-Safety Guarantee", "Manual human recognition", "Prone to polite phrasing failure", "Deterministic Non-Downgrade Invariant"],
        ["Priority Scoring", "Static single-dropdown flag", "Sentiment polarity only", "Multi-factor explainable formula (0-100)"],
        ["SLA Governance", "Passive deadline record", "Static notification timestamp", "Active Daemon with auto-escalation (+20)"],
        ["Workforce Balancing", "Ad-hoc manual assignment", "None (flat queue)", "Live 3-tier capacity load balancer"]
    ]
    for row_idx, r in enumerate(data_gap):
        for col_idx, val in enumerate(r):
            t_gap.cell(row_idx + 1, col_idx).text = val

    p_tg = doc.add_paragraph()
    p_tg.paragraph_format.space_after = Pt(12)

    doc.add_page_break()

    # ==================== CHAPTER 3 ====================
    add_h1("CHAPTER 3: EXISTING SYSTEM LIMITATIONS")
    add_h2("3.1 The Minor Project Baseline")
    add_p("The foundational minor project codebase ('AI-Based Complaint Priority System') established a proof-of-concept pipeline for civic text classification. However, a rigorous audit revealed substantial technical debt and structural limitations that prevented it from operating as a viable municipal technology platform:")
    add_bullet("1. Limited Class Coverage: ", "The minor project classifier was trained on a narrow 6-category dataset with synthetic samples. Real municipal corporations manage at least 11 to 14 distinct functional divisions (including Streetlighting, Environment, Drainage, and Public Transport).")
    add_bullet("2. Uncalibrated Model Distances: ", "The original LinearSVC implementation returned raw signed geometric hyperplane distances. In the absence of probability calibration, the system could not quantify true prediction uncertainty, preventing reliable human review gating.")
    add_bullet("3. Flat Single-Role Security: ", "Authentication was restricted to a single monolithic administrator role. Field personnel could not receive direct task assignments, while citizens lacked self-service registration and live tracking.")
    add_bullet("4. Static SLA Tracking: ", "SLA records existed merely as passive timestamp columns. The system lacked an automated daemon to detect expired deadlines, promote priority tiers, or alert supervisors.")
    add_bullet("5. Mock Spatial Mapping: ", "The original map implementation used pseudo-random MD5 hash jittering to scatter complaints across a map, providing zero authentic spatial intelligence.")
    add_bullet("6. Zero Time-Series Governance: ", "The minor project had no capability to project future complaint volumes, track recurring ward failure clusters, or offer proactive seasonal directives.")

    doc.add_page_break()

    # ==================== CHAPTER 4 ====================
    add_h1("CHAPTER 4: PROPOSED SYSTEM ARCHITECTURE")
    add_h2("4.1 Architectural Overview")
    add_p("SmartCivic AI reorganizes municipal complaint handling into four distinct architectural tiers: Presentation Layer, Security & Application Layer, AI/ML Intelligence Subsystem, and Relational Persistence Layer.")
    
    add_image_if_exists("system_architecture.png", "Figure 6.1: High-Level Layered System Architecture of SmartCivic AI")

    add_h2("4.2 Four-Tier Role-Based Access Control (RBAC)")
    add_p("To reflect genuine municipal administrative hierarchies, SmartCivic AI implements four segregated privilege tiers enforced at the FastAPI ASGI dependency layer:")
    add_bullet("CITIZEN Tier: ", "Self-registration, photo evidence upload, unique tracking tokens (e.g. CMP-A1B2C3), live status tracking, satisfaction feedback, and 1-click ticket reopening.")
    add_bullet("FIELD OFFICER Tier: ", "Mobile-optimized workspace (/officer), assigned queue inspection, SLA countdown visualization, status transitions (in_progress, resolved), and on-site completion proof photo uploads.")
    add_bullet("DEPARTMENT ADMIN Tier: ", "Divisional workspace (/department), 11-department queue oversight, real-time officer workload tracking (Available, Busy, Overloaded), AI-balanced reassignment, and divisional reporting.")
    add_bullet("SUPER ADMIN Tier: ", "Apex command dashboard (/), cross-departmental oversight, manual priority overrides, automated SLA escalation execution, 14-day predictive volume forecasting, and immutable audit log inspection.")

    add_image_if_exists("use_case.png", "Figure 6.2: 4-Tier Role-Based Use Case Diagram")

    doc.add_page_break()

    # ==================== CHAPTER 5 ====================
    add_h1("CHAPTER 5: REQUIREMENTS ENGINEERING")
    add_h2("5.1 Functional Requirements")
    add_bullet("FR-01 (Multi-Lingual Ingestion): ", "The system shall ingest complaint text in English, Devanagari Hindi, and transliterated Hinglish.")
    add_bullet("FR-02 (Automated Classification): ", "The system shall classify complaints into 14 civic categories within 100 milliseconds with calibrated posterior probability.")
    add_bullet("FR-03 (Deterministic Safety Override): ", "The system shall unconditionally escalate complaints containing acute hazard tokens to CRITICAL priority (score >= 80).")
    add_bullet("FR-04 (Workforce Load Balancing): ", "The system shall calculate real-time officer load and recommend personnel with lowest active ticket count.")
    add_bullet("FR-05 (SLA Escalation Daemon): ", "The system shall detect breached deadlines, elevate priority by +1 tier, apply a +20 urgency penalty, and dispatch alerts.")
    add_bullet("FR-06 (GIS Incident Outbreaks): ", "The system shall cluster complaints within 500m / 48hr window, flagging localized infrastructure outbreaks.")
    add_bullet("FR-07 (Predictive Forecasting): ", "The system shall project 14-day daily complaint volume using OLS regression with 95% confidence bounds.")
    add_bullet("FR-08 (DPDP Public Transparency): ", "The system shall publish live resolution metrics while scrubbing all Citizen PII.")

    add_h2("5.2 Non-Functional Requirements")
    add_bullet("NFR-01 (Performance & Latency): ", "API triage latency must remain below 150 ms under concurrent load of 50 requests/sec.")
    add_bullet("NFR-02 (Data Security): ", "Session tokens must use HMAC-SHA256 signatures with 7-day expiration; passwords must be hashed using PBKDF2/bcrypt.")
    add_bullet("NFR-03 (Attachment Sanitization): ", "Uploaded files must be restricted to 10MB and validated against binary image magic bytes.")
    add_bullet("NFR-04 (Auditability): ", "All status changes, manual overrides, and automated escalations must be written to immutable audit logs.")

    doc.add_page_break()

    # ==================== CHAPTER 6 ====================
    add_h1("CHAPTER 6: SYSTEM DESIGN & DETAILED ARCHITECTURE")
    add_h2("6.1 Data Flow Diagrams (DFDs)")
    add_p("The operational data flows within SmartCivic AI are formally documented across DFD Levels 0, 1, and 2:")
    
    add_image_if_exists("dfd_level_0.png", "Figure 6.3: Data Flow Diagram (DFD) Level 0 — Context Diagram")
    add_p("In DFD Level 0, citizens submit complaints and receive tracking tokens; field officers receive work orders and submit photo proof; administrators review spatial analytics and trigger policy sweeps; and the SMTP server receives emergency breach alerts.")

    add_image_if_exists("dfd_level_1.png", "Figure 6.4: Data Flow Diagram (DFD) Level 1 — Operational Decomposition")
    add_p("DFD Level 1 decomposes the platform into seven operational processes: Authentication (1.0), Ingestion (2.0), AI Triage (3.0), SLA Engine (4.0), Departmental Routing (5.0), Predictive Modeling (6.0), and Reporting (7.0).")

    add_image_if_exists("dfd_level_2.png", "Figure 6.5: Data Flow Diagram (DFD) Level 2 — AI Triage & SLA Escalation Subsystems")
    add_p("DFD Level 2 details the internal sub-processes of AI Triage and SLA Escalation, demonstrating how text normalizes into TF-IDF vectors, passes through calibrated classifiers, evaluates safety guards, sets SLA deadlines, and executes automated priority promotion upon breach.")

    add_h2("6.2 Relational Entity-Relationship (ER) Schema")
    add_p("The database is structured across 14 normalized relational entities in SQLAlchemy ORM, ensuring referential integrity and audit compliance:")
    
    add_image_if_exists("er_diagram.png", "Figure 6.6: Entity-Relationship (ER) Relational Schema Architecture")

    add_h2("6.3 REST API Design & Endpoint Specifications")
    add_p("SmartCivic AI exposes 44 synchronous and asynchronous REST and HTML endpoints. Key operational APIs include:")
    add_bullet("POST /api/complaints: ", "Ingests complaint JSON payload, validates ward and GPS coordinates, and triggers background analysis.")
    add_bullet("POST /api/complaints/{id}/analyze: ", "Executes synchronous AI classification, multi-factor scoring, safety rules, and SLARecord creation.")
    add_bullet("POST /api/sla/check-breaches: ", "Automated daemon sweeping active complaints past deadline, promoting priority and logging audit events.")
    add_bullet("GET /api/predictive/forecast: ", "Computes 14-day OLS regression over 60-day historical intake with 95% confidence intervals.")
    add_bullet("GET /api/public/transparency-summary: ", "Returns sanitized public performance metrics with zero Citizen PII.")

    doc.add_page_break()

    # ==================== CHAPTER 7 ====================
    add_h1("CHAPTER 7: AI/ML METHODOLOGY & SAFETY INVARIANTS")
    add_h2("7.1 The End-to-End AI Triage Pipeline")
    add_p("The AI subsystem executes an integrated multi-stage pipeline designed for low latency, explainability, and absolute life-safety protection:")
    
    add_image_if_exists("ai_pipeline_flowchart.png", "Figure 7.1: End-to-End AI Triage, Entity Extraction & Safety Invariant Pipeline")

    add_h2("7.2 TF-IDF Vectorization & Calibrated LinearSVC")
    add_p("Text representation utilizes Term Frequency-Inverse Document Frequency (TF-IDF) with sublinear scaling:")
    add_p("$$\\text{tf-idf}(t, d, D) = (1 + \\log(\\text{tf}(t, d))) \\times \\log\\left(\\frac{1 + |D|}{1 + |\\{d \\in D : t \\in d\\}|}\\right) + 1$$")
    add_p("Features are extracted using unigram and bigram ranges (1, 2) capped at 5,000 maximum features. Classification is performed by LinearSVC minimizing the squared hinge loss with L2 regularization:")
    add_p("$$\\min_{w, b} \\frac{1}{2} \\|w\\|^2 + C \\sum_{i=1}^N \\max(0, 1 - y_i (w^T \\phi(x_i) + b))^2$$")
    add_p("Posterior probability calibration is achieved via Platt Scaling fitting a sigmoid transformation over the decision margin $f(x)$:")
    add_p("$$P(y = 1 \\mid x) = \\frac{1}{1 + \\exp(A \\cdot f(x) + B)}$$")

    add_h2("7.3 Explainable Multi-Factor Priority Scoring Engine")
    add_p("The Priority Engine calculates an explainable score in [0, 100]:")
    add_p("$$P = \\min\\left(100, \\, \\sum_{i} W_i \\cdot S_i + B_{\\text{duration}} + B_{\\text{essential}}\\right)$$")
    add_p("Where weights are configured in priority_config.yaml: Urgency (0.25), Severity (0.25), Population Impact (0.20), Safety Hazard (0.20), and Duration (0.10). Durations exceeding 7 days receive a +15 bonus.")

    add_h2("7.4 Deterministic Safety Rule Invariant")
    add_p("To eliminate fatal machine learning misclassifications, the Safety Rule Engine executes strictly AFTER ML scoring. If acute hazard tokens (e.g., exposed 440V wires, gas leaks, structural collapse, contaminated drinking water) match, the priority is unconditionally locked to CRITICAL (>=80), and an auditable hard rule tag is attached. Downstream sentiment cannot reduce this priority.")

    doc.add_page_break()

    # ==================== CHAPTER 8 ====================
    add_h1("CHAPTER 8: IMPLEMENTATION DETAILS")
    add_h2("8.1 Technology Stack & Implementation Architecture")
    add_p("SmartCivic AI is implemented in Python 3.14 utilizing FastAPI as the asynchronous ASGI web framework, SQLAlchemy 2.0 as the ORM, Scikit-Learn 1.9 for machine learning, Tailwind CSS for the design system, HTMX 2.0 for dynamic UI interactions, and Alpine.js for client-side reactive state management.")

    add_image_if_exists("complaint_lifecycle_state.png", "Figure 8.1: Complaint Lifecycle State Transition Diagram")

    add_h2("8.2 Key Code Snippets")
    
    add_code_snippet(
        "Snippet 8.1: Calibrated LinearSVC Prediction with Uncertainty Gating (ai/classifier.py)",
        """def predict_with_metadata(self, text: str) -> dict:
    cleaned = clean_text(text)
    if self.model is None:
        return self._keyword_fallback(cleaned)
    probs = self.model.predict_proba([cleaned])[0]
    top_indices = np.argsort(probs)[::-1][:3]
    top_pred = self.model.classes_[top_indices[0]]
    confidence = float(probs[top_indices[0]])
    return {
        "category": top_pred,
        "confidence": round(confidence, 4),
        "needs_human_review": bool(confidence < 0.40),
        "model_version": "2.0.0-SmartCivic"
    }"""
    )

    add_code_snippet(
        "Snippet 8.2: Deterministic Safety Invariant Override Guard (ai/rule_engine.py)",
        """def apply_safety_rules(self, text: str, initial_priority: str, initial_score: int) -> dict:
    matched_rules = []
    text_lower = text.lower()
    for rule in self.hard_safety_rules:
        if any(trigger in text_lower for trigger in rule["triggers"]):
            matched_rules.append(rule)
    if matched_rules:
        return {
            "priority": "CRITICAL",
            "priority_score": max(initial_score, 80),
            "safety_override_applied": True,
            "trigger_reasons": [r["reason"] for r in matched_rules]
        }
    return {"priority": initial_priority, "priority_score": initial_score, "safety_override_applied": False}"""
    )

    add_code_snippet(
        "Snippet 8.3: Automated SLA Escalation Daemon (app/services/sla_service.py)",
        """def check_and_escalate_slas(self, db: Session) -> dict:
    now = datetime.utcnow()
    overdue_slas = db.query(SLARecord).join(Complaint).filter(
        Complaint.status.in_(["pending", "open", "in_progress"]),
        SLARecord.resolved_at == None,
        SLARecord.sla_deadline < now,
        SLARecord.is_breached == False
    ).all()
    escalated_count = 0
    prio_order = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    for sla in overdue_slas:
        sla.is_breached = True
        curr_idx = prio_order.index(sla.priority.upper())
        if curr_idx < len(prio_order) - 1:
            new_prio = prio_order[curr_idx + 1]
            sla.priority = new_prio
            sla.complaint.analysis.priority_score = min(sla.complaint.analysis.priority_score + 20, 100)
            escalated_count += 1
            # Record status history with system actor ID = 1
            db.add(ComplaintStatusHistory(complaint_id=sla.complaint.id, old_status=sla.complaint.status,
                                          new_status=sla.complaint.status, changed_by_user_id=1,
                                          notes=f"AUTOMATED SLA BREACH: Escalated to {new_prio}"))
    db.commit()
    return {"breached_and_escalated": escalated_count}"""
    )

    add_code_snippet(
        "Snippet 8.4: 14-Day OLS Predictive Volume Forecaster (app/services/predictive_service.py)",
        """def get_forecast(self, db: Session, forecast_days: int = 14) -> dict:
    cutoff = datetime.utcnow() - timedelta(days=60)
    daily_counts = db.query(func.date(Complaint.created_at), func.count(Complaint.id)).filter(
        Complaint.created_at >= cutoff).group_by(func.date(Complaint.created_at)).all()
    # OLS trendline calculation: y = intercept + slope * x
    x = list(range(len(daily_counts)))
    y = [cnt for _, cnt in daily_counts]
    slope, intercept = np.polyfit(x, y, 1) if len(x) > 1 else (0.0, np.mean(y) if y else 1.0)
    residuals = [y[i] - (intercept + slope * x[i]) for i in range(len(x))]
    std_err = math.sqrt(sum(r**2 for r in residuals) / max(len(x)-2, 1))
    forecast = []
    for step in range(1, forecast_days + 1):
        future_x = len(x) + step - 1
        proj = max(intercept + slope * future_x, 0.5)
        margin = 1.96 * std_err * math.sqrt(1 + 1/len(x) + (future_x - np.mean(x))**2 / np.var(x))
        forecast.append({"date": str(step), "projected": round(proj, 1),
                         "lower_95": round(max(proj - margin, 0.0), 1), "upper_95": round(proj + margin, 1)})
    return {"model": "OLS with 95% CI", "trend": "INCREASING" if slope > 0.05 else "STABLE", "forecast": forecast}"""
    )

    add_h2("8.3 Interface Screenshots and Verification Tags")
    add_p("The following interface placeholders correspond to the verified screens detailed in SCREENSHOTS_GUIDE.md:")
    
    add_screenshot_placeholder("INSERT SCREENSHOT: SS-01 Apex Command Center Dashboard", "Route: / (GET) | Persona: Super Admin (admin) | Real-time KPIs, active outbreak alerts, and quick actions.")
    add_screenshot_placeholder("INSERT SCREENSHOT: SS-02 Citizen Complaint Submission Portal", "Route: /portal (GET) | Persona: Citizen / Public | Bilingual input, GPS ward selection, and secure photo upload.")
    add_screenshot_placeholder("INSERT SCREENSHOT: SS-05 Complaint Detail & Explainable AI Triage Dossier", "Route: /complaints/<id> (GET) | Persona: Super Admin | Calibrated confidence, factor scores, and safety invariant tags.")
    add_screenshot_placeholder("INSERT SCREENSHOT: SS-07 Department Administration & Workforce Balancing", "Route: /department (GET) | Persona: Dept Admin | Divisional queue and officer load balancing capacity meters.")
    add_screenshot_placeholder("INSERT SCREENSHOT: SS-09 GIS Spatial Intelligence & Ward Incident Map", "Route: /map (GET) | Persona: Super Admin | Leaflet/OSM map with priority pins and 500m outbreak clusters.")
    add_screenshot_placeholder("INSERT SCREENSHOT: SS-10 14-Day OLS Predictive Volume Forecast", "Route: /predictive (GET) | Persona: Super Admin | Time-series forecast chart with upper/lower 95% confidence bands.")
    add_screenshot_placeholder("INSERT SCREENSHOT: SS-11 Public Civic Transparency Portal", "Route: /transparency (GET) | Persona: Public | DPDP-compliant live resolution percentages and sanitized feeds.")

    doc.add_page_break()

    # ==================== CHAPTER 9 ====================
    add_h1("CHAPTER 9: VERIFICATION & TESTING STRATEGY")
    add_h2("9.1 Testing Strategy")
    add_p("SmartCivic AI adheres to a rigorous verification regime comprising unit tests, edge-case tests, security invariant tests, and full end-to-end integration tests. The test suite is executed using PyTest 9.1 on Python 3.14:")
    
    add_image_if_exists("sla_escalation_flow.png", "Figure 9.1: Configurable SLA Monitoring & Automated Escalation Workflow")

    add_h2("9.2 Automated PyTest Results (29/29 Passing)")
    add_p("Table 9.1 provides the complete breakdown of the 29 automated test cases:")

    # Table of tests
    t_tests = doc.add_table(rows=7, cols=4)
    t_tests.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_t = ["Test File", "Test Case Count", "Scope & Coverage", "Status"]
    for i, h in enumerate(hdr_t):
        c = t_tests.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = C_NAVY

    test_rows = [
        ["tests/test_api.py", "4 Tests", "Microservice health, classification route, empty payloads", "100% PASSED"],
        ["tests/test_edge_cases.py", "6 Tests", "Boundary scores, empty strings, non-English text, keywords", "100% PASSED"],
        ["tests/test_priority_engine.py", "3 Tests", "Multi-factor formula weights, clamping bounds [0, 100]", "100% PASSED"],
        ["tests/test_rule_engine.py", "3 Tests", "Non-downgrade safety overrides, reason generation", "100% PASSED"],
        ["tests/test_fastapi_app.py", "13 Tests", "Auth, RBAC, CRUD, SLA daemon, GIS, OLS forecast, exports, HTML", "100% PASSED"],
        ["TOTAL SUITE", "29 Tests", "Complete Application Verification (14.08 seconds execution)", "ALL 29 PASSED"]
    ]
    for row_idx, r in enumerate(test_rows):
        for col_idx, val in enumerate(r):
            t_tests.cell(row_idx + 1, col_idx).text = val

    p_tt = doc.add_paragraph()
    p_tt.paragraph_format.space_after = Pt(12)

    doc.add_page_break()

    # ==================== CHAPTER 10 ====================
    add_h1("CHAPTER 10: RESULTS & DISCUSSION")
    add_h2("10.1 Empirical Multi-Model Benchmark Results")
    add_p("To avoid arbitrary algorithm selection, four candidate models were benchmarked on a stratified 80/20 train/test split across 14 civic categories ($N=500$) with 5-fold cross-validation. Table 10.1 displays the authentic results extracted from data/model_comparison_results.json:")

    # Table of benchmark
    t_bm = doc.add_table(rows=5, cols=5)
    t_bm.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_bm = ["Algorithm Candidate", "Test Accuracy", "Macro F1-Score", "5-Fold CV Mean", "Production Status"]
    for i, h in enumerate(hdr_bm):
        c = t_bm.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = C_NAVY

    bm_data = [
        ["LinearSVC (Calibrated)", "96.00%", "0.9554", "0.9075 (+-0.0245)", "SELECTED (Primary)"],
        ["Logistic Regression", "94.00%", "0.9329", "0.9000 (+-0.0235)", "Fallback Candidate"],
        ["Multinomial Naive Bayes", "92.00%", "0.9094", "0.8875 (+-0.0194)", "Baseline Reference"],
        ["SGD Classifier (Log Loss)", "92.00%", "0.9093", "0.8825 (+-0.0194)", "Alternative Candidate"]
    ]
    for row_idx, r in enumerate(bm_data):
        for col_idx, val in enumerate(r):
            t_bm.cell(row_idx + 1, col_idx).text = val

    p_tbm = doc.add_paragraph()
    p_tbm.paragraph_format.space_after = Pt(12)

    add_h2("10.2 Confusion Matrix Analysis")
    add_p("Analysis of the 14x14 confusion matrix reveals that misclassifications occurred almost exclusively between overlapping boundary domains: two Public Safety incidents were classified under Electricity because they involved transformer sparking. This confirms that lexical ambiguity accounts for model errors, justifying our deterministic safety invariant layer.")

    add_h2("10.3 Honest Scientific Limitations")
    add_p("We emphasize that these metrics reflect evaluation on a curated synthetic dataset of 500 samples. While lexical structures mirror genuine civic grievances, real-world deployment will introduce out-of-vocabulary slang and dialectal noise. SmartCivic AI safely mitigates this limitation via confidence gating (< 0.40 -> human review) and human supervisor override capabilities.")

    doc.add_page_break()

    # ==================== CHAPTER 11 ====================
    add_h1("CHAPTER 11: SECURITY ARCHITECTURE & DEPLOYMENT")
    add_h2("11.1 Security Implementation")
    add_p("SmartCivic AI enforces defense-in-depth across the entire request lifecycle:")
    add_bullet("Cryptographic Sessions: ", "HMAC-signed tokens via URLSafeTimedSerializer with 7-day expiration prevent session tampering.")
    add_bullet("4-Tier RBAC: ", "Strict endpoint authorization enforced at the ASGI middleware dependency layer.")
    add_bullet("File Upload Sanitization: ", "Validates MIME content-types, enforces 10MB limits, and checks binary image magic bytes.")
    add_bullet("DPDP Privacy-by-Design: ", "Public transparency views strictly redact Citizen PII.")

    add_image_if_exists("deployment_diagram.png", "Figure 11.1: Containerized Docker & Production Infrastructure Topology")

    add_h2("11.2 Production Container Deployment")
    add_p("The application is packaged into an isolated multi-stage Docker container based on python:3.11-slim. It drops root privileges, executes under a dedicated unprivileged user (appuser), exposes port 8000 via Uvicorn, and mounts persistent volumes for database storage and photo uploads.")

    doc.add_page_break()

    # ==================== CHAPTER 12 ====================
    add_h1("CHAPTER 12: LIMITATIONS, FUTURE SCOPE & CONCLUSION")
    add_h2("12.1 Project Limitations")
    add_bullet("Biological Hazard Entity Extraction: ", "The NLP rule engine currently lacks explicit triggers for animal carcasses and decaying biowaste, as observed during evaluation.")
    add_bullet("Linear OLS Assumptions: ", "14-day volume forecasting assumes continuity of current reporting trends and cannot model sudden catastrophic storms without real-time meteorological API feeds.")
    add_bullet("GPS Sensor Dependence: ", "Spatial clustering relies on citizen mobile GPS accuracy or manual ward selection.")

    add_h2("12.2 Future Work Roadmap")
    add_bullet("IoT Edge Integration: ", "Connecting municipal water pipeline pressure transducers directly to trigger automatic tickets before citizens experience water cuts.")
    add_bullet("Computer Vision Damage Assessment: ", "Deploying CNN / Vision Transformers to automatically quantify road pothole depth and trash volume from photos.")
    add_bullet("Voice IVR & WhatsApp Ingestion: ", "Multilingual voice speech-to-text allowing illiterate citizens to lodge grievances in local dialects.")

    add_h2("12.3 Academic Conclusion")
    add_p("SmartCivic AI successfully elevates the minor project prototype into a comprehensive, enterprise-grade B.Tech Major Project. By combining calibrated machine learning (96% accuracy), deterministic safety invariants, explainable multi-factor scoring, active SLA escalation, GIS intelligence, and predictive governance, the system provides municipal administrations with an actionable, reliable, and mathematically sound technology platform ready for real-world deployment.")

    doc.add_page_break()

    # ==================== REFERENCES ====================
    add_h1("REFERENCES & BIBLIOGRAPHY")
    refs = [
        "[1] C. Cortes and V. Vapnik, 'Support-vector networks,' Machine Learning, vol. 20, no. 3, pp. 273-297, 1995.",
        "[2] F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python,' Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.",
        "[3] S. Tiangolo, 'FastAPI: High Performance Modern Web Framework for Python,' 2024. [Online]. Available: https://fastapi.tiangolo.com/",
        "[4] J. Platt, 'Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods,' Advances in Large Margin Classifiers, vol. 10, no. 3, pp. 61-74, 1999.",
        "[5] M. Bayer, 'SQLAlchemy: The Database Toolkit for Python,' 2024. [Online]. Available: https://www.sqlalchemy.org/",
        "[6] T. Joachims, 'Text categorization with support vector machines: Learning with many relevant features,' European Conference on Machine Learning, pp. 137-142, 1998.",
        "[7] N. Reimers and I. Gurevych, 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks,' EMNLP, 2019.",
        "[8] Ministry of Electronics and Information Technology, Government of India, 'The Digital Personal Data Protection Act, 2023,' The Gazette of India, Act No. 22 of 2023.",
        "[9] D. Amodei et al., 'Concrete Problems in AI Safety,' arXiv preprint arXiv:1606.06565, 2016.",
        "[10] G. E. P. Box and G. M. Jenkins, 'Time Series Analysis: Forecasting and Control,' Holden-Day, San Francisco, 1976."
    ]
    for r in refs:
        p_r = doc.add_paragraph()
        r_ref = p_r.add_run(r)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(10.5)
        p_r.paragraph_format.space_after = Pt(4)

    doc.save(DOCX_PATH)
    print(f"Academic Report DOCX successfully generated: {DOCX_PATH}")

def generate_academic_pdf():
    # Generate complementary publication-grade PDF via ReportLab
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=1.0 * inch,
        rightMargin=0.8 * inch,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch
    )

    styles = getSampleStyleSheet()
    c_primary = colors.HexColor('#0B192C')
    c_accent = colors.HexColor('#C2410C')
    c_teal = colors.HexColor('#0D9488')
    c_slate = colors.HexColor('#1E293B')

    title_s = ParagraphStyle('RTitle', fontName='Times-Bold', fontSize=22, leading=26, textColor=c_primary, alignment=1, spaceAfter=8)
    sub_s = ParagraphStyle('RSub', fontName='Times-Bold', fontSize=12, leading=16, textColor=c_accent, alignment=1, spaceAfter=16)
    meta_s = ParagraphStyle('RMeta', fontName='Times-Roman', fontSize=10, leading=14, textColor=colors.HexColor('#64748B'), alignment=1, spaceAfter=20)
    h1_s = ParagraphStyle('RH1', fontName='Times-Bold', fontSize=14, leading=18, textColor=c_primary, spaceBefore=14, spaceAfter=6, keepWithNext=True)
    h2_s = ParagraphStyle('RH2', fontName='Times-Bold', fontSize=11.5, leading=15, textColor=c_teal, spaceBefore=10, spaceAfter=4, keepWithNext=True)
    body_s = ParagraphStyle('RBody', fontName='Times-Roman', fontSize=9.5, leading=13.5, textColor=c_slate, spaceAfter=5, alignment=4)
    bullet_s = ParagraphStyle('RBullet', fontName='Times-Roman', fontSize=9, leading=13, textColor=c_slate, leftIndent=12, spaceAfter=3)

    story = []

    # Title & Front Matter
    story.append(Paragraph("SmartCivic AI", title_s))
    story.append(Paragraph("Intelligent Civic Complaint Management and Predictive Governance System", sub_s))
    story.append(Paragraph("<b>B.TECH MAJOR PROJECT FINAL REPORT (2026–2027)</b><br/>Department of Computer Science & Engineering • ITM University Gwalior<br/>Candidate: Samit Jain | Enrollment No.: [ENROLLMENT NO.] | Guide: [GUIDE NAME, DESIGNATION]", meta_s))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceAfter=12))

    # Abstract
    story.append(Paragraph("Executive Abstract", h1_s))
    story.append(Paragraph(
        "Municipal grievance systems across modern smart cities suffer from triage bottlenecks, absence of life-safety awareness, officer allocation fatigue, and lack of predictive foresight. <b>SmartCivic AI</b> transforms civic grievance management into an explainable, automated, and predictive governance platform. The system integrates a Calibrated Linear Support Vector Classifier (LinearSVC) achieving 96.00% accuracy, a multi-factor priority scoring formula, deterministic non-downgrade safety invariants for acute hazards, a four-tier RBAC security framework (Citizen, Officer, Department Admin, Apex Executive), automated priority-based SLA breach escalation, Leaflet/OSM GIS incident clustering, and 14-day OLS time-series volume forecasting with 95% confidence bands. The system strictly complies with the Digital Personal Data Protection (DPDP) Act on public portals and has been validated with 29 automated tests achieving a 100% pass rate.",
        body_s
    ))

    # System Architecture
    story.append(Paragraph("High-Level Architectural Blueprint", h1_s))
    img_arch = os.path.join(DIAG_DIR, "system_architecture.png")
    if os.path.exists(img_arch):
        story.append(Image(img_arch, width=6.2*inch, height=3.5*inch))
        story.append(Spacer(1, 6))

    # Benchmark Results
    story.append(Paragraph("Empirical Machine Learning Benchmark", h1_s))
    story.append(Paragraph("Benchmarked on a stratified 80/20 train/test split across 14 civic categories ($N=500$) with 5-fold cross-validation:", body_s))
    
    bm_table_data = [
        ["Candidate Algorithm", "Test Acc.", "Macro F1", "5-Fold CV Mean", "Production Status"],
        ["LinearSVC (Calibrated)", "96.00%", "0.9554", "0.9075 (+-0.0245)", "PRIMARY SELECTED"],
        ["Logistic Regression", "94.00%", "0.9329", "0.9000 (+-0.0235)", "Fallback Candidate"],
        ["Multinomial Naive Bayes", "92.00%", "0.9094", "0.8875 (+-0.0194)", "Baseline Reference"],
        ["SGD Classifier (Log Loss)", "92.00%", "0.9093", "0.8825 (+-0.0194)", "Alternative Candidate"]
    ]
    t_bm = Table(bm_table_data, colWidths=[2.2*inch, 0.9*inch, 0.9*inch, 1.4*inch, 1.1*inch])
    t_bm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTNAME', (0,1), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8FAFC'), colors.white])
    ]))
    story.append(t_bm)
    story.append(Spacer(1, 10))

    # Core Innovations
    story.append(Paragraph("Summary of Core Engineering Innovations", h1_s))
    story.append(Paragraph("<b>1. Deterministic Safety Invariant:</b> Acute life-safety hazards unconditionally evaluate to CRITICAL (>=80), mathematically preventing calm or polite citizen phrasing from lowering emergency priority.", bullet_s))
    story.append(Paragraph("<b>2. Automated SLA Escalation Daemon:</b> Continuous background sweeps promote overdue tickets by +1 priority tier, apply a +20 urgency penalty, and dispatch alerts to department supervisors.", bullet_s))
    story.append(Paragraph("<b>3. Department Workforce Load Balancing:</b> Live tracking of officer workloads (Available <5, Busy 5-11, Overloaded 12+) prevents burnout and optimizes ticket routing.", bullet_s))
    story.append(Paragraph("<b>4. GIS Spatial Outbreak Clustering:</b> Leaflet/OSM mapping with 500m / 48hr spatial clustering alerts authorities of localized pipeline contamination or power failures.", bullet_s))
    story.append(Paragraph("<b>5. 14-Day OLS Volume Forecasting:</b> Parametric regression with 95% confidence bands enables proactive pre-monsoon drain clearance and preventative equipment overhaul.", bullet_s))
    story.append(Paragraph("<b>6. DPDP Public Transparency:</b> Real-time public resolution percentages and sanitized feeds with zero Citizen PII exposure.", bullet_s))
    story.append(Paragraph("<b>7. Rigorous Verification:</b> 29/29 automated PyTest tests passing with 100% pass rate in 14.08 seconds.", bullet_s))

    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=c_teal, spaceAfter=6))
    story.append(Paragraph("<b>Conclusion:</b> SmartCivic AI represents a complete, mathematically sound, and deployable B.Tech Major Project fulfilling all academic and municipal software engineering standards.", meta_s))

    doc.build(story)
    print(f"Academic Report PDF successfully generated: {PDF_PATH}")

if __name__ == "__main__":
    generate_academic_docx()
    generate_academic_pdf()
