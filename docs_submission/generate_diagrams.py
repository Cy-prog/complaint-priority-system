import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DIAG_DIR = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(DIAG_DIR, exist_ok=True)

# ==============================================================================
# 1. WRITE MERMAID (.mmd) FILES
# ==============================================================================

MMD_FILES = {
    "system_architecture.mmd": """flowchart TD
    subgraph PresentationLayer ["Presentation Layer (Jinja2 + HTMX + Tailwind + Leaflet)"]
        CP["Citizen Portal (/portal)"]
        AC["Apex Command Hub (/)"]
        DW["Dept Workspace (/department)"]
        OW["Officer Queue (/officer)"]
        GM["GIS Map (/map)"]
        PD["Predictive Dashboard (/predictive)"]
        TP["Public Transparency (/transparency)"]
    end

    subgraph SecurityLayer ["Security & Middleware Layer"]
        AUTH["Timed Sessions (URLSafeTimedSerializer)"]
        RBAC["4-Tier RBAC Enforcement"]
        VAL["Secure Upload Validator (Magic Bytes & MIME)"]
    end

    subgraph CoreServices ["Application & Core Services"]
        API["FastAPI ASGI REST API"]
        SLA["SLA Escalation Daemon"]
        WLB["Workforce Load Balancer"]
        NOTIF["Notification Center (In-App + SMTP)"]
        REP["Reporting Suite (CSV, Excel, PyMuPDF)"]
    end

    subgraph AISubsystem ["AI / ML Intelligence Subsystem"]
        VEC["TF-IDF Vectorizer (1-2 N-grams)"]
        SVC["Calibrated LinearSVC (96% Accuracy)"]
        EXT["Entity & Hazard Extractor"]
        PRIO["Multi-Factor Priority Scoring (0-100)"]
        RULE["Deterministic Safety Invariant Guard"]
        OLS["14-Day OLS Volume Forecaster (95% CI)"]
        SIM["SentenceTransformer Duplicate Detection"]
    end

    subgraph PersistenceLayer ["Persistence Layer"]
        DB[("SQLAlchemy Relational ORM (14 Tables)")]
        AUDIT[("Transactional Immutable Audit Trail")]
    end

    PresentationLayer --> SecurityLayer
    SecurityLayer --> CoreServices
    CoreServices --> AISubsystem
    CoreServices --> PersistenceLayer
""",

    "use_case.mmd": """flowchart LR
    Citizen((Citizen))
    Officer((Field Officer))
    DeptAdmin((Dept Admin))
    SuperAdmin((Super Admin))

    subgraph SmartCivicSystem ["SmartCivic AI Grievance System"]
        UC1["Submit Grievance & Evidence"]
        UC2["Track Status via Token"]
        UC3["Verify Resolution & Reopen"]
        UC4["View Public Transparency"]
        UC5["Inspect Assigned Queue"]
        UC6["Update Field Status & Upload Proof"]
        UC7["Manage Divisional Workload"]
        UC8["Reassign Field Officers"]
        UC9["Apex Command Overview"]
        UC10["Trigger SLA Escalation Sweeps"]
        UC11["Analyze 14-Day Predictive Forecast"]
        UC12["Export CSV / Excel / PDF Dossiers"]
    end

    Citizen --> UC1
    Citizen --> UC2
    Citizen --> UC3
    Citizen --> UC4

    Officer --> UC5
    Officer --> UC6
    Officer --> UC2

    DeptAdmin --> UC7
    DeptAdmin --> UC8
    DeptAdmin --> UC12

    SuperAdmin --> UC9
    SuperAdmin --> UC10
    SuperAdmin --> UC11
    SuperAdmin --> UC12
""",

    "dfd_level_0.mmd": """flowchart TD
    Citizen["Citizen User"]
    Officer["Field Officer"]
    Admin["Municipal Administrator"]
    SMTP["SMTP Mail Server"]

    SC["0.0\\nSmartCivic AI System\\n(Intelligent Municipal Platform)"]

    Citizen -->|"Grievance Text, Location, Photo"| SC
    SC -->|"Tracking Token, Live Status, Resolution Proof"| Citizen

    SC -->|"Assigned Task Details, SLA Deadlines"| Officer
    Officer -->|"Field Status Update, Resolution Evidence"| Officer

    Admin -->|"Manual Reassignment, System Policies"| SC
    SC -->|"GIS Analytics, 14-Day Forecast, Dossiers"| Admin

    SC -->|"Emergency SLA Breach Alerts"| SMTP
""",

    "dfd_level_1.mmd": """flowchart TD
    User["User / Citizen"] --> P1["1.0 Authentication & Session Control"]
    P1 --> D1[("D1 Users Store")]
    
    User --> P2["2.0 Grievance Ingestion & Upload Validation"]
    P2 --> D2[("D2 Complaints Store")]
    
    P2 --> P3["3.0 AI Triage & Safety Scoring Engine"]
    P3 --> D3[("D3 AI Analysis Store")]
    
    P3 --> P4["4.0 SLA Deadline Engine & Escalation"]
    P4 --> D4[("D4 SLA Records")]
    
    P4 --> P5["5.0 Departmental Routing & Load Balancer"]
    P5 --> D1
    
    D2 --> P6["6.0 Predictive Modeling & GIS Clustering"]
    P6 --> Out1["GIS Hotspot Map"]
    P6 --> Out2["14-Day OLS Volume Forecast"]
    
    D2 --> P7["7.0 Reporting & Transparency Engine"]
    P7 --> Out3["Public Portal (DPDP Safe)"]
    P7 --> Out4["CSV / Excel / PDF Dossiers"]
    
    P4 --> D5[("D5 Audit Trail")]
    P4 --> D6[("D6 Notifications")]
""",

    "dfd_level_2.mmd": """flowchart TD
    Input["Raw Complaint Text"] --> P31["3.1 Preprocessing & Language Detection"]
    P31 --> P32["3.2 TF-IDF & LinearSVC Classification"]
    P31 --> P33["3.3 Entity, Landmark & Hazard Extraction"]
    P31 --> P34["3.4 VADER Sentiment Polarity"]
    
    P32 & P33 & P34 --> P35["3.5 Multi-Factor Priority Score Formulation (0-100)"]
    P35 --> P36["3.6 Deterministic Safety Invariant Override Guard"]
    
    P36 --> Decision{"Acute Hazard\\nTriggered?"}
    Decision -->|"Yes (Gas/Wire/Fire)"| Escalate["Force Priority = CRITICAL\\nScore >= 80\\nLog Reason Tag"]
    Decision -->|"No"| ConfGate["3.7 Confidence Evaluation"]
    
    Escalate --> StoreAnalysis[("Store complaint_analysis")]
    ConfGate -->|"Confidence < 0.40"| FlagReview["Flag needs_human_review = True"]
    ConfGate -->|"Confidence >= 0.40"| StoreAnalysis
    FlagReview --> StoreAnalysis

    subgraph SLAEngine ["SLA Escalation Subsystem (4.0)"]
        StoreAnalysis --> P41["4.1 Initialize SLARecord Deadline"]
        P41 --> P42["4.2 Background Escalation Sweep Daemon"]
        P42 --> P43{"Deadline\\nBreached?"}
        P43 -->|"Yes & Unresolved"| P44["Promote Priority +1 Tier\\nAdd +20 Urgency Penalty\\nSet is_breached = True"]
        P44 --> P45["Dispatch High-Priority In-App & SMTP Alerts"]
        P44 --> P46[("Record Status History & Audit Log")]
        P43 -->|"No"| P47["Maintain Standard Queue"]
    end
""",

    "er_diagram.mmd": """erDiagram
    USERS ||--o{ COMPLAINTS : "creates / assigned_to"
    USERS ||--o{ PRIORITY_OVERRIDES : "authorizes"
    USERS ||--o{ COMPLAINT_STATUS_HISTORY : "triggers"
    USERS ||--o{ COMPLAINT_FEEDBACK : "submits"
    USERS ||--o{ NOTIFICATIONS : "receives"
    USERS ||--o{ AUDIT_LOGS : "acts_in"
    DEPARTMENTS ||--o{ USERS : "employs"
    DEPARTMENTS ||--o{ CATEGORIES : "manages"
    DEPARTMENTS ||--o{ COMPLAINTS : "assigned_department"
    CATEGORIES ||--o{ COMPLAINTS : "classifies"
    COMPLAINTS ||--|| COMPLAINT_ANALYSIS : "triaged_by"
    COMPLAINTS ||--|| SLA_RECORDS : "governed_by"
    COMPLAINTS ||--o{ PRIORITY_OVERRIDES : "overridden_by"
    COMPLAINTS ||--o{ COMPLAINT_STATUS_HISTORY : "tracks_history"
    COMPLAINTS ||--o{ COMPLAINT_FEEDBACK : "receives_feedback"
    COMPLAINTS ||--o{ SIMILAR_COMPLAINTS : "matched_with"
    INCIDENTS ||--o{ INCIDENT_COMPLAINTS : "aggregates"
    COMPLAINTS ||--o{ INCIDENT_COMPLAINTS : "belongs_to"

    USERS {
        int id PK
        string username
        string email
        string password_hash
        string role
        string phone
        int department_id FK
    }
    DEPARTMENTS {
        int id PK
        string name
        string contact_email
    }
    CATEGORIES {
        int id PK
        string name
        string risk_level
        boolean is_essential_service
        int department_id FK
    }
    COMPLAINTS {
        int id PK
        string complaint_id UK
        text complaint_text
        string status
        string ward
        float latitude
        float longitude
        int category_id FK
        int assigned_department_id FK
        int assigned_user_id FK
        int created_by_user_id FK
        string evidence_photo
        string resolution_photo
    }
    COMPLAINT_ANALYSIS {
        int id PK
        int complaint_id FK
        string priority
        int priority_score
        float confidence
        json entities
        text reasoning_summary
    }
    SLA_RECORDS {
        int id PK
        int complaint_id FK
        string priority
        datetime sla_deadline
        boolean is_breached
    }
""",

    "ai_pipeline_flowchart.mmd": """flowchart TD
    A["Raw Grievance Submission"] --> B["Language Normalizer (Hindi / English)"]
    B --> C["TF-IDF Vectorizer (1-2 N-grams)"]
    C --> D["Calibrated LinearSVC Classifier"]
    D --> E["Posterior Probability Confidence Estimation"]
    
    B --> F["Entity, Landmark & Risk Extractor"]
    F --> G["Duration & Population Extraction"]
    
    B --> H["VADER Lexicon Sentiment Analyzer"]
    
    D & F & G & H --> I["Multi-Factor Priority Scoring Engine"]
    I --> J["Compute Raw Score [0-100]"]
    
    J --> K["Deterministic Safety Invariant Guard"]
    K --> L{"Acute Life Safety\\nHazard Detected?"}
    
    L -->|"YES (Gas leak, wire, collapse)"| M["Force Priority = CRITICAL\\nScore = max(Score, 80)\\nAppend Hard Rule Audit Tag"]
    L -->|"NO"| N["Assign Score Tier\\n(CRITICAL >=80, HIGH >=60, MED >=35, LOW <35)"]
    
    M --> O["Confidence Gate Check"]
    N --> O
    
    O --> P{"Confidence < 0.40?"}
    P -->|"YES"| Q["Flag: needs_human_review = True"]
    P -->|"NO"| R["Direct Pipeline Dispatch"]
    
    Q --> S["SentenceTransformer Duplicate Detection"]
    R --> S
    S --> T["Structured Decision Explanation & Audit Record"]
""",

    "complaint_lifecycle_state.mmd": """stateDiagram-v2
    [*] --> Submitted : Citizen lodges complaint via /portal or API
    Submitted --> Analyzed : AI Pipeline executes (Category, Score, Safety Rule)
    Analyzed --> Assigned : Load Balancer routes to Dept & Field Officer
    Assigned --> In_Progress : Field Officer acknowledges & begins work
    In_Progress --> Resolved : Officer resolves issue & uploads photo evidence
    Resolved --> Closed : Citizen verifies resolution & marks Satisfied
    Resolved --> Reopened : Citizen rejects resolution (reopen_count++)
    Reopened --> In_Progress : Priority escalated for expedited supervisor action
    Closed --> [*]
""",

    "sla_escalation_flow.mmd": """flowchart TD
    Start["Ticket Assigned with Priority"] --> Init["Calculate SLA Deadline (SLARecord)"]
    Init --> Timer["SLA Countdown Active (e.g. Critical=6h, High=24h)"]
    Timer --> Sweep["Automated Escalation Daemon Sweep (/api/sla/check-breaches)"]
    
    Sweep --> CheckResolved{"Is Complaint\\nResolved?"}
    CheckResolved -->|"Yes"| RecordSuccess["Calculate Resolution Latency & Compliance Rate"]
    CheckResolved -->|"No"| CheckDeadline{"Has sla_deadline\\nPassed?"}
    
    CheckDeadline -->|"No"| ContinueCountdown["Maintain Standard Active Monitoring"]
    CheckDeadline -->|"Yes"| TriggerBreach["Flag is_breached = True"]
    
    TriggerBreach --> CheckLevel{"Current Priority < CRITICAL?"}
    CheckLevel -->|"Yes"| PromotePriority["Promote Priority +1 Tier (e.g. HIGH -> CRITICAL)\\nAdd +20 Urgency Score Penalty"]
    CheckLevel -->|"Already CRITICAL"| MaxUrgency["Maintain CRITICAL\\nFlag Overdue Emergency Status"]
    
    PromotePriority --> Alert["Dispatch High-Priority In-App & SMTP Alerts"]
    MaxUrgency --> Alert
    Alert --> Log["Append Immutable Entry in complaint_status_history & audit_logs"]
    Log --> End["Supervisor Real-Time Notification"]
""",

    "deployment_diagram.mmd": """flowchart TD
    subgraph ClientNodes ["Client Devices"]
        CB["Citizen Web Browser / Mobile Device"]
        OB["Field Officer Mobile Portal"]
        AB["Administrator Command Workstation"]
    end

    subgraph EdgeRouting ["Edge & Network Routing"]
        RP["Reverse Proxy / Nginx / Cloudflare (TLS 443 Termination)"]
    end

    subgraph ApplicationHost ["Docker Application Container"]
        ASGI["Uvicorn ASGI High-Concurrency Server"]
        FASTAPI["FastAPI 0.136.1 Web & REST Subsystem"]
        AILIB["Scikit-Learn 1.9.0 / LinearSVC Model"]
        ORM["SQLAlchemy 2.0.52 ORM Engine"]
    end

    subgraph StorageSubsystem ["Persistent Storage Volumes"]
        SQLDB[("SQLite database (data/complaints.db) / PostgreSQL 15")]
        MEDIA[("Static Uploads Directory (/uploads)")]
    end

    subgraph ExternalServices ["External Infrastructure"]
        SMTP_SERVER["Municipal SMTP Email Server"]
        OSM_TILES["OpenStreetMap CDN Tile Servers"]
    end

    ClientNodes -->|"HTTPS / WSS"| EdgeRouting
    EdgeRouting -->|"Port 8000"| ApplicationHost
    FASTAPI --> ORM
    FASTAPI --> AILIB
    ORM --> SQLDB
    FASTAPI --> MEDIA
    FASTAPI -->|"TLS / SMTP (587)"| SMTP_SERVER
    ClientNodes -->|"Direct Tile Fetch"| OSM_TILES
"""
}

for name, content in MMD_FILES.items():
    path = os.path.join(DIAG_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved: {path}")

# ==============================================================================
# 2. RENDER PUBLICATION-QUALITY PNG DIAGRAMS VIA MATPLOTLIB
# ==============================================================================

# Palette
DARK_NAVY = '#0B192C'
CARD_BG   = '#1E293B'
ACCENT    = '#F97316'
TEAL      = '#10B981'
INDIGO    = '#6366F1'
LIGHT_TXT = '#F8FAFC'
BORDER_C  = '#334155'

def draw_rounded_box(ax, x, y, w, h, title, bullets, color=TEAL, title_size=10, body_size=8):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                 linewidth=1.2, edgecolor=color, facecolor=CARD_BG)
    ax.add_patch(box)
    ax.text(x + w*0.05, y + h - 0.08, title, fontsize=title_size, fontweight='bold', color=color, va='top')
    offset_y = 0.18
    for b in bullets:
        ax.text(x + w*0.05, y + h - offset_y, f"• {b}", fontsize=body_size, color=LIGHT_TXT, va='top', wrap=True)
        offset_y += 0.07

def create_system_architecture_png(filename):
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=DARK_NAVY)
    ax.set_facecolor(DARK_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.title("SmartCivic AI — High-Level Layered System Architecture", fontsize=16, fontweight='bold', color=LIGHT_TXT, pad=15)

    # 4 Main horizontal layers
    draw_rounded_box(ax, 0.05, 0.76, 0.90, 0.18, "1. Presentation Layer (Jinja2 + HTMX + Alpine.js + Tailwind CSS)", 
                     ["Citizen Portal (/portal)", "Apex Command Center (/)", "Department Workspace (/department)", "Field Queue (/officer)", "GIS Map (/map)"], color=ACCENT)
    
    draw_rounded_box(ax, 0.05, 0.52, 0.90, 0.20, "2. Security & Application Core (FastAPI ASGI)", 
                     ["Cryptographic Timed Sessions (URLSafeTimedSerializer)", "4-Tier RBAC (Citizen, Officer, Dept Admin, Super Admin)", "Secure File Upload Guard (MIME & Magic Bytes)", "Automated SLA Escalation Daemon & Background Sweeps"], color=TEAL)

    draw_rounded_box(ax, 0.05, 0.28, 0.90, 0.20, "3. AI / ML & Predictive Governance Subsystem", 
                     ["TF-IDF Vectorizer + Calibrated LinearSVC (96% Accuracy)", "Deterministic Safety Invariant Guard (Non-Downgrade Invariant)", "Multi-Factor Priority Scoring Engine (0-100)", "14-Day OLS Volume Forecaster (95% CI) & Outbreak Clustering"], color=INDIGO)

    draw_rounded_box(ax, 0.05, 0.05, 0.90, 0.19, "4. Persistence & Audit Layer", 
                     ["SQLAlchemy Relational ORM across 14 Normalized Tables", "Cross-Engine Compatibility: SQLite (Dev) & PostgreSQL (Prod)", "Immutable Transactional Audit Logs capturing all human overrides & system actions"], color=ACCENT)

    # Connecting arrows
    for y_pos in [0.75, 0.51, 0.27]:
        ax.annotate('', xy=(0.5, y_pos - 0.03), xytext=(0.5, y_pos + 0.01),
                    arrowprops=dict(facecolor=ACCENT, edgecolor=ACCENT, width=1.5, headwidth=6))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, facecolor=DARK_NAVY)
    plt.close()
    print(f"Rendered: {filename}")

def create_er_diagram_png(filename):
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=DARK_NAVY)
    ax.set_facecolor(DARK_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.title("SmartCivic AI — Entity-Relationship (ER) Schema Overview", fontsize=16, fontweight='bold', color=LIGHT_TXT, pad=15)

    entities = [
        ("USERS (PK: id)", ["username, email, password_hash", "role (4 tiers), phone", "FK: department_id"], 0.05, 0.65, TEAL),
        ("DEPARTMENTS (PK: id)", ["name, description", "contact_email, is_active"], 0.05, 0.35, ACCENT),
        ("CATEGORIES (PK: id)", ["name, risk_level", "is_essential_service", "FK: department_id"], 0.05, 0.05, INDIGO),
        ("COMPLAINTS (PK: id)", ["complaint_id (UK), text", "ward, lat, lng, status", "FK: category_id, assigned_dept", "FK: assigned_user, created_by", "evidence_photo, resolution_photo"], 0.38, 0.35, ACCENT),
        ("COMPLAINT_ANALYSIS (PK: id)", ["FK: complaint_id", "priority, priority_score (0-100)", "confidence, sentiment, risk_level", "entities (JSON), reasoning_summary"], 0.70, 0.65, TEAL),
        ("SLA_RECORDS (PK: id)", ["FK: complaint_id", "priority, sla_deadline", "is_breached, response_at, resolved_at"], 0.70, 0.38, INDIGO),
        ("AUDIT_LOGS & NOTIFICATIONS", ["FK: user_id, action", "old_value, new_value, timestamps", "in-app unread tracking & email"], 0.70, 0.08, ACCENT)
    ]

    for title, fields, x, y, color in entities:
        draw_rounded_box(ax, x, y, 0.26, 0.24, title, fields, color=color, title_size=9, body_size=7.5)

    # Connections
    ax.annotate('', xy=(0.38, 0.47), xytext=(0.31, 0.75), arrowprops=dict(facecolor=TEAL, edgecolor=TEAL, width=1, headwidth=4))
    ax.annotate('', xy=(0.38, 0.47), xytext=(0.31, 0.47), arrowprops=dict(facecolor=ACCENT, edgecolor=ACCENT, width=1, headwidth=4))
    ax.annotate('', xy=(0.38, 0.47), xytext=(0.31, 0.17), arrowprops=dict(facecolor=INDIGO, edgecolor=INDIGO, width=1, headwidth=4))
    ax.annotate('', xy=(0.70, 0.77), xytext=(0.64, 0.47), arrowprops=dict(facecolor=TEAL, edgecolor=TEAL, width=1, headwidth=4))
    ax.annotate('', xy=(0.70, 0.47), xytext=(0.64, 0.47), arrowprops=dict(facecolor=INDIGO, edgecolor=INDIGO, width=1, headwidth=4))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, facecolor=DARK_NAVY)
    plt.close()
    print(f"Rendered: {filename}")

def create_ai_pipeline_png(filename):
    fig, ax = plt.subplots(figsize=(14, 8), facecolor=DARK_NAVY)
    ax.set_facecolor(DARK_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.title("SmartCivic AI — Machine Learning Triage & Safety Invariant Pipeline", fontsize=15, fontweight='bold', color=LIGHT_TXT, pad=15)

    boxes = [
        ("1. Input Grievance", ["Citizen submission (Text & Location)", "Hindi / English language detection"], 0.04, 0.40, TEAL),
        ("2. ML Classification", ["TF-IDF (1-2 N-grams, max=5000)", "Calibrated LinearSVC (96% Acc)", "Posterior Class Probabilities"], 0.23, 0.65, INDIGO),
        ("3. Entity & Hazard Extraction", ["Hospitals, schools, duration indicators", "Vehicle details for hit-and-run", "VADER sentiment polarity"], 0.23, 0.15, INDIGO),
        ("4. Multi-Factor Scoring", ["Score = W_urg*Urg + W_sev*Sev + ...", "Continuous range: [0, 100]", "Duration & essential service bonus"], 0.45, 0.40, ACCENT),
        ("5. Deterministic Safety Guard", ["HARD NON-DOWNGRADE INVARIANT", "Acute risk -> Unconditional CRITICAL (>=80)", "Prevents calm phrasing from masking danger"], 0.67, 0.40, '#EF4444'),
        ("6. Confidence & Explanation", ["Uncertainty check (< 0.40 -> Human Review)", "SentenceTransformers Duplicate Match", "Complete factor breakdown recorded"], 0.86, 0.40, TEAL)
    ]

    for title, bullets, x, y, color in boxes:
        draw_rounded_box(ax, x, y, 0.18, 0.26, title, bullets, color=color, title_size=8.5, body_size=7)

    # Connections
    ax.annotate('', xy=(0.23, 0.78), xytext=(0.22, 0.53), arrowprops=dict(facecolor=LIGHT_TXT, edgecolor=LIGHT_TXT, width=1, headwidth=4))
    ax.annotate('', xy=(0.23, 0.28), xytext=(0.22, 0.53), arrowprops=dict(facecolor=LIGHT_TXT, edgecolor=LIGHT_TXT, width=1, headwidth=4))
    ax.annotate('', xy=(0.45, 0.53), xytext=(0.41, 0.78), arrowprops=dict(facecolor=LIGHT_TXT, edgecolor=LIGHT_TXT, width=1, headwidth=4))
    ax.annotate('', xy=(0.45, 0.53), xytext=(0.41, 0.28), arrowprops=dict(facecolor=LIGHT_TXT, edgecolor=LIGHT_TXT, width=1, headwidth=4))
    ax.annotate('', xy=(0.67, 0.53), xytext=(0.63, 0.53), arrowprops=dict(facecolor=LIGHT_TXT, edgecolor=LIGHT_TXT, width=1, headwidth=4))
    ax.annotate('', xy=(0.86, 0.53), xytext=(0.85, 0.53), arrowprops=dict(facecolor=LIGHT_TXT, edgecolor=LIGHT_TXT, width=1, headwidth=4))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, facecolor=DARK_NAVY)
    plt.close()
    print(f"Rendered: {filename}")

def create_generic_flowchart_png(filename, title_text, steps):
    fig, ax = plt.subplots(figsize=(14, 7), facecolor=DARK_NAVY)
    ax.set_facecolor(DARK_NAVY)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.title(title_text, fontsize=15, fontweight='bold', color=LIGHT_TXT, pad=15)

    n = len(steps)
    step_w = 0.85 / n
    for i, (stitle, sbullets, scolor) in enumerate(steps):
        x = 0.06 + i * step_w
        draw_rounded_box(ax, x, 0.30, step_w - 0.02, 0.45, stitle, sbullets, color=scolor, title_size=9, body_size=7.5)
        if i < n - 1:
            ax.annotate('', xy=(x + step_w, 0.52), xytext=(x + step_w - 0.02, 0.52),
                        arrowprops=dict(facecolor=ACCENT, edgecolor=ACCENT, width=1.5, headwidth=5))

    plt.tight_layout()
    plt.savefig(filename, dpi=300, facecolor=DARK_NAVY)
    plt.close()
    print(f"Rendered: {filename}")

# Generate all PNGs
create_system_architecture_png(os.path.join(DIAG_DIR, "system_architecture.png"))
create_er_diagram_png(os.path.join(DIAG_DIR, "er_diagram.png"))
create_ai_pipeline_png(os.path.join(DIAG_DIR, "ai_pipeline_flowchart.png"))

# Use Case Diagram
create_generic_flowchart_png(
    os.path.join(DIAG_DIR, "use_case.png"),
    "SmartCivic AI — 4-Tier Role-Based Use Case Flows",
    [
        ("Citizen", ["Register / Login", "Lodge Complaint + Photo", "Track via Tracking Token", "Submit Feedback / Reopen"], TEAL),
        ("Field Officer", ["View Assigned Ward Queue", "Update Status to In-Progress", "Upload Photo Resolution Proof", "View SLA Countdown"], INDIGO),
        ("Department Admin", ["Monitor Division Workload", "Inspect Officer Capacity", "AI-Balanced Reassignment", "Generate Department Report"], ACCENT),
        ("Super Admin", ["Apex Command Dashboard", "Trigger SLA Escalation Sweeps", "14-Day Predictive Forecast", "Export CSV / Excel / PDF"], '#EC4899')
    ]
)

# DFD Level 0
create_generic_flowchart_png(
    os.path.join(DIAG_DIR, "dfd_level_0.png"),
    "SmartCivic AI — DFD Level 0 (Context Diagram)",
    [
        ("Citizen User", ["Submits grievance text & photo", "Receives token & resolution proof"], TEAL),
        ("SmartCivic AI Core (0.0)", ["Central Ingestion & Triage", "SLA Monitoring & Routing Engine", "Predictive Analytics & Reports"], ACCENT),
        ("Municipal Staff", ["Inspects assigned complaints", "Updates field status & proof photo"], INDIGO),
        ("Apex & Public Portal", ["Publishes live DPDP metrics", "Sends SMTP emergency breach alerts"], TEAL)
    ]
)

