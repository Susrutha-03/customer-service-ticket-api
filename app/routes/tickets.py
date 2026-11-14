
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.audit_service import get_ticket_audit_logs
from app.services import ticket_service
from app.services.assignment_service import assign_ticket
from app.services.update_service import (
    update_ticket_priority,
    update_ticket_status
)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("/", response_model=schemas.TicketResponse)
def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(get_db)
):
    return ticket_service.create_ticket(db, ticket)


@router.get("/search")
def search_tickets(
    keyword: str = None,
    status: str = None,
    priority: str = None,
    db: Session = Depends(get_db)
):
    return ticket_service.search_tickets(
        db, keyword, status, priority
    )


@router.get("/", response_model=list[schemas.TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    return ticket_service.get_all_tickets(db)


@router.get("/overdue")
def get_overdue_tickets(db: Session = Depends(get_db)):
    return ticket_service.get_overdue_tickets(db)


@router.get("/{ticket_id}", response_model=schemas.TicketResponse)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = ticket_service.get_ticket_by_id(db, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket


@router.put("/{ticket_id}/assign", response_model=schemas.TicketResponse)
def update_ticket_assignment(
    ticket_id: int,
    employee_name: str,
    db: Session = Depends(get_db)
):
    return assign_ticket(db, ticket_id, employee_name)


@router.put("/{ticket_id}/priority", response_model=schemas.TicketResponse)
def change_ticket_priority(
    ticket_id: int,
    priority: str,
    db: Session = Depends(get_db)
):
    return update_ticket_priority(db, ticket_id, priority)


@router.put("/{ticket_id}/status", response_model=schemas.TicketResponse)
def change_ticket_status(
    ticket_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    return update_ticket_status(db, ticket_id, status)


@router.get("/{ticket_id}/audit")
def get_ticket_audit_history(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    return get_ticket_audit_logs(db, ticket_id)
