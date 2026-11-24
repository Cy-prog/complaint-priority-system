import io
import csv
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
import fitz  # PyMuPDF
import xlsxwriter
from app.models import Complaint, Department, Category, SLARecord, ComplaintAnalysis

class ReportService:
    def export_csv(self, db: Session) -> str:
        """Exports sanitized municipal complaint registry as CSV."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        writer.writerow([
            "Complaint ID", "Date", "Status", "Priority", "Priority Score",
            "Category", "Department", "Ward", "Area", "SLA Status", "Reopen Count"
        ])
        
        complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
        for c in complaints:
            prio = c.analysis.priority if c.analysis else "UNASSIGNED"
            score = c.analysis.priority_score if c.analysis else 0
            cat_name = c.category.name if c.category else "General"
            dept_name = c.assigned_department.name if c.assigned_department else "Unassigned"
            sla_status = "BREACHED" if (c.sla_record and c.sla_record.is_breached) else "ON_TRACK"
            date_str = c.created_at.strftime("%Y-%m-%d %H:%M") if c.created_at else ""
            
            writer.writerow([
                c.complaint_id, date_str, c.status.upper(), prio, score,
                cat_name, dept_name, c.ward or "", c.area or "", sla_status, c.reopen_count or 0
            ])
            
        return output.getvalue()

    def export_excel(self, db: Session) -> bytes:
        """Exports complete multi-tab analytical Excel workbook using xlsxwriter."""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Formats
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#1E293B', 'font_color': '#FFFFFF',
            'border': 1, 'align': 'center'
        })
        cell_format = workbook.add_format({'border': 1})
        num_format = workbook.add_format({'border': 1, 'num_format': '#,##0'})
        pct_format = workbook.add_format({'border': 1, 'num_format': '0.0%'})
        
        # --- TAB 1: ALL COMPLAINTS ---
        ws_all = workbook.add_worksheet("Complaints Registry")
        headers = ["Token ID", "Date", "Category", "Department", "Priority", "Score", "Status", "Ward", "SLA Breached"]
        for col, h in enumerate(headers):
            ws_all.write(0, col, h, header_format)
            ws_all.set_column(col, col, 16)
            
        complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
        for row, c in enumerate(complaints, start=1):
            prio = c.analysis.priority if c.analysis else "N/A"
            score = c.analysis.priority_score if c.analysis else 0
            cat_name = c.category.name if c.category else "General"
            dept_name = c.assigned_department.name if c.assigned_department else "N/A"
            date_str = c.created_at.strftime("%Y-%m-%d") if c.created_at else ""
            is_br = "YES" if (c.sla_record and c.sla_record.is_breached) else "NO"
            
            ws_all.write(row, 0, c.complaint_id, cell_format)
            ws_all.write(row, 1, date_str, cell_format)
            ws_all.write(row, 2, cat_name, cell_format)
            ws_all.write(row, 3, dept_name, cell_format)
            ws_all.write(row, 4, prio, cell_format)
            ws_all.write(row, 5, score, num_format)
            ws_all.write(row, 6, c.status.upper(), cell_format)
            ws_all.write(row, 7, c.ward or "General", cell_format)
            ws_all.write(row, 8, is_br, cell_format)
            
        # --- TAB 2: DEPARTMENT PERFORMANCE ---
        ws_dept = workbook.add_worksheet("Department KPIs")
        dept_headers = ["Department", "Total Grievances", "Resolved", "Pending", "SLA Compliance"]
        for col, h in enumerate(dept_headers):
            ws_dept.write(0, col, h, header_format)
            ws_dept.set_column(col, col, 20)
            
        depts = db.query(Department).all()
        for row, d in enumerate(depts, start=1):
            tot = db.query(Complaint).filter(Complaint.assigned_department_id == d.id).count()
            res = db.query(Complaint).filter(Complaint.assigned_department_id == d.id, Complaint.status.in_(["resolved", "closed"])).count()
            pend = tot - res
            br = db.query(SLARecord).join(Complaint).filter(Complaint.assigned_department_id == d.id, SLARecord.is_breached == True).count()
            comp_rate = ((tot - br) / tot) if tot > 0 else 1.0
            
            ws_dept.write(row, 0, d.name, cell_format)
            ws_dept.write(row, 1, tot, num_format)
            ws_dept.write(row, 2, res, num_format)
            ws_dept.write(row, 3, pend, num_format)
            ws_dept.write(row, 4, comp_rate, pct_format)
            
        workbook.close()
        return output.getvalue()

    def generate_pdf_dossier(self, db: Session) -> bytes:
        """Generates executive PDF municipal report with statistics using PyMuPDF."""
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)  # A4 size in points
        
        now_str = datetime.utcnow().strftime("%d %B %Y, %H:%M UTC")
        
        # Header banner
        page.draw_rect(fitz.Rect(36, 36, 559, 100), fill=(0.12, 0.16, 0.23), color=(0.12, 0.16, 0.23))
        page.insert_text(fitz.Point(50, 68), "SMARTCIVIC AI — EXECUTIVE GOVERNANCE DOSSIER", fontsize=15, color=(1, 1, 1))
        page.insert_text(fitz.Point(50, 88), f"Generated: {now_str} | Municipal Corporation Apex Command Center", fontsize=9, color=(0.8, 0.85, 0.9))
        
        # Aggregate metrics
        total = db.query(Complaint).count()
        critical = db.query(Complaint).join(ComplaintAnalysis).filter(ComplaintAnalysis.priority == "CRITICAL").count()
        resolved = db.query(Complaint).filter(Complaint.status.in_(["resolved", "closed"])).count()
        breached = db.query(SLARecord).filter(SLARecord.is_breached == True).count()
        comp_rate = round(((total - breached) / total) * 100, 1) if total > 0 else 100.0
        
        # Metric cards
        cards = [
            ("Total Grievances", str(total), (0.1, 0.5, 0.8)),
            ("Critical Life-Safety", str(critical), (0.85, 0.15, 0.15)),
            ("Resolved Complaints", str(resolved), (0.1, 0.7, 0.4)),
            ("SLA Compliance", f"{comp_rate}%", (0.3, 0.4, 0.8))
        ]
        
        y_card = 120
        for i, (title, val, col) in enumerate(cards):
            x0 = 36 + i * 133
            x1 = x0 + 125
            page.draw_rect(fitz.Rect(x0, y_card, x1, y_card + 65), fill=(0.96, 0.97, 0.98), color=(0.85, 0.88, 0.92))
            page.insert_text(fitz.Point(x0 + 10, y_card + 22), title, fontsize=8, color=(0.4, 0.45, 0.5))
            page.insert_text(fitz.Point(x0 + 10, y_card + 50), val, fontsize=18, color=col)
            
        # Section 1: Department Performance Table
        page.insert_text(fitz.Point(36, 215), "1. MUNICIPAL DEPARTMENT PERFORMANCE SUMMARY", fontsize=11, color=(0.1, 0.15, 0.25))
        page.draw_line(fitz.Point(36, 222), fitz.Point(559, 222), color=(0.7, 0.75, 0.8))
        
        table_top = 232
        page.insert_text(fitz.Point(40, table_top), "Department", fontsize=9, color=(0.3, 0.35, 0.4))
        page.insert_text(fitz.Point(230, table_top), "Total", fontsize=9, color=(0.3, 0.35, 0.4))
        page.insert_text(fitz.Point(310, table_top), "Resolved", fontsize=9, color=(0.3, 0.35, 0.4))
        page.insert_text(fitz.Point(400, table_top), "Pending", fontsize=9, color=(0.3, 0.35, 0.4))
        page.insert_text(fitz.Point(480, table_top), "Compliance", fontsize=9, color=(0.3, 0.35, 0.4))
        
        depts = db.query(Department).limit(8).all()
        y_row = table_top + 18
        for d in depts:
            tot = db.query(Complaint).filter(Complaint.assigned_department_id == d.id).count()
            res = db.query(Complaint).filter(Complaint.assigned_department_id == d.id, Complaint.status.in_(["resolved", "closed"])).count()
            br = db.query(SLARecord).join(Complaint).filter(Complaint.assigned_department_id == d.id, SLARecord.is_breached == True).count()
            c_rate = f"{round(((tot - br)/tot)*100, 1)}%" if tot > 0 else "100.0%"
            
            page.insert_text(fitz.Point(40, y_row), d.name[:28], fontsize=8, color=(0.1, 0.1, 0.1))
            page.insert_text(fitz.Point(235, y_row), str(tot), fontsize=8, color=(0.2, 0.2, 0.2))
            page.insert_text(fitz.Point(315, y_row), str(res), fontsize=8, color=(0.1, 0.6, 0.3))
            page.insert_text(fitz.Point(405, y_row), str(tot - res), fontsize=8, color=(0.8, 0.3, 0.1))
            page.insert_text(fitz.Point(485, y_row), c_rate, fontsize=8, color=(0.1, 0.3, 0.7))
            y_row += 16
            
        # Section 2: Recent Critical Emergency Grievances
        page.insert_text(fitz.Point(36, y_row + 20), "2. RECENT CRITICAL LIFE-SAFETY GRIEVANCES TABLED FOR INTERVENTION", fontsize=11, color=(0.1, 0.15, 0.25))
        page.draw_line(fitz.Point(36, y_row + 27), fitz.Point(559, y_row + 27), color=(0.7, 0.75, 0.8))
        
        crits = db.query(Complaint).join(ComplaintAnalysis).filter(
            ComplaintAnalysis.priority == "CRITICAL"
        ).order_by(Complaint.created_at.desc()).limit(6).all()
        
        y_crit = y_row + 45
        for c in crits:
            txt = c.complaint_text.replace("\n", " ")[:85] + "..."
            page.insert_text(fitz.Point(40, y_crit), f"• [{c.complaint_id}] {c.ward or 'General'}: {txt}", fontsize=8, color=(0.15, 0.15, 0.15))
            y_crit += 16
            
        # Footer
        page.insert_text(fitz.Point(36, 810), "CONFIDENTIAL & PROPRIETARY — MUNICIPAL GOVERNANCE INTELLIGENCE SYSTEM — SMARTCIVIC AI", fontsize=7, color=(0.5, 0.5, 0.5))
        
        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes
