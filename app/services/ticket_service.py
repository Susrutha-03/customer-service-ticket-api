from app.audit_service import create_audit_log
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app import models, schemas

SLA_HOURS = {
    "Critical": 4,
    "High": 8,
    "Medium": 24,
    "Low": 48
}


def create_ticket(db: Session, ticket: schemas.TicketCreate):
    priority = ticket.priority

    hours = SLA_HOURS.get(priority, 24)
    sla_deadline = datetime.now() + timedelta(hours=hours)

    new_ticket = models.Ticket(
        **ticket.model_dump(),
        sla_due_at=sla_deadline
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    create_audit_log(
        db=db,
        ticket_id=new_ticket.id,
        action="Ticket Created",
        new_value=f"Priority: {priority}, Status: Open"
    )

    return new_ticket

def get_all_tickets(db: Session):
    return db.query(models.Ticket).all()


def get_ticket_by_id(db: Session, ticket_id: int):
    return (
        db.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
    )


def search_tickets(
    db: Session,
    keyword: str = None,
    status: str = None,
    priority: str = None
):
    query = db.query(models.Ticket)

    if keyword:
        search_text = f"%{keyword.strip()}%"
        query = query.filter(
            (models.Ticket.title.ilike(search_text)) |
            (models.Ticket.description.ilike(search_text)) |
            (models.Ticket.customer_name.ilike(search_text))
        )

    if status:
        query = query.filter(models.Ticket.status == status)

    if priority:
        query = query.filter(models.Ticket.priority == priority)

    return query.all()

def get_overdue_tickets(db: Session):
    current_time = datetime.now()

    return (
        db.query(models.Ticket)
        .filter(
            models.Ticket.sla_due_at < current_time,
            models.Ticket.status.notin_(["Resolved", "Closed"])
        )
        .all()
    )
