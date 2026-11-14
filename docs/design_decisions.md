
# Design Decisions

## 1. FastAPI
FastAPI was selected to build REST endpoints and provide interactive API documentation through Swagger UI.

## 2. SQLite
SQLite was selected as a lightweight database suitable for local development and demonstration.

## 3. SQLAlchemy
SQLAlchemy provides ORM-based database operations and separates database logic from API routes.

## 4. Pydantic
Pydantic validates incoming ticket data and rejects invalid input before processing.

## 5. Modular Architecture
The application separates routes, database models, schemas, and service logic to improve maintainability.

## 6. SLA Configuration
Project-defined SLA targets are based on ticket priority:

- Critical: 4 hours
- High: 8 hours
- Medium: 24 hours
- Low: 48 hours

## 7. Audit Logging
Audit records capture important ticket activities, including creation, assignment, priority updates, and status updates.

## 8. Testing Strategy
Pytest and an in-memory SQLite database are used to test API behavior without modifying the development database.

## 9. Current Limitations
- Authentication and authorization are not implemented.
- SQLite is intended for this demonstration, not high-concurrency production workloads.
- SLA targets are demonstration values.
- More extensive edge-case and integration testing is needed.

## 10. Future Improvements
- Add authentication and role-based access.
- Integrate PostgreSQL.
- Improve timezone handling.
- Add deployment and monitoring.
- Expand automated test coverage.