# DFD Level 1
create_generic_flowchart_png(
    os.path.join(DIAG_DIR, "dfd_level_1.png"),
    "SmartCivic AI — DFD Level 1 (Operational Decomposition)",
    [
        ("1. Ingestion & Auth", ["Citizen registration & login", "Secure upload verification", "Store in D2 Complaints"], TEAL),
        ("2. AI Triage Pipeline", ["TF-IDF & LinearSVC model", "Multi-factor priority formula", "Safety rule invariant guard"], INDIGO),
        ("3. SLA & Workforce", ["SLA deadline monitoring", "Auto-escalation daemon", "Officer workload balancing"], ACCENT),
        ("4. Analytics & Output", ["14-day OLS volume forecast", "Leaflet GIS marker feeds", "DPDP-compliant public metrics"], TEAL)
    ]
)

# DFD Level 2
create_generic_flowchart_png(
    os.path.join(DIAG_DIR, "dfd_level_2.png"),
    "SmartCivic AI — DFD Level 2 (AI Triage & SLA Escalation Subsystems)",
    [
        ("3.1 Text Analysis", ["Language normalization", "TF-IDF (1-2 N-grams)", "Calibrated LinearSVC"], TEAL),
        ("3.2 Multi-Factor Scoring", ["Urgency, Severity, Impact", "Hazard index & Duration", "Deterministic override check"], INDIGO),
        ("4.1 SLA Monitoring", ["Set deadline by priority tier", "Real-time countdown timer", "Store in D4 sla_records"], ACCENT),
        ("4.2 Auto-Escalation", ["Breach detection sweep", "Promote priority (+1 tier)", "Dispatch alerts & audit log"], '#EF4444')
    ]
)

