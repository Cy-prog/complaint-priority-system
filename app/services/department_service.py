from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Department, User, Complaint, Category, SLARecord, ComplaintStatusHistory, AuditLog
from app.core.exceptions import ComplaintNotFoundError

class DepartmentService:
    def list_departments(self, db: Session, active_only: bool = False) -> list[Department]:
        query = db.query(Department)
        if active_only:
            query = query.filter(Department.is_active == True)
        return query.order_by(Department.name.asc()).all()

    def get_department(self, department_id: int, db: Session) -> Department | None:
        return db.query(Department).filter(Department.id == department_id).first()

    def get_department_by_name(self, name: str, db: Session) -> Department | None:
        return db.query(Department).filter(Department.name.ilike(f"%{name}%")).first()

    def create_department(self, name: str, description: str, contact_email: str, db: Session) -> Department:
        dept = Department(
            name=name.strip(),
            description=description.strip() if description else None,
            contact_email=contact_email.strip() if contact_email else None,
            is_active=True
        )
        db.add(dept)
        db.commit()
        db.refresh(dept)
        return dept

    def list_department_officers(self, department_id: int, db: Session) -> list[User]:
        return db.query(User).filter(
            User.department_id == department_id,
            User.is_active == True
        ).all()

    def get_officer_workload(self, officer_id: int, db: Session) -> dict:
        """Computes live active load, completed tasks, and SLA performance for an officer."""
        officer = db.query(User).filter(User.id == officer_id).first()
        if not officer:
            return {}

        total_assigned = db.query(Complaint).filter(Complaint.assigned_user_id == officer_id).count()
        active_complaints = db.query(Complaint).filter(
            Complaint.assigned_user_id == officer_id,
            Complaint.status.in_(["open", "in_progress", "pending"])
        ).count()
        resolved_count = db.query(Complaint).filter(
            Complaint.assigned_user_id == officer_id,
            Complaint.status.in_(["resolved", "closed"])
        ).count()

        # SLA compliance for officer's resolved complaints
        sla_query = db.query(SLARecord).join(Complaint, SLARecord.complaint_id == Complaint.id).filter(
            Complaint.assigned_user_id == officer_id
        )
        total_slas = sla_query.count()
        breached_slas = sla_query.filter(SLARecord.is_breached == True).count()
        sla_rate = round(((total_slas - breached_slas) / total_slas) * 100, 1) if total_slas > 0 else 100.0

        capacity_limit = 15
        cap_pct = min(100, round((active_complaints / capacity_limit) * 100))
        status_label = "Available" if active_complaints < 5 else ("Busy" if active_complaints < 12 else "Overloaded")

        return {
            "officer_id": officer.id,
            "id": officer.id,
            "name": officer.full_name or officer.username,
            "username": officer.username,
            "full_name": officer.full_name or officer.username,
            "email": officer.email,
            "role": officer.role,
            "phone": officer.phone,
            "total_assigned": total_assigned,
            "active_complaints": active_complaints,
            "resolved_count": resolved_count,
            "capacity_limit": capacity_limit,
            "capacity_percentage": cap_pct,
            "status": status_label,
            "sla_compliance_percent": sla_rate,
            "capacity_status": "HIGH_LOAD" if active_complaints >= 10 else ("MODERATE" if active_complaints >= 5 else "OPTIMAL")
        }

    def recommend_assignment(self, complaint_id: str, db: Session) -> dict:
        """
        AI & Load-Balanced Assignment Recommendation:
        1. Identifies department from category metadata or complaint analysis.
        2. Queries active department officers.
        3. Ranks officers by lowest current active workload.
        """
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")

        # 1. Determine recommended department
        recommended_dept = None
        if complaint.category and complaint.category.department:
            recommended_dept = complaint.category.department
        elif complaint.assigned_department:
            recommended_dept = complaint.assigned_department
        else:
            # Fallback based on text heuristics
            text_lower = complaint.complaint_text.lower()
            if any(k in text_lower for k in ["water", "पानी", "नल", "leakage", "pipeline"]):
                recommended_dept = self.get_department_by_name("Water", db)
            elif any(k in text_lower for k in ["electric", "बिजली", "wire", "pole", "transformer", "power"]):
                recommended_dept = self.get_department_by_name("Electricity", db)
            elif any(k in text_lower for k in ["sewer", "drain", "नाली", "सीवर", "garbage", "कचरा", "सफाई"]):
                recommended_dept = self.get_department_by_name("Sanitation", db)
            elif any(k in text_lower for k in ["road", "pothole", "सड़क", "गड्ढा"]):
                recommended_dept = self.get_department_by_name("Public Works", db)
            else:
                recommended_dept = db.query(Department).first()

        if not recommended_dept:
            return {"recommended_department": None, "recommended_officer": None, "reason": "No department registered."}

        # 2. Find least loaded officer in department
        officers = self.list_department_officers(recommended_dept.id, db)
        if not officers:
            # Check all officers if department has none
            officers = db.query(User).filter(User.role.in_(["officer", "operator"]), User.is_active == True).all()

        recommended_officer = None
        lowest_load = 999999
        officer_workloads = []

        for off in officers:
            w = self.get_officer_workload(off.id, db)
            officer_workloads.append(w)
            if w["active_complaints"] < lowest_load:
                lowest_load = w["active_complaints"]
                recommended_officer = off

        return {
            "recommended_department_id": recommended_dept.id,
            "recommended_department_name": recommended_dept.name,
            "recommended_officer_id": recommended_officer.id if recommended_officer else None,
            "recommended_officer_name": recommended_officer.full_name if recommended_officer else None,
            "officer_active_load": lowest_load if recommended_officer else 0,
            "available_officers_count": len(officers),
            "assignment_rationale": f"Routed to {recommended_dept.name} based on civic category mapping. "
                                   f"Officer {recommended_officer.full_name if recommended_officer else 'General Queue'} "
                                   f"recommended with lowest active workload ({lowest_load} active tasks)."
        }

    def assign_complaint(
        self,
        complaint_id: str,
        department_id: int | None,
        officer_id: int | None,
        assigned_by_user_id: int,
        notes: str | None,
        db: Session
    ) -> Complaint:
        """Executes manual or automated reassignment with full audit logging."""
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            raise ComplaintNotFoundError(f"Complaint {complaint_id} not found")

        old_dept_id = complaint.assigned_department_id
        old_user_id = complaint.assigned_user_id

        if department_id is not None:
            complaint.assigned_department_id = department_id
        if officer_id is not None:
            complaint.assigned_user_id = officer_id

        # Update status if pending
        if complaint.status == "pending":
            complaint.status = "open"

        # Audit status history
        history = ComplaintStatusHistory(
            complaint_id=complaint.id,
            old_status=complaint.status,
            new_status=complaint.status,
            changed_by_user_id=assigned_by_user_id,
            notes=f"Reassigned: Department [{old_dept_id} -> {department_id}], Officer [{old_user_id} -> {officer_id}]. {notes or ''}".strip()
        )
        db.add(history)

        # Audit log
        audit = AuditLog(
            user_id=assigned_by_user_id,
            action="ASSIGNMENT_CHANGE",
            resource_type="complaint",
            resource_id=complaint.id,
            old_value={"department_id": old_dept_id, "officer_id": old_user_id},
            new_value={"department_id": complaint.assigned_department_id, "officer_id": complaint.assigned_user_id}
        )
        db.add(audit)

        # Send notification to assigned officer
        if officer_id:
            from app.services.notification_service import NotificationService
            NotificationService().create_notification(
                title=f"New Grievance Assigned: #{complaint.complaint_id}",
                message=f"You have been assigned complaint #{complaint.complaint_id} in {complaint.ward or 'General Ward'}. Text: {complaint.complaint_text[:90]}...",
                user_id=officer_id,
                notification_type="assignment",
                reference_id=complaint.complaint_id,
                db=db,
                send_email=True
            )

        db.commit()
        db.refresh(complaint)
        return complaint
