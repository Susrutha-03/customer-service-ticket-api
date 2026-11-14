
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Ticket
from app.audit_service import create_audit_log


ALLOWED_PRIORITIES = ["Low", "Medium", "High", "Critical"]

ALLOWED_STATUSES = [
    "Open",
    "In Progress",
    "Resolved",
    "Closed"
]


def update_ticket_priority(
    db: Session,
    ticket_id: int,
    priority: str
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if priority not in ALLOWED_PRIORITIES:
        raise HTTPException(
            status_code=400,
            detail="Invalid priority"
        )

    old_value = ticket.priority
    ticket.priority = priority

    db.commit()
    db.refresh(ticket)

    create_audit_log(
        db=db,
        ticket_id=ticket.id,
        action="Priority Updated",
        old_value=old_value,
        new_value=priority
    )

    return ticket


def update_ticket_status(
    db: Session,
    ticket_id: int,
    status: str
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    old_value = ticket.status
    ticket.status = status

    db.commit()
    db.refresh(ticket)

    create_audit_log(
        db=db,
        ticket_id=ticket.id,
        action="Status Updated",
        old_value=old_value,
        new_value=status
    )

    return ticket
