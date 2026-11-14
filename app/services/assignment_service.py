
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models import Ticket
from app.audit_service import create_audit_log


def assign_ticket(
    db: Session,
    ticket_id: int,
    employee_name: str
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if not employee_name or not employee_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Employee name cannot be empty"
        )

    old_value = ticket.assigned_to
    new_value = employee_name.strip()

    ticket.assigned_to = new_value
    db.commit()
    db.refresh(ticket)

    create_audit_log(
        db=db,
        ticket_id=ticket.id,
        action="Ticket Assigned",
        old_value=old_value,
        new_value=new_value
    )

    return ticket