# Complaint Lifecycle
create_generic_flowchart_png(
    os.path.join(DIAG_DIR, "complaint_lifecycle_state.png"),
    "SmartCivic AI — Complaint Lifecycle State Transitions",
    [
        ("1. SUBMITTED", ["Grievance logged via portal", "Unique token generated", "Status: 'pending'"], TEAL),
        ("2. ANALYZED", ["Category & Priority scored", "Safety invariants verified", "Confidence calculated"], INDIGO),
        ("3. ASSIGNED", ["Routed to Department", "Assigned to Field Officer", "Status: 'open'"], ACCENT),
        ("4. IN PROGRESS", ["Officer field investigation", "On-site status update", "Status: 'in_progress'"], TEAL),
        ("5. RESOLVED", ["Resolution photo uploaded", "Status: 'resolved'", "Citizen feedback requested"], INDIGO),
        ("6. CLOSED / REOPEN", ["Satisfied -> 'closed'", "Dissatisfied -> 'reopened'", "Escalates priority if reopened"], ACCENT)
    ]
)

# SLA Escalation Flow
create_generic_flowchart_png(
    os.path.join(DIAG_DIR, "sla_escalation_flow.png"),
    "SmartCivic AI — SLA Deadline & Automated Escalation Workflow",
    [
        ("1. Deadline Setting", ["CRITICAL: 6 Hours", "HIGH: 24 Hours", "MEDIUM: 72 Hours", "LOW: 168 Hours (7 Days)"], TEAL),
        ("2. Active Monitoring", ["Real-time countdown timer", "Automated sweep daemon", "Checks is_breached flag"], INDIGO),
        ("3. Breach Detection", ["Unresolved past deadline", "Sets is_breached = True", "Calculates breach latency"], ACCENT),
        ("4. Automated Escalation", ["Promotes priority (+1 level)", "Adds +20 urgency penalty", "Sends SMTP & in-app alerts"], '#EF4444')
    ]
)

# Deployment Diagram
create_generic_flowchart_png(
    os.path.join(DIAG_DIR, "deployment_diagram.png"),
    "SmartCivic AI — Production Container & Infrastructure Topology",
    [
        ("Client Devices", ["Citizen Mobile & Web Browser", "Field Officer Portal", "Admin Command Terminal"], TEAL),
        ("Edge & Ingress", ["Reverse Proxy / Nginx", "TLS 443 Termination", "Static asset caching"], INDIGO),
        ("FastAPI Container", ["Uvicorn ASGI High-Concurrency", "FastAPI Application Core", "Scikit-Learn ML Model"], ACCENT),
        ("Storage & External", ["SQLite / PostgreSQL 15 DB", "Uploads Volume Storage", "Municipal SMTP Email Server"], TEAL)
    ]
)

print("All 10 Mermaid files and 10 PNG diagrams successfully generated!")
