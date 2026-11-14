
from sqlalchemy.orm import Session
from app.models import AuditLog


def create_audit_log(
    db: Session,
    ticket_id: int,
    action: str,
    old_value: str = None,
    new_value: str = None,
    performed_by: str = "System"
):
    log = AuditLog(
        ticket_id=ticket_id,
        action=action,
        old_value=old_value,
        new_value=new_value,
        performed_by=performed_by
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log

def get_ticket_audit_logs(db: Session, ticket_id: int):
    return (
        db.query(AuditLog)
        .filter(AuditLog.ticket_id == ticket_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )
