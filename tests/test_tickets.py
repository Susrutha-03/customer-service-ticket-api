
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Create a separate in-memory test database
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "Running successfully"


def test_create_ticket(client):
    ticket_data = {
        "title": "Login Issue",
        "description": "Unable to login to my account",
        "customer_name": "Test Customer",
        "priority": "High"
    }

    response = client.post("/tickets/", json=ticket_data)

    assert response.status_code == 200
    assert response.json()["title"] == "Login Issue"
    assert response.json()["priority"] == "High"
    assert response.json()["status"] == "Open"
    assert response.json()["sla_due_at"] is not None


def test_invalid_ticket(client):
    ticket_data = {
        "title": "AB",
        "description": "Test issue",
        "customer_name": "Test Customer",
        "priority": "Urgent"
    }

    response = client.post("/tickets/", json=ticket_data)

    assert response.status_code == 422


def test_get_all_tickets(client):
    response = client.get("/tickets/")
    assert response.status_code == 200
    assert response.json() == []


def test_ticket_not_found(client):
    response = client.get("/tickets/9999")
    assert response.status_code == 404
    

def test_assign_ticket(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Network Issue",
            "description": "Internet is not working",
            "customer_name": "Test Customer",
            "priority": "Medium"
        }
    )
    ticket_id = create_response.json()["id"]

    response = client.put(
        f"/tickets/{ticket_id}/assign",
        params={"employee_name": "John"}
    )

    assert response.status_code == 200


def test_update_priority(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Payment Issue",
            "description": "Payment failed",
            "customer_name": "Test Customer",
            "priority": "Medium"
        }
    )
    ticket_id = create_response.json()["id"]

    response = client.put(
        f"/tickets/{ticket_id}/priority",
        params={"priority": "High"}
    )

    assert response.status_code == 200


def test_update_status(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Account Issue",
            "description": "Cannot access account",
            "customer_name": "Test Customer",
            "priority": "Low"
        }
    )
    ticket_id = create_response.json()["id"]

    response = client.put(
        f"/tickets/{ticket_id}/status",
        params={"status": "In Progress"}
    )

    assert response.status_code == 200


def test_audit_history(client):
    create_response = client.post(
        "/tickets/",
        json={
            "title": "Delivery Issue",
            "description": "Delivery is delayed",
            "customer_name": "Test Customer",
            "priority": "High"
        }
    )
    ticket_id = create_response.json()["id"]

    response = client.get(f"/tickets/{ticket_id}/audit")

    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["action"] == "Ticket Created"

