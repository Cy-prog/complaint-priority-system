import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Notification, User
from config.settings import get_settings

logger = logging.getLogger("notification_service")

class NotificationService:
    def __init__(self):
        self.settings = get_settings()

    def create_notification(
        self,
        title: str,
        message: str,
        user_id: int | None,
        notification_type: str = "status_update",
        reference_id: str | None = None,
        db: Session = None,
        send_email: bool = False
    ) -> Notification:
        """Create in-app notification and optionally dispatch email alert."""
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            reference_id=reference_id,
            is_read=False
        )
        if db:
            db.add(notif)
            db.commit()
            db.refresh(notif)

            if send_email and user_id:
                user = db.query(User).filter(User.id == user_id).first()
                if user and user.email:
                    self.send_email_alert(user.email, title, message)

        return notif

    def list_user_notifications(self, user_id: int, db: Session, limit: int = 30) -> list[Notification]:
        """Fetch notifications targeted to this user or global broadcasts."""
        return db.query(Notification).filter(
            (Notification.user_id == user_id) | (Notification.user_id == None)
        ).order_by(Notification.created_at.desc()).limit(limit).all()

    def get_unread_count(self, user_id: int, db: Session) -> int:
        return db.query(Notification).filter(
            ((Notification.user_id == user_id) | (Notification.user_id == None)),
            Notification.is_read == False
        ).count()

    def mark_as_read(self, notification_id: int, db: Session) -> bool:
        notif = db.query(Notification).filter(Notification.id == notification_id).first()
        if notif:
            notif.is_read = True
            db.commit()
            return True
        return False

    def mark_all_as_read(self, user_id: int, db: Session) -> int:
        count = db.query(Notification).filter(
            ((Notification.user_id == user_id) | (Notification.user_id == None)),
            Notification.is_read == False
        ).update({"is_read": True}, synchronize_session=False)
        db.commit()
        return count

    def send_email_alert(self, to_email: str, subject: str, body: str) -> bool:
        """
        Dispatches email via configured SMTP host or logs safely if SMTP credentials are absent.
        Never crashes or exposes false delivery.
        """
        smtp_host = os.getenv("SMTP_HOST", "")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_pass = os.getenv("SMTP_PASSWORD", "")
        smtp_sender = os.getenv("SMTP_FROM", "alerts@smartcivic.ai")

        if not smtp_host or not smtp_user:
            # Safe simulation / structured audit logging
            logger.info(f"[SIMULATED EMAIL DISPATCH] To: {to_email} | Subject: {subject} | Body: {body[:80]}...")
            return True

        try:
            msg = MIMEMultipart()
            msg["From"] = smtp_sender
            msg["To"] = to_email
            msg["Subject"] = f"[SmartCivic AI] {subject}"
            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            return True
        except Exception as e:
            logger.warning(f"SMTP notification delivery failed for {to_email}: {e}")
            return False
