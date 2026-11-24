from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import SLARecord, Complaint, ComplaintAnalysis, ComplaintStatusHistory, Department, User, AuditLog
from app.core.config_loader import load_priority_config

class SLAService:
    def create_sla_record(self, complaint_id: int, priority: str, db: Session) -> SLARecord:
        priority_config = load_priority_config()
        sla_hours = 48
        
        if hasattr(priority_config, 'sla_policies') and priority in priority_config.sla_policies:
            sla_hours = priority_config.sla_policies[priority].resolution_hours
        elif isinstance(priority_config, dict) and "sla_policies" in priority_config:
            policy = priority_config["sla_policies"].get(priority, {})
            sla_hours = policy.get("resolution_hours", 48)
                
        deadline = datetime.utcnow() + timedelta(hours=sla_hours)
        
        sla = SLARecord(
            complaint_id=complaint_id,
            priority=priority,
            sla_deadline=deadline,
            is_breached=False
        )
        db.add(sla)
        db.commit()
        db.refresh(sla)
        return sla

    def check_and_escalate_slas(self, db: Session) -> dict:
        """
        Automatic Overdue Detection and Escalation Engine:
        1. Identifies overdue complaints (deadline < now and not resolved).
        2. Marks is_breached = True.
        3. If unescalated, escalates priority by 1 step up to CRITICAL.
        4. Dispatches emergency notifications and records audit logs.
        """
        now = datetime.utcnow()
        overdue_slas = db.query(SLARecord).join(Complaint).filter(
            Complaint.status.in_(["pending", "open", "in_progress"]),
            SLARecord.resolved_at == None,
            SLARecord.sla_deadline < now
        ).all()

        breached_count = 0
        escalated_count = 0
        escalation_events = []

        from app.services.notification_service import NotificationService
        notif_service = NotificationService()

        prio_order = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

        for sla in overdue_slas:
            if not sla.is_breached:
                sla.is_breached = True
                breached_count += 1

            complaint = sla.complaint
            if not complaint:
                continue

            curr_prio = (sla.priority or "MEDIUM").upper()
            curr_idx = prio_order.index(curr_prio) if curr_prio in prio_order else 1

            # Auto-escalate if not yet at apex CRITICAL
            if curr_idx < len(prio_order) - 1:
                new_prio = prio_order[curr_idx + 1]
                sla.priority = new_prio

                if complaint.analysis:
                    complaint.analysis.priority = new_prio
                    complaint.analysis.priority_score = min(complaint.analysis.priority_score + 20, 100)

                # History log
                history = ComplaintStatusHistory(
                    complaint_id=complaint.id,
                    old_status=complaint.status,
                    new_status=complaint.status,
                    changed_by_user_id=1,
                    notes=f"AUTOMATED SLA BREACH ESCALATION: Priority escalated from {curr_prio} to {new_prio}. Deadline was {sla.sla_deadline}."
                )
                db.add(history)

                # Audit log
                audit = AuditLog(
                    action="SLA_BREACH_ESCALATION",
                    resource_type="complaint",
                    resource_id=complaint.id,
                    old_value={"priority": curr_prio},
                    new_value={"priority": new_prio}
                )
                db.add(audit)

                # Send emergency notifications to supervisor and assigned officer
                dept_name = complaint.assigned_department.name if complaint.assigned_department else "Municipal Services"
                notif_msg = (
                    f"CRITICAL SLA BREACH: Complaint #{complaint.complaint_id} in {complaint.ward or 'General Area'} "
                    f"breached resolution deadline. Auto-escalated to {new_prio}."
                )
                notif_service.create_notification(
                    title=f"⚠️ SLA Breach: #{complaint.complaint_id}",
                    message=notif_msg,
                    user_id=complaint.assigned_user_id,
                    notification_type="sla_warning",
                    reference_id=complaint.complaint_id,
                    db=db,
                    send_email=True
                )

                escalated_count += 1
                escalation_events.append({
                    "complaint_id": complaint.complaint_id,
                    "old_priority": curr_prio,
                    "new_priority": new_prio,
                    "deadline": str(sla.sla_deadline)
                })

        db.commit()
        return {
            "overdue_detected": len(overdue_slas),
            "newly_breached": breached_count,
            "escalated_count": escalated_count,
            "events": escalation_events
        }

    def get_sla_status(self, complaint_id: str, db: Session) -> dict:
        complaint = db.query(Complaint).filter(Complaint.complaint_id == complaint_id).first()
        if not complaint:
            return {}
            
        sla = db.query(SLARecord).filter(SLARecord.complaint_id == complaint.id).first()
        if not sla:
            return {}
            
        now = datetime.utcnow()
        remaining = sla.sla_deadline - now if not sla.resolved_at else timedelta(0)
        
        base_time = complaint.created_at or (sla.sla_deadline - timedelta(hours=48))
        total_allowed = (sla.sla_deadline - base_time).total_seconds()
        remaining_seconds = remaining.total_seconds()
        
        is_approaching = False
        if remaining_seconds > 0 and total_allowed > 0:
            if (remaining_seconds / total_allowed) < 0.25:
                is_approaching = True

        pct_elapsed = 100.0
        if total_allowed > 0:
            elapsed = (now - base_time).total_seconds() if not sla.resolved_at else (sla.resolved_at - base_time).total_seconds()
            pct_elapsed = min(max(round((elapsed / total_allowed) * 100, 1), 0), 100)
                
        return {
            "deadline": sla.sla_deadline,
            "remaining_time_minutes": round(remaining_seconds / 60, 1),
            "remaining_hours": round(remaining_seconds / 3600, 1),
            "percent_elapsed": pct_elapsed,
            "is_breached": sla.is_breached or (remaining_seconds < 0 and not sla.resolved_at),
            "is_approaching": is_approaching,
            "resolved_at": sla.resolved_at,
            "response_time_minutes": sla.response_time_minutes,
            "resolution_time_minutes": sla.resolution_time_minutes
        }

    def get_department_sla_metrics(self, department_id: int, db: Session) -> dict:
        total = db.query(Complaint).filter(Complaint.assigned_department_id == department_id).count()
        if total == 0:
            return {
                "total_complaints": 0,
                "resolved_count": 0,
                "breached_count": 0,
                "compliance_rate": 100.0,
                "avg_resolution_hours": 0.0
            }

        resolved_count = db.query(Complaint).filter(
            Complaint.assigned_department_id == department_id,
            Complaint.status.in_(["resolved", "closed"])
        ).count()

        breached_query = db.query(SLARecord).join(Complaint).filter(
            Complaint.assigned_department_id == department_id,
            SLARecord.is_breached == True
        )
        breached_count = breached_query.count()

        resolved_slas = db.query(SLARecord.resolution_time_minutes).join(Complaint).filter(
            Complaint.assigned_department_id == department_id,
            SLARecord.resolution_time_minutes != None
        ).all()

        avg_res_hours = 0.0
        if resolved_slas:
            avg_res_hours = round(sum(r[0] for r in resolved_slas) / len(resolved_slas) / 60.0, 1)

        compliance_rate = round(((total - breached_count) / total) * 100.0, 1) if total > 0 else 100.0

        return {
            "total_complaints": total,
            "resolved_count": resolved_count,
            "breached_count": breached_count,
            "compliance_rate": compliance_rate,
            "avg_resolution_hours": avg_res_hours
        }
